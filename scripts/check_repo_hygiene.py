"""Read-only repository hygiene checks for obviously committed secret files."""

from __future__ import annotations

from pathlib import Path
import sys


BLOCKED_FILENAMES = {".env", ".env.local", ".env.production", "id_rsa"}
BLOCKED_SUFFIXES = {".pem", ".p12", ".pfx"}


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    findings: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.name in BLOCKED_FILENAMES or path.suffix.lower() in BLOCKED_SUFFIXES:
            findings.append(str(path.relative_to(root)))

    if findings:
        print("Potential secret files found:")
        for finding in findings:
            print("- " + finding)
        return 1

    print("No blocked secret-file names were found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
