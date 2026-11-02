## Tracing the false positive

**The writer:** Minh, a second-language English speaker, submits a short personal essay he wrote himself. He sticks to words he's sure of, in short, clear sentences.

1. **Arrives:** `/submit` receives his text and `creator_id`. It's long enough to score.
2. **Signal one:** his common words and plain sentences are very predictable to GPT-2, so the model signal scores high, around 0.80. This is the blind spot doing exactly what it's known to do.
3. **Signal two:** his sentences are similar in length and his vocabulary repeats, so the style signal also leans AI-like, around 0.60.
4. **Score and label:** with weights of (0.55 / 0.45) the combined score is about 0.71. The two signals differ by only 0.20, so the disagreement cap doesn't apply. If my AI threshold were the starter's 0.65, Minh would be told his work is AI-generated.
5. **What he sees:** a label saying his own essay was probably written by AI, which is a wrong accusation.
6. **What he can do:** appeal with `/appeal`. His item moves to `under_review`, and a person looks at it. That's his only recourse.

**What this decides:** the AI threshold has to sit above the scores plain human writing can reach. If plain writing can score around 0.7, the AI label should need something like 0.80 or more, so Minh lands in "unsure" instead. That costs us some AI text slipping through as "unsure," which is the trade we choose. The unsure label must also not read as an accusation, and it should tell him he can appeal.

## Endpoint contracts

### POST /submit

**Request (JSON):**
| Field | Type | Required | Meaning |
|---|---|---|---|
| `text` | string | yes | The writing to check |
| `creator_id` | string | yes | Who submitted it |

**Response 200 (JSON):**
| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Unique id for this submission; needed to appeal |
| `guess` | string | `"ai"`, `"human"`, or `"unsure"` |
| `confidence` | float 0–1 | Combined score; higher = more likely AI |
| `label` | string | The full sentence the reader sees |
| `model_score` | float 0–1 | Signal one |
| `style_score` | float 0–1 | Signal two |
| `status` | string | `"decided"` |

**Errors (400, JSON `{"error": ..., "message": ...}`):** the request body is not valid JSON; `text` missing or not a string; `text` empty or too short to score; `text` over the length limit; `creator_id` missing or empty. Nothing is scored, and the rejection is logged.

### POST /appeal

**Request (JSON):**
| Field | Type | Required | Meaning |
|---|---|---|---|
| `content_id` | string | yes | The submission being appealed |
| `reasoning` | string | yes | The writer's explanation |

**Response 200 (JSON):**
| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Echoes the appealed submission |
| `status` | string | `"under_review"` |
| `message` | string | Plain-English confirmation for the writer |

**Errors:** 400 if `content_id` or `reasoning` is missing or empty; 404 if `content_id` doesn't exist in the log.

**Second appeal:** an appeal on an item already `under_review` returns 200, keeps the status `under_review`, and does not log a duplicate appeal.