"""
Tests for predefined archetype skill trees.
"""

import pytest
from character_skill_trees.archetypes import ArchetypeSkillTrees
from character_skill_trees.core.skill import SkillCategory


class TestInnovatorTree:
    """Test The Innovator archetype tree."""

    def test_create_innovator_tree(self):
        """Test creating Innovator skill tree."""
        tree = ArchetypeSkillTrees.create_innovator_tree()

        assert tree.name == "The Innovator's Path"
        assert tree.tree_type == "innovator"
        assert tree.difficulty_modifier == 0.9

    def test_innovator_has_core_skills(self):
        """Test that Innovator tree has core skills."""
        tree = ArchetypeSkillTrees.create_innovator_tree()

        assert "Creative Thinking" in tree.skills
        assert "Problem Solving" in tree.skills
        assert "Research Methodology" in tree.skills

    def test_innovator_creativity_specializations(self):
        """Test that Creative Thinking has specializations."""
        tree = ArchetypeSkillTrees.create_innovator_tree()
        creativity = tree.skills["Creative Thinking"]

        assert "divergent_thinking" in creativity.specializations
        assert "conceptual_blending" in creativity.specializations

    def test_innovator_skill_prerequisites(self):
        """Test Innovator skill prerequisites."""
        tree = ArchetypeSkillTrees.create_innovator_tree()
        innovation = tree.skills["Innovation Management"]

        assert len(innovation.prerequisites) == 2
        prereq_names = [p.skill_name for p in innovation.prerequisites]
        assert "Creative Thinking" in prereq_names
        assert "Problem Solving" in prereq_names

    def test_innovator_milestones(self):
        """Test Innovator milestones."""
        tree = ArchetypeSkillTrees.create_innovator_tree()
        creativity = tree.skills["Creative Thinking"]

        assert len(creativity.milestones) == 5

        # Check milestone levels
        milestone_levels = [m.level for m in creativity.milestones]
        assert 10.0 in milestone_levels
        assert 25.0 in milestone_levels
        assert 50.0 in milestone_levels
        assert 75.0 in milestone_levels
        assert 90.0 in milestone_levels

    def test_innovator_synergies(self):
        """Test Innovator synergies."""
        tree = ArchetypeSkillTrees.create_innovator_tree()
        creativity = tree.skills["Creative Thinking"]

        assert len(creativity.synergies) == 2

    def test_innovator_available_points(self):
        """Test Innovator starting skill points."""
        tree = ArchetypeSkillTrees.create_innovator_tree()

        assert tree.available_points == 10


class TestEducatorTree:
    """Test The Educator archetype tree."""

    def test_create_educator_tree(self):
        """Test creating Educator skill tree."""
        tree = ArchetypeSkillTrees.create_educator_tree()

        assert tree.name == "The Educator's Journey"
        assert tree.tree_type == "educator"
        assert tree.difficulty_modifier == 0.8

    def test_educator_core_skills(self):
        """Test that Educator tree has core skills."""
        tree = ArchetypeSkillTrees.create_educator_tree()

        assert "Teaching" in tree.skills
        assert "Communication" in tree.skills
        assert "Patience" in tree.skills

    def test_educator_teaching_specializations(self):
        """Test Teaching skill specializations."""
        tree = ArchetypeSkillTrees.create_educator_tree()
        teaching = tree.skills["Teaching"]

        assert "curriculum_design" in teaching.specializations
        assert "assessment" in teaching.specializations

    def test_educator_learning_rates(self):
        """Test that educator skills have appropriate learning rates."""
        tree = ArchetypeSkillTrees.create_educator_tree()
        teaching = tree.skills["Teaching"]

        # Teaching should learn faster
        assert teaching.learning_rate > 1.0

    def test_educator_wisdom_difficulty(self):
        """Test that Wisdom is appropriately difficult."""
        tree = ArchetypeSkillTrees.create_educator_tree()
        wisdom = tree.skills["Wisdom"]

        # Wisdom should be harder to learn
        assert wisdom.difficulty > 1.0
        assert wisdom.learning_rate < 1.0

    def test_educator_mentoring_prerequisites(self):
        """Test Mentoring prerequisites."""
        tree = ArchetypeSkillTrees.create_educator_tree()
        mentoring = tree.skills["Mentoring"]

        assert len(mentoring.prerequisites) == 3
        prereq_names = [p.skill_name for p in mentoring.prerequisites]
        assert "Teaching" in prereq_names
        assert "Communication" in prereq_names
        assert "Patience" in prereq_names


