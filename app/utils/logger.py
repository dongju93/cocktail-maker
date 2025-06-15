import fcntl
from pathlib import Path
from typing import Any, Mapping, MutableMapping  # noqa: UP035

import orjson
import structlog


class Logger:
    """jsonl 포맷으로 로그 기록"""

    def __init__(self, log_file: str = "service.jsonl") -> None:
        """인스턴트 초기화"""
        self.log_path: Path = Path.cwd().parent / "log" / log_file
        self._init_log_file()

    def _init_log_file(self) -> None:
        """파일 생성"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.touch()

    def _format_and_write(
        self, logger: Any, name: str, event_dict: MutableMapping[str, Any]
    ) -> Mapping[str, Any]:
        """로그 포맷팅 및 내용 쓰기"""
        formatted_log: dict[str, Any] = {
            "timestamp": event_dict["timestamp"],
            "level": event_dict["level"],
            "event": event_dict["event"],
            "details": {
                k: v
                for k, v in event_dict.items()
                if k not in {"timestamp", "level", "event", "handler", "processor"}
            },
        }

        try:
            with open(self.log_path, "ab") as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)

                f.write(orjson.dumps(formatted_log))
                f.write(b"\n")

                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except Exception as e:
            print(f"Failed to write log: {e}")

        return event_dict

    def setup(self) -> structlog.BoundLogger:
        """로거 설정"""
        structlog.configure(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                self._format_and_write,
                structlog.processors.JSONRenderer(serializer=orjson.dumps),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger()
