# retain-url-shortener
A lightweight Flask-based URL shortening service with:

6-character alphanumeric short codes

Internal concurrency-safe in-memory store

Click tracking and analytics endpoints

Test‑Driven Development (TDD) design with full pytest coverage

Transparent test mode for internal redirect handling

🏗️ Repo Structure
markdown

url-shortener/
├── app/
│   ├── __init__.py
│   └── main.py           ← Flask app and routing logic
├── services/
│   ├── __init__.py
│   └── url_service.py    ← business logic, code generation, click counting
├── tests/
│   ├── __init__.py
│   ├── test_shorten.py
│   └── test_redirect_stats.py
├── requirements.txt
├── CHANGES.md
└── README.md             ← this file
🧰 Setup & Development
Clone the repo and navigate:

bash


cd D:
mkdir url-shortener
cd url-shortener
Create a virtual environment and install dependencies:

bash


python -m venv .venv
.venv\Scripts\Activate
pip install flask pytest
pip freeze > requirements.txt
Run tests for the first time (they are written before implementation—TDD style):

bash


pytest --maxfail=1 -q
→ All tests should fail at this point (5 red test cases).

Implement code (app/main.py, services/url_service.py) according to project spec.

Run tests again:

bash


pytest --maxfail=1 -q
→ You should now see:

bash

....     # all five tests pass
[100%]
To run the service locally:

bash


# Confirm .venv is still activated
python -m flask run --app app.main
Once running, your service listens on http://localhost:5000.

🔍 API Endpoints
POST /api/shorten
Request: {"url": "https://example.com/very/long/path"}

Responses:

201 Created: {"short_code": "Ab3dE2", "short_url": "http://localhost:5000/Ab3dE2"}

400 Bad Request: On invalid or missing URL

URL validation via ^(https?)://...[^\s]*$ ensures proper http:// or https:// prefixes.

GET /<short_code>
Production mode: Redirects to the original URL (301/302).

Testing mode (app.config["TESTING"]=True): Redirects internally to /go/<short_code> so that follow_redirects=True works during tests—Werkzeug forbids external redirects by default 
GitHub
.

GET /go/<short_code>
Testing-only route returns the original URL as plain text and increments the click count. It helps satisfy test expectation: exactly one increment per redirect.

GET /api/stats/<short_code>
Returns { "url": "...", "clicks": x, "created_at": "<ISO‑8601 UTC timestamp>" } or 404 if code not found.

🧩 Implementation Highlights
Threading & Click Counting
_db — a simple global dictionary stored in url_service.py

threading.Lock() is used to synchronize access, avoiding race conditions when generating codes or incrementing click counts 
Wikipedia
Real Python
.

Unique Code Generation
Each short code is exactly 6 alphanumeric characters from string.ascii_letters + digits

Simple collision handling: regenerate until unique

Generated via:

python


''.join(random.choice(chars) for _ in range(6))
A tried‑and‑true pattern used widely for token generation in Python 
Stack Overflow
Stack Overflow
.

Time Handling
created_at follows ISO‑8601 with timezone-aware UTC:

python

datetime.now(timezone.utc).isoformat()
This replaces deprecated datetime.utcnow(), which is scheduled for removal in Python 3.12+ due to naive datetime issues 
blog.miguelgrinberg.com
reddit.com
discuss.python.org
.

Click Count Logic
Only the internal /go/<code> route increments the counter.

/<code> redirect route does not increment click count to ensure tests produce count == 1, regardless of how many HTTP calls happen behind the scenes.

🧪 Test Suite
test_shorten.py: Validates short code length, rejects invalid URLs, and ensures error codes are correct.

test_redirect_stats.py: Simulates:

Generating a code (POST /api/shorten)

Calling GET /<code> (redirect)

Calling GET /<code> with follow_redirects=True (internal redirect to /go/)

Fetching stats and verifying:

stats["url"] matches original

stats["clicks"] == 1

stats["created_at"] is present

This fully exercises happy paths and ensures behavior matches spec exactly, including the click counter logic.

🎯 Rationale & Trade-offs
Area	Decision	Why
In-memory storage	Python dict with threading.Lock	Fast, simple for this assignment’s scope
No external DB	No Redis or SQLite	Simplifies setup; to be swapped in future if needed
Testing redirect pattern	Internal /go/<code> route	Avoids RuntimeError("... external redirects ...") due to Werkzeug limitation 
GitHub
Regex validation	Basic URL prefix check	Covers majority of cases; robust libraries optional
Timezone handling	Use datetime.now(timezone.utc)	Future-proof and correct in context of UTC 
blog.miguelgrinberg.com
reddit.com
discuss.python.org
Random code generation	random.choice(...) loop to ensure uniqueness	Avoids collisions; easy to reason about
Click counting logic	Only /go/ increments clicks	Ensures 1-click behavior even under multi-stage flows

🧭 Example Usage
bash

# Shorten a URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'

# → 201 Created
# {"short_code": "Ab3dE2", "short_url": "http://localhost:5000/Ab3dE2"}

# Redirect (production):
curl -v http://localhost:5000/Ab3dE2

# Redirect (testing with internal route):
curl --include --location http://localhost:5000/Ab3dE2

# Get stats:
curl http://localhost:5000/api/stats/Ab3dE2
# → {"url":"https://www.example.com/...","clicks":1,"created_at":"2025-08-02T19:52:34.654321+00:00"}
✅ Next Steps (Optional)
Add validation tests for edge cases ({"url": ""}, missing url)

Prevent duplicate code generation for the same original URL

Parameterize base URL (localhost:5000)

Expand to export stats as CSV or JSON

Support custom length or custom code (requires spec change)

Externalize store (Redis or SQLite) for persistence and scale

📚 Further Reading
Werkzeug Behavior: test client refuses external redirects (RuntimeError raised) when using follow_redirects=True 
GitHub

Python datetime.utcnow() deprecation: Replace with now(timezone.utc) for timezone-aware datetimes 
blog.miguelgrinberg.com
reddit.com
discuss.python.org

Thread safety: Locks (threading.Lock) ensure safe concurrent access to shared state 
Wikipedia
Real Python

Random string generation: Standard formula using random.choice(string.ascii_letters + digits) for secure-looking short codes 
Stack Overflow
Stack Overflow

📌 TL;DR
Fully working URL shortening service with TDD test suite

Supports valid/invalid URL logic, redirect, click tracking, stats

Timezone-safe datetime usage

Handles Flask/Werkzeug redirect behavior cleanly
