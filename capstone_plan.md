# Unit 9 Capstone — Plan and Guidance for Working with a Claude Agent

Student: Hieu Quach · System: **Provenance Guard** · Repo: `https://github.com/jessie-184/ai201-project4-provenance-guard-starter-v2026`

This document is for an AI agent helping me through the AI201 Unit 9 capstone. It is built only from the official brief ("Show What You Know: The Capstone"), the grading rubric I was given, and what is actually in my repository. Where something is not stated in the brief or not yet known, it is marked **VERIFY** or **DECIDE (student)**. Do not fill those in by guessing.

---

## 0. Rules for the agent (read first, follow throughout)

1. **Stay inside the brief.** If a step isn't in this document or the brief, ask me before doing it. Do not add features, files, sections or "nice to haves".
2. **Do not write code unless I explicitly ask for it in that message.** Default to explaining what to change, where, and why. When I do ask for code, change only what I asked for.
3. **Do not write, draft, rewrite or "improve" my acceptance criteria.** The brief says: *"don't ask a model to write these. Ask it whether each one could be checked by a person who couldn't ask you what you meant."* The only thing you may do with my criteria is answer, for each one: (a) how exactly you'd test it using only the sentence itself, (b) would two people score it the same way, (c) what would have to happen for it to fail. Don't rewrite them.
4. **Never invent results.** Every number in the README must come from a run I actually did and pasted to you, or a file in the repo. If you compute something (counts, averages, arithmetic), show how and say it was computed from which file.
5. **Never rewrite git history.** No `git commit --amend` on pushed commits, no `rebase`, no `push --force`, no deleting/recreating the repo. The commit order is graded.
6. **Same repository.** All work goes in the repo above. No copies, no new repo.
7. **Verdicts are strict.** A target must hold in all three trials. If any trial misses, the verdict is MISSED. Don't take the generous reading.
8. **When unsure, say so and ask.** Don't fill a gap with a plausible-sounding answer.

---

## 1. What I'm doing (decisions already made)

| Decision | Choice |
|---|---|
| System | Provenance Guard (AI201 project 4, units 7–8) |
| Shape | **B — Harden against failure** ("make it survive when things don't… your criteria are about what happens on the bad path") |
| Run path | **Path B — local with logs** (the brief says a system that loads a local model belongs on Path B; the free host's 512 MB isn't enough for GPT-2) |
| Extension idea (DECIDE (student) — final wording is mine) | One input gate in `app.py::submit` that refuses text the signals can't meaningfully score (e.g. too few real words, or mostly non-letter characters) **before** signal one or signal two runs |

Why this extension: my Unit 8 "What's Still Broken" already named route validation as the first fix: MF03 (control characters) and MF04 (punctuation only) are still scored and labelled human; MF05–MF07 (long word, emoji, Arabic) only held by accident through the disagreement cap; EV08 (10 words) evades.

**Scope rule from the brief:** the extension must be ONE piece of work, about 90 minutes of building at most. No "rewrite", "from scratch" or "new project".

---

## 2. Facts about the current system (verified from the repo — don't contradict these)

