# Proxy Harvester

A robust Python CLI tool to scrape free proxies from [free-proxy-list.net](https://free-proxy-list.net/) and save them in `ip:port` format. Supports flexible output paths, colored logging, and protocol filtering.

## Installation

You can install the proxy harvester using pip from the github repo:

```bash
pip install git+https://github.com/TheSilentPatch/Proxy-Harvester.git
```
Then use:
```bash
# for help
proxy-harvester --help
```

If you want to install a specific release:
```bash
pip install git+https://github.com/TheSilentPatch/Proxy-Harvester.git@<release_tag>
# browse releases in https://github.com/TheSilentPatch/Proxy-Harvester/releases
```

---

## Features

- Docstrings in [proxy-harvester.py](https://github.com/TheSilentPatch/Proxy-Harvester/blob/main/proxy_harvester.py) makes it super understandable
- Scrapes proxies from a public source with a single command
- Supports HTTP, HTTPS, or all proxies
- Output to a file or directory (auto-creates folders)
- Colored, informative CLI output
- Verbose logging for debugging
- Modern Python packaging and release automation

---

## Usage

```bash
# Basic usage (HTTPS proxies)
python proxy_harvester.py

# HTTP proxies with custom output
python proxy_harvester.py --type http -o http_proxies.txt

# All proxies with verbose output
python proxy_harvester.py -t all -v

# Output to a directory (auto-creates if needed)
python proxy_harvester.py -o ./output/
```

### Options

* `--type` or `-t` (default `https`)

  * Filter proxies by protocol: `http`, `https`, or `all`
* `--output` or `-o`

  * Set output file or directory (default `proxies.txt`)
* `--verbose` or `-v`

  * Enable verbose debug output
* `--version`

  * Show version information

## Output

The harvested proxies will be saved to a `.txt` file, with one proxy per line in this format:

```
123.45.67.89:8080
12.34.56.78:3128
```

## Release Automation

- Releases are triggered by pushing a tag like `v2.0.0` to GitHub.
- GitHub Actions will build the package and upload release assets automatically.
- Release notes are auto-generated.

## Notes

* Uses `requests`, `beautifulsoup4`, and `colorama` with the `lxml` parser.
* By default, pulls proxies from `free-proxy-list.net`.
* Designed for educational or ethical usage only — respect the site’s terms of service.
* You should validate each proxy before using it in production.

## Author

[**Silent Coder**](https://github.com/TheSilentPatch/)

# Happy harvesting!
