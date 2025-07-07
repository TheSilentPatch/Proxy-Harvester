#!/usr/bin/env python3
# proxy_harvester.py
"""
Proxy Harvester - Scrape free proxies from public sources with robust CLI functionality.
"""

import argparse
import logging
import sys
import re
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from importlib.metadata import version
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

ver = version("proxy-harvester")
BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
 ____                           _   _                           _            
|  _ \ _ __ _____  ___   _     | | | | __ _ _ ____   _____  ___| |_ ___ _ __ 
| |_) | '__/ _ \ \/ / | | |    | |_| |/ _` | '__\ \ / / _ \/ __| __/ _ \ '__|
|  __/| | | (_) >  <| |_| |    |  _  | (_| | |   \ V /  __/\__ \ ||  __/ |   
|_|   |_|  \___/_/\_\\__, |    |_| |_|\__,_|_|    \_/ \___||___/\__\___|_|   
                     |___/                                                   

Proxy Harvester v{ver}
by github.com/TheSilentPatch
{Style.RESET_ALL}"""

SOURCE_URL = "https://free-proxy-list.net/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
}
IP_PORT_PATTERN = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$")

def setup_logger(verbose: bool = False) -> logging.Logger:
    """Configure and return logger instance"""
    logger = logging.getLogger("proxy_harvester")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

def validate_output_path(path: str, logger: logging.Logger) -> Path:
    """
    Validate and normalize output path with enhanced features:
    - Handles directory paths (appends default filename)
    - Creates parent directories if needed
    - Checks write permissions
    - Resolves absolute paths
    """
    try:
        path_obj = Path(path).expanduser().resolve()
        
        # If path is a directory, append default filename
        if path_obj.is_dir() or path.endswith(os.sep):
            logger.info(f"Output is directory, using default filename")
            path_obj = path_obj / "proxies.txt"
        
        # Create parent directories if needed
        if not path_obj.parent.exists():
            logger.info(f"Creating parent directories: {path_obj.parent}")
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            
        # Check write access
        if path_obj.exists():
            logger.info(f"Output file exists, will overwrite: {path_obj}")
        else:
            logger.info(f"Output file will be created: {path_obj}")
            
        # Test write access
        path_obj.touch(exist_ok=True)
        return path_obj
        
    except (PermissionError, OSError) as e:
        logger.error(f"Filesystem error: {e}")
        print(f"{Fore.RED}✗ Output path error: {e}{Style.RESET_ALL}")
        sys.exit(3)

def fetch_html_content(url: str, logger: logging.Logger) -> str:
    """Fetch HTML content from target URL with error handling"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        logger.info(f"Successfully fetched content from {url}")
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Network request failed: {e}")
        print(f"{Fore.RED}✗ Network error: {e}{Style.RESET_ALL}")
        sys.exit(1)

def parse_proxy_table(html: str, logger: logging.Logger) -> List[Dict[str, str]]:
    """Parse HTML and extract proxy data from table"""
    try:
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table", class_="table table-striped table-bordered")
        
        if not table:
            raise ValueError("Proxy table not found in HTML")
        
        headers = [th.text.strip().lower() for th in table.find("thead").find_all("th")]
        proxies = []
        
        for row in table.find("tbody").find_all("tr"):
            cols = [td.text.strip() for td in row.find_all("td")]
            if len(cols) != len(headers):
                continue
            proxy_data = dict(zip(headers, cols))
            proxies.append(proxy_data)
        
        logger.info(f"Found {len(proxies)} raw proxies in table")
        return proxies
        
    except Exception as e:
        logger.exception(f"Parsing failed: {e}")
        print(f"{Fore.RED}✗ Parsing error: {e}{Style.RESET_ALL}")
        sys.exit(2)

def validate_proxy(proxy: Dict[str, str]) -> Optional[str]:
    """Validate proxy entry and return formatted ip:port if valid"""
    try:
        ip = proxy["ip address"]
        port = proxy["port"]
        
        if not ip or not port:
            return None
        
        # Validate port range
        if not port.isdigit() or not (1 <= int(port) <= 65535):
            return None
        
        # Basic IP validation
        if not all(part.isdigit() and 0 <= int(part) <= 255 for part in ip.split(".")):
            return None
            
        return f"{ip}:{port}"
    except KeyError:
        return None

def filter_proxies(
    proxies: List[Dict[str, str]], 
    proxy_type: str,
    logger: logging.Logger
) -> List[str]:
    """Filter proxies based on type and validation criteria"""
    valid_proxies = []
    for proxy in proxies:
        try:
            # Skip if missing required fields
            if "https" not in proxy:
                continue
                
            # Type filtering
            if proxy_type == "https" and proxy["https"] != "yes":
                continue
            if proxy_type == "http" and proxy["https"] != "no":
                continue
            
            formatted = validate_proxy(proxy)
            if formatted:
                valid_proxies.append(formatted)
        except KeyError as e:
            logger.warning(f"Missing key in proxy data: {e}")
    
    return valid_proxies

def save_proxies(proxies: List[str], path: Path, logger: logging.Logger) -> None:
    """Save proxies to output file with validation"""
    try:
        # Validate we have proxies to save
        if not proxies:
            logger.warning("No valid proxies to save")
            print(f"{Fore.YELLOW}⚠ No valid proxies found to save{Style.RESET_ALL}")
            
        # Write to file
        with path.open("w", encoding="utf-8") as f:
            f.write("\n".join(proxies))
        logger.info(f"Saved {len(proxies)} proxies to {path}")
        print(f"{Fore.GREEN}✓ Saved {len(proxies)} proxies to {path}{Style.RESET_ALL}")
        
    except (IOError, PermissionError) as e:
        logger.error(f"File write error: {e}")
        print(f"{Fore.RED}✗ Failed to write output: {e}{Style.RESET_ALL}")
        sys.exit(4)

def print_summary(
    total_scraped: int,
    valid_count: int,
    proxy_type: str,
    output_path: Path,
    logger: logging.Logger
) -> None:
    """Print colored summary to console"""
    logger.info(f"Scraping completed. Total: {total_scraped}, Valid: {valid_count}")
    
    print(f"\n{Fore.GREEN}✓ Harvest complete!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}• Scraped proxies:{Fore.CYAN} {total_scraped}")
    print(f"{Fore.YELLOW}• Valid proxies:{Fore.CYAN} {valid_count}")
    print(f"{Fore.YELLOW}• Proxy type:{Fore.CYAN} {proxy_type.upper()}")
    print(f"{Fore.YELLOW}• Output file:{Fore.CYAN} {output_path}{Style.RESET_ALL}")

def main() -> None:
    """Main CLI entry point"""
    print(BANNER)
    
    parser = argparse.ArgumentParser(
        description="Harvest free proxies from public sources",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-t", "--type",
        choices=["http", "https", "all"],
        default="https",
        help="Proxy protocol type to harvest"
    )
    parser.add_argument(
        "-o", "--output",
        default="proxies.txt",
        help="Output file or directory path (default: proxies.txt)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {ver}"
    )
    args = parser.parse_args()
    
    logger = setup_logger(args.verbose)
    logger.info(f"Starting harvest (type={args.type}, output={args.output})")
    
    # Validate and normalize output path
    output_path = validate_output_path(args.output, logger)
    
    # Scrape and process proxies
    html = fetch_html_content(SOURCE_URL, logger)
    raw_proxies = parse_proxy_table(html, logger)
    valid_proxies = filter_proxies(raw_proxies, args.type, logger)
    
    # Save and report results
    save_proxies(valid_proxies, output_path, logger)
    print_summary(
        total_scraped=len(raw_proxies),
        valid_count=len(valid_proxies),
        proxy_type=args.type,
        output_path=output_path,
        logger=logger
    )

if __name__ == "__main__":
    main()