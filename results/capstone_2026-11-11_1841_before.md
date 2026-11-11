# Capstone run log — before

- Produced by: `run_capstone.py::main` · inputs: `capstone_inputs.py`
- Service: `app.py::submit` (gate: `app.py::_gate`) · commit `a99e5db`
- 3 trials, 65s apart, nothing changed in between · started 2026-11-11 18:41:19
- creator_id prefix: `cap_11111841_t<trial>_`

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Control characters refused | 10 of 10 refused (400, no decided line) | 0/10 refused | 0/10 refused | 0/10 refused | MISSED |
| 2. Non-English refused | at least 9 of 10 refused (400) | 5/10 refused | 5/10 refused | 5/10 refused | MISSED |
| 3. Short human texts not refused | 0 of 20 refused by the gate | 5/20 refused | 5/20 refused | 5/20 refused | MISSED |
| 4. Bad requests logged | 10 of 10 with exactly one rejected line, reason + duration_ms | 8/10 logged | 8/10 logged | 8/10 logged | MISSED |
| 5. Warm latency | at least 29 of 30 at or under 150 ms (warm model) | 30/30 ≤ 150 ms | 30/30 ≤ 150 ms | 30/30 ≤ 150 ms | MET |

## Criterion 1 — control characters

**Trial 1**

| id | code | http | error | decided_lines | duration_ms | pass |
|---|---|---|---|---|---|---|
| C1_01 | 0x00 null | 200 |  | 1 | 33.6 | False |
| C1_02 | 0x04 end of transmission | 200 |  | 1 | 28.1 | False |
| C1_03 | 0x07 bell | 200 |  | 1 | 27.9 | False |
| C1_04 | 0x08 backspace | 200 |  | 1 | 28.9 | False |
| C1_05 | 0x0B vertical tab | 200 |  | 1 | 31.8 | False |
| C1_06 | 0x0C form feed | 200 |  | 1 | 29.6 | False |
| C1_07 | 0x1A substitute | 200 |  | 1 | 28.8 | False |
| C1_08 | 0x1B escape (ANSI colour) | 200 |  | 1 | 32.6 | False |
| C1_09 | 0x1F unit separator | 200 |  | 1 | 30.9 | False |
| C1_10 | 0x7F delete | 200 |  | 1 | 32.4 | False |

**Trial 2**

| id | code | http | error | decided_lines | duration_ms | pass |
|---|---|---|---|---|---|---|
| C1_01 | 0x00 null | 200 |  | 1 | 75.7 | False |
| C1_02 | 0x04 end of transmission | 200 |  | 1 | 29.3 | False |
| C1_03 | 0x07 bell | 200 |  | 1 | 28.9 | False |
| C1_04 | 0x08 backspace | 200 |  | 1 | 28.9 | False |
| C1_05 | 0x0B vertical tab | 200 |  | 1 | 31.6 | False |
| C1_06 | 0x0C form feed | 200 |  | 1 | 27.6 | False |
| C1_07 | 0x1A substitute | 200 |  | 1 | 29.6 | False |
| C1_08 | 0x1B escape (ANSI colour) | 200 |  | 1 | 33.8 | False |
| C1_09 | 0x1F unit separator | 200 |  | 1 | 31.2 | False |
| C1_10 | 0x7F delete | 200 |  | 1 | 31.9 | False |

**Trial 3**

| id | code | http | error | decided_lines | duration_ms | pass |
|---|---|---|---|---|---|---|
| C1_01 | 0x00 null | 200 |  | 1 | 38.8 | False |
| C1_02 | 0x04 end of transmission | 200 |  | 1 | 29.5 | False |
| C1_03 | 0x07 bell | 200 |  | 1 | 28.2 | False |
| C1_04 | 0x08 backspace | 200 |  | 1 | 28.4 | False |
| C1_05 | 0x0B vertical tab | 200 |  | 1 | 33.3 | False |
| C1_06 | 0x0C form feed | 200 |  | 1 | 28.1 | False |
| C1_07 | 0x1A substitute | 200 |  | 1 | 28.1 | False |
| C1_08 | 0x1B escape (ANSI colour) | 200 |  | 1 | 34.6 | False |
| C1_09 | 0x1F unit separator | 200 |  | 1 | 33.1 | False |
| C1_10 | 0x7F delete | 200 |  | 1 | 35.1 | False |

