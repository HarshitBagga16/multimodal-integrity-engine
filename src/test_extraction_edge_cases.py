
from pathlib import Path
from tempfile import TemporaryDirectory

from src.extractors.document_extractor import extract_document


def main():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # A corrupt DOCX should raise an error that the pipeline can catch.
        corrupt_docx = temp_path / "corrupt.docx"
        corrupt_docx.write_text("This is not a real DOCX file.")

        try:
            extract_document(corrupt_docx)
        except Exception as exc:
            print("Corrupt DOCX detected:", type(exc).__name__)
        else:
            raise AssertionError("Corrupt DOCX was not detected")

        # Unsupported extensions should be rejected explicitly.
        unsupported = temp_path / "notes.txt"
        unsupported.write_text("Some text")

        try:
            extract_document(unsupported)
        except ValueError:
            print("Unsupported format rejected correctly")
        else:
            raise AssertionError("Unsupported format was not rejected")

    print("\nExtraction edge-case tests passed!")


if __name__ == "__main__":
    main()