- Flask service, started with `python app.py`, at `http://127.0.0.1:5000` (`config.HOST`, `config.PORT`).
- Routes: `POST /ping`, `POST /submit`, `POST /appeal`, `GET /log`, `GET /health`.
- Signal one: `detector.model_signal`, a GPT-2 perplexity score (`config.DETECTOR_MODEL = "gpt2"`, reads up to `DETECTOR_MAX_TOKENS = 400`). The model is downloaded on first use (requirements.txt says about 550 MB). It runs locally and there's no API key.
- Signal two: `stylometry.style_signal`. After the Unit 8 fix, `W_SPREAD, W_PUNCT, W_TTR = 1.00, 0.00, 0.00`, so it uses sentence-length spread only. Fewer than 2 sentences gives neutral 0.5.
- Combining: `scoring.combine_signals`, weights 0.55 / 0.45, disagreement cap (gap > 0.4 → at most 0.71). Labels: `scoring.score_to_label`, human < 0.45, unsure 0.45–0.72, ai > 0.72.
- Rate limit: Flask-Limiter, 5/minute and 50/day per `creator_id` (falls back to IP). 429s are logged.
- Audit log: `audit.py` writes JSON lines to `logs/audit.jsonl` via `log_decision`, `log_appeal` and `log_rejection`. `log_decision` and `log_rejection` accept `**extra`, so new fields can be added without changing the nine existing ones. **The log has no duration field yet.**
- Existing test tooling: `run_eval.py` (runs `scenarios.py` scenarios, 3 trials, writes `results/run_<time>_<label>.md`), `run_attacks.py` (`--set attack_set --label …`, `--id`, `--flood N`), `attack_set/attacks.csv`, `attack_set/attacks_malformed_requests.csv`, `test.py`.
- `requirements.txt` uses version **ranges** (lower and upper bounds), including `gunicorn` marked "UNIT 9". Supported Python: 3.11–3.13.
- GPT-2 scoring gave **identical scores across three trials** in Unit 8 (no sampling). The brief warns: *"If a criterion involving a model came out identical three times, check you're really re-running."*
- README already contains Unit 7–8 sections, including ones with the same names the capstone needs ("How I Used AI", "Run Log and Verdicts", "The Improvement", "What's Still Broken"). `criteria.md` already holds my Unit 7 criteria.

---

## 3. How it's graded

60 points in total: 30 for the build half and 30 for the test half. Missing my own criteria does **not** cost points. Shape and run path don't affect the score.

**Build half asks:**
1. Did I extend a system I built, and can a reader see what's new and what's out of scope?
2. Does it run somewhere that isn't my editor, with a record of it running?
3. Are my criteria real criteria: specific, testable, with targets, and mostly about the extension?

**Rubric items I was given (point values as stated):**

