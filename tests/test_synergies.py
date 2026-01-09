"""
Tests for skill synergies and cross-skill transfer effects.
"""

import pytest
from character_skill_trees.transfer.synergies import (
    SkillSynergy,
    SynergyCalculator
)


class TestSkillSynergy:
    """Test individual synergy functionality."""

    def test_create_synergy(self):
        """Test creating a skill synergy."""
        synergy = SkillSynergy(
            primary_skill="Skill A",
            secondary_skill="Skill B",
            bonus_type="experience",
            bonus_value=1.5,
            activation_level=10.0
        )

        assert synergy.primary_skill == "Skill A"
        assert synergy.secondary_skill == "Skill B"
        assert synergy.bonus_type == "experience"
        assert synergy.bonus_value == 1.5
        assert synergy.activation_level == 10.0

    def test_synergy_is_active_both_met(self):
        """Test synergy is active when both skills meet requirements."""
        synergy = SkillSynergy("Skill A", "Skill B", "experience", 1.5, 10.0)

        assert synergy.is_active(15.0, 12.0) is True

    def test_synergy_is_active_primary_low(self):
        """Test synergy not active when primary skill is too low."""
        synergy = SkillSynergy("Skill A", "Skill B", "experience", 1.5, 10.0)

        assert synergy.is_active(5.0, 15.0) is False

    def test_synergy_is_active_secondary_low(self):
        """Test synergy not active when secondary skill is too low."""
        synergy = SkillSynergy("Skill A", "Skill B", "experience", 1.5, 10.0)

        assert synergy.is_active(15.0, 5.0) is False

    def test_synergy_is_active_exactly_at_threshold(self):
        """Test synergy activation at exact threshold."""
        synergy = SkillSynergy("Skill A", "Skill B", "experience", 1.5, 10.0)

        assert synergy.is_active(10.0, 10.0) is True

    def test_calculate_bonus_when_active(self):
        """Test bonus calculation when synergy is active."""
        synergy = SkillSynergy("Skill A", "Skill B", "experience", 1.5, 10.0)

        bonus = synergy.calculate_bonus(15.0, 15.0)

        # Level factor: (15 + 15) / (2 * 10) = 1.5
        # Bonus: 1.5 * 1.5 = 2.25
        assert bonus == pytest.approx(2.25, rel=0.01)

    def test_calculate_bonus_when_inactive(self):
        """Test bonus calculation when synergy is not active."""
        synergy = SkillSynergy("Skill A", "Skill B", "experience", 1.5, 10.0)

        bonus = synergy.calculate_bonus(5.0, 15.0)

        assert bonus == 0.0

    def test_synergy_to_dict(self):
        """Test synergy serialization."""
        synergy = SkillSynergy("Skill A", "Skill B", "level", 0.2, 15.0)

        synergy_dict = synergy.to_dict()

        assert synergy_dict['primary_skill'] == "Skill A"
        assert synergy_dict['secondary_skill'] == "Skill B"
        assert synergy_dict['bonus_type'] == "level"
        assert synergy_dict['bonus_value'] == 0.2
        assert synergy_dict['activation_level'] == 15.0


