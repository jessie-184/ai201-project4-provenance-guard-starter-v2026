# Capstone run log — after

- Produced by: `run_capstone.py::main` · inputs: `capstone_inputs.py`
- Service: `app.py::submit` (gate: `app.py::_gate`) · commit `3cb84c7`
- 3 trials, 65s apart, nothing changed in between · started 2026-11-11 18:49:03
- creator_id prefix: `cap_11111849_t<trial>_`

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Control characters refused | 10 of 10 refused (400, no decided line) | 10/10 refused | 10/10 refused | 10/10 refused | MET |
| 2. Non-English refused | at least 9 of 10 refused (400) | 5/10 refused | 5/10 refused | 5/10 refused | MISSED |
| 3. Short human texts not refused | 0 of 20 refused by the gate | 5/20 refused | 5/20 refused | 5/20 refused | MISSED |
| 4. Bad requests logged | 10 of 10 with exactly one rejected line, reason + duration_ms | 10/10 logged | 10/10 logged | 10/10 logged | MET |
| 5. Warm latency | at least 29 of 30 at or under 150 ms (warm model) | 30/30 ≤ 150 ms | 30/30 ≤ 150 ms | 30/30 ≤ 150 ms | MET |

## Criterion 1 — control characters

**Trial 1**

| id | code | http | error | decided_lines | duration_ms | pass |
|---|---|---|---|---|---|---|
| C1_01 | 0x00 null | 400 | control_characters | 0 | 0.4 | True |
| C1_02 | 0x04 end of transmission | 400 | control_characters | 0 | 0.2 | True |
| C1_03 | 0x07 bell | 400 | control_characters | 0 | 0.2 | True |
| C1_04 | 0x08 backspace | 400 | control_characters | 0 | 0.2 | True |
| C1_05 | 0x0B vertical tab | 400 | control_characters | 0 | 0.3 | True |
| C1_06 | 0x0C form feed | 400 | control_characters | 0 | 0.2 | True |
| C1_07 | 0x1A substitute | 400 | control_characters | 0 | 0.2 | True |
| C1_08 | 0x1B escape (ANSI colour) | 400 | control_characters | 0 | 0.2 | True |
| C1_09 | 0x1F unit separator | 400 | control_characters | 0 | 0.2 | True |
| C1_10 | 0x7F delete | 400 | control_characters | 0 | 0.3 | True |

**Trial 2**

| id | code | http | error | decided_lines | duration_ms | pass |
|---|---|---|---|---|---|---|
| C1_01 | 0x00 null | 400 | control_characters | 0 | 1.3 | True |
| C1_02 | 0x04 end of transmission | 400 | control_characters | 0 | 0.3 | True |
| C1_03 | 0x07 bell | 400 | control_characters | 0 | 0.3 | True |
| C1_04 | 0x08 backspace | 400 | control_characters | 0 | 0.3 | True |
| C1_05 | 0x0B vertical tab | 400 | control_characters | 0 | 0.3 | True |
| C1_06 | 0x0C form feed | 400 | control_characters | 0 | 0.2 | True |
| C1_07 | 0x1A substitute | 400 | control_characters | 0 | 0.3 | True |
| C1_08 | 0x1B escape (ANSI colour) | 400 | control_characters | 0 | 0.3 | True |
| C1_09 | 0x1F unit separator | 400 | control_characters | 0 | 0.3 | True |
| C1_10 | 0x7F delete | 400 | control_characters | 0 | 0.5 | True |

**Trial 3**

| id | code | http | error | decided_lines | duration_ms | pass |
|---|---|---|---|---|---|---|
| C1_01 | 0x00 null | 400 | control_characters | 0 | 0.4 | True |
| C1_02 | 0x04 end of transmission | 400 | control_characters | 0 | 0.3 | True |
| C1_03 | 0x07 bell | 400 | control_characters | 0 | 0.3 | True |
| C1_04 | 0x08 backspace | 400 | control_characters | 0 | 0.3 | True |
| C1_05 | 0x0B vertical tab | 400 | control_characters | 0 | 0.3 | True |
| C1_06 | 0x0C form feed | 400 | control_characters | 0 | 0.2 | True |
| C1_07 | 0x1A substitute | 400 | control_characters | 0 | 0.3 | True |
| C1_08 | 0x1B escape (ANSI colour) | 400 | control_characters | 0 | 0.2 | True |
| C1_09 | 0x1F unit separator | 400 | control_characters | 0 | 0.3 | True |
| C1_10 | 0x7F delete | 400 | control_characters | 0 | 0.2 | True |

