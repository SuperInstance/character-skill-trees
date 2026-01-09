# Test Suite for Character Skill Trees

This directory contains a comprehensive test suite for the `character-skill-trees` package.

## Test Structure

### Test Files

1. **test_skills.py** - Tests for individual skill functionality
   - Skill creation and initialization
   - Skill categories (8 categories)
   - Experience gaining and progression
   - Usage tracking
   - Specializations
   - Mastery level properties
   - Serialization
   - Validation

2. **test_progression.py** - Tests for progression system
   - Mastery level determination (6 levels)
   - Skill milestones
   - Experience calculations
   - Level progression
   - Integration testing

3. **test_prerequisites.py** - Tests for prerequisite system
   - Individual prerequisites
   - Optional vs required prerequisites
   - Prerequisite checking
   - Progress calculation
   - Prerequisite chains
   - Cycle detection
   - Integration with skills

4. **test_synergies.py** - Tests for synergy system
   - Individual synergies
   - Activation conditions
   - Bonus calculations
   - Synergy calculator utilities
   - Cross-skill transfers
   - Network strength

5. **test_archetypes.py** - Tests for predefined archetypes
   - Innovator tree
   - Educator tree
   - Empath tree
   - Engineer tree
   - Archetype characteristics
   - Integration tests

6. **test_integration.py** - Complete workflow tests
   - Skill tree workflows
   - Specialization workflows
   - Synergy activation
   - Archetype progression
   - Serialization
   - Error handling
   - Statistics

## Fixtures

The `conftest.py` file provides comprehensive fixtures:

- **sample_skill** - Basic skill for testing
- **novice_skill** - Level 5 skill
- **expert_skill** - Level 70 skill
- **master_skill** - Level 90 skill
- **skill_with_specializations** - Skill with 3 specializations
- **skill_with_prerequisites** - Skill with prerequisites
- **skill_with_synergies** - Skill with synergies
- **skill_with_milestones** - Skill with milestones
- **skill_tree** - Basic skill tree structure
- **skill_tree_with_synergies** - Tree with synergies
- **prerequisite_chain** - Chain of prerequisites
- **synergy_list** - List of synergies
- **skill_levels** - Dictionary of skill levels
- **mastery_levels** - All 6 mastery levels
- **milestone_list** - List of milestones

## Running Tests

### Run all tests:

```bash
# Using pytest directly
pytest

# Using the test runner
python tests/run_tests.py

# With verbose output
pytest -v

# With coverage
pytest --cov=character_skill_trees --cov-report=html
```

### Run specific test files:

```bash
pytest tests/test_skills.py
pytest tests/test_progression.py
pytest tests/test_prerequisites.py
pytest tests/test_synergies.py
pytest tests/test_archetypes.py
pytest tests/test_integration.py
```

### Run specific test classes:

```bash
pytest tests/test_skills.py::TestSkillCreation
pytest tests/test_progression.py::TestMasteryLevel
```

### Run specific test functions:

```bash
pytest tests/test_skills.py::TestSkillCreation::test_create_basic_skill
```

### Run tests matching a pattern:

```bash
pytest -k "test_mastery"
pytest -k "synergy"
pytest -k "prerequisite"
```

### Run with markers (when implemented):

```bash
pytest -m unit
pytest -m integration
pytest -m "not slow"
```

## Coverage

The test suite targets **80%+ code coverage**.

### Generate coverage report:

```bash
# Terminal report with missing lines
pytest --cov=character_skill_trees --cov-report=term-missing

# HTML report
pytest --cov=character_skill_trees --cov-report=html
open htmlcov/index.html

# XML report (for CI/CD)
pytest --cov=character_skill_trees --cov-report=xml
```

### View coverage by module:

```bash
pytest --cov=character_skill_trees/core --cov-report=term-missing
pytest --cov=character_skill_trees/progression --cov-report=term-missing
pytest --cov=character_skill_trees/prerequisites --cov-report=term-missing
pytest --cov=character_skill_trees/transfer --cov-report=term-missing
```

## Test Categories

### Unit Tests
- Test individual components in isolation
- Fast execution
- Mock external dependencies

### Integration Tests
- Test component interactions
- Full workflow testing
- End-to-end scenarios

## Coverage Goals

By module:

- `core/skill.py` - 90%+ coverage
- `core/skill_tree.py` - 85%+ coverage
- `progression/mastery.py` - 95%+ coverage
- `progression/experience.py` - 90%+ coverage
- `prerequisites/requirements.py` - 90%+ coverage
- `transfer/synergies.py` - 90%+ coverage
- `archetypes.py` - 85%+ coverage
- `manager.py` - 80%+ coverage

Overall target: **85%+ coverage**

## Test Features Covered

### Skill System
✓ 8 skill categories
✓ 6 mastery levels (Novice to Grandmaster)
✓ Experience calculations
✓ Learning rates
✓ Difficulty modifiers
✓ Usage tracking
✓ Specializations
✓ Skill validation

### Progression System
✓ Level progression
✓ Experience scaling
✓ Milestone tracking
✓ Mastery transitions
✓ Time-based calculations

### Prerequisites
✓ Required prerequisites
✓ Optional prerequisites
✓ Prerequisite chains
✓ Progress tracking
✓ Cycle detection
✓ Validation

### Synergies
✓ Cross-skill bonuses
✓ Activation conditions
✓ Bonus calculations
✓ Network strength
✓ Recommendations

### Archetypes
✓ 4 predefined trees
✓ Tree characteristics
✓ Skill relationships
✓ Progression paths
✓ Difficulty modifiers

### Integration
✓ Full workflows
✓ Serialization
✓ Error handling
✓ Statistics
✓ Multi-component scenarios

## Continuous Integration

The tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements-test.txt
    pytest --cov=character_skill_trees --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Best Practices

1. **Run tests before committing**
   ```bash
   pytest -x -v
   ```

2. **Check coverage regularly**
   ```bash
   pytest --cov=character_skill_trees --cov-report=term-missing
   ```

3. **Add tests for new features**
   - Aim for 80%+ coverage on new code
   - Test both success and failure cases
   - Include edge cases

4. **Use fixtures for common setup**
   - Fixtures are defined in `conftest.py`
   - Reuse existing fixtures when possible

5. **Keep tests independent**
   - Each test should be able to run alone
   - Don't rely on test execution order

## Troubleshooting

### Tests fail with import errors:
```bash
# Install the package in development mode
pip install -e .
```

### Coverage not reporting:
```bash
# Install pytest-cov
pip install pytest-cov
```

### Tests running slowly:
```bash
# Run specific tests only
pytest tests/test_skills.py -k "test_create"
```

## Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Check coverage is maintained
4. Update this README if needed

## Test Statistics

Total test files: 6
Total test cases: 150+
Fixtures: 20+
Coverage target: 80%+
