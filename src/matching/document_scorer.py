
from collections import defaultdict


def build_document_summary(
    chunks: list[dict],
    matches: list[dict],
) -> dict:
    """Build pairwise coverage scores and a document comparison matrix."""

    files = sorted({
        chunk["source_file"]
        for chunk in chunks
    })

    total_chunks = defaultdict(int)

    for chunk in chunks:
        total_chunks[chunk["source_file"]] += 1

    matched_chunks = defaultdict(set)

    for match in matches:
        query_file = match["query_file"]
        matched_file = match["matched_file"]
        query_chunk = match.get("query_chunk")

        if query_chunk is not None:
            matched_chunks[(query_file, matched_file)].add(query_chunk)

    pairwise = {}
    matrix = {}

    for source_file in files:
        matrix[source_file] = {}

        for target_file in files:
            if source_file == target_file:
                matrix[source_file][target_file] = None
                continue

            count = len(
                matched_chunks[(source_file, target_file)]
            )
            denominator = total_chunks[source_file]

            percentage = (
                100.0 * count / denominator
                if denominator
                else 0.0
            )

            percentage = round(percentage, 2)

            matrix[source_file][target_file] = percentage

            pairwise[f"{source_file} -> {target_file}"] = {
                "source_file": source_file,
                "target_file": target_file,
                "total_source_chunks": denominator,
                "matched_source_chunks": count,
                "matched_chunk_coverage_percent": percentage,
            }

    return {
        "files": files,
        "pairwise": pairwise,
        "comparison_matrix": matrix,
    }
