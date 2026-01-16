# Contributing to THC Meal Prep Planner

Thank you for your interest in contributing to the THC Meal Prep Planner project! This document outlines the standards and procedures for contributing to this repository.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Code Review Guidelines](#code-review-guidelines)
- [Documentation Standards](#documentation-standards)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/thc-meal-prep-planner.git`
3. Create a new branch for your work: `git checkout -b feature/your-feature-name`
4. Review the [Onboarding Guide](docs/ONBOARDING.md) for setup instructions
5. Review the [Code Style Guide](CODE_STYLE.md) and [Documentation Standards](docs/DOCUMENTATION_STANDARDS.md)

## Development Workflow

### Branch Naming Conventions

Use descriptive branch names that follow these patterns:

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions or modifications

### Commit Messages

Write clear, concise commit messages that explain **what** changed and **why**:

```
<type>: <short description>

<optional longer description>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or changes
- `chore`: Build process or auxiliary tool changes

**Examples:**
```
feat: add meal planning calendar view

fix: resolve recipe ingredient calculation error

docs: update API documentation for meal service
```

### Making Changes

1. Make your changes in your feature branch
2. Follow the [Code Style Guide](CODE_STYLE.md)
3. Ensure all code is well-documented (see [Documentation Standards](docs/DOCUMENTATION_STANDARDS.md))
4. Test your changes manually and verify they work as expected
5. Commit your changes with clear commit messages

## Pull Request Process

### Before Submitting a PR

1. Ensure your code follows all style and documentation standards
2. Verify your changes work correctly
3. Update relevant documentation if needed
4. Rebase your branch on the latest main branch if needed

### Submitting a PR

1. Push your branch to your fork
2. Open a Pull Request against the `main` branch
3. Fill out the PR template completely
4. Link any related issues using keywords (e.g., "Closes #123" or "Relates to #456")
5. Add appropriate labels to your PR

### PR Title Format

Use clear, descriptive titles that summarize the change:

```
<type>: <brief description>
```

**Examples:**
- `feat: implement weekly meal planning feature`
- `fix: correct grocery list quantity calculation`
- `docs: add API usage examples`

### PR Description Requirements

Your PR description should include:

1. **Summary**: What does this PR do?
2. **Motivation**: Why is this change needed?
3. **Changes**: List of specific changes made
4. **Testing**: How were the changes tested/verified?
5. **Screenshots**: If applicable, add screenshots or GIFs
6. **Related Issues**: Link to related issues

## Code Review Guidelines

### For Authors

- Be responsive to feedback and questions
- Be open to suggestions and constructive criticism
- Update your PR based on reviewer feedback
- Mark conversations as resolved once addressed

### For Reviewers

- Be respectful and constructive in your feedback
- Focus on code quality, maintainability, and adherence to standards
- Check that:
  - Code follows the [Code Style Guide](CODE_STYLE.md)
  - Code is well-documented according to [Documentation Standards](docs/DOCUMENTATION_STANDARDS.md)
  - Changes are minimal and focused on the stated goal
  - Logic is clear and maintainable
- Approve PRs that meet all standards
- Request changes if standards are not met

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Code is well-documented with appropriate comments/docstrings
- [ ] Changes are focused and minimal
- [ ] Code is readable and maintainable
- [ ] No unnecessary complexity
- [ ] Breaking changes are documented
- [ ] Related documentation is updated

## Documentation Standards

All code must be explainable and maintainable. See:

- [Documentation Standards](docs/DOCUMENTATION_STANDARDS.md) for docstring and commenting guidelines
- [Code Style Guide](CODE_STYLE.md) for language-specific style rules

## Testing

While automated testing in CI is not required, you should:

- Manually test your changes thoroughly
- Document how you tested your changes in the PR description
- Ensure your code doesn't break existing functionality

## Questions?

If you have questions about contributing, please:

1. Review this guide and related documentation
2. Check existing issues and PRs for similar questions
3. Open a new issue with the "question" label

Thank you for contributing to THC Meal Prep Planner!
