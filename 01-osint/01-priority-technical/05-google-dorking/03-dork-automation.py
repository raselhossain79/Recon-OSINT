#!/usr/bin/env python3
"""
Google Dorking Automation Tool
==============================

Purpose:
- Generate custom dorks from templates
- Execute dorks with rate limiting & proxy support
- Collect & parse results
- Output in multiple formats (txt, csv, json)

Usage:
    python3 dork-automation.py -t example.com -o results.txt
    python3 dork-automation.py -t example.com --delay 5 --proxy-list proxies.txt
    python3 dork-automation.py -t example.com -c custom-dorks.txt --json

Requirements:
    pip install selenium requests beautifulsoup4 python-dotenv

Author: Security Researcher
License: MIT
"""

import argparse
import csv
import json
import logging
import os
import random
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote, urlencode

try:
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
except ImportError as e:
    print(f"Error: Required module missing. Install with: pip install selenium requests beautifulsoup4")
    sys.exit(1)

# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

# Built-in dork templates (placeholder: {target})
DORK_TEMPLATES = {
    "subdomain_discovery": [
        "site:*.{target}",
        "site:*.{target} inurl:admin",
        "site:*.{target} inurl:api",
        "site:*.{target} inurl:staging",
        "site:*.{target} inurl:dev",
        "site:*.{target} inurl:test",
    ],
    "config_files": [
        "site:{target} filetype:env",
        "site:{target} filetype:conf",
        "site:{target} filetype:config",
        "site:{target} filetype:ini",
        "site:{target} filetype:json intext:api_key",
    ],
    "backup_files": [
        "site:{target} filetype:sql",
        "site:{target} filetype:bak",
        "site:{target} filetype:old",
        "site:{target} filetype:zip",
        "inurl:backup filetype:sql",
    ],
    "credentials": [
        "site:{target} intext:password filetype:txt",
        "site:{target} intext:username intext:password",
        "intext:\"API_KEY\" site:{target}",
        "intext:\"api_secret\" site:{target}",
    ],
    "admin_panels": [
        "site:{target} inurl:admin",
        "site:{target} inurl:/login",
        "site:{target} intitle:admin",
        "site:{target} intitle:dashboard",
    ],
    "exposed_files": [
        'intitle:"Index of" site:{target}',
        "site:{target} inurl:.git",
        "site:{target} inurl:.env",
        "site:{target} filetype:log",
    ],
    "cloud_storage": [
        "site:s3.amazonaws.com {target}",
        "site:blob.core.windows.net {target}",
        "site:storage.googleapis.com {target}",
    ],
}

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# ============================================================================
# DORK GENERATION
# ============================================================================

class DorkGenerator:
    """Generate dorks from templates or custom file."""

    def __init__(self, target: str):
        self.target = target

    def generate_from_templates(self, categories: Optional[List[str]] = None) -> List[str]:
        """Generate dorks from built-in templates."""
        dorks = []
        
        if not categories:
            categories = list(DORK_TEMPLATES.keys())
        
        for category in categories:
            if category in DORK_TEMPLATES:
                for template in DORK_TEMPLATES[category]:
                    dork = template.format(target=self.target)
                    dorks.append(dork)
                    logger.debug(f"Generated dork: {dork}")
        
        logger.info(f"Generated {len(dorks)} dorks from templates")
        return dorks

    def load_from_file(self, filepath: str) -> List[str]:
        """Load custom dorks from file (one per line)."""
        if not os.path.exists(filepath):
            logger.error(f"Dork file not found: {filepath}")
            return []
        
        with open(filepath, 'r') as f:
            dorks = [
                line.strip().format(target=self.target)
                for line in f if line.strip() and not line.startswith('#')
            ]
        
        logger.info(f"Loaded {len(dorks)} custom dorks from {filepath}")
        return dorks

# ============================================================================
# SEARCH EXECUTION
# ============================================================================

