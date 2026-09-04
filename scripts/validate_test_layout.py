"""Read-only validation that the required SECOD test surfaces are present."""

from __future__ import annotations

from pathlib import Path
import sys


REQUIRED_DIRECTORIES = (
    "trigger-cases",
    "behavior-cases",
    "insecure-fixtures",
    "expected-results",
)


def main() -> int:
    tests_root = Path(__file__).resolve().parents[1] / "tests"
    missing = [name for name in REQUIRED_DIRECTORIES if not (tests_root / name).is_dir()]
    if missing:
        print("Missing test directories: " + ", ".join(missing))
        return 1
    print("SECOD test layout is present. Fixture coverage still requires review.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
