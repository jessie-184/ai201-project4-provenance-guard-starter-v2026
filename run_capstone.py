"""
Unit 9 capstone runner: the five criteria in criteria.md ("Unit 9 — Capstone
criteria"), three trials, nothing changed in between.

    python app.py                      # in one terminal; wait for "Debugger PIN"
    python run_capstone.py before      # in another; label is "before" or "after"

Inputs come from capstone_inputs.py (committed before any run). Every request
is sent one at a time, and the log lines it added are read back from
logs/audit.jsonl straight afterwards, so each result below is what the log
actually recorded for that request.

Writes results/capstone_<date>_<time>_<label>.md (tables + per-input rows)
and a .json file with every row.
"""
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

import capstone_inputs as inp
import config

URL = f"http://{config.HOST}:{config.PORT}"
LOG = config.AUDIT_LOG
TRIALS = 3
PAUSE_BETWEEN_TRIALS_S = 65    # lets the per-minute rate-limit window reset
GATE_REASONS = {"not_english_text", "too_few_words"}
C5_LIMIT_MS = 150


# ── Talking to the service and reading the log back ─────────────────────────

def _log_len():
    with open(LOG, encoding="utf-8") as f:
        return sum(1 for _ in f)


def _log_from(n):
    with open(LOG, encoding="utf-8") as f:
        return [json.loads(l) for l in f.read().splitlines()[n:] if l.strip()]


def send(body, raw=False):
    """One /submit request. Returns the response and the log lines it added."""
    before = _log_len()
    if raw:
        r = requests.post(f"{URL}/submit", data=body.encode("utf-8"),
                          headers={"Content-Type": "application/json"}, timeout=120)
    else:
        r = requests.post(f"{URL}/submit", json=body, timeout=120)
    resp = r.json() if r.content else {}
    return r.status_code, resp, _log_from(before)


def row(item_id, status, resp, lines, **extra):
    decided = [l for l in lines if l.get("status") == "decided"]
    rejected = [l for l in lines if l.get("event") == "rejected"]
    first = (decided or rejected or [{}])[0]
    return {
        "id": item_id, "http": status,
        "error": resp.get("error"), "label": resp.get("label"),
        "log_lines": len(lines), "decided_lines": len(decided), "rejected_lines": len(rejected),
        "reason": first.get("reason"), "duration_ms": first.get("duration_ms"),
        "content_id": first.get("content_id"), "timestamp": first.get("timestamp"),
        **extra,
    }


def health():
    return requests.get(f"{URL}/health", timeout=10).json()


# ── One trial of each criterion ─────────────────────────────────────────────

def trial(n, tag):
    cid = lambda item: f"cap_{tag}_t{n}_{item}"
    out = {}

    rows = []
    for item, code, text in inp.CONTROL_CHAR_TEXTS:
        r = row(item, *send({"creator_id": cid(item), "text": text}), code=code)
        r["pass"] = r["http"] == 400 and r["decided_lines"] == 0
        rows.append(r)
    out["c1"] = rows

    rows = []
    for item, lang, text in inp.NON_ENGLISH_TEXTS:
        r = row(item, *send({"creator_id": cid(item), "text": text}), language=lang)
        r["pass"] = r["http"] == 400
        rows.append(r)
    out["c2"] = rows

    rows = []
    for item, text in inp.SHORT_HUMAN_TEXTS:
        r = row(item, *send({"creator_id": cid(item), "text": text}))
        r["pass"] = r["error"] not in GATE_REASONS     # pass = not refused by the gate
        rows.append(r)
    out["c3"] = rows

    rows = []
    for req in inp.BAD_REQUESTS:
        body = req["body"]
        if req["kind"] == "raw":
            body = body.replace('"c4_01"', json.dumps(cid("C4_01")))
            got = send(body, raw=True)
        else:
            body = dict(body)
            if "creator_id" in body:
                body["creator_id"] = cid(req["id"])
            if req["kind"] == "flood":
                for _ in range(5):                      # the first five aren't counted
                    send(body)
            got = send(body)
        r = row(req["id"], *got, what=req["what"])
        only = got[2][0] if len(got[2]) == 1 else {}
        r["pass"] = (len(got[2]) == 1 and only.get("event") == "rejected"
                     and only.get("reason") is not None and only.get("duration_ms") is not None)
        rows.append(r)
    out["c4"] = rows

    h = health()
    rows = []
    for item, text in inp.SPEED_TEXTS:
        r = row(item, *send({"creator_id": cid(item), "text": text}),
                words=len(text.split()))
        r["pass"] = (r["decided_lines"] == 1 and r["duration_ms"] is not None
                     and r["duration_ms"] <= C5_LIMIT_MS)
        rows.append(r)
    out["c5"] = rows
    out["c5_health_before"] = h
    return out


# ── Scoring each trial against the target in criteria.md ────────────────────

