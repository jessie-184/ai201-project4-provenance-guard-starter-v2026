"""
Settings for Provenance Guard.

Everything you're likely to change lives here, at the top, on purpose.

You'll edit the thresholds in Milestone 5 and the rate limits in unit 8.
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent


# ─── The service ─────────────────────────────────────────────────────────────

# `127.0.0.1` is loopback — only your own machine can reach it, which is what
# you want all through units 7 and 8. A host somewhere else has to accept
# traffic from outside the box, and that means `0.0.0.0`. Setting the env var
# is how you get it; the default keeps your local `curl` commands unchanged.
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))

# Flask's debug mode gives anyone who can reach the service an interactive
# Python prompt inside your process. Fine on loopback, a gift to strangers
# anywhere else — so it turns itself off the moment HOST isn't loopback.
DEBUG = os.getenv("AI201_DEBUG", "1") == "1" and HOST in ("127.0.0.1", "localhost")


# ─── The local model ─────────────────────────────────────────────────────────
# Your first signal runs a language model ON YOUR OWN MACHINE. No account, no
# key, no card. It downloads about 550 MB the first time — do that before
# class, not during it.
#
# What it measures: how *predictable* your text is to a language model. Text a
# model finds easy to predict tends to be text a model wrote.
#
# The first call is the slow one — ten to twenty seconds while the model loads,
# longer on an older laptop. After that it stays in memory and a submission
# takes a second or two. That cost is part of what you're learning: this is
# what running a model inline in a request actually looks like.

DETECTOR_MODEL = os.getenv("AI201_DETECTOR_MODEL", "gpt2")

# Longer text gives a steadier reading but takes longer. 400 tokens is roughly
# 300 words, which is enough for the signal to mean something.
DETECTOR_MAX_TOKENS = 400


# ─── Scoring (Milestone 4) ───────────────────────────────────────────────────
# How much each signal counts toward the combined score.
#
# ⚠️ These are placeholders. Milestone 4 asks you to write your combining rule
# down BEFORE you code it, and to put the numbers in your README. Whatever you
# decide, it goes here.

WEIGHT_MODEL_SIGNAL = 0.55
WEIGHT_STYLE_SIGNAL = 0.45

# If the two signals differ by more than this, the combined score is capped
# just below AI_THRESHOLD: strong disagreement can mean "unsure", never "AI".
DISAGREEMENT_LIMIT = 0.4


# ─── Thresholds (Milestone 5) ────────────────────────────────────────────────
# Where one label becomes another. Scores run 0.0 (confidently human) to 1.0
# (confidently AI).
#
#   score < HUMAN_THRESHOLD          -> high-confidence human
#   between the two                  -> unsure
#   score > AI_THRESHOLD             -> high-confidence AI
#
# ⚠️ This is where your false-positive decision from Milestone 1 actually gets
# made. Widening the unsure band means fewer wrong accusations and more AI text
# getting through. There is no setting that avoids the trade — only settings
# that decide who pays for it.

HUMAN_THRESHOLD = 0.45
AI_THRESHOLD = 0.72

# ⚠️ One thing that catches people out in Milestone 5. A weighted average can
# only land between its two inputs — so while `style_signal` is still the stub
# returning 0.5, the combined score can never leave 0.25–0.75 no matter what
# the model signal says, and the human label needs a model score below 0.20 to
# be reachable at all.
#
# If a label you can't reach is the problem, the fix is upstream of the
# thresholds: a style signal that actually varies. `scoring.label_ranges()`
# prints the bands; the reachable range is a different question.


# ─── Input gate (UNIT 9 capstone) ────────────────────────────────────────────
# Runs in app.py::submit after the JSON and field checks and before either
# signal. Text that fails any rule is refused with a 400 and never scored.
#
#   control chars any ASCII control character except tab, newline and
#                 carriage return -> "control_characters". Checked first.
#                 Added in Milestone 6: the before run scored all 10
#                 control-character texts (criteria 1 and 4).
#   letter share  A–Z letters ÷ all non-whitespace characters. Below
#                 GATE_MIN_LETTER_SHARE -> refused as "not_english_text".
#                 Checked before word count, so emoji, Arabic and punctuation
#                 are reported as not English, not as too short.
#   real words    runs of A–Z letters, one internal apostrophe allowed
#                 ("don't"). Fewer than GATE_MIN_WORDS -> "too_few_words".
#
# Why these numbers (measured on the Unit 8 attack set and scenarios.py):
# every real human or AI text there has 8+ words and a letter share of 0.876
# or more (lowest PI05 0.876, FP08 0.897). The junk is far below: MF03 0.474,
# MF01/04/06/07 0.000, MF02 and MF05 one word each. 0.70 sits in that gap,
# and 3 words leaves room under FP08 (8 words, genuine human) for very short
# real writing. Short AI text like EV08 (10 words) is out of scope: no word
# count separates it from FP08.

GATE_MIN_WORDS = 3
GATE_MIN_LETTER_SHARE = 0.70


# ─── Structured logging (UNIT 9 capstone) ────────────────────────────────────
# Every /submit log record also carries duration_ms, text_chars, word_count
# and the first LOG_EXCERPT_CHARS characters of the text. The log is committed
# to a public repo, so it keeps an excerpt, not whole submissions.

LOG_EXCERPT_CHARS = 60


# ─── Rate limiting (UNIT 8) ──────────────────────────────────────────────────
# Off in unit 7. You turn it on and choose the numbers in unit 8, Milestone 1.
#
# Think about two people: a real writer submitting their own work a few times
# an hour, and a script sending a thousand variations to map your thresholds.
# Your README has to say why your numbers and not others.

# RATE_LIMITING_ENABLED = os.getenv("AI201_RATE_LIMITS", "0") == "1"
RATE_LIMITING_ENABLED = True

RATE_LIMIT_PER_MINUTE = 5
RATE_LIMIT_PER_DAY = 50

# Flask-Limiter warns loudly without this. In-memory is right for one laptop
# and wrong for anything real — a restart forgets every count, and two copies
# of the service wouldn't share limits.
RATE_LIMIT_STORAGE = "memory://"


# ─── Paths ───────────────────────────────────────────────────────────────────

LOG_DIR = ROOT / "logs"
AUDIT_LOG = LOG_DIR / "audit.jsonl"
RESULTS_DIR = ROOT / "results"
