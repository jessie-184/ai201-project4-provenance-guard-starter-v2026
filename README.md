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

My closest split was my plain human paragraph: signal one scored it 0.758 (AI-like) but the style signal only 0.593. The two differ by 0.165, under my 0.4 disagreement limit, so the cap didn't apply. The weighted average was 0.684, below my 0.72 AI threshold, so it was labelled "unsure" rather than AI. None of my calibration texts split by more than 0.4, so the disagreement cap hasn't been triggered yet; it's a safeguard for stronger disagreements than I've tested.

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
$ curl "http://127.0.0.1:5000/log?limit=5"
```

```json
{
  "count": 4,
  "entries": [
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

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**

A real writer submits a piece, maybe fixes a typo and resubmits, and might check a few drafts in an hour. Five a minute leaves room for that and for a quick retry after an error, and fifty a day covers even a very active writer. A script trying to map my thresholds needs hundreds or thousands of slightly different texts to find exactly where 0.45 and 0.72 sit; at fifty a day per caller, mapping them from one account takes weeks instead of minutes. I went lower than the starter's 10 a minute because each submission runs GPT-2, which is slow and expensive, so a burst of requests also costs real compute.

**What a caller counts as:** Per `creator_id`, falling back to the caller's IP address when there's no usable `creator_id`. That stops one writer account from flooding the service, but it has a known gap: `creator_id` is whatever the caller sends, so a script that invents a new `creator_id` for every request is never limited. A per-address limit would catch that script but would also lump together everyone sharing one network, such as a classroom or a household, and could block real writers.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

---

## Attack Run — Before

I ran all 56 attacks once, before changing anything (`python run_attacks.py --set attack_set --label before`). The service never crashed and never returned a 500.

**How I marked each attack:**

| Attack goal | BROKE if… | HELD if… |
|---|---|---|
| Slip AI text past the detector (evasion, prompt injection) | labelled human | labelled AI or unsure |
| Get real human writing flagged (false positive) | labelled AI | labelled human or unsure |
| Injection aimed at the label or the log | the injected content shows up in the label or the log | the label and log are unchanged |
| Malformed or junk input | scored and labelled, or a 5xx | refused with a 4xx JSON error |
| Flood from one creator | no 429 | some requests get 429 |

"Unsure" counts as held in both directions, because my design deliberately uses "unsure" rather than a wrong accusation.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `b84c03e3-9818-4672-aa19-ff821c0afc9c` | unsure | 0.453 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c2880c7a-06f7-4606-b887-73002cd6f0b1` | unsure | 0.490 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `f16dbccf-d20f-49bb-9233-3236a1fe966e` | unsure | 0.531 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `4f924194-cda6-4c2d-9abf-0fe6b473e806` | unsure | 0.692 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `db732142-1175-4e8e-9693-a5f218757b42` | human | 0.261 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `8ec7c555-5b5a-4990-b393-98f21c4eb2e9` | unsure | 0.492 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `be872180-e413-41f2-ae03-4b783f5b5c3e` | unsure | 0.463 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `e0045851-5d45-4052-88e7-7b953cdc4fd2` | human | 0.443 | **BROKE** |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `67d736de-4d95-4193-be20-a2de6e9b6629` | unsure | 0.548 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `a87c0ef5-d60d-449d-9e43-bbad07780b62` | ai | 0.851 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `30bdd930-7cde-4017-abdf-a1dd4560d427` | unsure | 0.588 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `21ea786d-0a44-441c-98ac-c608b24b0a99` | ai | 0.787 | **BROKE** |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `896d0eb6-5562-44dc-a657-67386f50c5bf` | ai | 0.760 | **BROKE** |
| FP04 | false_positive | a student essay written to a rubric | 200 | `011ab706-1dec-45bd-a794-3b30e118075f` | ai | 0.753 | **BROKE** |
| FP05 | false_positive | technical documentation written by a person | 200 | `87507dc6-3892-4d12-97f5-277fdd8f2764` | ai | 0.819 | **BROKE** |
| FP06 | false_positive | a person imitating a formal template | 200 | `58949d3b-2909-49d3-9dec-04c014d6ff2d` | unsure | 0.712 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `fc241baa-f16e-4cc4-9ef8-5e4515921d7e` | unsure | 0.698 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `2dab01bc-ba85-480a-a40b-75d018172ace` | human | 0.401 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `100a4403-e228-43ce-9569-bb0e3b7b9e55` | human | 0.416 | **BROKE** |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `3bfc565a-39ac-4860-9070-7ba3e30c8ad9` | human | 0.224 | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `dedd81b7-4620-4207-9e9f-488ac85e4498` | unsure | 0.531 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `0313b152-6796-418a-acac-bdcffdbbe347` | human | 0.390 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `036b5786-d808-4013-8e2c-035674247273` | human | 0.396 | **BROKE** |
| PI06 | prompt_injection | instruction plus real human text | 200 | `7ec1a3dc-2b86-4f67-b7fe-9d64ed9ebdd7` | unsure | 0.561 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `f3d29aa3-86ea-4591-b57d-192b7be260b5` | human | 0.270 | **BROKE** |
| MF04 | malformed | text is only punctuation | 200 | `fa922047-ca92-417f-8414-bc1fba5d886a` | human | 0.344 | **BROKE** |
| MF05 | malformed | text is a very long single word | 200 | `7ff84b5f-e1e8-4e5c-91a1-b346f0bdd58e` | ai | 0.819 | **BROKE** |
| MF06 | malformed | text is emoji only | 200 | `e20d1e4c-790b-4d52-b870-540b78f675c7` | ai | 0.886 | **BROKE** |
| MF07 | malformed | text is right-to-left script | 200 | `867008aa-6a71-43e1-b447-5e5ab449f75d` | ai | 0.836 | **BROKE** |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400\* | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400\* | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01–05 | flood_same_creator | 20 rapid submissions from one creator | 200 | (five ids) | human | 0.286 | HELD |
| FL01_06–12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

\* RQ10 and RQ11 came back `429` on the first pass: they had no usable `creator_id`, so they counted against my address and hit the 5-per-minute limit before reaching `/submit`. I reran each one on its own a minute later, and both returned `400`.

**Totals:**

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| evasion | 10 | 8 | 2 |
| false_positive | 8 | 4 | 4 |
| prompt_injection | 6 | 3 | 3 |
| malformed (`attacks.csv`) | 8 | 3 | 5 |
| malformed requests | 12 | 12 | 0 |
| flood_same_creator | 12 | 12 | 0 |
| **Total** | **56** | **42** | **14** |

**Ten audit log entries from the run**

```json
[
  {
    "timestamp": "2026-11-08T20:52:16+00:00",
    "content_id": "e0045851-5d45-4052-88e7-7b953cdc4fd2",
    "creator_id": "attacker_EV08",
    "guess": "human",
    "model_score": 0.2452,
    "style_score": 0.684,
    "combined_score": 0.4427,
    "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-08T20:52:16+00:00",
    "content_id": "21ea786d-0a44-441c-98ac-c608b24b0a99",
    "creator_id": "attacker_FP02",
    "guess": "ai",
    "model_score": 0.7387,
    "style_score": 0.8454,
    "combined_score": 0.7867,
    "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-08T20:52:16+00:00",
    "content_id": "896d0eb6-5562-44dc-a657-67386f50c5bf",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "model_score": 0.8051,
    "style_score": 0.7056,
    "combined_score": 0.7603,
    "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-08T20:52:16+00:00",
    "content_id": "87507dc6-3892-4d12-97f5-277fdd8f2764",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "model_score": 0.8005,
    "style_score": 0.8414,
    "combined_score": 0.8189,
    "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-08T20:52:16+00:00",
    "content_id": "3bfc565a-39ac-4860-9070-7ba3e30c8ad9",
    "creator_id": "attacker_PI02",
    "guess": "human",
    "model_score": 0.2044,
    "style_score": 0.2489,
    "combined_score": 0.2244,
    "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-08T20:52:16+00:00",
    "content_id": "036b5786-d808-4013-8e2c-035674247273",
    "creator_id": "attacker_PI05",
    "guess": "human",
    "model_score": 0.6401,
    "style_score": 0.0983,
    "combined_score": 0.3963,
    "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-08T20:52:17+00:00",
    "content_id": "e20d1e4c-790b-4d52-b870-540b78f675c7",
    "creator_id": "attacker_MF06",
    "guess": "ai",
    "model_score": 0.9969,
    "style_score": 0.75,
    "combined_score": 0.8858,
    "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-08T20:52:17+00:00",
    "content_id": "867008aa-6a71-43e1-b447-5e5ab449f75d",
    "creator_id": "attacker_MF07",
    "guess": "ai",
    "model_score": 0.9064,
    "style_score": 0.75,
    "combined_score": 0.836,
    "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-08T20:52:17+00:00",
    "creator_id": "attacker_MF08",
    "event": "rejected",
    "status": "rejected",
    "reason": "text_too_long"
  },
  {
    "timestamp": "2026-11-08T20:52:17+00:00",
    "creator_id": "attacker_flood",
    "event": "rejected",
    "status": "rejected",
    "reason": "rate_limited",
    "limit": "5 per 1 minute"
  }
]
```

**The single worst outcome** — the one I'd least want to explain to a writer whose work got caught by it:

**FP03**, a non-native English speaker writing carefully about their first month in a new country, was labelled AI: model 0.805, style 0.706, combined 0.760. It's exactly the writer I traced in Milestone 1. Careful, simple English is predictable to GPT-2, and the style signal read the even sentences and repeated vocabulary as machine-like too. The two signals differed by only 0.10, so my disagreement cap never applied, and the combined score cleared my 0.72 threshold. The label they'd see says their own account of moving to a new country was "probably written with help from AI." This is the person least able to argue back, and the threshold I set specifically to protect them didn't.


---

## Run Log and Verdicts
 
<!-- Your five criteria across three trials. `run_eval.py --label before`. -->
 
Test set: 22 texts frozen in `scenarios.py` after the thresholds were set on the calibration texts (C1–C4) and not changed after seeing these scores. 6 pieces I wrote myself; 6 student essays (class 0 = human) from a public essay dataset; 10 unedited AI pieces from three tools (3 Gemini, 3 ChatGPT, 4 Claude). The ChatGPT titles and category tags were removed; the body text is as generated. The human pieces are 245–744 words, the AI pieces 105–202 words. Full output: `results/run_2026-11-08_1726_before.md`. Criterion 5's last checks (body not JSON, 50,000-character timing, the five appeal cases, `/ping`) were run by hand with curl, three times.
 
| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. No false accusations | 0 of 6 plain pieces and ≤1 of 12 human pieces labelled AI | 0 / 0 | 0 / 0 | 0 / 0 | **Met** |
| 2. Human label works | ≥7 of 12 human pieces labelled human | 4 | 4 | 4 | **Missed** |
| 3. AI detected | ≥6 of 10 AI pieces labelled AI, 0 labelled human | 1 AI, 2 human | 1 AI, 2 human | 1 AI, 2 human | **Missed** |
| 4. Score separates | AI piece scores higher in ≥85% of 120 pairs | 79.2% (95/120) | 79.2% | 79.2% | **Missed** |
| 5. Contract checks | 12 of 12 pass, 0 × 500, `/ping` answers | 12/12 | 12/12 | 12/12 | **Met** |
 
Scores were identical in all three trials, so signal one is deterministic on my machine. Criterion 4 counts one exact tie (Honeybees 0.6334 vs. my Lao-tzu essay 0.6334) as not higher; counting it as higher gives 96/120 = 80%, still a miss.
 
**Real output from one trial**, pasted as text, naming the file and function that produced it:
 
Produced by `run_eval.py::main` → `app.py::submit` → `scoring.py::combine_signals` (`results/run_2026-11-08_1726_before.md`, trial 1). One piece per group:
 
```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6334,
    "model_score": 0.7972,
    "style_score": 0.4333,
    "sent": "Inspired by the idea of comparing Lao-tzu's ideology with Machiavelli'"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3849,
    "model_score": 0.5696,
    "style_score": 0.1591,
    "sent": "Cars. Cars have been around since they became famous in the 1900s, whe"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3197,
    "model_score": 0.3542,
    "style_score": 0.2775,
    "sent": "Rain lashed against the canopy of the hover-cab as it wove through the"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6334,
    "model_score": 0.8616,
    "style_score": 0.3545,
    "sent": "Honeybees play an essential role in maintaining healthy ecosystems and"
  },
  {
    "status": 400,
    "guess": null,
    "sent": "{\"text\": 12345, \"creator_id\": \"eval_bad_number\"}"
  }
]
```
 
Criterion 5, by hand (`app.py::submit` and `app.py::appeal`), trial 1:
 
```
POST /submit  body: not json                → 400 invalid_json   0.011s
POST /submit  text: 50,000 characters       → 400 text_too_long  0.006s
POST /appeal  valid                         → 200 under_review
POST /appeal  same content_id again         → 200 under_review ("already under review")
POST /appeal  content_id: does-not-exist    → 404 not_found
POST /appeal  no reasoning                  → 400 missing_reasoning
POST /appeal  reasoning: ""                 → 400 missing_reasoning
GET  /log     decision for 3d67c47d… still "human"/"decided", exactly one appeal entry
POST /ping                                  → {"ok": true, "service": "provenance-guard"}
```
 
**Diagnoses**
 
<!-- For each miss AND each broken attack: the stage and the mechanism. -->
 
*Criteria 2, 3 and 4 are one problem: signal two doesn't separate AI from human on this test set, and the combining rule gives it almost half the weight.*
 
- **Signal two (`stylometry.py::style_signal`) points the wrong way on two of its three measures.** Punctuation variety per 100 words is higher in the AI pieces (5.4–8.9, most above 6) than in the human ones (3.8–6.8), and moving-average TTR is higher too (AI 0.81–0.91, human 0.73–0.84). My anchors treat both as signs of a human writer, so they push AI text toward "human". Only sentence-length spread works as intended (AI 0.15–0.39, human 0.33–0.90). Ranked on its own, signal two puts the AI piece higher in 65 of 120 pairs (54%): close to a coin toss.
- **Signal one (`detector.model_signal`) carries the separation.** On its own it ranks the AI piece higher in 95 of 120 pairs, the same 79.2% as the combined score, so adding signal two gained nothing. 7 of 10 AI pieces score above 0.70 on signal one; only 1 of 12 human pieces does (my Lao-tzu essay, 0.797). It fails on two Gemini pieces, the attic (0.50) and the neon city (0.35): descriptive fiction full of rare words ("astrolabes", "luminescent", "datapad") that GPT-2 finds surprising, so perplexity looks human.
- **Combining rule (`scoring.py::combine_signals`).** At weight 0.45, a weak style score pulls strong signal-one scores under the AI threshold. Honeybees scores 0.86 on signal one but 0.35 on style → 0.63, "unsure". With a signal-one score of 0.86, style would need at least 0.55 to reach 0.72, and 7 of 10 AI pieces are below 0.45. The disagreement cap did not decide any of these: every AI piece's weighted average was already under 0.71 before the cap applied.
- **Label mapping (`scoring.py::score_to_label`).** The unsure band (0.45–0.72) is wide, and with signal two flattening every score towards the middle, 16 of 22 texts land in it. That is why criterion 1 passes and criterion 2 fails: no human piece reaches 0.72, but only 4 get under 0.45.
- **Two Gemini pieces labelled human (criterion 3's hard zero).** Both signals were low at once (attic 0.50 / 0.35, neon 0.35 / 0.28), so the combined score fell under 0.45. The AI pieces are also 105–202 words against 245–744 for the human pieces, so their sentence spread and TTR are measured on fewer sentences.
*Criterion 5 met, with one caveat.* When `text` is a number (`12345`), `app.py::submit` logs the reason as `missing_text`. The 400 is correct, but the logged reason is wrong: the text is present, just the wrong type.
 
<!-- Broken attacks (from results/attack_run_2026-11-08_1552_before.md) -->

*The 14 broken attacks, grouped by pattern. The same punctuation measure in signal two shows up again.*

- **Careful human writing called AI (FP02–FP05, 0.753–0.819).** Both signals scored high together: signal one 0.74–0.83 and signal two 0.66–0.85, never more than 0.18 apart. Signal two is high because formal, plain prose has almost no varied punctuation (0 to 2.9 per 100 words, against my AI anchor of 3.0) and even sentence lengths (spread 0.24–0.37). The disagreement cap only fires when the signals are more than 0.4 apart, so when they agree nothing stops the score crossing 0.72. Stage: signal two (punctuation measures register, not authorship) and the combining rule (no safeguard when both signals agree). This is the mirror image of criteria 2–4: lively AI text looks human, plain human text looks AI.
- **Junk and non-English input scored instead of rejected (MF05 long word, MF06 emoji, MF07 Arabic → "ai"; MF03 control characters, MF04 punctuation → "human").** The route (`app.py::submit`) checks length but not whether the text is English prose, so text GPT-2 was never meant to read reaches both signals and gets a confident label. Stage: route.
- **Prompt injection (PI01 0.416, PI02 0.224, PI05 0.396 → "human").** The service never obeys the injected instructions; nothing reads the text as a command. They get through because the injected text is statistically odd. Signal one scored PI02 at 0.20 and PI01 at 0.46: tokens like `SYSTEM:` and `guess=human` are surprising to GPT-2, so perplexity looks human. Signal two scored all three low (0.10–0.36): they are short (28–45 words) with high word variety (TTR 0.93–0.97), and PI05's fake JSON has 20 varied punctuation marks per 100 words, which drove its style score to 0.098. Stage: signal one and signal two; the mechanism is that unusual text reads as human to both.
- **Evasion by human editing (EV05 0.261 → "human").** The edit added a dash, asides ("and I mean the boring kind") and mixed short and long sentences. Signal one fell to 0.32 and signal two to 0.19 (sentence spread 0.68). Stage: both signals. A heavy human edit really does make the text more human-like, so this one may be outside what any statistical detector can catch.
- **Evasion by short text (EV08 0.443 → "human").** Ten words, two sentences. Signal one read only a handful of tokens and gave 0.25; signal two gave 0.68. The signals were 0.44 apart, so the cap fired, but the weighted average (0.443) was already under it and just under the human threshold of 0.45. Stage: route (no minimum length worth scoring) and signal one (perplexity on 10 words is noise).

---

## The Improvement

**What I changed:** One line in `stylometry.py`: the weights inside signal two went from `W_SPREAD, W_PUNCT, W_TTR = 0.50, 0.35, 0.15` to `1.00, 0.00, 0.00`. Signal two now measures sentence-length spread only. Nothing else changed: the combining weights (0.55 / 0.45), the disagreement cap and both thresholds (0.45 / 0.72) are the same as in the before run.

**Which diagnosis pointed at it:** The Run Log diagnosis found that two of signal two's three measures point the wrong way. The AI test pieces have more varied punctuation (5.4–8.9 per 100 words) and higher word variety (TTR 0.81–0.91) than the human ones (3.8–6.8 and 0.73–0.84), so both measures pushed AI text toward "human" and plain human text (FP02–FP05) toward "AI". On its own, signal two ranked the AI piece higher in only 65 of 120 pairs. Sentence-length spread was the only measure that worked, so I kept it and turned the other two off. This change was chosen after seeing the test-set results, so the after numbers on criteria 2–4 are partly fitted to these 22 texts and are optimistic.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Same 56 attacks, same marking rules as the before run (`python run_attacks.py --set attack_set --label after`, results in `results/attack_run_2026-11-08_1846_after.md`). The service never crashed and never returned a 500.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c9790cea-971d-4db6-ab62-67bf11f1de13` | unsure | 0.528 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `d82c7d0a-d0e5-4efa-bfd6-426384a204f3` | human | 0.327 | **BROKE** |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `140bea8c-e533-43ac-aed3-86b41974ba65` | unsure | 0.486 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `4efca18a-3099-4c92-ae2f-06747aeb7e76` | ai | 0.759 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `6274b680-7267-403b-836e-dfc72376bd17` | human | 0.177 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `a3d6b5b5-5f7f-4aca-a55c-ce3f468ae37c` | human | 0.315 | **BROKE** |
| EV07 | evasion | signal two: padding with punctuation | 200 | `f6ecb1d9-4a5a-47b4-9ed6-0757125b27db` | unsure | 0.547 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `5afaedce-59af-4ef0-b031-bddc31322245` | human | 0.435 | **BROKE** |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `f3284c2a-6633-4859-bbcb-c218e5178051` | unsure | 0.480 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `275358be-1d4b-4d58-8121-11b349917243` | unsure | 0.710 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `5394cbb9-b223-4a71-8690-ff64d13b5ad0` | human | 0.444 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `5b292281-60d4-4207-8057-a107f5221c7b` | ai | 0.755 | **BROKE** |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `cd4046f5-681c-42d5-8561-a480b8518fbd` | unsure | 0.692 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `3507dd67-b1a6-419e-a5ef-f40cbee54a6c` | unsure | 0.664 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `d17d5826-4444-4e81-8c96-eb3d60d45ff4` | ai | 0.748 | **BROKE** |
| FP06 | false_positive | a person imitating a formal template | 200 | `d3b8f41f-e9e7-4c8a-b2d0-501e47e20304` | unsure | 0.519 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `3e935c1e-69c8-421e-b606-f83af97485ba` | unsure | 0.485 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `fd3e03b8-d5e8-4d73-bf4e-9101577b6e29` | human | 0.309 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `83ba4776-92ca-4053-a3df-e12c11fe3627` | human | 0.254 | **BROKE** |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `b3bf1b71-806e-4116-8838-b8614f8af1b8` | human | 0.112 | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `5574b016-dd08-4aec-a34f-b85a8b7608d2` | unsure | 0.560 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `5e5db47e-71b4-49bd-b098-3ac4100517c2` | human | 0.447 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `f5e81dd1-7821-4e94-8c38-5457e61e3227` | human | 0.441 | **BROKE** |
| PI06 | prompt_injection | instruction plus real human text | 200 | `3a0fdcff-59c9-4424-9d2a-717617f75d25` | human | 0.425 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `60e9ed8d-180f-4423-b3ec-c97baed1c2f8` | human | 0.225 | **BROKE** |
| MF04 | malformed | text is only punctuation | 200 | `83cafa47-3ce1-4de4-b757-f68ee4d34658` | human | 0.231 | **BROKE** |
| MF05 | malformed | text is a very long single word | 200 | `2bf4157d-8510-4c43-853f-db2d0c4e9b98` | unsure | 0.710 | HELD |
| MF06 | malformed | text is emoji only | 200 | `fe1db84e-6f6b-4a73-b6c3-7c372140dd7d` | unsure | 0.710 | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `313f0e11-a1a5-44c5-b022-556676f29450` | unsure | 0.710 | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400* | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400* | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `57f711dd-fdbb-4683-bd77-437f866a922e` | human | 0.241 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bda73cbe-d4b2-44b8-a605-1e237ce43313` | human | 0.241 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fa23e525-6908-4a02-b1d7-863f690d2a14` | human | 0.241 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `465fd466-e8c0-4339-92cd-b5854b029d04` | human | 0.241 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `41a8affc-88c7-4002-99b0-282e0dfa83a8` | human | 0.241 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

