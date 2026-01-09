"""
Advanced Skill with full progression system.

Defines the core AdvancedSkill class with experience tracking,
mastery levels, specializations, and usage tracking.
"""

import math
from datetime import datetime
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SkillCategory(Enum):
    """Categories of skills"""
    COGNITIVE = "cognitive"
    SOCIAL = "social"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    EMOTIONAL = "emotional"
    PHYSICAL = "physical"
    LEADERSHIP = "leadership"
    WISDOM = "wisdom"


@dataclass
class AdvancedSkill:
    """Enhanced skill with full progression system"""
    name: str
    category: SkillCategory
    description: str
    current_level: float = 0.0
    max_level: float = 100.0
    experience_points: int = 0
    experience_to_next_level: int = 100

    # Usage tracking
    total_uses: int = 0
    successful_uses: int = 0
    last_used: Optional[datetime] = None

    # Learning factors
    learning_rate: float = 1.0  # Multiplier for experience gain
    difficulty: float = 1.0     # Base difficulty (higher = harder to level)

    # Specializations
    specializations: Dict[str, float] = field(default_factory=dict)  # name -> level
    current_specialization: Optional[str] = None

    # Progression elements
    prerequisites: List[Any] = field(default_factory=list)
    synergies: List[Any] = field(default_factory=list)
    milestones: List[Any] = field(default_factory=list)

    # Metadata
    tags: Set[str] = field(default_factory=set)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def mastery_level(self) -> str:
        """Get current mastery level based on skill level"""
        level_percentage = self.current_level / self.max_level

        if level_percentage >= 0.95:
            return "Grandmaster"
        elif level_percentage >= 0.80:
            return "Master"
        elif level_percentage >= 0.60:
            return "Expert"
        elif level_percentage >= 0.40:
            return "Journeyman"
        elif level_percentage >= 0.20:
            return "Apprentice"
        else:
            return "Novice"

    @property
    def success_rate(self) -> float:
        """Calculate success rate based on level and experience"""
        base_rate = self.current_level / self.max_level
        experience_bonus = math.log(max(1, self.total_uses)) * 0.01
        return min(0.95, base_rate + experience_bonus)

    def add_experience(self, amount: int) -> Tuple[bool, float]:
        """Add experience and return (leveled_up, new_level)"""
        self.experience_points += int(amount * self.learning_rate)
        self.total_uses += 1
        self.last_used = datetime.now()

        leveled_up = False
        old_level = self.current_level

        # Calculate new level based on experience
        while self.experience_points >= self.experience_to_next_level and self.current_level < self.max_level:
            self.experience_points -= self.experience_to_next_level
            self.current_level = min(self.max_level, self.current_level + 1.0)
            self.experience_to_next_level = int(self._calculate_next_level_exp())
            leveled_up = True

            # Check milestones
            self._check_milestones()

        self.updated_at = datetime.now()

        if leveled_up:
            logger.info(f"Skill {self.name} leveled up from {old_level:.1f} to {self.current_level:.1f}")

        return (leveled_up, self.current_level)

    def _calculate_next_level_exp(self) -> int:
        """Calculate experience needed for next level using exponential scaling"""
        base_exp = 100
        level_factor = math.pow(self.current_level + 1, self.difficulty * 1.5)
        return int(base_exp * level_factor)

    def _check_milestones(self):
        """Check if any milestones have been reached"""
        for milestone in self.milestones:
            if self.current_level >= milestone.level and milestone.title not in self.tags:
                self.tags.add(milestone.title)
                logger.info(f"Milestone reached: {milestone.title} for skill {self.name}")

    def can_specialize_in(self, specialization: str) -> bool:
        """Check if character can specialize in a specific area"""
        return self.current_level >= 20.0 and specialization not in self.specializations

    def add_specialization(self, name: str, initial_level: float = 1.0):
        """Add a specialization to this skill"""
        if self.can_specialize_in(name):
            self.specializations[name] = min(10.0, initial_level)
            self.updated_at = datetime.now()
            return True
        return False

    def practice_specialization(self, name: str, success: bool) -> float:
        """Practice a specific specialization"""
        if name not in self.specializations:
            return 0.0

        # Calculate improvement
        base_improvement = 0.1 if success else 0.05
        synergy_bonus = self._calculate_synergy_bonus(name)
        total_improvement = base_improvement * (1.0 + synergy_bonus)

        # Update specialization level
        current = self.specializations[name]
        new_level = min(10.0, current + total_improvement)
        self.specializations[name] = new_level
        self.updated_at = datetime.now()

        return new_level - current

    def _calculate_synergy_bonus(self, specialization: str) -> float:
        """Calculate synergy bonus from related skills"""
        total_bonus = 0.0

        for synergy in self.synergies:
            if synergy.secondary_skill == specialization:
                # This would reference the actual skill level in a full implementation
                # For now, we'll use a simplified calculation
                total_bonus += synergy.bonus_value * 0.1

        return total_bonus

    def to_dict(self) -> Dict[str, Any]:
        """Convert skill to dictionary for serialization"""
        return {
            'name': self.name,
            'category': self.category.value,
            'description': self.description,
            'current_level': self.current_level,
            'max_level': self.max_level,
            'experience_points': self.experience_points,
            'experience_to_next_level': self.experience_to_next_level,
            'mastery_level': self.mastery_level,
            'success_rate': self.success_rate,
            'total_uses': self.total_uses,
            'successful_uses': self.successful_uses,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'learning_rate': self.learning_rate,
            'difficulty': self.difficulty,
            'specializations': self.specializations,
            'current_specialization': self.current_specialization,
            'tags': list(self.tags),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
