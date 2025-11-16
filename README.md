# PersonaGenerator

Generate comprehensive, AI-powered audience personas from LinkedIn profiles.

## Overview

PersonaGenerator analyzes LinkedIn profiles and uses AI to synthesize detailed composite personas that include:

- **Demographic & Professional Profile** - Roles, industries, career stage, education
- **Goals & Motivations** - What drives them professionally and personally
- **Pain Points & Challenges** - Problems they face and constraints they work under
- **Behaviors & Habits** - Daily routines, decision-making style, technology adoption
- **Communication Preferences** - Tone, formats, detail level, reading time
- **Content Engagement Patterns** - Topics of interest, sharing behavior, engagement triggers
- **Skills & Expertise** - Core competencies and learning priorities
- **Content Testing Framework** - Actionable scores to test content relevance

## Perfect For

- **Content Creators**: Test if your content will resonate with your target audience
- **Marketers**: Understand your ideal customer profile at a deep level
- **Product Managers**: Validate feature ideas against user personas
- **Sales Teams**: Better understand decision-makers and their pain points
- **Founders**: Define and understand your target market

## Features

✅ Scrapes public LinkedIn profile data (no API key required)
✅ Uses AI to synthesize composite personas from multiple profiles
✅ Generates actionable markdown personas with 12 detailed sections
✅ Supports multiple AI models (Qwen/free, GPT-4, Claude, Gemini)
✅ Saves raw profile data for future reference
✅ CLI-friendly for automation

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Chrome browser** (for Selenium)
3. **ChromeDriver** - Install with:
   ```bash
   brew install chromedriver
   ```
4. **UnifiedLLMClient** - Must be available at `~/Development/Scripts/UnifiedLLMClient`

### Setup

```bash
# Navigate to directory
cd ~/Development/Scripts/PersonaGenerator

# Install dependencies
pip3 install -r requirements.txt

# Copy environment template
cp .env.example .env

# Add your API keys to .env
# For free option, use Qwen (no API key needed)
```

## Usage

### Basic Usage

```bash
# From a file with URLs (one per line)
python3 persona_generator.py --urls sample_urls.txt

# From command line (comma-separated)
python3 persona_generator.py --urls "https://linkedin.com/in/user1,https://linkedin.com/in/user2,https://linkedin.com/in/user3"
```

### Advanced Options

```bash
# Custom output directory
python3 persona_generator.py --urls urls.txt --output ./personas

# Custom persona name
python3 persona_generator.py --urls urls.txt --name "enterprise_cto_persona"

# Full example
python3 persona_generator.py \
  --urls executive_urls.txt \
  --output ./output/executives \
  --name c_suite_persona
```

## Input Format

Create a text file with LinkedIn URLs (one per line):

```text
# executive_urls.txt
https://www.linkedin.com/in/sarah-chen-tech-vp/
https://www.linkedin.com/in/john-smith-cto/
https://www.linkedin.com/in/maria-garcia-engineering-director/
https://www.linkedin.com/in/david-kumar-head-of-product/
https://www.linkedin.com/in/jennifer-liu-vp-operations/
```

**Tips:**
- Include 3-10 profiles for best results
- Choose profiles that represent your target audience
- More profiles = more accurate composite persona
- Profiles should share similar characteristics (role, industry, seniority)

## Output

PersonaGenerator creates two files:

### 1. `{name}_profiles.json`
Raw scraped data from all LinkedIn profiles for reference.

### 2. `{name}.md`
Complete persona document with 12 sections:

1. **Persona Overview** - Name, archetype, summary
2. **Demographics & Professional Profile** - Roles, industries, education
3. **Goals & Motivations** - What they're trying to achieve
4. **Pain Points & Challenges** - Problems they face
5. **Behaviors & Habits** - Daily routines, decision-making
6. **Communication Preferences** - Tone, formats, reading time
7. **Content Engagement Patterns** - Topics, sharing behavior
8. **Professional Context** - Reporting structure, buying authority
9. **Skills & Expertise** - Competencies and knowledge areas
10. **Content Testing Framework** - Relevance, engagement, action scores
11. **Example Content That Resonates** - Specific headlines/topics
12. **Anti-Patterns** - What NOT to do

## Example Output

```markdown
# Persona: Tech Executive

## 1. PERSONA OVERVIEW

**Name**: Tech Executive
**Archetype**: Strategic Technical Leader
**One-line Summary**: Senior technology leaders who balance technical excellence with business strategy, leading engineering teams at high-growth companies.

## 2. DEMOGRAPHICS & PROFESSIONAL PROFILE

**Typical Roles/Titles**:
- VP of Engineering
- Chief Technology Officer (CTO)
- Head of Product Engineering
- Director of Engineering
- VP of Technology

**Industries**: SaaS, fintech, e-commerce, enterprise software...

[... continues with 10 more sections ...]
```

