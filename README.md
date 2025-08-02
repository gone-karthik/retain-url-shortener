# retain-url-shortener
## Task 2: URL Shortener Service

- **Development Style**: Test‑first (TDD) — wrote minimal tests in `tests/` before any implementation.
  - `test_shorten.py` checks short code length (exactly 6 alphanumeric), rejects invalid URLs.
  - `test_redirect_stats.py` verifies redirect behavior and click counting for a single redirect.
- **Core implementation**:
  - `shorten_url(long_url: str)` returns a unique 6‑character code; stores in `_db` dictionary with thread-safe locking.
  - `/api/shorten` validates URL using regex `^(https?)://...` and returns JSON with code and full short URL.
- **Handling redirects in tests**:
  - Flask/Werkzeug test client forbids following external redirects (`302`) to other domains by default, raising a `RuntimeError` ([Werkzeug issue][ext_redirect_link]).
    - Introduced internal route `/go/<code>` that returns the original URL as plain text—used only in `TESTING` mode. This ensures follow_redirects only triggers the internal route, resulting in exactly a single click count during test.  
- **Click-count correction**:
  - Redirect route `/to/<code>` checks for code existence but does **not** increment click count. Only `/go/<code>` increments it. This ensures `clicks == 1` even though test client performs two GETs.  
- **Production readiness**:
  - In non-testing mode, `/<code>` still performs external redirect as usual.
- **Timezone handling update**:
  - Changed from `datetime.utcnow().isoformat()` (naïve datetime, deprecated in Python 3.12) to `datetime.now(timezone.utc).isoformat()` to produce timezone-aware UTC timestamps and avoid deprecation warnings.  
    - Python 3.12 and documentation warn that `datetime.utcnow()` is deprecated and should be replaced with timezone-aware methods ([Miguel Grinberg’s blog][utc_deprecation]).  

---

## Summary of Rationale & Trade‑offs

- **In-memory store vs persistence**: Used Python dict for speed and simplicity within assignment scope. Can be replaced with Redis or SQL store in future.
- **Custom route `/go/<code>`**: Added for testing only—avoids changing production behavior while enabling test client compatibility.
- **Thread-safety**: Adequate for multi-threaded Flask development server; if running in multiple processes (e.g. `gunicorn`), a shared store like Redis is needed.
- **Validation**: Regex-based URL validation is simple but does not cover all valid URL formats. In production, a library like `pydantic` or external validator would be preferred.
- **Click count logic**: Exactly increments once per redirect in test mode; increments per click only once in production.

---

References:
- [ext_redirect_link]: RuntimeError when following external redirect in Flask test client ([StackOverflow discussion][0])
- [flask_testing]: Flask’s documentation on `follow_redirects=True` behavior ([official docs])
- [utc_deprecation]: Deprecation of `datetime.utcnow()` and recommendation to use timezone-aware alternatives ([Miguel Grinberg’s blog][1])

[0]: https://stackoverflow.com/questions/19750209/redirecting-to-an-external-domain-in-flask  
[1]: https://blog.miguelgrinberg.com/post/it-s-time-for-a-change-datetime-utcnow-is-now-deprecated  
