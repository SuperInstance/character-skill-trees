# Character Skill Trees

**Advanced Skill Progression and Specialization System for AI Characters**

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)]()

A comprehensive, production-ready skill tree system for AI characters featuring experience-based progression, mastery levels, skill prerequisites, cross-skill synergies, and specialization paths.

## Features

### Core Capabilities

- **8 Skill Categories**: Cognitive, Social, Creative, Technical, Emotional, Physical, Leadership, Wisdom
- **6 Mastery Levels**: Novice → Apprentice → Journeyman → Expert → Master → Grandmaster
- **Skill Prerequisites**: Chain skills together with requirement validation
- **Cross-Skill Synergies**: Unlock bonuses by developing complementary skills
- **Specialization Paths**: Deepen expertise in specific skill areas
- **Experience-Based Progression**: Mathematical progression with customizable difficulty
- **Skill Milestones**: Achievement milestones at key progression points
- **Predefined Archetypes**: Ready-to-use skill trees for common character types

### Advanced Features

- **Skill Tree Manager**: Track character development across multiple skill trees
- **Progression Path Analysis**: Visualize the path to unlock advanced skills
- **Synergy Network**: Calculate and optimize cross-skill bonuses
- **Smart Recommendations**: AI-powered skill development suggestions
- **Experience Calculator**: Flexible progression math with difficulty scaling

## Installation

```bash
# Basic installation
pip install character-skill-trees

# With development dependencies
pip install character-skill-trees[dev]

# With examples dependencies
pip install character-skill-trees[examples]
```

## Quick Start

```python
from character_skill_trees import SkillTreeManager, ArchetypeSkillTrees

# Create a skill tree manager
manager = SkillTreeManager()

# Create a skill tree for a character
character_id = "character_001"
archetype = "The Innovator"

# Generate a predefined skill tree
tree = ArchetypeSkillTrees.create_innovator_tree()

# Or use the manager to create and track
tree = manager.create_tree_for_character(character_id, archetype)

# Practice skills
results = manager.practice_skill(
    character_id=character_id,
    skill_name="Creative Thinking",
    success=True,
    difficulty=1.5,
    time_spent=30.0
)

print(f"Experience gained: {results['experience_gained']}")
print(f"Level up: {results['level_up']}")
print(f"New level: {results['new_level']}")
```

## Skill Categories

The system organizes skills into 8 categories:

| Category | Description | Example Skills |
|----------|-------------|----------------|
| **Cognitive** | Mental processing and analysis | Problem Solving, Systems Thinking |
| **Social** | Interpersonal abilities | Communication, Active Listening |
| **Creative** | Innovation and expression | Creative Thinking, Technical Innovation |
| **Technical** | Practical skills and crafting | System Design, Prototyping |
| **Emotional** | Feeling and empathy | Empathy, Emotional Intelligence |
| **Physical** | Bodily capabilities | Athletics, Craftsmanship |
| **Leadership** | Guiding others | Mentoring, Innovation Management |
| **Wisdom** | Deep understanding and judgment | Emotional Healing, Wisdom |

## Mastery Levels

Skills progress through 6 mastery levels based on their current level relative to max level:

```
Novice (0-20%)       → Apprentice (20-40%)   → Journeyman (40-60%)
Expert (60-80%)      → Master (80-95%)       → Grandmaster (95-100%)
```

Each mastery level represents a significant threshold in skill development and can be used to unlock abilities, increase success rates, or provide bonuses.

## Creating Custom Skills

```python
from character_skill_trees import AdvancedSkill, SkillCategory, SkillMilestone
from character_skill_trees.prerequisites import SkillPrerequisite
from character_skill_trees.transfer import SkillSynergy

# Create a new skill
programming = AdvancedSkill(
    name="Programming",
    category=SkillCategory.TECHNICAL,
    description="Write and understand computer code",
    learning_rate=1.2,  # Learn 20% faster
    difficulty=0.9,     # Slightly easier than average
    tags={"core", "development"}
)

# Add prerequisites
programming.prerequisites = [
    SkillPrerequisite("Problem Solving", 10.0),
    SkillPrerequisite("Logic", 15.0)
]

# Add synergies
programming.synergies = [
    SkillSynergy(
        primary_skill="Programming",
        secondary_skill="Mathematics",
        bonus_type="experience",
        bonus_value=1.5,
        activation_level=20.0
    )
]

# Add milestones
programming.milestones = [
    SkillMilestone(
        level=10.0,
        title="Hello World",
        description="Write your first program",
        unlocks=["basic_syntax"],
        rewards={"confidence": 0.1}
    ),
    SkillMilestone(
        level=50.0,
        title="Senior Developer",
        description="Master complex systems",
        unlocks=["advanced_architecture"],
        rewards={"job_opportunities": "high"}
    )
]
```

