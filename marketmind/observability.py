"""Structured logging and request tracing for MarketMind."""

from __future__ import annotations

import json
import logging
import logging.handlers
import re
import sys
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class APIKeyMaskingFilter(logging.Filter):
    """Mask API keys in log messages."""
    _KEY_PATTERN = re.compile(r"(sk-[a-zA-Z0-9]{6})[a-zA-Z0-9]+")

    def filter(self, record: logging.LogRecord) -> bool:
        if hasattr(record, 'msg') and isinstance(record.msg, str):
            record.msg = self._KEY_PATTERN.sub(r"\1****", record.msg)
        return True


class JSONFormatter(logging.Formatter):
    """Structured JSON log formatter."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        if hasattr(record, "stage"):
            log_entry["stage"] = record.stage
        if hasattr(record, "data"):
            log_entry["data"] = record.data
        return json.dumps(log_entry, ensure_ascii=False, default=str)


def setup_logger(name: str = "marketmind", level: str = "INFO", log_dir: Optional[Path] = None, debug: bool = False) -> logging.Logger:
    """Configure application logger with JSON formatting."""
    logger = logging.getLogger(name)

    # In debug mode, force DEBUG level regardless of config
    effective_level = "DEBUG" if debug else level
    logger.setLevel(getattr(logging, effective_level.upper(), logging.INFO))

    if logger.handlers:
        return logger

    logger.addFilter(APIKeyMaskingFilter())

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(JSONFormatter())
    logger.addHandler(console)

    # Error handler to stderr
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(JSONFormatter())
    stderr_handler.setLevel(logging.ERROR)
    logger.addHandler(stderr_handler)

    # File handler
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        fh = logging.handlers.TimedRotatingFileHandler(
            log_dir / "app.log", when="D", interval=1, backupCount=7, encoding="utf-8"
        )
        fh.setFormatter(JSONFormatter())
        logger.addHandler(fh)

        # LLM calls log
        llm_handler = logging.FileHandler(log_dir / "llm_calls.log", encoding="utf-8")
        llm_handler.setFormatter(JSONFormatter())
        llm_handler.addFilter(lambda record: "LLM call" in record.getMessage())
        logger.addHandler(llm_handler)

        # Errors log
        error_handler = logging.FileHandler(log_dir / "errors.log", encoding="utf-8")
        error_handler.setFormatter(JSONFormatter())
        error_handler.setLevel(logging.ERROR)
        logger.addHandler(error_handler)

    return logger


@dataclass
class StageTrace:
    name: str
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    status: str = "running"
    llm_calls: int = 0
    metadata: dict = field(default_factory=dict)

    def finish(self, status: str = "success") -> None:
        self.end_time = time.time()
        self.status = status

    @property
    def duration_seconds(self) -> float:
        end = self.end_time or time.time()
        return round(end - self.start_time, 3)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "duration_seconds": self.duration_seconds,
            "status": self.status,
            "llm_calls": self.llm_calls,
            "metadata": self.metadata,
        }


@dataclass
class RequestTrace:
    request_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    stages: list[StageTrace] = field(default_factory=list)
    total_llm_calls: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    final_status: str = "running"
    error_message: Optional[str] = None

    def start_stage(self, name: str) -> StageTrace:
        stage = StageTrace(name=name)
        self.stages.append(stage)
        return stage

    def finish(self, status: str = "success", error: Optional[str] = None) -> None:
        self.end_time = time.time()
        self.final_status = status
        self.error_message = error

    @property
    def duration_seconds(self) -> float:
        end = self.end_time or time.time()
        return round(end - self.start_time, 3)

    def to_dict(self) -> dict:
        return {
            "request_id": self.request_id,
            "duration_seconds": self.duration_seconds,
            "stages": [s.to_dict() for s in self.stages],
            "total_llm_calls": self.total_llm_calls,
            "total_tokens": self.total_tokens,
            "total_cost": round(self.total_cost, 6),
            "final_status": self.final_status,
            "error_message": self.error_message,
        }

    def save(self, log_dir: Path) -> None:
        traces_dir = log_dir / "traces"
        traces_dir.mkdir(parents=True, exist_ok=True)
        path = traces_dir / f"{self.request_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)


class MetricsCollector:
    """Simple in-memory metrics collector for PoC."""

    def __init__(self):
        self._counters: dict[str, int] = {}
        self._histograms: dict[str, list[float]] = {}

    def inc(self, name: str, labels: dict | None = None, value: int = 1) -> None:
        """Increment a counter metric."""
        key = self._make_key(name, labels)
        self._counters[key] = self._counters.get(key, 0) + value

    def observe(self, name: str, value: float, labels: dict | None = None) -> None:
        """Record a histogram observation."""
        key = self._make_key(name, labels)
        if key not in self._histograms:
            self._histograms[key] = []
        self._histograms[key].append(value)

    def _make_key(self, name: str, labels: dict | None = None) -> str:
        if not labels:
            return name
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

    def get_metrics(self) -> dict:
        """Return all collected metrics."""
        result = {}
        for key, value in self._counters.items():
            result[key] = {"type": "counter", "value": value}
        for key, values in self._histograms.items():
            result[key] = {
                "type": "histogram",
                "count": len(values),
                "sum": sum(values),
                "avg": sum(values) / len(values) if values else 0,
            }
        return result

    def reset(self) -> None:
        """Reset all metrics."""
        self._counters.clear()
        self._histograms.clear()


# Global metrics instance
metrics = MetricsCollector()


def save_eval_checkpoint(
    logs_dir: Path,
    request_id: str,
    checkpoint: str,
    input_data: dict,
    output_data: dict,
) -> None:
    """Save evaluation checkpoint for offline quality assessment."""
    evals_dir = logs_dir / "evals" / checkpoint
    evals_dir.mkdir(parents=True, exist_ok=True)

    eval_data = {
        "request_id": request_id,
        "checkpoint": checkpoint,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": input_data,
        "output": output_data,
    }

    eval_path = evals_dir / f"{request_id}.json"
    with open(eval_path, "w", encoding="utf-8") as f:
        json.dump(eval_data, f, ensure_ascii=False, indent=2, default=str)
