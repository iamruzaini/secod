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

REQUIRED_EXECUTABLE_FIXTURES = {
    "secod-abuse-limits": (
        "fixture_app.py", "test_abuse_limits.py", "run_fixtures.py", "README.md"
    ),
    "secod-crypto-data-protection": (
        "fixture_app.py", "test_secure_patterns.py", "run_fixtures.py", "README.md"
    ),
    "secod-failure-safety": (
        "fixture_app.py", "test_failure_safety.py", "run_fixtures.py", "README.md"
    ),
    "secod-observability-response": (
        "fixture_app.py", "test_observability_response.py", "run_fixtures.py", "README.md"
    ),
    "secod-packages-delivery": (
        "fixture_app.py", "test_packages_delivery.py", "run_fixtures.py", "README.md"
    ),
    "secod-payments-billing": (
        "fixture_app.py", "test_payments_billing.py", "run_fixtures.py", "README.md"
    ),
    "secod-secrets-config": (
        "fixture_app.py", "test_secrets_config.py", "run_fixtures.py", "README.md"
    ),
    "secod-identity-access": (
        "fixture_app.py", "test_secure_patterns.py", "run_fixtures.py", "README.md"
    ),
    "secod-inputs-apis": (
        "fixture_app.py", "test_secure_patterns.py", "run_fixtures.py", "README.md"
    ),
    "secod-data-files": (
        "fixture_app.py", "test_secure_patterns.py", "run_fixtures.py", "README.md"
    ),
    "secod-nextjs": (
        "fixture_app.py", "test_secure_patterns.py", "run_fixtures.py", "README.md"
    ),
    "secod-firebase": (
        "fixture_app.py", "test_secure_patterns.py", "run_fixtures.py", "README.md"
    ),
    "secod-supabase": (
        "fixture_app.py", "test_secure_patterns.py", "run_fixtures.py", "README.md"
    ),
    "secod-openai": (
        "fixture_app.py", "test_secure_patterns.py", "run_fixtures.py", "README.md"
    ),
    "secod-critical-behaviors": ("run_fixtures.py", "README.md"),
}


def main() -> int:
    tests_root = Path(__file__).resolve().parents[1] / "tests"
    missing = [name for name in REQUIRED_DIRECTORIES if not (tests_root / name).is_dir()]
    if missing:
        print("Missing test directories: " + ", ".join(missing))
        return 1

    fixtures_root = tests_root / "insecure-fixtures"
    missing_fixtures = [
        f"{fixture}/{filename}"
        for fixture, filenames in REQUIRED_EXECUTABLE_FIXTURES.items()
        for filename in filenames
        if not (fixtures_root / fixture / filename).is_file()
    ]
    if missing_fixtures:
        print("Missing required executable fixtures: " + ", ".join(missing_fixtures))
        return 1

    executable = sorted(
        path.name for path in fixtures_root.iterdir() if (path / "run_fixtures.py").is_file()
    )
    print(
        "SECOD test layout is present. Executable fixture suites: "
        + str(len(executable))
        + "; skill-owned documentation-only plans remain allowed for uncovered skills."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
