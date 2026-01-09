# Quick Start Guide - Running Tests

## One-Time Setup

```bash
cd /mnt/c/users/casey/character-skill-trees
./setup_test_env.sh
source venv/bin/activate
```

## Run All Tests

```bash
# Basic run
pytest

# Verbose output
pytest -v

# With coverage
pytest --cov=character_skill_trees
```

## Run Specific Tests

```bash
# By file
pytest tests/test_skills.py

# By class
pytest tests/test_skills.py::TestSkillCreation

# By function
pytest tests/test_skills.py::TestSkillCreation::test_create_basic_skill

# By pattern
pytest -k "mastery"
pytest -k "synergy"
pytest -k "prerequisite"
```

## View Coverage

```bash
# HTML report
pytest --cov=character_skill_trees --cov-report=html
open htmlcov/index.html

# Terminal with missing lines
pytest --cov=character_skill_trees --cov-report=term-missing
```

## Quick Commands

```bash
# Run tests only (no coverage)
pytest tests/ -v --no-cov

# Stop on first failure
pytest -x

# Run with detailed output
pytest -vv -s

# Run specific test files
pytest tests/test_skills.py tests/test_progression.py

# Count tests
pytest --collect-only
```

## Test Stats

- Total tests: 163
- Total fixtures: 16
- Test files: 6
- Coverage target: 80%+

## Troubleshooting

**Import errors?**
```bash
pip install -e .
```

**Pytest not found?**
```bash
pip install pytest pytest-cov
```

**Tests running slowly?**
```bash
pytest -k "specific_test"  # Run specific tests only
```

## Documentation

- Full test documentation: `tests/README.md`
- Test summary: `tests/TEST_SUMMARY.md`
- Verify tests: `python tests/verify_tests.py`
