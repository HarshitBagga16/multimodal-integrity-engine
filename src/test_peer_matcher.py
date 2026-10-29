
from src.matching.embedding_engine import EmbeddingEngine
from src.matching.peer_matcher import compare_submissions


def main():
    chunks = [
        {
            "text": (
                "Machine learning identifies patterns in data "
                "and helps computers make predictions."
            ),
            "source_file": "student_a.pdf",
            "page_number": 1,
            "timestamp": None,
            "chunk_number": 1,
        },
        {
            "text": (
                "Machine learning identifies patterns in data "
                "and helps computers make predictions."
            ),
            "source_file": "student_b.docx",
            "page_number": None,
            "timestamp": None,
            "chunk_number": 1,
        },
        {
            "text": "The weather forecast predicts rain tomorrow.",
            "source_file": "student_c.pdf",
            "page_number": 1,
            "timestamp": None,
            "chunk_number": 1,
        },
    ]

    engine = EmbeddingEngine()
    matches = compare_submissions(chunks, engine, threshold=0.70)

    for match in matches:
        print(
            f"{match['query_file']} -> {match['matched_file']} | "
            f"similarity={match['similarity']:.3f}"
        )

    assert any(
        {
            match["query_file"],
            match["matched_file"],
        } == {"student_a.pdf", "student_b.docx"}
        for match in matches
    )

    assert not any(
        match["query_file"] == match["matched_file"]
        for match in matches
    )

    assert not any(
        "student_c.pdf" in {
            match["query_file"],
            match["matched_file"],
        }
        and "student_a.pdf" in {
            match["query_file"],
            match["matched_file"],
        }
        for match in matches
    )

    print("\nPeer matcher tests passed!")


if __name__ == "__main__":
    main()