## How It Works

```
┌─────────────────────┐
│  LinkedIn URLs      │
│  (input file)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  LinkedIn Scraper   │
│  (Selenium)         │
│  - Name             │
│  - Headline         │
│  - About            │
│  - Experience       │
│  - Education        │
│  - Skills           │
│  - Recent posts     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Profile Data       │
│  (JSON)             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  AI Synthesizer     │
│  (UnifiedLLMClient) │
│  - Pattern analysis │
│  - Persona creation │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  persona.md         │
│  (Output)           │
└─────────────────────┘
```

## AI Model Options

Configure in `.env` or via UnifiedLLMClient:

- **qwen** (default, free) - Good quality, no API key needed
- **gpt-4o** - High quality, requires OpenAI API key
- **claude-3-5-sonnet** - Excellent quality, requires Anthropic API key
- **gemini-1.5-pro** - Good quality, requires Google API key

## Best Practices

### For Better Personas:

1. **Use 5-10 profiles** - More data = better synthesis
2. **Choose similar profiles** - Same industry, role level, or target segment
3. **Review the output** - AI-generated, but should be human-validated
4. **Update regularly** - Personas should evolve with your market

### For Content Testing:

Use the generated persona to evaluate content:

1. **Relevance Check**: Does this solve their problems?
2. **Engagement Check**: Would they read, like, or share?
3. **Action Check**: Would they take the next step?
4. **Red Flag Check**: Does it trigger any anti-patterns?

## Limitations

- **Public Data Only**: Can only scrape publicly visible LinkedIn information
- **LinkedIn Changes**: Scraper may break if LinkedIn changes their HTML structure
- **Rate Limiting**: Be respectful of LinkedIn - don't scrape too many profiles at once
- **Authentication**: Does not use LinkedIn API (which requires auth)
- **Accuracy**: AI synthesis is based on patterns, not guaranteed predictions

## Troubleshooting

### ChromeDriver Not Found
```bash
brew install chromedriver
# Or download from: https://chromedriver.chromium.org/
```

### UnifiedLLMClient Not Found
```bash
# Ensure UnifiedLLMClient is installed at:
~/Development/Scripts/UnifiedLLMClient
```

### LinkedIn Blocking
If you get blocked:
- Wait a few hours before retrying
- Use fewer profiles per session
- Consider using LinkedIn Premium
- Use VPN if needed

### Selenium Errors
```bash
# Update Selenium
pip3 install --upgrade selenium webdriver-manager

# Try non-headless mode for debugging
# Edit linkedin_scraper.py: headless=False
```

## Examples

### Example 1: SaaS Executive Persona
```bash
python3 persona_generator.py \
  --urls saas_execs.txt \
  --name saas_executive_persona
```

### Example 2: Developer Persona
```bash
python3 persona_generator.py \
  --urls developer_profiles.txt \
  --name full_stack_developer_persona
```

### Example 3: Marketing Leader Persona
```bash
python3 persona_generator.py \
  --urls marketing_leaders.txt \
  --output ./marketing_personas \
  --name cmo_persona
```

## Integration with Other Tools

### Use with AgenticContentGenerator

Generated personas can be used to test content from AgenticContentGenerator:

```bash
# 1. Generate persona
cd ~/Development/Scripts/PersonaGenerator
python3 persona_generator.py --urls exec_urls.txt --name exec_persona

# 2. Use persona to evaluate content
cd ~/Development/Scripts/AgenticContentGenerator
# Reference persona.md when reviewing generated topics/documents
```

### Use with ContentScorer

Add persona-based scoring criteria to evaluate content fit.

## Project Structure

```
PersonaGenerator/
├── README.md                    # This file
├── persona_generator.py         # Main CLI script
├── linkedin_scraper.py          # Selenium-based LinkedIn scraper
├── persona_synthesizer.py       # AI-powered persona synthesis
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── sample_urls.txt              # Example input file
└── output/                      # Generated personas (auto-created)
    ├── {name}_profiles.json     # Raw profile data
    └── {name}.md                # Persona document
```

## Contributing

Suggestions and improvements welcome! This tool is part of the Qwilo content generation ecosystem.

## License

MIT License - Use freely for personal and commercial projects.

## Related Tools

Part of the Qwilo content generation toolkit:
- **UnifiedLLMClient** - AI provider abstraction
- **AgenticContentGenerator** - Multi-agent content pipeline
- **WritingStylePromptGenerator** - Personal writing style capture

---

**Created by**: Stephen Sklarew
**Part of**: Qwilo Content Generation Ecosystem
**Repository**: ~/Development/Scripts/PersonaGenerator