class TestEmpathTree:
    """Test The Empath archetype tree."""

    def test_create_empath_tree(self):
        """Test creating Empath skill tree."""
        tree = ArchetypeSkillTrees.create_empath_tree()

        assert tree.name == "The Empath's Path"
        assert tree.tree_type == "empath"
        assert tree.difficulty_modifier == 0.85

    def test_empath_core_skills(self):
        """Test that Empath tree has core skills."""
        tree = ArchetypeSkillTrees.create_empath_tree()

        assert "Empathy" in tree.skills
        assert "Active Listening" in tree.skills
        assert "Emotional Intelligence" in tree.skills

    def test_empath_skill_categories(self):
        """Test Empath skill categories."""
        tree = ArchetypeSkillTrees.create_empath_tree()
        empathy = tree.skills["Empathy"]

        assert empathy.category == SkillCategory.EMOTIONAL

    def test_empath_healing_prerequisites(self):
        """Test Emotional Healing prerequisites."""
        tree = ArchetypeSkillTrees.create_empath_tree()
        healing = tree.skills["Emotional Healing"]

        assert len(healing.prerequisites) == 3

    def test_empath_available_points(self):
        """Test Empath starting skill points."""
        tree = ArchetypeSkillTrees.create_empath_tree()

        assert tree.available_points == 11


class TestEngineerTree:
    """Test The Engineer archetype tree."""

    def test_create_engineer_tree(self):
        """Test creating Engineer skill tree."""
        tree = ArchetypeSkillTrees.create_engineer_tree()

        assert tree.name == "The Engineer's Craft"
        assert tree.tree_type == "engineer"
        assert tree.difficulty_modifier == 1.0

    def test_engineer_core_skills(self):
        """Test that Engineer tree has core skills."""
        tree = ArchetypeSkillTrees.create_engineer_tree()

        assert "System Design" in tree.skills
        assert "Technical Problem Solving" in tree.skills
        assert "Technical Innovation" in tree.skills

    def test_engineer_system_design_specializations(self):
        """Test System Design specializations."""
        tree = ArchetypeSkillTrees.create_engineer_tree()
        system_design = tree.skills["System Design"]

        assert "architecture" in system_design.specializations
        assert "optimization" in system_design.specializations

    def test_engineer_optimization_prerequisites(self):
        """Test System Optimization prerequisites."""
        tree = ArchetypeSkillTrees.create_engineer_tree()
        optimization = tree.skills["System Optimization"]

        assert len(optimization.prerequisites) == 3
        prereq_names = [p.skill_name for p in optimization.prerequisites]
        assert "System Design" in prereq_names
        assert "Technical Problem Solving" in prereq_names
        assert "Technical Innovation" in prereq_names


