"""
Skill synergies and cross-skill transfer effects.
"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class SkillSynergy:
    """Synergy between skills that provides bonuses"""
    primary_skill: str
    secondary_skill: str
    bonus_type: str  # "experience", "level", "success_rate"
    bonus_value: float
    activation_level: float

    def is_active(self, primary_level: float, secondary_level: float) -> bool:
        """
        Check if synergy is active.

        Args:
            primary_level: Current level of primary skill
            secondary_level: Current level of secondary skill

        Returns:
            True if both skills meet activation requirements
        """
        return primary_level >= self.activation_level and secondary_level >= self.activation_level

    def calculate_bonus(self, primary_level: float, secondary_level: float) -> float:
        """
        Calculate the bonus provided by this synergy.

        Args:
            primary_level: Current level of primary skill
            secondary_level: Current level of secondary skill

        Returns:
            Bonus value
        """
        if not self.is_active(primary_level, secondary_level):
            return 0.0

        # Bonus scales with skill levels
        level_factor = (primary_level + secondary_level) / (2 * self.activation_level)
        return self.bonus_value * level_factor

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'primary_skill': self.primary_skill,
            'secondary_skill': self.secondary_skill,
            'bonus_type': self.bonus_type,
            'bonus_value': self.bonus_value,
            'activation_level': self.activation_level
        }


class SynergyCalculator:
    """Calculate and manage skill synergies"""

    @staticmethod
    def calculate_total_synergy_bonus(skill_name: str, all_synergies: List[SkillSynergy],
                                     skill_levels: Dict[str, float],
                                     bonus_type: str = None) -> float:
        """
        Calculate total synergy bonus for a skill.

        Args:
            skill_name: Name of the skill to calculate bonus for
            all_synergies: List of all synergies
            skill_levels: Dictionary mapping skill names to current levels
            bonus_type: Filter by bonus type (None for all types)

        Returns:
            Total bonus value
        """
        total_bonus = 0.0

        for synergy in all_synergies:
            # Check if this synergy involves the skill
            if synergy.primary_skill != skill_name and synergy.secondary_skill != skill_name:
                continue

            # Filter by bonus type if specified
            if bonus_type and synergy.bonus_type != bonus_type:
                continue

            # Get skill levels
            primary_level = skill_levels.get(synergy.primary_skill, 0.0)
            secondary_level = skill_levels.get(synergy.secondary_skill, 0.0)

            # Calculate and add bonus
            bonus = synergy.calculate_bonus(primary_level, secondary_level)
            total_bonus += bonus

        return total_bonus

    @staticmethod
    def get_active_synergies(skill_name: str, all_synergies: List[SkillSynergy],
                            skill_levels: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Get all active synergies for a skill.

        Args:
            skill_name: Name of the skill
            all_synergies: List of all synergies
            skill_levels: Dictionary mapping skill names to current levels

        Returns:
            List of active synergy information dictionaries
        """
        active = []

        for synergy in all_synergies:
            if synergy.primary_skill != skill_name and synergy.secondary_skill != skill_name:
                continue

            primary_level = skill_levels.get(synergy.primary_skill, 0.0)
            secondary_level = skill_levels.get(synergy.secondary_skill, 0.0)

            if synergy.is_active(primary_level, secondary_level):
                bonus = synergy.calculate_bonus(primary_level, secondary_level)
                active.append({
                    'synergy': synergy.to_dict(),
                    'bonus_value': bonus,
                    'primary_level': primary_level,
                    'secondary_level': secondary_level
                })

        return active

    @staticmethod
    def recommend_synergy_development(skill_name: str, all_synergies: List[SkillSynergy],
                                     skill_levels: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Recommend skills to develop for synergy benefits.

        Args:
            skill_name: Name of the skill
            all_synergies: List of all synergies
            skill_levels: Dictionary mapping skill names to current levels

        Returns:
            List of recommendations
        """
        recommendations = []

        for synergy in all_synergies:
            # Find synergies involving this skill
            other_skill = None
            if synergy.primary_skill == skill_name:
                other_skill = synergy.secondary_skill
            elif synergy.secondary_skill == skill_name:
                other_skill = synergy.primary_skill
            else:
                continue

            current_level = skill_levels.get(other_skill, 0.0)
            primary_level = skill_levels.get(synergy.primary_skill, 0.0)
            secondary_level = skill_levels.get(synergy.secondary_skill, 0.0)

            # Check if synergy is not yet active
            if not synergy.is_active(primary_level, secondary_level):
                progress = min(primary_level, secondary_level) / synergy.activation_level
                recommendations.append({
                    'skill': other_skill,
                    'activation_level': synergy.activation_level,
                    'current_level': current_level,
                    'progress': progress * 100,
                    'bonus_type': synergy.bonus_type,
                    'potential_bonus': synergy.bonus_value,
                    'priority': synergy.bonus_value / synergy.activation_level
                })

        # Sort by priority (bonus per level)
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        return recommendations

    @staticmethod
    def calculate_synergy_network_strength(all_synergies: List[SkillSynergy],
                                         skill_levels: Dict[str, float]) -> float:
        """
        Calculate overall strength of synergy network.

        Args:
            all_synergies: List of all synergies
            skill_levels: Dictionary mapping skill names to current levels

        Returns:
            Network strength score (0-100)
        """
        if not all_synergies:
            return 0.0

        total_bonus = 0.0
        possible_bonus = 0.0

        for synergy in all_synergies:
            primary_level = skill_levels.get(synergy.primary_skill, 0.0)
            secondary_level = skill_levels.get(synergy.secondary_skill, 0.0)

            # Calculate current bonus
            total_bonus += synergy.calculate_bonus(primary_level, secondary_level)

            # Calculate max possible bonus
            max_level = max(primary_level, secondary_level, synergy.activation_level)
            possible_bonus += synergy.calculate_bonus(max_level, max_level)

        if possible_bonus == 0:
            return 0.0

        return (total_bonus / possible_bonus) * 100.0
