# GitHub Copilot Instructions for Proxy-Harvester

## 🚀 Commit Messages

* Follow **Conventional Commits**:

  * `feat:` for new features
  * `fix:` for bug fixes
  * `docs:` for documentation changes
  * `style:` for code style changes (no logic change)
  * `refactor:` for refactoring code
  * `test:` for adding or improving tests
  * `chore:` for build processes or auxiliary tools
* Example: `feat(parser): add proxy list parser`
* Keep commit messages short, clear, and in imperative mood.

## 🧩 Code Quality

* Prioritize human-readable and maintainable code.
* Use clear and descriptive variable and function names.
* Avoid single-letter variable names except for indexes in loops.
* Add inline comments where necessary to clarify logic.
* Write idiomatic Python following PEP8 style guidelines.
* Prefer modern Python features (type hints, f-strings, pathlib, etc.).
* Avoid overcomplicating solutions — simple is better than complex.

## 📚 Documentation

* Add docstrings to all public classes and functions.
* Follow PEP257 docstring conventions.
* Include clear parameter and return value documentation.
* Provide usage examples in comments if logic is non-trivial.

## 🔒 Security & Safety

* Avoid use of `eval`, `exec`, or insecure deserialization (like `pickle.loads` with untrusted data).
* Validate and sanitize all external inputs.
* Prefer `with` context managers to handle files or network resources safely.

## 🛠 Project Structure

* Keep reusable code inside Python packages (e.g. `proxy_harvester/`).
* Keep the CLI entry point separate (if needed).
* Maintain a clear folder hierarchy with logical separation (e.g. `tests/`, `scripts/`, `docs/`).

## 💡 Testing

* Follow `pytest` style tests in the `tests/` folder.
* Use descriptive test function names.
* Include tests for critical code paths.

## 🤖 Copilot Suggestions

* When suggesting commits, default to Conventional Commit patterns.
* When suggesting code, prioritize readability over cleverness.
* When suggesting PR descriptions, include:

  * **What changed**
  * **Why it changed**
  * **How to test it**
* Suggest semantic versioning aligned with features/fixes.
