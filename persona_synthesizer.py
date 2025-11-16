"""
Persona Synthesizer

Uses AI to synthesize composite personas from multiple LinkedIn profiles
"""

import os
import sys
from typing import List, Dict, Any
from pathlib import Path

# Add UnifiedLLMClient to path
llm_client_path = Path.home() / "Development" / "Scripts" / "UnifiedLLMClient"
sys.path.insert(0, str(llm_client_path))

try:
    from llm_client.client_factory import LLMClientFactory
    UnifiedLLMClient = LLMClientFactory
except ImportError:
    print("⚠️  UnifiedLLMClient not found. Install from ~/Development/Scripts/UnifiedLLMClient")
    UnifiedLLMClient = None


class PersonaSynthesizer:
    """Synthesizes composite personas from profile data using AI"""

    def __init__(self, model: str = "qwen"):
        """
        Initialize synthesizer

        Args:
            model: AI model to use (qwen, gpt-4o, claude-3-5-sonnet)
        """
        if not UnifiedLLMClient:
            raise ImportError("UnifiedLLMClient is required. Install from ~/Development/Scripts/UnifiedLLMClient")

        self.client = UnifiedLLMClient.create(model)
        self.model = model

    def synthesize_persona(self, profiles: List[Dict[str, Any]], persona_name: str) -> str:
        """
        Synthesize composite persona from multiple profiles

        Args:
            profiles: List of profile dictionaries
            persona_name: Name for the persona

        Returns:
            Markdown formatted persona document
        """
        # Build synthesis prompt
        prompt = self._build_synthesis_prompt(profiles, persona_name)

        # Generate persona using AI
        print(f"  Using model: {self.model}")
        response = self.client.generate(prompt)

        return response

    def _build_synthesis_prompt(self, profiles: List[Dict[str, Any]], persona_name: str) -> str:
        """Build AI prompt for persona synthesis"""

        # Summarize profile data
        profiles_summary = self._summarize_profiles(profiles)

        prompt = f"""You are an expert persona designer and audience analyst. Your task is to create a comprehensive, actionable persona based on LinkedIn profiles of {len(profiles)} individuals.

# INPUT DATA

{profiles_summary}

# YOUR TASK

Create a detailed composite persona named "{persona_name}" that represents the common patterns, behaviors, and characteristics across these individuals. This persona will be used to test content relevance and engagement potential.

# REQUIRED PERSONA STRUCTURE

Generate a well-formatted markdown document with the following sections:

## 1. PERSONA OVERVIEW
- **Name**: {persona_name}
- **Archetype**: A descriptive 2-3 word label (e.g., "Strategic Executive", "Technical Leader")
- **One-line Summary**: Concise description of who this persona represents

## 2. DEMOGRAPHICS & PROFESSIONAL PROFILE
- **Typical Roles/Titles**: List 3-5 common job titles
- **Industries**: Primary industries they work in
- **Company Sizes**: Startup, SMB, Enterprise, etc.
- **Career Stage**: Early career, mid-level, senior, executive
- **Geographic Distribution**: Regions or countries
- **Education Background**: Common degrees, institutions, or certifications

## 3. GOALS & MOTIVATIONS
- **Professional Goals**: What they're trying to achieve (3-5 bullets)
- **Personal Drivers**: What motivates them beyond work
- **Success Metrics**: How they measure success

## 4. PAIN POINTS & CHALLENGES
- **Primary Challenges**: Top 5 problems they face
- **Frustrations**: What causes them stress or friction
- **Resource Constraints**: Time, budget, knowledge gaps

## 5. BEHAVIORS & HABITS
- **Daily Routines**: How they structure their workday
- **Decision-Making Style**: Analytical, intuitive, collaborative, etc.
- **Information Consumption**: When and how they consume content
- **Technology Adoption**: Early adopter, pragmatist, conservative
- **Social Media Activity**: Platforms used, posting frequency, engagement style

## 6. COMMUNICATION PREFERENCES
- **Preferred Tone**: Formal, conversational, technical, storytelling
- **Content Formats**: Articles, videos, podcasts, infographics, case studies
- **Detail Level**: High-level overview, deep technical detail, balanced
- **Reading Time**: Short-form (2-3 min), medium (5-7 min), long-form (10+ min)
- **Trigger Words**: Language that resonates positively
- **Turn-offs**: Language or approaches to avoid

## 7. CONTENT ENGAGEMENT PATTERNS
- **Topics of Interest**: Top 10 subjects they care about
- **Content Discovery**: How they find new content (LinkedIn, newsletters, search, recommendations)
- **Engagement Triggers**: What makes them like, comment, or share
- **Sharing Behavior**: When and why they share content with their network
- **Time Investment**: How much time they'll spend on content per session

## 8. PROFESSIONAL CONTEXT
- **Reporting Structure**: Who they report to, who reports to them
- **Buying Authority**: Decision maker, influencer, end user
- **Key Relationships**: Departments or roles they work closely with
- **Meeting Schedule**: Percentage of day in meetings vs focused work
- **Travel Frequency**: How often they travel for work

## 9. SKILLS & EXPERTISE
- **Core Competencies**: Top skills they possess
- **Knowledge Areas**: Domains where they're experts
- **Learning Priorities**: Skills they're actively developing
- **Thought Leadership**: Topics where they have strong opinions

## 10. CONTENT TESTING FRAMEWORK
- **Relevance Score**: Rate content 1-10 on: Does this solve their problem?
- **Engagement Score**: Rate content 1-10 on: Would they read, like, comment, or share?
- **Action Score**: Rate content 1-10 on: Would they take action (click, download, contact)?
- **Red Flags**: Content elements that would immediately turn them off
- **Green Flags**: Content elements that would immediately hook them

## 11. EXAMPLE CONTENT THAT RESONATES
- Provide 3-5 hypothetical headlines or content topics that would strongly appeal to this persona
- Explain WHY each would resonate

## 12. ANTI-PATTERNS
- List 5 things to NEVER do when creating content for this persona
- Explain the reasoning

# SYNTHESIS GUIDELINES

1. **Find Common Patterns**: Look for shared characteristics across profiles
2. **Be Specific**: Use concrete details, not generic descriptions
3. **Stay Realistic**: Base insights on actual profile data, not assumptions
4. **Include Nuance**: Note variations where they exist ("Some prefer X, while others Y")
5. **Make It Actionable**: Every section should help content creators make better decisions
6. **Use Data**: Reference specific examples from the profiles when relevant

# OUTPUT FORMAT

- Use clear markdown formatting
- Use bullet points for lists
- Use **bold** for emphasis
- Include specific examples where helpful
- Make it scannable and easy to reference

Generate the complete persona document now."""

        return prompt

    def _summarize_profiles(self, profiles: List[Dict[str, Any]]) -> str:
        """Create a structured summary of all profiles"""

        summary_parts = []

        for i, profile in enumerate(profiles, 1):
            name = profile.get('name', f'Profile {i}')
            headline = profile.get('headline', 'No headline')
            location = profile.get('location', 'Unknown location')
            about = profile.get('about', '')[:500]  # Limit length

            summary = f"""
## Profile {i}: {name}

**Headline**: {headline}
**Location**: {location}

**About**: {about if about else 'No about section'}
"""

            # Add experience
            experiences = profile.get('experience', [])
            if experiences:
                summary += "\n**Recent Experience**:\n"
                for exp in experiences[:3]:
                    summary += f"- {exp.get('title', 'Unknown')} at {exp.get('company', 'Unknown')} ({exp.get('duration', 'Unknown')})\n"

            # Add education
            education = profile.get('education', [])
            if education:
                summary += "\n**Education**:\n"
                for edu in education[:2]:
                    summary += f"- {edu.get('degree', 'Unknown')} from {edu.get('school', 'Unknown')}\n"

            # Add skills
            skills = profile.get('skills', [])
            if skills:
                summary += f"\n**Skills**: {', '.join(skills[:10])}\n"

            # Add recent posts
            posts = profile.get('posts', [])
            if posts:
                summary += "\n**Recent Activity/Interests**:\n"
                for post in posts[:2]:
                    text = post.get('text', '')[:200]
                    if text:
                        summary += f"- {text}...\n"

            summary_parts.append(summary)

        return "\n---\n".join(summary_parts)


if __name__ == "__main__":
    # Test with sample data
    sample_profiles = [
        {
            'name': 'Sarah Chen',
            'headline': 'VP of Engineering at TechCorp | Building AI-powered solutions',
            'location': 'San Francisco Bay Area',
            'about': 'Passionate about building scalable systems and leading high-performing engineering teams...',
            'experience': [
                {'title': 'VP Engineering', 'company': 'TechCorp', 'duration': '2020 - Present'},
                {'title': 'Director of Engineering', 'company': 'StartupXYZ', 'duration': '2017 - 2020'},
            ],
            'skills': ['Leadership', 'Cloud Architecture', 'Python', 'Team Building'],
        }
    ]

    synthesizer = PersonaSynthesizer(model="qwen")
    persona = synthesizer.synthesize_persona(sample_profiles, "Tech Executive")
    print(persona)
