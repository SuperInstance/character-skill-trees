"""
Pytest fixtures for character-skill-trees tests.
"""

import pytest
from datetime import datetime
from character_skill_trees.core.skill import AdvancedSkill, SkillCategory
from character_skill_trees.core.skill_tree import SkillTree
from character_skill_trees.progression.mastery import MasteryLevel, SkillMilestone
from character_skill_trees.prerequisites.requirements import SkillPrerequisite
from character_skill_trees.transfer.synergies import SkillSynergy


@pytest.fixture
def sample_skill():
    """Create a sample skill for testing."""
    return AdvancedSkill(
        name="Test Skill",
        category=SkillCategory.TECHNICAL,
        description="A skill for testing purposes",
        learning_rate=1.0,
        difficulty=1.0
    )


@pytest.fixture
def novice_skill():
    """Create a novice level skill (level 5)."""
    skill = AdvancedSkill(
        name="Novice Skill",
        category=SkillCategory.COGNITIVE,
        description="A beginner skill",
        current_level=5.0
    )
    return skill


@pytest.fixture
def expert_skill():
    """Create an expert level skill (level 70)."""
    skill = AdvancedSkill(
        name="Expert Skill",
        category=SkillCategory.TECHNICAL,
        description="An expert skill",
        current_level=70.0
    )
    return skill


@pytest.fixture
def master_skill():
    """Create a master level skill (level 90)."""
    skill = AdvancedSkill(
        name="Master Skill",
        category=SkillCategory.WISDOM,
        description="A master skill",
        current_level=90.0
    )
    return skill


@pytest.fixture
def skill_with_specializations():
    """Create a skill with multiple specializations."""
    skill = AdvancedSkill(
        name="Programming",
        category=SkillCategory.TECHNICAL,
        description="Programming skill with specializations",
        current_level=25.0
    )
    skill.add_specialization("python", 5.0)
    skill.add_specialization("javascript", 3.0)
    skill.add_specialization("systems_design", 2.0)
    return skill


@pytest.fixture
def skill_with_prerequisites():
    """Create a skill with prerequisites."""
    skill = AdvancedSkill(
        name="Advanced Programming",
        category=SkillCategory.TECHNICAL,
        description="Advanced programming requiring basics",
        current_level=0.0
    )
    skill.prerequisites = [
        SkillPrerequisite("Basic Programming", 20.0),
        SkillPrerequisite("Data Structures", 15.0, optional=False)
    ]
    return skill


@pytest.fixture
def skill_with_synergies():
    """Create a skill with synergies."""
    skill = AdvancedSkill(
        name="System Architecture",
        category=SkillCategory.TECHNICAL,
        description="Architecture skill with synergies",
        current_level=30.0
    )
    skill.synergies = [
        SkillSynergy("System Architecture", "Database Design", "experience", 1.5, 20.0),
        SkillSynergy("System Architecture", "Network Engineering", "level", 0.2, 15.0)
    ]
    return skill


@pytest.fixture
def skill_with_milestones():
    """Create a skill with milestones."""
    skill = AdvancedSkill(
        name="Leadership",
        category=SkillCategory.LEADERSHIP,
        description="Leadership skill with milestones",
        current_level=35.0
    )
    skill.milestones = [
        SkillMilestone(10.0, "Team Lead", "Can lead small teams",
                      ["team_leadership"], {"team_size": 5}),
        SkillMilestone(25.0, "Department Lead", "Can lead departments",
                      ["dept_leadership"], {"team_size": 20}),
        SkillMilestone(50.0, "Executive", "Can lead organizations",
                      ["executive_leadership"], {"team_size": 100})
    ]
    return skill


@pytest.fixture
def skill_categories():
    """Provide all skill categories for testing."""
    return list(SkillCategory)


