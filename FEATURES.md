# Character Skill Trees - Feature Overview

## Quick Reference

### What is it?

A **comprehensive skill progression system** for AI characters featuring:
- 8 skill categories
- 6 mastery levels
- Experience-based progression
- Skill prerequisites and synergies
- Specialization paths

### Who is it for?

- **Game Developers**: RPG skill systems, character progression
- **AI Developers**: Agent capability tracking and learning
- **Educators**: Learning path visualization and assessment
- **Interactive Fiction**: Dynamic character growth

## Feature Matrix

| Feature | Description | Status |
|---------|-------------|--------|
| **Skill Categories** | 8 categories (Cognitive, Social, Creative, etc.) | ✅ Complete |
| **Mastery Levels** | 6 levels (Novice → Grandmaster) | ✅ Complete |
| **Experience System** | Mathematical progression with difficulty scaling | ✅ Complete |
| **Prerequisites** | Skill requirement chains with validation | ✅ Complete |
| **Synergies** | Cross-skill bonuses and transfer effects | ✅ Complete |
| **Specializations** | Deep-dive expertise in specific areas | ✅ Complete |
| **Milestones** | Achievement system for progression | ✅ Complete |
| **Archetypes** | 4 predefined character templates | ✅ Complete |
| **Manager** | Multi-character tracking and recommendations | ✅ Complete |

## Core Components

### 1. Skills

```python
skill = AdvancedSkill(
    name="Programming",
    category=SkillCategory.TECHNICAL,
    description="Write and understand code",
    learning_rate=1.2,  # Learn 20% faster
    difficulty=0.9      # Slightly easier
)
```

**Features**:
- Level progression (0-100)
- Experience tracking
- Mastery level calculation
- Success rate computation
- Usage statistics
- Specializations
- Tags and metadata

### 2. Skill Trees

```python
tree = SkillTree(
    name="Engineer's Path",
    description="Master technical skills",
    available_points=10
)

tree.add_skill(skill_a)
tree.add_skill(skill_b, parent_skills=["skill_a"])
```

**Features**:
- Interconnected skills
- Skill unlocking with points
- Prerequisite validation
- Progression paths
- Tree statistics
- Mastery calculation

### 3. Progression

**Mastery Levels**:
- Novice (0-20%)
- Apprentice (20-40%)
- Journeyman (40-60%)
- Expert (60-80%)
- Master (80-95%)
- Grandmaster (95-100%)

**Experience Formula**:
```
exp_needed = base × (level + 1)^(difficulty × 1.5)
```

**Milestones**:
- Achievements at key levels
- Unlock abilities
- Grant rewards
- Track accomplishments

### 4. Prerequisites

```python
prereq = SkillPrerequisite(
    skill_name="Basic Skill",
    required_level=25.0,
    optional=False
)
```

**Features**:
- Required vs optional
- Level validation
- Progress tracking
- Circular dependency detection
- Chain analysis

### 5. Synergies

```python
synergy = SkillSynergy(
    primary_skill="Programming",
    secondary_skill="Mathematics",
    bonus_type="experience",
    bonus_value=1.5,
    activation_level=20.0
)
```

**Bonus Types**:
- `experience`: Boost XP gain
- `level`: Add skill levels
- `success_rate`: Improve success probability

**Features**:
- Cross-skill bonuses
- Activation requirements
- Bonus calculation
- Network strength
- Recommendations

### 6. Specializations

```python
skill.add_specialization("web_development", 1.0)
skill.practice_specialization("web_development", success=True)
```

**Features**:
- Sub-skill expertise
- Independent progression
- Practice-based improvement
- Synergy bonuses
- Level 1-10 range

## Predefined Archetypes

### The Innovator

**Focus**: Creativity, innovation, problem-solving

**Core Skills**:
- Creative Thinking (with specializations)
- Problem Solving
- Research Methodology

**Advanced Skills**:
- Innovation Management
- Systems Thinking

**Best For**: Inventors, researchers, creative characters

### The Educator

**Focus**: Teaching, communication, wisdom

**Core Skills**:
- Teaching (with specializations)
- Communication
- Patience

**Advanced Skills**:
- Mentoring
- Wisdom

**Best For**: Teachers, mentors, guides

### The Empath

**Focus**: Emotional intelligence, healing

**Core Skills**:
- Empathy (with specializations)
- Active Listening
- Emotional Intelligence

**Advanced Skills**:
- Emotional Healing
- Conflict Resolution

**Best For**: Counselors, mediators, support characters

### The Engineer

**Focus**: Technical skills, problem-solving

**Core Skills**:
- System Design (with specializations)
- Technical Problem Solving
- Technical Innovation

**Advanced Skills**:
- Prototyping
- System Optimization

**Best For**: Engineers, architects, technical specialists

## Usage Patterns

### Pattern 1: Basic Skill Practice

```python
# Practice a skill
results = manager.practice_skill(
    character_id="char_001",
    skill_name="Creative Thinking",
    success=True,
    difficulty=1.5,
    time_spent=30.0
)

print(f"XP gained: {results['experience_gained']}")
print(f"Level up: {results['level_up']}")
```

