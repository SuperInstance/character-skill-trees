# Character Skill Trees - Architecture

## System Overview

The Character Skill Trees system is organized into a modular architecture with clear separation of concerns:

```
character_skill_trees/
├── core/              # Core skill and tree classes
├── progression/       # Mastery and experience systems
├── prerequisites/     # Requirement validation
├── transfer/          # Synergy and cross-skill effects
├── manager.py         # Character development tracking
└── archetypes.py      # Predefined skill trees
```

## Core Components

### 1. Core Module (`core/`)

**Purpose**: Define fundamental skill and tree structures

**Classes**:
- `AdvancedSkill`: Individual skill with progression tracking
- `SkillCategory`: Enum of 8 skill categories
- `SkillTree`: Collection of interconnected skills

**Key Features**:
- Experience-based leveling
- Mastery level calculation
- Specialization tracking
- Usage statistics
- Tag and metadata system

**Data Flow**:
```
User Input → add_experience() → Update Level → Check Milestones → Return Results
```

### 2. Progression Module (`progression/`)

**Purpose**: Handle mathematical progression and milestones

**Classes**:
- `MasteryLevel`: Enum of 6 mastery levels (Novice → Grandmaster)
- `SkillMilestone`: Achievement milestones at key levels
- `ExperienceCalculator`: Mathematical progression utilities

**Key Algorithms**:

**Experience Formula**:
```python
exp_needed = base_exp * (current_level + 1) ^ (difficulty * 1.5)
```

**Mastery Level Calculation**:
```python
level_percentage = current_level / max_level

if level_percentage >= 0.95: return Grandmaster
elif level_percentage >= 0.80: return Master
elif level_percentage >= 0.60: return Expert
elif level_percentage >= 0.40: return Journeyman
elif level_percentage >= 0.20: return Apprentice
else: return Novice
```

### 3. Prerequisites Module (`prerequisites/`)

**Purpose**: Validate skill requirements and dependencies

**Classes**:
- `SkillPrerequisite`: Single prerequisite requirement
- `PrerequisiteChecker`: Validation and chain analysis

**Key Features**:
- Circular dependency detection
- Prerequisite chain traversal
- Progress calculation
- Missing requirement identification

**Validation Process**:
```
Check Prerequisites → Validate Levels → Detect Cycles → Return (valid, missing)
```

### 4. Transfer Module (`transfer/`)

**Purpose**: Handle cross-skill synergies and bonuses

**Classes**:
- `SkillSynergy`: Single synergy definition
- `SynergyCalculator`: Bonus calculation and recommendations

**Synergy Types**:
- `experience`: Boost experience gain
- `level`: Add levels to related skills
- `success_rate`: Improve success probability

**Bonus Formula**:
```python
level_factor = (primary_level + secondary_level) / (2 * activation_level)
bonus = base_bonus_value * level_factor
```

### 5. Manager (`manager.py`)

**Purpose**: Track character development across multiple skill trees

**Class**: `SkillTreeManager`

**Responsibilities**:
- Create skill trees for characters
- Track skill practice and progression
- Generate progress summaries
- Recommend next skills to develop
- Unlock skills using skill points

**Data Structures**:
```python
skill_trees: Dict[str, SkillTree]              # tree_id → tree
character_trees: Dict[str, List[str]]          # character_id → [tree_ids]
global_skill_registry: Dict[str, AdvancedSkill] # skill_name → skill
```

### 6. Archetypes (`archetypes.py`)

**Purpose**: Provide predefined skill trees for common character types

**Class**: `ArchetypeSkillTrees`

**Available Archetypes**:
1. The Innovator - Creativity and innovation
2. The Educator - Teaching and wisdom
3. The Empath - Emotional intelligence
4. The Engineer - Technical problem-solving

**Design Pattern**: Factory methods for tree creation

## Data Flow

### Skill Practice Flow

```
1. User calls practice_skill()
   ↓
2. Manager locates skill in character's trees
   ↓
3. ExperienceCalculator calculates XP gain
   ↓
4. skill.add_experience() updates level
   ↓
5. Check for level-up
   ↓
6. Check milestones
   ↓
7. Practice specialization if active
   ↓
8. Return results dictionary
```

### Skill Unlock Flow

```
1. User calls unlock_skill()
   ↓
2. PrerequisiteChecker validates prerequisites
   ↓
3. Check skill points availability
   ↓
4. Deduct points
   ↓
5. Initialize skill level
   ↓
6. Update tree statistics
   ↓
7. Return success/failure
```

### Synergy Calculation Flow

```
1. User requests synergy bonus
   ↓
2. SynergyCalculator filters relevant synergies
   ↓
3. For each synergy:
   - Check activation requirements
   - Calculate current bonus
   - Add to total
   ↓
4. Return aggregated bonus
```

## Design Patterns

### 1. Dataclass Pattern
- Used for skill, prerequisite, and synergy definitions
- Provides automatic `__init__`, `__repr__`, and equality checks

### 2. Factory Pattern
- `ArchetypeSkillTrees` creates predefined skill trees
- Encapsulates complex tree construction logic

### 3. Manager Pattern
- `SkillTreeManager` centralizes character tracking
- Provides single point of access for character development

### 4. Calculator Pattern
- Static utility classes for mathematical operations
- `ExperienceCalculator`, `SynergyCalculator`, `PrerequisiteChecker`

## Extension Points

### Adding New Skill Categories

1. Add to `SkillCategory` enum in `core/skill.py`
2. Update documentation
3. Consider archetype balance

### Creating Custom Archetypes

1. Add factory method to `ArchetypeSkillTrees`
2. Define core and advanced skills
3. Set up prerequisites and synergies
4. Add milestones

### Custom Progression Formulas

1. Extend `ExperienceCalculator`
2. Add custom formula methods
3. Integrate with `AdvancedSkill.add_experience()`

### New Synergy Types

1. Add to `SkillSynergy.bonus_type` options
2. Implement calculation in `SynergyCalculator`
3. Document effects and use cases

## Performance Considerations

### Complexity Analysis

- **Skill Lookup**: O(1) - Dictionary access
- **Prerequisite Validation**: O(n) - n = number of prerequisites
- **Synergy Calculation**: O(m) - m = number of synergies
- **Tree Traversal**: O(v + e) - v = skills, e = connections

### Optimization Opportunities

1. **Caching**: Cache skill tree statistics
2. **Lazy Loading**: Load archetypes on-demand
3. **Indexing**: Index skills by category for faster filtering

### Memory Usage

- **Per Skill**: ~2KB (with full metadata)
- **Per Tree**: ~100KB (5-10 skills)
- **Per Character**: ~500KB (multiple trees)

## Testing Strategy

### Unit Tests
- Test each component independently
- Mock dependencies
- Focus on algorithms and calculations

### Integration Tests
- Test component interactions
- Use real skill trees
- Verify end-to-end flows

### Property Tests
- Test mathematical properties
- Verify monotonicity
- Check boundary conditions

## Future Enhancements

1. **Persistence**: Save/load character progression
2. **Visualization**: Skill tree graph rendering
3. **Balancing**: Auto-balance archetype trees
4. **Machine Learning**: Learn optimal skill paths
5. **Multiplayer**: Shared skill trees for parties
6. **Modding**: Plugin system for custom skills