class DorkRunner:
    """Execute dorks and collect results."""

    def __init__(self, delay: float = 3.0, proxy_list: Optional[List[str]] = None,
                 headless: bool = True, timeout: int = 10):
        self.delay = delay
        self.proxy_list = proxy_list or []
        self.headless = headless
        self.timeout = timeout
        self.results: Dict[str, List[str]] = {}

    def _get_proxy(self) -> Optional[str]:
        """Return random proxy or None."""
        if self.proxy_list:
            return random.choice(self.proxy_list)
        return None

    def _get_user_agent(self) -> str:
        """Return random User-Agent."""
        return random.choice(DEFAULT_USER_AGENTS)

    def run_dork_headless(self, dork: str) -> List[str]:
        """
        Execute dork using Selenium with headless Chrome.
        Better for handling JavaScript, but slower.
        """
        urls = []
        
        try:
            chrome_options = ChromeOptions()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"user-agent={self._get_user_agent()}")
            
            # Proxy support (if available)
            proxy = self._get_proxy()
            if proxy:
                chrome_options.add_argument(f"--proxy-server={proxy}")
            
            driver = webdriver.Chrome(options=chrome_options)
            search_url = f"https://www.google.com/search?q={quote(dork)}"
            
            logger.debug(f"Navigating to: {search_url}")
            driver.get(search_url)
            
            # Wait for results to load
            wait = WebDriverWait(driver, self.timeout)
            wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@href]")))
            
            # Extract results
            for link in driver.find_elements(By.XPATH, "//a[@href]"):
                href = link.get_attribute('href')
                if href and not href.startswith('http'):
                    continue
                if '/search?' in href or 'google.com' in href:
                    continue
                urls.append(href)
            
            driver.quit()
            logger.info(f"✓ Dork: {dork[:60]}... | Found {len(urls)} URLs")
        
        except Exception as e:
            logger.warning(f"✗ Dork: {dork[:60]}... | Error: {str(e)}")
        
        return urls

    def run_dork_requests(self, dork: str) -> List[str]:
        """
        Execute dork using requests library (faster, but limited JS support).
        """
        urls = []
        
        try:
            headers = {
                "User-Agent": self._get_user_agent(),
            }
            
            search_url = f"https://www.google.com/search?q={quote(dork)}"
            
            # Proxy support
            proxies = {}
            proxy = self._get_proxy()
            if proxy:
                proxies = {
                    "http": proxy,
                    "https": proxy,
                }
            
            logger.debug(f"GET {search_url}")
            response = requests.get(search_url, headers=headers, proxies=proxies,
                                   timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Parse Google result links
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    # Filter Google's internal links
                    if href.startswith('/url?q='):
                        real_url = href.split('?q=')[1].split('&')[0]
                        urls.append(real_url)
                
                logger.info(f"✓ Dork: {dork[:60]}... | Found {len(urls)} URLs")
            
            elif response.status_code == 429:
                logger.warning("Rate limited by Google (429). Increase delay or use proxy.")
            else:
                logger.warning(f"HTTP {response.status_code}: {dork[:60]}...")
        
        except Exception as e:
            logger.warning(f"✗ Dork: {dork[:60]}... | Error: {str(e)}")
        
        return urls

    def run(self, dorks: List[str], use_headless: bool = False) -> Dict[str, List[str]]:
        """Execute all dorks and collect results."""
        self.results = {}
        runner = self.run_dork_headless if use_headless else self.run_dork_requests
        
        for i, dork in enumerate(dorks, 1):
            logger.info(f"[{i}/{len(dorks)}] Running dork...")
            urls = runner(dork)
            self.results[dork] = urls
            
            # Rate limiting
            if i < len(dorks):
                sleep_time = self.delay + random.uniform(0, 2)
                logger.debug(f"Sleeping {sleep_time:.2f}s...")
                time.sleep(sleep_time)
        
        logger.info(f"Completed {len(dorks)} dorks. Total URLs found: {sum(len(u) for u in self.results.values())}")
        return self.results

# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

class ResultExporter:
    """Export results in multiple formats."""

    @staticmethod
    def to_txt(results: Dict[str, List[str]], filepath: str) -> None:
        """Export as plain text."""
        with open(filepath, 'w') as f:
            f.write(f"# Google Dorking Results\n")
            f.write(f"# Generated: {datetime.now().isoformat()}\n")
            f.write(f"# Total URLs: {sum(len(urls) for urls in results.values())}\n\n")
            
            for dork, urls in results.items():
                f.write(f"## Dork: {dork}\n")
                f.write(f"## Results: {len(urls)}\n")
                for url in urls:
                    f.write(f"{url}\n")
                f.write("\n")
        
        logger.info(f"Exported results to {filepath}")

    @staticmethod
    def to_csv(results: Dict[str, List[str]], filepath: str) -> None:
        """Export as CSV."""
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Dork', 'URL', 'Found Date'])
            
            for dork, urls in results.items():
                for url in urls:
                    writer.writerow([dork, url, datetime.now().isoformat()])
        
        logger.info(f"Exported results to {filepath}")

    @staticmethod
    def to_json(results: Dict[str, List[str]], filepath: str) -> None:
        """Export as JSON."""
        output = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "total_dorks": len(results),
                "total_urls": sum(len(urls) for urls in results.values()),
            },
            "results": results,
        }
        
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        
        logger.info(f"Exported results to {filepath}")

    @staticmethod
    def to_summary(results: Dict[str, List[str]]) -> str:
        """Generate summary statistics."""
        total_dorks = len(results)
        total_urls = sum(len(urls) for urls in results.values())
        avg_urls = total_urls / total_dorks if total_dorks > 0 else 0
        
        summary = f"""
========================================
Google Dorking Summary
========================================
Total Dorks Run:    {total_dorks}
Total URLs Found:   {total_urls}
Average per Dork:   {avg_urls:.2f}
Execution Time:     {datetime.now().isoformat()}

Top Results:
"""
        
        sorted_results = sorted(
            results.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:5]
        
        for dork, urls in sorted_results:
            summary += f"  {len(urls):3d} URLs: {dork}\n"
        
        summary += "\n========================================\n"
        return summary

