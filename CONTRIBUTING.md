# Contributing to DivineNode

We welcome contributions to the DivineNode project! This document provides guidelines for contributing to the codebase.

## Getting Started

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Test your changes thoroughly
5. Submit a pull request

## Development Workflow

### Branching Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Feature development branches
- `hotfix/*`: Critical bug fixes

### Commit Guidelines

- Use clear, descriptive commit messages
- Follow conventional commit format: `type(scope): description`
- Examples:
  - `feat(android): add voice recognition capability`
  - `fix(api): resolve authentication timeout issue`
  - `docs(readme): update installation instructions`

### Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add/update tests for new functionality
4. Request review from maintainers
5. Address review feedback promptly

## Code Standards

### Android (Kotlin)
- Follow [Kotlin coding conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Use meaningful variable and function names
- Add KDoc comments for public APIs
- Maintain consistent indentation (4 spaces)

### Backend (Python)
- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Add docstrings for modules, classes, and functions
- Maintain test coverage above 80%
- Use meaningful variable names

### General Guidelines
- Keep functions small and focused
- Write self-documenting code
- Add comments for complex logic
- Ensure cross-platform compatibility
- Follow SOLID principles

## Testing

### Android Testing
- Write unit tests for business logic
- Include UI tests for critical user flows
- Use Android testing framework conventions

### Backend Testing
- Write unit tests using pytest
- Include integration tests for API endpoints
- Mock external dependencies appropriately
- Test error conditions and edge cases

### Test Coverage
- Aim for minimum 80% code coverage
- Focus on testing critical business logic
- Include both positive and negative test cases

## Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for structural changes
- Add inline comments for complex algorithms
- Document API changes in relevant files

## Issue Guidelines

### Bug Reports
- Use the bug report template
- Provide clear reproduction steps
- Include system information
- Attach relevant logs/screenshots

### Feature Requests
- Use the feature request template
- Describe the use case clearly
- Explain expected behavior
- Consider implementation impact

## Security

- Follow secure coding practices
- Never commit secrets or credentials
- Use environment variables for configuration
- Report security issues privately to maintainers

## Code Review Checklist

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Security considerations addressed
- [ ] Performance impact considered
- [ ] Backward compatibility maintained

## Questions?

If you have questions about contributing, please:
- Check existing documentation
- Search closed issues for similar questions
- Open a discussion issue for complex topics
- Contact maintainers for sensitive matters

Thank you for contributing to DivineNode!