## Criterion 2 — non-English

**Trial 1**

| id | language | http | error | label | duration_ms | pass |
|---|---|---|---|---|---|---|
| C2_01 | Arabic | 400 | not_english_text |  | 0.2 | True |
| C2_02 | Russian | 400 | not_english_text |  | 0.1 | True |
| C2_03 | Chinese | 400 | not_english_text |  | 0.3 | True |
| C2_04 | Hindi | 400 | not_english_text |  | 0.1 | True |
| C2_05 | Korean | 400 | not_english_text |  | 0.2 | True |
| C2_06 | Spanish | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 34.6 | False |
| C2_07 | French | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 33.7 | False |
| C2_08 | German | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 34.7 | False |
| C2_09 | Vietnamese | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 52.1 | False |
| C2_10 | Indonesian | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 35.7 | False |

**Trial 2**

| id | language | http | error | label | duration_ms | pass |
|---|---|---|---|---|---|---|
| C2_01 | Arabic | 400 | not_english_text |  | 0.3 | True |
| C2_02 | Russian | 400 | not_english_text |  | 0.2 | True |
| C2_03 | Chinese | 400 | not_english_text |  | 0.2 | True |
| C2_04 | Hindi | 400 | not_english_text |  | 0.2 | True |
| C2_05 | Korean | 400 | not_english_text |  | 0.2 | True |
| C2_06 | Spanish | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 35.7 | False |
| C2_07 | French | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 34.9 | False |
| C2_08 | German | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 40.3 | False |
| C2_09 | Vietnamese | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 51.2 | False |
| C2_10 | Indonesian | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 34.5 | False |

**Trial 3**

| id | language | http | error | label | duration_ms | pass |
|---|---|---|---|---|---|---|
| C2_01 | Arabic | 400 | not_english_text |  | 0.3 | True |
| C2_02 | Russian | 400 | not_english_text |  | 0.3 | True |
| C2_03 | Chinese | 400 | not_english_text |  | 0.3 | True |
| C2_04 | Hindi | 400 | not_english_text |  | 0.2 | True |
| C2_05 | Korean | 400 | not_english_text |  | 0.2 | True |
| C2_06 | Spanish | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 37.5 | False |
| C2_07 | French | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 37.6 | False |
| C2_08 | German | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 36.8 | False |
| C2_09 | Vietnamese | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 50.3 | False |
| C2_10 | Indonesian | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 37.3 | False |

## Criterion 3 — short human texts

**Trial 1**

| id | http | error | label | duration_ms | pass |
|---|---|---|---|---|---|
| C3_01 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 15.8 | True |
| C3_02 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 21.7 | True |
| C3_03 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.3 | True |
| C3_04 | 400 | not_english_text |  | 0.2 | False |
| C3_05 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 27.6 | True |
| C3_06 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 21.2 | True |
| C3_07 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 21.3 | True |
| C3_08 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.6 | True |
| C3_09 | 400 | not_english_text |  | 0.3 | False |
| C3_10 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.4 | True |
| C3_11 | 400 | not_english_text |  | 0.2 | False |
| C3_12 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.0 | True |
| C3_13 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 18.6 | True |
| C3_14 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 20.6 | True |
| C3_15 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.6 | True |
| C3_16 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 15.7 | True |
| C3_17 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 15.7 | True |
| C3_18 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 20.8 | True |
| C3_19 | 400 | not_english_text |  | 0.2 | False |
| C3_20 | 400 | not_english_text |  | 0.2 | False |

**Trial 2**

| id | http | error | label | duration_ms | pass |
|---|---|---|---|---|---|
| C3_01 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.2 | True |
| C3_02 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 21.4 | True |
| C3_03 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.1 | True |
| C3_04 | 400 | not_english_text |  | 0.3 | False |
| C3_05 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 27.3 | True |
| C3_06 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 21.1 | True |
| C3_07 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 21.4 | True |
| C3_08 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.4 | True |
| C3_09 | 400 | not_english_text |  | 0.2 | False |
| C3_10 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.6 | True |
| C3_11 | 400 | not_english_text |  | 0.3 | False |
| C3_12 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.4 | True |
| C3_13 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 18.0 | True |
| C3_14 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 21.2 | True |
| C3_15 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.5 | True |
| C3_16 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.3 | True |
| C3_17 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 15.5 | True |
| C3_18 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 20.2 | True |
| C3_19 | 400 | not_english_text |  | 0.2 | False |
| C3_20 | 400 | not_english_text |  | 0.2 | False |

