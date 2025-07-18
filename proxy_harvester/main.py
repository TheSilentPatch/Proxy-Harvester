#!/usr/bin/env python3
# proxy_harvester.py
"""
Proxy Harvester - Scrape free proxies from multiple public sources with robust CLI functionality.
"""

import argparse
import logging
import sys
import os
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

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
}

# Specific parsers for different sites
def parse_free_proxy_list(html: str, logger: logging.Logger) -> List[Dict[str, str]]:
    """Parser for free-proxy-list.net format"""
    return parse_generic_proxy_table(html, logger)

def parse_sslproxies(html: str, logger: logging.Logger) -> List[Dict[str, str]]:
    """Parser for sslproxies.org format"""
    return parse_generic_proxy_table(html, logger)

def parse_us_proxy(html: str, logger: logging.Logger) -> List[Dict[str, str]]:
    """Parser for us-proxy.org format"""
    return parse_generic_proxy_table(html, logger)

def parse_proxy_list_download(html: str, logger: logging.Logger) -> List[Dict[str, str]]:
    """Parser for proxy-list.download format"""
    proxies = []
    try:
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table", {"id": "tblproxy"})
        if not table:
            return []
            
        headers = [th.text.strip().lower() for th in table.find("thead").find_all("th")]
        for row in table.find("tbody").find_all("tr"):
            cols = [td.text.strip() for td in row.find_all("td")]
            if len(cols) == len(headers):
                proxy_data = dict(zip(headers, cols))
                proxies.append(proxy_data)
    except Exception as e:
        logger.warning(f"Failed to parse proxy-list.download format: {e}")
    return proxies

def parse_raw_proxy_list(html: str, logger: logging.Logger) -> List[Dict[str, str]]:
    """Parser for raw text proxy lists"""
    proxies = []
    for line in html.splitlines():
        line = line.strip()
        if line and ":" in line:
            ip, port = line.split(":", 1)
            proxies.append({"ip": ip, "port": port})
    return proxies

def parse_generic_proxy_table(html: str, logger: logging.Logger) -> List[Dict[str, str]]:
    """Generic parser for HTML tables"""
    proxies = []
    try:
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table")
        if not table:
            return []
            
        headers = []
        thead = table.find("thead")
        if thead:
            headers = [th.text.strip().lower() for th in thead.find_all("th")]
        
        # If no headers in thead, try to find them in the first row
        if not headers:
            first_row = table.find("tr")
            if first_row:
                headers = [td.text.strip().lower() for td in first_row.find_all("td")]
                rows = table.find_all("tr")[1:]  # Skip header row
            else:
                rows = table.find_all("tr")
        else:
            rows = table.find_all("tr")[1:] if thead else table.find_all("tr")
        
        for row in rows:
            cols = [td.text.strip() for td in row.find_all("td")]
            if len(cols) == len(headers):
                proxy_data = dict(zip(headers, cols))
                proxies.append(proxy_data)
            elif cols:  # Handle rows with different column counts
                # Try to extract IP and port from first two columns
                if len(cols) >= 2:
                    proxies.append({"ip": cols[0], "port": cols[1]})
                
        logger.info(f"Parsed {len(proxies)} proxies from HTML")
    except Exception as e:
        logger.warning(f"Generic parsing failed: {e}")
    return proxies

# Parser registry for different proxy source formats
PARSERS = {
    "free-proxy-list.net": parse_free_proxy_list,
    "sslproxies.org": parse_sslproxies,
    "us-proxy.org": parse_us_proxy,
    "proxy-list.download": parse_proxy_list_download,
    "raw.githubusercontent.com": parse_raw_proxy_list
}

def get_parser_for_url(url: str):
    """Get the appropriate parser for a given URL"""
    for domain, parser in PARSERS.items():
        if domain in url:
            return parser
    return parse_generic_proxy_table  # Fallback parser

# List of proxy source URLs to scrape
SOURCES = [
    "https://free-proxy-list.net/",
    "https://www.sslproxies.org/",
    "https://www.us-proxy.org/",
    "https://www.proxy-list.download/http",
    "https://www.proxy-list.download/https",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
]

