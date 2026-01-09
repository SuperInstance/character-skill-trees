"""
Predefined skill trees for character archetypes.
"""

from .core.skill import AdvancedSkill, SkillCategory
from .core.skill_tree import SkillTree
from .progression.mastery import SkillMilestone
from .prerequisites.requirements import SkillPrerequisite
from .transfer.synergies import SkillSynergy


class ArchetypeSkillTrees:
    """Predefined skill trees for each character archetype"""

    @staticmethod
    def create_innovator_tree() -> SkillTree:
        """Create skill tree for The Innovator archetype"""
        tree = SkillTree(
            name="The Innovator's Path",
            description="Master the arts of discovery, creativity, and groundbreaking innovation",
            tree_type="innovator",
            difficulty_modifier=0.9  # Slightly easier progression
        )

        # Core Skills
        creativity = AdvancedSkill(
            name="Creative Thinking",
            category=SkillCategory.CREATIVE,
            description="Generate novel ideas and think outside conventional boundaries",
            learning_rate=1.2,
            difficulty=0.8,
            tags={"core", "innovation"}
        )
        creativity.add_specialization("divergent_thinking", 3.0)
        creativity.add_specialization("conceptual_blending", 2.0)

        problem_solving = AdvancedSkill(
            name="Problem Solving",
            category=SkillCategory.COGNITIVE,
            description="Analyze complex problems and develop effective solutions",
            learning_rate=1.1,
            difficulty=0.9,
            tags={"core", "analytical"}
        )

        research = AdvancedSkill(
            name="Research Methodology",
            category=SkillCategory.TECHNICAL,
            description="Conduct systematic research and gather meaningful insights",
            learning_rate=1.0,
            difficulty=1.0,
            tags={"core", "methodical"}
        )

        # Specialized Skills
        innovation = AdvancedSkill(
            name="Innovation Management",
            category=SkillCategory.LEADERSHIP,
            description="Lead innovation initiatives and manage creative teams",
            learning_rate=0.9,
            difficulty=1.1,
            tags={"advanced", "leadership"}
        )

        systems_thinking = AdvancedSkill(
            name="Systems Thinking",
            category=SkillCategory.COGNITIVE,
            description="Understand complex systems and their interconnections",
            learning_rate=0.8,
            difficulty=1.2,
            tags={"advanced", "analytical"}
        )

        # Add prerequisites
        innovation.prerequisites = [
            SkillPrerequisite("Creative Thinking", 15.0),
            SkillPrerequisite("Problem Solving", 10.0)
        ]

        systems_thinking.prerequisites = [
            SkillPrerequisite("Problem Solving", 20.0),
            SkillPrerequisite("Research Methodology", 15.0)
        ]

        # Add synergies
        creativity.synergies = [
            SkillSynergy("Creative Thinking", "Innovation Management", "experience", 1.5, 10.0),
            SkillSynergy("Creative Thinking", "Systems Thinking", "level", 0.2, 15.0)
        ]

        # Add milestones
        creativity.milestones = [
            SkillMilestone(10.0, "Creative Spark", "First signs of creative genius",
                         ["basic_ideation"], {"inspiration_bonus": 0.1}),
            SkillMilestone(25.0, "Creative Flow", "Consistent creative output",
                         ["advanced_ideation"], {"flow_state_chance": 0.2}),
            SkillMilestone(50.0, "Innovation Catalyst", "Inspire creativity in others",
                         ["creative_leadership"], {"team_creativity_bonus": 0.3}),
            SkillMilestone(75.0, "Creative Visionary", "Transformative creative thinking",
                         ["paradigm_shift"], {"breakthrough_chance": 0.4}),
            SkillMilestone(90.0, "Creative Genius", "Master of innovation",
                         ["legendary_innovator"], {"breakthrough_multiplier": 2.0})
        ]

        # Build tree structure
        tree.add_skill(creativity)  # Root skill
        tree.add_skill(problem_solving, ["Creative Thinking"])
        tree.add_skill(research, ["Problem Solving"])
        tree.add_skill(innovation, ["Creative Thinking", "Problem Solving"])
        tree.add_skill(systems_thinking, ["Problem Solving", "Research Methodology"])

        # Set unlock requirements
        tree.unlock_requirements["Innovation Management"] = {"points": 3, "level": 10}
        tree.unlock_requirements["Systems Thinking"] = {"points": 5, "level": 15}

        tree.available_points = 10

        return tree

    @staticmethod
    def create_educator_tree() -> SkillTree:
        """Create skill tree for The Educator archetype"""
        tree = SkillTree(
            name="The Educator's Journey",
            description="Master the arts of teaching, mentoring, and knowledge transmission",
            tree_type="educator",
            difficulty_modifier=0.8  # Easier progression - teaching builds on itself
        )

        # Core Skills
        teaching = AdvancedSkill(
            name="Teaching",
            category=SkillCategory.SOCIAL,
            description="Effectively convey knowledge and facilitate learning",
            learning_rate=1.3,
            difficulty=0.7,
            tags={"core", "communication"}
        )
        teaching.add_specialization("curriculum_design", 2.0)
        teaching.add_specialization("assessment", 1.5)

        communication = AdvancedSkill(
            name="Communication",
            category=SkillCategory.SOCIAL,
            description="Clearly articulate ideas and listen actively",
            learning_rate=1.2,
            difficulty=0.8,
            tags={"core", "social"}
        )

        patience = AdvancedSkill(
            name="Patience",
            category=SkillCategory.EMOTIONAL,
            description="Maintain composure and provide consistent support",
            learning_rate=1.1,
            difficulty=0.9,
            tags={"core", "emotional"}
        )

        # Specialized Skills
        mentoring = AdvancedSkill(
            name="Mentoring",
            category=SkillCategory.LEADERSHIP,
            description="Guide others through personal and professional development",
            learning_rate=1.0,
            difficulty=1.0,
            tags={"advanced", "leadership"}
        )

        wisdom = AdvancedSkill(
            name="Wisdom",
            category=SkillCategory.WISDOM,
            description="Apply knowledge with deep understanding and judgment",
            learning_rate=0.7,
            difficulty=1.3,
            tags={"advanced", "wisdom"}
        )

        # Add prerequisites and structure
        mentoring.prerequisites = [
            SkillPrerequisite("Teaching", 20.0),
            SkillPrerequisite("Communication", 15.0),
            SkillPrerequisite("Patience", 10.0)
        ]

        wisdom.prerequisites = [
            SkillPrerequisite("Teaching", 30.0),
            SkillPrerequisite("Communication", 25.0),
            SkillPrerequisite("Patience", 20.0)
        ]

        # Add milestones for teaching
        teaching.milestones = [
            SkillMilestone(10.0, "Natural Teacher", "Gift for explaining concepts",
                         ["clear_explanations"], {"comprehension_bonus": 0.2}),
            SkillMilestone(25.0, "Inspiring Educator", "Motivate students to excel",
                         ["inspiration_techniques"], {"student_motivation": 0.3}),
            SkillMilestone(50.0, "Master Teacher", "Transform educational approaches",
                         ["educational_innovation"], {"learning_efficiency": 0.4}),
            SkillMilestone(75.0, "Educational Visionary", "Revolutionize learning",
                         ["paradigm_education"], ["educational_breakthrough"]),
            SkillMilestone(90.0, "Legendary Mentor", "Shape generations of thinkers",
                         ["immortal_educator"], ["legacy_multiplier"])
        ]

        # Build tree
        tree.add_skill(teaching)  # Root
        tree.add_skill(communication, ["Teaching"])
        tree.add_skill(patience, ["Communication"])
        tree.add_skill(mentoring, ["Teaching", "Communication", "Patience"])
        tree.add_skill(wisdom, ["Teaching", "Communication", "Patience"])

        tree.available_points = 12
        return tree

    @staticmethod
    def create_empath_tree() -> SkillTree:
        """Create skill tree for The Empath archetype"""
        tree = SkillTree(
            name="The Empath's Path",
            description="Master emotional intelligence, deep listening, and compassionate support",
            tree_type="empath",
            difficulty_modifier=0.85
        )

        # Core Skills
        empathy = AdvancedSkill(
            name="Empathy",
            category=SkillCategory.EMOTIONAL,
            description="Deeply understand and share the feelings of others",
            learning_rate=1.4,
            difficulty=0.6,
            tags={"core", "emotional"}
        )
        empathy.add_specialization("emotional_resonance", 4.0)
        empathy.add_specialization("compassionate_action", 3.0)

        listening = AdvancedSkill(
            name="Active Listening",
            category=SkillCategory.SOCIAL,
            description="Listen with full attention and understanding",
            learning_rate=1.3,
            difficulty=0.7,
            tags={"core", "social"}
        )

        emotional_intelligence = AdvancedSkill(
            name="Emotional Intelligence",
            category=SkillCategory.EMOTIONAL,
            description="Recognize, understand, and manage emotions",
            learning_rate=1.2,
            difficulty=0.8,
            tags={"core", "emotional"}
        )

        # Specialized Skills
        healing = AdvancedSkill(
            name="Emotional Healing",
            category=SkillCategory.WISDOM,
            description="Help others process and heal from emotional wounds",
            learning_rate=0.9,
            difficulty=1.1,
            tags={"advanced", "wisdom"}
        )

        conflict_resolution = AdvancedSkill(
            name="Conflict Resolution",
            category=SkillCategory.SOCIAL,
            description="Mediate conflicts and find harmonious solutions",
            learning_rate=1.0,
            difficulty=1.0,
            tags={"advanced", "social"}
        )

        # Build structure
        healing.prerequisites = [
            SkillPrerequisite("Empathy", 25.0),
            SkillPrerequisite("Active Listening", 20.0),
            SkillPrerequisite("Emotional Intelligence", 15.0)
        ]

        conflict_resolution.prerequisites = [
            SkillPrerequisite("Active Listening", 15.0),
            SkillPrerequisite("Emotional Intelligence", 20.0)
        ]

        # Add milestones
        empathy.milestones = [
            SkillMilestone(10.0, "Natural Empath", "Instinctive understanding of others",
                         ["intuitive_empathy"], {"emotional_accuracy": 0.3}),
            SkillMilestone(25.0, "Deep Listener", "Hear what's unsaid",
                         ["profound_listening"], ["hidden_meaning_detection"]),
            SkillMilestone(50.0, "Emotional Guide", "Help others navigate feelings",
                         ["emotional_guidance"], {"healing_effectiveness": 0.4}),
            SkillMilestone(75.0, "Compassionate Healer", "Facilitate deep healing",
                         ["transformative_empathy"], ["emotional_breakthrough"]),
            SkillMilestone(90.0, "Master Empath", "Transcendent emotional connection",
                         ["emotional_transcendence"], ["emotional_mastery"])
        ]

        # Build tree
        tree.add_skill(empathy)  # Root
        tree.add_skill(listening, ["Empathy"])
        tree.add_skill(emotional_intelligence, ["Empathy", "Active Listening"])
        tree.add_skill(healing, ["Empathy", "Active Listening", "Emotional Intelligence"])
        tree.add_skill(conflict_resolution, ["Active Listening", "Emotional Intelligence"])

        tree.available_points = 11
        return tree

    @staticmethod
    def create_engineer_tree() -> SkillTree:
        """Create skill tree for The Engineer archetype"""
        tree = SkillTree(
            name="The Engineer's Craft",
            description="Master system design, problem-solving, and technical innovation",
            tree_type="engineer",
            difficulty_modifier=1.0
        )

        # Core Skills
        system_design = AdvancedSkill(
            name="System Design",
            category=SkillCategory.TECHNICAL,
            description="Design complex, efficient systems",
            learning_rate=1.1,
            difficulty=0.9,
            tags={"core", "technical"}
        )
        system_design.add_specialization("architecture", 3.0)
        system_design.add_specialization("optimization", 2.5)

        problem_solving = AdvancedSkill(
            name="Technical Problem Solving",
            category=SkillCategory.COGNITIVE,
            description="Solve complex technical challenges",
            learning_rate=1.1,
            difficulty=0.9,
            tags={"core", "analytical"}
        )

        innovation = AdvancedSkill(
            name="Technical Innovation",
            category=SkillCategory.CREATIVE,
            description="Create novel technical solutions",
            learning_rate=1.0,
            difficulty=1.0,
            tags={"core", "creative"}
        )

        # Specialized Skills
        prototyping = AdvancedSkill(
            name="Prototyping",
            category=SkillCategory.TECHNICAL,
            description="Build and test rapid prototypes",
            learning_rate=1.2,
            difficulty=0.8,
            tags={"advanced", "technical"}
        )

        optimization = AdvancedSkill(
            name="System Optimization",
            category=SkillCategory.TECHNICAL,
            description="Maximize system efficiency and performance",
            learning_rate=0.9,
            difficulty=1.1,
            tags={"advanced", "technical"}
        )

        # Build structure
        prototyping.prerequisites = [
            SkillPrerequisite("System Design", 15.0),
            SkillPrerequisite("Technical Problem Solving", 10.0)
        ]

        optimization.prerequisites = [
            SkillPrerequisite("System Design", 20.0),
            SkillPrerequisite("Technical Problem Solving", 25.0),
            SkillPrerequisite("Technical Innovation", 15.0)
        ]

        # Build tree
        tree.add_skill(system_design)  # Root
        tree.add_skill(problem_solving, ["System Design"])
        tree.add_skill(innovation, ["System Design", "Technical Problem Solving"])
        tree.add_skill(prototyping, ["System Design", "Technical Problem Solving"])
        tree.add_skill(optimization, ["System Design", "Technical Problem Solving", "Technical Innovation"])

        tree.available_points = 10
        return tree
