"""
Tests for prerequisite system and requirement checking.
"""

import pytest
from character_skill_trees.prerequisites.requirements import (
    SkillPrerequisite,
    PrerequisiteChecker
)


class TestSkillPrerequisite:
    """Test individual prerequisite functionality."""

    def test_create_prerequisite(self):
        """Test creating a prerequisite."""
        prereq = SkillPrerequisite("Test Skill", 20.0)

        assert prereq.skill_name == "Test Skill"
        assert prereq.required_level == 20.0
        assert prereq.optional is False

    def test_create_optional_prerequisite(self):
        """Test creating an optional prerequisite."""
        prereq = SkillPrerequisite("Optional Skill", 10.0, optional=True)

        assert prereq.optional is True

    def test_prerequisite_is_met(self):
        """Test checking if prerequisite is met."""
        prereq = SkillPrerequisite("Skill A", 20.0)
        skill_levels = {"Skill A": 25.0}

        assert prereq.is_met(skill_levels) is True

    def test_prerequisite_not_met(self):
        """Test when prerequisite is not met."""
        prereq = SkillPrerequisite("Skill A", 20.0)
        skill_levels = {"Skill A": 15.0}

        assert prereq.is_met(skill_levels) is False

    def test_prerequisite_missing_skill(self):
        """Test when required skill is missing."""
        prereq = SkillPrerequisite("Skill A", 20.0)
        skill_levels = {}  # Skill not present

        assert prereq.is_met(skill_levels) is False

    def test_optional_prerequisite_always_met(self):
        """Test that optional prerequisites are always met."""
        prereq = SkillPrerequisite("Skill A", 100.0, optional=True)
        skill_levels = {}  # Even when missing

        assert prereq.is_met(skill_levels) is True

    def test_prerequisite_progress_complete(self):
        """Test progress when prerequisite is complete."""
        prereq = SkillPrerequisite("Skill A", 20.0)
        skill_levels = {"Skill A": 25.0}

        assert prereq.get_progress(skill_levels) == 100.0

    def test_prerequisite_progress_partial(self):
        """Test partial progress toward prerequisite."""
        prereq = SkillPrerequisite("Skill A", 20.0)
        skill_levels = {"Skill A": 10.0}

        assert prereq.get_progress(skill_levels) == 50.0

    def test_prerequisite_progress_zero(self):
        """Test zero progress toward prerequisite."""
        prereq = SkillPrerequisite("Skill A", 20.0)
        skill_levels = {"Skill A": 0.0}

        assert prereq.get_progress(skill_levels) == 0.0

    def test_optional_prerequisite_progress(self):
        """Test that optional prerequisites show 100% progress."""
        prereq = SkillPrerequisite("Skill A", 100.0, optional=True)
        skill_levels = {}

        assert prereq.get_progress(skill_levels) == 100.0

    def test_prerequisite_to_dict(self):
        """Test prerequisite serialization."""
        prereq = SkillPrerequisite("Test Skill", 15.0, optional=False)

        prereq_dict = prereq.to_dict()

        assert prereq_dict['skill_name'] == "Test Skill"
        assert prereq_dict['required_level'] == 15.0
        assert prereq_dict['optional'] is False


