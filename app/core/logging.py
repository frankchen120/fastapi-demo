import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        if record.levelno >= logging.ERROR:
            payload.update({
                "filename": record.filename,
                "function": record.funcName,
                "lineno": record.lineno,
            })

        # 把 extra 合併進去（我們 middleware 用 extra 放欄位）
        # logging 內建欄位很多，避免全倒進去，只拿我們需要的
        for key in ("request_id", "method", "path", "status_code", "duration_ms", "client_ip", "has_auth"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)

        return json.dumps(payload, ensure_ascii=False)

def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]
