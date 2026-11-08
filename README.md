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
    "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to reviewthis.",
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
    "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to reviewthis.",
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
    "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to reviewthis.",
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
    "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to reviewthis.",
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
    "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to reviewthis.",
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