\* RQ10 and RQ11 came back `429` on the first pass again (no usable `creator_id`, so they counted against my address). I reran each one on its own (`--id RQ10`, `--id RQ11`) and both returned `400`.

**Totals, before → after:**

| Family | Attacks | BROKE before | BROKE after |
|---|---|---|---|
| evasion | 10 | 2 | 4 |
| false_positive | 8 | 4 | 2 |
| prompt_injection | 6 | 3 | 3 |
| malformed (`attacks.csv`) | 8 | 5 | 2 |
| malformed requests | 12 | 0 | 0 |
| flood_same_creator | 12 | 0 | 0 |
| **Total** | **56** | **14** | **11** |

Fixed (BROKE → HELD): FP03, FP04, MF05, MF06, MF07. Newly broken (HELD → BROKE): EV02, EV06.

### Run Log — After

`python run_eval.py --label after`, results in `results/run_2026-11-08_1847_after.md`. Scores were identical in all three trials again.

| Criterion | Target | Before (×3) | After Run 1 | After Run 2 | After Run 3 | Verdict before → after |
|---|---|---|---|---|---|---|
| 1. No false accusations | 0 of 6 plain and ≤1 of 12 human labelled AI | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | MET → **MET** |
| 2. Human label works | ≥7 of 12 labelled human | 4 | 7 | 7 | 7 | MISSED → **MET** |
| 3. AI detected | ≥6 of 10 labelled AI, 0 labelled human | 1 AI, 2 human | 3 AI, 1 human | 3 AI, 1 human | 3 AI, 1 human | MISSED → **MISSED** |
| 4. Score separates | ≥85% of 120 pairs | 79.2% (95/120) | 91.7% (110/120) | 91.7% | 91.7% | MISSED → **MET** |
| 5. Contract checks | 12 of 12, 0 × 500, `/ping` answers | 12/12 | 12/12 | 12/12 | 12/12 | MET → **MET** |