**Trial 3**

| id | http | error | label | duration_ms | pass |
|---|---|---|---|---|---|
| C3_01 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.5 | True |
| C3_02 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 23.2 | True |
| C3_03 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.4 | True |
| C3_04 | 400 | not_english_text |  | 0.3 | False |
| C3_05 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 27.8 | True |
| C3_06 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 20.7 | True |
| C3_07 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 21.6 | True |
| C3_08 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.1 | True |
| C3_09 | 400 | not_english_text |  | 0.2 | False |
| C3_10 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.5 | True |
| C3_11 | 400 | not_english_text |  | 0.3 | False |
| C3_12 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.1 | True |
| C3_13 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.4 | True |
| C3_14 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 20.9 | True |
| C3_15 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.2 | True |
| C3_16 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.8 | True |
| C3_17 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.0 | True |
| C3_18 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 20.7 | True |
| C3_19 | 400 | not_english_text |  | 0.3 | False |
| C3_20 | 400 | not_english_text |  | 0.2 | False |

## Criterion 4 — bad requests

**Trial 1**

| id | what | http | log_lines | rejected_lines | reason | duration_ms | pass |
|---|---|---|---|---|---|---|---|
| C4_01 | invalid JSON | 400 | 1 | 1 | invalid_json | 1.1 | True |
| C4_02 | missing creator_id | 400 | 1 | 1 | missing_creator_id | 0.7 | True |
| C4_03 | missing text | 400 | 1 | 1 | missing_text | 0.2 | True |
| C4_04 | empty text | 400 | 1 | 1 | empty_text | 0.2 | True |
| C4_05 | text over 10,000 characters | 400 | 1 | 1 | text_too_long | 0.2 | True |
| C4_06 | punctuation-only text | 400 | 1 | 1 | not_english_text | 0.2 | True |
| C4_07 | one-word text | 400 | 1 | 1 | too_few_words | 0.1 | True |
| C4_08 | rate-limited (6th request in a minute) | 429 | 1 | 1 | rate_limited | 0.3 | True |
| C4_09 | control characters (clear screen) | 200 | 1 | 0 |  | 27.6 | False |
| C4_10 | control character (0x03, Ctrl+C) | 200 | 1 | 0 |  | 27.8 | False |

**Trial 2**

| id | what | http | log_lines | rejected_lines | reason | duration_ms | pass |
|---|---|---|---|---|---|---|---|
| C4_01 | invalid JSON | 400 | 1 | 1 | invalid_json | 0.2 | True |
| C4_02 | missing creator_id | 400 | 1 | 1 | missing_creator_id | 0.2 | True |
| C4_03 | missing text | 400 | 1 | 1 | missing_text | 0.2 | True |
| C4_04 | empty text | 400 | 1 | 1 | empty_text | 0.2 | True |
| C4_05 | text over 10,000 characters | 400 | 1 | 1 | text_too_long | 0.2 | True |
| C4_06 | punctuation-only text | 400 | 1 | 1 | not_english_text | 0.2 | True |
| C4_07 | one-word text | 400 | 1 | 1 | too_few_words | 0.2 | True |
| C4_08 | rate-limited (6th request in a minute) | 429 | 1 | 1 | rate_limited | 0.3 | True |
| C4_09 | control characters (clear screen) | 200 | 1 | 0 |  | 27.2 | False |
| C4_10 | control character (0x03, Ctrl+C) | 200 | 1 | 0 |  | 27.8 | False |

**Trial 3**