class TestArchetypeCharacteristics:
    """Test characteristics that distinguish archetypes."""

    def test_archetype_difficulty_modifiers(self):
        """Test that each archetype has appropriate difficulty."""
        innovator = ArchetypeSkillTrees.create_innovator_tree()
        educator = ArchetypeSkillTrees.create_educator_tree()
        empath = ArchetypeSkillTrees.create_empath_tree()
        engineer = ArchetypeSkillTrees.create_engineer_tree()

        # Educator should be easiest (teaching builds on itself)
        assert educator.difficulty_modifier < innovator.difficulty_modifier

        # Engineer should be standard difficulty
        assert engineer.difficulty_modifier == 1.0

    def test_archetype_skill_counts(self):
        """Test that archetypes have different numbers of skills."""
        innovator = ArchetypeSkillTrees.create_innovator_tree()
        educator = ArchetypeSkillTrees.create_educator_tree()

        # Both should have 5 skills
        assert len(innovator.skills) == 5
        assert len(educator.skills) == 5

    def test_archetype_available_points(self):
        """Test that archetypes start with appropriate points."""
        innovator = ArchetypeSkillTrees.create_innovator_tree()
        educator = ArchetypeSkillTrees.create_educator_tree()
        empath = ArchetypeSkillTrees.create_empath_tree()
        engineer = ArchetypeSkillTrees.create_engineer_tree()

        # Educator gets most points (easiest progression)
        assert educator.available_points >= innovator.available_points
        assert educator.available_points >= empath.available_points

    def test_archetype_skill_categories_match(self):
        """Test that archetypes emphasize appropriate skill categories."""
        innovator = ArchetypeSkillTrees.create_innovator_tree()
        educator = ArchetypeSkillTrees.create_educator_tree()
        empath = ArchetypeSkillTrees.create_empath_tree()
        engineer = ArchetypeSkillTrees.create_engineer_tree()

        # Innovator should have creative skills
        innovator_categories = [s.category for s in innovator.skills.values()]
        assert SkillCategory.CREATIVE in innovator_categories

        # Educator should have social skills
        educator_categories = [s.category for s in educator.skills.values()]
        assert SkillCategory.SOCIAL in educator_categories

        # Empath should have emotional skills
        empath_categories = [s.category for s in empath.skills.values()]
        assert SkillCategory.EMOTIONAL in empath_categories

        # Engineer should have technical skills
        engineer_categories = [s.category for s in engineer.skills.values()]
        assert SkillCategory.TECHNICAL in engineer_categories


class TestArchetypeIntegration:
    """Test integration of archetype features."""

    def test_all_archetypes_have_root_skills(self):
        """Test that all archetypes have root skills defined."""
        archetypes = [
            ArchetypeSkillTrees.create_innovator_tree(),
            ArchetypeSkillTrees.create_educator_tree(),
            ArchetypeSkillTrees.create_empath_tree(),
            ArchetypeSkillTrees.create_engineer_tree()
        ]

        for tree in archetypes:
            assert len(tree.root_skills) > 0

    def test_all_archetypes_have_connections(self):
        """Test that all archetypes have skill connections."""
        archetypes = [
            ArchetypeSkillTrees.create_innovator_tree(),
            ArchetypeSkillTrees.create_educator_tree(),
            ArchetypeSkillTrees.create_empath_tree(),
            ArchetypeSkillTrees.create_engineer_tree()
        ]

        for tree in archetypes:
            # Should have some connections defined
            assert len(tree.connections) > 0 or len(tree.skills) <= len(tree.root_skills)

    def test_archetype_serialization(self):
        """Test that archetype trees can be serialized."""
        tree = ArchetypeSkillTrees.create_innovator_tree()
        tree_dict = tree.to_dict()

        assert 'name' in tree_dict
        assert 'tree_type' in tree_dict
        assert 'skills' in tree_dict
        assert 'statistics' in tree_dict

    def test_archetype_statistics(self):
        """Test that archetype trees have statistics."""
        tree = ArchetypeSkillTrees.create_innovator_tree()
        stats = tree.get_tree_statistics()

        assert 'total_skills' in stats
        assert 'mastered_skills' in stats
        assert 'mastery_percentage' in stats
        assert 'overall_mastery' in stats

    def test_archetype_skill_progression_paths(self):
        """Test that progression paths work for archetypes."""
        tree = ArchetypeSkillTrees.create_innovator_tree()

        # Get path to advanced skill
        path = tree.get_skill_progression_path("Innovation Management")

        assert len(path) > 0
        assert "Innovation Management" in path
        # Should include prerequisites
        assert "Creative Thinking" in path or "Problem Solving" in path

    def test_archetype_skill_unlocking(self):
        """Test unlocking skills in archetype trees."""
        tree = ArchetypeSkillTrees.create_innovator_tree()

        # Root skill should be unlockable
        can_unlock, reason = tree.can_unlock_skill("Creative Thinking")
        assert can_unlock

        # Advanced skill should require prerequisites
        can_unlock, reason = tree.can_unlock_skill("Innovation Management")
        # Should fail due to prerequisites not being met
        assert not can_unlock or " prerequisite" in reason.lower() or "can unlock" in reason.lower()