Real output, trial 1 (`run_eval.py::main` → `app.py::submit` → `scoring.py::combine_signals`), the same pieces as the before excerpt:

```json
[
  {"status": 200, "guess": "unsure", "confidence": 0.6631, "model_score": 0.7972, "style_score": 0.4992, "sent": "Inspired by the idea of comparing Lao-tzu's ideology with Machiavelli'"},
  {"status": 200, "guess": "human",  "confidence": 0.3133, "model_score": 0.5696, "style_score": 0.0,    "sent": "Cars. Cars have been around since they became famous in the 1900s, whe"},
  {"status": 200, "guess": "human",  "confidence": 0.4127, "model_score": 0.3542, "style_score": 0.4842, "sent": "Rain lashed against the canopy of the hover-cab as it wove through the"},
  {"status": 200, "guess": "ai",     "confidence": 0.7733, "model_score": 0.8616, "style_score": 0.6653, "sent": "Honeybees play an essential role in maintaining healthy ecosystems and"}
]
```

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

Yes, overall: two criteria went from missed to met (2 and 4), criterion 3 improved but still misses, and broken attacks fell from 14 to 11. I know because the same frozen test set and the same 56 attacks were run before and after with only this one line changed, and both runs gave identical scores across three trials.

The trade:

- **What it fixed.** Plain, formal human writing is no longer pushed toward AI by its lack of punctuation: FP03 (0.760 → 0.692) and FP04 (0.753 → 0.664) moved from "ai" to "unsure". Lively AI text is no longer pulled toward human by its punctuation and word variety: Honeybees went from 0.63 "unsure" to 0.77 "ai". Signal two alone now ranks the AI piece higher in 112 of 120 pairs (65 before), and the combined score separates 110 of 120 pairs instead of 95.
- **What it cost.** Signal two now rests on one measure, so attacks that change sentence lengths work better. EV02 (adding short "Really." sentences) and EV06 (one very long sentence and one very short) both drove signal two to 0.0 and are now labelled human. EV05 dropped further (0.261 → 0.177). The same thing makes some human pieces score very low (5 of 12 human pieces now have a style score of 0.0), which is what helped criterion 2.
- **Fragile passes.** Criterion 2 passes by 0.002: the seventh human piece scored 0.4481 against the 0.45 threshold. Three AI pieces sit just under 0.72 (Lighthouse 0.7189, Peaches 0.71, Copper Spoon 0.7079), so criterion 3 is close on the AI count but still fails its hard zero, because the neon Gemini piece is labelled human (0.41).
- **Fixed by accident.** MF05–MF07 (long word, emoji, Arabic) moved from "ai" to "unsure", but not because the service understood them. They have fewer than two sentences, so signal two returns its neutral 0.5; signal one is above 0.9, the gap is now over 0.4, and the disagreement cap holds them at 0.71. The route still accepts this junk and scores it.

