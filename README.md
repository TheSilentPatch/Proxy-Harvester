# Proxy Harvester

A simple Python CLI script to scrape free proxies from [free-proxy-list.net](https://free-proxy-list.net/) and save them into a text file in `ip:port` format.

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

```
# Basic usage (HTTPS proxies)
python proxy_harvester.py

# HTTP proxies with custom output
python proxy_harvester.py --type http -o http_proxies.txt

# All proxies with verbose output
python proxy_harvester.py -t all -v
```

### Options

* `--type` or `-t` (default `https`)

  * Filter proxies by protocol: `http`, `https`, or `all`
* `--output` or `-o`

  * Set output file name (default `proxies.txt`)
* `--verbose` or `-v`

  * Enable verbose debug output
* `--version`

  * Show version information

---

## Output

The harvested proxies will be saved to a `.txt` file, with one proxy per line in this format:

```
123.45.67.89:8080
12.34.56.78:3128
```

---

## Notes

* This script uses `requests` and `beautifulsoup4` with the `lxml` parser.
* By default, it pulls proxies from `free-proxy-list.net`.
* Designed for educational or ethical usage only — respect the site’s terms of service.
* You should validate each proxy manually before using it in production.

---

## Author

[**Silent Coder**](https://github.com/TheSilentPatch/)

---

Happy harvesting!
