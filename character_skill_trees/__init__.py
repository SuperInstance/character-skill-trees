"""
Character Skill Trees - Advanced Skill Progression System

A comprehensive skill tree system for AI characters with progression,
specialization paths, mastery levels, and cross-skill synergies.
"""

from .core.skill import AdvancedSkill, SkillCategory
from .core.skill_tree import SkillTree
from .progression.mastery import MasteryLevel, SkillMilestone
from .progression.experience import ExperienceCalculator
from .prerequisites.requirements import SkillPrerequisite, PrerequisiteChecker
from .transfer.synergies import SkillSynergy, SynergyCalculator
from .manager import SkillTreeManager
from .archetypes import ArchetypeSkillTrees

__version__ = "1.0.0"
__author__ = "LucidDreamer Team"

__all__ = [
    # Core classes
    "AdvancedSkill",
    "SkillCategory",
    "SkillTree",

    # Progression
    "MasteryLevel",
    "SkillMilestone",
    "ExperienceCalculator",

    # Prerequisites
    "SkillPrerequisite",
    "PrerequisiteChecker",

    # Transfer effects
    "SkillSynergy",
    "SynergyCalculator",

    # Management
    "SkillTreeManager",
    "ArchetypeSkillTrees",
]