| id | what | http | log_lines | rejected_lines | reason | duration_ms | pass |
|---|---|---|---|---|---|---|---|
| C4_01 | invalid JSON | 400 | 1 | 1 | invalid_json | 0.3 | True |
| C4_02 | missing creator_id | 400 | 1 | 1 | missing_creator_id | 0.2 | True |
| C4_03 | missing text | 400 | 1 | 1 | missing_text | 0.2 | True |
| C4_04 | empty text | 400 | 1 | 1 | empty_text | 0.2 | True |
| C4_05 | text over 10,000 characters | 400 | 1 | 1 | text_too_long | 0.2 | True |
| C4_06 | punctuation-only text | 400 | 1 | 1 | not_english_text | 0.2 | True |
| C4_07 | one-word text | 400 | 1 | 1 | too_few_words | 0.1 | True |
| C4_08 | rate-limited (6th request in a minute) | 429 | 1 | 1 | rate_limited | 0.3 | True |
| C4_09 | control characters (clear screen) | 200 | 1 | 0 |  | 28.2 | False |
| C4_10 | control character (0x03, Ctrl+C) | 200 | 1 | 0 |  | 27.8 | False |

## Criterion 5 — warm latency

**Trial 1** · `/health` before: `{"detector_loaded": true, "detector_model": "gpt2", "log_entries": 443, "ok": true, "rate_limiting": true}`

| id | words | http | label | duration_ms | content_id | pass |
|---|---|---|---|---|---|---|
| C5_01 | 112 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 40.8 | cb7d6fb0-d0c2-4737-9c15-657712def95f | True |
| C5_02 | 159 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 58.7 | ed7a3dca-7653-4ffe-81ba-e22173a8aae2 | True |
| C5_03 | 191 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 66.1 | 8371f9af-a9f7-4b7c-b6c6-930fdbf0a5e1 | True |
| C5_04 | 100 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 40.9 | f607b3b6-772d-48f8-a7b1-35caee0fadc9 | True |
| C5_05 | 165 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 53.0 | d1178b81-7c1e-4e06-b66b-1c3ca2160f0c | True |
| C5_06 | 122 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 44.5 | 1e12deaf-7574-4749-84fd-2e2e03474c6c | True |
| C5_07 | 229 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 74.9 | de358279-6148-4bf9-ba1c-e67be5bc2696 | True |
| C5_08 | 273 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 85.0 | 386d5388-453c-4cda-ab8c-cd43d64afe86 | True |
| C5_09 | 113 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 45.4 | 620ea837-0625-4027-b625-f838433be9b4 | True |
| C5_10 | 117 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 44.2 | b4a6b56e-11f8-418b-8e03-b394fac4eb1c | True |
| C5_11 | 216 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 63.6 | 5e6d928a-2252-4fc4-937c-f20e9fdf1117 | True |
| C5_12 | 151 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 49.6 | a5e416e6-06b7-43c3-87cc-9d7fa7c0140b | True |
| C5_13 | 109 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 44.2 | b974b0a4-4918-4d42-ae87-2eb53cc08830 | True |
| C5_14 | 258 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 73.7 | 28cd78b9-f4b5-4e2f-8145-be2c51c0bf34 | True |
| C5_15 | 217 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 59.9 | afead56d-5a80-4bf8-9c9f-fdf384cd020b | True |
| C5_16 | 116 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 44.5 | f190738e-40fc-4ac1-8c36-e5ad44b42e68 | True |
| C5_17 | 104 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 40.7 | 6d2a19d3-3492-4a65-b7d3-926361bec44d | True |
| C5_18 | 397 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 107.0 | 6139302d-8111-4f66-90c5-74b7de3674d8 | True |
| C5_19 | 190 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 59.2 | d44c758a-210a-4d12-88bd-60aa3522974b | True |
| C5_20 | 127 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 44.6 | 0c16bea7-1d87-4093-8fdf-1053efcbfb40 | True |
| C5_21 | 120 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 45.3 | cdd93b55-aeab-4232-8d5b-5408d1b039d7 | True |
| C5_22 | 266 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 70.8 | c96724b8-45d8-4ab4-9d98-68c3d4c8c719 | True |
| C5_23 | 180 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 54.3 | cc86330a-5e8f-48e5-83cd-7fe7eb1e450d | True |
| C5_24 | 382 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 87.4 | d5aba7d0-a9c4-4c4e-b7f0-7c7364dfecd6 | True |
| C5_25 | 191 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 55.9 | e0705e44-e924-4e84-b0f1-f61a183b5099 | True |
| C5_26 | 127 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 45.1 | 0802ecc2-066d-40fb-8274-8c829bdc7106 | True |
| C5_27 | 184 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 54.7 | aeb37432-5b54-4e58-ba39-301fccd36a6a | True |
| C5_28 | 101 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 41.1 | 041ed0be-90f3-4f9e-8bac-bf175845d747 | True |
| C5_29 | 259 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 69.1 | e43ec393-2726-4b0c-a7ea-fd556e9e5ca0 | True |
| C5_30 | 201 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 58.5 | f90f1b63-1111-41b3-9778-b82a1ad401fb | True |

