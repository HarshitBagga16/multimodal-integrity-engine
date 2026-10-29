
from pathlib import Path
import logging

import whisper

logger = logging.getLogger(__name__)

_model = None


def get_whisper_model():
    global _model

    if _model is None:
        _model = whisper.load_model("base")

    return _model


def extract_video(file_path: Path) -> list[dict]:
    """Transcribe video speech and preserve segment timestamps."""
    model = get_whisper_model()

    try:
        result = model.transcribe(
            str(file_path),
            fp16=False,
            verbose=False,
        )
    except RuntimeError as exc:
        error_message = str(exc).lower()

        # Whisper/FFmpeg produces this when the video has no audio stream.
        if "does not contain any stream" in error_message:
            logger.warning("Video has no audio stream: %s", file_path.name)
            return []

        # Other failures should remain visible to the pipeline.
        raise

    extracted = []

    for segment in result.get("segments", []):
        text = segment.get("text", "").strip()

        if not text:
            continue

        extracted.append({
            "text": text,
            "source_file": file_path.name,
            "file_type": "mp4",
            "page_number": None,
            "timestamp": {
                "start": round(segment["start"], 2),
                "end": round(segment["end"], 2),
            },
        })

    if not extracted:
        logger.warning("No speech detected in video: %s", file_path.name)

    return extracted
