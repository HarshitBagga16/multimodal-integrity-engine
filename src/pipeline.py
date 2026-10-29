
import logging
from pathlib import Path

from src.extractors.document_extractor import extract_document
from src.processing.chunker import chunk_records
from src.matching.embedding_engine import EmbeddingEngine
from src.matching.peer_matcher import compare_submissions
from src.matching.document_scorer import build_document_summary
from src.reporting.report_writer import (
    write_json_report,
    write_markdown_report,
)
from src.matching.external_matcher import compare_external_references
from src.processing.ai_style_estimator import estimate_ai_style


logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".mp4"}


def run_pipeline(input_dir: Path, output_dir: Path) -> dict:
    """Process submissions and generate integrity reports."""
    input_dir = input_dir.resolve()
    output_dir = output_dir.resolve()

    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory not found: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not files:
        raise ValueError(f"No supported PDF or DOCX files found in {input_dir}")

    records = []
    file_status = {}

    for file_path in files:
        try:
            extracted = extract_document(file_path)

            if not extracted:
                file_status[file_path.name] = {
                    "status": "empty",
                    "error": None,
                }
                continue

            records.extend(extracted)
            file_status[file_path.name] = {
                "status": "processed",
                "error": None,
            }

        except Exception as exc:
            logger.exception("Could not extract %s", file_path.name)
            file_status[file_path.name] = {
                "status": "error",
                "error": str(exc),
            }

    chunks = chunk_records(records)

    if chunks:
        engine = EmbeddingEngine()
        matches = compare_submissions(chunks, engine)
        external_matches = compare_external_references(chunks, engine)
    else:
        matches = []
        external_matches = []

    summary = build_document_summary(chunks, matches)

    summary["file_status"] = file_status
    summary["external_matches"] = external_matches

# Estimate writing style separately for each submission.
    style_estimates = {}

    for filename in files:
        document_text = " ".join(
            chunk["text"]
            for chunk in chunks
            if chunk["source_file"] == filename.name
        )
        style_estimates[filename.name] = estimate_ai_style(document_text)

    summary["ai_style_estimates"] = style_estimates

    summary["total_input_files"] = len(files)
    summary["total_chunks"] = len(chunks)
    summary["total_matches"] = len(matches)

    # Write one JSON report for each input file.
    for file_path in files:
        filename = file_path.name

        file_matches = [
            match
            for match in matches
            if match["query_file"] == filename
        ]

        report = {
            "filename": filename,
            "status": file_status[filename]["status"],
            "error": file_status[filename]["error"],
            "total_chunks": sum(
                chunk["source_file"] == filename for chunk in chunks
            ),
            "matches": file_matches,
            "external_matches": [
                match
                for match in external_matches
                if match["query_file"] == filename
            ],
            "ai_style_estimate": style_estimates[filename],
        }

        safe_stem = file_path.stem.replace("/", "_").replace("\\", "_")
        write_json_report(
            report,
            output_dir / f"{safe_stem}.json",
        )

    write_json_report(summary, output_dir / "summary.json")

    write_markdown_report(
        summary,
        matches,
        output_dir / "integrity_report.md",
    )

    logger.info(
        "Processed %d input files and %d chunks; found %d directional matches",
        len(files),
        len(chunks),
        len(matches),
    )

    return summary
