from pathlib import Path

from extractors.document_extractor import extract_document


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_DIR = PROJECT_ROOT / "sample_submissions"


def main():
    for filename in ["test.pdf", "test.docx"]:
        file_path = SAMPLE_DIR / filename

        if not file_path.exists():
            print(f"[SKIP] Create this sample file first: {filename}")
            continue

        results = extract_document(file_path)

        print(f"\n--- {filename} ---")
        print(f"Extracted sections: {len(results)}")

        for item in results[:3]:
            print(item)


if __name__ == "__main__":
    main()
