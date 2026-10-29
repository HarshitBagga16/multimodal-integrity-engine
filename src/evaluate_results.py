import json
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / "output" / "summary.json"
REPORT_PATH = ROOT / "EVALUATION.md"
METRICS_PATH = ROOT / "output" / "evaluation_metrics.json"

# Expected related pairs in our deliberately constructed test dataset.
# Each pair is unordered: A-B is the same as B-A.
GROUND_TRUTH = {
    frozenset(("01_ml_fundamentals.pdf", "02_ml_fundamentals_copy.pdf")),
    frozenset(("01_ml_fundamentals.pdf", "03_ml_paraphrase.pdf")),
    frozenset(("02_ml_fundamentals_copy.pdf", "03_ml_paraphrase.pdf")),

    frozenset(("04_network_security.pdf", "06_network_security.docx")),
    frozenset(("04_network_security.pdf", "07_network_security_copy.docx")),
    frozenset(("06_network_security.docx", "07_network_security_copy.docx")),

    frozenset(("05_climate_research.pdf", "10_solar_energy.docx")),
    frozenset(("05_climate_research.pdf", "11_renewable_speech.mp4")),
    frozenset(("10_solar_energy.docx", "11_renewable_speech.mp4")),
}


def main():
    if not SUMMARY_PATH.exists():
        raise FileNotFoundError(
            f"Run the integrity pipeline first. Missing: {SUMMARY_PATH}"
        )

    summary = json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))
    matrix = summary["comparison_matrix"]

    # Only compare files that have a row in the matrix.
    # Empty/silent files are reported separately as edge cases.
    files = sorted(matrix.keys())
    all_pairs = [
        (a, b)
        for a, b in combinations(files, 2)
    ]

    predicted = set()

    for a, b in all_pairs:
        score_ab = matrix.get(a, {}).get(b) or 0.0
        score_ba = matrix.get(b, {}).get(a) or 0.0

        # The current matrix stores matched-chunk coverage percentages.
        # A positive coverage in either direction counts as a detected pair.
        if max(score_ab, score_ba) > 0:
            predicted.add(frozenset((a, b)))

    actual = GROUND_TRUTH
    tp = len(predicted & actual)
    fp = len(predicted - actual)
    fn = len(actual - predicted)
    tn = len(all_pairs) - tp - fp - fn

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )
    accuracy = (tp + tn) / len(all_pairs) if all_pairs else 0.0

    metrics = {
        "files_evaluated": len(files),
        "total_unique_pairs": len(all_pairs),
        "ground_truth_positive_pairs": len(actual),
        "predicted_positive_pairs": len(predicted),
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "accuracy": round(accuracy, 4),
        "threshold_rule": "Detected if matched-chunk coverage > 0 in either direction",
    }

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Evaluation Report",
        "",
        "## Dataset and method",
        "",
        f"- Files evaluated: {len(files)} files with extracted text.",
        f"- Unique file pairs evaluated: {len(all_pairs)}.",
        f"- Expected related pairs: {len(actual)}.",
        "- Prediction rule: a pair is detected when matched-chunk coverage "
        "is greater than zero in either direction.",
        "- The matrix contains matched-chunk coverage percentages, "
        "not raw cosine similarity scores.",
        "",
        "## Metrics",
        "",
        "| Metric | Result |",
        "|---|---:|",
        f"| True positives | {tp} |",
        f"| False positives | {fp} |",
        f"| False negatives | {fn} |",
        f"| True negatives | {tn} |",
        f"| Precision | {precision:.2%} |",
        f"| Recall | {recall:.2%} |",
        f"| F1 score | {f1:.2%} |",
        f"| Accuracy | {accuracy:.2%} |",
        "",
        "## Confusion matrix",
        "",
        "| Actual / Predicted | Related | Not detected |",
        "|---|---:|---:|",
        f"| Related | {tp} (TP) | {fn} (FN) |",
        f"| Unrelated | {fp} (FP) | {tn} (TN) |",
        "",
        "## Detected pairs",
        "",
    ]

    if predicted:
        for pair in sorted(predicted, key=lambda p: sorted(p)):
            a, b = sorted(pair)
            label = "expected related" if pair in actual else "unexpected match"
            lines.append(f"- `{a}` ↔ `{b}` — {label}")
    else:
        lines.append("- No pairs detected.")

    lines.extend([
        "",
        "## Edge cases and limitations",
        "",
        "1. **Silent video:** `13_silent_video.mp4` has no extracted speech. "
        "The pipeline reports it as empty without crashing. It cannot compare "
        "content that was not extracted.",
        "",
        "2. **Unequal document lengths:** the renewable-energy video transcript "
        "is shorter than the PDF and DOCX. Coverage can differ by direction; "
        "a 100% score in one direction does not mean the entire pair is identical.",
        "",
        "3. **Chunk identification:** the network-security DOCX copies show "
        "only 50% coverage in the current matrix despite being exact copies. "
        "This indicates a likely chunk accounting/scoring limitation that "
        "should be fixed or disclosed.",
        "",
        "4. **Common boilerplate:** generic phrases shared by unrelated documents "
        "could trigger matches. A production system should down-weight common "
        "boilerplate and require meaningful matching text.",
        "",
        "5. **AI-writing estimate:** writing style alone cannot reliably prove "
        "that a document was generated by AI. This report does not claim to "
        "validate AI authorship.",
        "",
        "## Interpretation and trade-offs",
        "",
        "These results measure performance on a small, deliberately constructed "
        "synthetic dataset. They are not evidence of equivalent accuracy on real "
        "submissions. The current non-zero-coverage rule is intentionally simple "
        "and may over-flag weak matches. A stronger evaluation would tune a "
        "minimum semantic-similarity threshold on a larger labelled dataset, "
        "evaluate exact copies separately from paraphrases and cross-modal matches, "
        "and report precision/recall for each category.",
        "",
        "The silent video is excluded from pairwise metrics because no text was "
        "extracted; its graceful handling is assessed as an edge-case test.",
        "",
    ])

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print("Evaluation complete.")
    print(json.dumps(metrics, indent=2))
    print(f"\nMarkdown report: {REPORT_PATH}")
    print(f"Metrics JSON: {METRICS_PATH}")


if __name__ == "__main__":
    main()
