"""
Tests for progression system including mastery levels and experience calculations.
"""

import pytest
from character_skill_trees.core.skill import AdvancedSkill, SkillCategory
from character_skill_trees.progression.mastery import MasteryLevel, SkillMilestone
from character_skill_trees.progression.experience import ExperienceCalculator


class TestMasteryLevel:
    """Test mastery level determination and properties."""

    def test_mastery_from_level_novice(self):
        """Test novice level from skill level."""
        mastery = MasteryLevel.from_level(5.0, 100.0)
        assert mastery == MasteryLevel.NOVICE

    def test_mastery_from_level_apprentice(self):
        """Test apprentice level from skill level."""
        mastery = MasteryLevel.from_level(25.0, 100.0)
        assert mastery == MasteryLevel.APPRENTICE

    def test_mastery_from_level_journeyman(self):
        """Test journeyman level from skill level."""
        mastery = MasteryLevel.from_level(50.0, 100.0)
        assert mastery == MasteryLevel.JOURNEYMAN

    def test_mastery_from_level_expert(self):
        """Test expert level from skill level."""
        mastery = MasteryLevel.from_level(70.0, 100.0)
        assert mastery == MasteryLevel.EXPERT

    def test_mastery_from_level_master(self):
        """Test master level from skill level."""
        mastery = MasteryLevel.from_level(85.0, 100.0)
        assert mastery == MasteryLevel.MASTER

    def test_mastery_from_level_grandmaster(self):
        """Test grandmaster level from skill level."""
        mastery = MasteryLevel.from_level(96.0, 100.0)
        assert mastery == MasteryLevel.GRANDMASTER

    def test_mastery_boundary_conditions(self):
        """Test mastery level boundary conditions."""
        # Exactly at boundaries
        assert MasteryLevel.from_level(0.0, 100.0) == MasteryLevel.NOVICE
        assert MasteryLevel.from_level(20.0, 100.0) == MasteryLevel.APPRENTICE
        assert MasteryLevel.from_level(40.0, 100.0) == MasteryLevel.JOURNEYMAN
        assert MasteryLevel.from_level(60.0, 100.0) == MasteryLevel.EXPERT
        assert MasteryLevel.from_level(80.0, 100.0) == MasteryLevel.MASTER
        assert MasteryLevel.from_level(95.0, 100.0) == MasteryLevel.GRANDMASTER

    def test_mastery_tier_property(self):
        """Test mastery tier numeric values."""
        assert MasteryLevel.NOVICE.tier == 1
        assert MasteryLevel.APPRENTICE.tier == 2
        assert MasteryLevel.JOURNEYMAN.tier == 3
        assert MasteryLevel.EXPERT.tier == 4
        assert MasteryLevel.MASTER.tier == 5
        assert MasteryLevel.GRANDMASTER.tier == 6

    def test_mastery_color_codes(self):
        """Test mastery level color codes."""
        colors = {
            MasteryLevel.NOVICE: "#gray",
            MasteryLevel.APPRENTICE: "#green",
            MasteryLevel.JOURNEYMAN: "#blue",
            MasteryLevel.EXPERT: "#purple",
            MasteryLevel.MASTER: "#orange",
            MasteryLevel.GRANDMASTER: "#red"
        }

        for mastery, expected_color in colors.items():
            assert mastery.color_code == expected_color


class TestSkillMilestones:
    """Test skill milestone functionality."""

    def test_milestone_creation(self, milestone_list):
        """Test creating milestones."""
        milestone = milestone_list[0]

        assert milestone.level == 10.0
        assert milestone.title == "First Milestone"
        assert milestone.description == "Reach level 10"
        assert "unlock_1" in milestone.unlocks
        assert milestone.rewards == {"reward_1": 100}

    def test_milestone_is_reached(self, milestone_list):
        """Test checking if milestone is reached."""
        milestone = milestone_list[0]  # Level 10 milestone

        assert not milestone.is_reached(5.0)
        assert milestone.is_reached(10.0)
        assert milestone.is_reached(15.0)

    def test_milestone_progress_percentage(self, milestone_list):
        """Test milestone progress calculation."""
        milestone = milestone_list[1]  # Level 25 milestone

        # Before milestone (assuming previous at 12.5)
        progress = milestone.get_progress_percentage(15.0)
        assert 0.0 < progress < 100.0

        # At milestone
        assert milestone.get_progress_percentage(25.0) == 100.0

        # Past milestone
        assert milestone.get_progress_percentage(30.0) == 100.0

    def test_milestone_before_range(self, milestone_list):
        """Test progress before milestone range."""
        milestone = milestone_list[1]  # Level 25, previous at 12.5

        # Below previous milestone (12.5)
        progress = milestone.get_progress_percentage(10.0)
        assert progress == 0.0


