"""Tool execution wrapper with retry, timeout, fallback, and logging."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from marketmind.observability import metrics

logger = logging.getLogger("marketmind")


@dataclass
class ToolResult:
    success: bool
    data: Any
    fallback_used: bool = False
    latency_ms: int = 0
    error: Optional[str] = None


def execute_tool(
    tool_name: str,
    handler: Callable,
    params: dict,
    timeout_sec: int = 10,
    max_retries: int = 2,
    fallback_handler: Optional[Callable] = None,
) -> ToolResult:
    """Execute a tool with retry, timeout, and fallback logic."""
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            start = time.time()
            result = handler(**params)
            latency = int((time.time() - start) * 1000)

            logger.info(
                f"Tool '{tool_name}' succeeded",
                extra={"data": {"tool": tool_name, "attempt": attempt + 1, "latency_ms": latency}},
            )
            labels = {"tool": tool_name}
            metrics.inc("tool_calls_total", labels={**labels, "status": "success"})
            metrics.observe("tool_latency_seconds", (time.time() - start), labels=labels)
            if isinstance(result, list):
                metrics.observe("tool_results_count", len(result), labels=labels)
            return ToolResult(success=True, data=result, latency_ms=latency)

        except Exception as e:
            last_error = e
            logger.warning(
                f"Tool '{tool_name}' failed (attempt {attempt + 1}/{max_retries + 1}): {e}",
                extra={"data": {"tool": tool_name, "attempt": attempt + 1, "error": str(e)}},
            )
            if attempt < max_retries:
                time.sleep(min(2 ** attempt, 4))

    # All retries exhausted — use fallback
    if fallback_handler:
        try:
            start = time.time()
            fallback_data = fallback_handler(**params)
            latency = int((time.time() - start) * 1000)
            logger.info(f"Tool '{tool_name}' using fallback", extra={"data": {"tool": tool_name}})
            metrics.inc("tool_fallback_used", labels={"tool": tool_name})
            return ToolResult(success=False, data=fallback_data, fallback_used=True, latency_ms=latency, error=str(last_error))
        except Exception as fb_err:
            logger.error(f"Tool '{tool_name}' fallback also failed: {fb_err}")

    metrics.inc("tool_calls_total", labels={"tool": tool_name, "status": "error"})
    return ToolResult(success=False, data=None, error=str(last_error))
