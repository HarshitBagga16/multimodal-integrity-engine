
from src.matching.embedding_engine import EmbeddingEngine


def compare_submissions(
    chunks: list[dict],
    engine: EmbeddingEngine,
    threshold: float = 0.70,
) -> list[dict]:
    """
    Find similar chunks across different files.

    The threshold is a configurable similarity score,
    not a probability of plagiarism.
    """
    if not chunks:
        return []

    texts = [chunk["text"] for chunk in chunks]
    embeddings = engine.encode(texts)
    similarity_matrix = engine.similarity_matrix(embeddings)

    matches = []

    for i, query_chunk in enumerate(chunks):
        best_by_source = {}

        for j, candidate_chunk in enumerate(chunks):
            # Don't compare a chunk against itself.
            if i == j:
                continue

            # Ignore matches within the same submission.
            if (
                query_chunk["source_file"]
                == candidate_chunk["source_file"]
            ):
                continue

            score = float(similarity_matrix[i, j])

            if score < threshold:
                continue

            source_file = candidate_chunk["source_file"]

            # Retain the strongest matching passage per source file.
            if (
                source_file not in best_by_source
                or score > best_by_source[source_file]["similarity"]
            ):
                best_by_source[source_file] = {
                    "query_file": query_chunk["source_file"],
                    "matched_file": source_file,
                    "query_text": query_chunk["text"],
                    "matched_text": candidate_chunk["text"],
                    "query_page": query_chunk.get("page_number"),
                    "matched_page": candidate_chunk.get("page_number"),
                    "query_timestamp": query_chunk.get("timestamp"),
                    "matched_timestamp": candidate_chunk.get("timestamp"),
                    "query_chunk": query_chunk.get("chunk_number"),
                    "matched_chunk": candidate_chunk.get("chunk_number"),
                    "similarity": score,
                }

        matches.extend(best_by_source.values())

    return matches