def score(t):
    c1 = sum(r["pass"] for r in t["c1"])
    c2 = sum(r["pass"] for r in t["c2"])
    c3_refused = sum(not r["pass"] for r in t["c3"])
    c4 = sum(r["pass"] for r in t["c4"])
    c5 = sum(r["pass"] for r in t["c5"])
    warm = t["c5_health_before"].get("detector_loaded") is True
    return [
        ("1. Control characters refused", "10 of 10 refused (400, no decided line)",
         f"{c1}/10 refused", c1 == 10),
        ("2. Non-English refused", "at least 9 of 10 refused (400)",
         f"{c2}/10 refused", c2 >= 9),
        ("3. Short human texts not refused", "0 of 20 refused by the gate",
         f"{c3_refused}/20 refused", c3_refused == 0),
        ("4. Bad requests logged", "10 of 10 with exactly one rejected line, reason + duration_ms",
         f"{c4}/10 logged", c4 == 10),
        ("5. Warm latency", f"at least 29 of 30 at or under {C5_LIMIT_MS} ms (warm model)",
         f"{c5}/30 ≤ {C5_LIMIT_MS} ms" + ("" if warm else " (NOT warm)"), c5 >= 29 and warm),
    ]


def md_rows(rows, cols):
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    body = "".join("| " + " | ".join("" if r.get(c) is None else str(r.get(c)) for c in cols) + " |\n"
                   for r in rows)
    return head + body


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "before"
    started = datetime.now()
    tag = started.strftime("%m%d%H%M")
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()

    h = health()
    print("health at start:", h)
    if not h.get("detector_loaded"):
        print("model cold: sending one warm-up request (not counted)")
        send({"creator_id": f"cap_{tag}_warmup", "text": inp.SPEED_TEXTS[0][1]})
        print("health after warm-up:", health())

    trials = []
    for n in range(1, TRIALS + 1):
        if n > 1:
            print(f"waiting {PAUSE_BETWEEN_TRIALS_S}s before trial {n}")
            time.sleep(PAUSE_BETWEEN_TRIALS_S)
        print(f"trial {n} ...")
        t = trial(n, tag)
        trials.append(t)
        for name, _, got, ok in score(t):
            print(f"  {name}: {got}  {'pass' if ok else 'MISS'}")

    scores = [score(t) for t in trials]
    stem = f"capstone_{started.strftime('%Y-%m-%d_%H%M')}_{label}"
    out_dir = config.RESULTS_DIR
    out_dir.mkdir(exist_ok=True)

    md = [f"# Capstone run log — {label}\n",
          f"- Produced by: `run_capstone.py::main` · inputs: `capstone_inputs.py`",
          f"- Service: `app.py::submit` (gate: `app.py::_gate`) · commit `{commit}`",
          f"- {TRIALS} trials, {PAUSE_BETWEEN_TRIALS_S}s apart, nothing changed in between · "
          f"started {started:%Y-%m-%d %H:%M:%S}",
          f"- creator_id prefix: `cap_{tag}_t<trial>_`\n",
          "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
          "|---|---|---|---|---|---|"]
    for i in range(5):
        name, target = scores[0][i][0], scores[0][i][1]
        runs = [s[i][2] for s in scores]
        verdict = "MET" if all(s[i][3] for s in scores) else "MISSED"
        md.append(f"| {name} | {target} | {runs[0]} | {runs[1]} | {runs[2]} | {verdict} |")
    md.append("")

    sections = [
        ("c1", "Criterion 1 — control characters", ["id", "code", "http", "error", "decided_lines", "duration_ms", "pass"]),
        ("c2", "Criterion 2 — non-English", ["id", "language", "http", "error", "label", "duration_ms", "pass"]),
        ("c3", "Criterion 3 — short human texts", ["id", "http", "error", "label", "duration_ms", "pass"]),
        ("c4", "Criterion 4 — bad requests", ["id", "what", "http", "log_lines", "rejected_lines", "reason", "duration_ms", "pass"]),
        ("c5", "Criterion 5 — warm latency", ["id", "words", "http", "label", "duration_ms", "content_id", "pass"]),
    ]
    for key, title, cols in sections:
        md.append(f"## {title}\n")
        for n, t in enumerate(trials, 1):
            md.append(f"**Trial {n}**" + (f" · `/health` before: `{json.dumps(t['c5_health_before'])}`"
                                          if key == "c5" else "") + "\n")
            md.append(md_rows(t[key], cols))
    (out_dir / f"{stem}.md").write_text("\n".join(md), encoding="utf-8")
    (out_dir / f"{stem}.json").write_text(
        json.dumps({"label": label, "commit": commit, "started": started.isoformat(),
                    "trials": trials}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote results/{stem}.md and results/{stem}.json")
    print("\n".join(md[5:12]))


if __name__ == "__main__":
    main()
