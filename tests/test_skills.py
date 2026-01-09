"""
Tests for individual skills functionality.
"""

import pytest
from datetime import datetime
from character_skill_trees.core.skill import AdvancedSkill, SkillCategory


class TestSkillCreation:
    """Test skill creation and initialization."""

    def test_create_basic_skill(self, sample_skill):
        """Test creating a basic skill."""
        assert sample_skill.name == "Test Skill"
        assert sample_skill.category == SkillCategory.TECHNICAL
        assert sample_skill.description == "A skill for testing purposes"
        assert sample_skill.current_level == 0.0
        assert sample_skill.max_level == 100.0
        assert sample_skill.experience_points == 0
        assert sample_skill.experience_to_next_level == 100

    def test_skill_with_custom_attributes(self):
        """Test creating a skill with custom attributes."""
        skill = AdvancedSkill(
            name="Custom Skill",
            category=SkillCategory.CREATIVE,
            description="A custom skill",
            current_level=25.0,
            max_level=150.0,
            learning_rate=1.5,
            difficulty=0.8
        )

        assert skill.current_level == 25.0
        assert skill.max_level == 150.0
        assert skill.learning_rate == 1.5
        assert skill.difficulty == 0.8

    def test_skill_initialization_defaults(self):
        """Test default values for skill attributes."""
        skill = AdvancedSkill(
            name="Default Skill",
            category=SkillCategory.SOCIAL,
            description="Testing defaults"
        )

        assert skill.current_level == 0.0
        assert skill.max_level == 100.0
        assert skill.experience_points == 0
        assert skill.total_uses == 0
        assert skill.successful_uses == 0
        assert skill.learning_rate == 1.0
        assert skill.difficulty == 1.0
        assert skill.specializations == {}
        assert skill.tags == set()
        assert isinstance(skill.created_at, datetime)
        assert isinstance(skill.updated_at, datetime)


class TestSkillCategories:
    """Test skill categories."""

    def test_all_categories_exist(self):
        """Test that all 8 skill categories are defined."""
        categories = [
            SkillCategory.COGNITIVE,
            SkillCategory.SOCIAL,
            SkillCategory.CREATIVE,
            SkillCategory.TECHNICAL,
            SkillCategory.EMOTIONAL,
            SkillCategory.PHYSICAL,
            SkillCategory.LEADERSHIP,
            SkillCategory.WISDOM
        ]
        assert len(categories) == 8

    def test_category_values(self):
        """Test category enum values."""
        assert SkillCategory.COGNITIVE.value == "cognitive"
        assert SkillCategory.SOCIAL.value == "social"
        assert SkillCategory.CREATIVE.value == "creative"
        assert SkillCategory.TECHNICAL.value == "technical"
        assert SkillCategory.EMOTIONAL.value == "emotional"
        assert SkillCategory.PHYSICAL.value == "physical"
        assert SkillCategory.LEADERSHIP.value == "leadership"
        assert SkillCategory.WISDOM.value == "wisdom"


class TestSkillExperience:
    """Test experience gaining and level progression."""

    def test_add_experience_basic(self, sample_skill):
        """Test basic experience addition."""
        leveled_up, new_level = sample_skill.add_experience(50)

        assert sample_skill.experience_points == 50
        assert sample_skill.total_uses == 1
        assert not leveled_up
        assert new_level == 0.0

    def test_add_experience_with_level_up(self, sample_skill):
        """Test experience addition that causes level up."""
        leveled_up, new_level = sample_skill.add_experience(100)

        assert leveled_up
        assert new_level == 1.0
        assert sample_skill.current_level == 1.0

    def test_add_multiple_levels(self, sample_skill):
        """Test gaining multiple levels at once."""
        # Add enough experience for multiple levels
        sample_skill.add_experience(500)

        # Should have gained multiple levels
        assert sample_skill.current_level > 1.0

    def test_learning_rate_affects_experience(self):
        """Test that learning rate affects experience gain."""
        skill1 = AdvancedSkill(
            name="Fast Learner",
            category=SkillCategory.COGNITIVE,
            description="Learns quickly",
            learning_rate=2.0
        )

        skill2 = AdvancedSkill(
            name="Normal Learner",
            category=SkillCategory.COGNITIVE,
            description="Normal learning",
            learning_rate=1.0
        )

        skill1.add_experience(100)
        skill2.add_experience(100)

        assert skill1.experience_points == 200
        assert skill2.experience_points == 100

    def test_max_level_cap(self):
        """Test that skill cannot exceed max level."""
        skill = AdvancedSkill(
            name="Capped Skill",
            category=SkillCategory.TECHNICAL,
            description="Has a level cap",
            max_level=50.0,
            current_level=49.0
        )

        # Add experience that would exceed max level
        skill.add_experience(10000)

        assert skill.current_level <= 50.0


class TestSkillUsage:
    """Test skill usage tracking."""

    def test_record_usage(self, sample_skill):
        """Test that usage is recorded."""
        initial_uses = sample_skill.total_uses
        sample_skill.add_experience(50)

        assert sample_skill.total_uses == initial_uses + 1
        assert sample_skill.last_used is not None

    def test_last_used_timestamp(self, sample_skill):
        """Test that last_used timestamp is updated."""
        before = datetime.now()
        sample_skill.add_experience(50)
        after = datetime.now()

        assert before <= sample_skill.last_used <= after


