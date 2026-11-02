# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

Provenance Guard is a small backend a writing site could plug into. A writer submits text, and the service sends back a guess about whether it was AI-generated, how confident that guess is, a plain-English label the reader sees, and a way for the writer to appeal. Here's the path one submission takes:

1. **The text arrives.** A writing site sends `POST /submit` with JSON containing `text` and `creator_id`. If `text` is missing, empty, or too short to score, the service answers with an error instead of guessing.
2. **Signal one reads it for meaning.** `detector.model_signal` runs GPT-2 locally and measures how predictable the text is (perplexity). Predictable text scores closer to 1 (AI-like), surprising text closer to 0 (human-like).
3. **Signal two measures its shape.** `stylometry.style_signal` measures the text without reading it: how much sentence length varies, how varied the vocabulary is, and how punctuation is used. It also returns a 0–1 score where higher means more AI-like.
4. **The scores become one confidence score and a label.** `scoring.combine_signals` merges the two signals into a single score from 0 (confidently human) to 1 (confidently AI). `scoring.score_to_label` then checks that score against two thresholds in `config.py`: below the human threshold it's "probably written by a person," above the AI threshold it's "probably AI-generated," and anything in between is "unsure." Calling a real writer's work AI needs much stronger evidence than calling it human, because a wrong accusation is the expensive mistake.
5. **The decision is logged and returned.** `audit.log_decision` records the submission under a new `content_id` with both signal scores, the combined score, and the label. The writer gets back JSON with the `content_id`, guess, confidence, label text, and both signal scores.
6. **The writer can push back.** If the writer thinks the label is wrong, they send `POST /appeal` with the `content_id` and their reasoning. The service checks the item exists, records the appeal, moves the item to `under_review`, and confirms. Nothing is re-scored automatically; a person reviews it.


---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** How predictable the text is to a language model. `detector.model_signal` runs GPT-2 locally, computes the text's perplexity (how surprised the model is by each next word), and maps it onto a 0–1 score where low perplexity (very predictable) scores close to 1, meaning more likely AI.

**Why that might differ between human and AI writing:** A language model writes by repeatedly choosing a likely next word, so text a model produced tends to be text a model finds easy to predict. People wander more: an odd word choice, an abrupt turn, a specific detail instead of the typical one. That surprise pushes perplexity up and the score down.

**What it can't see:** Predictability is not authorship. Plain writing, with common words in short, ordinary sentences, is predictable no matter who wrote it. A second-language writer sticking to vocabulary they're sure of, a younger writer, or anyone writing plainly on purpose can score as machine-like as actual AI text. That is the false positive this whole project is about, and it lands on the writers least able to argue back. It also fails the other way: dense, ornate prose full of rare words can score as human even if a model wrote it, and AI text with a few unusual words swapped in becomes less predictable without becoming more human.

I confirmed this in calibration, running `detector.py` on three paragraphs:

| Text | Who wrote it | Perplexity | `model_signal` |
|---|---|---|---|
| Clear AI paragraph about AI | AI | 21.7 | 0.763 |
| Plain, simple paragraph about modern life | Human | 22.1 | 0.758 |
| Personal, specific paragraph about AI's impact | Human | 50.2 | 0.457 |

The plain human paragraph scored almost exactly the same as the AI one, so on signal one alone no threshold can separate them. Any setting that labels the AI paragraph "AI" would also accuse that writer.

### Signal two — the style signal

**What it measures:** The shape of the text, without reading it. `stylometry.style_signal` combines three measures: how much sentence length varies (standard deviation over mean), how varied the vocabulary is (unique words over total words), and how much and what kind of punctuation is used. Each is put on a 0–1 scale and pointed the same way, so higher means more AI-like.

**Why that might differ between human and AI writing:** Generated prose tends toward even, mid-length sentences and a narrower band of vocabulary, because "most likely next word" produces that on average. Human writing is lumpier: a three-word sentence next to a forty-word one, a semicolon or a dash where a model would use a comma.

