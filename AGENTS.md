# AGENTS.md

This file contains guidelines and commands for AI agents working in this repository.

## Project Overview

This is a multi-lesson AI agent development course repository with Python-based projects focusing on Claude AI capabilities. The main mature projects are:
- **L6**: Task CLI (Typer-based command-line tool)
- **L7**: Multi-agent system (Claude Agent SDK)

## Development Commands

### Environment Setup
```bash
# Install dependencies for any project
uv sync

# For L6 Task CLI - install globally
uv tool install -e .
```

### Testing Commands
```bash
# Run all tests
uv run pytest

# Run single test file
uv run pytest tests/test_add.py

# Run single test function
uv run pytest tests/test_add.py::TestAdd::test_adds_task_with_minimal_input

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=src
```

### Running Applications
```bash
# L6 Task CLI
uv run task <command>

# L7 Agent System
uv run python agent.py
```

## Code Style Guidelines

### Python Conventions
1. **Type Hints**: Required on all function signatures and class attributes
2. **Docstrings**: Required for all public functions and classes using Google-style
3. **Imports**: Standard library → third-party → local imports (each section alphabetized)
4. **Naming**: 
   - Functions/variables: `snake_case`
   - Classes: `PascalCase`
   - Constants: `UPPER_SNAKE_CASE`
5. **Error Handling**: Use descriptive error messages with proper exception types

### Code Organization (L6 Pattern)
```
src/project_name/
├── main.py           # Entry point
├── commands/         # CLI command modules
├── models.py         # Data models with Pydantic
├── storage.py        # Data persistence layer
├── display.py        # Output formatting
└── constants.py      # Application constants

tests/
├── conftest.py       # Test fixtures
└── test_*.py         # Test files
```

### Testing Standards
- Use pytest with descriptive test class names inheriting from `object`
- Test method names should describe the scenario: `test_<action>_when_<condition>_expects_<result>`
- Use fixtures for common setup (see `tests/conftest.py`)
- Test both happy path and edge cases
- Use `typer.testing.CliRunner` for CLI testing
- Maintain comprehensive test coverage

### Project-Specific Guidelines

#### L6 Task CLI
- Use Typer for CLI framework
- Rich for terminal formatting
- JSON file storage in `~/.task/` directory
- Follow existing command patterns in `src/task/commands/`

#### L7 Agent System  
- Use Claude Agent SDK
- Implement async/await patterns
- Use python-dotenv for environment variables
- Follow multi-agent communication patterns

## Working with Existing Agents

This repository contains several AI agents and skills:

### Cursor Skills
- Located in `.cursor/skills/`
- Custom skills for marketing analysis, time series, practice questions

### Claude Skills  
- Located in `.claude/skills/`
- Follow the established skill pattern when creating new ones

### Agent Integration
- When modifying CLI commands, ensure compatibility with existing agents
- Test agent workflows after making changes
- Maintain backward compatibility for agent integrations

## File Creation Guidelines

### When creating new files:
1. Follow the existing directory structure
2. Use the established naming conventions
3. Add appropriate type hints and docstrings
4. Include corresponding test files
5. Update any relevant configuration files

### When modifying existing files:
1. Maintain existing code style and patterns
2. Add tests for new functionality
3. Update documentation as needed
4. Ensure agent compatibility

## Environment Variables

For L7 Agent System:
- Create `.env` file with required API keys
- Use `python-dotenv` for loading environment variables

## Package Management

- Use `uv` for dependency management
- `pyproject.toml` for project configuration
- Hatchling as build backend
- Follow semantic versioning for releases

## Common Patterns

### CLI Command Structure (L6)
```python
def command_name(arg: str, optional_arg: str = "default") -> None:
    """Command description."""
    # Validate input
    # Process data
    # Store/display results
```

### Error Handling Pattern
```python
if not valid_input:
    raise typer.BadParameter("Descriptive error message")
```

### Testing Pattern
```python
class TestFeature(object):
    def test_action_when_condition_expects_result(self):
        # Arrange
        # Act  
        # Assert
```

## Important Notes

- This is an educational repository - maintain clarity and good documentation
- Test thoroughly before committing changes
- Follow the established patterns rather than introducing new conventions
- Consider the impact on existing agents and skills when making changes