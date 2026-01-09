"""
Skill Tree Manager for character development and tracking.
"""

import uuid
import logging
from typing import Dict, List, Any

from .core.skill import AdvancedSkill, SkillCategory
from .core.skill_tree import SkillTree
from .progression.mastery import SkillMilestone
from .progression.experience import ExperienceCalculator
from .prerequisites.requirements import SkillPrerequisite
from .transfer.synergies import SkillSynergy

logger = logging.getLogger(__name__)


class SkillTreeManager:
    """Manages skill trees for character development"""

    def __init__(self):
        self.skill_trees: Dict[str, SkillTree] = {}
        self.character_trees: Dict[str, List[str]] = {}  # character_id -> list of tree_ids
        self.global_skill_registry: Dict[str, AdvancedSkill] = {}  # Global skill database

    def create_tree_for_character(self, character_id: str, archetype: str) -> SkillTree:
        """Create appropriate skill tree for character archetype"""
        from .archetypes import ArchetypeSkillTrees

        tree_creators = {
            "The Innovator": ArchetypeSkillTrees.create_innovator_tree,
            "The Educator": ArchetypeSkillTrees.create_educator_tree,
            "The Empath": ArchetypeSkillTrees.create_empath_tree,
            "The Engineer": ArchetypeSkillTrees.create_engineer_tree,
        }

        creator = tree_creators.get(archetype, ArchetypeSkillTrees.create_innovator_tree)
        tree = creator()

        tree_id = str(uuid.uuid4())
        self.skill_trees[tree_id] = tree

        if character_id not in self.character_trees:
            self.character_trees[character_id] = []
        self.character_trees[character_id].append(tree_id)

        # Register skills globally
        for skill in tree.skills.values():
            self.global_skill_registry[skill.name] = skill

        logger.info(f"Created {tree.name} for character {character_id}")
        return tree

    def get_character_trees(self, character_id: str) -> List[SkillTree]:
        """Get all skill trees for a character"""
        if character_id not in self.character_trees:
            return []

        return [self.skill_trees[tree_id] for tree_id in self.character_trees[character_id]]

    def practice_skill(self, character_id: str, skill_name: str,
                      success: bool, difficulty: float, time_spent: float) -> Dict[str, Any]:
        """Practice a skill and return results"""
        results = {
            'skill_name': skill_name,
            'success': success,
            'experience_gained': 0,
            'level_up': False,
            'new_level': 0,
            'specialization_improvement': 0
        }

        # Find the skill in character's trees
        trees = self.get_character_trees(character_id)
        target_skill = None

        for tree in trees:
            if skill_name in tree.skills:
                target_skill = tree.skills[skill_name]
                break

        if not target_skill:
            logger.warning(f"Skill {skill_name} not found for character {character_id}")
            return results

        # Calculate experience gain
        base_experience = ExperienceCalculator.calculate_experience_gain(
            success, difficulty, time_spent, target_skill.learning_rate
        )

        # Add experience
        leveled_up, new_level = target_skill.add_experience(base_experience)

        results.update({
            'experience_gained': base_experience,
            'level_up': leveled_up,
            'new_level': new_level
        })

        # Practice specialization if applicable
        if target_skill.current_specialization:
            spec_improvement = target_skill.practice_specialization(
                target_skill.current_specialization, success
            )
            results['specialization_improvement'] = spec_improvement

        return results

    def get_skill_progress_summary(self, character_id: str) -> Dict[str, Any]:
        """Get comprehensive skill progress summary for character"""
        trees = self.get_character_trees(character_id)

        if not trees:
            return {'error': 'No skill trees found for character'}

        summary = {
            'character_id': character_id,
            'total_trees': len(trees),
            'tree_statistics': [],
            'total_skills': 0,
            'mastered_skills': 0,
            'total_specializations': 0,
            'available_points': 0,
            'overall_mastery': 0.0
        }

        for tree in trees:
            stats = tree.get_tree_statistics()
            summary['tree_statistics'].append(stats)
            summary['total_skills'] += stats['total_skills']
            summary['mastered_skills'] += stats['mastered_skills']
            summary['total_specializations'] += stats['total_specializations']
            summary['available_points'] += stats['available_points']
            summary['overall_mastery'] += stats['overall_mastery']

        # Calculate averages
        if len(trees) > 0:
            summary['overall_mastery'] /= len(trees)

        return summary

    def recommend_next_skills(self, character_id: str, count: int = 5) -> List[Dict[str, Any]]:
        """Recommend next skills to learn based on current progress"""
        trees = self.get_character_trees(character_id)
        recommendations = []

        for tree in trees:
            for skill_name, skill in tree.skills.items():
                if skill.current_level < 5.0:  # Focus on underdeveloped skills
                    can_unlock, reason = tree.can_unlock_skill(skill_name)

                    if can_unlock or skill.current_level > 0:
                        # Calculate priority based on prerequisites and utility
                        priority = self._calculate_skill_priority(tree, skill_name)

                        recommendations.append({
                            'skill_name': skill_name,
                            'current_level': skill.current_level,
                            'can_unlock': can_unlock,
                            'reason': reason,
                            'priority': priority,
                            'tree_name': tree.name,
                            'category': skill.category.value,
                            'description': skill.description
                        })

        # Sort by priority and return top recommendations
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        return recommendations[:count]

    def _calculate_skill_priority(self, tree: SkillTree, skill_name: str) -> float:
        """Calculate priority score for a skill"""
        skill = tree.skills[skill_name]
        priority = 0.0

        # Lower level skills get higher priority
        priority += (10.0 - skill.current_level) * 0.5

        # Skills that unlock other abilities get priority
        dependent_count = len([s for s in tree.skills.values()
                             if any(prereq.skill_name == skill_name for prereq in s.prerequisites)])
        priority += dependent_count * 2.0

        # Core skills get priority
        if 'core' in skill.tags:
            priority += 3.0

        # Synergistic skills get priority
        synergy_count = len(skill.synergies)
        priority += synergy_count * 1.0

        return priority

    def unlock_skill_for_character(self, character_id: str, tree_id: str,
                                 skill_name: str) -> Dict[str, Any]:
        """Unlock a skill for a character"""
        if tree_id not in self.skill_trees:
            return {'success': False, 'reason': 'Tree not found'}

        tree = self.skill_trees[tree_id]

        if character_id not in self.character_trees or tree_id not in self.character_trees[character_id]:
            return {'success': False, 'reason': 'Tree not assigned to character'}

        success = tree.unlock_skill(skill_name)

        if success:
            return {
                'success': True,
                'skill_name': skill_name,
                'new_level': tree.skills[skill_name].current_level,
                'remaining_points': tree.available_points
            }
        else:
            can_unlock, reason = tree.can_unlock_skill(skill_name)
            return {'success': False, 'reason': reason}

    def to_dict(self) -> Dict[str, Any]:
        """Convert manager state to dictionary"""
        return {
            'total_trees': len(self.skill_trees),
            'total_characters': len(self.character_trees),
            'registered_skills': len(self.global_skill_registry),
            'skill_trees': {tid: tree.to_dict() for tid, tree in self.skill_trees.items()},
            'character_trees': self.character_trees
        }
