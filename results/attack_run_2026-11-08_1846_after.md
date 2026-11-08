# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 18:46
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c9790cea-971d-4db6-ab62-67bf11f1de13` | unsure | 0.528 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `d82c7d0a-d0e5-4efa-bfd6-426384a204f3` | human | 0.327 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `140bea8c-e533-43ac-aed3-86b41974ba65` | unsure | 0.486 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `4efca18a-3099-4c92-ae2f-06747aeb7e76` | ai | 0.759 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `6274b680-7267-403b-836e-dfc72376bd17` | human | 0.177 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `a3d6b5b5-5f7f-4aca-a55c-ce3f468ae37c` | human | 0.315 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `f6ecb1d9-4a5a-47b4-9ed6-0757125b27db` | unsure | 0.547 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `5afaedce-59af-4ef0-b031-bddc31322245` | human | 0.435 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `f3284c2a-6633-4859-bbcb-c218e5178051` | unsure | 0.480 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `275358be-1d4b-4d58-8121-11b349917243` | unsure | 0.710 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `5394cbb9-b223-4a71-8690-ff64d13b5ad0` | human | 0.444 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `5b292281-60d4-4207-8057-a107f5221c7b` | ai | 0.755 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `cd4046f5-681c-42d5-8561-a480b8518fbd` | unsure | 0.692 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `3507dd67-b1a6-419e-a5ef-f40cbee54a6c` | unsure | 0.664 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `d17d5826-4444-4e81-8c96-eb3d60d45ff4` | ai | 0.748 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `d3b8f41f-e9e7-4c8a-b2d0-501e47e20304` | unsure | 0.519 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `3e935c1e-69c8-421e-b606-f83af97485ba` | unsure | 0.485 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `fd3e03b8-d5e8-4d73-bf4e-9101577b6e29` | human | 0.309 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `83ba4776-92ca-4053-a3df-e12c11fe3627` | human | 0.254 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `b3bf1b71-806e-4116-8838-b8614f8af1b8` | human | 0.112 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `5574b016-dd08-4aec-a34f-b85a8b7608d2` | unsure | 0.560 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `5e5db47e-71b4-49bd-b098-3ac4100517c2` | human | 0.447 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `f5e81dd1-7821-4e94-8c38-5457e61e3227` | human | 0.441 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `3a0fdcff-59c9-4424-9d2a-717617f75d25` | human | 0.425 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `60e9ed8d-180f-4423-b3ec-c97baed1c2f8` | human | 0.225 |  |
| MF04 | malformed | text is only punctuation | 200 | `83cafa47-3ce1-4de4-b757-f68ee4d34658` | human | 0.231 |  |
| MF05 | malformed | text is a very long single word | 200 | `2bf4157d-8510-4c43-853f-db2d0c4e9b98` | unsure | 0.710 |  |
| MF06 | malformed | text is emoji only | 200 | `fe1db84e-6f6b-4a73-b6c3-7c372140dd7d` | unsure | 0.710 |  |
| MF07 | malformed | text is right-to-left script | 200 | `313f0e11-a1a5-44c5-b022-556676f29450` | unsure | 0.710 |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `57f711dd-fdbb-4683-bd77-437f866a922e` | human | 0.241 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bda73cbe-d4b2-44b8-a605-1e237ce43313` | human | 0.241 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fa23e525-6908-4a02-b1d7-863f690d2a14` | human | 0.241 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `465fd466-e8c0-4339-92cd-b5854b029d04` | human | 0.241 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `41a8affc-88c7-4002-99b0-282e0dfa83a8` | human | 0.241 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c9790cea-971d-4db6-ab62-67bf11f1de13",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5279,
  "model_score": 0.1635,
  "style_score": 0.9732,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "d82c7d0a-d0e5-4efa-bfd6-426384a204f3",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.3269,
  "model_score": 0.5943,
  "style_score": 0.0,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "140bea8c-e533-43ac-aed3-86b41974ba65",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4863,
  "model_score": 0.6662,
  "style_score": 0.2665,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "4efca18a-3099-4c92-ae2f-06747aeb7e76",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.7593,
  "model_score": 0.6114,
  "style_score": 0.94,
  "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "6274b680-7267-403b-836e-dfc72376bd17",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.1767,
  "model_score": 0.3212,
  "style_score": 0.0,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "a3d6b5b5-5f7f-4aca-a55c-ce3f468ae37c",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.315,
  "model_score": 0.5727,
  "style_score": 0.0,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "f6ecb1d9-4a5a-47b4-9ed6-0757125b27db",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5474,
  "model_score": 0.5862,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "5afaedce-59af-4ef0-b031-bddc31322245",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.4355,
  "model_score": 0.2452,
  "style_score": 0.668,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "f3284c2a-6633-4859-bbcb-c218e5178051",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.4801,
  "model_score": 0.7042,
  "style_score": 0.2063,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "275358be-1d4b-4d58-8121-11b349917243",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.71,
  "model_score": 0.9792,
  "style_score": 0.3903,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "5394cbb9-b223-4a71-8690-ff64d13b5ad0",
  "creator_id": "attacker_FP01",
  "guess": "human",
  "confidence": 0.4437,
  "model_score": 0.6175,
  "style_score": 0.2313,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "5b292281-60d4-4207-8057-a107f5221c7b",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7547,
  "model_score": 0.7387,
  "style_score": 0.7742,
  "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "cd4046f5-681c-42d5-8561-a480b8518fbd",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6923,
  "model_score": 0.8051,
  "style_score": 0.5545,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "3507dd67-b1a6-419e-a5ef-f40cbee54a6c",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6643,
  "model_score": 0.8329,
  "style_score": 0.4582,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "d17d5826-4444-4e81-8c96-eb3d60d45ff4",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7475,
  "model_score": 0.8005,
  "style_score": 0.6828,
  "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "d3b8f41f-e9e7-4c8a-b2d0-501e47e20304",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5194,
  "model_score": 0.8814,
  "style_score": 0.077,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "3e935c1e-69c8-421e-b606-f83af97485ba",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.4849,
  "model_score": 0.8816,
  "style_score": 0.0,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "fd3e03b8-d5e8-4d73-bf4e-9101577b6e29",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3089,
  "model_score": 0.3223,
  "style_score": 0.2925,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "83ba4776-92ca-4053-a3df-e12c11fe3627",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.2544,
  "model_score": 0.4625,
  "style_score": 0.0,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "b3bf1b71-806e-4116-8838-b8614f8af1b8",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1124,
  "model_score": 0.2044,
  "style_score": 0.0,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "5574b016-dd08-4aec-a34f-b85a8b7608d2",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5596,
  "model_score": 0.5943,
  "style_score": 0.5172,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "5e5db47e-71b4-49bd-b098-3ac4100517c2",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.4473,
  "model_score": 0.4998,
  "style_score": 0.3832,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "f5e81dd1-7821-4e94-8c38-5457e61e3227",
  "creator_id": "attacker_PI05",
  "guess": "human",
  "confidence": 0.4405,
  "model_score": 0.6401,
  "style_score": 0.1965,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "3a0fdcff-59c9-4424-9d2a-717617f75d25",
  "creator_id": "attacker_PI06",
  "guess": "human",
  "confidence": 0.4247,
  "model_score": 0.5583,
  "style_score": 0.2615,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "60e9ed8d-180f-4423-b3ec-c97baed1c2f8",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.225,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "83cafa47-3ce1-4de4-b757-f68ee4d34658",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.2312,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "2bf4157d-8510-4c43-853f-db2d0c4e9b98",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.71,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "fe1db84e-6f6b-4a73-b6c3-7c372140dd7d",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.71,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "313f0e11-a1a5-44c5-b022-556676f29450",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.71,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "57f711dd-fdbb-4683-bd77-437f866a922e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2408,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "bda73cbe-d4b2-44b8-a605-1e237ce43313",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2408,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "fa23e525-6908-4a02-b1d7-863f690d2a14",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2408,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "465fd466-e8c0-4339-92cd-b5854b029d04",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2408,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "41a8affc-88c7-4002-99b0-282e0dfa83a8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2408,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This looks like it was written by a person. Our check found the patterns we usually see in human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