class TestSynergyCalculator:
    """Test synergy calculation utilities."""

    def test_calculate_total_synergy_bonus(self, synergy_list, skill_levels):
        """Test calculating total synergy bonus for a skill."""
        total_bonus = SynergyCalculator.calculate_total_synergy_bonus(
            "Skill A",
            synergy_list,
            skill_levels
        )

        # Should have bonuses from both synergies involving Skill A
        assert total_bonus > 0

    def test_calculate_synergy_bonus_filter_by_type(self, synergy_list, skill_levels):
        """Test filtering synergy bonus by type."""
        exp_bonus = SynergyCalculator.calculate_total_synergy_bonus(
            "Skill A",
            synergy_list,
            skill_levels,
            bonus_type="experience"
        )

        level_bonus = SynergyCalculator.calculate_total_synergy_bonus(
            "Skill A",
            synergy_list,
            skill_levels,
            bonus_type="level"
        )

        # Should get different values for different types
        # (Both synergies for Skill A have different types)
        assert exp_bonus > 0 or level_bonus > 0

    def test_calculate_synergy_bonus_no_synergies(self, skill_levels):
        """Test calculating bonus with no synergies."""
        total_bonus = SynergyCalculator.calculate_total_synergy_bonus(
            "Skill A",
            [],
            skill_levels
        )

        assert total_bonus == 0.0

    def test_get_active_synergies(self, synergy_list, skill_levels):
        """Test getting list of active synergies."""
        active = SynergyCalculator.get_active_synergies(
            "Skill A",
            synergy_list,
            skill_levels
        )

        # Skill A has synergies with Skill B and Skill C
        # All should be active given the skill_levels
        assert len(active) > 0

        # Check structure of returned data
        for item in active:
            assert 'synergy' in item
            assert 'bonus_value' in item
            assert 'primary_level' in item
            assert 'secondary_level' in item

    def test_get_active_synergies_inactive(self, synergy_list):
        """Test getting active synergies when none are active."""
        low_levels = {
            "Skill A": 5.0,
            "Skill B": 5.0,
            "Skill C": 5.0
        }

        active = SynergyCalculator.get_active_synergies(
            "Skill A",
            synergy_list,
            low_levels
        )

        # Should be empty or contain only inactive synergies
        # But the method only returns active ones
        for item in active:
            synergy = SkillSynergy(**item['synergy'])
            assert synergy.is_active(
                item['primary_level'],
                item['secondary_level']
            )

    def test_recommend_synergy_development(self, synergy_list, skill_levels):
        """Test getting synergy development recommendations."""
        recommendations = SynergyCalculator.recommend_synergy_development(
            "Skill D",
            synergy_list,
            skill_levels
        )

        # Skill D is at level 5, so it might have recommendations
        # (depending on synergies involving it)
        assert isinstance(recommendations, list)

    def test_recommend_synergy_development_sorted(self, synergy_list):
        """Test that recommendations are sorted by priority."""
        skill_levels = {
            "Skill A": 25.0,
            "Skill B": 5.0,
            "Skill C": 5.0
        }

        recommendations = SynergyCalculator.recommend_synergy_development(
            "Skill B",
            synergy_list,
            skill_levels
        )

        # Check if sorted by priority (descending)
        if len(recommendations) > 1:
            for i in range(len(recommendations) - 1):
                assert recommendations[i]['priority'] >= recommendations[i + 1]['priority']

    def test_calculate_synergy_network_strength(self, synergy_list, skill_levels):
        """Test calculating overall synergy network strength."""
        strength = SynergyCalculator.calculate_synergy_network_strength(
            synergy_list,
            skill_levels
        )

        assert 0.0 <= strength <= 100.0

    def test_calculate_synergy_network_strength_empty(self):
        """Test network strength with no synergies."""
        strength = SynergyCalculator.calculate_synergy_network_strength(
            [],
            {}
        )

        assert strength == 0.0

    def test_recommend_synergy_development_structure(self, synergy_list, skill_levels):
        """Test structure of recommendation data."""
        recommendations = SynergyCalculator.recommend_synergy_development(
            "Skill A",
            synergy_list,
            skill_levels
        )

        for rec in recommendations:
            assert 'skill' in rec
            assert 'activation_level' in rec
            assert 'current_level' in rec
            assert 'progress' in rec
            assert 'bonus_type' in rec
            assert 'potential_bonus' in rec
            assert 'priority' in rec


