# PersonaGenerator - Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies

```bash
cd ~/Development/Scripts/PersonaGenerator
./install.sh
```

### 2. Test It Works

```bash
./test_persona.sh
```

This generates a test persona from sample data. View it:

```bash
cat output/test_persona.md
```

### 3. Add Your LinkedIn URLs

Edit `sample_urls.txt`:

```bash
nano sample_urls.txt
```

Add real LinkedIn profile URLs (one per line):

```
https://www.linkedin.com/in/username1/
https://www.linkedin.com/in/username2/
https://www.linkedin.com/in/username3/
```

**Tip**: Use 5-10 profiles that represent your target audience.

### 4. Generate Your Persona

```bash
python3 persona_generator.py --urls sample_urls.txt --name my_target_audience
```

### 5. View Results

```bash
# View the persona
cat output/my_target_audience.md

# View raw profile data
cat output/my_target_audience_profiles.json
```

## Common Use Cases

### Marketing Team: Understand Your ICP

```bash
# 1. Gather LinkedIn URLs of 5-10 customers
# 2. Create customer_urls.txt
# 3. Generate persona
python3 persona_generator.py --urls customer_urls.txt --name ideal_customer

# 4. Use persona to test marketing copy
```

### Content Creator: Know Your Audience

```bash
# 1. Find LinkedIn profiles of people who engage with your content
# 2. Create audience_urls.txt
# 3. Generate persona
python3 persona_generator.py --urls audience_urls.txt --name content_consumer

# 4. Reference persona when creating new content
```

### Product Manager: Define User Personas

```bash
# 1. Gather URLs of target users in each segment
# 2. Generate persona for each segment
python3 persona_generator.py --urls enterprise_urls.txt --name enterprise_admin
python3 persona_generator.py --urls smb_urls.txt --name smb_owner

# 3. Use personas for feature prioritization
```

### Sales Team: Understand Decision Makers

```bash
# 1. Collect URLs of successful deals' decision makers
# 2. Generate buyer persona
python3 persona_generator.py --urls buyers_urls.txt --name enterprise_buyer

# 3. Reference persona in sales conversations
```

## What You Get

### Output Files

1. **`{name}.md`** - Complete persona document with:
   - Demographics & professional profile
   - Goals & motivations
   - Pain points & challenges
   - Communication preferences
   - Content engagement patterns
   - Content testing framework
   - Example headlines that resonate
   - Anti-patterns to avoid

2. **`{name}_profiles.json`** - Raw scraped data for reference

### Persona Sections

The generated persona includes **12 comprehensive sections**:

1. Persona Overview
2. Demographics & Professional Profile
3. Goals & Motivations
4. Pain Points & Challenges
5. Behaviors & Habits
6. Communication Preferences
7. Content Engagement Patterns
8. Professional Context
9. Skills & Expertise
10. Content Testing Framework ⭐
11. Example Content That Resonates ⭐
12. Anti-Patterns ⭐

⭐ = Especially useful for content testing

## Content Testing Workflow

Once you have a persona, use it to evaluate content:

```bash
# 1. Generate persona
python3 persona_generator.py --urls urls.txt --name target_persona

# 2. Open persona.md
open output/target_persona.md

# 3. For each piece of content, ask:
# - Does it solve their pain points? (Section 4)
# - Does it match their communication preferences? (Section 6)
# - Would it trigger engagement? (Section 7)
# - Does it avoid anti-patterns? (Section 12)

# 4. Score your content using the framework (Section 10):
# - Relevance: 1-10
# - Engagement: 1-10
# - Action: 1-10
```

## Tips for Better Results

### Choose the Right Profiles

✅ **Do**:
- Use 5-10 profiles minimum
- Select profiles with similar characteristics
- Include decision-makers from your target segment
- Use recent, active profiles

❌ **Don't**:
- Mix vastly different roles (CEO + intern)
- Use outdated or inactive profiles
- Include too few profiles (< 3)
- Use profiles from irrelevant industries

### AI Model Selection

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| Qwen (default) | Fast | Good | Free | Testing, iteration |
| GPT-4o | Medium | Excellent | $$ | Production personas |
| Claude Sonnet | Medium | Excellent | $$ | Detailed analysis |
| Gemini Pro | Fast | Very Good | $ | Balanced option |

To use premium models, add API keys to `.env`:

```bash
# Edit .env file
nano .env

# Add your key
ANTHROPIC_API_KEY=your_key_here
# or
OPENAI_API_KEY=your_key_here
```

## Troubleshooting

### "ChromeDriver not found"

```bash
brew install chromedriver
```

### "UnifiedLLMClient not found"

Ensure UnifiedLLMClient is at:
```
~/Development/Scripts/UnifiedLLMClient/
```

### LinkedIn Scraping Issues

- **Rate limited**: Wait a few hours, use fewer profiles
- **Access denied**: LinkedIn may block automated access
- **Incomplete data**: Some profiles have privacy settings

### No API Key Needed!

**Qwen model is free** and works without any API key. Just run:

```bash
python3 persona_generator.py --urls urls.txt
```

## Next Steps

1. **Generate your first persona** using real LinkedIn URLs
2. **Test existing content** against the persona
3. **Create new content** guided by persona insights
4. **Iterate and refine** as your audience evolves

## Need Help?

- Read the full `README.md` for detailed documentation
- Check the `test_persona.sh` output for a working example
- Review `persona_synthesizer.py` to understand the AI prompt

---

**Happy persona building!** 🎯