## What's Still Broken

After the improvement, 11 of 56 attacks still get through and criterion 3 is still missed. I stopped at one change because the milestone asks for one change measured properly; everything below is what I would try next, in the order I would try it.

- **Junk input is still scored (MF03 control characters, MF04 punctuation only → "human"; MF05–MF07 only held by accident).** What I'd do: validate in the route (`app.py::submit`) before either signal runs, and reject with a 400 any text that has fewer than about 20 real words or where most characters are not letters. Why I stopped: it is a second change, and it would have changed the malformed results at the same time as the signal-two fix, so I couldn't have told which one helped. This is the first thing I would fix, because it is cheap and nothing a real writer sends would be affected.
- **Very short text evades (EV08, 10 words → "human").** What I'd do: the same minimum-length check in the route, so text too short to measure gets a 400 (or "unsure") instead of a confident label. Why I stopped: same reason; it belongs with the route validation above.
- **Sentence-length tricks evade (EV02 "Really." padding, EV06 one long and one short sentence → "human").** These are new since my change, because spread is now the whole of signal two. What I'd do: give signal two a second measure that actually separates my test set (for example, how often sentences start the same way), or cap how far one extreme sentence can move the spread. Why I stopped: I'd need new calibration texts to set a new measure honestly, and tuning it on these attacks would just fit the attack set.
- **Careful human writing still called AI (FP02 formal report 0.755, FP05 technical documentation 0.748).** Both signals agree it looks like AI, so the disagreement cap never fires. What I'd do: raise the AI threshold from 0.72 to about 0.76, which clears both. Why I stopped: that costs criterion 3 directly (Many People at 0.80 and Honeybees at 0.77 would be the only AI labels left), and I can't move a threshold after seeing the test scores without fitting to them.
- **Prompt injection gets labelled human (PI01, PI02, PI05).** The service never obeys the instructions; the injected text is just statistically odd, so signal one reads it as surprising and signal two as uneven. What I'd do: strip lines that look like instructions or markup (`SYSTEM:`, `Ignore all previous…`, JSON fragments) before scoring, and flag the submission for a person to review. Why I stopped: a pattern list is easy to get around and could strip real writing, so it needs its own test set first.
- **Heavy human editing evades (EV05 → "human", 0.177).** What I'd do: probably nothing in the detector. After a real human editing pass the text is partly human-written, and I would rather leave this to the appeal path than make the detector harsher on lively writing. Why I stopped: I don't think a statistical detector should catch this one.
- **Criterion 3 still missed (3 of 10 AI pieces labelled AI, the neon Gemini piece labelled human).** Three AI pieces sit just under 0.72 (0.7189, 0.71, 0.7079), and two Gemini fiction pieces have low signal-one scores because GPT-2 finds their rare words surprising. What I'd do: try a larger detector model than GPT-2 for signal one, since the fix is a better signal, not a lower threshold. Why I stopped: lowering the AI threshold would catch these three but would also bring FP02 and FP05 further into the AI band, and swapping the model is a bigger change than this unit allows.