## Criterion 2 — non-English

**Trial 1**

| id | language | http | error | label | duration_ms | pass |
|---|---|---|---|---|---|---|
| C2_01 | Arabic | 400 | not_english_text |  | 0.2 | True |
| C2_02 | Russian | 400 | not_english_text |  | 0.3 | True |
| C2_03 | Chinese | 400 | not_english_text |  | 0.1 | True |
| C2_04 | Hindi | 400 | not_english_text |  | 0.2 | True |
| C2_05 | Korean | 400 | not_english_text |  | 0.2 | True |
| C2_06 | Spanish | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 35.3 | False |
| C2_07 | French | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 37.0 | False |
| C2_08 | German | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 35.2 | False |
| C2_09 | Vietnamese | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 51.8 | False |
| C2_10 | Indonesian | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 35.7 | False |

**Trial 2**

| id | language | http | error | label | duration_ms | pass |
|---|---|---|---|---|---|---|
| C2_01 | Arabic | 400 | not_english_text |  | 0.2 | True |
| C2_02 | Russian | 400 | not_english_text |  | 0.4 | True |
| C2_03 | Chinese | 400 | not_english_text |  | 0.3 | True |
| C2_04 | Hindi | 400 | not_english_text |  | 0.3 | True |
| C2_05 | Korean | 400 | not_english_text |  | 0.2 | True |
| C2_06 | Spanish | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 85.6 | False |
| C2_07 | French | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 38.2 | False |
| C2_08 | German | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 36.9 | False |
| C2_09 | Vietnamese | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 50.9 | False |
| C2_10 | Indonesian | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 36.4 | False |

**Trial 3**

| id | language | http | error | label | duration_ms | pass |
|---|---|---|---|---|---|---|
| C2_01 | Arabic | 400 | not_english_text |  | 0.4 | True |
| C2_02 | Russian | 400 | not_english_text |  | 0.2 | True |
| C2_03 | Chinese | 400 | not_english_text |  | 0.2 | True |
| C2_04 | Hindi | 400 | not_english_text |  | 0.2 | True |
| C2_05 | Korean | 400 | not_english_text |  | 0.3 | True |
| C2_06 | Spanish | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 37.7 | False |
| C2_07 | French | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 37.5 | False |
| C2_08 | German | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 36.9 | False |
| C2_09 | Vietnamese | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 50.0 | False |
| C2_10 | Indonesian | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 34.9 | False |

## Criterion 3 — short human texts

**Trial 1**

| id | http | error | label | duration_ms | pass |
|---|---|---|---|---|---|
| C3_01 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.4 | True |
| C3_02 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 22.8 | True |
| C3_03 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.0 | True |
| C3_04 | 400 | not_english_text |  | 0.3 | False |
| C3_05 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 28.5 | True |
| C3_06 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 21.4 | True |
| C3_07 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 21.9 | True |
| C3_08 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.0 | True |
| C3_09 | 400 | not_english_text |  | 0.3 | False |
| C3_10 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.2 | True |
| C3_11 | 400 | not_english_text |  | 0.3 | False |
| C3_12 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 18.5 | True |
| C3_13 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.6 | True |
| C3_14 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 20.9 | True |
| C3_15 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.2 | True |
| C3_16 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.3 | True |
| C3_17 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.2 | True |
| C3_18 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 21.7 | True |
| C3_19 | 400 | not_english_text |  | 0.3 | False |
| C3_20 | 400 | not_english_text |  | 0.2 | False |

**Trial 2**

| id | http | error | label | duration_ms | pass |
|---|---|---|---|---|---|
| C3_01 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.7 | True |
| C3_02 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 23.0 | True |
| C3_03 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.2 | True |
| C3_04 | 400 | not_english_text |  | 0.3 | False |
| C3_05 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 29.3 | True |
| C3_06 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 21.1 | True |
| C3_07 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 22.2 | True |
| C3_08 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.0 | True |
| C3_09 | 400 | not_english_text |  | 0.3 | False |
| C3_10 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 18.1 | True |
| C3_11 | 400 | not_english_text |  | 0.3 | False |
| C3_12 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.4 | True |
| C3_13 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.5 | True |
| C3_14 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 22.0 | True |
| C3_15 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 18.0 | True |
| C3_16 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.4 | True |
| C3_17 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.5 | True |
| C3_18 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 21.6 | True |
| C3_19 | 400 | not_english_text |  | 0.3 | False |
| C3_20 | 400 | not_english_text |  | 0.2 | False |

