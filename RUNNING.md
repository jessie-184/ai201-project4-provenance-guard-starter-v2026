# Running Provenance Guard

Everything about how the starter works.

This is a **web service**. It runs on your machine and you talk to it with
`curl` from another terminal. If you've not built a backend before, that's
assumed — the starter ships one that already answers.

---

## Unit 9 capstone — running it (Path B: local, with logs)

This is how the capstone version runs. It runs on one machine; it is not
hosted (GPT-2 plus torch doesn't fit a 512 MB free tier — see
[Running it somewhere else](#running-it-somewhere-else-unit-9)).

### Start command

From the repo folder, with the virtual environment active:

```bash
python app.py
```

It serves on `http://127.0.0.1:5000`. Every request to `/submit` writes one
JSON line to `logs/audit.jsonl`; that file is the run record.

### Environment

| What | Version / size |
|---|---|
| Python | 3.13.15 (3.11–3.13 supported; **not** 3.14) |
| Tested on | Apple M4 Pro, 24 GB RAM, macOS 27.0.1, CPU only |
| GPT-2 model files | 525 MB on disk (`du -sh ~/.cache/huggingface/hub/models--gpt2`), downloaded on first use |
| Free disk | `test.py` asks for about 9 GB — torch is most of it |
| API keys | none |

`requirements.txt` gives version ranges. The exact versions this was run with
(`pip freeze`) are:

<details>
<summary>Exact installed versions (40 packages)</summary>

```
blinker==1.9.0
certifi==2026.10.23
charset-normalizer==3.5.2
click==8.5.0
Deprecated==3.0.0
filelock==4.2.4
Flask==3.1.3
Flask-Limiter==3.12
fsspec==2026.9.0
gunicorn==23.0.0
hf-xet==1.7.1
huggingface_hub==0.36.2
idna==3.20
itsdangerous==2.2.0
Jinja2==3.1.6
limits==5.8.0
markdown-it-py==4.2.0
MarkupSafe==3.0.4
mdurl==0.1.2
mpmath==1.3.0
networkx==3.7
numpy==2.5.4
ordered-set==4.1.0
packaging==26.3
Pygments==2.21.0
PyYAML==6.0.3
regex==2026.9.29
requests==2.34.2
rich==13.9.4
safetensors==0.8.0
setuptools==84.2.1
sympy==1.14.0
tokenizers==0.22.2
torch==2.15.0
tqdm==4.70.1
transformers==4.57.6
typing_extensions==4.16.0
urllib3==2.8.0
Werkzeug==3.1.9
wrapt==2.5.1
```

</details>

### From a fresh clone

```bash
git clone https://github.com/jessie-184/ai201-project4-provenance-guard-starter-v2026.git
cd ai201-project4-provenance-guard-starter-v2026
python3.13 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python test.py                     # no FAIL lines; "Detector model" is a WARN until the next step
python detector.py                 # downloads GPT-2 (525 MB) once, scores a sample
python app.py
```

Wait until the first terminal prints `Debugger PIN: …`. Debug mode starts the
server, then restarts it once; a request sent before that line can get an empty
reply. Then, in a second terminal:

```bash
curl http://127.0.0.1:5000/health               # "ok": true
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "We got to the campsite about four. The pitch was fine, a bit sloped.", "creator_id": "me"}'
curl "http://127.0.0.1:5000/log?limit=1"
```

### What the clean-checkout test found

I cloned the repo into a new folder on 2026-11-11 and followed the steps above
exactly, with a fresh virtual environment. What happened:

- `pip install -r requirements.txt` worked (46 s, but pip reused wheels it had
  already downloaded for my main checkout; a first-ever install downloads torch
  and takes longer).
- `python test.py` passed 9 of 9 and `python detector.py` scored its sample
  without downloading anything, **because GPT-2 was already in
  `~/.cache/huggingface` on this machine.** That cache is shared between
  checkouts, so this test could not show the download step. On a machine
  without it, expect the WARN and the 525 MB download.
- **The first two `curl` commands came back empty.** I sent them straight after
  `python app.py`, while debug mode was still restarting. Sent again after
  `Debugger PIN` appeared, they worked: the submission came back `unsure`
  (0.6425) and `/log?limit=1` showed its entry with `duration_ms` 5037.7, the
  cold first request. Fix: the "wait until `Debugger PIN`" line above, and a
  `/health` check first.

### Things that will catch you out

- **The first `/submit` after starting is slow** (4.2 s measured) because it
  loads GPT-2 into memory. After that a submission takes about 50 ms.
  `GET /health` shows `"detector_loaded": true` once it's warm.
- **Debug mode restarts the server when a `.py` file changes.** The restart
  unloads the model (the next request is cold again) and forgets every
  rate-limit count. Don't edit code during a measured run.
- **Stop it with Ctrl+C in its own terminal.** Debug mode runs two `Python
  app.py` processes; killing only one can leave the other holding port 5000,
  and the next `python app.py` then fails with "Address already in use".
- **macOS AirPlay Receiver also listens on port 5000.** It didn't stop the
  service binding to `127.0.0.1:5000` here, but if you get "Address already in
  use", check `lsof -nP -iTCP:5000 -sTCP:LISTEN`.
- **The rate limit is 5 a minute per `creator_id`, and refused requests count
  too.** Sending a sixth request from one `creator_id` inside a minute gets a
  429. Use a different `creator_id` per test input.

---

## Before your first class

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python test.py
```

**You're ready when `python test.py` passes.**

You'll see `[WARN] Detector model — not downloaded yet`:

```bash
python detector.py
```

That downloads about 550 MB and scores a sample.

> **No API key for this pair.** Nothing here calls a hosted service. The model
> that reads your text runs on your own laptop.

---

## Your first five minutes

Two terminals. In the first:

```bash
python app.py
```

In the second:

```bash
curl -X POST http://127.0.0.1:5000/ping \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

You should get JSON back. That's the whole idea of a web service — something
sent it data, it sent something back.

> **On Windows, use `curl.exe` and keep it on one line.**
>
> In PowerShell, `curl` is an alias for a different tool and the command above
> fails with `Cannot bind parameter 'Headers'` before it ever reaches your
> service. The `\` line breaks don't work there either. This does:
>
> ```powershell
> curl.exe -X POST http://127.0.0.1:5000/ping -H "Content-Type: application/json" -d '{\"message\": \"hello\"}'
> ```
>
> Every `curl` command in this file and in the brief works the same way: swap
> `curl` for `curl.exe` and put it on one line. Git Bash needs no change.

**Leave `/ping` alone.** It's your control. When something breaks later, check
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself, and that's a help-channel question.

Then try the route you're going to build:

```bash
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "some writing", "creator_id": "me"}'
```

It returns a `501` saying it isn't built yet. **That's the correct starting
position.**

---

## The routes

| Route | State | What it does |
|---|---|---|
| `POST /ping` | **works** | The example. Don't edit it |
| `GET /health` | **works** | Is the service up, is the model loaded |
| `GET /log` | **works** | The audit log, as JSON |
| `POST /submit` | **you build it** | Milestones 3, 4, 5 |
| `POST /appeal` | **you build it** | Milestone 5 |

---

## Every command

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment |
| `python app.py` | Runs the service |
| `python detector.py` | Downloads the model and scores a sample — **run before class** |
| `python detector.py "some text"` | Score one piece of text from the terminal |
| `python stylometry.py "some text"` | Your style measures, on one piece of text |
| `python run_attacks.py --set <folder>` | The attack set — **unit 8** |
| `python run_attacks.py --flood 15` | Push past your rate limit and print the status codes — **unit 8** |
| `python run_eval.py --label before` | Your five criteria, three trials — **unit 8** |

---

## Which piece goes with which milestone

### Unit 7 — the build

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Trace a submission on paper | Nothing to run |
| 2 | Write your criteria | `criteria.md` — all five are yours |
| 3 | The route, one signal, the log | `app.py::submit`, `detector.py`, `audit.py` |
| 4 | Second signal, combine, score | `stylometry.py`, `scoring.py::combine_signals` |
| 5 | Labels and the appeal path | `scoring.py::score_to_label`, `app.py::appeal` |
| 6 | Write it up | `README.md` |

### Unit 8 — the test

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Rate limiting and the full log | `config.py`, the decorator in `app.py` |
| 2 | Run the attack set | `run_attacks.py` |
| 3 | Run your own criteria | `scenarios.py`, `run_eval.py` |
| 4 | Verdicts and diagnoses | `README.md` |
| 5 | Fix one thing, re-run | `run_attacks.py --label after` |
| 6 | What's still broken | `README.md` |

---

## Building `/submit` in three passes

The ordering is deliberate. It's how you tell a broken route from a broken
signal.

**Milestone 3.** Return a hardcoded response. Confirm `curl` gets it back
**before** you add any logic. Then pull `text` and `creator_id` out. Then call
one signal. Then log it.

**Milestone 4.** Add the second signal. Combine them. Log both scores.

**Milestone 5.** Turn the score into a label.

> Test each signal from a terminal on its own before wiring it in. If you skip
> that you'll spend an hour not knowing whether the route or the signal is
> lying to you.

---

## Turning on rate limiting (unit 8)

Three steps:

1. In `config.py`, set `RATE_LIMITING_ENABLED = True` — or run with
   `AI201_RATE_LIMITS=1`.
2. Choose your numbers there.
3. In `app.py`, uncomment the `@limiter.limit(...)` line above `submit`.

Then push past your limit and watch for `429`:

```bash
python run_attacks.py --flood 15
```

That sends 15 submissions from one `creator_id` and prints the run of status
codes — `200 200 200 ... 429 429` — which is exactly what your README's **Rate
Limiting** section asks you to paste. It also writes `results/flood_<date>.md`.

The attack set can't do this for you. Every attack row submits under its own
`creator_id`, so a full attack run looks like forty-odd different callers and
never trips a limit however long it is.

No `429` at all? Either your limit is above 15 a minute, or rate limiting is
still off. `GET /health` reports which.

Rejections are logged for you. **An attack that shows up only as an absence is
one you'll never find** — a thousand requests that got a `429` and left no
trace look exactly like a quiet afternoon.

---

## Running it somewhere else (unit 9)

Unit 9 asks you to deploy one of your systems. **Read this before you pick
which one** — for this project the answer is already decided, and it isn't the
hosted one.

Flask's built-in server says "development server" on startup because that's
what it is. A real one comes from `gunicorn`, which is in
`requirements.txt` and unused until now:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

Two settings do the work, and both read the environment:

| Variable | Default | What it does |
|---|---|---|
| `HOST` | `127.0.0.1` | Loopback — your machine only. A host needs `0.0.0.0`, or nothing outside the box can reach the service and it looks like the app is down |
| `PORT` | `5000` | Most hosts hand you a port in `PORT` and expect you to bind exactly that one |
| `AI201_DEBUG` | `1` | Debug mode. Off automatically whenever `HOST` isn't loopback — an interactive debugger on a public address is a stranger's Python prompt inside your process |

Nothing about your local workflow changes. With no variables set you get
`http://127.0.0.1:5000` and every `curl` above still works.

### This project will not fit a free host

Say it plainly, because the arithmetic is the point:

| What has to be in memory | Roughly |
|---|---|
| `torch` | ~200–800 MB depending on the build |
| the `gpt2` weights | ~550 MB on disk, loaded into RAM to score |
| Flask, gunicorn, your code | the rest |
| **A free tier gives you** | **512 MB** |

That's over budget before a single request arrives — and a free host has no
persistent disk, so the 550 MB download starts again after every idle
spin-down. There is no configuration that fixes this. The model is the size it
is.

**So pair 4 extensions take Path B — local, with logs.** That is the expected
answer for this project, not a fallback and not a failure. Working out that a
system doesn't fit its host *before* you spend an evening watching it get
killed is the skill unit 9 is actually testing. Write the arithmetic above in
your write-up; that's the deliverable.

---

## Where everything lives

| File | What it does |
|---|---|
| `config.py` | Every setting: thresholds, weights, rate limits, the model |
| `app.py` | The service. `/ping` and `/log` work; `/submit` and `/appeal` are yours |
| `detector.py` | Signal one — the local model. Given to you |
| `stylometry.py` | Signal two. **Stubs — you build these** |
| `scoring.py` | Combining and labelling. **Stubs — you build these** |
| `audit.py` | The audit log writer. Given to you |
| `run_attacks.py` | Runs the attack set — **unit 8** |
| `run_eval.py` | Runs your criteria three times — **unit 8** |
| `scenarios.py` | What your test runs. **You fill this in** |
| `criteria.md` | Your five criteria. **You write all five** |
| `logs/audit.jsonl` | Your audit log. **Commit it** |
| `results/` | Attack runs and run logs. **Commit them** |

---

## The two blind spots, up front

Both signals have one, and unit 8's attack set is built out of them. You have
to name them yourself in Milestone 1 — but knowing they exist now saves you
from being surprised.

**Signal one** measures how *predictable* your text is. Predictability isn't
authorship. What it really rewards is common words in short, ordinary
sentences — someone writing in a second language and staying with vocabulary
they're sure of, a younger writer, anyone writing plainly on purpose. Writing
like that scores about as machine-like as machine writing does. (Dense, ornate
prose often goes the other way and reads as human, because rare words are what
a language model fails to predict.) So the writers this signal is most likely
to accuse are the ones with the least room to argue back. That is the false
positive the whole project is about, and it's structural rather than a bug.

**Signal two** cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — typos, broken-up
sentences, a pasted quotation. That is very cheap to do on purpose.

---

## When something goes wrong

| What you see | What it means |
|---|---|
| `501 not_implemented` | Correct at the start — that's the TODO in `app.py` |
| `404` from curl | Is the server running? Is the path exactly what you typed? |
| `Cannot bind parameter 'Headers'` | You're in PowerShell, where `curl` is a different tool. Use `curl.exe`, on one line |
| Request body arrives empty | curl needs `-H "Content-Type: application/json"` |
| `Address already in use` | A server left running from an earlier attempt. Kill it, don't debug it |
| The first submission takes 10+ seconds | Signal one is loading the model into memory. Later ones take a second or two |
| *Every* submission takes 10+ seconds | Something is reloading the model each call. `GET /health` shows `detector_loaded` — if it goes back to `false`, look for a reload in your handler |
| `DetectorUnavailable` | Run `python detector.py` once to download the model |
| `/appeal` seems to do nothing | Does the `content_id` you sent actually exist in the log? A typo there fails silently |
| Every request gets through, no `429` ever | The decorator is uncommented but limiting is still off. Set `RATE_LIMITING_ENABLED` in `config.py` |
| Flask-Limiter warns about storage | Shouldn't happen — `storage_uri` is preconfigured. If you changed it, put it back |
| All three of your labels never appear | Your ranges have a gap. `scoring.label_ranges()` prints them |

If the route won't respond, go back to `/ping`. If that answers, the problem is
in your handler.

---

## A note on committing

At least four new commits in unit 7, four more in unit 8.

`logs/` and `results/` are deliberately **not** in `.gitignore`. Your audit log
is evidence, and the entries you paste into your README are what unit 8 grades.

**Do not delete and recreate this repository.** You submit the same URL both
units.
