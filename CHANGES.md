# Changelog

All notable changes to this project are documented in this file.

This changelog follows the guidelines from [Keep a Changelog] and Semantic Versioning.

## [Unreleased]

### Added
- Implement URL shortening endpoint `POST /api/shorten` with 6‑character alphanumeric code generation  
- Add redirect endpoint `GET /<short_code>` that performs HTTP 302 redirect  
- Track and store click counts in memory datastore and update on each redirect  
- Add analytics endpoint `GET /api/stats/<short_code>` returning original URL, click count, and ISO‑8601 timestamp  
- Validate submitted URLs; return HTTP 400 on invalid input  
- Include structured error handling and proper HTTP status codes (400, 404, etc.)  
- Build a suite of pytest tests covering core flows: shortening, redirection, stats, invalid input scenarios  

### Changed
- Refactored service code for clear separation between `app/main.py` and `services/url_service.py`.  
- Added `__init__.py` files in `app/`, `services/`, and `tests/` to support Python module imports  

### Removed
- Removed previously tracked compiled bytecode (`__pycache__/`, `.pyc`) and updated `.gitignore` accordingly  

## [1.0.0] – 2025-08-02

### Added
- Initial public release meeting Task 2 assignment requirements  
- README with setup instructions, API usage examples, tests guidelines  
- CHANGES.md documenting deliverables, progress, and tests status  

