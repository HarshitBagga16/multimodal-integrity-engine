
from pathlib import Path
import json

import pymupdf
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "sample_submissions"
MANIFEST_PATH = DATA_DIR / "dataset_manifest.json"


SUBMISSIONS = [
    {
        "filename": "01_ml_fundamentals.pdf",
        "format": "pdf",
        "case": "original",
        "text": (
            "Machine learning enables computers to discover useful patterns "
            "from examples. A training dataset contains observations and "
            "features. The learning algorithm adjusts its parameters to "
            "minimize prediction errors. Evaluation data helps measure how "
            "well a trained model generalizes to unseen examples. "
            "Data quality, representative sampling, and appropriate metrics "
            "are essential for reliable predictions."
        ),
    },
    {
        "filename": "02_ml_fundamentals_copy.pdf",
        "format": "pdf",
        "case": "exact_copy",
        "copy_of": "01_ml_fundamentals.pdf",
        "text": (
            "Machine learning enables computers to discover useful patterns "
            "from examples. A training dataset contains observations and "
            "features. The learning algorithm adjusts its parameters to "
            "minimize prediction errors. Evaluation data helps measure how "
            "well a trained model generalizes to unseen examples. "
            "Data quality, representative sampling, and appropriate metrics "
            "are essential for reliable predictions."
        ),
    },
    {
        "filename": "03_ml_paraphrase.pdf",
        "format": "pdf",
        "case": "paraphrase",
        "related_to": "01_ml_fundamentals.pdf",
        "text": (
            "Computers can learn patterns by studying examples rather than "
            "following only manually written rules. During training, an "
            "algorithm uses observations and input features to improve its "
            "parameters and reduce mistakes. Separate evaluation examples "
            "show whether the resulting model works on data it has not seen "
            "before. Reliable outcomes depend on clean data, representative "
            "samples, and suitable evaluation measures."
        ),
    },
    {
        "filename": "04_network_security.pdf",
        "format": "pdf",
        "case": "independent",
        "text": (
            "Network security protects systems and information from "
            "unauthorized access. Firewalls inspect traffic according to "
            "defined rules, while encryption protects information during "
            "transmission. Multi-factor authentication adds another layer "
            "of identity verification. Security teams should monitor logs, "
            "apply software updates, and test recovery procedures regularly."
        ),
    },
    {
        "filename": "05_climate_research.pdf",
        "format": "pdf",
        "case": "cross_modal_reference",
        "text": (
            "Renewable energy systems convert naturally replenished "
            "resources into useful power. Solar panels use photovoltaic "
            "cells to convert sunlight into electricity. Wind turbines "
            "convert moving air into rotational energy and then electrical "
            "power. Energy storage and grid planning help balance variable "
            "generation with changing demand."
        ),
    },
    {
        "filename": "06_network_security.docx",
        "format": "docx",
        "case": "original",
        "text": (
            "Network security protects systems and information from "
            "unauthorized access. Firewalls inspect traffic according to "
            "defined rules, while encryption protects information during "
            "transmission. Multi-factor authentication adds another layer "
            "of identity verification. Security teams should monitor logs, "
            "apply software updates, and test recovery procedures regularly."
        ),
    },
    {
        "filename": "07_network_security_copy.docx",
        "format": "docx",
        "case": "exact_copy",
        "copy_of": "06_network_security.docx",
        "text": (
            "Network security protects systems and information from "
            "unauthorized access. Firewalls inspect traffic according to "
            "defined rules, while encryption protects information during "
            "transmission. Multi-factor authentication adds another layer "
            "of identity verification. Security teams should monitor logs, "
            "apply software updates, and test recovery procedures regularly."
        ),
    },
    {
        "filename": "08_ai_generated_sample.docx",
        "format": "docx",
        "case": "ai_style_heuristic_test",
        "text": (
            "In conclusion, artificial intelligence offers several important "
            "advantages. Furthermore, it can improve productivity across "
            "different industries. Moreover, responsible implementation "
            "requires careful planning and evaluation. It is important to "
            "consider both opportunities and limitations. Therefore, a "
            "balanced approach can support effective and responsible use."
        ),
    },
    {
        "filename": "09_database_design.docx",
        "format": "docx",
        "case": "independent",
        "text": (
            "Database normalization organizes relational tables to reduce "
            "unnecessary duplication. Primary keys uniquely identify rows, "
            "while foreign keys represent relationships between tables. "
            "Indexes can speed up selected queries, although they introduce "
            "storage costs and additional work during writes. Query plans "
            "help engineers understand database execution."
        ),
    },
    {
        "filename": "10_solar_energy.docx",
        "format": "docx",
        "case": "cross_modal_reference",
        "text": (
            "Renewable energy systems convert naturally replenished "
            "resources into useful power. Solar panels use photovoltaic "
            "cells to convert sunlight into electricity. Wind turbines "
            "convert moving air into rotational energy and then electrical "
            "power. Energy storage and grid planning help balance variable "
            "generation with changing demand."
        ),
    },
]


def create_pdf(path: Path, text: str) -> None:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_textbox(
        pymupdf.Rect(60, 60, 540, 740),
        text,
        fontsize=12,
    )
    doc.save(path)
    doc.close()


def create_docx(path: Path, text: str) -> None:
    doc = Document()
    doc.add_heading(path.stem.replace("_", " "), level=1)
    doc.add_paragraph(text)
    doc.save(path)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []

    for item in SUBMISSIONS:
        path = DATA_DIR / item["filename"]

        if item["format"] == "pdf":
            create_pdf(path, item["text"])
        else:
            create_docx(path, item["text"])

        manifest.append({
            "filename": item["filename"],
            "format": item["format"],
            "case": item["case"],
            "expected_copy_of": item.get("copy_of"),
            "expected_related_to": item.get("related_to"),
            "text": item["text"],
        })

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print(f"Created {len(SUBMISSIONS)} PDF/DOCX submissions.")
    print(f"Manifest saved to: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