@pytest.fixture
def skill_tree():
    """Create a basic skill tree."""
    tree = SkillTree(
        name="Test Tree",
        description="A test skill tree",
        available_points=10
    )

    # Add root skill
    root = AdvancedSkill(
        name="Root Skill",
        category=SkillCategory.TECHNICAL,
        description="Root of the tree"
    )
    tree.add_skill(root)

    # Add intermediate skills
    intermediate1 = AdvancedSkill(
        name="Intermediate Skill 1",
        category=SkillCategory.TECHNICAL,
        description="First intermediate skill"
    )
    intermediate1.prerequisites = [
        SkillPrerequisite("Root Skill", 10.0)
    ]
    tree.add_skill(intermediate1, ["Root Skill"])

    intermediate2 = AdvancedSkill(
        name="Intermediate Skill 2",
        category=SkillCategory.COGNITIVE,
        description="Second intermediate skill"
    )
    intermediate2.prerequisites = [
        SkillPrerequisite("Root Skill", 10.0)
    ]
    tree.add_skill(intermediate2, ["Root Skill"])

    # Add advanced skill
    advanced = AdvancedSkill(
        name="Advanced Skill",
        category=SkillCategory.WISDOM,
        description="Advanced skill requiring both intermediates"
    )
    advanced.prerequisites = [
        SkillPrerequisite("Intermediate Skill 1", 20.0),
        SkillPrerequisite("Intermediate Skill 2", 20.0)
    ]
    tree.add_skill(advanced, ["Intermediate Skill 1", "Intermediate Skill 2"])

    return tree


@pytest.fixture
def skill_tree_with_synergies():
    """Create a skill tree with synergies between skills."""
    tree = SkillTree(
        name="Synergy Tree",
        description="Tree with skill synergies"
    )

    skill1 = AdvancedSkill(
        name="Design",
        category=SkillCategory.CREATIVE,
        description="Design skill",
        current_level=30.0
    )

    skill2 = AdvancedSkill(
        name="Development",
        category=SkillCategory.TECHNICAL,
        description="Development skill",
        current_level=25.0
    )

    skill3 = AdvancedSkill(
        name="Testing",
        category=SkillCategory.TECHNICAL,
        description="Testing skill",
        current_level=20.0
    )

    # Add synergies
    skill1.synergies = [
        SkillSynergy("Design", "Development", "experience", 1.2, 15.0)
    ]

    skill2.synergies = [
        SkillSynergy("Development", "Testing", "success_rate", 0.1, 10.0)
    ]

    tree.add_skill(skill1)
    tree.add_skill(skill2, ["Design"])
    tree.add_skill(skill3, ["Development"])

    return tree


@pytest.fixture
def prerequisite_chain():
    """Create a chain of prerequisites."""
    return {
        "Skill A": [],
        "Skill B": [SkillPrerequisite("Skill A", 10.0)],
        "Skill C": [
            SkillPrerequisite("Skill A", 15.0),
            SkillPrerequisite("Skill B", 10.0)
        ],
        "Skill D": [SkillPrerequisite("Skill C", 20.0)]
    }


@pytest.fixture
def synergy_list():
    """Create a list of synergies for testing."""
    return [
        SkillSynergy("Skill A", "Skill B", "experience", 1.5, 10.0),
        SkillSynergy("Skill A", "Skill C", "level", 0.2, 15.0),
        SkillSynergy("Skill B", "Skill C", "success_rate", 0.1, 20.0)
    ]


@pytest.fixture
def skill_levels():
    """Provide a dictionary of skill levels for testing."""
    return {
        "Skill A": 25.0,
        "Skill B": 20.0,
        "Skill C": 15.0,
        "Skill D": 5.0
    }


@pytest.fixture
def mastery_levels():
    """Provide all mastery levels for testing."""
    return [
        MasteryLevel.NOVICE,
        MasteryLevel.APPRENTICE,
        MasteryLevel.JOURNEYMAN,
        MasteryLevel.EXPERT,
        MasteryLevel.MASTER,
        MasteryLevel.GRANDMASTER
    ]


@pytest.fixture
def milestone_list():
    """Create a list of milestones for testing."""
    return [
        SkillMilestone(10.0, "First Milestone", "Reach level 10",
                      ["unlock_1"], {"reward_1": 100}),
        SkillMilestone(25.0, "Second Milestone", "Reach level 25",
                      ["unlock_2"], {"reward_2": 250}),
        SkillMilestone(50.0, "Third Milestone", "Reach level 50",
                      ["unlock_3"], {"reward_3": 500})
    ]