class TestSynergyIntegration:
    """Test integration with skill and skill tree systems."""

    def test_skill_with_synergies(self, skill_with_synergies):
        """Test skill with synergies attached."""
        assert len(skill_with_synergies.synergies) == 2

        synergy1 = skill_with_synergies.synergies[0]
        assert synergy1.primary_skill == "System Architecture"
        assert synergy1.secondary_skill == "Database Design"

    def test_synergy_activation_in_context(self, skill_with_synergies):
        """Test synergy activation with related skill levels."""
        related_skill_levels = {
            "System Architecture": 30.0,
            "Database Design": 25.0,
            "Network Engineering": 20.0
        }

        # First synergy: System Architecture + Database Design (activation 20.0)
        synergy1 = skill_with_synergies.synergies[0]
        assert synergy1.is_active(
            related_skill_levels["System Architecture"],
            related_skill_levels["Database Design"]
        )

        # Second synergy: System Architecture + Network Engineering (activation 15.0)
        synergy2 = skill_with_synergies.synergies[1]
        assert synergy2.is_active(
            related_skill_levels["System Architecture"],
            related_skill_levels["Network Engineering"]
        )

    def test_cross_skill_bonuses(self, skill_tree_with_synergies):
        """Test cross-skill bonuses in skill tree."""
        skill_levels = {
            "Design": 30.0,
            "Development": 25.0,
            "Testing": 20.0
        }

        # Calculate bonus for Development from Design synergy
        all_synergies = []
        for skill in skill_tree_with_synergies.skills.values():
            all_synergies.extend(skill.synergies)

        dev_bonus = SynergyCalculator.calculate_total_synergy_bonus(
            "Development",
            all_synergies,
            skill_levels
        )

        # Should have bonus from Design
        assert dev_bonus > 0

    def test_synergy_network_development(self, skill_tree_with_synergies):
        """Test overall synergy network development."""
        all_synergies = []
        skill_levels = {}

        for name, skill in skill_tree_with_synergies.skills.items():
            all_synergies.extend(skill.synergies)
            skill_levels[name] = skill.current_level

        network_strength = SynergyCalculator.calculate_synergy_network_strength(
            all_synergies,
            skill_levels
        )

        assert 0.0 <= network_strength <= 100.0

    def test_synergy_types(self):
        """Test different synergy bonus types."""
        bonus_types = ["experience", "level", "success_rate"]

        for bonus_type in bonus_types:
            synergy = SkillSynergy(
                "Skill A",
                "Skill B",
                bonus_type,
                1.0,
                10.0
            )
            assert synergy.bonus_type == bonus_type


class TestSynergyCalculations:
    """Test detailed synergy calculations."""

    def test_bonus_scaling_with_levels(self):
        """Test that bonus scales with skill levels."""
        synergy = SkillSynergy("Skill A", "Skill B", "experience", 1.0, 10.0)

        bonus_low = synergy.calculate_bonus(10.0, 10.0)
        bonus_high = synergy.calculate_bonus(20.0, 20.0)

        assert bonus_high > bonus_low

    def test_bonus_asymmetric_levels(self):
        """Test bonus with asymmetric skill levels."""
        synergy = SkillSynergy("Skill A", "Skill B", "experience", 1.0, 10.0)

        bonus1 = synergy.calculate_bonus(15.0, 10.0)
        bonus2 = synergy.calculate_bonus(10.0, 15.0)

        # Should be the same (uses average)
        assert bonus1 == bonus2

    def test_activation_threshold_impact(self):
        """Test impact of different activation thresholds."""
        synergy_low = SkillSynergy("Skill A", "Skill B", "experience", 1.0, 5.0)
        synergy_high = SkillSynergy("Skill A", "Skill B", "experience", 1.0, 20.0)

        bonus_low = synergy_low.calculate_bonus(10.0, 10.0)
        bonus_high = synergy_high.calculate_bonus(25.0, 25.0)

        # Lower threshold should give higher bonus at same absolute levels
        # (because level factor is higher)
        assert bonus_low > bonus_high

    def test_bonus_value_impact(self):
        """Test impact of different bonus values."""
        synergy_low = SkillSynergy("Skill A", "Skill B", "experience", 0.5, 10.0)
        synergy_high = SkillSynergy("Skill A", "Skill B", "experience", 2.0, 10.0)

        bonus_low = synergy_low.calculate_bonus(15.0, 15.0)
        bonus_high = synergy_high.calculate_bonus(15.0, 15.0)

        assert bonus_high == 4 * bonus_low  # 2.0 is 4x 0.5
