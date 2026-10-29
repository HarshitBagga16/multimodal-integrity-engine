import re
from statistics import pstdev


TRANSITION_PHRASES = [
    "furthermore",
    "moreover",
    "in conclusion",
    "it is important to note",
    "additionally",
    "consequently",
    "in summary",
    "on the other hand",
]


def estimate_ai_style(text: str) -> dict:
    """Return transparent writing-style signals, not an AI authorship verdict."""
    if not text or not text.strip():
        return {
            "score": None,
            "label": "not assessable",
            "signals": {},
            "disclaimer": "Writing style cannot establish AI authorship.",
        }

    sentences = [
        sentence.strip()
        for sentence in re.split(r"[.!?]+", text)
        if len(sentence.split()) >= 4
    ]
    words = re.findall(r"\b[\w'-]+\b", text.lower())

    transition_count = sum(
        len(re.findall(r"\b" + re.escape(phrase) + r"\b", text.lower()))
        for phrase in TRANSITION_PHRASES
    )

    sentence_lengths = [len(sentence.split()) for sentence in sentences]
    length_variation = pstdev(sentence_lengths) if len(sentence_lengths) > 1 else 0.0

    # Simple, documented heuristic. These are stylistic signals only.
    transition_rate = transition_count / max(len(sentences), 1)
    transition_signal = min(transition_rate / 0.30, 1.0) * 40
    consistency_signal = max(0.0, 1.0 - length_variation / 12.0) * 30
    length_signal = min(len(words) / 150.0, 1.0) * 30

    score = round(
        min(100.0, transition_signal + consistency_signal + length_signal),
        1,
    )

    if len(words) < 40:
        label = "insufficient text"
    elif score >= 65:
        label = "higher stylistic signals"
    elif score >= 40:
        label = "moderate stylistic signals"
    else:
        label = "lower stylistic signals"

    return {
        "score": score,
        "label": label,
        "signals": {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "transition_phrase_count": transition_count,
            "sentence_length_stddev": round(length_variation, 2),
        },
        "disclaimer": (
            "Heuristic style score only. It is not a calibrated probability "
            "and must not be used as proof of AI authorship."
        ),
    }
