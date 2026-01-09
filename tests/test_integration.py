"""
Integration tests for complete skill tree workflows.
"""

import pytest
from character_skill_trees.core.skill import AdvancedSkill, SkillCategory
from character_skill_trees.core.skill_tree import SkillTree
from character_skill_trees.progression.mastery import SkillMilestone
from character_skill_trees.prerequisites.requirements import SkillPrerequisite
from character_skill_trees.transfer.synergies import SkillSynergy
from character_skill_trees.archetypes import ArchetypeSkillTrees


class TestSkillTreeWorkflow:
    """Test complete skill tree workflows."""

    def test_create_and_populate_tree(self):
        """Test creating a skill tree and populating it."""
        tree = SkillTree(
            name="Integration Test Tree",
            description="Testing complete workflow",
            available_points=5
        )

        # Add root skill
        root = AdvancedSkill(
            name="Root Skill",
            category=SkillCategory.TECHNICAL,
            description="Base skill"
        )
        tree.add_skill(root)

        # Add child skill
        child = AdvancedSkill(
            name="Child Skill",
            category=SkillCategory.COGNITIVE,
            description="Dependent skill"
        )
        child.prerequisites = [SkillPrerequisite("Root Skill", 10.0)]
        tree.add_skill(child, ["Root Skill"])

        assert len(tree.skills) == 2
        assert "Root Skill" in tree.root_skills

    def test_skill_progression_workflow(self, skill_tree):
        """Test complete skill progression workflow."""
        root_skill = skill_tree.skills["Root Skill"]

        # Add experience
        for _ in range(15):
            root_skill.add_experience(100)

        # Should have leveled up
        assert root_skill.current_level > 0

        # Now can unlock intermediate skill
        can_unlock, _ = skill_tree.can_unlock_skill("Intermediate Skill 1")
        assert can_unlock

    def test_skill_unlock_workflow(self, skill_tree):
        """Test unlocking skills in the tree."""
        # Level up root skill
        root = skill_tree.skills["Root Skill"]
        root.add_experience(1000)  # Enough to reach level 10+

        # Unlock intermediate skill
        success = skill_tree.unlock_skill("Intermediate Skill 1")
        assert success

        # Check points were deducted
        assert skill_tree.total_points_spent > 0

    def test_complete_skill_journey(self):
        """Test a complete journey from novice to expert."""
        # Create skill
        skill = AdvancedSkill(
            name="Complete Journey",
            category=SkillCategory.WISDOM,
            description="Test full progression",
            learning_rate=1.0,
            difficulty=1.0
        )

        # Add milestones
        skill.milestones = [
            SkillMilestone(20.0, "Apprentice", "Reach apprentice", [], {}),
            SkillMilestone(50.0, "Expert", "Reach expert", [], {}),
            SkillMilestone(80.0, "Master", "Reach master", [], {})
        ]

        # Progress through levels
        mastery_levels = []
        for _ in range(85):
            leveled_up, _ = skill.add_experience(1000)
            if leveled_up:
                mastery_levels.append(skill.mastery_level)

        # Should have progressed through multiple mastery levels
        assert len(set(mastery_levels)) > 1
        assert skill.current_level >= 80.0

    def test_prerequisite_unlock_workflow(self, skill_tree):
        """Test unlocking through prerequisite chain."""
        # Start from root
        root = skill_tree.skills["Root Skill"]

        # Level up root to meet prerequisite
        root.add_experience(2000)  # Should reach level 10+

        # Unlock first intermediate
        assert skill_tree.unlock_skill("Intermediate Skill 1")

        # Level up intermediate
        intermediate1 = skill_tree.skills["Intermediate Skill 1"]
        intermediate1.add_experience(3000)  # Should reach level 20+

        # Can now unlock advanced
        can_unlock, _ = skill_tree.can_unlock_skill("Advanced Skill")
        # May still need Intermediate Skill 2
        # Let's level that too
        intermediate2 = skill_tree.skills["Intermediate Skill 2"]
        intermediate2.current_level = 20.0

        can_unlock, _ = skill_tree.can_unlock_skill("Advanced Skill")
        assert can_unlock