## Skill Prerequisites

Skills can require other skills to be at certain levels before they can be unlocked:

```python
from character_skill_trees.prerequisites import SkillPrerequisite, PrerequisiteChecker

# Define prerequisites
advanced_skill.prerequisites = [
    SkillPrerequisite(
        skill_name="Basic Skill",
        required_level=25.0,
        optional=False  # Must be met
    ),
    SkillPrerequisite(
        skill_name="Optional Skill",
        required_level=10.0,
        optional=True   # Nice to have, not required
    )
]

# Check if prerequisites are met
skill_levels = {
    "Basic Skill": 30.0,
    "Optional Skill": 5.0
}

checker = PrerequisiteChecker()
all_met, missing = checker.check_prerequisites(
    prerequisites=advanced_skill.prerequisites,
    skill_levels=skill_levels
)

if all_met:
    print("All prerequisites met!")
else:
    print(f"Missing: {missing}")
```

## Skill Synergies

Synergies provide bonuses when multiple skills are developed together:

```python
from character_skill_trees.transfer import SkillSynergy, SynergyCalculator

# Create a synergy
synergy = SkillSynergy(
    primary_skill="Creative Thinking",
    secondary_skill="Problem Solving",
    bonus_type="experience",  # Can be: "experience", "level", "success_rate"
    bonus_value=1.5,          # 50% bonus
    activation_level=20.0     # Activates when both skills reach level 20
)

# Calculate total synergy bonus
calculator = SynergyCalculator()

skill_levels = {
    "Creative Thinking": 35.0,
    "Problem Solving": 28.0
}

bonus = calculator.calculate_total_synergy_bonus(
    skill_name="Creative Thinking",
    all_synergies=[synergy],
    skill_levels=skill_levels
)

print(f"Synergy bonus: {bonus:.2f}")
```

## Specializations

Skills can have specialized sub-skills that develop independently:

```python
# Add specializations to a skill
skill.add_specialization("web_development", initial_level=1.0)
skill.add_specialization("machine_learning", initial_level=1.0)

# Practice a specific specialization
improvement = skill.practice_specialization(
    name="web_development",
    success=True
)

print(f"Web development improved by: {improvement:.2f}")
print(f"Current level: {skill.specializations['web_development']:.1f}/10.0")
```

## Predefined Archetypes

The package includes 4 ready-to-use skill trees for common character archetypes:

### The Innovator
Focuses on creativity, problem-solving, and innovation management.
- **Core Skills**: Creative Thinking, Problem Solving, Research Methodology
- **Advanced Skills**: Innovation Management, Systems Thinking
- **Best For**: Creative characters, inventors, researchers

### The Educator
Specializes in teaching, communication, and wisdom.
- **Core Skills**: Teaching, Communication, Patience
- **Advanced Skills**: Mentoring, Wisdom
- **Best For**: Teachers, mentors, guides

### The Empath
Masters emotional intelligence and healing.
- **Core Skills**: Empathy, Active Listening, Emotional Intelligence
- **Advanced Skills**: Emotional Healing, Conflict Resolution
- **Best For**: Counselors, mediators, support characters

### The Engineer
Expert in system design and technical problem-solving.
- **Core Skills**: System Design, Technical Problem Solving, Technical Innovation
- **Advanced Skills**: Prototyping, System Optimization
- **Best For**: Engineers, architects, technical specialists

```python
# Use an archetype
from character_skill_trees import ArchetypeSkillTrees

# Get a predefined tree
innovator_tree = ArchetypeSkillTrees.create_innovator_tree()

# Access skills
creativity = innovator_tree.skills["Creative Thinking"]
print(f"Description: {creativity.description}")
print(f"Specializations: {list(creativity.specializations.keys())}")

# View tree statistics
stats = innovator_tree.get_tree_statistics()
print(f"Total skills: {stats['total_skills']}")
print(f"Available points: {stats['available_points']}")
```

