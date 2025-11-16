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
        # Generate evidence tables first
        print(f"  Analyzing {len(profiles)} profiles for evidence...")
        evidence = self._generate_evidence_tables(profiles)

        # Build synthesis prompt with evidence
        prompt = self._build_synthesis_prompt(profiles, persona_name, evidence)

        # Generate persona using AI
        print(f"  Using model: {self.model}")
        response = self.client.generate(prompt)

        return response

    def _build_synthesis_prompt(self, profiles: List[Dict[str, Any]], persona_name: str, evidence: str = "") -> str:
        """Build AI prompt for persona synthesis"""

        # Summarize profile data
        profiles_summary = self._summarize_profiles(profiles)

        prompt = f"""You are an expert persona designer and audience analyst. Your task is to create a comprehensive, actionable persona based on LinkedIn profiles of {len(profiles)} individuals.

# INPUT DATA

{profiles_summary}

# EVIDENCE ANALYSIS

{evidence}

# YOUR TASK

Create a detailed composite persona named "{persona_name}" that represents the common patterns, behaviors, and characteristics across these individuals. This persona will be used to test content relevance and engagement potential.

IMPORTANT: Use the evidence analysis above to back your persona with concrete data. Reference specific frequencies and patterns from the evidence tables.

# REQUIRED PERSONA STRUCTURE

Generate a well-formatted markdown document with the following sections:

## 1. PERSONA OVERVIEW
- **Name**: {persona_name}
- **Archetype**: A descriptive 2-3 word label (e.g., "Strategic Executive", "Technical Leader")
- **One-line Summary**: Concise description of who this persona represents

## 2. DEMOGRAPHICS & PROFESSIONAL PROFILE

### Evidence Base (n={len(profiles)} profiles)

Include a table showing concrete evidence:
| Metric | Finding | Frequency |
|--------|---------|-----------|
| Most Common Titles | [Actual titles from evidence] | [%] |
| Industries | [Actual industries] | [Distribution] |
| Locations | [Geographic data] | [%] |
| Education | [Patterns from evidence] | [%] |

Then provide:
- **Typical Roles/Titles**: List 3-5 common job titles (backed by evidence)
- **Industries**: Primary industries they work in (with percentages)
- **Company Sizes**: Startup, SMB, Enterprise, etc. (with data)
- **Career Stage**: Early career, mid-level, senior, executive
- **Geographic Distribution**: Regions or countries (with distribution)
- **Education Background**: Common degrees, institutions, or certifications (with percentages)

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

## 10. CONTENT SCORING WORKSHEET

Create an actionable scoring worksheet with the following structure:

### Instructions
1. Read your content draft
2. Score each dimension 1-5 using the rubric below
3. Calculate total score (max 50 points)
4. Use action items if score < 35

---

### Dimension 1: Relevance (Weight: 2x)
**Question**: Does this solve a problem this persona faces?

| Score | Criteria |
|-------|----------|
| 5 | Directly addresses top 3 pain points with specific solutions |
| 4 | Addresses relevant pain point with general guidance |
| 3 | Tangentially related to persona's challenges |
| 2 | Mentions persona's industry but not their problems |
| 1 | Completely off-topic |

**Your Score**: _____ × 2 = _____

**Evidence Checklist** (based on profile analysis):
- [ ] Mentions specific pain points identified in evidence
- [ ] Uses industry-specific examples (from industry distribution)
- [ ] Addresses career stage appropriately

---

### Dimension 2: Engagement (Weight: 1.5x)
**Question**: Would they read, like, comment, or share this?

| Score | Criteria |
|-------|----------|
| 5 | Shareable insight + specific data/story they'd comment on |
| 4 | Interesting content they'd save for later |
| 3 | Read but unlikely to engage |
| 2 | Skim and move on |
| 1 | Click away immediately |

**Your Score**: _____ × 1.5 = _____

**Engagement Triggers** (from profile patterns):
- [ ] Includes specific data point or surprising stat
- [ ] Has a concrete example or mini case study
- [ ] Uses preferred tone (from communication preferences)

---

[Continue with remaining 8 dimensions: Tone Match, Format Fit, Technical Depth, Actionability, Credibility, Shareability, Time Investment, Professional Value]

---

### TOTAL SCORE: _____ / 50

### Interpretation
- **40-50**: Excellent fit, publish with confidence
- **30-39**: Good fit, minor tweaks recommended
- **20-29**: Moderate fit, needs significant revision
- **<20**: Poor fit, reconsider audience or rewrite

### Action Items (if score < 35)
[Generate specific action items based on persona's evidence tables]

## 11. EXAMPLE CONTENT THAT RESONATES
- Provide 3-5 hypothetical headlines or content topics that would strongly appeal to this persona
- Explain WHY each would resonate

## 12. ANTI-PATTERNS
- List 5 things to NEVER do when creating content for this persona
- Explain the reasoning

## 13. PERSONA METADATA

Include tracking and validation information:

**Created**: [Today's date]
**Version**: 1.0
**Status**: Active

### Data Sources
- **Profiles Analyzed**: {len(profiles)}
- **Data Collection Date**: [Today's date]
- **Confidence Score**: [From evidence analysis]

### Validation Status
| Criterion | Status | Notes |
|-----------|--------|-------|
| Minimum profiles (≥5) | [✅/❌] | {len(profiles)} profiles |
| Data completeness | [✅/⚠️/❌] | [Assessment] |
| Evidence quality | [Score from analysis] | [Notes] |

### Recommended Actions
[List any recommendations to improve persona quality]

### Changelog
- **v1.0** ([Date]): Initial generation from {len(profiles)} LinkedIn profiles

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

    def _generate_evidence_tables(self, profiles: List[Dict[str, Any]]) -> str:
        """Generate statistical evidence from profile data"""
        from collections import Counter

        n = len(profiles)
        evidence = []

        # Analyze titles
        titles = [p.get('headline', '').split('|')[0].split('at')[0].strip() for p in profiles if p.get('headline')]
        title_counts = Counter(titles).most_common(5)

        if title_counts:
            evidence.append("## Title Distribution")
            for title, count in title_counts:
                pct = (count / n) * 100
                evidence.append(f"- {title}: {count}/{n} ({pct:.0f}%)")

        # Analyze industries
        industries = [p.get('industry', '') for p in profiles if p.get('industry')]
        industry_counts = Counter(industries).most_common(5)

        if industry_counts:
            evidence.append("\n## Industry Distribution")
            for industry, count in industry_counts:
                pct = (count / len(industries)) * 100 if industries else 0
                evidence.append(f"- {industry}: {count}/{len(industries)} ({pct:.0f}%)")

        # Analyze locations
        locations = [p.get('location', '') for p in profiles if p.get('location')]
        location_counts = Counter(locations).most_common(5)

        if location_counts:
            evidence.append("\n## Geographic Distribution")
            for location, count in location_counts:
                pct = (count / n) * 100
                evidence.append(f"- {location}: {count}/{n} ({pct:.0f}%)")

        # Analyze skills (aggregate across all profiles)
        all_skills = []
        for p in profiles:
            all_skills.extend(p.get('skills', []))

        skill_counts = Counter(all_skills).most_common(10)

        if skill_counts:
            evidence.append("\n## Top Skills (across all profiles)")
            for skill, count in skill_counts:
                pct = (count / n) * 100
                evidence.append(f"- {skill}: {count}/{n} profiles ({pct:.0f}%)")

        # Analyze education patterns
        degrees = []
        schools = []
        for p in profiles:
            for edu in p.get('education', []):
                if edu.get('degree'):
                    degrees.append(edu['degree'])
                if edu.get('school'):
                    schools.append(edu['school'])

        if degrees:
            evidence.append("\n## Education Patterns")
            degree_counts = Counter(degrees).most_common(5)
            for degree, count in degree_counts:
                evidence.append(f"- {degree}: {count} profiles")

        # Calculate confidence score
        confidence = self._calculate_confidence_score(profiles)
        evidence.append(f"\n## Confidence Score: {confidence:.1f}/10")
        evidence.append(f"Based on {n} profiles analyzed")

        return "\n".join(evidence)

    def _calculate_confidence_score(self, profiles: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on data quality"""
        n = len(profiles)
        score = 0.0

        # Base score from number of profiles
        if n >= 10:
            score += 3.0
        elif n >= 5:
            score += 2.0
        else:
            score += 1.0

        # Score from data completeness
        complete_profiles = sum(1 for p in profiles if p.get('headline') and p.get('experience'))
        completeness_ratio = complete_profiles / n if n > 0 else 0
        score += completeness_ratio * 3.0

        # Score from skill data
        profiles_with_skills = sum(1 for p in profiles if p.get('skills'))
        if profiles_with_skills > 0:
            score += 2.0

        # Score from education data
        profiles_with_education = sum(1 for p in profiles if p.get('education'))
        if profiles_with_education > 0:
            score += 2.0

        return min(score, 10.0)


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