**Trial 2** · `/health` before: `{"detector_loaded": true, "detector_model": "gpt2", "log_entries": 528, "ok": true, "rate_limiting": true}`

| id | words | http | label | duration_ms | content_id | pass |
|---|---|---|---|---|---|---|
| C5_01 | 112 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 42.8 | e26429d3-beb6-4872-b71e-66840d5bdc7c | True |
| C5_02 | 159 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 55.3 | 5f1ab437-35e8-43eb-9ee6-1977b9c46951 | True |
| C5_03 | 191 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 67.1 | 2a8ada7c-90c7-417f-b29b-0c543e028abf | True |
| C5_04 | 100 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 41.2 | b3109aeb-3c00-4986-ba91-ca857450ff13 | True |
| C5_05 | 165 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 50.9 | ff076d49-3fe3-44b1-bd88-c1ce67e08aa9 | True |
| C5_06 | 122 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 45.9 | 5d478eb5-e071-473a-a262-ca656928c8b2 | True |
| C5_07 | 229 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 81.2 | bb32875a-1647-4d65-97d0-c5cec2d900e8 | True |
| C5_08 | 273 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 96.1 | 91313bba-fced-4af3-9f29-5162f3978c99 | True |
| C5_09 | 113 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 42.6 | cc75abf0-d349-4d45-a578-eff43d092d09 | True |
| C5_10 | 117 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 43.6 | de01e44c-c8c1-4261-8637-2b18cf443e48 | True |
| C5_11 | 216 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 62.4 | b80da161-a931-4db4-9e01-039d837bc5bd | True |
| C5_12 | 151 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 49.1 | f9dce849-ff26-4066-afa3-4d1af7c5dfba | True |
| C5_13 | 109 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 44.6 | bb8cba77-5de8-4953-8547-4a1a8e932da1 | True |
| C5_14 | 258 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 74.7 | 83bd372e-8d99-4eeb-9b64-d14706de0d1f | True |
| C5_15 | 217 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 86.7 | 9c7416bf-d3d1-4fe2-8c26-113286e90034 | True |
| C5_16 | 116 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 44.9 | cc635bcb-7009-4bc2-a2de-1982d0e711c0 | True |
| C5_17 | 104 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 40.2 | a7a4269e-c0bc-48ac-b33d-79eb948c6711 | True |
| C5_18 | 397 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 115.1 | 337a0608-5ed5-4d5f-9411-95ce2d778158 | True |
| C5_19 | 190 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 58.6 | d4cbacf6-2af6-4db0-b74a-fc7cbfb7c0c0 | True |
| C5_20 | 127 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 46.8 | 21f3c18d-c078-4b72-b3b7-1f9c67a6e6bd | True |
| C5_21 | 120 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 43.8 | 2a2f94df-d2d6-4ae8-8fb7-ecab214bba9a | True |
| C5_22 | 266 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 72.5 | e1ab5c23-6b52-4ce8-92f6-641f0ae132d9 | True |
| C5_23 | 180 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 61.2 | 19307641-0c36-4062-82f5-a41df003e920 | True |
| C5_24 | 382 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 88.0 | 73a54f9a-171e-414f-9e3f-0382d5c29ef7 | True |
| C5_25 | 191 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 55.0 | b6dbe1e8-d7bc-4a7d-9cda-962b27e3b641 | True |
| C5_26 | 127 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 48.2 | e5ecdc9a-1622-48d1-8785-cc1edf40c710 | True |
| C5_27 | 184 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 56.1 | 6726b686-faa3-4e8b-a948-a26e49a95c69 | True |
| C5_28 | 101 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 40.7 | 6481df66-cbf0-4ee4-8841-b5aee5b1db92 | True |
| C5_29 | 259 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 71.1 | 1e56ad55-e36f-4865-97e8-d8aacf65f70f | True |
| C5_30 | 201 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 58.8 | bc07df05-b903-4757-9ae5-a7e7e19dfaf2 | True |

