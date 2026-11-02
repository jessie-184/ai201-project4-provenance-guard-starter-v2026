"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

# ── Scaling: where each raw measure counts as AI-like (1.0) or human-like (0.0) ──
# Set from my calibration texts (C1 clear AI, C2 personal human, C3 plain human).
# Values between the two ends are scaled in a straight line; values outside are clipped.
SPREAD_AI, SPREAD_HUMAN = 0.15, 0.55   # sentence-length spread (stdev / mean)
PUNCT_AI, PUNCT_HUMAN = 3.0, 8.0       # varied punctuation per 100 words
TTR_AI, TTR_HUMAN = 0.70, 0.95         # moving-average type-token ratio

# How much each measure counts inside the style signal.
# Type-token ratio gets the least: in calibration it pointed the WRONG way for
# plain human writing (C3 0.75, lower than the clear AI paragraph's 0.89).
W_SPREAD, W_PUNCT, W_TTR = 0.50, 0.35, 0.15

TTR_WINDOW = 50   # words per window, so long and short texts are comparable

# Punctuation that varies between writers. Full stops are left out on purpose:
# everyone uses them, so they say nothing about style.
_VARIED_PUNCTUATION = re.compile(r"[,;:!?()\u2014\u2013]|--|\s-\s")

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies: standard deviation of sentence lengths
    (in words) divided by the mean.

    Scale: 0 upwards. Higher = lumpier sentences = MORE HUMAN.
    Fewer than two sentences has no spread to measure and returns 0.0;
    style_signal treats that case as neutral rather than as AI-like.

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return round(statistics.stdev(lengths) / mean, 4) if mean else 0.0


def type_token_ratio(text: str) -> float:
    """
    How varied the vocabulary is: unique words over total words, averaged over
    sliding 50-word windows (a "moving-average" type-token ratio).

    Scale: 0 to 1. Higher = more varied vocabulary.
    Plain unique/total falls as text gets longer, so the windows keep a long
    text and a short one comparable. Texts of 50 words or fewer use plain
    unique/total.

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    if len(tokens) <= TTR_WINDOW:
        return round(len(set(tokens)) / len(tokens), 4)
    windows = [
        len(set(tokens[i:i + TTR_WINDOW])) / TTR_WINDOW
        for i in range(len(tokens) - TTR_WINDOW + 1)
    ]
    return round(statistics.mean(windows), 4)


def punctuation_density(text: str) -> float:
    """
    Varied punctuation per 100 words: commas, semicolons, colons, question and
    exclamation marks, parentheses, and dashes. Full stops are not counted.

    Scale: 0 upwards. Higher = more varied punctuation = MORE HUMAN.

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    return round(100 * len(_VARIED_PUNCTUATION.findall(text)) / len(tokens), 4)


# ── Combining them ───────────────────────────────────────────────────────────
def _ai_likeness(value: float, ai_end: float, human_end: float) -> float:
    """Map a raw measure onto 0–1, where 1.0 = at the AI end, 0.0 = at the human end."""
    position = (value - ai_end) / (human_end - ai_end)
    return min(max(1.0 - position, 0.0), 1.0)

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Each measure is flipped so higher = more AI-like, scaled onto 0–1 using the
    ranges at the top of this file, then combined as a weighted average
    (spread 0.50, punctuation 0.35, type-token ratio 0.15).

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    sentence_count = len([s for s in sentences(text) if words(s)])
    if sentence_count < 2:
        spread = 0.5   # one sentence: no evidence either way, so neutral
    else:
        spread = _ai_likeness(sentence_length_spread(text), SPREAD_AI, SPREAD_HUMAN)
    punct = _ai_likeness(punctuation_density(text), PUNCT_AI, PUNCT_HUMAN)
    ttr = _ai_likeness(type_token_ratio(text), TTR_AI, TTR_HUMAN)
    return round(W_SPREAD * spread + W_PUNCT * punct + W_TTR * ttr, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