**Trial 3**

| id | http | error | label | duration_ms | pass |
|---|---|---|---|---|---|
| C3_01 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.6 | True |
| C3_02 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 23.3 | True |
| C3_03 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.0 | True |
| C3_04 | 400 | not_english_text |  | 0.3 | False |
| C3_05 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 28.6 | True |
| C3_06 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 23.3 | True |
| C3_07 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 24.4 | True |
| C3_08 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.9 | True |
| C3_09 | 400 | not_english_text |  | 0.3 | False |
| C3_10 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.1 | True |
| C3_11 | 400 | not_english_text |  | 0.2 | False |
| C3_12 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.7 | True |
| C3_13 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.8 | True |
| C3_14 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 21.4 | True |
| C3_15 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.5 | True |
| C3_16 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 17.0 | True |
| C3_17 | 200 |  | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 16.6 | True |
| C3_18 | 200 |  | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 21.4 | True |
| C3_19 | 400 | not_english_text |  | 0.3 | False |
| C3_20 | 400 | not_english_text |  | 0.3 | False |

## Criterion 4 — bad requests

**Trial 1**

| id | what | http | log_lines | rejected_lines | reason | duration_ms | pass |
|---|---|---|---|---|---|---|---|
| C4_01 | invalid JSON | 400 | 1 | 1 | invalid_json | 0.2 | True |
| C4_02 | missing creator_id | 400 | 1 | 1 | missing_creator_id | 0.2 | True |
| C4_03 | missing text | 400 | 1 | 1 | missing_text | 0.1 | True |
| C4_04 | empty text | 400 | 1 | 1 | empty_text | 0.2 | True |
| C4_05 | text over 10,000 characters | 400 | 1 | 1 | text_too_long | 0.2 | True |
| C4_06 | punctuation-only text | 400 | 1 | 1 | not_english_text | 0.4 | True |
| C4_07 | one-word text | 400 | 1 | 1 | too_few_words | 0.1 | True |
| C4_08 | rate-limited (6th request in a minute) | 429 | 1 | 1 | rate_limited | 0.3 | True |
| C4_09 | control characters (clear screen) | 400 | 1 | 1 | control_characters | 0.2 | True |
| C4_10 | control character (0x03, Ctrl+C) | 400 | 1 | 1 | control_characters | 0.2 | True |

**Trial 2**

| id | what | http | log_lines | rejected_lines | reason | duration_ms | pass |
|---|---|---|---|---|---|---|---|
| C4_01 | invalid JSON | 400 | 1 | 1 | invalid_json | 0.2 | True |
| C4_02 | missing creator_id | 400 | 1 | 1 | missing_creator_id | 0.2 | True |
| C4_03 | missing text | 400 | 1 | 1 | missing_text | 0.2 | True |
| C4_04 | empty text | 400 | 1 | 1 | empty_text | 0.3 | True |
| C4_05 | text over 10,000 characters | 400 | 1 | 1 | text_too_long | 0.2 | True |
| C4_06 | punctuation-only text | 400 | 1 | 1 | not_english_text | 0.3 | True |
| C4_07 | one-word text | 400 | 1 | 1 | too_few_words | 0.2 | True |
| C4_08 | rate-limited (6th request in a minute) | 429 | 1 | 1 | rate_limited | 0.3 | True |
| C4_09 | control characters (clear screen) | 400 | 1 | 1 | control_characters | 0.2 | True |
| C4_10 | control character (0x03, Ctrl+C) | 400 | 1 | 1 | control_characters | 0.2 | True |

**Trial 3**

