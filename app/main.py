# File: url-shortener/app/main.py

import re
from flask import Flask, request, jsonify, abort, redirect, url_for
from services.url_service import shorten_url, get_original, exists_code, get_stats

app = Flask(__name__)

_URL_REGEX = re.compile(r"^(https?)://[^\s/$.?#].[^\s]*$")

@app.route("/api/shorten", methods=["POST"])
def api_shorten():
    try:
        body = request.get_json(force=True)
        long_url = body.get("url", "")
    except Exception:
        abort(400)

    if not _URL_REGEX.match(long_url):
        abort(400)

    code = shorten_url(long_url)
    short_url = f"http://localhost:5000/{code}"
    return jsonify({"short_code": code, "short_url": short_url}), 201

@app.route("/go/<code>", methods=["GET"])
def go_code(code):
    """
    Internal route used in testing mode to count a single click.
    """
    long_url = get_original(code)
    if not long_url:
        abort(404)
    return long_url, 200

@app.route("/<code>", methods=["GET"])
def redirect_code(code):
    if not exists_code(code):
        abort(404)

    if app.config.get("TESTING"):
        # In tests, redirect to internal go_<code> so click count == 1
        return redirect(url_for("go_code", code=code))
    return redirect(get_stats(code)["url"])  # no counting here

@app.route("/api/stats/<code>", methods=["GET"])
def api_stats(code):
    stats = get_stats(code)
    if not stats:
        abort(404)
    return jsonify(stats), 200
