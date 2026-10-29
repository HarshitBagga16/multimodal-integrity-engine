# Multimodal Submission Integrity & Plagiarism Detection Engine

## 1. Overview

A Python CLI pipeline that analyzes PDF, DOCX, and MP4 submissions for potentially duplicated or related content.

The system extracts text from documents and video speech, splits text into overlapping chunks, generates semantic embeddings, compares submissions, and produces evidence-based reports for human review.

**Important:** similarity indicates potential overlap, not proof of plagiarism. The AI-style score is an experimental heuristic, not proof of AI authorship.

## 2. Features

- PDF text extraction with page metadata.
- DOCX text extraction.
- MP4 speech transcription using Whisper and FFmpeg.
- Graceful handling of empty or silent video files.
- Text cleaning and overlapping chunking.
- Semantic embeddings using `all-MiniLM-L6-v2`.
- Peer comparison using normalized embedding vectors and NumPy.
- Evidence containing matched passages, source files, similarity scores, and available page/timestamp metadata.
- Local reference-corpus comparison.
- Experimental, explainable writing-style heuristic.
- Per-document JSON reports and an aggregate Markdown report.
- Evaluation metrics and a confusion matrix for a synthetic dataset.

## 3. Technology Stack

- Python 3.11
- PyMuPDF
- python-docx
- OpenAI Whisper (open-source speech recognition package)
- FFmpeg
- Sentence Transformers
- NumPy
- scikit-learn for evaluation utilities where applicable
- JSON and Markdown for outputs

The current implementation uses an in-memory NumPy similarity matrix. It does not require a hosted vector database or a paid LLM API.

## 4. Project Structure

