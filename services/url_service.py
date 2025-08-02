# File: url-shortener/services/url_service.py
from datetime import datetime, timezone
import threading
import random
import string
from datetime import datetime

_lock = threading.Lock()
_db = {}

def _generate_code():
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(6))

def shorten_url(long_url: str) -> str:
    with _lock:
        while True:
            code = _generate_code()
            if code not in _db:
                break
    _db[code] = {
        "url": long_url,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "clicks": 0,
    }
    return code

def get_original(code: str) -> str | None:
    """
    Called only by /go/<code>: increments click count.
    """
    with _lock:
        entry = _db.get(code)
        if not entry:
            return None
        entry["clicks"] += 1
        return entry["url"]

def exists_code(code: str) -> bool:
    """
    Called by /<code> to check existence without incrementing.
    """
    with _lock:
        return code in _db

def get_stats(code: str) -> dict | None:
    with _lock:
        entry = _db.get(code)
        if not entry:
            return None
    return {
        "url": entry["url"],
        "clicks": entry["clicks"],
        "created_at": entry["created_at"],
    }
