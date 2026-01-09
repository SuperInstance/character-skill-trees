"""
Experience calculation and progression utilities.
"""

import math
from typing import Tuple, Dict, Any


class ExperienceCalculator:
    """Calculate experience requirements and progression"""

    @staticmethod
    def calculate_next_level_exp(current_level: float, difficulty: float = 1.0,
                                base_exp: int = 100) -> int:
        """
        Calculate experience needed for next level using exponential scaling.

        Args:
            current_level: Current skill level
            difficulty: Skill difficulty modifier (higher = harder)
            base_exp: Base experience requirement

        Returns:
            Experience points needed for next level
        """
        level_factor = math.pow(current_level + 1, difficulty * 1.5)
        return int(base_exp * level_factor)

    @staticmethod
    def calculate_total_exp_to_level(target_level: float, difficulty: float = 1.0,
                                    base_exp: int = 100) -> int:
        """
        Calculate total experience needed to reach a specific level.

        Args:
            target_level: Target level to reach
            difficulty: Skill difficulty modifier
            base_exp: Base experience requirement

        Returns:
            Total experience points needed
        """
        total_exp = 0
        for level in range(int(target_level)):
            total_exp += ExperienceCalculator.calculate_next_level_exp(
                level, difficulty, base_exp
            )
        return total_exp

    @staticmethod
    def calculate_experience_gain(success: bool, difficulty: float,
                                 time_spent: float, learning_rate: float = 1.0) -> int:
        """
        Calculate experience gain from practicing a skill.

        Args:
            success: Whether the practice attempt was successful
            difficulty: Task difficulty modifier
            time_spent: Time spent practicing (in minutes)
            learning_rate: Character's learning rate multiplier

        Returns:
            Experience points gained
        """
        base_exp = int(difficulty * time_spent * 10)
        if success:
            base_exp = int(base_exp * 1.5)

        return int(base_exp * learning_rate)

    @staticmethod
    def calculate_level_progress(current_exp: int, exp_to_next: int) -> float:
        """
        Calculate progress percentage toward next level.

        Args:
            current_exp: Current experience points
            exp_to_next: Experience needed for next level

        Returns:
            Progress percentage (0-100)
        """
        return min(100.0, (current_exp / exp_to_next) * 100.0)

    @staticmethod
    def estimate_level_from_total_exp(total_exp: int, difficulty: float = 1.0,
                                     base_exp: int = 100) -> float:
        """
        Estimate current level from total experience points.

        Args:
            total_exp: Total experience accumulated
            difficulty: Skill difficulty modifier
            base_exp: Base experience requirement

        Returns:
            Estimated level
        """
        level = 0.0
        remaining_exp = total_exp

        while remaining_exp > 0:
            needed = ExperienceCalculator.calculate_next_level_exp(level, difficulty, base_exp)
            if remaining_exp < needed:
                # Partial level progress
                level += remaining_exp / needed
                break
            remaining_exp -= needed
            level += 1.0

        return level
