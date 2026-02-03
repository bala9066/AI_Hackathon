"""
Demo script for Playwright integration in AI Hardware Pipeline.
Shows how to use browser automation for component scraping.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright_utils import ComponentScraper, BrowserAutomation
import json


def demo_basic_navigation():
    """Demo: Basic browser navigation and screenshot."""
    print("\n=== Demo: Basic Navigation ===")
    
    with BrowserAutomation(headless=True) as browser:
        page = browser.new_page()
        
        # Navigate to a page
        browser.navigate(page, "https://www.digikey.com")
        
        # Take a screenshot
        screenshot_path = os.path.join(os.path.dirname(__file__), "..", "output", "digikey_homepage.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        browser.screenshot(page, screenshot_path)
        
        # Get the page title
        title = page.title()
        print(f"Page title: {title}")
        print(f"Screenshot saved to: {screenshot_path}")
        
        page.close()


def demo_component_search():
    """Demo: Search for components across suppliers."""
    print("\n=== Demo: Component Search ===")
    
    # Initialize scraper
    scraper = ComponentScraper(
        headless=True,           # Run without visible browser
        delay_between_requests=2  # Be respectful of rate limits
    )
    
    # Search for a component
    keywords = "STM32F407"
    print(f"Searching for: {keywords}")
    
    # Search individual suppliers
    print("\nSearching DigiKey...")
    digikey_results = scraper.search_digikey(keywords, max_results=3)
    print(f"Found {len(digikey_results)} results on DigiKey")
    
    for comp in digikey_results:
        print(f"  - {comp.part_number}: ${comp.unit_price} ({comp.stock} in stock)")
    
    return digikey_results


def demo_table_extraction():
    """Demo: Extract table data from a webpage."""
    print("\n=== Demo: Table Extraction ===")
    
    with BrowserAutomation(headless=True) as browser:
        page = browser.new_page()
        
        # Navigate to any page with a table (example)
        browser.navigate(page, "https://www.w3schools.com/html/html_tables.asp")
        
        # Extract table data
        table_data = browser.extract_table_data(page, "table")
        
        print(f"Extracted {len(table_data)} rows from table")
        for row in table_data[:3]:
            print(f"  {row}")
        
        page.close()


def demo_fill_form():
    """Demo: Fill a search form."""
    print("\n=== Demo: Form Filling ===")
    
    with BrowserAutomation(headless=True) as browser:
        page = browser.new_page()
        
        browser.navigate(page, "https://www.mouser.com")
        
        # Find and fill search box
        try:
            search_selector = '#searchInput, [name="keyword"], input[type="search"]'
            browser.fill(page, search_selector, "LM7805")
            print("Filled search box with 'LM7805'")
            
            # Press Enter to search
            page.keyboard.press("Enter")
            page.wait_for_load_state("networkidle")
            
            print(f"Current URL: {page.url}")
        except Exception as e:
            print(f"Form fill demo skipped: {e}")
        
        page.close()


def main():
    """Run all demos."""
    print("=" * 60)
    print("Playwright Integration Demo for AI Hardware Pipeline")
    print("=" * 60)
    
    # Run demos
    try:
        demo_basic_navigation()
    except Exception as e:
        print(f"Basic navigation demo failed: {e}")
    
    try:
        demo_table_extraction()
    except Exception as e:
        print(f"Table extraction demo failed: {e}")
    
    try:
        demo_fill_form()
    except Exception as e:
        print(f"Form fill demo failed: {e}")
    
    # Component search - may take longer
    try:
        components = demo_component_search()
        
        # Export results
        if components:
            output_path = os.path.join(os.path.dirname(__file__), "..", "output", "demo_components.json")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w') as f:
                json.dump([c.to_dict() for c in components], f, indent=2)
            print(f"\nComponents exported to: {output_path}")
    except Exception as e:
        print(f"Component search demo failed: {e}")
    
    print("\n" + "=" * 60)
    print("Demos complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
