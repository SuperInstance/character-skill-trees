"""
Skill Tree with interconnected skills and progression paths.
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

from .skill import AdvancedSkill

logger = logging.getLogger(__name__)


@dataclass
class SkillTree:
    """Complete skill tree with interconnected skills"""
    name: str
    description: str
    root_skills: List[str] = field(default_factory=list)
    skills: Dict[str, AdvancedSkill] = field(default_factory=dict)
    connections: Dict[str, List[str]] = field(default_factory=dict)  # skill -> list of connected skills

    # Tree progression
    total_points_spent: int = 0
    available_points: int = 0
    unlock_requirements: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Mastery achievements
    completed_paths: List[str] = field(default_factory=list)
    mastery_bonuses: Dict[str, float] = field(default_factory=dict)

    # Metadata
    tree_type: str = "general"
    difficulty_modifier: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)

    def add_skill(self, skill: AdvancedSkill, parent_skills: List[str] = None):
        """Add a skill to the tree"""
        self.skills[skill.name] = skill

        if parent_skills:
            self.connections[skill.name] = parent_skills
            for parent in parent_skills:
                if parent not in self.connections:
                    self.connections[parent] = []
                if skill.name not in self.connections[parent]:
                    self.connections[parent].append(skill.name)
        elif not self.root_skills:
            self.root_skills.append(skill.name)

    def can_unlock_skill(self, skill_name: str) -> Tuple[bool, str]:
        """Check if a skill can be unlocked"""
        if skill_name not in self.skills:
            return False, "Skill not found in tree"

        skill = self.skills[skill_name]

        # Check prerequisites
        for prereq in skill.prerequisites:
            if not prereq.optional:
                if prereq.skill_name not in self.skills:
                    return False, f"Missing prerequisite: {prereq.skill_name}"
                elif self.skills[prereq.skill_name].current_level < prereq.required_level:
                    return False, f"Prerequisite {prereq.skill_name} needs level {prereq.required_level}"

        # Check point requirements
        if skill_name in self.unlock_requirements:
            reqs = self.unlock_requirements[skill_name]
            if reqs.get('points', 0) > self.available_points:
                return False, f"Need {reqs['points']} skill points"

        return True, "Can unlock"

    def unlock_skill(self, skill_name: str, point_cost: int = 1) -> bool:
        """Unlock a skill using skill points"""
        can_unlock, reason = self.can_unlock_skill(skill_name)

        if not can_unlock:
            logger.warning(f"Cannot unlock {skill_name}: {reason}")
            return False

        if self.available_points < point_cost:
            logger.warning(f"Insufficient skill points for {skill_name}")
            return False

        # Deduct points and unlock skill
        self.available_points -= point_cost
        self.total_points_spent += point_cost

        # Initialize skill if it's at level 0
        if self.skills[skill_name].current_level == 0:
            self.skills[skill_name].current_level = 1.0

        logger.info(f"Unlocked skill: {skill_name}")
        return True

    def get_skill_progression_path(self, skill_name: str) -> List[str]:
        """Get the progression path to unlock a skill"""
        if skill_name not in self.skills:
            return []

        path = []
        visited = set()

        def dfs(current_skill: str):
            if current_skill in visited or current_skill not in self.skills:
                return

            visited.add(current_skill)

            # Add prerequisites first
            for prereq in self.skills[current_skill].prerequisites:
                if not prereq.optional:
                    dfs(prereq.skill_name)
                    if prereq.skill_name not in path:
                        path.append(prereq.skill_name)

            # Add current skill
            if current_skill not in path:
                path.append(current_skill)

        dfs(skill_name)
        return path

    def calculate_mastery_level(self) -> float:
        """Calculate overall mastery level of the tree"""
        if not self.skills:
            return 0.0

        total_levels = sum(skill.current_level for skill in self.skills.values())
        max_possible = sum(skill.max_level for skill in self.skills.values())

        return (total_levels / max_possible) * 100.0

    def get_tree_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the skill tree"""
        total_skills = len(self.skills)
        mastered_skills = sum(1 for skill in self.skills.values()
                            if skill.mastery_level in ["Master", "Grandmaster"])

        total_specializations = sum(len(skill.specializations) for skill in self.skills.values())

        return {
            'tree_name': self.name,
            'total_skills': total_skills,
            'mastered_skills': mastered_skills,
            'mastery_percentage': (mastered_skills / max(1, total_skills)) * 100,
            'total_specializations': total_specializations,
            'available_points': self.available_points,
            'total_points_spent': self.total_points_spent,
            'overall_mastery': self.calculate_mastery_level(),
            'completed_paths': len(self.completed_paths),
            'created_at': self.created_at.isoformat()
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert skill tree to dictionary for serialization"""
        return {
            'name': self.name,
            'description': self.description,
            'root_skills': self.root_skills,
            'skills': {name: skill.to_dict() for name, skill in self.skills.items()},
            'connections': self.connections,
            'total_points_spent': self.total_points_spent,
            'available_points': self.available_points,
            'unlock_requirements': self.unlock_requirements,
            'completed_paths': self.completed_paths,
            'mastery_bonuses': self.mastery_bonuses,
            'tree_type': self.tree_type,
            'difficulty_modifier': self.difficulty_modifier,
            'created_at': self.created_at.isoformat(),
            'statistics': self.get_tree_statistics()
        }