class TestSpecializationWorkflow:
    """Test specialization workflows."""

    def test_specialization_unlock_workflow(self):
        """Test unlocking and using specializations."""
        skill = AdvancedSkill(
            name="Specialization Test",
            category=SkillCategory.TECHNICAL,
            description="Testing specializations"
        )

        # Level up to 20
        skill.add_experience(5000)

        assert skill.current_level >= 20.0

        # Can now specialize
        result = skill.add_specialization("advanced_techniques", 3.0)
        assert result

        assert "advanced_techniques" in skill.specializations

        # Practice specialization
        improvement = skill.practice_specialization("advanced_techniques", True)
        assert improvement > 0

    def test_multiple_specializations_workflow(self):
        """Test developing multiple specializations."""
        skill = AdvancedSkill(
            name="Multi-Spec",
            category=SkillCategory.CREATIVE,
            description="Multiple specializations"
        )

        skill.add_experience(10000)  # Level up significantly

        # Add multiple specializations
        skill.add_specialization("spec1", 1.0)
        skill.add_specialization("spec2", 1.0)
        skill.add_specialization("spec3", 1.0)

        assert len(skill.specializations) == 3

        # Practice all
        for spec_name in skill.specializations:
            skill.practice_specialization(spec_name, True)

        # All should have improved
        for level in skill.specializations.values():
            assert level > 1.0


class TestSynergyWorkflow:
    """Test synergy activation and bonus workflows."""

    def test_synergy_activation_workflow(self):
        """Test activating synergies through skill development."""
        # Create two skills with synergy
        skill1 = AdvancedSkill(
            name="Primary Skill",
            category=SkillCategory.TECHNICAL,
            description="Primary skill"
        )

        skill2 = AdvancedSkill(
            name="Secondary Skill",
            category=SkillCategory.TECHNICAL,
            description="Secondary skill"
        )

        # Create synergy
        synergy = SkillSynergy("Primary Skill", "Secondary Skill", "experience", 1.5, 20.0)
        skill1.synergies = [synergy]

        # Initially not active
        skill_levels = {
            "Primary Skill": skill1.current_level,
            "Secondary Skill": skill2.current_level
        }

        assert not synergy.is_active(skill1.current_level, skill2.current_level)

        # Level up both skills
        skill1.add_experience(50000)
        skill2.add_experience(50000)

        skill_levels = {
            "Primary Skill": skill1.current_level,
            "Secondary Skill": skill2.current_level
        }

        # Should now be active
        assert synergy.is_active(skill1.current_level, skill2.current_level)

    def test_synergy_bonus_application(self):
        """Test applying synergy bonuses."""
        from character_skill_trees.transfer.synergies import SynergyCalculator

        skill1 = AdvancedSkill(
            name="Skill A",
            category=SkillCategory.COGNITIVE,
            description="Skill A"
        )

        skill2 = AdvancedSkill(
            name="Skill B",
            category=SkillCategory.SOCIAL,
            description="Skill B"
        )

        synergy = SkillSynergy("Skill A", "Skill B", "experience", 2.0, 15.0)
        skill1.synergies = [synergy]

        # Level up both
        skill1.add_experience(30000)
        skill2.add_experience(30000)

        skill_levels = {
            "Skill A": skill1.current_level,
            "Skill B": skill2.current_level
        }

        # Calculate bonus
        bonus = SynergyCalculator.calculate_total_synergy_bonus(
            "Skill A",
            [synergy],
            skill_levels
        )

        assert bonus > 0


