"""
Component Scraper Module for AI Hardware Pipeline
Scrapes electronic component data from supplier websites.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from .browser_automation import BrowserAutomation, run_browser_task
import json
import logging
import re
import time

logger = logging.getLogger(__name__)


@dataclass
class ComponentInfo:
    """Data class for component information."""
    part_number: str
    manufacturer: str
    description: str
    unit_price: float
    stock: int
    datasheet_url: str
    supplier: str
    supplier_part_number: str
    category: str = ""
    specifications: Dict[str, str] = None
    
    def __post_init__(self):
        if self.specifications is None:
            self.specifications = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "part_number": self.part_number,
            "manufacturer": self.manufacturer,
            "description": self.description,
            "unit_price": self.unit_price,
            "stock": self.stock,
            "datasheet_url": self.datasheet_url,
            "supplier": self.supplier,
            "supplier_part_number": self.supplier_part_number,
            "category": self.category,
            "specifications": self.specifications
        }


class ComponentScraper:
    """
    Scrapes component data from electronic component suppliers.
    Use this when APIs are unavailable or have rate limits.
    """
    
    def __init__(self, headless: bool = True, delay_between_requests: float = 2.0):
        """
        Initialize component scraper.
        
        Args:
            headless: Run browser in headless mode
            delay_between_requests: Seconds to wait between requests (be respectful!)
        """
        self.headless = headless
        self.delay = delay_between_requests
    
    def search_digikey(self, keywords: str, max_results: int = 5) -> List[ComponentInfo]:
        """
        Search DigiKey for components.
        
        Args:
            keywords: Search keywords
            max_results: Maximum results to return
        
        Returns:
            List of ComponentInfo objects
        """
        def _scrape(browser: BrowserAutomation) -> List[ComponentInfo]:
            page = browser.new_page()
            results = []
            
            try:
                # Navigate to DigiKey search
                search_url = f"https://www.digikey.com/en/products/filter?keywords={keywords.replace(' ', '%20')}"
                browser.navigate(page, search_url)
                
                # Wait for results to load
                time.sleep(2)
                
                # Try to extract product data from the page
                products = page.evaluate("""
                    () => {
                        const items = document.querySelectorAll('[data-testid="product-row"], .product-row, tr[data-product]');
                        return Array.from(items).slice(0, """ + str(max_results) + """).map(item => {
                            return {
                                partNumber: item.querySelector('[data-testid="part-number"], .part-number a')?.textContent?.trim() || '',
                                manufacturer: item.querySelector('[data-testid="manufacturer"], .manufacturer')?.textContent?.trim() || '',
                                description: item.querySelector('[data-testid="description"], .description')?.textContent?.trim() || '',
                                price: item.querySelector('[data-testid="unit-price"], .unit-price')?.textContent?.trim() || '0',
                                stock: item.querySelector('[data-testid="quantity-available"], .quantity-available')?.textContent?.trim() || '0',
                                datasheet: item.querySelector('[data-testid="datasheet-link"] a, .datasheet a')?.href || ''
                            };
                        });
                    }
                """)
                
                for product in products:
                    try:
                        price = float(re.sub(r'[^\d.]', '', product.get('price', '0')) or '0')
                        stock = int(re.sub(r'[^\d]', '', product.get('stock', '0')) or '0')
                        
                        results.append(ComponentInfo(
                            part_number=product.get('partNumber', ''),
                            manufacturer=product.get('manufacturer', ''),
                            description=product.get('description', '')[:200],
                            unit_price=price,
                            stock=stock,
                            datasheet_url=product.get('datasheet', ''),
                            supplier='DigiKey',
                            supplier_part_number=product.get('partNumber', ''),
                            category=keywords
                        ))
                    except Exception as e:
                        logger.warning(f"Error parsing DigiKey product: {e}")
                
            except Exception as e:
                logger.error(f"DigiKey scrape error: {e}")
            finally:
                page.close()
            
            return results
        
        return run_browser_task(_scrape, headless=self.headless)
    
    def search_mouser(self, keywords: str, max_results: int = 5) -> List[ComponentInfo]:
        """
        Search Mouser for components.
        
        Args:
            keywords: Search keywords
            max_results: Maximum results to return
        
        Returns:
            List of ComponentInfo objects
        """
        def _scrape(browser: BrowserAutomation) -> List[ComponentInfo]:
            page = browser.new_page()
            results = []
            
            try:
                search_url = f"https://www.mouser.com/Search/Refine?Keyword={keywords.replace(' ', '%20')}"
                browser.navigate(page, search_url)
                
                time.sleep(2)
                
                # Extract product data
                products = page.evaluate("""
                    () => {
                        const items = document.querySelectorAll('.search-result-row, [class*="SearchResult"]');
                        return Array.from(items).slice(0, """ + str(max_results) + """).map(item => {
                            return {
                                partNumber: item.querySelector('[class*="part-number"], .mfr-part-num a')?.textContent?.trim() || '',
                                manufacturer: item.querySelector('[class*="manufacturer"], .mfr')?.textContent?.trim() || '',
                                description: item.querySelector('[class*="description"]')?.textContent?.trim() || '',
                                price: item.querySelector('[class*="price"], .price')?.textContent?.trim() || '0',
                                stock: item.querySelector('[class*="availability"], .availability')?.textContent?.trim() || '0',
                                datasheet: item.querySelector('[class*="datasheet"] a')?.href || ''
                            };
                        });
                    }
                """)
                
                for product in products:
                    try:
                        price = float(re.sub(r'[^\d.]', '', product.get('price', '0')) or '0')
                        stock_text = re.sub(r'[^\d]', '', product.get('stock', '0'))
                        stock = int(stock_text) if stock_text else 0
                        
                        results.append(ComponentInfo(
                            part_number=product.get('partNumber', ''),
                            manufacturer=product.get('manufacturer', ''),
                            description=product.get('description', '')[:200],
                            unit_price=price,
                            stock=stock,
                            datasheet_url=product.get('datasheet', ''),
                            supplier='Mouser',
                            supplier_part_number=product.get('partNumber', ''),
                            category=keywords
                        ))
                    except Exception as e:
                        logger.warning(f"Error parsing Mouser product: {e}")
                
            except Exception as e:
                logger.error(f"Mouser scrape error: {e}")
            finally:
                page.close()
            
            return results
        
        return run_browser_task(_scrape, headless=self.headless)
    
    def search_lcsc(self, keywords: str, max_results: int = 5) -> List[ComponentInfo]:
        """
        Search LCSC (good for Chinese components, cheaper options).
        
        Args:
            keywords: Search keywords
            max_results: Maximum results to return
        
        Returns:
            List of ComponentInfo objects
        """
        def _scrape(browser: BrowserAutomation) -> List[ComponentInfo]:
            page = browser.new_page()
            results = []
            
            try:
                search_url = f"https://www.lcsc.com/search?q={keywords.replace(' ', '%20')}"
                browser.navigate(page, search_url)
                
                time.sleep(3)  # LCSC can be slower
                
                products = page.evaluate("""
                    () => {
                        const items = document.querySelectorAll('.product-list-item, [class*="product-item"]');
                        return Array.from(items).slice(0, """ + str(max_results) + """).map(item => {
                            return {
                                partNumber: item.querySelector('[class*="part-number"], .mfs-code a')?.textContent?.trim() || '',
                                manufacturer: item.querySelector('[class*="manufacturer"], .brand')?.textContent?.trim() || '',
                                description: item.querySelector('[class*="description"], .cart-product')?.textContent?.trim() || '',
                                price: item.querySelector('[class*="price"]')?.textContent?.trim() || '0',
                                stock: item.querySelector('[class*="stock"]')?.textContent?.trim() || '0',
                                datasheet: item.querySelector('[class*="datasheet"] a')?.href || ''
                            };
                        });
                    }
                """)
                
                for product in products:
                    try:
                        price = float(re.sub(r'[^\d.]', '', product.get('price', '0')) or '0')
                        stock = int(re.sub(r'[^\d]', '', product.get('stock', '0')) or '0')
                        
                        results.append(ComponentInfo(
                            part_number=product.get('partNumber', ''),
                            manufacturer=product.get('manufacturer', ''),
                            description=product.get('description', '')[:200],
                            unit_price=price,
                            stock=stock,
                            datasheet_url=product.get('datasheet', ''),
                            supplier='LCSC',
                            supplier_part_number=product.get('partNumber', ''),
                            category=keywords
                        ))
                    except Exception as e:
                        logger.warning(f"Error parsing LCSC product: {e}")
                
            except Exception as e:
                logger.error(f"LCSC scrape error: {e}")
            finally:
                page.close()
            
            return results
        
        return run_browser_task(_scrape, headless=self.headless)
    
    def search_all(self, keywords: str, max_results_per_supplier: int = 3) -> Dict[str, List[Dict]]:
        """
        Search all supported suppliers.
        
        Args:
            keywords: Search keywords
            max_results_per_supplier: Max results per supplier
        
        Returns:
            Dictionary with supplier names as keys and component lists as values
        """
        results = {}
        
        # Search each supplier with delay between requests
        suppliers = [
            ('DigiKey', self.search_digikey),
            ('Mouser', self.search_mouser),
            ('LCSC', self.search_lcsc)
        ]
        
        for supplier_name, search_func in suppliers:
            try:
                logger.info(f"Searching {supplier_name}...")
                components = search_func(keywords, max_results_per_supplier)
                results[supplier_name] = [c.to_dict() for c in components]
                time.sleep(self.delay)
            except Exception as e:
                logger.error(f"Error searching {supplier_name}: {e}")
                results[supplier_name] = []
        
        return results
    
    def export_to_csv(self, components: List[ComponentInfo], output_path: str) -> str:
        """Export components to CSV file."""
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'supplier', 'part_number', 'manufacturer', 'description',
                'unit_price', 'stock', 'datasheet_url', 'category'
            ])
            writer.writeheader()
            for comp in components:
                writer.writerow({
                    'supplier': comp.supplier,
                    'part_number': comp.part_number,
                    'manufacturer': comp.manufacturer,
                    'description': comp.description,
                    'unit_price': comp.unit_price,
                    'stock': comp.stock,
                    'datasheet_url': comp.datasheet_url,
                    'category': comp.category
                })
        
        logger.info(f"Exported {len(components)} components to {output_path}")
        return output_path


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python component_scraper.py <search_keywords>")
        print("Example: python component_scraper.py 'Artix-7 FPGA'")
        sys.exit(1)
    
    keywords = ' '.join(sys.argv[1:])
    print(f"Searching for: {keywords}")
    
    scraper = ComponentScraper(headless=True)
    results = scraper.search_all(keywords)
    
    print(json.dumps(results, indent=2))
