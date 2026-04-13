"""LLM Client — wrapper over DeepSeek API with retries, cost tracking, and guardrails."""

from __future__ import annotations

import json
import logging
import time
from typing import Optional

from openai import OpenAI

from marketmind.config import LLMConfig
from marketmind.models import LLMResponse
from marketmind.observability import metrics

logger = logging.getLogger("marketmind")

# DeepSeek pricing per 1K tokens
PRICING = {
    "deepseek-chat": {"input": 0.0001, "output": 0.0002},
    "deepseek-reasoner": {"input": 0.0005, "output": 0.001},
}


class LLMBudgetExceededError(Exception):
    pass


class LLMTimeoutError(Exception):
    pass


class LLMRateLimitError(Exception):
    pass


class LLMResponseValidationError(Exception):
    pass


class LLMAuthError(Exception):
    pass


class LLMClient:
    """Wrapper over DeepSeek API (OpenAI-compatible) with guardrails."""

    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
        )
        # Session counters
        self._calls = 0
        self._total_tokens = 0
        self._total_cost = 0.0
        self._session_start: float | None = None
        self._cache: dict[str, LLMResponse] = {}

    def _cache_key(self, messages: list[dict], model: str, temperature: float) -> str:
        """Generate cache key from request parameters."""
        import hashlib
        content = f"{model}:{temperature}:" + str([(m.get('role',''), m.get('content','')) for m in messages])
        return hashlib.md5(content.encode()).hexdigest()

    def _check_guardrails(self) -> None:
        if self._calls >= self.config.max_calls_per_request:
            raise LLMBudgetExceededError(
                f"Max LLM calls exceeded: {self._calls}/{self.config.max_calls_per_request}"
            )
        if self._total_tokens >= self.config.max_tokens_per_request:
            raise LLMBudgetExceededError(
                f"Max tokens exceeded: {self._total_tokens}/{self.config.max_tokens_per_request}"
            )
        if self._total_cost >= self.config.max_cost_per_request:
            raise LLMBudgetExceededError(
                f"Max cost exceeded: ${self._total_cost:.4f}/${self.config.max_cost_per_request}"
            )
        if self._session_start and (time.time() - self._session_start) > self.config.max_duration_seconds:
            raise LLMBudgetExceededError(
                f"Max duration exceeded: {time.time() - self._session_start:.0f}s/{self.config.max_duration_seconds}s"
            )

    def _calc_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        pricing = PRICING.get(model, PRICING["deepseek-chat"])
        return (input_tokens / 1000) * pricing["input"] + (output_tokens / 1000) * pricing["output"]

    def call(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        response_format: Optional[str] = None,
        model_override: Optional[str] = None,
    ) -> LLMResponse:
        """Make an LLM call with retries and guardrails.

        Args:
            model_override: Use a specific model instead of the default.
                            Enables per-stage LLM routing.
        """
        self._check_guardrails()

        model = model_override or self.config.model

        cache_key = self._cache_key(messages, model, temperature)
        if cache_key in self._cache:
            logger.info("LLM cache hit", extra={"data": {"model": model, "cache_key": cache_key[:8]}})
            cached = self._cache[cache_key]
            self._calls += 1
            return cached

        kwargs: dict = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "timeout": self.config.timeout,
        }
        if response_format == "json":
            kwargs["response_format"] = {"type": "json_object"}

        last_error = None
        for attempt in range(self.config.max_retries + 1):
            try:
                start = time.time()
                response = self.client.chat.completions.create(**kwargs)
                latency_ms = int((time.time() - start) * 1000)

                usage = response.usage
                input_tokens = usage.prompt_tokens if usage else 0
                output_tokens = usage.completion_tokens if usage else 0
                cost = self._calc_cost(model, input_tokens, output_tokens)

                # Update counters
                self._calls += 1
                self._total_tokens += input_tokens + output_tokens
                self._total_cost += cost

                content = response.choices[0].message.content or ""

                logger.info(
                    "LLM call completed",
                    extra={
                        "data": {
                            "model": model,
                            "input_tokens": input_tokens,
                            "output_tokens": output_tokens,
                            "latency_ms": latency_ms,
                            "cost_usd": round(cost, 6),
                            "attempt": attempt + 1,
                            "call_id": f"{id(response):x}",
                            "success": True,
                            "retry_count": attempt,
                            "temperature": temperature,
                        }
                    },
                )

                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(
                        "LLM call details",
                        extra={
                            "data": {
                                "messages": [{"role": m["role"], "content": m["content"][:500]} for m in messages],
                                "response": content[:500],
                                "model": model,
                            }
                        },
                    )

                # Record metrics
                metrics.inc("llm_calls_total", labels={"model": model, "status": "success"})
                metrics.observe("llm_latency_seconds", (time.time() - start), labels={"model": model})
                metrics.observe("llm_tokens_total", input_tokens + output_tokens, labels={"model": model, "type": "total"})
                metrics.observe("llm_cost_usd_total", cost, labels={"model": model})

                self._cache[cache_key] = LLMResponse(
                    content=content,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    latency_ms=latency_ms,
                    cost_usd=cost,
                )

                return LLMResponse(
                    content=content,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    latency_ms=latency_ms,
                    cost_usd=cost,
                )

            except Exception as e:
                last_error = e
                err_str = str(e).lower()
                # Map to specific exception types
                if "timeout" in err_str or "timed out" in err_str:
                    last_error = LLMTimeoutError(str(e))
                elif "rate" in err_str and "limit" in err_str:
                    last_error = LLMRateLimitError(str(e))
                elif "auth" in err_str or "401" in err_str or "api key" in err_str:
                    last_error = LLMAuthError(str(e))
                    raise last_error  # Don't retry auth errors

                logger.warning(
                    f"LLM call failed (attempt {attempt + 1}): {e}",
                    extra={"data": {"attempt": attempt + 1, "error": str(e)}},
                )
                metrics.inc("llm_retries_total", labels={"model": model})
                if attempt < self.config.max_retries:
                    time.sleep(min(2 ** attempt, 4))

        metrics.inc("llm_calls_total", labels={"model": model, "status": "error"})
        metrics.inc("llm_errors_total", labels={"model": model, "error_type": type(last_error).__name__})
        raise last_error  # type: ignore[misc]

    def call_json(
        self,
        messages: list[dict],
        temperature: float = 0.3,
        max_tokens: int = 2048,
        model_override: Optional[str] = None,
        schema: Optional[type] = None,
    ) -> dict:
        """Make an LLM call expecting JSON response, with retry on parse failure.

        Args:
            schema: Optional Pydantic model class for response validation.
                    If provided, the parsed JSON is validated against this schema.
        """
        for attempt in range(2):
            resp = self.call(messages, temperature=temperature, max_tokens=max_tokens, response_format="json", model_override=model_override)
            try:
                data = json.loads(resp.content)
            except json.JSONDecodeError:
                if attempt == 0:
                    messages = messages + [
                        {"role": "assistant", "content": resp.content},
                        {
                            "role": "user",
                            "content": "Предыдущий ответ был невалидным JSON. Ответь СТРОГО в формате JSON, без текста до/после.",
                        },
                    ]
                    continue
                else:
                    raise

            # Validate against Pydantic schema if provided
            if schema is not None:
                try:
                    schema.model_validate(data)
                except Exception as e:
                    logger.warning(f"Schema validation failed: {e}")
                    if attempt == 0:
                        messages = messages + [
                            {"role": "assistant", "content": resp.content},
                            {
                                "role": "user",
                                "content": f"JSON не соответствует ожидаемой схеме: {e}. Исправь и верни валидный JSON.",
                            },
                        ]
                        continue
                    # On second attempt, return raw data even if schema fails
                    logger.warning("Schema validation failed on retry, returning raw data")

            return data

        return {}  # unreachable

    def get_usage_stats(self) -> dict:
        return {
            "calls": self._calls,
            "total_tokens": self._total_tokens,
            "total_cost": round(self._total_cost, 6),
        }

    def reset_session(self) -> None:
        self._calls = 0
        self._total_tokens = 0
        self._total_cost = 0.0
        self._session_start = time.time()
        self._cache.clear()