| id | what | http | log_lines | rejected_lines | reason | duration_ms | pass |
|---|---|---|---|---|---|---|---|
| C4_01 | invalid JSON | 400 | 1 | 1 | invalid_json | 0.2 | True |
| C4_02 | missing creator_id | 400 | 1 | 1 | missing_creator_id | 0.2 | True |
| C4_03 | missing text | 400 | 1 | 1 | missing_text | 0.2 | True |
| C4_04 | empty text | 400 | 1 | 1 | empty_text | 0.1 | True |
| C4_05 | text over 10,000 characters | 400 | 1 | 1 | text_too_long | 0.2 | True |
| C4_06 | punctuation-only text | 400 | 1 | 1 | not_english_text | 0.2 | True |
| C4_07 | one-word text | 400 | 1 | 1 | too_few_words | 0.3 | True |
| C4_08 | rate-limited (6th request in a minute) | 429 | 1 | 1 | rate_limited | 0.3 | True |
| C4_09 | control characters (clear screen) | 400 | 1 | 1 | control_characters | 0.3 | True |
| C4_10 | control character (0x03, Ctrl+C) | 400 | 1 | 1 | control_characters | 0.2 | True |

## Criterion 5 — warm latency

**Trial 1** · `/health` before: `{"detector_loaded": true, "detector_model": "gpt2", "log_entries": 699, "ok": true, "rate_limiting": true}`

| id | words | http | label | duration_ms | content_id | pass |
|---|---|---|---|---|---|---|
| C5_01 | 112 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 41.8 | 25f09e99-3c13-41a4-80e8-4f42faeadc4b | True |
| C5_02 | 159 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 59.9 | 16b253f8-d4da-403f-91cb-24858384fae2 | True |
| C5_03 | 191 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 66.8 | 10c29468-f1ea-4cd9-b3f6-0a71237c68a6 | True |
| C5_04 | 100 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 42.1 | b6447685-f8a1-44b0-93ea-ce4bbaeb2a41 | True |
| C5_05 | 165 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 54.8 | e6f55585-80b2-45f6-a787-fc6c0e0b0092 | True |
| C5_06 | 122 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 48.0 | 78921ee5-0087-4585-a944-c9633ca281dc | True |
| C5_07 | 229 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 73.3 | b5232545-2099-425a-b12f-a345b01ef842 | True |
| C5_08 | 273 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 90.1 | e7b19355-7cbd-49b6-b5fa-1f3f9bdb47d5 | True |
| C5_09 | 113 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 42.7 | bdb3994b-96f5-4667-94ed-5320d2d5d25c | True |
| C5_10 | 117 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 44.1 | 2a70365f-2980-42a6-84ab-591dabfabdbe | True |
| C5_11 | 216 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 64.7 | 13dbbdf4-6b08-4e54-bd46-9a1084a80912 | True |
| C5_12 | 151 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 49.5 | fdb6edf5-244e-47ec-b9e1-8d2f5941f94c | True |
| C5_13 | 109 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 53.8 | d82b6369-995d-41fc-85f1-69f15681fd62 | True |
| C5_14 | 258 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 75.7 | 23c2336c-3dbb-49ed-aa36-f998cd2971c2 | True |
| C5_15 | 217 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 62.1 | 42669d6d-9728-4cd6-8c70-7f0000ef4336 | True |
| C5_16 | 116 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 46.1 | f9d83c6e-d77c-444d-94c2-ca310706d0ec | True |
| C5_17 | 104 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 42.0 | c8ed837f-9e29-4e87-aa34-bb90d34b4973 | True |
| C5_18 | 397 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 114.4 | edf243fa-b736-46d3-b717-3bb54ac47f13 | True |
| C5_19 | 190 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 63.0 | 072b6f1a-39c9-49f3-9259-8f35a6170abb | True |
| C5_20 | 127 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 50.9 | 1bbfeedc-3ed9-4536-953a-294c2e83e598 | True |
| C5_21 | 120 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 78.0 | 3cc567b1-c592-4013-9243-5626e915c389 | True |
| C5_22 | 266 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 100.3 | 7a1f59c0-eef2-4444-a2f6-53856c36385d | True |
| C5_23 | 180 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 78.2 | d093fb9f-b7c0-49ba-a4aa-44991b153400 | True |
| C5_24 | 382 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 135.8 | 56bba4d7-4232-410e-b101-af0fd9fd30b1 | True |
| C5_25 | 191 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 78.1 | c27dd642-d52d-4bc3-825c-bf3cee4ae443 | True |
| C5_26 | 127 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 61.3 | 3c208b7f-d24e-42a2-965d-4e729e3ad2dc | True |
| C5_27 | 184 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 75.5 | eca202ff-defc-4a6f-95bd-947198ee6916 | True |
| C5_28 | 101 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 58.4 | 7a213b3e-31af-4642-a63c-03981ae25e05 | True |
| C5_29 | 259 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 84.1 | 33ae9ae4-4bb9-43fb-889b-0cf3ec222c40 | True |
| C5_30 | 201 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 73.7 | d9398257-6d61-4da0-a51b-d341c0639f0b | True |

