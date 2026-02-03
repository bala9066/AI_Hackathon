"""
Browser Automation Module for AI Hardware Pipeline
Uses Playwright for headless browser automation tasks.
"""

import asyncio
from playwright.async_api import async_playwright, Browser, Page
from playwright.sync_api import sync_playwright
from typing import Optional, Dict, Any, List
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BrowserAutomation:
    """
    Core browser automation class using Playwright.
    Supports both sync and async operations.
    """
    
    def __init__(self, headless: bool = True, slow_mo: int = 0):
        """
        Initialize browser automation.
        
        Args:
            headless: Run browser in headless mode (default: True)
            slow_mo: Slow down operations by specified milliseconds (for debugging)
        """
        self.headless = headless
        self.slow_mo = slow_mo
        self._browser: Optional[Browser] = None
        self._playwright = None
    
    def __enter__(self):
        """Context manager entry - sync mode."""
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - sync mode."""
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
    
    async def __aenter__(self):
        """Async context manager entry."""
        self._playwright = await async_playwright().start()
        self._browser = await self._playwright.chromium.launch(
            headless=self.headless,
            slow_mo=self.slow_mo
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
    
    def new_page(self) -> Page:
        """Create a new browser page (sync mode)."""
        return self._browser.new_page()
    
    async def new_page_async(self) -> Page:
        """Create a new browser page (async mode)."""
        return await self._browser.new_page()
    
    def navigate(self, page: Page, url: str, wait_until: str = "networkidle") -> None:
        """
        Navigate to a URL (sync mode).
        
        Args:
            page: Browser page
            url: URL to navigate to
            wait_until: Wait condition ('load', 'domcontentloaded', 'networkidle')
        """
        page.goto(url, wait_until=wait_until)
        logger.info(f"Navigated to: {url}")
    
    async def navigate_async(self, page: Page, url: str, wait_until: str = "networkidle") -> None:
        """Navigate to a URL (async mode)."""
        await page.goto(url, wait_until=wait_until)
        logger.info(f"Navigated to: {url}")
    
    def screenshot(self, page: Page, path: str, full_page: bool = True) -> str:
        """
        Take a screenshot of the current page.
        
        Args:
            page: Browser page
            path: Output file path
            full_page: Capture full scrollable page
        
        Returns:
            Path to saved screenshot
        """
        page.screenshot(path=path, full_page=full_page)
        logger.info(f"Screenshot saved: {path}")
        return path
    
    def get_page_content(self, page: Page) -> str:
        """Get full HTML content of page."""
        return page.content()
    
    def get_text(self, page: Page, selector: str) -> str:
        """Get text content of an element."""
        element = page.query_selector(selector)
        return element.text_content() if element else ""
    
    def get_all_text(self, page: Page, selector: str) -> List[str]:
        """Get text content of all matching elements."""
        elements = page.query_selector_all(selector)
        return [el.text_content() for el in elements if el]
    
    def click(self, page: Page, selector: str, timeout: int = 30000) -> None:
        """Click an element."""
        page.click(selector, timeout=timeout)
        logger.info(f"Clicked: {selector}")
    
    def fill(self, page: Page, selector: str, value: str) -> None:
        """Fill a form field."""
        page.fill(selector, value)
        logger.info(f"Filled {selector} with value")
    
    def wait_for_selector(self, page: Page, selector: str, timeout: int = 30000) -> None:
        """Wait for an element to appear."""
        page.wait_for_selector(selector, timeout=timeout)
    
    def evaluate(self, page: Page, expression: str) -> Any:
        """Execute JavaScript in the page context."""
        return page.evaluate(expression)
    
    def extract_table_data(self, page: Page, table_selector: str) -> List[Dict[str, str]]:
        """
        Extract data from an HTML table.
        
        Args:
            page: Browser page
            table_selector: CSS selector for the table
        
        Returns:
            List of dictionaries with table data
        """
        return page.evaluate(f"""
            () => {{
                const table = document.querySelector('{table_selector}');
                if (!table) return [];
                
                const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent.trim());
                const rows = Array.from(table.querySelectorAll('tbody tr'));
                
                return rows.map(row => {{
                    const cells = Array.from(row.querySelectorAll('td'));
                    const rowData = {{}};
                    cells.forEach((cell, index) => {{
                        const header = headers[index] || `col_${{index}}`;
                        rowData[header] = cell.textContent.trim();
                    }});
                    return rowData;
                }});
            }}
        """)


# Convenience function for quick operations
def run_browser_task(task_func, headless: bool = True):
    """
    Run a browser task with automatic setup/teardown.
    
    Usage:
        def my_task(browser):
            page = browser.new_page()
            browser.navigate(page, "https://example.com")
            return page.title()
        
        result = run_browser_task(my_task)
    """
    with BrowserAutomation(headless=headless) as browser:
        return task_func(browser)


# Async version
async def run_browser_task_async(task_func, headless: bool = True):
    """Run a browser task asynchronously."""
    async with BrowserAutomation(headless=headless) as browser:
        return await task_func(browser)