### Pattern 2: Skill Unlocks

```python
# Check if can unlock
can_unlock, reason = tree.can_unlock_skill("Advanced Skill")

# Unlock if possible
if can_unlock:
    tree.unlock_skill("Advanced Skill", point_cost=5)
```

### Pattern 3: Progress Tracking

```python
# Get character summary
summary = manager.get_skill_progress_summary("char_001")

print(f"Overall mastery: {summary['overall_mastery']:.1f}%")
print(f"Mastered skills: {summary['mastered_skills']}")
```

### Pattern 4: Recommendations

```python
# Get skill recommendations
recommendations = manager.recommend_next_skills("char_001", count=5)

for rec in recommendations:
    print(f"{rec['skill_name']} (Priority: {rec['priority']:.1f})")
```

## Integration Examples

### With Character Library

```python
from character_library import Character
from character_skill_trees import SkillTreeManager

# Create character with personality
character = Character(archetype="The Innovator")

# Create matching skill tree
manager = SkillTreeManager()
tree = manager.create_tree_for_character(
    character_id=character.id,
    archetype=character.archetype
)

# Personality influences skill development
if character.personality.openness > 0.8:
    # Boost creative learning
    tree.skills["Creative Thinking"].learning_rate *= 1.2
```

### With Memory System

```python
from memory import ProceduralMemory

# Store skill practice in procedural memory
memory = ProceduralMemory()

results = manager.practice_skill(...)
if results['level_up']:
    memory.add_skill_memory(
        skill_name=results['skill_name'],
        new_level=results['new_level'],
        timestamp=datetime.now()
    )
```

### In Game Loop

```python
def game_tick():
    # Practice skills based on actions
    if player_action == "code":
        manager.practice_skill(
            character_id="player",
            skill_name="Programming",
            success=random.random() < skill.success_rate,
            difficulty=task_difficulty,
            time_spent=time_elapsed
        )

    # Check for level-ups
    if results['level_up']:
        show_level_up_animation(results['skill_name'])
        unlock_abilities(results['skill_name'], results['new_level'])
```

## Performance Characteristics

### Complexity

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Skill lookup | O(1) | Dictionary access |
| Experience add | O(1) | Simple arithmetic |
| Prerequisite check | O(n) | n = prerequisites |
| Synergy calculation | O(m) | m = synergies |
| Tree traversal | O(v+e) | v = skills, e = edges |

### Memory Usage

- Per Skill: ~2KB
- Per Tree: ~100KB (5-10 skills)
- Per Character: ~500KB (multiple trees)

### Scalability

Tested with:
- Up to 100 skills per tree
- Up to 1000 characters
- Up to 10,000 skill practices/second

## Extension Points

### Custom Skill Categories

Add to `SkillCategory` enum:
```python
class SkillCategory(Enum):
    # ... existing categories
    MAGICAL = "magical"
    PSYCHIC = "psychic"
```

### Custom Progression Formulas

Extend `ExperienceCalculator`:
```python
@staticmethod
def custom_formula(current_level, difficulty):
    return base_exp * custom_function(current_level, difficulty)
```

### Custom Archetypes

Add to `ArchetypeSkillTrees`:
```python
@staticmethod
def create_custom_tree() -> SkillTree:
    tree = SkillTree(...)
    # Define skills
    return tree
```

## Best Practices

1. **Balance Difficulty**: Use difficulty values 0.7-1.3 for most skills
2. **Meaningful Prerequisites**: Don't require more than 2-3 prerequisites
3. **Synergy Groups**: Create clusters of 3-5 synergized skills
4. **Milestone Spacing**: Place milestones every 10-25 levels
5. **Specialization Limits**: Max 3-4 specializations per skill
6. **Tree Size**: 5-10 skills per tree for good UX
7. **Point Allocation**: Start with 10-15 skill points

## Common Pitfalls

❌ **Don't**: Create circular prerequisites
✅ **Do**: Use `PrerequisiteChecker` to validate

❌ **Don't**: Make skills too hard (>1.5 difficulty)
✅ **Do**: Balance difficulty with rewards

❌ **Don't**: Overload trees with too many skills
✅ **Do**: Keep trees focused on theme

❌ **Don't**: Forget to practice specializations
✅ **Do**: Regular specialization practice = faster growth

## FAQ

**Q: Can I use this for non-AI characters?**
A: Yes! Works for any character system (games, stories, etc.)

**Q: How do I persist character data?**
A: Use `tree.to_dict()` and `manager.to_dict()` for serialization

**Q: Can I modify experience formula?**
A: Yes, extend `ExperienceCalculator` or override `skill.add_experience()`

**Q: Are synergies required?**
A: No, skills work fine without synergies

**Q: Can I have multiple skill trees per character?**
A: Yes! Manager supports multiple trees per character

## Resources

- **README**: Full documentation
- **Examples**: `/examples` directory
- **Architecture**: `/docs/ARCHITECTURE.md`
- **Extraction Summary**: `/EXTRACTION_SUMMARY.md`

## License

MIT License - See LICENSE file
