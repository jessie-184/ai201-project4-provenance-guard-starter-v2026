#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import re
import time
import uuid

from flask import Flask, g, jsonify, request

import audit
import config
import detector
import scoring
import stylometry

app = Flask(__name__)


# ── Request timing — UNIT 9 capstone ─────────────────────────────────────────
# Registered BEFORE the rate limiter below, so this hook runs first and a 429
# is timed from the start of the request like everything else.

@app.before_request
def _start_timer():
    g.start = time.perf_counter()


def _request_fields(text=None):
    """
    What came in and how long it took. Added to every /submit log record —
    decisions, refusals and 429s — next to the nine original fields.
    """
    start = g.get("start")
    is_text = isinstance(text, str)
    return {
        "duration_ms": round((time.perf_counter() - start) * 1000, 1) if start else None,
        "text_chars": len(text) if is_text else None,
        "word_count": len(_REAL_WORD.findall(text)) if is_text else None,
        "text_excerpt": text[:config.LOG_EXCERPT_CHARS] if is_text else None,
    }


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
            **_request_fields(payload.get("text")),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


MAX_TEXT_CHARS = 10_000   # longer input is rejected before it reaches the model


def _reject(creator_id, reason, message, status=400, text=None):
    """Refuse a request, leave a trace in the audit log, and tell the caller why."""
    audit.log_rejection(creator_id=creator_id or "unknown", reason=reason,
                        **_request_fields(text))
    return jsonify({"error": reason, "message": message}), status


# ── Input gate — UNIT 9 capstone. Rules and numbers live in config.py ────────
_REAL_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
# ASCII control characters except tab, newline and carriage return (codes 0–8,
# 11, 12, 14–31 and 127). Nobody types these into writing.
_CONTROL_CHAR = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def _gate(text):
    """
    Can the signals meaningfully score this text? Returns None if yes, or
    (reason, message) if it should be refused before either signal runs.
    """
    # Checked first and on its own: one control character barely moves the
    # letter share, and Python treats some (0x0B, 0x0C, 0x1C–0x1F) as spaces.
    if _CONTROL_CHAR.search(text):
        return ("control_characters",
                "'text' contains control characters (such as null bytes or "
                "terminal escape codes), which don't belong in writing.")
    visible = [c for c in text if not c.isspace()]
    letters = sum(1 for c in visible if c.isascii() and c.isalpha())
    if letters / len(visible) < config.GATE_MIN_LETTER_SHARE:
        return ("not_english_text",
                "This service only scores English writing, and most of this "
                "text isn't English letters.")
    if len(_REAL_WORD.findall(text)) < config.GATE_MIN_WORDS:
        return ("too_few_words",
                f"'text' needs at least {config.GATE_MIN_WORDS} words to score.")
    return None


@app.post("/submit")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """Take a piece of text, score it, log the decision, answer. (Milestone 3: one signal.)"""
    payload = request.get_json(silent=True)

    # ── Check the input before anything touches the model ──────────────────
    if not isinstance(payload, dict):
        return _reject(None, "invalid_json",
                       "Send a JSON object with 'text' and 'creator_id'.")

    creator_id = payload.get("creator_id")
    text = payload.get("text")

    if not isinstance(creator_id, str) or not creator_id.strip():
        return _reject(None, "missing_creator_id",
                       "'creator_id' is required and must be a non-empty string.", text=text)
    if not isinstance(text, str):
        return _reject(creator_id, "missing_text",
                       "'text' is required and must be a string.")
    if not text.strip():
        return _reject(creator_id, "empty_text", "'text' is empty.", text=text)
    if len(text) > MAX_TEXT_CHARS:
        return _reject(creator_id, "text_too_long",
                       f"'text' is over {MAX_TEXT_CHARS} characters.", text=text)

    # ── Input gate: refuse what the signals can't meaningfully score ──────
    refused = _gate(text)
    if refused:
        return _reject(creator_id, *refused, text=text)

    # ── Signal one ──────────────────────────────────────────────────────────
    try:
        model_score = detector.model_signal(text)
    except ValueError:
        return _reject(creator_id, "text_too_short",
                       "'text' is too short to score. Send a few sentences at least.",
                       text=text)
    except detector.DetectorUnavailable:
        return _reject(creator_id, "detector_unavailable",
                       "The detector model isn't loaded. Run `python detector.py` once.", 503,
                       text=text)

    # ── Signal two, then combine and label ──────────────────────────────────
    style_score = stylometry.style_signal(text)
    combined = scoring.combine_signals(model_score, style_score)
    guess, label = scoring.score_to_label(combined)
    content_id = str(uuid.uuid4())

    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined,
        label=label,
        status="decided",
        **_request_fields(text),
    )

    return jsonify({
        "content_id": content_id,
        "guess": guess,
        "confidence": combined,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
        "status": "decided",
    })

@app.post("/appeal")
def appeal():
    """A writer says we got it wrong. Record it, move the item to under_review, confirm."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "invalid_json",
                        "message": "Send a JSON object with 'content_id' and 'reasoning'."}), 400

    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")

    if not isinstance(content_id, str) or not content_id.strip():
        return jsonify({"error": "missing_content_id",
                        "message": "'content_id' is required."}), 400
    if not isinstance(reasoning, str) or not reasoning.strip():
        return jsonify({"error": "missing_reasoning",
                        "message": "Please explain why you think the label is wrong."}), 400

    entries = audit.entries_for(content_id)
    decision = next((e for e in entries if e.get("status") == "decided"), None)
    if decision is None:
        return jsonify({"error": "not_found",
                        "message": f"No submission found with content_id '{content_id}'."}), 404

    # A second appeal on the same item: keep the status, don't log a duplicate.
    already_appealed = any(e.get("event") == "appeal" for e in entries)
    if not already_appealed:
        audit.log_appeal(content_id=content_id,
                         creator_id=decision["creator_id"],
                         reasoning=reasoning)

    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": ("Thanks. Your appeal has been recorded and a person will review this decision."
                    if not already_appealed else
                    "This submission is already under review. Your earlier appeal is on record."),
    })

# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
