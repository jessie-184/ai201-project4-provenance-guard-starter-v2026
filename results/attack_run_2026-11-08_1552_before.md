# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 15:52
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `b84c03e3-9818-4672-aa19-ff821c0afc9c` | unsure | 0.453 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c2880c7a-06f7-4606-b887-73002cd6f0b1` | unsure | 0.490 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `f16dbccf-d20f-49bb-9233-3236a1fe966e` | unsure | 0.531 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `4f924194-cda6-4c2d-9abf-0fe6b473e806` | unsure | 0.692 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `db732142-1175-4e8e-9693-a5f218757b42` | human | 0.261 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `8ec7c555-5b5a-4990-b393-98f21c4eb2e9` | unsure | 0.492 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `be872180-e413-41f2-ae03-4b783f5b5c3e` | unsure | 0.463 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `e0045851-5d45-4052-88e7-7b953cdc4fd2` | human | 0.443 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `67d736de-4d95-4193-be20-a2de6e9b6629` | unsure | 0.548 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `a87c0ef5-d60d-449d-9e43-bbad07780b62` | ai | 0.851 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `30bdd930-7cde-4017-abdf-a1dd4560d427` | unsure | 0.588 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `21ea786d-0a44-441c-98ac-c608b24b0a99` | ai | 0.787 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `896d0eb6-5562-44dc-a657-67386f50c5bf` | ai | 0.760 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `011ab706-1dec-45bd-a794-3b30e118075f` | ai | 0.753 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `87507dc6-3892-4d12-97f5-277fdd8f2764` | ai | 0.819 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `58949d3b-2909-49d3-9dec-04c014d6ff2d` | unsure | 0.712 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `fc241baa-f16e-4cc4-9ef8-5e4515921d7e` | unsure | 0.698 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `2dab01bc-ba85-480a-a40b-75d018172ace` | human | 0.401 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `100a4403-e228-43ce-9569-bb0e3b7b9e55` | human | 0.416 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `3bfc565a-39ac-4860-9070-7ba3e30c8ad9` | human | 0.224 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `dedd81b7-4620-4207-9e9f-488ac85e4498` | unsure | 0.531 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `0313b152-6796-418a-acac-bdcffdbbe347` | human | 0.390 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `036b5786-d808-4013-8e2c-035674247273` | human | 0.396 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `7ec1a3dc-2b86-4f67-b7fe-9d64ed9ebdd7` | unsure | 0.561 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `f3d29aa3-86ea-4591-b57d-192b7be260b5` | human | 0.270 |  |
| MF04 | malformed | text is only punctuation | 200 | `fa922047-ca92-417f-8414-bc1fba5d886a` | human | 0.344 |  |
| MF05 | malformed | text is a very long single word | 200 | `7ff84b5f-e1e8-4e5c-91a1-b346f0bdd58e` | ai | 0.819 |  |
| MF06 | malformed | text is emoji only | 200 | `e20d1e4c-790b-4d52-b870-540b78f675c7` | ai | 0.886 |  |
| MF07 | malformed | text is right-to-left script | 200 | `867008aa-6a71-43e1-b447-5e5ab449f75d` | ai | 0.836 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `979ec2ec-3710-4a8a-ab49-699a78172484` | human | 0.286 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `14414432-c158-4820-9c30-7af938b9e743` | human | 0.286 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `253f5ff7-3f09-4eb2-99f4-e322eebb9974` | human | 0.286 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `64e91821-dfc9-44a6-9308-bcdc2cd1ff31` | human | 0.286 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `99d09646-ef3c-4c0f-9441-d33fc6b47678` | human | 0.286 |  |
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
  "content_id": "b84c03e3-9818-4672-aa19-ff821c0afc9c",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4526,
  "model_score": 0.1635,
  "style_score": 0.8059,
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
  "content_id": "c2880c7a-06f7-4606-b887-73002cd6f0b1",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4901,
  "model_score": 0.5943,
  "style_score": 0.3627,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
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
  "content_id": "f16dbccf-d20f-49bb-9233-3236a1fe966e",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5312,
  "model_score": 0.6662,
  "style_score": 0.3661,
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
  "content_id": "4f924194-cda6-4c2d-9abf-0fe6b473e806",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6924,
  "model_score": 0.6114,
  "style_score": 0.7915,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
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
  "content_id": "db732142-1175-4e8e-9693-a5f218757b42",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.261,
  "model_score": 0.3212,
  "style_score": 0.1875,
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
  "content_id": "8ec7c555-5b5a-4990-b393-98f21c4eb2e9",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4916,
  "model_score": 0.5727,
  "style_score": 0.3925,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
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
  "content_id": "be872180-e413-41f2-ae03-4b783f5b5c3e",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.4632,
  "model_score": 0.5862,
  "style_score": 0.3128,
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
  "content_id": "e0045851-5d45-4052-88e7-7b953cdc4fd2",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.4427,
  "model_score": 0.2452,
  "style_score": 0.684,
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
  "content_id": "67d736de-4d95-4193-be20-a2de6e9b6629",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5482,
  "model_score": 0.7042,
  "style_score": 0.3575,
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
  "content_id": "a87c0ef5-d60d-449d-9e43-bbad07780b62",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8514,
  "model_score": 0.9792,
  "style_score": 0.6951,
  "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
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
  "content_id": "30bdd930-7cde-4017-abdf-a1dd4560d427",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5879,
  "model_score": 0.6175,
  "style_score": 0.5518,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
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
  "content_id": "21ea786d-0a44-441c-98ac-c608b24b0a99",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7867,
  "model_score": 0.7387,
  "style_score": 0.8454,
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
  "content_id": "896d0eb6-5562-44dc-a657-67386f50c5bf",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7603,
  "model_score": 0.8051,
  "style_score": 0.7056,
  "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
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
  "content_id": "011ab706-1dec-45bd-a794-3b30e118075f",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7535,
  "model_score": 0.8329,
  "style_score": 0.6565,
  "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
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
  "content_id": "87507dc6-3892-4d12-97f5-277fdd8f2764",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8189,
  "model_score": 0.8005,
  "style_score": 0.8414,
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
  "content_id": "58949d3b-2909-49d3-9dec-04c014d6ff2d",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.712,
  "model_score": 0.8814,
  "style_score": 0.5049,
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
  "content_id": "fc241baa-f16e-4cc4-9ef8-5e4515921d7e",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6976,
  "model_score": 0.8816,
  "style_score": 0.4727,
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
  "content_id": "2dab01bc-ba85-480a-a40b-75d018172ace",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.4006,
  "model_score": 0.3223,
  "style_score": 0.4962,
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
  "content_id": "100a4403-e228-43ce-9569-bb0e3b7b9e55",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.4164,
  "model_score": 0.4625,
  "style_score": 0.36,
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
  "content_id": "3bfc565a-39ac-4860-9070-7ba3e30c8ad9",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2244,
  "model_score": 0.2044,
  "style_score": 0.2489,
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
  "content_id": "dedd81b7-4620-4207-9e9f-488ac85e4498",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5306,
  "model_score": 0.5943,
  "style_score": 0.4528,
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
  "content_id": "0313b152-6796-418a-acac-bdcffdbbe347",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.3904,
  "model_score": 0.4998,
  "style_score": 0.2566,
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
  "content_id": "036b5786-d808-4013-8e2c-035674247273",
  "creator_id": "attacker_PI05",
  "guess": "human",
  "confidence": 0.3963,
  "model_score": 0.6401,
  "style_score": 0.0983,
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
  "content_id": "7ec1a3dc-2b86-4f67-b7fe-9d64ed9ebdd7",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5606,
  "model_score": 0.5583,
  "style_score": 0.5633,
  "label": "We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review.",
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
  "content_id": "f3d29aa3-86ea-4591-b57d-192b7be260b5",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.27,
  "model_score": 0.0,
  "style_score": 0.6,
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
  "content_id": "fa922047-ca92-417f-8414-bc1fba5d886a",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.3437,
  "model_score": 0.0112,
  "style_score": 0.75,
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
  "content_id": "7ff84b5f-e1e8-4e5c-91a1-b346f0bdd58e",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8187,
  "model_score": 0.9976,
  "style_score": 0.6,
  "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
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
  "content_id": "e20d1e4c-790b-4d52-b870-540b78f675c7",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.8858,
  "model_score": 0.9969,
  "style_score": 0.75,
  "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
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
  "content_id": "867008aa-6a71-43e1-b447-5e5ab449f75d",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.836,
  "model_score": 0.9064,
  "style_score": 0.75,
  "label": "This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this.",
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
  "content_id": "979ec2ec-3710-4a8a-ab49-699a78172484",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2858,
  "model_score": 0.0287,
  "style_score": 0.6,
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
  "content_id": "14414432-c158-4820-9c30-7af938b9e743",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2858,
  "model_score": 0.0287,
  "style_score": 0.6,
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
  "content_id": "253f5ff7-3f09-4eb2-99f4-e322eebb9974",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2858,
  "model_score": 0.0287,
  "style_score": 0.6,
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
  "content_id": "64e91821-dfc9-44a6-9308-bcdc2cd1ff31",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2858,
  "model_score": 0.0287,
  "style_score": 0.6,
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
  "content_id": "99d09646-ef3c-4c0f-9441-d33fc6b47678",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2858,
  "model_score": 0.0287,
  "style_score": 0.6,
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