class TestSkillSpecializations:
    """Test skill specializations."""

    def test_add_specialization(self, sample_skill):
        """Test adding a specialization."""
        sample_skill.current_level = 20.0  # Meet requirement

        result = sample_skill.add_specialization("testing", 3.0)

        assert result is True
        assert "testing" in sample_skill.specializations
        assert sample_skill.specializations["testing"] == 3.0

    def test_cannot_specialize_below_level_20(self, sample_skill):
        """Test that specialization requires level 20."""
        sample_skill.current_level = 15.0

        result = sample_skill.add_specialization("advanced", 1.0)

        assert result is False
        assert "advanced" not in sample_skill.specializations

    def test_specialization_level_cap(self):
        """Test that specialization is capped at 10.0."""
        skill = AdvancedSkill(
            name="Capped Specialization",
            category=SkillCategory.TECHNICAL,
            description="Testing cap",
            current_level=50.0
        )

        skill.add_specialization("overshoot", 15.0)

        assert skill.specializations["overshoot"] == 10.0

    def test_practice_specialization(self, skill_with_specializations):
        """Test practicing a specialization."""
        initial_level = skill_with_specializations.specializations["python"]

        improvement = skill_with_specializations.practice_specialization("python", True)

        assert improvement > 0
        assert skill_with_specializations.specializations["python"] > initial_level

    def test_practice_nonexistent_specialization(self, skill_with_specializations):
        """Test practicing a specialization that doesn't exist."""
        improvement = skill_with_specializations.practice_specialization("rust", True)

        assert improvement == 0.0


class TestSkillProperties:
    """Test skill property calculations."""

    def test_mastery_level_novice(self):
        """Test novice mastery level (0-19%)."""
        skill = AdvancedSkill(
            name="Novice",
            category=SkillCategory.TECHNICAL,
            description="Novice level",
            current_level=10.0
        )

        assert skill.mastery_level == "Novice"

    def test_mastery_level_apprentice(self):
        """Test apprentice mastery level (20-39%)."""
        skill = AdvancedSkill(
            name="Apprentice",
            category=SkillCategory.TECHNICAL,
            description="Apprentice level",
            current_level=25.0
        )

        assert skill.mastery_level == "Apprentice"

    def test_mastery_level_journeyman(self):
        """Test journeyman mastery level (40-59%)."""
        skill = AdvancedSkill(
            name="Journeyman",
            category=SkillCategory.TECHNICAL,
            description="Journeyman level",
            current_level=50.0
        )

        assert skill.mastery_level == "Journeyman"

    def test_mastery_level_expert(self):
        """Test expert mastery level (60-79%)."""
        skill = AdvancedSkill(
            name="Expert",
            category=SkillCategory.TECHNICAL,
            description="Expert level",
            current_level=70.0
        )

        assert skill.mastery_level == "Expert"

    def test_mastery_level_master(self):
        """Test master mastery level (80-94%)."""
        skill = AdvancedSkill(
            name="Master",
            category=SkillCategory.TECHNICAL,
            description="Master level",
            current_level=85.0
        )

        assert skill.mastery_level == "Master"

    def test_mastery_level_grandmaster(self):
        """Test grandmaster mastery level (95-100%)."""
        skill = AdvancedSkill(
            name="Grandmaster",
            category=SkillCategory.TECHNICAL,
            description="Grandmaster level",
            current_level=97.0
        )

        assert skill.mastery_level == "Grandmaster"

    def test_success_rate_calculation(self, expert_skill):
        """Test success rate calculation."""
        success_rate = expert_skill.success_rate

        assert 0.0 <= success_rate <= 0.95
        assert success_rate > 0.5  # Expert should have good success rate


class TestSkillSerialization:
    """Test skill serialization to dictionary."""

    def test_to_dict(self, sample_skill):
        """Test converting skill to dictionary."""
        skill_dict = sample_skill.to_dict()

        assert isinstance(skill_dict, dict)
        assert skill_dict['name'] == "Test Skill"
        assert skill_dict['category'] == "technical"
        assert skill_dict['current_level'] == 0.0
        assert skill_dict['max_level'] == 100.0
        assert 'mastery_level' in skill_dict
        assert 'success_rate' in skill_dict

    def test_to_dict_with_specializations(self, skill_with_specializations):
        """Test serialization with specializations."""
        skill_dict = skill_with_specializations.to_dict()

        assert 'specializations' in skill_dict
        assert isinstance(skill_dict['specializations'], dict)
        assert len(skill_dict['specializations']) == 3

    def test_to_dict_includes_tags(self, sample_skill):
        """Test that tags are included in serialization."""
        sample_skill.tags.add("test_tag")
        sample_skill.tags.add("another_tag")

        skill_dict = sample_skill.to_dict()

        assert 'tags' in skill_dict
        assert isinstance(skill_dict['tags'], list)
        assert "test_tag" in skill_dict['tags']
        assert "another_tag" in skill_dict['tags']


class TestSkillValidation:
    """Test skill validation logic."""

    def test_can_specialize_in(self, sample_skill):
        """Test checking if specialization is possible."""
        # Below level 20
        assert not sample_skill.can_specialize_in("new_spec")

        # At or above level 20
        sample_skill.current_level = 20.0
        assert sample_skill.can_specialize_in("new_spec")

        # Already has specialization
        sample_skill.specializations["existing"] = 5.0
        assert not sample_skill.can_specialize_in("existing")

    def test_skill_tags(self, sample_skill):
        """Test skill tag management."""
        sample_skill.tags.add("technical")
        sample_skill.tags.add("beginner")

        assert "technical" in sample_skill.tags
        assert "beginner" in sample_skill.tags
        assert len(sample_skill.tags) == 2
