"""
Test script for Playwright installation and basic functionality.
Run this to verify Playwright is working correctly.
"""

import sys
from playwright.sync_api import sync_playwright


def test_playwright():
    """Test basic Playwright functionality."""
    print("Testing Playwright installation...")
    
    try:
        with sync_playwright() as p:
            # Test Chromium
            print("  Launching Chromium browser...")
            browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()
            print("  Navigating to example.com...")
            page.goto("https://example.com")
            
            title = page.title()
            print(f"  Page title: {title}")
            
            # Verify it worked
            assert "Example" in title, f"Unexpected title: {title}"
            
            browser.close()
            print("\n✅ Playwright is working correctly!")
            return True
            
    except Exception as e:
        print(f"\n❌ Playwright test failed: {e}")
        print("\nTry running: playwright install chromium")
        return False


def test_component_scraper():
    """Test component scraper import."""
    print("\nTesting component scraper module...")
    
    try:
        import sys
        import os
        # Add parent directory to path for imports
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        
        from playwright_utils import ComponentScraper, BrowserAutomation
        print("  ✅ Imports successful")
        
        scraper = ComponentScraper(headless=True)
        print("  ✅ ComponentScraper initialized")
        
        return True
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Playwright Integration Test")
    print("=" * 50)
    
    pw_ok = test_playwright()
    scraper_ok = test_component_scraper()
    
    print("\n" + "=" * 50)
    if pw_ok and scraper_ok:
        print("All tests passed! ✅")
        sys.exit(0)
    else:
        print("Some tests failed. ❌")
        sys.exit(1)