**Trial 3** · `/health` before: `{"detector_loaded": true, "detector_model": "gpt2", "log_entries": 613, "ok": true, "rate_limiting": true}`

| id | words | http | label | duration_ms | content_id | pass |
|---|---|---|---|---|---|---|
| C5_01 | 112 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 42.5 | 0dceddd7-3d6e-415a-b745-7aca4437af30 | True |
| C5_02 | 159 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 57.5 | ca798fd4-d44f-4f96-9d92-968577b42952 | True |
| C5_03 | 191 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 67.0 | 0c1c310c-ec5c-4c90-b994-0672b1d0af7b | True |
| C5_04 | 100 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 41.1 | 7224d23a-9109-467b-b6a7-c4a0128544c1 | True |
| C5_05 | 165 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 51.1 | 5b6b8aa5-5be7-4e0b-80b2-aeb4f0cdc18b | True |
| C5_06 | 122 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 46.3 | 796a929b-cfa1-46f8-a2bc-c36d04bbeee9 | True |
| C5_07 | 229 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 75.9 | a4a279a7-7fc0-43d6-971f-be31896b1f38 | True |
| C5_08 | 273 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 83.8 | f4e7c378-91ff-4823-afac-9bc69f6730a1 | True |
| C5_09 | 113 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 42.2 | f899533a-211d-4fd7-ac30-de74bf9528b4 | True |
| C5_10 | 117 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 43.8 | ac76e3b8-caed-469f-a4c1-53131bf6cddc | True |
| C5_11 | 216 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 64.5 | e33814d8-88e1-4626-8637-cf892d40c5d5 | True |
| C5_12 | 151 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 49.0 | ae4abbf9-ae7f-4fe2-8573-0394068f3f50 | True |
| C5_13 | 109 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 44.6 | 5345b750-190d-43e4-aceb-59108995c823 | True |
| C5_14 | 258 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 72.6 | cbb99029-2aaa-40b8-9091-46fd1c194be4 | True |
| C5_15 | 217 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 62.3 | 75837bf8-2d25-46f3-b7bf-0628da133525 | True |
| C5_16 | 116 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 46.7 | fc3ca9f8-ef0c-4f20-915b-cc50b420abec | True |
| C5_17 | 104 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 41.4 | 8ecdad5c-c723-42eb-909a-312747322c64 | True |
| C5_18 | 397 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 106.0 | 399c053e-6188-4e09-8343-5ebb799c2a99 | True |
| C5_19 | 190 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 58.4 | 43efa5f2-6597-4371-8ea8-c54505a94058 | True |
| C5_20 | 127 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 46.8 | 47f70a7d-14f2-49e8-a52f-b8065646cb8d | True |
| C5_21 | 120 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 45.1 | 83fe9bde-df27-483e-8d30-2e2d87fd0442 | True |
| C5_22 | 266 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 73.8 | 6d3cb71b-0a99-41b4-bd7c-d406f4b29d77 | True |
| C5_23 | 180 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 56.5 | aff44896-c55c-49ff-b643-6f7e1e5d5f70 | True |
| C5_24 | 382 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 89.0 | fc926e21-84eb-48a4-8a1d-2e2c8749ed77 | True |
| C5_25 | 191 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 58.9 | 9517d26a-3eb8-4162-8430-e1190a314bdd | True |
| C5_26 | 127 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 46.3 | 92719e97-d5f3-47f3-9e61-1e271509a658 | True |
| C5_27 | 184 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 56.9 | 49097d72-90c6-42a1-8c56-17e208ec8f52 | True |
| C5_28 | 101 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 42.4 | 2e6d7b9e-7324-4591-94ff-2be951c69faa | True |
| C5_29 | 259 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 99.6 | 8b806b57-7423-4742-af4c-713d9d1b6bec | True |
| C5_30 | 201 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 72.5 | 2901d833-382e-49d2-9e62-8c52b7b43e4a | True |
