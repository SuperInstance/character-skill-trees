#!/usr/bin/env python3
"""
Archetype demonstration for Character Skill Trees system.

Shows how to use predefined skill trees for character archetypes.
"""

from character_skill_trees import ArchetypeSkillTrees, SkillTreeManager


def main():
    print("=" * 60)
    print("Character Skill Trees - Archetype Demo")
    print("=" * 60)

    # Create a manager
    manager = SkillTreeManager()

    # Create character
    character_id = "innovator_001"
    archetype = "The Innovator"

    print(f"\nCreating {archetype} skill tree...")

    # Create skill tree for character
    tree = manager.create_tree_for_character(character_id, archetype)

    print(f"\n{tree.name}")
    print(f"Description: {tree.description}")
    print(f"Total Skills: {len(tree.skills)}")
    print(f"Available Points: {tree.available_points}")

    # List all skills
    print("\nSkills in tree:")
    for skill_name, skill in tree.skills.items():
        print(f"\n  {skill_name}")
        print(f"    Category: {skill.category.value}")
        print(f"    Description: {skill.description}")
        print(f"    Level: {skill.current_level}/{skill.max_level}")
        if skill.specializations:
            print(f"    Specializations: {list(skill.specializations.keys())}")

    # Show skill connections
    print("\nSkill Tree Structure:")
    print("  Creative Thinking (Root)")
    print("  ├── Problem Solving")
    print("  │   ├── Research Methodology")
    print("  │   │   └── Systems Thinking")
    print("  │   └── Systems Thinking")
    print("  └── Innovation Management")

    # Practice some skills
    print("\n" + "-" * 60)
    print("Practicing Skills")
    print("-" * 60)

    # Practice creative thinking
    print("\nPracticing Creative Thinking...")
    for i in range(10):
        results = manager.practice_skill(
            character_id=character_id,
            skill_name="Creative Thinking",
            success=(i % 3 != 0),  # 66% success rate
            difficulty=1.2,
            time_spent=30.0
        )

        if results['level_up']:
            print(f"  ⚡ Level up! Now level {results['new_level']:.1f}")

    # Check progress
    creativity = tree.skills["Creative Thinking"]
    print(f"\nCreative Thinking Progress:")
    print(f"  Level: {creativity.current_level:.1f}/{creativity.max_level}")
    print(f"  Mastery: {creativity.mastery_level}")
    print(f"  Success Rate: {creativity.success_rate:.1%}")
    print(f"  Total Uses: {creativity.total_uses}")

    # Level up other skills to unlock prerequisites
    print("\nLeveling up prerequisite skills...")

    tree.skills["Creative Thinking"].current_level = 20.0
    tree.skills["Problem Solving"].current_level = 15.0

    print("  Creative Thinking: 20.0")
    print("  Problem Solving: 15.0")

    # Try to unlock advanced skill
    print("\nAttempting to unlock Innovation Management...")

    can_unlock, reason = tree.can_unlock_skill("Innovation Management")
    print(f"Can unlock: {can_unlock}")
    print(f"Reason: {reason}")

    if can_unlock:
        success = tree.unlock_skill("Innovation Management", point_cost=3)
        if success:
            innovation = tree.skills["Innovation Management"]
            print(f"\n✓ Unlocked Innovation Management!")
            print(f"  Level: {innovation.current_level}")
            print(f"  Remaining points: {tree.available_points}")

    # Get progress summary
    print("\n" + "-" * 60)
    print("Character Progress Summary")
    print("-" * 60)

    summary = manager.get_skill_progress_summary(character_id)

    print(f"\nTotal Trees: {summary['total_trees']}")
    print(f"Total Skills: {summary['total_skills']}")
    print(f"Mastered Skills: {summary['mastered_skills']}")
    print(f"Overall Mastery: {summary['overall_mastery']:.1f}%")

    # Get recommendations
    print("\nSkill Development Recommendations:")

    recommendations = manager.recommend_next_skills(character_id, count=3)

    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['skill_name']}")
        print(f"   Priority: {rec['priority']:.1f}")
        print(f"   Description: {rec['description']}")
        print(f"   Current Level: {rec['current_level']:.1f}")
        print(f"   Can Unlock: {rec['can_unlock']}")

    # Show all archetypes
    print("\n" + "=" * 60)
    print("Available Archetypes")
    print("=" * 60)

    archetypes = [
        ("The Innovator", "Creativity and innovation"),
        ("The Educator", "Teaching and wisdom"),
        ("The Empath", "Emotional intelligence and healing"),
        ("The Engineer", "Technical problem-solving")
    ]

    for name, focus in archetypes:
        print(f"\n{name}")
        print(f"  Focus: {focus}")

    print("\n" + "=" * 60)
    print("Archetype demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
