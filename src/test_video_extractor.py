
from pathlib import Path

from src.extractors.video_extractor import extract_video


def main():
    video_path = Path("sample_submissions/test.mp4")

    if not video_path.exists():
        print(
            "Add a short speech-containing MP4 at "
            "sample_submissions/test.mp4 first."
        )
        return

    segments = extract_video(video_path)

    print("Transcript segments:", len(segments))

    for segment in segments:
        print(segment)

    if segments:
        assert all(
            isinstance(segment["timestamp"], dict)
            for segment in segments
        )
        print("\nVideo extraction test passed!")
    else:
        print(
            "\nNo speech was transcribed. Check whether the video "
            "contains audible speech."
        )


if __name__ == "__main__":
    main()
