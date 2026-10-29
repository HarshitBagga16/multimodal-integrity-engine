import json
from pathlib import Path

from src.matching.embedding_engine import EmbeddingEngine

ROOT = Path(__file__).resolve().parents[2]
REFERENCE_PATH = ROOT / "reference_corpus.json"


def compare_external_references(
    chunks: list[dict],
    engine: EmbeddingEngine,
    threshold: float = 0.70,
) -> list[dict]:
    """Compare submission chunks with a small local reference corpus."""
    if not REFERENCE_PATH.exists():
        return []

    references = json.loads(
        REFERENCE_PATH.read_text(encoding="utf-8")
    )

    if not chunks or not references:
        return []

    query_texts = [chunk["text"] for chunk in chunks]
    reference_texts = [item["text"] for item in references]

    query_vectors = engine.encode(query_texts)
    reference_vectors = engine.encode(reference_texts)

    # Both embedding sets are normalized, so dot product gives cosine similarity.
    similarities = query_vectors @ reference_vectors.T
    results = []

    for index, chunk in enumerate(chunks):
        best_index = int(similarities[index].argmax())
        score = float(similarities[index, best_index])

        if score < threshold:
            continue

        reference = references[best_index]

        results.append({
            "query_file": chunk["source_file"],
            "query_text": chunk["text"],
            "query_page": chunk.get("page_number"),
            "query_timestamp": chunk.get("timestamp"),
            "reference_id": reference["id"],
            "reference_title": reference["title"],
            "reference_text": reference["text"],
            "reference_source": reference.get("source", "local"),
            "similarity": round(score, 4),
        })

    return results
