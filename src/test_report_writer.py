
import json
from pathlib import Path

from src.reporting.report_writer import (
    write_json_report,
    write_markdown_report,
)


def main():
    output_dir = Path("output/report_writer_test")

    summary = {
        "files": ["a.pdf", "b.docx"],
        "comparison_matrix": {
            "a.pdf": {"a.pdf": None, "b.docx": 50.0},
            "b.docx": {"a.pdf": 25.0, "b.docx": None},
        },
    }

    matches = [
        {
            "query_file": "a.pdf",
            "matched_file": "b.docx",
            "similarity": 0.91,
            "query_page": 1,
            "matched_page": None,
            "query_timestamp": None,
            "matched_timestamp": None,
            "query_text": "Machine learning identifies patterns.",
            "matched_text": "Machine learning identifies patterns.",
        }
    ]

    json_path = output_dir / "a.json"
    markdown_path = output_dir / "integrity_report.md"

    write_json_report(
        {"filename": "a.pdf", "matches": matches},
        json_path,
    )
    write_markdown_report(summary, matches, markdown_path)

    with json_path.open(encoding="utf-8") as file:
        loaded = json.load(file)

    assert loaded["filename"] == "a.pdf"
    assert markdown_path.exists()
    assert "Machine learning identifies patterns." in (
        markdown_path.read_text(encoding="utf-8")
    )

    print("JSON report:", json_path.resolve())
    print("Markdown report:", markdown_path.resolve())
    print("\nReport writer tests passed!")


if __name__ == "__main__":
    main()
