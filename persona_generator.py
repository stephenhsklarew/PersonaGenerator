#!/usr/bin/env python3
"""
PersonaGenerator - Generate comprehensive personas from LinkedIn profiles

Usage:
    python3 persona_generator.py --urls urls.txt
    python3 persona_generator.py --urls "https://linkedin.com/in/user1,https://linkedin.com/in/user2"
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import json

from linkedin_scraper import LinkedInScraper
from persona_synthesizer import PersonaSynthesizer


class PersonaGenerator:
    """Main orchestrator for persona generation"""

    def __init__(self, output_dir: str = "./output"):
        """
        Initialize PersonaGenerator

        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.scraper = LinkedInScraper()
        self.synthesizer = PersonaSynthesizer()

    def generate_from_urls(self, urls: List[str], persona_name: str = "composite_persona") -> str:
        """
        Generate persona from list of LinkedIn URLs

        Args:
            urls: List of LinkedIn profile URLs
            persona_name: Name for the generated persona

        Returns:
            Path to generated persona.md file
        """
        print(f"🚀 PersonaGenerator - Processing {len(urls)} LinkedIn profiles")
        print("=" * 60)

        # Step 1: Scrape LinkedIn profiles
        profiles = []
        for i, url in enumerate(urls, 1):
            print(f"\n📊 [{i}/{len(urls)}] Scraping: {url}")
            try:
                profile = self.scraper.scrape_profile(url)
                if profile:
                    profiles.append(profile)
                    print(f"✅ Scraped: {profile.get('name', 'Unknown')}")
                else:
                    print(f"⚠️  Failed to scrape profile")
            except Exception as e:
                print(f"❌ Error scraping {url}: {e}")

        if not profiles:
            print("\n❌ No profiles were successfully scraped")
            return None

        print(f"\n✅ Successfully scraped {len(profiles)} profiles")

        # Save raw profile data
        profiles_file = self.output_dir / f"{persona_name}_profiles.json"
        with open(profiles_file, 'w') as f:
            json.dump(profiles, f, indent=2)
        print(f"💾 Saved profile data: {profiles_file}")

        # Step 2: Synthesize persona
        print(f"\n🤖 Synthesizing composite persona...")
        persona_md = self.synthesizer.synthesize_persona(profiles, persona_name)

        # Save persona markdown
        persona_file = self.output_dir / f"{persona_name}.md"
        with open(persona_file, 'w') as f:
            f.write(persona_md)
        print(f"✅ Generated persona: {persona_file}")

        print("\n" + "=" * 60)
        print(f"✨ Persona generation complete!")
        print(f"📄 Persona file: {persona_file}")
        print(f"📊 Profile data: {profiles_file}")
        print("=" * 60)

        return str(persona_file)


def parse_urls(url_input: str) -> List[str]:
    """
    Parse URLs from file or comma-separated string

    Args:
        url_input: Path to file with URLs or comma-separated URL string

    Returns:
        List of URLs
    """
    # Check if it's a file
    if os.path.isfile(url_input):
        with open(url_input, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    else:
        # Assume comma-separated string
        urls = [u.strip() for u in url_input.split(',') if u.strip()]

    # Validate URLs
    valid_urls = []
    for url in urls:
        if 'linkedin.com/in/' in url:
            valid_urls.append(url)
        else:
            print(f"⚠️  Skipping invalid LinkedIn URL: {url}")

    return valid_urls


def main():
    parser = argparse.ArgumentParser(
        description="Generate comprehensive personas from LinkedIn profiles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From file
  python3 persona_generator.py --urls urls.txt

  # From command line
  python3 persona_generator.py --urls "https://linkedin.com/in/user1,https://linkedin.com/in/user2"

  # Custom output directory and name
  python3 persona_generator.py --urls urls.txt --output ./personas --name executive_persona
        """
    )

    parser.add_argument(
        '--urls',
        required=True,
        help='Path to file with LinkedIn URLs (one per line) or comma-separated URLs'
    )

    parser.add_argument(
        '--output',
        default='./output',
        help='Output directory for generated files (default: ./output)'
    )

    parser.add_argument(
        '--name',
        default='composite_persona',
        help='Name for the generated persona (default: composite_persona)'
    )

    args = parser.parse_args()

    # Parse URLs
    urls = parse_urls(args.urls)

    if not urls:
        print("❌ No valid LinkedIn URLs found")
        sys.exit(1)

    # Generate persona
    generator = PersonaGenerator(output_dir=args.output)
    persona_file = generator.generate_from_urls(urls, persona_name=args.name)

    if persona_file:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