**What it can't see:** It has no idea what the text says. Anything that changes the shape without changing the substance moves it: adding typos, splitting long sentences into short ones, pasting in a quotation, or sprinkling in dashes. That is cheap to do on purpose. It also depends on length: vocabulary variety falls as text gets longer, and a one- or two-sentence submission has almost no sentence-length spread to measure, so short texts get a weak reading.


### The combining rule

**The rule:** A weighted average of the two signals, with signal one (the model) weighted a little higher than signal two (style). One extra rule protects against wrong accusations: if the two signals disagree by more than 0.4, the combined score is capped just below the AI threshold. When two different methods disagree that strongly, the system can call the text "unsure" but never "AI."

**The numbers:**

| Signal | Weight |
|---|---|
| Model signal | 0.55 |
| Style signal | 0.45 |

Disagreement cap: if |model − style| > 0.4, the combined score is capped at just below `AI_THRESHOLD`.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

[Fill in from your Milestone 4 calibration runs, for example: "My plainly written human paragraph scored model 0.__ and style 0.__. The weighted average was 0.__, and because the two differ by 0.__, the cap kept it out of the AI label, so it was labelled 'unsure' instead of AI."]

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.45 | "This looks like it was written by a person. Our check found the patterns we usually see in human writing." |
| unsure | 0.45 – 0.72 | "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review." |
| high-confidence AI | 0.72 – 1.00 | "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this." |

**Why I worded the "unsure" one this way:**

The person reading "unsure" may well have written every word themselves. My own calibration showed a plain human paragraph scoring almost the same as AI text, and "unsure" is exactly where writers like that will land. So the label says plainly that the system couldn't tell, and doesn't hint at suspicion. "A lot of genuine writing looks like this" tells both the writer and anyone else reading it that this label is common and not an accusation. It names the review option as something the writer can choose, not something they have to do to clear their name. I avoided words like "flagged," "suspicious," "detected," and any numbers or confidence scores, because a reader who has never heard the word "threshold" would read a number like 0.68 as "68% likely to be AI," which isn't what it means.

---

## Sample Run

