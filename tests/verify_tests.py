#!/usr/bin/env python3
"""
Verify test structure without running tests.
"""

import os
import sys
from pathlib import Path


def verify_test_structure():
    """Verify that all test files exist and are structured correctly."""
    project_root = Path(__file__).parent.parent
    tests_dir = project_root / "tests"

    print(f"Project root: {project_root}")
    print(f"Tests directory: {tests_dir}")
    print()

    # Expected test files
    expected_files = [
        "tests/__init__.py",
        "tests/conftest.py",
        "tests/test_skills.py",
        "tests/test_progression.py",
        "tests/test_prerequisites.py",
        "tests/test_synergies.py",
        "tests/test_archetypes.py",
        "tests/test_integration.py",
        "tests/run_tests.py",
        "tests/README.md"
    ]

    print("Checking for test files...")
    all_exist = True
    for file_path in expected_files:
        full_path = project_root / file_path
        exists = full_path.exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {file_path}")
        if exists:
            # Check file size
            size = full_path.stat().st_size
            print(f"      Size: {size} bytes")
        if not exists:
            all_exist = False

    print()

    # Count test functions
    print("Counting test functions...")
    test_files = [
        "tests/test_skills.py",
        "tests/test_progression.py",
        "tests/test_prerequisites.py",
        "tests/test_synergies.py",
        "tests/test_archetypes.py",
        "tests/test_integration.py"
    ]

    total_tests = 0
    for test_file in test_files:
        full_path = project_root / test_file
        if full_path.exists():
            with open(full_path, 'r') as f:
                content = f.read()
                test_count = content.count("def test_")
                total_tests += test_count
                print(f"  {test_file}: {test_count} tests")

    print()
    print(f"Total test functions: {total_tests}")
    print()

    # Check fixtures
    print("Checking fixtures...")
    conftest_path = tests_dir / "conftest.py"
    if conftest_path.exists():
        with open(conftest_path, 'r') as f:
            content = f.read()
            fixture_count = content.count("@pytest.fixture")
            print(f"  Total fixtures: {fixture_count}")

            # List fixtures
            import re
            fixtures = re.findall(r'@pytest.fixture\s*\ndef\s+(\w+)', content)
            print("  Fixture names:")
            for fixture in fixtures:
                print(f"    - {fixture}")

    print()

    # Check configuration
    print("Checking configuration files...")
    config_files = [
        "pytest.ini",
        "requirements-test.txt",
        "setup_test_env.sh"
    ]

    for config_file in config_files:
        full_path = project_root / config_file
        exists = full_path.exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {config_file}")

    print()
    if all_exist:
        print("✓ All test files present!")
        print()
        print("To run tests:")
        print("  1. Setup environment: ./setup_test_env.sh")
        print("  2. Activate venv: source venv/bin/activate")
        print("  3. Run tests: pytest tests/ -v")
        print("  4. Run with coverage: pytest --cov=character_skill_trees --cov-report=html")
        return 0
    else:
        print("✗ Some test files are missing!")
        return 1


if __name__ == "__main__":
    sys.exit(verify_test_structure())