| Area | Points | Item |
|---|---|---|
| Ran and observable | 1 | Evidence it ran outside the editor (Path B: a committed run record produced by the documented start command) |
| | 1 | Structured logging: at least 10 entries pasted as text, each with named fields including **timestamp, what came in, what came out, and a duration** |
| | 1 | Failures logged: at least one entry for a run that errored, timed out or was rejected (or a note that the failure path was tested and produced none) |
| Runs happened (5) | 2 | All five criteria in the run log, three trials each, in the required table format |
| | 2 | **Real output pasted under each criterion**: actual log lines or responses, with the file and function named |
| | 1 | Criteria committed before results, **both commits identifiable from their messages** |
| Verdicts (6) | 4 | All five verdicts follow from the run log and the target |
| | 2 | Revision handled correctly (none, or only because a criterion couldn't be measured or measured the wrong thing; original line kept, new one underneath with a reason) |
| Diagnosis (7) | 7 | Every miss names a **component** and states the **mechanism** (full credit if nothing missed and I name which target was too low and a tighter one) |
| Improvement (6) | 2 | README names the change and connects it to a specific diagnosed failure |
| | 2 | **Full criteria set rerun** after the change, three trials each, both result sets in the same format |
| | 2 | Says whether it helped, how I know, and what it cost elsewhere |
| Cost and what's left (6) | 2 | What It Costs: the hundred-a-day arithmetic **shown**, following from the measured per-run number |
| | 2 | What's Still Broken: every missed criterion, what I'd do, and why I stopped |
| | 2 | The one thing I'd do first, and why that one rather than the others |

VERIFY: the full breakdown is "on the course grading page". The items above are what I was given; don't assume the rest.

---

## 4. Final deliverables checklist (from the brief's submission section)

**Files:**
- [ ] `criteria.md`: five numbered criteria, each with a target and a reason; any revisions written underneath the originals.
- [ ] `RUNNING.md`: the start command and the environment it needs.
- [ ] `README.md`: the nine sections below, added to what's already there.
- [ ] At least **8 new commits** this unit. `criteria.md` committed before any results, and both of those commits named in their messages.

**README sections, in this order:**

| Section | What goes in it |
|---|---|
| What This Extends | Which system, and what's new |
| The Shape | A, B or C, and what's out of scope |
| Running It | Which path, and a pointer to RUNNING.md |
| Instrumentation | What each log record holds, plus at least 10 entries pasted as text |
| What It Costs | Measured per-run cost, how it was measured, and the hundred-a-day arithmetic |
| Run Log and Verdicts | 5 criteria × 3 trials, MET or MISSED, and the stage and mechanism for each miss |
| The Improvement | What changed, why, and the second run log in the same format |
| What's Still Broken | Each remaining miss, why I stopped, and the one thing I'd do first |
| How I Used AI | Two specific moments: what I asked, what I got, what I changed |

**Paste everything as text. No screenshots, no video.**

**DECIDE (student) / VERIFY with TF:** the README and `criteria.md` already hold Unit 7–8 content with some of the same section names. Proposed handling, unless the TF says otherwise: add a top-level heading `# Unit 9 — Capstone` to the README with the nine sections under it, and add a heading `# Unit 9 — Capstone criteria` to `criteria.md` with the new five under it. Don't delete or edit any Unit 7–8 content.

---

## 5. Milestone-by-milestone plan

### Milestone 1 — Pick the system, pick the shape, cut the scope (~35 min)

**Steps:**
1. I write **The Shape** in the README: Shape B, and one paragraph on what I'm adding.
2. I write **two or three out-of-scope items** (things I considered and decided not to do). Candidates from my Unit 8 findings, my choice which: flagging prompt-injection text; replacing GPT-2 with a bigger model; changing thresholds or weights; adding a reviewer endpoint for appeals; hosting it (Path A).
3. I write **What This Extends**: Provenance Guard, and what's new.
4. Sanity-check the size. Building it should take at most about 90 minutes.

**Agent's job:** when I paste my plan, answer exactly the brief's prompt: *"Break it into the separate pieces of work it actually contains, and tell me how many of them there are. Don't tell me whether it's achievable and don't suggest a smaller version."* If there's more than one piece, I cut it down myself.

**Done when:** the README names the system, the shape and what's out of scope.
**Commit:** e.g. `Capstone M1: shape and scope`

---

### Milestone 2 — Build the extension (~90 min)

**Steps:**
1. **DECIDE (student):** the gate's exact rules and numbers (for example a minimum count of real words, a minimum share of letters). Write them down before building.
2. Build the gate in `app.py::submit` so it runs **after** the existing JSON and field checks and **before** `detector.model_signal` and `stylometry.style_signal`.
3. A refused input should return a 4xx JSON error with a reason code, and be logged with `audit.log_rejection`, the same pattern as the existing rejections.
4. **Confirm the original system still works:** `python test.py`, a normal human and AI submission through `/submit`, an appeal through `/appeal`, and `/ping`. *"An extension that breaks what it extends is a regression."*
5. Commit as I go: **at least 3 commits in this milestone.**

**Agent's job:** explain where and how to change the code. Write code only if I ask. Point out if a gate rule would also refuse real human writing. My Unit 8 attack set has FP08 ("very short genuine human submission"), which currently holds as human, so a length rule has a real cost.

**If stuck after an hour:** cut it down, don't push through, and write down what I cut and why. That sentence goes in What's Still Broken.

**Done when:** the extension does something I can demonstrate, and the original system still works.
**Commits:** e.g. `Capstone M2: add input gate to /submit`, `Capstone M2: log gate rejections`, `Capstone M2: check original routes still work`

---

### Milestone 3 — Get it running, and make it observable (~75 min)

**A. RUNNING.md (Path B).** Add a capstone section with:
- **The exact start command,** tested from a clean checkout.
- **The environment:**
  - Python version (VERIFY: run `python --version`).
  - Pinned dependencies. `requirements.txt` has ranges; record the exact installed versions too, for example from `pip freeze`.
  - Model files and their size. VERIFY: measure the actual size of the downloaded GPT-2 cache on my machine, and don't just copy the "~550 MB" from requirements.txt.
- **Test it on myself:** clone the repo into a new folder, follow RUNNING.md exactly, and fix whatever was missing. *"It will fail the first time. Whatever was missing is the thing a reader would have hit."* Note that the model cache may already be on my machine, so a clean checkout might not show the download step. Say so in RUNNING.md.

**B. Structured logging.** Every request to `/submit` writes one JSON record to `logs/audit.jsonl` (a file, not `print()`) with named fields:
- `timestamp` (already there).
- **What came in:** for example `creator_id`, text length, word count, and a short excerpt. DECIDE (student): how much text to keep.
- **What came out:** guess, scores and label for decisions, or `reason` for rejections.
- **`duration_ms`:** time from request start to response. New.
- Optional: the stage that refused or failed.
- **Failures too:** gate rejections, other 400s, 429s, and 503 detector-unavailable each leave a record with a duration.
- Keep the existing nine decision fields as they are, so old and new entries stay comparable.

**C. Cost of one run.** Seconds of compute is the real cost here (no API spend):
- Run **ten** normal submissions, take the average `duration_ms`, and write down exactly how it was measured (which inputs, warm or cold model, which machine).
- *"A number from the pricing page isn't a measurement."*

**D. README:**
- **Running It:** Path B, with a pointer to RUNNING.md.
- **Instrumentation:** what each record holds, plus at least 10 real entries pasted as text, including at least one rejection.
- **What It Costs:** the measured number and its method. The arithmetic comes in Milestone 7.

**Optional stretch** (extra credit; **declare it in the README before starting**): a latency breakdown with time per stage (gate, signal one, signal two, combining) in each record.

**Done when:** the system starts from RUNNING.md alone, and ten log entries and a measured cost number are in the README.
**Commit:** e.g. `Capstone M3: RUNNING.md, structured logging with duration, cost measurement`

---

### Milestone 4 — Write the criteria, unaided (~45 min) — **I write these myself**

**Requirements from the brief:**
- Five numbered criteria in `criteria.md`, written **before running anything.**
- **At least 3 of the 5 are about the extension** (the gate, its logging, the bad path), not the parts that already worked.
- Each has a target: a number, a rate, or something a person could plainly see. No "works", "reliable", "good" or "fast".
- Under each, why that target and not a stricter or looser one, tied to my system or to what being wrong would cost.
- **At least one is about what happens when things go wrong:** an error, a timeout, an empty result, a bad input.
- If one is about response time, say whether it means a warm request or any request. On Path B, that means a warm model or the first request after starting.

**Agent's job (only this):** for each of my five, answer *"how exactly would you test it using only the sentence itself, would two people score it the same way, and what would have to happen for it to fail? Don't rewrite them."* The third question matters most: if nothing can be pictured that makes it fail, the target is too low.

**Also decide now, before results:** what each criterion will be run against. *"Nobody wrote a test set for you this unit."* My Unit 8 attack set and 22-text test set were used to diagnose the Unit 8 fix and to motivate this gate, so a criterion tested only on those inputs is tested on what I designed for. Consider writing down fresh inputs for the gate (junk that should be refused and real short human writing that should pass) before running anything.

**Commit `criteria.md` on its own, before any results,** with a message that names it, e.g. `Add capstone criteria (criteria.md)`.

---

### Milestone 5 — Run the test (~50 min)

**Steps:**
1. For each criterion, decide what has to run to produce its number. Failure criteria need failures triggered on purpose. A latency criterion needs enough runs to give a distribution, not a single number.
2. Run everything **three separate times, changing nothing in between,** and save the real output: `results/` files, curl output, and log lines.
3. Fill the run log table (exact format from the brief):

```
| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
```
Five rows, one per criterion. Fewer than five rows isn't a complete run log.

4. Under the table, paste **real output for each criterion** from one of the runs, naming the file and function that produced it.
5. **Identical results:** if a model-based criterion comes out identical three times, show it really was rerun (a different `content_id` and timestamp per trial) and explain why the scores match: GPT-2 scoring is deterministic, with no sampling.

**Commit the first results on their own,** with a message that names them, e.g. `First capstone results: before run`.

---

### Milestone 6 — Call every criterion, diagnose every miss, fix one (~70 min)

**Steps:**
1. Write MET or MISSED against each target, strictly: all three trials must hold.
2. For each miss, name **the component** (gate, `/submit` route, signal one, signal two, combining rule, label mapping, logging, rate limiter) **and the mechanism.** The brief's example of a real diagnosis: *"Three of ten runs came back over 5 seconds. All three had queries that matched more than twelve chunks, and my reranker scores every match serially before it truncates. The stage is the reranker; the mechanism is that its cost scales with match count…"*
3. Look for a pattern. Three misses in one stage are one problem, and saying so is worth more.
4. **Make one improvement,** aimed at something just diagnosed. Rerun **all five criteria**, three trials each, in the same format.
5. Put both result sets in the README side by side, and say whether it helped and what it cost. A trade-off reported honestly earns full credit.
6. **Revising a criterion:** only if it couldn't be measured or measured the wrong thing. Keep the original, put the new line underneath with the reason. Never weaken a target because it was hard to hit.
7. If the improvement isn't working after 40 minutes, keep both result sets anyway and write down what was tried and where it broke.

**Commits:** e.g. `Capstone M6: verdicts and diagnoses`, `Capstone M6: improvement`, `Capstone M6: after run`

---

### Milestone 7 — Cost, what's left, submit (~30 min)

**Steps:**
1. **What It Costs:** the measured per-run number, how it was measured, and one sentence on running it for a hundred people a day, **with the multiplication shown.** DECIDE (student) and state: how many submissions per person per day is assumed. If a dollar figure is added, cite where the price came from; the measured seconds stay the main number.
2. **What's Still Broken:** for each criterion still missed, what I'd do and why I stopped. "I ran out of time" is fine if true.
3. **Two sentences on the one thing I'd do first** with another unit, and why that one rather than the others. Not a wish list.
4. **How I Used AI:** two specific moments from this unit. What I asked, what I got, what I changed.
5. Check the repo against section 4 of this document, then submit the **same repo URL** as before.

**Commit:** e.g. `Capstone M7: cost, what's still broken, how I used AI`

---

## 6. Commit plan (at least 8; order matters)

1. `Capstone M1: shape and scope`
2. `Capstone M2: …` (build, part 1)
3. `Capstone M2: …` (build, part 2)
4. `Capstone M2: …` (original system still works)
5. `Capstone M3: RUNNING.md, logging, cost`
6. **`Add capstone criteria (criteria.md)`**: `criteria.md` only, **before any results exist**
7. **`First capstone results: before run`**
8. `Capstone M6: verdicts, diagnoses, improvement, after run`
9. `Capstone M7: cost arithmetic, what's still broken, how I used AI`

Note: Milestone 3 asks for "ten log entries and a measured cost number" in the README **before** Milestone 4's criteria. Those are instrumentation output, not criteria results, but to keep the order unambiguous, **DECIDE (student) / VERIFY with TF:** whether cost and log entries can be committed before the criteria commit. The brief's order (M3 then M4) suggests yes.

---

## 7. Known risks to watch

- **Scope creep:** the gate plus injection flagging plus a new model is three projects. Keep one.
- **Over-refusing real writers:** a strict gate can refuse genuine short human text (FP08 in my attack set). Worth a criterion.
- **Testing on what I tuned for:** reusing the Unit 8 attack set or test set as the only test inputs.
- **Identical trials:** explain them; don't hide them.
- **Commit order:** criteria commit, then results commit, both clearly named. No history rewriting.
- **Clean-checkout test skipped:** the brief expects it to fail the first time. Record what I fixed.
- **Screenshots:** not allowed. Paste text only.