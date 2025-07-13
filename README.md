# Proxy Harvester

Easily scrape free proxies from public sources and save them in `ip:port` format. This modern Python CLI tool is fast, flexible, and easy to use.

---

## 🚀 Quick Start

Install directly from GitHub:
```bash
pip install git+https://github.com/TheSilentPatch/Proxy-Harvester.git
```

Then run:
```bash
proxy-harvester --help
```

---

## 📦 Features
- Scrapes proxies from multiple public sources
- Supports HTTP, HTTPS, or all proxies
- Output to a file or directory (auto-creates folders)
- Colored, informative CLI output
- Verbose logging for debugging
- Modern Python packaging and release automation

---

## 🛠️ Installation

**Latest version:**
```bash
pip install git+https://github.com/TheSilentPatch/Proxy-Harvester.git
```

**Specific release:**
```bash
pip install git+https://github.com/TheSilentPatch/Proxy-Harvester.git@<release_tag>
# See releases: https://github.com/TheSilentPatch/Proxy-Harvester/releases
```

**From source:**
```bash
git clone https://github.com/TheSilentPatch/Proxy-Harvester.git
cd Proxy-Harvester
pip install .
```

---

## 📝 Usage Examples

### Basic CLI usage
```bash
proxy-harvester
```

### Filter by protocol
```bash
proxy-harvester --type http
proxy-harvester --type all
```

### Custom output file
```bash
proxy-harvester -o myproxies.txt
```

### Verbose/debug output
```bash
proxy-harvester -v
```

### See all options
```bash
proxy-harvester --help
```

---

## ⚙️ Command-line Options
| Option            | Description                                 | Default         |
|-------------------|---------------------------------------------|-----------------|
| `--type`, `-t`    | Proxy type: `http`, `https`, or `all`       | `https`         |
| `--output`, `-o`  | Output file or directory                    | `proxies.txt`   |
| `--verbose`, `-v` | Enable verbose debug output                 | Off             |
| `--version`       | Show version information                    |                 |

---

## 📂 Output Format
Each harvested proxy is saved on a new line in the format:
```
IP:PORT
```
Example:
```
123.45.67.89:8080
12.34.56.78:3128
```

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🔗 Links
- [GitHub Repository](https://github.com/TheSilentPatch/Proxy-Harvester)
- [Report Issues](https://github.com/TheSilentPatch/Proxy-Harvester/issues)

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