**Trial 2** · `/health` before: `{"detector_loaded": true, "detector_model": "gpt2", "log_entries": 784, "ok": true, "rate_limiting": true}`

| id | words | http | label | duration_ms | content_id | pass |
|---|---|---|---|---|---|---|
| C5_01 | 112 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 42.2 | d1b2ae4f-8b9a-4d44-a3ea-44ca0fa1e8f4 | True |
| C5_02 | 159 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 57.7 | 3851b7ef-5c17-41ea-a212-45212ef19658 | True |
| C5_03 | 191 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 64.8 | 089a450e-8eb6-43ea-a8e1-a1819b5471b0 | True |
| C5_04 | 100 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 41.7 | 1897c1f6-8a0c-4fb3-9b77-58bd3a1079fb | True |
| C5_05 | 165 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 52.0 | 5e5d448a-a4ac-440d-b9e4-7cda9388bb4a | True |
| C5_06 | 122 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 71.3 | 710815e7-23f2-45a2-bc9c-f6d778789bf8 | True |
| C5_07 | 229 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 81.3 | d02e3188-8363-4652-b310-3cd2078060f6 | True |
| C5_08 | 273 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 87.3 | 37b1b827-5640-4b62-b1d3-cb64adb54ef4 | True |
| C5_09 | 113 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 41.9 | 2ee19f45-e8de-46bf-a35b-88ae64d91198 | True |
| C5_10 | 117 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 44.6 | b166537c-9eb3-4689-b08b-c60dd3249692 | True |
| C5_11 | 216 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 62.0 | 681235b3-ecff-4cc3-a1fa-d60b9f413d06 | True |
| C5_12 | 151 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 50.0 | b04d81c2-e5df-489a-ad65-a6c12be0c176 | True |
| C5_13 | 109 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 45.1 | e74398ea-af3a-4540-af5d-099b1c4d73ce | True |
| C5_14 | 258 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 71.7 | 3986fbf0-77be-4d76-a127-8551a67e15bb | True |
| C5_15 | 217 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 63.7 | 9808ce2a-4fe5-4228-9502-d3cf6c95eda8 | True |
| C5_16 | 116 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 44.8 | 7d2b7bb3-d70e-445b-96ff-e3f65c8de10f | True |
| C5_17 | 104 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 41.1 | 8312bb08-7e02-475c-9c3c-3cf5e47b26e0 | True |
| C5_18 | 397 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 107.6 | fe9cd5b7-b3f2-46bf-ad88-903539f7c1ae | True |
| C5_19 | 190 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 58.9 | ca6d4b62-e679-4a60-97fe-12e659442956 | True |
| C5_20 | 127 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 48.3 | fa4629dc-9d0f-4b94-9132-4f0eb0b64b05 | True |
| C5_21 | 120 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 45.9 | b1337593-fd31-4a50-a8e4-7206239e26bc | True |
| C5_22 | 266 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 73.7 | 190ad97d-9d2d-49ba-9a6d-1b0df50355ea | True |
| C5_23 | 180 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 57.2 | 313ddd55-c061-41e9-b200-2ce29c51dd02 | True |
| C5_24 | 382 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 91.8 | 75a0bb5e-fe53-4cfb-a499-242e575427a8 | True |
| C5_25 | 191 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 65.3 | bb717c21-a708-431f-8a0d-bdd5964b8c6b | True |
| C5_26 | 127 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 56.5 | 9973411f-de04-4fa3-9905-4ce6db8617f4 | True |
| C5_27 | 184 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 62.6 | 70873761-d282-40c6-b0fd-8abd82024795 | True |
| C5_28 | 101 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 46.1 | 9efb178b-77a5-491d-b50b-d106556d038b | True |
| C5_29 | 259 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 79.2 | b58179af-31ff-4857-b24c-2194a91c4ca2 | True |
| C5_30 | 201 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 69.5 | 1d51211a-fe7a-474f-b5c3-6482354c828a | True |