class TestPrerequisiteChecker:
    """Test prerequisite checking utilities."""

    def test_check_all_prerequisites_met(self):
        """Test checking when all prerequisites are met."""
        prerequisites = [
            SkillPrerequisite("Skill A", 10.0),
            SkillPrerequisite("Skill B", 15.0)
        ]
        skill_levels = {
            "Skill A": 15.0,
            "Skill B": 20.0
        }

        all_met, missing = PrerequisiteChecker.check_prerequisites(
            prerequisites, skill_levels
        )

        assert all_met is True
        assert len(missing) == 0

    def test_check_prerequisites_some_missing(self):
        """Test checking when some prerequisites are missing."""
        prerequisites = [
            SkillPrerequisite("Skill A", 10.0),
            SkillPrerequisite("Skill B", 15.0),
            SkillPrerequisite("Skill C", 20.0)
        ]
        skill_levels = {
            "Skill A": 15.0,
            "Skill B": 10.0  # Below required 15
            # Skill C missing
        }

        all_met, missing = PrerequisiteChecker.check_prerequisites(
            prerequisites, skill_levels
        )

        assert all_met is False
        assert len(missing) == 2
        assert "Skill B (need level 15.0)" in missing
        assert "Skill C (need level 20.0)" in missing

    def test_check_prerequisites_all_optional(self):
        """Test checking when all prerequisites are optional."""
        prerequisites = [
            SkillPrerequisite("Skill A", 10.0, optional=True),
            SkillPrerequisite("Skill B", 15.0, optional=True)
        ]
        skill_levels = {}  # None present

        all_met, missing = PrerequisiteChecker.check_prerequisites(
            prerequisites, skill_levels
        )

        assert all_met is True
        assert len(missing) == 0

    def test_get_overall_progress_empty(self):
        """Test overall progress with no prerequisites."""
        progress = PrerequisiteChecker.get_overall_progress([], {})

        assert progress == 100.0

    def test_get_overall_partial_progress(self):
        """Test overall progress with partial completion."""
        prerequisites = [
            SkillPrerequisite("Skill A", 10.0),
            SkillPrerequisite("Skill B", 20.0)
        ]
        skill_levels = {
            "Skill A": 10.0,  # 100%
            "Skill B": 10.0   # 50%
        }

        progress = PrerequisiteChecker.get_overall_progress(
            prerequisites, skill_levels
        )

        assert progress == 75.0  # (100 + 50) / 2

    def test_get_prerequisite_chain_simple(self, prerequisite_chain):
        """Test getting simple prerequisite chain."""
        chain = PrerequisiteChecker.get_prerequisite_chain(
            "Skill B", prerequisite_chain
        )

        assert "Skill A" in chain

    def test_get_prerequisite_chain_complex(self, prerequisite_chain):
        """Test getting complex prerequisite chain."""
        chain = PrerequisiteChecker.get_prerequisite_chain(
            "Skill D", prerequisite_chain
        )

        # Should include all prerequisites in order
        assert "Skill A" in chain
        assert "Skill B" in chain
        assert "Skill C" in chain

    def test_get_prerequisite_chain_no_prereqs(self, prerequisite_chain):
        """Test chain for skill with no prerequisites."""
        chain = PrerequisiteChecker.get_prerequisite_chain(
            "Skill A", prerequisite_chain
        )

        assert len(chain) == 0

    def test_validate_tree_no_cycles(self, prerequisite_chain):
        """Test validating a tree without cycles."""
        result = PrerequisiteChecker.validate_prerequisite_tree(prerequisite_chain)

        assert result['valid'] is True
        assert result['has_cycles'] is False
        assert len(result['cycles']) == 0

    def test_validate_tree_with_cycles(self):
        """Test detecting circular dependencies."""
        tree_with_cycle = {
            "Skill A": [SkillPrerequisite("Skill B", 10.0)],
            "Skill B": [SkillPrerequisite("Skill C", 10.0)],
            "Skill C": [SkillPrerequisite("Skill A", 10.0)]  # Creates cycle
        }

        result = PrerequisiteChecker.validate_prerequisite_tree(tree_with_cycle)

        assert result['valid'] is False
        assert result['has_cycles'] is True
        assert len(result['cycles']) > 0

    def test_validate_tree_self_reference(self):
        """Test detecting self-referencing prerequisites."""
        self_referencing = {
            "Skill A": [SkillPrerequisite("Skill A", 10.0)]
        }

        result = PrerequisiteChecker.validate_prerequisite_tree(self_referencing)

        assert result['valid'] is False
        assert result['has_cycles'] is True


class TestPrerequisiteIntegration:
    """Test integration with skill and skill tree systems."""

    def test_skill_with_prerequisites_check(self, skill_with_prerequisites):
        """Test checking prerequisites on a skill."""
        skill_levels = {
            "Basic Programming": 25.0,
            "Data Structures": 20.0
        }

        all_met, missing = PrerequisiteChecker.check_prerequisites(
            skill_with_prerequisites.prerequisites,
            skill_levels
        )

        assert all_met is True
        assert len(missing) == 0

    def test_skill_prerequisite_progress(self, skill_with_prerequisites):
        """Test progress toward skill prerequisites."""
        skill_levels = {
            "Basic Programming": 15.0,  # 75% of 20
            "Data Structures": 7.5      # 50% of 15
        }

        progress = PrerequisiteChecker.get_overall_progress(
            skill_with_prerequisites.prerequisites,
            skill_levels
        )

        assert progress == 62.5  # (75 + 50) / 2

    def test_optional_vs_required_prerequisites(self):
        """Test behavior with mixed optional and required prerequisites."""
        prerequisites = [
            SkillPrerequisite("Required Skill", 20.0, optional=False),
            SkillPrerequisite("Optional Skill", 20.0, optional=True)
        ]

        # Only have required skill
        skill_levels = {"Required Skill": 25.0}

        all_met, missing = PrerequisiteChecker.check_prerequisites(
            prerequisites, skill_levels
        )

        assert all_met is True  # Optional not needed

    def test_complex_prerequisite_tree_validation(self):
        """Test validating a complex prerequisite structure."""
        complex_tree = {
            "Root Skill": [],
            "Intermediate A": [SkillPrerequisite("Root Skill", 10.0)],
            "Intermediate B": [SkillPrerequisite("Root Skill", 10.0)],
            "Advanced": [
                SkillPrerequisite("Intermediate A", 20.0),
                SkillPrerequisite("Intermediate B", 20.0)
            ]
        }

        result = PrerequisiteChecker.validate_prerequisite_tree(complex_tree)

        assert result['valid'] is True

    def test_prerequisite_chain_ordering(self, prerequisite_chain):
        """Test that prerequisite chain maintains proper order."""
        chain = PrerequisiteChecker.get_prerequisite_chain(
            "Skill D", prerequisite_chain
        )

        # Skill A should come before Skill B
        # Skill B should come before Skill C
        if "Skill A" in chain and "Skill B" in chain:
            assert chain.index("Skill A") < chain.index("Skill B")

        if "Skill B" in chain and "Skill C" in chain:
            assert chain.index("Skill B") < chain.index("Skill C")
