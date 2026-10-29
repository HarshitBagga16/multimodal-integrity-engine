from src.processing.text_cleaner import clean_text
from collections import defaultdict


def chunk_record(
    record: dict,
    chunk_size: int = 250,
    overlap: int = 40,
) -> list[dict]:
    """Split one extracted record into overlapping word-based chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    text = clean_text(record["text"])

    if not text:
        return []

    words = text.split()
    chunks = []
    start = 0
    chunk_number = 1

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_text = " ".join(words[start:end])

        chunks.append({
            **record,
            "text": chunk_text,
            "chunk_number": chunk_number,
            "word_start": start,
            "word_end": end,
        })

        if end == len(words):
            break

        start = end - overlap
        chunk_number += 1

    return chunks


def chunk_records(records: list[dict]) -> list[dict]:
    """Chunk records and assign unique chunk numbers per document."""

    all_chunks = []
    chunk_counters = defaultdict(int)

    for record in records:
        chunks = chunk_record(record)

        for chunk in chunks:
            filename = chunk["source_file"]
            chunk_counters[filename] += 1

            # Ensure chunk numbers are unique within each document.
            chunk["chunk_number"] = chunk_counters[filename]

            all_chunks.append(chunk)

    return all_chunks