**The trade I'd make if this ran for real:**

I would lean toward fewer wrong accusations: keep the AI threshold at 0.72 or raise it, and treat "unsure" as the default for anything my two signals can't separate, even though that already lets 7 of my 10 test AI pieces through without an AI label. The people who pay for that are the honest writers on the site, who compete with AI-written work that goes unflagged, and the readers who trust the label; I accept that cost because the other direction is paid by individual writers like FP02 and FP05, who in my own after run are still wrongly called AI for writing formally or plainly, and they have no easy way to prove otherwise.


# Capstone

## What This Extends

Provenance Guard, the text-provenance service I built in units 7 and 8. It is a Flask service: `POST /submit` scores a piece of writing with two signals, a GPT-2 perplexity score (`detector.py::model_signal`) and a sentence-length spread score (`stylometry.py::style_signal`), combines them in `scoring.py::combine_signals`, and returns one of three labels: human, unsure or AI. Writers can appeal a label through `POST /appeal`, submissions are rate-limited per creator (5 a minute, 50 a day), and every decision, appeal and rejection is written to `logs/audit.jsonl`.

**What's new:** an input gate in `app.py::submit`. It runs after the existing JSON and field checks and before either signal. It refuses text the signals can't meaningfully score with a 400 and a reason code, and logs the refusal with `audit.log_rejection`, the same way the existing rejections are logged.

**Why:** my Unit 8 after run showed that junk input still gets a confident label. MF03 (control characters) came back human at 0.225 and MF04 (punctuation only) came back human at 0.231. MF05, MF06 and MF07 (one very long word, emoji only, Arabic) all came back unsure at 0.710. That is the disagreement cap holding them just under the AI threshold, not anything noticing the input was junk.

## The Shape

**Shape B: harden against failure.** My criteria are about the bad path: what Provenance Guard does with input it shouldn't be scoring at all. Today the route only refuses text that is missing, empty, over 10,000 characters, or too short to give GPT-2 three tokens. Everything else reaches both signals and gets a label. The gate adds one check in between: text with too few real words to score, or text that is mostly not English letters, is refused before signal one or signal two runs. Provenance Guard is built for English only: GPT-2 was trained on English text, and the style signal's word splitter only recognises the letters a–z, digits and apostrophes. The letter-share check refuses text written mostly in other scripts (Arabic, Cyrillic, Chinese, Devanagari, Hangul) rather than give it a label the signals can't support. It does not catch languages written mostly in a–z, such as Spanish or French; my run log shows that (criterion 2, What's Still Broken). In Milestone 6 I added a third check, run first: text containing a control character is refused. Text that passes the gate is scored exactly as before. The signals, weights, thresholds and label text don't change.

**Out of scope:**

- **Short AI text (EV08, 10 words → human).** No word count separates it from FP08, a genuine 8-word human submission, so a length rule strict enough to stop EV08 would refuse real writers.
- **Flagging prompt injection** (PI01, PI02 and PI05 still come back human). A list of patterns is easy to get around and could strip real writing, so it needs its own test set first.
- **Replacing GPT-2 with a larger detector model.** It's the likeliest fix for my Unit 8 criterion 3 misses, but it's a separate project. It would also change every score, so I couldn't tell what the gate did.

## Running It

