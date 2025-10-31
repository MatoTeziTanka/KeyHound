# 🤝 Contributing to KeyHound

**Version:** V1.1.0  
**Last Updated:** October 31, 2025

Thanks for your interest in contributing to KeyHound! This guide will help you understand our development workflow, coding standards, and version control practices.

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Version Control Standards](#version-control-standards)
3. [Coding Standards](#coding-standards)
4. [Documentation Requirements](#documentation-requirements)
5. [Testing Guidelines](#testing-guidelines)
6. [Commit Messages](#commit-messages)
7. [Pull Requests](#pull-requests)
8. [Security](#security)
9. [AI Collaboration](#ai-collaboration)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ (3.12+ recommended)
- Git
- Basic understanding of Bitcoin cryptography (helpful but not required)

### Setup Steps

1. **Fork and clone the repo:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/KeyHound.git
   cd KeyHound
   ```

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   # OR for bug fixes
   git checkout -b fix/bug-description
   ```

3. **Set up Python virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -e .
   pip install -r requirements.txt
   ```

5. **Verify installation:**
   ```bash
   python3 main.py --help
   ```

---

## 📦 Version Control Standards

### Version Numbering

**Format:** `VMAJOR.MINOR.PATCH`

- **MAJOR (V1.x.x → V2.x.x):** New AI Colab session with major features or architectural changes
- **MINOR (Vx.1.x → Vx.2.x):** AI response within same session adding features/improvements
- **PATCH (Vx.x.1 → Vx.x.2):** Small fixes, typos, corrections (no AI assistance required)

### Module Header Requirements

Every Python module **must** include a header with version information:

```python
"""
Module Name: core/your_module.py
Version: V1.1.0
Last Updated: 2025-10-31
AI Session: Session 2 (Claude Sonnet 4.5)
Status: Production | Development | Deprecated

Description:
    Clear, concise description of what this module does.
    Include key features and responsibilities.

Changelog:
    V1.0.0 (2025-10-14): Initial implementation
    V1.1.0 (2025-10-31): Added feature X, improved Y
    
Dependencies:
    - module1.py V1.0.0
    - module2.py V1.1.0
    - Python 3.8+

Usage:
    from core.your_module import YourClass
    obj = YourClass(param=value)
    result = obj.method()
"""
```

### Version Update Checklist

When making changes:

1. **Update module header version**
2. **Add changelog entry** in module header
3. **Update VERSION.md** if creating new file or major change
4. **Update PROGRESS.md** for significant milestones
5. **Update AI_COLLABORATION.md** session history (for AI contributors)

---

## 💻 Coding Standards

### General Principles

- **Python 3.8+** compatibility
- **Clear, descriptive names** over brevity
- **Explicit is better than implicit** (Zen of Python)
- **Don't Repeat Yourself (DRY)**
- **Keep functions focused** (single responsibility)

### Style Guidelines

- **PEP 8** compliance (use `black` or `autopep8`)
- **Type hints** for all function parameters and return values
- **Docstrings** for all public functions, classes, and modules
- **Maximum line length:** 100 characters (120 acceptable for readability)
- **Import order:** Standard library → Third-party → Local modules

### Example: Well-Documented Function

```python
def solve_puzzle(
    bits: int,
    target_address: Optional[str] = None,
    max_attempts: Optional[int] = None,
    timeout: int = 3600
) -> Dict[str, Any]:
    """
    Solve a Bitcoin puzzle of specified bit length.
    
    This function generates and tests Bitcoin private keys within a specified
    bit range until the target address is found or limits are reached.
    
    Args:
        bits: Puzzle difficulty (40-66 bits). Higher = more difficult.
        target_address: Bitcoin address to find. If None, runs in benchmark mode.
        max_attempts: Maximum keys to test. If None, calculated from puzzle size.
        timeout: Maximum seconds to run before stopping (default 3600 = 1 hour).
    
    Returns:
        Dictionary containing:
            - private_key (str): Found key in hex format (if solved)
            - address (str): Generated Bitcoin address
            - attempts (int): Total keys tested
            - time_elapsed (float): Seconds taken
            - solved (bool): Whether puzzle was solved
            - checkpoint_saved (bool): Whether progress was checkpointed
    
    Raises:
        ValueError: If bits < 40 or bits > 66 (invalid difficulty)
        RuntimeError: If Bitcoin cryptography initialization fails
    
    Example:
        >>> keyhound = SimpleKeyHound(verbose=True)
        >>> result = keyhound.solve_puzzle(
        ...     bits=67,
        ...     target_address="1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",
        ...     timeout=3600
        ... )
        >>> if result['solved']:
        ...     print(f"Found key: {result['private_key']}")
    
    Notes:
        - Progress is automatically checkpointed every 60 seconds
        - On restart, solving resumes from last checkpoint
        - Checkpoint file: checkpoints/puzzle_{bits}_checkpoint.json
    """
    # Implementation here...
```

### Error Handling

**Always use specific exception types:**

```python
# ❌ Bad: Catches everything, hard to debug
try:
    result = do_something()
except:
    pass

# ✅ Good: Specific exceptions, proper logging
try:
    result = do_something()
except ValueError as e:
    logger.error(f"Invalid value provided: {e}")
    raise
except KeyError as e:
    logger.warning(f"Missing key {e}, using default")
    result = default_value
except Exception as e:
    logger.exception(f"Unexpected error in do_something: {e}")
    raise RuntimeError("Something operation failed") from e
```

---

## 📝 Documentation Requirements

### Module Documentation

- **Module docstring** at top of file (see header template above)
- **Version information** in header
- **Changelog** with version history
- **Usage examples** in docstring

### Function Documentation

- **Docstring** for every public function/method
- **Args, Returns, Raises** sections
- **Type hints** in function signature
- **Usage example** for complex functions

### Class Documentation

```python
class BitcoinPuzzleSolver:
    """
    High-performance Bitcoin puzzle solver with checkpointing.
    
    This class provides CPU and GPU-accelerated solving for Bitcoin puzzles
    with automatic progress checkpointing and resume capability.
    
    Attributes:
        verbose (bool): Enable detailed logging output
        start_time (float): Unix timestamp when solver initialized
        keys_generated (int): Total keys generated in current session
    
    Example:
        >>> solver = BitcoinPuzzleSolver(verbose=True)
        >>> result = solver.solve(puzzle_bits=67, timeout=3600)
        >>> print(f"Keys tested: {result['attempts']}")
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize Bitcoin puzzle solver.
        
        Args:
            verbose: If True, enable INFO-level logging. If False, WARNING-level only.
        """
        # Implementation...
```

---

## 🧪 Testing Guidelines

### Test Coverage Goals

- **V1.2.0:** 50% coverage for core modules
- **V1.4.0:** 80% coverage for core modules
- **V2.0.0:** 90% coverage across entire codebase

### Writing Tests

```python
import unittest
from core.bitcoin_cryptography import BitcoinCryptography

class TestBitcoinCryptography(unittest.TestCase):
    """Test suite for Bitcoin cryptography module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.crypto = BitcoinCryptography()
    
    def test_private_key_to_address(self):
        """Test private key to address conversion."""
        # Known test vector from Bitcoin documentation
        private_key = "0000000000000000000000000000000000000000000000000000000000000001"
        expected_address = "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"
        
        address = self.crypto.generate_bitcoin_address(private_key)
        self.assertEqual(address, expected_address)
    
    def test_invalid_private_key_raises(self):
        """Test that invalid private keys raise ValueError."""
        with self.assertRaises(ValueError):
            self.crypto.generate_bitcoin_address("invalid_key")
```

### Running Tests

```bash
# Run all tests
python3 -m unittest discover tests/

# Run specific test file
python3 -m unittest tests/test_bitcoin_cryptography.py

# Run with coverage report
pip install coverage
coverage run -m unittest discover
coverage report
coverage html  # Generate HTML report in htmlcov/
```

---

## 📝 Commit Messages

### Conventional Commits Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code formatting (no logic change)
- `refactor:` Code restructuring (no behavior change)
- `perf:` Performance improvement
- `test:` Adding or updating tests
- `chore:` Maintenance tasks (dependencies, build, etc.)

### Examples

```bash
# Good commit messages
git commit -m "feat(checkpointing): add range checkpointing to puzzle solver

- Save progress every 60 seconds to checkpoint file
- Resume from last tested key on restart
- Sequential key generation for reproducibility
- Checkpoint deletion on successful solve

Closes #42"

git commit -m "fix(systemd): correct environment variable quoting

Workers were failing due to unquoted SMTP_PASSWORD containing
special characters. This fix properly quotes the value and uses
UnsetEnvironment to clear inherited variables.

Fixes #123"

git commit -m "docs: update README with V1.1.0 features"
```

### Subject Line Rules

- ≤ 72 characters
- Lowercase after type prefix
- No period at end
- Imperative mood ("add" not "added" or "adds")

---

## 🔀 Pull Requests

### Before Opening a PR

1. **Rebase on latest main:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests:**
   ```bash
   python3 -m unittest discover tests/
   ```

3. **Check linting:**
   ```bash
   # Install linters if needed
   pip install flake8 black mypy
   
   # Format code
   black core/ web/ main.py
   
   # Check style
   flake8 core/ web/ main.py --max-line-length=100
   
   # Type check
   mypy core/ web/ main.py
   ```

4. **Update documentation:**
   - Module headers with new version
   - VERSION.md if applicable
   - README if user-facing changes

### PR Template

```markdown
## Description
<!-- Clear description of what this PR does -->

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Version
**Target Version:** V1.2.0  
**Files Modified:**
- `core/module.py` (V1.1.0 → V1.2.0)
- `docs/README.md`

## Testing
<!-- How was this tested? -->
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] Tested on VM191
- [ ] Tested on Colab

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
- [ ] Version numbers updated

## Related Issues
<!-- Link related issues -->
Closes #123
Related to #456

## Screenshots (if applicable)
<!-- Add screenshots for UI changes -->
```

---

## 🔒 Security

### Sensitive Data

- **Never commit secrets** (API keys, passwords, private keys)
- Use **environment variables** for configuration
- Add sensitive files to `.gitignore`
- Use **example config files** with placeholders

### Reporting Security Issues

- **Do not** open public GitHub issues for security vulnerabilities
- Email maintainers privately
- Allow reasonable time for patch before disclosure

---

## 🤖 AI Collaboration

### For AI Contributors

If you're an AI assistant contributing to KeyHound:

1. **Read AI_COLLABORATION.md first** - Complete context essential
2. **Check SESSION History** - Understand what's been done
3. **Update version numbers** - Increment appropriately
4. **Document in PROGRESS.md** - Add session notes
5. **Follow versioning standards** - Module headers, VERSION.md

### Version Increment Guidelines for AI

- **V1.x.1 → V1.x.2:** Small fixes within same session
- **V1.1.x → V1.2.0:** New AI response in session (features added)
- **V1.x.x → V2.0.0:** New AI session with major changes

### Session Documentation

After each AI contribution session, update:

1. **AI_COLLABORATION.md** - Session history section
2. **PROGRESS.md** - Accomplishments and metrics
3. **VERSION.md** - Module version table
4. **Module headers** - Version and changelog

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the Apache-2.0 License.

---

## 🙏 Thank You!

Your contributions make KeyHound better for everyone. Whether you're fixing a typo, adding a feature, or improving documentation, every contribution is valued.

**Questions?** Open a GitHub issue or reach out to maintainers.

---

**Last Updated:** October 31, 2025  
**Version:** V1.1.0  
**Maintained By:** MatoTeziTanka & AI Collaborators
