
import json
from pathlib import Path


def write_json_report(data: dict, output_path: Path) -> None:
    """Write a structured JSON report."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def write_markdown_report(
    summary: dict,
    matches: list[dict],
    output_path: Path,
) -> None:
    """Write an overall human-readable integrity report."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Multimodal Submission Integrity Report",
        "",
        "> Similarity indicates potential overlap, not proof of plagiarism.",
        "",
        "## Submissions",
        "",
    ]

    for filename in summary["files"]:
        lines.append(f"- {filename}")

    lines.extend([
        "",
        "## Pairwise matched-chunk coverage",
        "",
        "Coverage is directional and based on unique matched source chunks.",
        "",
    ])

    files = summary["files"]
    header = "| Submission | " + " | ".join(files) + " |"
    separator = "|---|" + "---:|" * len(files)

    lines.extend([header, separator])

    for source_file in files:
        values = []

        for target_file in files:
            score = summary["comparison_matrix"][source_file][target_file]

            if score is None:
                values.append("—")
            else:
                values.append(f"{score:.2f}%")

        lines.append(
            "| " + source_file + " | " + " | ".join(values) + " |"
        )

    lines.extend(["", "## Matching evidence", ""])

    if not matches:
        lines.append("No matches found at the configured threshold.")
    else:
        for index, match in enumerate(matches, start=1):
            lines.extend([
                f"### Match {index}",
                "",
                f"- Query file: `{match['query_file']}`",
                f"- Matched file: `{match['matched_file']}`",
                f"- Similarity: {match['similarity']:.4f}",
                f"- Query page: {match.get('query_page')}",
                f"- Matched page: {match.get('matched_page')}",
                f"- Query timestamp: {match.get('query_timestamp')}",
                f"- Matched timestamp: {match.get('matched_timestamp')}",
                "",
                "**Query passage**",
                "",
                f"> {match['query_text']}",
                "",
                "**Matched passage**",
                "",
                f"> {match['matched_text']}",
                "",
            ])

    output_path.write_text("\n".join(lines), encoding="utf-8")
