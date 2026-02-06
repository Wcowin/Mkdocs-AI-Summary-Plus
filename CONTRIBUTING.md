# Contributing to MkDocs AI Summary Plugin

We love your input! We want to make contributing to MkDocs AI Summary Plugin as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- A text editor or IDE

### Setting Up Your Development Environment

1. **Fork and Clone the Repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/mkdocs-ai-summary.git
   cd mkdocs-ai-summary
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**

   ```bash
   pip install -e ".[dev]"
   # Or alternatively:
   pip install -r requirements-dev.txt
   ```

4. **Set Up Pre-commit Hooks** (Optional but recommended)

   ```bash
   pre-commit install
   ```

5. **Create Environment File**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys for testing
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=mkdocs_ai_summary

# Run specific test file
pytest tests/test_plugin.py

# Run tests with verbose output
pytest -v
```

### Code Quality

We use several tools to maintain code quality:

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Lint with flake8
flake8 .

# Type checking with mypy
mypy .

# Run all quality checks
make lint  # If Makefile is available
```

### Testing Your Changes

1. **Unit Tests**: Ensure all unit tests pass
2. **Integration Tests**: Test with a real MkDocs project
3. **Manual Testing**: Test with different AI services and configurations

#### Manual Testing Setup

```bash
# Create a test MkDocs project
mkdocs new test-project
cd test-project

# Install your local plugin
pip install -e /path/to/mkdocs-ai-summary

# Configure mkdocs.yml
echo "
plugins:
  - ai-summary:
      ai_service: 'deepseek'
      summary_language: 'en'
" >> mkdocs.yml

# Test build
mkdocs build
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Maximum line length: 88 characters (Black default)

### Code Organization

- Keep functions and classes focused and small
- Use descriptive variable and function names
- Add docstrings to all public functions and classes
- Include type hints for function parameters and return values

### Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions and classes
- Update CHANGELOG.md for notable changes
- Include examples in docstrings when helpful

### Commit Messages

Use clear and meaningful commit messages:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(ai-services): add support for Claude API
fix(cache): resolve cache invalidation issue
docs(readme): update installation instructions
```

## Issue Reporting

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/mkdocs-ai-summary/mkdocs-ai-summary/issues).

### Bug Reports

Great bug reports tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

### Feature Requests

We welcome feature requests! Please:

- Explain the feature and why it would be useful
- Provide examples of how it would be used
- Consider the scope and complexity
- Check if similar features already exist

## Project Structure

```
mkdocs-ai-summary/
├── mkdocs_ai_summary/          # Main plugin package
│   ├── __init__.py             # Package initialization
│   ├── plugin.py               # Main plugin class
│   ├── ai_services.py          # AI service management
│   ├── cache_manager.py        # Caching functionality
│   ├── content_processor.py    # Content processing
│   └── config_manager.py       # Configuration management
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_plugin.py
│   ├── test_ai_services.py
│   ├── test_cache_manager.py
│   ├── test_content_processor.py
│   └── test_config_manager.py
├── docs/                       # Documentation
├── examples/                   # Example configurations
├── setup.py                    # Package setup (legacy)
├── pyproject.toml             # Modern package configuration
├── requirements.txt           # Runtime dependencies
├── requirements-dev.txt       # Development dependencies
├── README.md                  # Main documentation
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # This file
└── LICENSE                   # MIT License
```

## Adding New AI Services

To add support for a new AI service:

1. **Update `ai_services.py`**:
   - Add service configuration
   - Implement API call method
   - Add error handling

2. **Update Configuration**:
   - Add service to valid options
   - Update documentation

3. **Add Tests**:
   - Unit tests for the new service
   - Integration tests
   - Mock API responses

4. **Update Documentation**:
   - README.md
   - Configuration examples
   - API key setup instructions

## Release Process

1. Update version in `mkdocs_ai_summary/__init__.py`
2. Update `CHANGELOG.md`
3. Create a pull request
4. After merge, create a GitHub release
5. PyPI release is automated via GitHub Actions

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

### Communication

- Use GitHub Issues for bug reports and feature requests
- Use GitHub Discussions for questions and general discussion
- Be clear and concise in your communication
- Provide context and examples when asking for help

## Getting Help

If you need help with development:

1. Check existing issues and discussions
2. Read the documentation thoroughly
3. Ask questions in GitHub Discussions
4. Reach out to maintainers if needed

## Recognition

Contributors will be recognized in:

- CHANGELOG.md for significant contributions
- README.md contributors section
- GitHub contributors page

Thank you for contributing to MkDocs AI Summary Plugin! 🎉