**A submission**

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel like human is trying to make their lives so complicated. Before we only need to find food and a shelter that is enough for having a happy life. However, nowadays, we have so many things that we have to worried about. For example, we need to make enough money, we need to maintain our social relationship, we need to make sure everything goes smoothly, etc. I don't know if we're going in the right direction as so many of us feel lost sometimes. We're too worried about running toward the standard of the society. I hope we can get out of our own trap one day.", "creator_id": "Bob"}'
```

```json
{
  "confidence": 0.6836,
  "content_id": "095941bd-5373-429b-90d5-9d55903f3b9d",
  "guess": "unsure",
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "model_score": 0.7576,
  "status": "decided",
  "style_score": 0.5931
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "095941bd-5373-429b-90d5-9d55903f3b9d", "reasoning": "I wrote this myself. English is my second language, so I use simple words and short sentences."}'
```

```json
{
  "content_id": "095941bd-5373-429b-90d5-9d55903f3b9d",
  "message": "Thanks. Your appeal has been recorded and a person will review this decision.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=10"
```

```json
{
  "count": 8,
  "entries": [
    {
      "combined_score": null,
      "content_id": "fd8a7106-2d4b-41cc-8884-46d3308937bc",
      "creator_id": "sample1",
      "guess": "unsure",
      "label": "PLACEHOLDER \u2014 label comes in Milestone 5.",
      "model_score": 0.7407,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-02T03:09:48+00:00"
    },
    {
      "combined_score": null,
      "content_id": "f54a43f0-eaff-4e82-a985-aad3b9199ae9",
      "creator_id": "sample2",
      "guess": "unsure",
      "label": "PLACEHOLDER \u2014 label comes in Milestone 5.",
      "model_score": 0.4566,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-02T03:12:36+00:00"
    },
    {
      "combined_score": null,
      "content_id": "20b85fe7-afb6-419f-87f3-ff6d5f6a2d87",
      "creator_id": "sample3",
      "guess": "unsure",
      "label": "PLACEHOLDER \u2014 label comes in Milestone 5.",
      "model_score": 0.7576,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-02T03:13:18+00:00"
    },
    {
      "creator_id": "sample1",
      "event": "rejected",
      "reason": "empty_text",
      "status": "rejected",
      "timestamp": "2026-11-02T03:18:02+00:00"
    },
    {
      "combined_score": 0.4201,
      "content_id": "c9a3140b-b24b-48dd-8267-4467c2da2d42",
      "creator_id": "Alex",
      "guess": "human",
      "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
      "model_score": 0.4566,
      "status": "decided",
      "style_score": 0.3755,
      "timestamp": "2026-11-02T05:22:43+00:00"
    },
    {
      "combined_score": 0.6836,
      "content_id": "095941bd-5373-429b-90d5-9d55903f3b9d",
      "creator_id": "Bob",
      "guess": "unsure",
      "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
      "model_score": 0.7576,
      "status": "decided",
      "style_score": 0.5931,
      "timestamp": "2026-11-02T05:22:58+00:00"
    },
    {
      "combined_score": 0.7536,
      "content_id": "f4cb6e23-8186-4986-b49d-515078fcd548",
      "creator_id": "Carol",
      "guess": "ai",
      "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
      "model_score": 0.7628,
      "status": "decided",
      "style_score": 0.7423,
      "timestamp": "2026-11-02T05:23:45+00:00"
    },
    {
      "content_id": "095941bd-5373-429b-90d5-9d55903f3b9d",
      "creator_id": "Bob",
      "event": "appeal",
      "reasoning": "I wrote this myself. English is my second language, so I use simple words and short sentences.",
      "status": "under_review",
      "timestamp": "2026-11-02T05:26:08+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I wrote a plain paragraph myself (sample 3: short sentences, everyday words, the way a second-language writer might write) and asked Claude to help me check whether signal one would call it AI. That's the false-positive case I describe under signal one's blind spot.
- *What came back:* My own paragraph scored 0.758 on signal one, almost identical to a clearly AI-written paragraph (0.763), while a more personal, specific paragraph I wrote scored 0.457. Claude pointed out that on signal one alone no threshold could separate my plain writing from the AI text, and that the style signal and combining rule would have to protect writers like this.
- *What I changed:* I added the three scores to my README as evidence for signal one's blind spot. When I set my thresholds, I put the AI threshold at 0.72, above the 0.68 combined score my plain paragraph got, so writing like it lands in "unsure" instead of being called AI. I also wrote the "unsure" label to say clearly that it isn't an accusation and that the writer can ask for a review.

**Moment 2**

- *What I asked for:* I was deciding how to weight the model signal against the style signal. I leaned toward giving style more weight, because AI writing often sounds formal and polished, but I also knew the model signal mattered, so I asked Claude to help me reason it through.
- *What came back:* Claude suggested weighting the model signal slightly higher (0.55 model, 0.45 style) instead of leaning toward style. Its reasoning: the style signal can't read, so cheap changes like typos or split sentences move it, and in my calibration one of its three measures (vocabulary variety) pointed the wrong way, giving my plain human paragraph a more AI-like score than the actual AI text. It also suggested a disagreement rule: if the two signals differ by more than 0.4, the combined score is capped below the AI threshold, so two methods disagreeing can produce "unsure" but never an accusation.
- *What I changed:* I tested my assumption that formal means AI with a formal paragraph I wrote myself. Its style score was 0.456, slightly on the human side, so formal style alone doesn't mark text as AI, and I dropped the idea of weighting style higher. I kept 0.55 / 0.45 with the disagreement cap, and inside the style signal I gave vocabulary variety the lowest weight (0.15), since it was the measure that worked against plain writers.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
