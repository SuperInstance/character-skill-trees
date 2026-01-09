"""
Mastery levels and milestones for skill progression.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class MasteryLevel(Enum):
    """Mastery levels with visual indicators"""
    NOVICE = "Novice"
    APPRENTICE = "Apprentice"
    JOURNEYMAN = "Journeyman"
    EXPERT = "Expert"
    MASTER = "Master"
    GRANDMASTER = "Grandmaster"

    @classmethod
    def from_level(cls, level: float, max_level: float = 100.0) -> 'MasteryLevel':
        """Get mastery level from current skill level"""
        level_percentage = level / max_level

        if level_percentage >= 0.95:
            return cls.GRANDMASTER
        elif level_percentage >= 0.80:
            return cls.MASTER
        elif level_percentage >= 0.60:
            return cls.EXPERT
        elif level_percentage >= 0.40:
            return cls.JOURNEYMAN
        elif level_percentage >= 0.20:
            return cls.APPRENTICE
        else:
            return cls.NOVICE

    @property
    def tier(self) -> int:
        """Get numeric tier for mastery level"""
        tiers = {
            MasteryLevel.NOVICE: 1,
            MasteryLevel.APPRENTICE: 2,
            MasteryLevel.JOURNEYMAN: 3,
            MasteryLevel.EXPERT: 4,
            MasteryLevel.MASTER: 5,
            MasteryLevel.GRANDMASTER: 6
        }
        return tiers[self]

    @property
    def color_code(self) -> str:
        """Get color code for visualization"""
        colors = {
            MasteryLevel.NOVICE: "#gray",
            MasteryLevel.APPRENTICE: "#green",
            MasteryLevel.JOURNEYMAN: "#blue",
            MasteryLevel.EXPERT: "#purple",
            MasteryLevel.MASTER: "#orange",
            MasteryLevel.GRANDMASTER: "#red"
        }
        return colors[self]


@dataclass
class SkillMilestone:
    """Milestone achievements for skill progression"""
    level: float
    title: str
    description: str
    unlocks: List[str]
    rewards: Dict[str, Any]

    def is_reached(self, current_level: float) -> bool:
        """Check if milestone has been reached"""
        return current_level >= self.level

    def get_progress_percentage(self, current_level: float) -> float:
        """Get progress percentage toward this milestone"""
        # Assuming previous milestone was at level/2
        previous_milestone = self.level / 2
        if current_level <= previous_milestone:
            return 0.0
        if current_level >= self.level:
            return 100.0
        return ((current_level - previous_milestone) / (self.level - previous_milestone)) * 100.0