class TestArchetypeWorkflow:
    """Test complete archetype workflows."""

    def test_educator_progression_workflow(self):
        """Test progressing through Educator tree."""
        tree = ArchetypeSkillTrees.create_educator_tree()

        # Start with teaching
        teaching = tree.skills["Teaching"]
        teaching.add_experience(5000)

        # Should be able to unlock communication
        can_unlock, _ = tree.can_unlock_skill("Communication")
        assert can_unlock

        # Unlock and progress
        tree.unlock_skill("Communication")
        communication = tree.skills["Communication"]
        communication.add_experience(5000)

        # Check mastery
        assert teaching.mastery_level in ["Apprentice", "Journeyman", "Expert"]

    def test_innovator_complete_workflow(self):
        """Test complete Innovator progression."""
        tree = ArchetypeSkillTrees.create_innovator_tree()

        # Progress through core skills
        creativity = tree.skills["Creative Thinking"]
        problem_solving = tree.skills["Problem Solving"]

        # Add significant experience
        for _ in range(20):
            creativity.add_experience(500)
            problem_solving.add_experience(500)

        # Check if prerequisites for Innovation Management are met
        innovation = tree.skills["Innovation Management"]
        skill_levels = {
            "Creative Thinking": creativity.current_level,
            "Problem Solving": problem_solving.current_level
        }

        from character_skill_trees.prerequisites.requirements import PrerequisiteChecker
        all_met, _ = PrerequisiteChecker.check_prerequisites(
            innovation.prerequisites,
            skill_levels
        )

        # With enough experience, should meet prerequisites
        if creativity.current_level >= 15.0 and problem_solving.current_level >= 10.0:
            assert all_met

    def test_multiple_archetypes_comparison(self):
        """Test comparing progression across archetypes."""
        innovator = ArchetypeSkillTrees.create_innovator_tree()
        engineer = ArchetypeSkillTrees.create_engineer_tree()

        # Get root skills
        innovator_root = innovator.skills[innovator.root_skills[0]]
        engineer_root = engineer.skills[engineer.root_skills[0]]

        # Add same experience to both
        for _ in range(10):
            innovator_root.add_experience(500)
            engineer_root.add_experience(500)

        # Check mastery levels
        innovator_mastery = innovator_root.mastery_level
        engineer_mastery = engineer_root.mastery_level

        # Both should have progressed
        assert innovator_root.current_level > 0
        assert engineer_root.current_level > 0


class TestSerializationWorkflow:
    """Test serialization and deserialization workflows."""

    def test_skill_serialization_workflow(self, sample_skill):
        """Test complete skill serialization workflow."""
        # Add some data
        sample_skill.add_experience(500)
        sample_skill.tags.add("test_tag")
        sample_skill.add_specialization("test_spec", 2.0)

        # Serialize
        skill_dict = sample_skill.to_dict()

        # Verify all data is present
        assert skill_dict['name'] == sample_skill.name
        assert skill_dict['current_level'] == sample_skill.current_level
        assert "test_tag" in skill_dict['tags']
        assert "test_spec" in skill_dict['specializations']

    def test_tree_serialization_workflow(self, skill_tree):
        """Test complete tree serialization workflow."""
        # Serialize
        tree_dict = skill_tree.to_dict()

        # Verify structure
        assert 'name' in tree_dict
        assert 'skills' in tree_dict
        assert 'connections' in tree_dict
        assert 'statistics' in tree_dict

        # Check statistics
        stats = tree_dict['statistics']
        assert stats['total_skills'] == len(skill_tree.skills)


class TestErrorHandlingWorkflow:
    """Test error handling in various workflows."""

    def test_unlock_without_prerequisites(self, skill_tree):
        """Test attempting to unlock without meeting prerequisites."""
        # Try to unlock advanced skill immediately
        success = skill_tree.unlock_skill("Advanced Skill")

        # Should fail
        assert not success

    def test_unlock_without_points(self, skill_tree):
        """Test attempting to unlock without sufficient points."""
        # Use up all points
        skill_tree.available_points = 0

        # Try to unlock
        success = skill_tree.unlock_skill("Root Skill")

        # Should fail
        assert not success

    def test_specialize_before_level_20(self, sample_skill):
        """Test specializing before level 20."""
        # Try to specialize at low level
        result = sample_skill.add_specialization("early_spec", 1.0)

        # Should fail
        assert not result


class TestStatisticsWorkflow:
    """Test statistics calculation workflows."""

    def test_tree_statistics_workflow(self, skill_tree):
        """Test calculating tree statistics."""
        stats = skill_tree.get_tree_statistics()

        assert stats['total_skills'] == len(skill_tree.skills)
        assert 'mastery_percentage' in stats
        assert 'overall_mastery' in stats

    def test_mastery_calculation_workflow(self, skill_tree):
        """Test overall mastery calculation."""
        mastery = skill_tree.calculate_mastery_level()

        assert 0.0 <= mastery <= 100.0

    def test_progression_path_workflow(self, skill_tree):
        """Test getting progression path."""
        path = skill_tree.get_skill_progression_path("Advanced Skill")

        # Should include prerequisites
        assert "Advanced Skill" in path
        assert len(path) > 1
