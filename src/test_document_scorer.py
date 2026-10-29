
from src.matching.document_scorer import build_document_summary


def main():
    chunks = [
        {"source_file": "a.pdf", "chunk_number": 1},
        {"source_file": "a.pdf", "chunk_number": 2},
        {"source_file": "a.pdf", "chunk_number": 3},
        {"source_file": "a.pdf", "chunk_number": 4},
        {"source_file": "b.docx", "chunk_number": 1},
        {"source_file": "b.docx", "chunk_number": 2},
    ]

    matches = [
        {
            "query_file": "a.pdf",
            "matched_file": "b.docx",
            "query_chunk": 1,
        },
        {
            "query_file": "a.pdf",
            "matched_file": "b.docx",
            "query_chunk": 2,
        },
        {
            "query_file": "b.docx",
            "matched_file": "a.pdf",
            "query_chunk": 1,
        },
    ]

    summary = build_document_summary(chunks, matches)

    print("Comparison matrix:")

    for filename, row in summary["comparison_matrix"].items():
        print(filename, row)

    assert summary["comparison_matrix"]["a.pdf"]["b.docx"] == 50.0
    assert summary["comparison_matrix"]["b.docx"]["a.pdf"] == 50.0
    assert summary["comparison_matrix"]["a.pdf"]["a.pdf"] is None

    print("\nDocument scorer tests passed!")


if __name__ == "__main__":
    main()