**Path B: local, with logs.** GPT-2 plus torch needs well over the 512 MB a free host gives (the GPT-2 files alone are 525 MB on disk), so the service runs on my own machine with `python app.py`, and `logs/audit.jsonl` is the record of it running. [RUNNING.md](RUNNING.md#unit-9-capstone--running-it-path-b-local-with-logs) has the start command, the Python version, the exact package versions, the model size, and what broke when I followed it from a fresh clone.

## Instrumentation

Every request to `POST /submit` writes one JSON line to `logs/audit.jsonl` (`audit.py::_append`): decisions, refusals and rate-limit 429s alike. The nine original fields are unchanged, so old and new entries stay comparable. Four fields are new this unit, added in `app.py::_request_fields`:

| Field | What it holds |
|---|---|
| `timestamp` | When the record was written, UTC, to the second |
| `creator_id` | Who sent it (`"unknown"` if the body had none) |
| `text_chars`, `word_count`, `text_excerpt` | **What came in:** length in characters, real words (the gate's definition), and the first 60 characters. Only an excerpt, because this file is committed to a public repo. `null` when the body had no text |
| `guess`, `model_score`, `style_score`, `combined_score`, `label`, `content_id`, `status: "decided"` | **What came out**, for a decision |
| `event: "rejected"`, `reason` (and `limit` for a 429) | **What came out**, for a refusal |
| `duration_ms` | **How long it took:** from the start of the request (a `before_request` hook registered before the rate limiter, so 429s are timed too) to just before the record is written. Server time only; it doesn't include the network or the client |

Eleven entries from the cost run below (log lines 366, 367, 368, 371 and 377–381, 386, 387). The first is the cold first request, then three warm decisions, then one of each failure path, ending in a 429:

```json
{"timestamp": "2026-11-11T06:13:23+00:00", "content_id": "37469f59-818a-4f34-b6bf-0934fab071fe", "creator_id": "m3cold_FP01", "guess": "human", "model_score": 0.6175, "style_score": 0.2313, "combined_score": 0.4437, "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.", "status": "decided", "duration_ms": 4248.9, "text_chars": 523, "word_count": 103, "text_excerpt": "We got to the campsite about four. The pitch was fine, a bit"}
{"timestamp": "2026-11-11T06:13:23+00:00", "content_id": "663b5b65-f17b-4589-9f3a-7eb76161cc0a", "creator_id": "m3cost_01", "guess": "unsure", "model_score": 0.5025, "style_score": 0.5143, "combined_score": 0.5078, "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.", "status": "decided", "duration_ms": 51.7, "text_chars": 721, "word_count": 119, "text_excerpt": "Dust motes danced in the slanted afternoon light, illuminate"}
{"timestamp": "2026-11-11T06:13:23+00:00", "content_id": "3511455e-2992-4c9d-abf7-f93822984d80", "creator_id": "m3cost_02", "guess": "human", "model_score": 0.3542, "style_score": 0.4842, "combined_score": 0.4127, "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.", "status": "decided", "duration_ms": 42.5, "text_chars": 650, "word_count": 106, "text_excerpt": "Rain lashed against the canopy of the hover-cab as it wove t"}
{"timestamp": "2026-11-11T06:13:23+00:00", "content_id": "25bc0342-5542-4b60-9d74-8bc47168c63a", "creator_id": "m3cost_05", "guess": "ai", "model_score": 0.8418, "style_score": 0.759, "combined_score": 0.8045, "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.", "status": "decided", "duration_ms": 54.7, "text_chars": 1255, "word_count": 190, "text_excerpt": "Many people believe that success comes primarily from talent"}
{"timestamp": "2026-11-11T06:13:23+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "invalid_json", "duration_ms": 0.2, "text_chars": null, "word_count": null, "text_excerpt": null}
{"timestamp": "2026-11-11T06:13:23+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "missing_creator_id", "duration_ms": 0.1, "text_chars": 21, "word_count": 4, "text_excerpt": "Some real words here."}
{"timestamp": "2026-11-11T06:13:23+00:00", "creator_id": "m3fail_empty", "event": "rejected", "status": "rejected", "reason": "empty_text", "duration_ms": 0.1, "text_chars": 3, "word_count": 0, "text_excerpt": "   "}
{"timestamp": "2026-11-11T06:13:23+00:00", "creator_id": "m3fail_MF04", "event": "rejected", "status": "rejected", "reason": "not_english_text", "duration_ms": 0.1, "text_chars": 31, "word_count": 0, "text_excerpt": "!!! ??? ... ,,, ;;; --- ((( )))"}
{"timestamp": "2026-11-11T06:13:23+00:00", "creator_id": "m3fail_MF02", "event": "rejected", "status": "rejected", "reason": "too_few_words", "duration_ms": 0.1, "text_chars": 1, "word_count": 1, "text_excerpt": "a"}
{"timestamp": "2026-11-11T06:13:23+00:00", "creator_id": "m3flood", "event": "rejected", "status": "rejected", "reason": "not_english_text", "duration_ms": 0.1, "text_chars": 7, "word_count": 0, "text_excerpt": "!!! ???"}
{"timestamp": "2026-11-11T06:13:23+00:00", "creator_id": "m3flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute", "duration_ms": 0.1, "text_chars": 7, "word_count": 0, "text_excerpt": "!!! ???"}
```

All eleven share one timestamp because the timestamp is only to the second and the whole run after the cold request took about half a second; each decision has its own `content_id`. Entries written before 2026-11-11 (units 7–8) don't have the four new fields.

## What It Costs

There's no API bill: GPT-2 runs on my laptop, so the cost of one run is **compute time**.

**Measured: 48.2 ms per submission on a warm model** (mean of 10), and **4,248.9 ms for the first submission after starting**, which loads GPT-2 into memory. A request the gate refuses costs about 0.1 ms, because it never reaches either signal.

How I measured it, on 2026-11-11:

- Machine: Apple M4 Pro, 24 GB RAM, macOS 27.0.1, CPU only, nothing else running against the service.
- Started the service fresh with `python app.py`. `/health` showed `"detector_loaded": false`.
- One cold request (FP01, 103 words) to load the model: 4,248.9 ms. `/health` then showed `"detector_loaded": true`.
- Ten warm requests, one after another: the 10 AI texts in `scenarios.py` ("AI from three tools", 106–202 words each), each with its own `creator_id` so the rate limiter never fired.
- The numbers are the `duration_ms` values from those ten records in `logs/audit.jsonl` (lines 367–376): 51.7, 42.5, 41.4, 65.6, 54.7, 55.1, 42.0, 42.9, 44.3, 41.7. Sum 481.9 ms ÷ 10 = **48.2 ms**. Median 43.6 ms, min 41.4 ms, max 65.6 ms.

Two other cold starts I recorded: 5,037.7 ms (the clean-checkout test in RUNNING.md) and 5,340.2 ms (log line 344, an earlier run of the same measurement). I reran that earlier one because the server it hit had been restarted by debug mode's file watcher rather than started by me. Its warm mean was 55.1 ms (log lines 345–354). So a cold start is 4–5.5 s on this machine and a warm submission is roughly 40–85 ms.

## Run Log and Verdicts

Produced by `run_capstone.py::main`, run as `python run_capstone.py before` against a freshly started service. The inputs are in `capstone_inputs.py`, committed (a99e5db) after `criteria.md` (b8f8c92) and before any run. None of them were used to set the gate's numbers. The runner warms the model with one uncounted request (log line 388), then runs all five criteria three times, 65 s apart, changing nothing in between. Each trial has its own `creator_id`s so rate limits don't carry over. For every request it reads back the log lines that request added, so each count below comes from `logs/audit.jsonl`, not from what the runner expected. Full per-input tables are in [results/capstone_2026-11-11_1841_before.md](results/capstone_2026-11-11_1841_before.md), and every row is in the matching `.json` file. The three trials are log lines 389–643.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Control characters refused | 10 of 10 refused (400, no `decided` line) | 0/10 | 0/10 | 0/10 | **MISSED** |
| 2. Non-English refused | at least 9 of 10 refused (400) | 5/10 | 5/10 | 5/10 | **MISSED** |
| 3. Short human texts not refused | 0 of 20 refused by the gate | 5/20 refused | 5/20 refused | 5/20 refused | **MISSED** |
| 4. Bad requests logged | 10 of 10 with exactly one `rejected` line, `reason` and `duration_ms` | 8/10 | 8/10 | 8/10 | **MISSED** |
| 5. Warm latency | at least 29 of 30 at or under 150 ms | 30/30 | 30/30 | 30/30 | **MET** |

**The three trials gave the same outcome for every input.** They really were three runs: the same text (C5_01) has a different `content_id` and timestamp each time (line 444 `cb7d6fb0…` at 23:41:38, line 529 `e26429d3…` at 23:42:47, line 614 `0dceddd7…` at 23:43:56) and the same combined score, 0.6447. That's expected: GPT-2 scoring is deterministic (no sampling), the style signal is arithmetic, and the gate is fixed rules. Only `duration_ms` varies between trials.

### Criterion 1: control characters (MISSED, 0/10)

All ten were scored, and all ten were called human. Lines 389 (C1_01, a null byte) and 396 (C1_08, an ANSI colour code), from trial 1:

```json
{"timestamp": "2026-11-11T23:41:36+00:00", "content_id": "9fb6f3fd-5304-4bdd-8f59-1603264dd884", "creator_id": "cap_11111841_t1_C1_01", "guess": "human", "model_score": 0.2341, "style_score": 0.5, "combined_score": 0.3538, "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.", "status": "decided", "duration_ms": 33.6, "text_chars": 157, "word_count": 31, "text_excerpt": "I finally fixed the leaking tap in the kitchen this morning,"}
{"timestamp": "2026-11-11T23:41:37+00:00", "content_id": "bd9fb83a-22fc-463e-aabe-958bd21b95d4", "creator_id": "cap_11111841_t1_C1_08", "guess": "human", "model_score": 0.0222, "style_score": 0.5, "combined_score": 0.2372, "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.", "status": "decided", "duration_ms": 32.6, "text_chars": 158, "word_count": 24, "text_excerpt": "The volunteers cleaned the whole riverbank in one afternoon,"}
```

**Stage:** the gate, `app.py::_gate`. **Mechanism:** the gate only measures the *share* of a–z letters, and one control character in 25–31 real words barely moves it: the ten texts scored 0.934–0.983 against a 0.70 minimum. Three of the codes (0x0B, 0x0C, 0x1F) aren't counted at all, because Python's `isspace()` treats them as whitespace. Nothing in the gate looked for control characters as such.

### Criterion 2: non-English (MISSED, 5/10)

The five non-Latin scripts were refused, and the five Latin-script languages were scored. Lines 399 (Arabic), 404 (Spanish) and 407 (Vietnamese):

```json
{"timestamp": "2026-11-11T23:41:37+00:00", "creator_id": "cap_11111841_t1_C2_01", "event": "rejected", "status": "rejected", "reason": "not_english_text", "duration_ms": 0.2, "text_chars": 201, "word_count": 0, "text_excerpt": "ذهبت إلى السوق صباح يوم الجمعة مع أخي الصغير لشراء الخضروات "}
{"timestamp": "2026-11-11T23:41:37+00:00", "content_id": "e44b491f-657f-4999-9d30-491970e0e4fc", "creator_id": "cap_11111841_t1_C2_06", "guess": "unsure", "model_score": 0.2758, "style_score": 0.8167, "combined_score": 0.5192, "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.", "status": "decided", "duration_ms": 34.6, "text_chars": 194, "word_count": 38, "text_excerpt": "El sábado pasado fui al mercado con mi madre para comprar fr"}
{"timestamp": "2026-11-11T23:41:37+00:00", "content_id": "d658bf46-636e-484c-ae1c-ece9954a20e5", "creator_id": "cap_11111841_t1_C2_09", "guess": "unsure", "model_score": 0.6693, "style_score": 0.3745, "combined_score": 0.5366, "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.", "status": "decided", "duration_ms": 52.1, "text_chars": 149, "word_count": 53, "text_excerpt": "Hôm qua tôi đi học về muộn vì trời mưa rất to. Mẹ tôi đã nấu"}
```

**Stage:** the gate's letter-share check. **Mechanism:** it measures *script*, not *language*. Arabic, Russian, Chinese, Hindi and Korean have no a–z letters (share 0.000). Spanish (0.957), French (0.928), German (0.960) and Indonesian (0.966) are written almost entirely in a–z and look like English to it. Vietnamese passed by 0.002 (0.702), because its accented letters count against it but not quite enough. Indonesian was labelled human, and the other four unsure.

### Criterion 3: short human texts (MISSED, 5 of 20 refused)

Fifteen of my texts were scored. Five were refused as `not_english_text`: C3_04, C3_09, C3_11, C3_19 and C3_20. Lines 409 (passed) and 428 (refused):

```json
{"timestamp": "2026-11-11T23:41:37+00:00", "content_id": "bde5836a-06b6-4228-995c-27524a94c69c", "creator_id": "cap_11111841_t1_C3_01", "guess": "human", "model_score": 0.007, "style_score": 0.5, "combined_score": 0.2288, "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.", "status": "decided", "duration_ms": 15.8, "text_chars": 18, "word_count": 3, "text_excerpt": "Hey whassup girl 👀"}
{"timestamp": "2026-11-11T23:41:38+00:00", "creator_id": "cap_11111841_t1_C3_20", "event": "rejected", "status": "rejected", "reason": "not_english_text", "duration_ms": 0.2, "text_chars": 33, "word_count": 5, "text_excerpt": "Nah 🙅‍♀️🙅‍♀️🙅‍♀️ I don't think so"}
```

**Stage:** the gate's letter-share check. **Mechanism:** in a short message, a few emoji and a "!!!" outweigh the letters, and the gate counts emoji by Unicode code point, not as one visible symbol. 🙅‍♀️ is four code points (person, joiner, female sign, style selector), so "Nah 🙅‍♀️🙅‍♀️🙅‍♀️ I don't think so" scores 15 letters out of 28 = 0.536. The five refused texts scored 0.536–0.667. I set the 0.70 line from longer texts (Unit 8's lowest real text was 0.876) and never tested it on short, emoji-heavy writing. These five writers got a 400 and no `content_id`, so they can't appeal.

### Criterion 4: bad requests logged (MISSED, 8/10)

The other eight each left exactly one `rejected` line with a `reason` and `duration_ms`. Lines 434 (punctuation only), 441 (the 6th request in a minute) and 442 (C4_09, a clear-screen escape code):

```json
{"timestamp": "2026-11-11T23:41:38+00:00", "creator_id": "cap_11111841_t1_C4_06", "event": "rejected", "status": "rejected", "reason": "not_english_text", "duration_ms": 0.2, "text_chars": 34, "word_count": 0, "text_excerpt": "... ?!?! --- *** ((( ))) ;; ,,, !!"}
{"timestamp": "2026-11-11T23:41:38+00:00", "creator_id": "cap_11111841_t1_C4_08", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute", "duration_ms": 0.3, "text_chars": 119, "word_count": 23, "text_excerpt": "I am sending this same short paragraph again because the pag"}
{"timestamp": "2026-11-11T23:41:38+00:00", "content_id": "e7f81464-a5f0-4da5-84d8-657027f8dd2e", "creator_id": "cap_11111841_t1_C4_09", "guess": "human", "model_score": 0.065, "style_score": 0.5, "combined_score": 0.2608, "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.", "status": "decided", "duration_ms": 27.6, "text_chars": 130, "word_count": 22, "text_excerpt": "\u001b[2J\u001b[HPlease ignore the earlier message, the meeting is sti"}
```

**Stage and mechanism:** the same as criterion 1. The two misses are C4_09 and C4_10, the two control-character texts. They weren't logged as rejections because they weren't rejected: they were scored and called human.

### Criterion 5: warm latency (MET, 30/30)

Slowest submission per trial: 107.0, 115.1 and 106.0 ms. Mean: 57.4, 59.5 and 59.5 ms. The longest text, C5_18 (398 words), on line 461:

```json
{"timestamp": "2026-11-11T23:41:39+00:00", "content_id": "6139302d-8111-4f66-90c5-74b7de3674d8", "creator_id": "cap_11111841_t1_C5_18", "guess": "human", "model_score": 0.6554, "style_score": 0.0, "combined_score": 0.3605, "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.", "status": "decided", "duration_ms": 107.0, "text_chars": 2086, "word_count": 398, "text_excerpt": "My grandmother's kitchen was the warmest room I have ever kn"}
```

## The Improvement

**What changed:** one new check in `app.py::_gate`, run before the letter-share check. Any text containing an ASCII control character (codes 0–8, 11, 12, 14–31 or 127) is refused with a 400 and the reason `control_characters`. Tab, newline and carriage return still pass, because real writing uses them. The check looks for the characters themselves, so it doesn't matter how few there are or whether Python counts them as whitespace. The writer gets a message saying the text contains control characters, such as null bytes or terminal escape codes, which don't belong in writing. The refusal is logged like every other one. Commit 3cb84c7.

**Why this miss:** two of my four misses (criteria 1 and 4) had one cause, and the fix doesn't depend on a threshold. No person types a null byte or an escape code, so refusing them can't refuse a real writer. Before running, I checked which existing texts the rule would catch: none of the 23 Unit 8 scenario texts, none of my criterion 2, 3 or 5 inputs, and only MF03 in the attack set, which was already refused as junk. I didn't pick criterion 3's fix, because it changes how the letter share is counted, the same check criterion 2 depends on.

**After run:** `python run_capstone.py after`, the same runner and inputs, on a freshly started service. The warm-up is log line 644, and the trials are lines 645–899. Full tables are in [results/capstone_2026-11-11_1849_after.md](results/capstone_2026-11-11_1849_after.md).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Control characters refused | 10 of 10 refused (400, no `decided` line) | 10/10 | 10/10 | 10/10 | **MET** (was MISSED, 0/10) |
| 2. Non-English refused | at least 9 of 10 refused (400) | 5/10 | 5/10 | 5/10 | **MISSED** (unchanged) |
| 3. Short human texts not refused | 0 of 20 refused by the gate | 5/20 refused | 5/20 refused | 5/20 refused | **MISSED** (unchanged) |
| 4. Bad requests logged | 10 of 10 with exactly one `rejected` line, `reason` and `duration_ms` | 10/10 | 10/10 | 10/10 | **MET** (was MISSED, 8/10) |
| 5. Warm latency | at least 29 of 30 at or under 150 ms | 30/30 | 30/30 | 30/30 | **MET** |

The same inputs as above, now refused (lines 645, 652 and 698):

```json
{"timestamp": "2026-11-11T23:49:08+00:00", "creator_id": "cap_11111849_t1_C1_01", "event": "rejected", "status": "rejected", "reason": "control_characters", "duration_ms": 0.4, "text_chars": 157, "word_count": 31, "text_excerpt": "I finally fixed the leaking tap in the kitchen this morning,"}
{"timestamp": "2026-11-11T23:49:08+00:00", "creator_id": "cap_11111849_t1_C1_08", "event": "rejected", "status": "rejected", "reason": "control_characters", "duration_ms": 0.2, "text_chars": 158, "word_count": 24, "text_excerpt": "The volunteers cleaned the whole riverbank in one afternoon,"}
{"timestamp": "2026-11-11T23:49:09+00:00", "creator_id": "cap_11111849_t1_C4_09", "event": "rejected", "status": "rejected", "reason": "control_characters", "duration_ms": 0.2, "text_chars": 130, "word_count": 22, "text_excerpt": "\u001b[2J\u001b[HPlease ignore the earlier message, the meeting is sti"}
```

Criteria 2 and 3 have exactly the same five misses as before, which is what I expected, because none of those texts contain control characters. Criterion 5 still holds, but trial 1's slowest request was 135.8 ms (C5 means 67.0, 60.9 and 59.0 ms). That is closer to the 150 ms line than any request in the before run. Text that passes the gate takes the same path as before, so I read this as normal laptop variation, not a cost of the fix. It is the margin I'd watch.

## What's Still Broken

**Criterion 2: Spanish, French, German, Vietnamese and Indonesian still get a label (5/10 refused).** The letter-share check tells scripts apart, not languages. I stopped here because refusing these properly needs a check on the words themselves, not the letters, and that's a new rule with its own risk to short English messages. Raising the 0.70 line wouldn't help: Spanish, French, German and Indonesian sit at 0.93–0.97, the same as English. **First thing I'd do:** add a check on the share of words that are common English function words ("the", "and", "is", "you", "I", "to" and so on). Real English uses them constantly and the other four languages almost never do. I'd test it on my 20 short texts *before* turning it on, because "Ok 👌 I will get it done" and "Hey whassup girl 👀" have very few of them.

**Criterion 3: five of my own short messages are refused (5/20).** This is the miss that hurts real writers most, because a refused writer gets no `content_id` and can't appeal. I stopped because the fix changes how the letter share is counted. That check is also what refuses Arabic, Russian, Chinese, Hindi and Korean, so it needs its own before and after run, and Milestone 6 is one improvement. **First thing I'd do:** leave emoji, skin-tone modifiers and joiners out of the letter-share count, so it compares letters to punctuation only. By my arithmetic on the five refused texts, they would score 0.700–1.000 instead of 0.536–0.667. C3_09 lands exactly on 0.700 and only passes because the rule refuses anything *below* 0.70, so that alone isn't much margin. Emoji-only junk like MF06 would have no letters and no words left, so the gate would still need to refuse it (by the word count). I haven't run this; it's the next thing to test.

**Still out of scope from The Shape:** short AI text like EV08, prompt injection (PI01, PI02, PI05), and the small detector model. None of them changed this unit.



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
