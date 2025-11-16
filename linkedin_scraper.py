"""
LinkedIn Profile Scraper

Extracts profile information from LinkedIn URLs
Uses Selenium for browser automation to handle LinkedIn's dynamic content
"""

import os
import time
from typing import Dict, Any, Optional, List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class LinkedInScraper:
    """Scraper for LinkedIn profiles"""

    def __init__(self, headless: bool = True):
        """
        Initialize LinkedIn scraper

        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.driver = None

    def _init_driver(self):
        """Initialize Selenium WebDriver"""
        if self.driver:
            return

        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        # Try to use chromedriver from PATH
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"⚠️  Error initializing Chrome driver: {e}")
            print("💡 Install chromedriver with: brew install chromedriver")
            raise

    def _close_driver(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def scrape_profile(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape LinkedIn profile

        Args:
            url: LinkedIn profile URL

        Returns:
            Profile data dictionary
        """
        try:
            self._init_driver()

            print(f"  Loading profile...")
            self.driver.get(url)
            time.sleep(3)  # Wait for page to load

            profile = {
                'url': url,
                'name': self._extract_name(),
                'headline': self._extract_headline(),
                'location': self._extract_location(),
                'about': self._extract_about(),
                'experience': self._extract_experience(),
                'education': self._extract_education(),
                'skills': self._extract_skills(),
                'posts': self._extract_recent_posts(),
            }

            return profile

        except Exception as e:
            print(f"  Error scraping profile: {e}")
            return None

    def _extract_name(self) -> str:
        """Extract profile name"""
        try:
            # Try multiple selectors
            selectors = [
                "h1.text-heading-xlarge",
                "h1.top-card-layout__title",
                "h1[class*='pv-top-card']",
            ]

            for selector in selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    return element.text.strip()
                except NoSuchElementException:
                    continue

            return "Unknown"
        except Exception:
            return "Unknown"

    def _extract_headline(self) -> str:
        """Extract profile headline"""
        try:
            selectors = [
                "div.text-body-medium",
                "div.top-card-layout__headline",
                "div[class*='pv-top-card--experience-list-item']",
            ]

            for selector in selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    return element.text.strip()
                except NoSuchElementException:
                    continue

            return ""
        except Exception:
            return ""

    def _extract_location(self) -> str:
        """Extract location"""
        try:
            selectors = [
                "span.text-body-small.inline",
                "span[class*='top-card__subline-item']",
            ]

            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in elements:
                        text = elem.text.strip()
                        if text and not text.startswith('Contact'):
                            return text
                except NoSuchElementException:
                    continue

            return ""
        except Exception:
            return ""

    def _extract_about(self) -> str:
        """Extract about section"""
        try:
            selectors = [
                "section[data-section='summary'] div.pv-shared-text-with-see-more",
                "section.artdeco-card div.display-flex.ph5.pv3",
                "div[class*='about'] div[class*='text']",
            ]

            for selector in selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    return element.text.strip()
                except NoSuchElementException:
                    continue

            return ""
        except Exception:
            return ""

    def _extract_experience(self) -> List[Dict[str, str]]:
        """Extract experience section"""
        experiences = []
        try:
            # Look for experience section
            exp_section = self.driver.find_element(By.ID, "experience")
            if not exp_section:
                return experiences

            # Find all experience entries
            exp_items = self.driver.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")

            for item in exp_items[:5]:  # Get top 5 experiences
                try:
                    title = item.find_element(By.CSS_SELECTOR, "div[class*='experience-item__title']").text.strip()
                    company = item.find_element(By.CSS_SELECTOR, "span[class*='experience-item__subtitle']").text.strip()
                    duration = item.find_element(By.CSS_SELECTOR, "span[class*='date-range']").text.strip()

                    experiences.append({
                        'title': title,
                        'company': company,
                        'duration': duration,
                    })
                except NoSuchElementException:
                    continue

        except Exception:
            pass

        return experiences

    def _extract_education(self) -> List[Dict[str, str]]:
        """Extract education section"""
        education = []
        try:
            # Look for education section
            edu_section = self.driver.find_element(By.ID, "education")
            if not edu_section:
                return education

            # Find all education entries
            edu_items = self.driver.find_elements(By.CSS_SELECTOR, "li.artdeco-list__item")

            for item in edu_items[:3]:  # Get top 3
                try:
                    school = item.find_element(By.CSS_SELECTOR, "span[class*='education__school-name']").text.strip()
                    degree = item.find_element(By.CSS_SELECTOR, "span[class*='education__degree']").text.strip()

                    education.append({
                        'school': school,
                        'degree': degree,
                    })
                except NoSuchElementException:
                    continue

        except Exception:
            pass

        return education

    def _extract_skills(self) -> List[str]:
        """Extract skills"""
        skills = []
        try:
            # Look for skills section
            skills_section = self.driver.find_element(By.ID, "skills")
            if not skills_section:
                return skills

            # Find skill items
            skill_items = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='skill-item']")

            for item in skill_items[:10]:  # Get top 10 skills
                try:
                    skill = item.find_element(By.CSS_SELECTOR, "span[class*='skill-name']").text.strip()
                    if skill:
                        skills.append(skill)
                except NoSuchElementException:
                    continue

        except Exception:
            pass

        return skills

    def _extract_recent_posts(self) -> List[Dict[str, str]]:
        """Extract recent activity/posts"""
        posts = []
        try:
            # Scroll to activity section
            activity_section = self.driver.find_element(By.ID, "activity")
            if activity_section:
                self.driver.execute_script("arguments[0].scrollIntoView();", activity_section)
                time.sleep(2)

                # Find recent posts
                post_items = self.driver.find_elements(By.CSS_SELECTOR, "div[class*='feed-shared-update-v2']")

                for item in post_items[:3]:  # Get last 3 posts
                    try:
                        text = item.find_element(By.CSS_SELECTOR, "span[class*='break-words']").text.strip()
                        if text:
                            posts.append({'text': text[:500]})  # Limit to 500 chars
                    except NoSuchElementException:
                        continue

        except Exception:
            pass

        return posts

    def __del__(self):
        """Cleanup driver on deletion"""
        self._close_driver()
