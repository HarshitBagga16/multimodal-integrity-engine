
import argparse
import logging
from pathlib import Path

from src.pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Multimodal Submission Integrity Checker"
    )

    parser.add_argument(
        "--input_dir",
        type=Path,
        required=True,
        help="Directory containing PDF and DOCX submissions",
    )

    parser.add_argument(
        "--output_dir",
        type=Path,
        required=True,
        help="Directory where reports will be saved",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    try:
        summary = run_pipeline(args.input_dir, args.output_dir)
    except (ValueError, NotADirectoryError) as exc:
        parser.error(str(exc))

    print("\nIntegrity check completed.")
    print(f"Input files: {summary['total_input_files']}")
    print(f"Chunks: {summary['total_chunks']}")
    print(f"Directional matches: {summary['total_matches']}")
    print(f"Reports saved to: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
