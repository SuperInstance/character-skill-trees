"""
Skill prerequisites and requirement checking system.
"""

from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class SkillPrerequisite:
    """Skill prerequisite with required level"""
    skill_name: str
    required_level: float
    optional: bool = False

    def is_met(self, skill_levels: Dict[str, float]) -> bool:
        """
        Check if prerequisite is met.

        Args:
            skill_levels: Dictionary mapping skill names to current levels

        Returns:
            True if prerequisite is met or optional
        """
        if self.optional:
            return True

        current_level = skill_levels.get(self.skill_name, 0.0)
        return current_level >= self.required_level

    def get_progress(self, skill_levels: Dict[str, float]) -> float:
        """
        Get progress toward meeting this prerequisite.

        Args:
            skill_levels: Dictionary mapping skill names to current levels

        Returns:
            Progress percentage (0-100)
        """
        if self.optional:
            return 100.0

        current_level = skill_levels.get(self.skill_name, 0.0)
        if current_level >= self.required_level:
            return 100.0

        return (current_level / self.required_level) * 100.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'skill_name': self.skill_name,
            'required_level': self.required_level,
            'optional': self.optional
        }


class PrerequisiteChecker:
    """Check and validate skill prerequisites"""

    @staticmethod
    def check_prerequisites(prerequisites: List[SkillPrerequisite],
                           skill_levels: Dict[str, float]) -> Tuple[bool, List[str]]:
        """
        Check if all prerequisites are met.

        Args:
            prerequisites: List of skill prerequisites
            skill_levels: Dictionary mapping skill names to current levels

        Returns:
            Tuple of (all_met, missing_prereqs)
        """
        missing = []

        for prereq in prerequisites:
            if not prereq.is_met(skill_levels):
                missing.append(
                    f"{prereq.skill_name} (need level {prereq.required_level})"
                )

        return len(missing) == 0, missing

    @staticmethod
    def get_overall_progress(prerequisites: List[SkillPrerequisite],
                            skill_levels: Dict[str, float]) -> float:
        """
        Get overall progress toward meeting all prerequisites.

        Args:
            prerequisites: List of skill prerequisites
            skill_levels: Dictionary mapping skill names to current levels

        Returns:
            Overall progress percentage (0-100)
        """
        if not prerequisites:
            return 100.0

        total_progress = sum(prereq.get_progress(skill_levels)
                           for prereq in prerequisites)
        return total_progress / len(prerequisites)

    @staticmethod
    def get_prerequisite_chain(skill_name: str,
                               all_skills: Dict[str, List[SkillPrerequisite]],
                               visited: set = None) -> List[str]:
        """
        Get the complete chain of prerequisites for a skill.

        Args:
            skill_name: Name of the skill
            all_skills: Dictionary mapping skill names to their prerequisites
            visited: Set of already visited skills (to prevent cycles)

        Returns:
            Ordered list of prerequisite skill names
        """
        if visited is None:
            visited = set()

        if skill_name in visited:
            return []

        visited.add(skill_name)

        chain = []
        prerequisites = all_skills.get(skill_name, [])

        for prereq in prerequisites:
            if not prereq.optional:
                # Add recursive prerequisites first
                chain.extend(PrerequisiteChecker.get_prerequisite_chain(
                    prereq.skill_name, all_skills, visited
                ))
                # Then add this prerequisite
                if prereq.skill_name not in chain:
                    chain.append(prereq.skill_name)

        return chain

    @staticmethod
    def validate_prerequisite_tree(all_skills: Dict[str, List[SkillPrerequisite]]) -> Dict[str, Any]:
        """
        Validate that there are no circular dependencies in prerequisites.

        Args:
            all_skills: Dictionary mapping skill names to their prerequisites

        Returns:
            Dictionary with validation results
        """
        has_cycles = False
        cycles = []

        for skill_name in all_skills.keys():
            visited = set()
            path = []
            if PrerequisiteChecker._detect_cycle(skill_name, all_skills, visited, path):
                has_cycles = True
                cycles.append(path)

        return {
            'valid': not has_cycles,
            'has_cycles': has_cycles,
            'cycles': cycles
        }

    @staticmethod
    def _detect_cycle(skill_name: str, all_skills: Dict[str, List[SkillPrerequisite]],
                     visited: set, path: List[str]) -> bool:
        """Helper to detect circular dependencies"""
        if skill_name in path:
            return True

        if skill_name in visited:
            return False

        visited.add(skill_name)
        path.append(skill_name)

        for prereq in all_skills.get(skill_name, []):
            if PrerequisiteChecker._detect_cycle(prereq.skill_name, all_skills, visited, path):
                return True

        path.pop()
        return False