## Experience Calculation

The system uses mathematical progression for experience requirements:

```python
from character_skill_trees.progression import ExperienceCalculator

# Calculate experience needed for next level
exp_needed = ExperienceCalculator.calculate_next_level_exp(
    current_level=10.0,
    difficulty=1.0,
    base_exp=100
)
print(f"Exp needed for level 11: {exp_needed}")

# Calculate total experience to reach a level
total_exp = ExperienceCalculator.calculate_total_exp_to_level(
    target_level=20.0,
    difficulty=1.0
)
print(f"Total exp to reach level 20: {total_exp}")

# Calculate experience from practice
gained = ExperienceCalculator.calculate_experience_gain(
    success=True,
    difficulty=1.5,
    time_spent=30.0,
    learning_rate=1.2
)
print(f"Experience gained: {gained}")
```

## Skill Progression Paths

Visualize the path to unlock advanced skills:

```python
# Get the progression path for a skill
path = tree.get_skill_progression_path("Systems Thinking")
print(f"Path to Systems Thinking: {' → '.join(path)}")

# Check if a skill can be unlocked
can_unlock, reason = tree.can_unlock_skill("Systems Thinking")
print(f"Can unlock: {can_unlock}")
print(f"Reason: {reason}")

# Unlock a skill
success = tree.unlock_skill("Systems Thinking", point_cost=5)
if success:
    print("Skill unlocked!")
```

## Character Development Tracking

```python
# Get comprehensive progress summary
summary = manager.get_skill_progress_summary(character_id)

print(f"Total skills: {summary['total_skills']}")
print(f"Mastered skills: {summary['mastered_skills']}")
print(f"Overall mastery: {summary['overall_mastery']:.1f}%")

# Get skill recommendations
recommendations = manager.recommend_next_skills(character_id, count=5)

for rec in recommendations:
    print(f"\n{rec['skill_name']} (Priority: {rec['priority']:.1f})")
    print(f"  {rec['description']}")
    print(f"  Current level: {rec['current_level']:.1f}")
    print(f"  Category: {rec['category']}")
```

## Use Cases

### Game Development
- RPG character progression systems
- Skill-based advancement mechanics
- Specialization and class systems

### AI Agents
- Learning and development tracking
- Capability progression
- Agent specialization

### Educational Software
- Learning path visualization
- Skill assessment and tracking
- Personalized learning recommendations

### Interactive Fiction
- Character growth mechanics
- Story-driven skill development
- Dynamic character capabilities

## Examples

See the `/examples` directory for complete examples:

- `basic_usage.py`: Basic skill tree operations
- `custom_skills.py`: Creating custom skills and trees
- `synergies.py`: Implementing skill synergies
- `character_development.py`: Full character progression example

Run examples:
```bash
cd examples
python basic_usage.py
```

## API Reference

### Core Classes

- **`AdvancedSkill`**: Individual skill with progression tracking
- **`SkillTree`**: Collection of interconnected skills
- **`SkillTreeManager`**: Manage skill trees for multiple characters
- **`ArchetypeSkillTrees`**: Predefined skill trees for archetypes

### Progression

- **`MasteryLevel`**: Enum of mastery levels
- **`SkillMilestone`**: Achievement milestones
- **`ExperienceCalculator`**: Calculate progression math

### Prerequisites

- **`SkillPrerequisite`**: Define skill requirements
- **`PrerequisiteChecker`**: Validate prerequisites

### Synergies

- **`SkillSynergy`**: Define cross-skill bonuses
- **`SynergyCalculator`**: Calculate synergy effects

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=character_skill_trees --cov-report=html

# Run specific test
pytest tests/test_skill.py
```

## Contributing

Contributions are welcome! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Part of the LucidDreamer ecosystem for AI character development.

## Support

- **Documentation**: [GitHub Wiki](https://github.com/luciddreamer/character-skill-trees/wiki)
- **Issues**: [GitHub Issues](https://github.com/luciddreamer/character-skill-trees/issues)
- **Discussions**: [GitHub Discussions](https://github.com/luciddreamer/character-skill-trees/discussions)

## Changelog

### Version 1.0.0 (2026-01-08)
- Initial release
- 8 skill categories
- 6 mastery levels
- Skill prerequisites and synergies
- 4 predefined archetypes
- Experience-based progression
- Specialization paths
- Full documentation and examples
