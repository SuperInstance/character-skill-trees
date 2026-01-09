#!/usr/bin/env python3
"""
Test runner script for character-skill-trees.

This script provides a convenient way to run tests with various options.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(verbose=False, coverage=False, pattern=None, marker=None, fail_fast=False):
    """
    Run tests using pytest.

    Args:
        verbose: Enable verbose output
        coverage: Generate coverage report
        pattern: Filter tests by pattern
        marker: Filter tests by marker
        fail_fast: Stop on first failure

    Returns:
        Exit code from pytest
    """
    # Build pytest command
    cmd = ["python", "-m", "pytest"]

    # Add verbose flag
    if verbose:
        cmd.append("-v")

    # Add coverage
    if coverage:
        cmd.extend([
            "--cov=character_skill_trees",
            "--cov-report=html",
            "--cov-report=term-missing"
        ])

    # Add pattern filter
    if pattern:
        cmd.extend(["-k", pattern])

    # Add marker filter
    if marker:
        cmd.extend(["-m", marker])

    # Add fail fast
    if fail_fast:
        cmd.append("-x")

    # Add test directory
    cmd.append("tests/")

    # Run pytest
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    return result.returncode


def main():
    """Main entry point for test runner."""
    parser = argparse.ArgumentParser(
        description="Run tests for character-skill-trees package"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "-c", "--coverage",
        action="store_true",
        help="Generate coverage report"
    )

    parser.add_argument(
        "-k", "--pattern",
        type=str,
        help="Filter tests by pattern"
    )

    parser.add_argument(
        "-m", "--marker",
        type=str,
        help="Filter tests by marker"
    )

    parser.add_argument(
        "-x", "--fail-fast",
        action="store_true",
        help="Stop on first failure"
    )

    parser.add_argument(
        "--no-cov",
        action="store_true",
        help="Disable coverage (even if configured in pytest.ini)"
    )

    args = parser.parse_args()

    # Change to project directory
    project_dir = Path(__file__).parent.parent
    import os
    os.chdir(project_dir)

    # Run tests
    exit_code = run_tests(
        verbose=args.verbose,
        coverage=args.coverage,
        pattern=args.pattern,
        marker=args.marker,
        fail_fast=args.fail_fast
    )

    # Print summary
    if exit_code == 0:
        print("\n✓ All tests passed!")
    else:
        print(f"\n✗ Tests failed with exit code {exit_code}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
