# Contributing to KeyHound

Thanks for your interest in contributing! Please follow these guidelines to ensure smooth reviews.

## Getting started
- Fork and clone the repo
- Create a feature branch: `git checkout -b feature/your-change`
- Use a Python venv: `python3 -m venv .venv && source .venv/bin/activate`
- Install: `pip install -e .`

## Coding standards
- Python 3.8+
- Prefer clear, descriptive names; avoid unnecessary complexity
- Add or update tests where meaningful (`tests/`)
- Keep comments concise and only when non-obvious

## Commit messages
- Use conventional style where possible: `feat:`, `fix:`, `docs:`, `chore:`
- Keep subject ≤ 72 chars; include context in body if needed

## Pull requests
- Rebase on latest `main` before opening
- Include a brief description, screenshots for UI, and testing notes
- Link related issues (e.g., `Fixes #123`)

## Security
- Do not include secrets in code or configs
- Report sensitive issues privately if applicable

## License
By contributing, you agree your contributions are licensed under the Apache-2.0 License.