# ============================================================================
# PROXY MANAGEMENT
# ============================================================================

def load_proxy_list(filepath: str) -> List[str]:
    """Load proxies from file (one per line)."""
    if not os.path.exists(filepath):
        logger.error(f"Proxy file not found: {filepath}")
        return []
    
    with open(filepath, 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]
    
    logger.info(f"Loaded {len(proxies)} proxies")
    return proxies

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Google Dorking Automation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate and run dorks for example.com
  python3 dork-automation.py -t example.com

  # Use custom dorks file with 10s delay
  python3 dork-automation.py -t example.com -c custom-dorks.txt --delay 10

  # Export as JSON with proxy rotation
  python3 dork-automation.py -t example.com -p proxies.txt -o results.json

  # Use specific dorking categories
  python3 dork-automation.py -t example.com --categories subdomain_discovery,config_files
        """
    )
    
    # Core arguments
    parser.add_argument('-t', '--target', required=True, help='Target domain (e.g., example.com)')
    parser.add_argument('-c', '--custom-dorks', help='File with custom dorks (one per line)')
    parser.add_argument('-o', '--output', default='dork-results.txt', help='Output file (default: dork-results.txt)')
    
    # Execution options
    parser.add_argument('--delay', type=float, default=3.0, help='Delay between requests in seconds (default: 3.0)')
    parser.add_argument('-p', '--proxy-list', help='File with proxy list (one per line, format: http://ip:port)')
    parser.add_argument('--headless', action='store_true', help='Use headless Selenium (slower, better JS support)')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout in seconds (default: 10)')
    
    # Template options
    parser.add_argument(
        '--categories',
        help='Comma-separated list of dork categories (default: all). Options: ' + ', '.join(DORK_TEMPLATES.keys())
    )
    
    # Output format
    parser.add_argument(
        '--format',
        choices=['txt', 'csv', 'json'],
        default='txt',
        help='Output format (default: txt)'
    )
    
    # Logging
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    # Setup
    setup_logging(args.verbose)
    logger.info(f"Starting Google Dorking for {args.target}")
    
    # Generate/load dorks
    generator = DorkGenerator(args.target)
    
    if args.custom_dorks:
        dorks = generator.load_from_file(args.custom_dorks)
    else:
        categories = args.categories.split(',') if args.categories else None
        dorks = generator.generate_from_templates(categories)
    
    if not dorks:
        logger.error("No dorks to run. Exiting.")
        return 1
    
    # Load proxies if specified
    proxies = []
    if args.proxy_list:
        proxies = load_proxy_list(args.proxy_list)
    
    # Run dorks
    runner = DorkRunner(
        delay=args.delay,
        proxy_list=proxies,
        headless=args.headless,
        timeout=args.timeout
    )
    
    results = runner.run(dorks, use_headless=args.headless)
    
    # Export results
    output_base = os.path.splitext(args.output)[0]
    
    if args.format == 'txt':
        ResultExporter.to_txt(results, f"{output_base}.txt")
    elif args.format == 'csv':
        ResultExporter.to_csv(results, f"{output_base}.csv")
    elif args.format == 'json':
        ResultExporter.to_json(results, f"{output_base}.json")
    
    # Print summary
    print(ResultExporter.to_summary(results))
    logger.info("Done!")
    return 0

if __name__ == '__main__':
    sys.exit(main())