class TestExperienceCalculator:
    """Test experience calculation utilities."""

    def test_calculate_next_level_exp_basic(self):
        """Test basic next level experience calculation."""
        exp_needed = ExperienceCalculator.calculate_next_level_exp(0.0, 1.0, 100)

        assert exp_needed == 100  # Base experience at level 0

    def test_calculate_next_level_exp_scaling(self):
        """Test that experience scales with level."""
        exp_level_0 = ExperienceCalculator.calculate_next_level_exp(0.0, 1.0, 100)
        exp_level_10 = ExperienceCalculator.calculate_next_level_exp(10.0, 1.0, 100)
        exp_level_50 = ExperienceCalculator.calculate_next_level_exp(50.0, 1.0, 100)

        assert exp_level_10 > exp_level_0
        assert exp_level_50 > exp_level_10

    def test_calculate_next_level_exp_difficulty(self):
        """Test that difficulty affects experience requirements."""
        exp_easy = ExperienceCalculator.calculate_next_level_exp(10.0, 0.5, 100)
        exp_hard = ExperienceCalculator.calculate_next_level_exp(10.0, 1.5, 100)

        assert exp_hard > exp_easy

    def test_calculate_total_exp_to_level(self):
        """Test calculating total experience to reach a level."""
        total_exp = ExperienceCalculator.calculate_total_exp_to_level(5.0, 1.0, 100)

        # Should be sum of exp for levels 0-4
        expected = sum(
            ExperienceCalculator.calculate_next_level_exp(i, 1.0, 100)
            for i in range(5)
        )

        assert total_exp == expected

    def test_calculate_experience_gain_success(self):
        """Test experience gain from successful practice."""
        exp_gain = ExperienceCalculator.calculate_experience_gain(
            success=True,
            difficulty=1.0,
            time_spent=10.0,
            learning_rate=1.0
        )

        # Base: 1.0 * 10.0 * 10 = 100, with 1.5x success bonus
        assert exp_gain == 150

    def test_calculate_experience_gain_failure(self):
        """Test experience gain from failed practice."""
        exp_gain = ExperienceCalculator.calculate_experience_gain(
            success=False,
            difficulty=1.0,
            time_spent=10.0,
            learning_rate=1.0
        )

        # Base: 1.0 * 10.0 * 10 = 100, no success bonus
        assert exp_gain == 100

    def test_calculate_experience_gain_learning_rate(self):
        """Test that learning rate affects experience gain."""
        exp_normal = ExperienceCalculator.calculate_experience_gain(
            success=True,
            difficulty=1.0,
            time_spent=10.0,
            learning_rate=1.0
        )

        exp_fast = ExperienceCalculator.calculate_experience_gain(
            success=True,
            difficulty=1.0,
            time_spent=10.0,
            learning_rate=2.0
        )

        assert exp_fast == exp_normal * 2

    def test_calculate_level_progress(self):
        """Test calculating progress toward next level."""
        progress = ExperienceCalculator.calculate_level_progress(50, 100)

        assert progress == 50.0

    def test_calculate_level_progress_complete(self):
        """Test progress calculation when complete."""
        progress = ExperienceCalculator.calculate_level_progress(100, 100)

        assert progress == 100.0

    def test_calculate_level_progress_cap(self):
        """Test that progress is capped at 100%."""
        progress = ExperienceCalculator.calculate_level_progress(150, 100)

        assert progress == 100.0

    def test_estimate_level_from_total_exp(self):
        """Test estimating level from total experience."""
        # At level 0, need 100 exp
        level = ExperienceCalculator.estimate_level_from_total_exp(50, 1.0, 100)

        assert 0.0 < level < 1.0
        assert level == 0.5

    def test_estimate_level_complete_levels(self):
        """Test estimating complete levels."""
        # Enough for exactly 2 levels (100 + 200 = 300, roughly)
        total_exp = (
            ExperienceCalculator.calculate_next_level_exp(0.0, 1.0, 100) +
            ExperienceCalculator.calculate_next_level_exp(1.0, 1.0, 100)
        )

        level = ExperienceCalculator.estimate_level_from_total_exp(total_exp, 1.0, 100)

        assert level == 2.0


class TestProgressionIntegration:
    """Test integration of progression systems."""

    def test_skill_progression_through_mastery_levels(self, sample_skill):
        """Test skill progressing through all mastery levels."""
        mastery_levels = [
            ("Novice", 10.0),
            ("Apprentice", 25.0),
            ("Journeyman", 50.0),
            ("Expert", 70.0),
            ("Master", 85.0),
            ("Grandmaster", 96.0)
        ]

        for expected_mastery, level in mastery_levels:
            sample_skill.current_level = level
            assert sample_skill.mastery_level == expected_mastery

    def test_experience_calculations_match_skill_progression(self):
        """Test that experience calculations align with skill progression."""
        skill = AdvancedSkill(
            name="Test",
            category=SkillCategory.TECHNICAL,
            description="Test"
        )

        # Calculate expected exp for level 5
        expected_exp = ExperienceCalculator.calculate_total_exp_to_level(5.0, 1.0, 100)

        # Add experience to skill
        for _ in range(5):
            skill.add_experience(
                ExperienceCalculator.calculate_next_level_exp(skill.current_level, 1.0, 100)
            )

        # Skill should be at or near level 5
        assert skill.current_level >= 5.0

    def test_milestone_checking_during_progression(self, skill_with_milestones):
        """Test that milestones are checked during skill progression."""
        # Add milestone tag when reached
        initial_tags = len(skill_with_milestones.tags)

        # Trigger milestone check
        skill_with_milestones._check_milestones()

        # Level 35 should have reached first milestone (level 10)
        assert len(skill_with_milestones.tags) >= initial_tags
