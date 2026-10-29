
from src.processing.text_cleaner import clean_text
from src.processing.chunker import chunk_record


def main():
    messy_text = "  AI   can\nanalyze\t documents.  "

    print("Cleaned text:")
    print(clean_text(messy_text))

    record = {
        "text": " ".join(f"word{i}" for i in range(600)),
        "source_file": "demo.pdf",
        "file_type": "pdf",
        "page_number": 1,
        "timestamp": None,
    }

    chunks = chunk_record(record, chunk_size=250, overlap=40)

    print(f"\nNumber of chunks: {len(chunks)}")

    for chunk in chunks:
        print(
            f"Chunk {chunk['chunk_number']}: "
            f"{chunk['word_start']}–{chunk['word_end'] - 1}, "
            f"{len(chunk['text'].split())} words"
        )

    assert len(chunks) == 3
    assert len(chunks[0]["text"].split()) == 250
    assert len(chunks[1]["text"].split()) == 250
    assert len(chunks[2]["text"].split()) == 180
    assert chunks[1]["source_file"] == "demo.pdf"

    print("\nChunking tests passed!")


if __name__ == "__main__":
    main()