**Trial 3** · `/health` before: `{"detector_loaded": true, "detector_model": "gpt2", "log_entries": 869, "ok": true, "rate_limiting": true}`

| id | words | http | label | duration_ms | content_id | pass |
|---|---|---|---|---|---|---|
| C5_01 | 112 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 42.3 | 3d550268-751e-48f7-81ae-8752991f7482 | True |
| C5_02 | 159 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 57.0 | ac41a832-1cff-4a76-a69d-7ef191c50d05 | True |
| C5_03 | 191 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 67.7 | c5e8c421-db4b-4e85-bb8c-fffec4fb4d68 | True |
| C5_04 | 100 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 41.9 | 39921911-b122-4f80-aca6-07767a0db4e5 | True |
| C5_05 | 165 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 50.9 | 003f52ee-2173-4d58-948e-1982087ac8b0 | True |
| C5_06 | 122 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 47.0 | cf77b727-4056-42c5-b747-5369cd8d2beb | True |
| C5_07 | 229 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 74.5 | 724fbc37-16a7-42f6-a2a8-e465ee233124 | True |
| C5_08 | 273 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 83.7 | 0b541520-e096-4d5c-942d-fe51099facc2 | True |
| C5_09 | 113 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 42.4 | fabdf65e-c981-426b-8564-0fe6df3505bc | True |
| C5_10 | 117 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 45.3 | e0b4812c-0f4a-4ae5-90bf-038236421291 | True |
| C5_11 | 216 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 62.3 | 6b375dba-0a82-414f-af8b-92d55d6a3886 | True |
| C5_12 | 151 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 52.2 | f5984b54-bba8-4ac0-9a31-f70f8d0a8e4b | True |
| C5_13 | 109 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 45.3 | 2cad5e58-8b8a-49dc-90bb-901ccb18bec0 | True |
| C5_14 | 258 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 73.4 | 56960604-8745-412d-b3a3-5d8e944bb5b6 | True |
| C5_15 | 217 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 62.8 | 5d49a1d1-1930-4792-bdb9-db9b967e0705 | True |
| C5_16 | 116 | 200 | This was probably written with help from AI. Our check found strong signs of machine-generated writing. Automated checks can be wrong, so the writer can ask for a person to review this. | 46.1 | 54de6dd2-09d9-4ea2-b457-2d0b33170cfe | True |
| C5_17 | 104 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 42.1 | e579512c-3f72-4a17-9b60-e4bb31ae33fd | True |
| C5_18 | 397 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 105.0 | 92987e86-cb90-4253-8f22-2f8011f90c71 | True |
| C5_19 | 190 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 76.3 | e19a68da-995f-4ce9-a02f-534d3081ce05 | True |
| C5_20 | 127 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 48.4 | 6f1a9881-f38e-4fbc-b9d0-0bc9f1a0c1c0 | True |
| C5_21 | 120 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 45.6 | d3348807-127e-4834-b0f7-4217fb211f4a | True |
| C5_22 | 266 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 70.7 | f51afe5e-c683-4165-8fd9-72b59da90a30 | True |
| C5_23 | 180 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 61.0 | 88e21533-9a23-41f0-9eb3-6a2cf4835807 | True |
| C5_24 | 382 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 92.8 | 5584aae6-2c85-4f25-bb01-5c682eb07d52 | True |
| C5_25 | 191 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 56.5 | 1d663a1d-025d-4a91-ad2d-7fc56723d8c7 | True |
| C5_26 | 127 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 45.8 | 74f41d64-8d74-441a-b717-7dc43771d9b5 | True |
| C5_27 | 184 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 57.7 | 3de4e9d9-47ff-438b-8eca-ad6436ad0c68 | True |
| C5_28 | 101 | 200 | We can't tell whether this was written by a person or with help from AI. A lot of genuine writing looks like this, so this isn't a sign that anything is wrong. If you wrote this and want a person to take a look, you can ask for a review. | 41.5 | 37ac1321-8488-4456-9205-9b17fce6f5ed | True |
| C5_29 | 259 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 71.5 | 87523699-2c4f-425b-9688-84eb3856a87d | True |
| C5_30 | 201 | 200 | This looks like it was written by a person. Our check found the patterns we usually see in human writing. | 59.5 | ee847072-1756-496a-b590-c22429391e9e | True |
