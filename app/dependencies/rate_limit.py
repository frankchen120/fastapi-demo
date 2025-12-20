import time 
from fastapi import Request 
from fastapi import Depends
from app.core.exceptions import TooManyRequestsError

#in-memory store
_rate_limit_store: dict[str, list[float]] = {}

def rate_limit(
    limit: int,
    window_seconds: int
):
    def _checker(request: Request):
        ip = request.client.host
        key = f"{ip}:{request.url.path}"
        now = time.time()
        
        timestamps = _rate_limit_store.get(key, [])
        timestamps = [t for t in timestamps if now - t < window_seconds]
        
        if len(timestamps) >= limit:
            raise TooManyRequestsError("too many requests")
        
        timestamps.append(now)
        _rate_limit_store[key] = timestamps
    return _checker
    
