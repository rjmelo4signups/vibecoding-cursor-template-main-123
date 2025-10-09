# Job Scraper - BambooHR Careers Page (Improved Version)
# This program opens a browser, goes to the BambooHR jobs page, and scrapes job listings
# Uses multiple strategies to find job listings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def scrape_jobs():
    """
    Opens a browser, navigates to BambooHR careers page, and scrapes job listings
    Uses multiple strategies to find jobs on the page
    """
    print("Starting improved job scraper...")
    
    # Create a new browser window
    driver = webdriver.Chrome()
    
    try:
        # Navigate to the BambooHR careers page
        print("Opening BambooHR careers page...")
        driver.get("https://people.bamboohr.com/careers")
        
        # Wait for the page to load completely
        print("Waiting for page to load...")
        time.sleep(5)
        
        # Get page information for debugging
        print(f"Page title: {driver.title}")
        print(f"Current URL: {driver.current_url}")
        
        # Strategy 1: Look for common job-related text patterns
        print("\n=== Strategy 1: Looking for job-related text ===")
        page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
        
        # Look for job-related keywords
        job_keywords = ['engineer', 'developer', 'manager', 'analyst', 'coordinator', 'specialist', 'director', 'lead', 'senior', 'junior']
        found_keywords = [keyword for keyword in job_keywords if keyword in page_text]
        print(f"Found job-related keywords: {found_keywords}")
        
        # Strategy 2: Look for links that might be job postings
        print("\n=== Strategy 2: Looking for job links ===")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        job_links = []
        
        for link in all_links:
            try:
                href = link.get_attribute("href")
                text = link.text.strip()
                
                # Look for links that might be jobs
                if href and any(keyword in text.lower() for keyword in job_keywords):
                    job_links.append(f"Link: {text} -> {href}")
                    print(f"Found potential job link: {text[:50]}...")
            except:
                continue
        
        # Strategy 3: Look for elements with job-related classes or IDs
        print("\n=== Strategy 3: Looking for job elements ===")
        job_selectors = [
            "[class*='job']", "[class*='position']", "[class*='career']", "[class*='opening']",
            "[id*='job']", "[id*='position']", "[id*='career']", "[id*='opening']",
            "div[class*='card']", "div[class*='item']", "div[class*='listing']"
        ]
        
        all_job_elements = []
        for selector in job_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                all_job_elements.extend(elements)
                if elements:
                    print(f"Found {len(elements)} elements with selector: {selector}")
            except:
                continue
        
        # Strategy 4: Look for any text that looks like job titles
        print("\n=== Strategy 4: Looking for job title patterns ===")
        all_text_elements = driver.find_elements(By.XPATH, "//*[text()]")
        potential_jobs = []
        
        for element in all_text_elements:
            try:
                text = element.text.strip()
                # Look for text that might be job titles (2-5 words, title case)
                if (len(text.split()) >= 2 and len(text.split()) <= 5 and 
                    text.istitle() and 
                    any(keyword in text.lower() for keyword in job_keywords)):
                    potential_jobs.append(text)
            except:
                continue
        
        # Remove duplicates and show results
        unique_potential_jobs = list(set(potential_jobs))
        print(f"Found {len(unique_potential_jobs)} potential job titles:")
        for i, job in enumerate(unique_potential_jobs[:10]):  # Show first 10
            print(f"  {i+1}. {job}")
        
        # Strategy 5: Look for any clickable elements that might be jobs
        print("\n=== Strategy 5: Looking for clickable job elements ===")
        clickable_elements = driver.find_elements(By.XPATH, "//*[@onclick or @href or @role='button']")
        clickable_jobs = []
        
        for element in clickable_elements:
            try:
                text = element.text.strip()
                if (text and len(text) > 5 and len(text) < 100 and 
                    any(keyword in text.lower() for keyword in job_keywords)):
                    clickable_jobs.append(text)
            except:
                continue
        
        # Combine all findings
        all_findings = []
        
        if job_links:
            all_findings.extend([f"LINK: {link}" for link in job_links])
        
        if unique_potential_jobs:
            all_findings.extend([f"TITLE: {job}" for job in unique_potential_jobs])
        
        if clickable_jobs:
            all_findings.extend([f"CLICKABLE: {job}" for job in clickable_jobs])
        
        # Save all findings
        if all_findings:
            print(f"\n=== SUMMARY: Found {len(all_findings)} potential job listings ===")
            
            with open("scraped_jobs.txt", "w", encoding="utf-8") as f:
                f.write("BambooHR Job Listings - Improved Scraper\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Page Title: {driver.title}\n")
                f.write(f"Page URL: {driver.current_url}\n")
                f.write(f"Total findings: {len(all_findings)}\n\n")
                
                for i, finding in enumerate(all_findings, 1):
                    f.write(f"{i}. {finding}\n")
                    print(f"{i}. {finding}")
            
            print(f"\nAll findings saved to 'scraped_jobs.txt'")
            
        else:
            print("\n=== No job listings found with any strategy ===")
            print("This might mean:")
            print("1. The page uses JavaScript to load jobs dynamically")
            print("2. Jobs are loaded from an external API")
            print("3. The page structure is very different")
            
            # Save page source for manual inspection
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Page source saved to 'page_source.html' for manual inspection")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Close the browser
        print("\nClosing browser...")
        driver.quit()

if __name__ == "__main__":
    scrape_jobs()
