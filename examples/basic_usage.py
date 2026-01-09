#!/usr/bin/env python3
"""
Basic usage example for Character Skill Trees system.

Demonstrates fundamental operations including creating skills,
adding experience, and tracking progression.
"""

from character_skill_trees import (
    AdvancedSkill,
    SkillCategory,
    SkillTree,
    MasteryLevel
)


def main():
    print("=" * 60)
    print("Character Skill Trees - Basic Usage Example")
    print("=" * 60)

    # Create a custom skill
    print("\n1. Creating a custom skill...")
    swordsmanship = AdvancedSkill(
        name="Swordsmanship",
        category=SkillCategory.PHYSICAL,
        description="Master the art of blade combat",
        learning_rate=1.1,
        difficulty=1.0
    )

    print(f"   Created: {swordsmanship.name}")
    print(f"   Category: {swordsmanship.category.value}")
    print(f"   Initial Level: {swordsmanship.current_level}/{swordsmanship.max_level}")
    print(f"   Mastery: {swordsmanship.mastery_level}")

    # Practice the skill
    print("\n2. Practicing the skill...")

    practice_sessions = [
        (50, True, "Morning training"),
        (45, True, "Sparring match"),
        (30, False, "Difficult opponent"),
        (60, True, "Intensive training"),
        (55, True, "Tournament preparation")
    ]

    for exp, success, activity in practice_sessions:
        leveled_up, new_level = swordsmanship.add_experience(exp)
        print(f"   {activity}: +{exp} XP")
        if leveled_up:
            print(f"      ⚡ Level up! Now level {new_level:.1f}")

    # Check skill state
    print("\n3. Current skill state:")
    print(f"   Level: {swordsmanship.current_level:.1f}/{swordsmanship.max_level}")
    print(f"   Mastery: {swordsmanship.mastery_level}")
    print(f"   Success Rate: {swordsmanship.success_rate:.1%}")
    print(f"   Total Uses: {swordsmanship.total_uses}")
    print(f"   XP to Next Level: {swordsmanship.experience_to_next_level}")

    # Create a skill tree
    print("\n4. Creating a skill tree...")

    tree = SkillTree(
        name="Warrior's Path",
        description="Master the arts of combat and warfare",
        tree_type="warrior",
        available_points=10
    )

    # Add related skills
    agility = AdvancedSkill(
        name="Agility",
        category=SkillCategory.PHYSICAL,
        description="Move quickly and gracefully",
        learning_rate=1.2,
        difficulty=0.9
    )

    strength = AdvancedSkill(
        name="Strength",
        category=SkillCategory.PHYSICAL,
        description="Physical power and endurance",
        learning_rate=1.1,
        difficulty=1.0
    )

    combat_tactics = AdvancedSkill(
        name="Combat Tactics",
        category=SkillCategory.COGNITIVE,
        description="Strategic thinking in battle",
        learning_rate=1.0,
        difficulty=1.1
    )

    # Build tree structure
    tree.add_skill(swordsmanship)  # Root skill
    tree.add_skill(agility, ["Swordsmanship"])
    tree.add_skill(strength, ["Swordsmanship"])
    tree.add_skill(combat_tactics, ["Swordsmanship", "Agility"])

    print(f"   Created: {tree.name}")
    print(f"   Root skills: {tree.root_skills}")
    print(f"   Total skills: {len(tree.skills)}")
    print(f"   Available points: {tree.available_points}")

    # View tree statistics
    print("\n5. Tree statistics:")
    stats = tree.get_tree_statistics()
    for key, value in stats.items():
        if key not in ['created_at']:
            print(f"   {key}: {value}")

    # Add specializations
    print("\n6. Adding specializations...")

    if swordsmanship.can_specialize_in("two_handed"):
        swordsmanship.add_specialization("two_handed", 1.0)
        print(f"   Added specialization: two_handed")

    if swordsmanship.can_specialize_in("dual_wield"):
        swordsmanship.add_specialization("dual_wield", 1.0)
        print(f"   Added specialization: dual_wield")

    print(f"   Specializations: {list(swordsmanship.specializations.keys())}")

    # Practice specializations
    print("\n7. Practicing specializations...")

    for _ in range(5):
        improvement = swordsmanship.practice_specialization("two_handed", success=True)
        print(f"   two_handed improved by: {improvement:.2f}")

    print(f"\n   Final specialization levels:")
    for spec, level in swordsmanship.specializations.items():
        print(f"   {spec}: {level:.1f}/10.0")

    print("\n" + "=" * 60)
    print("Basic usage example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