def setup_logger(verbose: bool = False) -> logging.Logger:
    logger = logging.getLogger("proxy_harvester")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def validate_output_path(path: str, logger: logging.Logger) -> Path:
    try:
        path_obj = Path(path).expanduser().resolve()
        # If directory, append default filename
        if path_obj.is_dir() or path.endswith(os.sep):
            logger.info("Output is a directory; using default filename proxies.txt")
            path_obj = path_obj / "proxies.txt"
        # Create parent directories if missing
        if not path_obj.parent.exists():
            logger.info(f"Creating directories: {path_obj.parent}")
            path_obj.parent.mkdir(parents=True, exist_ok=True)
        # Ensure file exists for later reading/updating
        path_obj.touch(exist_ok=True)
        return path_obj
    except (PermissionError, OSError) as e:
        logger.error(f"Filesystem error: {e}")
        print(f"{Fore.RED}[ERROR] Output path error: {e}{Style.RESET_ALL}")
        sys.exit(3)

def fetch_html_content(url: str, logger: logging.Logger) -> Optional[str]:
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        logger.info(f"Fetched content from {url}")
        return response.text
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return None

def validate_proxy(proxy: Dict[str, str]) -> Optional[str]:
    try:
        ip = proxy.get("ip address") or proxy.get("ip")
        port = proxy.get("port")
        if not ip or not port or not port.isdigit():
            return None
        # Basic IP validation
        if not all(0 <= int(part) <= 255 for part in ip.split(".")):
            return None
        return f"{ip}:{port}"
    except Exception:
        return None

def filter_proxies(proxies: List[Dict[str, str]], proxy_type: str, logger: logging.Logger) -> List[str]:
    valid = []
    for p in proxies:
        https_flag = p.get("https")
        if proxy_type == "https" and https_flag != "yes":
            continue
        if proxy_type == "http" and https_flag != "no":
            continue
        formatted = validate_proxy(p)
        if formatted:
            valid.append(formatted)
    return valid

def save_proxies(proxies: List[str], path: Path, logger: logging.Logger) -> None:
    try:
        existing = set()
        # Read existing entries
        with path.open("r", encoding="utf-8") as f:
            existing = set(line.strip() for line in f if line.strip())
        new_set = set(proxies)
        combined = sorted(existing | new_set)
        with path.open("w", encoding="utf-8") as f:
            f.write("\n".join(combined))
        added = len(new_set - existing)
        logger.info(f"Updated {path}: +{added} new, total {len(combined)}")
        print(f"{Fore.GREEN}[OK] Saved {added} new proxies to {path}{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"File write error: {e}")
        print(f"{Fore.RED}[ERROR] Failed to write output: {e}{Style.RESET_ALL}")
        sys.exit(4)

def print_summary(total: int, valid_count: int, proxy_type: str, output_path: Path, logger: logging.Logger) -> None:
    logger.info(f"Scraping complete — total scraped: {total}, valid: {valid_count}")
    print(f"\n{Fore.GREEN}[OK] Harvest complete!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}• Scraped proxies:{Fore.CYAN} {total}")
    print(f"{Fore.YELLOW}• Valid proxies:{Fore.CYAN} {valid_count}")
    print(f"{Fore.YELLOW}• Type:{Fore.CYAN} {proxy_type.upper()}")
    print(f"{Fore.YELLOW}• Output:{Fore.CYAN} {output_path}{Style.RESET_ALL}")

def main() -> None:
    print(BANNER)
    parser = argparse.ArgumentParser(
        description="Harvest free proxies from multiple public sources",
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
        help="Output file or directory path"
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

    output_path = validate_output_path(args.output, logger)

    all_raw = []
    total_scraped = 0

    for url in SOURCES:
        html = fetch_html_content(url, logger)
        if html:
            parser = get_parser_for_url(url)
            raw = parser(html, logger)
            all_raw.extend(raw)
            total_scraped += len(raw)

    if args.type == "all":
        valid_list = [v for p in all_raw if (v := validate_proxy(p))]
    else:
        valid_list = filter_proxies(all_raw, args.type, logger)

    save_proxies(valid_list, output_path, logger)
    print_summary(total_scraped, len(valid_list), args.type, output_path, logger)

if __name__ == "__main__":
    main()