```text
multimodal-integrity-engine/
├── src/
│   ├── extractors/
│   │   ├── document_extractor.py
│   │   └── video_extractor.py
│   ├── matching/
│   │   ├── embedding_engine.py
│   │   ├── peer_matcher.py
│   │   ├── document_scorer.py
│   │   └── external_matcher.py
│   ├── processing/
│   │   ├── text_cleaner.py
│   │   ├── chunker.py
│   │   └── ai_style_estimator.py
│   ├── reporting/
│   │   └── report_writer.py
│   ├── pipeline.py
│   ├── evaluate_results.py
│   └── create_synthetic_dataset.py
├── sample_submissions/
├── tests/
├── reference_corpus.json
├── run_integrity_check.py
├── EVALUATION.md
└── README.md

## 5. File-by-File Code Overview

### Entry Point and Pipeline

| File | Responsibility |
|---|---|
| `run_integrity_check.py` | CLI entry point. Reads input/output directory arguments and starts the pipeline. |
| `src/pipeline.py` | Coordinates extraction, chunking, embeddings, peer matching, external matching, style estimation, and report generation. |

### Text Extraction

| File | Responsibility |
|---|---|
| `src/extractors/document_extractor.py` | Routes supported files to the appropriate extractor and collects extracted text with source metadata. |
| `src/extractors/video_extractor.py` | Uses Whisper to transcribe speech from MP4 files and preserves segment timestamps. Handles videos without audio. |

### Text Processing

| File | Responsibility |
|---|---|
| `src/processing/text_cleaner.py` | Normalizes extracted text, removes unwanted null characters, and collapses excess whitespace. |
| `src/processing/chunker.py` | Splits cleaned text into overlapping chunks and retains source metadata needed for matching evidence. |
| `src/processing/ai_style_estimator.py` | Calculates a heuristic writing-style score from text length, transition phrases, and sentence-length consistency. It does not prove AI authorship. |

### Matching and Similarity

| File | Responsibility |
|---|---|
| `src/matching/embedding_engine.py` | Loads `all-MiniLM-L6-v2`, converts passages into normalized vectors, and calculates cosine similarity matrices. |
| `src/matching/peer_matcher.py` | Compares chunks across submissions, excludes self-matches, applies a similarity threshold, and returns matching passages with source metadata. |
| `src/matching/document_scorer.py` | Aggregates chunk-level matches into document-level directional coverage and a pairwise comparison matrix. |
| `src/matching/external_matcher.py` | Compares submission chunks against the local reference corpus and returns matching passages with similarity scores. |

### Reporting and Evaluation

| File | Responsibility |
|---|---|
| `src/reporting/report_writer.py` | Writes JSON reports and a human-readable Markdown report containing pairwise coverage and matching evidence. |
| `src/evaluate_results.py` | Compares detected pairs against the synthetic ground truth and calculates precision, recall, F1 score, accuracy, and confusion-matrix counts. |
| `src/create_synthetic_dataset.py` | Generates synthetic PDF and DOCX submissions for testing the detection pipeline. Check the script for the exact files and formats it generates. |

### Configuration and Data

| File or directory | Responsibility |
|---|---|
| `reference_corpus.json` | Contains the local reference passages used to demonstrate external-reference matching. |
| `sample_submissions/` | Contains the synthetic PDF, DOCX, and MP4 test submissions. |
| `tests/fixtures/` | Stores test files kept separate from the main submission dataset. |
| `output/` | Stores generated JSON reports, the aggregate Markdown report, and evaluation metrics. |
| `requirements.txt` | Lists Python package dependencies required to install the project. |
| `EVALUATION.md` | Documents the evaluation methodology, results, failure cases, and limitations. |
| `README.md` | Explains setup, usage, architecture, methodology, and proposed scaling improvements. |



## 6. Setup

### Prerequisites
- Python 3.11
- FFmpeg installed and available on PATH
- Internet access for the initial model downloads

### Install dependencies

Activate your virtual environment and install the project dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Verify FFmpeg:

```powershell
ffmpeg -version
```

## 7. Run the Pipeline

Place PDF, DOCX, and MP4 files in `sample_submissions/`.

Run the integrity checker:

```powershell
python run_integrity_check.py --input_dir ./sample_submissions --output_dir ./output
```

Generated outputs include:
- `summary.json`: aggregate results and file statuses.
- `integrity_report.md`: pairwise coverage and matching evidence.
- Individual JSON reports for submissions.
- `evaluation_metrics.json`: metrics generated by the evaluation script.

Run evaluation:

```powershell
python src/evaluate_results.py
```

## 8. Methodology

### Extraction
PDF and DOCX extractors collect text and available metadata. Whisper transcribes speech from MP4 files and records timestamps. Empty or silent videos are handled without crashing.

### Cleaning and chunking
Text is normalized and divided into overlapping chunks so that relevant passages can be compared independently.

### Embeddings and peer matching
The `all-MiniLM-L6-v2` model generates normalized embeddings. NumPy calculates cosine similarity using dot products. Candidate matches above the configured threshold are retained.

### Matched-chunk coverage
The pairwise matrix represents directional matched-chunk coverage, not raw cosine similarity or a definitive percentage of plagiarism.

### External references
Submissions are compared against a small local synthetic reference corpus. This demonstrates reference matching; it is not a live internet search.

### AI-writing style estimate
A heuristic evaluates transition phrases, sentence-length consistency, and text length. Its score is not a calibrated probability and cannot prove AI authorship.

## 9. Evaluation

See `EVALUATION.md` for the synthetic dataset, precision, recall, F1 score, confusion matrix, and limitations.

The test dataset includes exact copies, paraphrased content, cross-format matches, speech matching document content, and a silent video.

Results on a small synthetic dataset do not establish real-world accuracy. The evaluation metrics must be interpreted in the context of the selected test cases and detection rule.

## 10. Limitations

- Video processing analyzes extracted speech, not all visual content.
- Scanned PDFs may require OCR, which is not currently implemented.
- The local reference corpus is small and synthetic.
- Semantic similarity can miss paraphrases or flag generic content.
- Chunk accounting and directional coverage require further validation.
- The AI-writing heuristic cannot reliably establish AI authorship.
- The current in-memory implementation is intended for a small assessment dataset.

## 11. Scaling to 10,000 Submissions

The current implementation is suitable for a small assessment dataset. A production system processing 10,000 submissions would require a more scalable architecture.

### Processing architecture
Use asynchronous workers and a job queue to process files independently. Apply retries, timeouts, file-size limits, and failure tracking.

### Embedding throughput
Batch text chunks before generating embeddings. Use CPU workers for moderate throughput and benchmark GPU acceleration for high-volume embedding and transcription workloads.

### Vector search
The current approach computes similarities in memory. For larger collections, consider FAISS with an HNSW approximate nearest-neighbour index. Compare its retrieval quality against exact search before deployment.

### Storage
Store original submissions in object storage, metadata and job status in a database, and vectors in a suitable vector index. Apply access controls and retention policies.

### Cost and latency
Video transcription, embedding generation, repeated processing, and large similarity comparisons are likely bottlenecks. Cache embeddings by content hash, batch workloads, and avoid processing unchanged files repeatedly.

### Monitoring
Track processing failures, throughput, queue depth, latency, memory usage, precision, and recall. Re-evaluate the detection threshold against labelled data as the system evolves.

These are proposed scaling improvements; they are not implemented in the current CLI prototype.

## 12. Responsible Use

This tool supports human review and does not make final misconduct decisions. Reviewers should inspect the matched passages and source metadata before drawing conclusions. Neither semantic similarity nor the AI-writing style score independently proves plagiarism or AI authorship.