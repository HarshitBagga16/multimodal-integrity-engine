# To test the environment, run this script from the project root. It will check for the presence of required directories and print the Python version.

import sys
from pathlib import Path


def main():
    # Find the project root, regardless of the terminal's location.
    project_root = Path(__file__).resolve().parent.parent

    required_dirs = [
        "src",
        "src/extractors",
        "src/processing",
        "src/matching",
        "src/reporting",
        "sample_submissions",
        "tests",
        "output",
    ]

    print(f"Python version: {sys.version.split()[0]}")

    for directory in required_dirs:
        path = project_root / directory

        assert path.is_dir(), f"Missing directory: {directory}"

        print(f"[OK] {directory}")

    print("\nEnvironment smoke test passed!")


if __name__ == "__main__":
    main()
