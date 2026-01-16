# Standards Reference Guide

Quick reference guide to all documentation and SDLC standards for THC Meal Prep Planner.

## 📚 Documentation Overview

This repository maintains comprehensive standards to ensure code quality, consistency, and maintainability.

### Core Documents

| Document | Purpose | Audience |
|----------|---------|----------|
| [README.md](../README.md) | Project overview, setup, and usage | All users and contributors |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | How to contribute, PR process | Contributors |
| [CODE_STYLE.md](../CODE_STYLE.md) | Coding standards for Python & TypeScript | Developers |
| [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md) | Documentation requirements | Developers |
| [ONBOARDING.md](ONBOARDING.md) | Getting started guide | New contributors |

## 🚀 Quick Start for Contributors

1. **First Time Setup**
   - Read: [ONBOARDING.md](ONBOARDING.md)
   - Review: [CONTRIBUTING.md](../CONTRIBUTING.md)

2. **Before Writing Code**
   - Review: [CODE_STYLE.md](../CODE_STYLE.md)
   - Review: [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md)

3. **Before Submitting a PR**
   - Check: [CONTRIBUTING.md - PR Process](../CONTRIBUTING.md#pull-request-process)
   - Use: [Pull Request Template](../.github/pull_request_template.md)

## 📝 Key Standards Summary

### Code Style

#### Python
- **Standard**: PEP 8
- **Line Length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Type Hints**: Required for all functions
- **Documentation**: Google-style docstrings

#### TypeScript
- **Standard**: Google TypeScript Style Guide
- **Line Length**: 100 characters
- **Indentation**: 2 spaces
- **Type Safety**: Avoid `any`, use strict types
- **Documentation**: JSDoc for all public APIs

### Documentation Requirements

#### All Code Must Be:
- ✅ **Explainable**: Clear purpose and logic
- ✅ **Documented**: Appropriate docstrings/JSDoc
- ✅ **Maintainable**: Easy to understand and modify
- ✅ **Consistent**: Follow established patterns

#### Required Documentation:
- **Python**: Docstrings for modules, classes, public functions
- **TypeScript**: JSDoc for classes, interfaces, exported functions
- **Comments**: Explain "why", not "what"
- **README**: For modules and packages

### Pull Request Process

#### Before Submitting
1. ✅ Code follows style guidelines
2. ✅ All code is properly documented
3. ✅ Changes are manually tested
4. ✅ Commit messages are clear
5. ✅ PR template is filled out

#### Review Checklist
- [ ] Follows [Code Style Guide](../CODE_STYLE.md)
- [ ] Meets [Documentation Standards](DOCUMENTATION_STANDARDS.md)
- [ ] Changes are minimal and focused
- [ ] Code is readable and maintainable
- [ ] Testing documented in PR description

### Branch Naming

```
feature/description   - New features
fix/description      - Bug fixes
docs/description     - Documentation updates
refactor/description - Code refactoring
test/description     - Test additions
```

### Commit Message Format

```
<type>: <short description>

<optional longer description>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🧪 Testing Standards

- **CI Testing**: Not required
- **Manual Testing**: Required for all changes
- **Documentation**: Describe testing in PR description
- **Verification**: Ensure no existing functionality breaks

## 📋 Code Review Guidelines

### For Authors
- Be responsive to feedback
- Update PR based on reviews
- Mark conversations as resolved
- Keep changes focused

### For Reviewers
- Be constructive and respectful
- Check style and documentation compliance
- Verify code maintainability
- Focus on readability

## 🎯 Quality Principles

1. **Readability First**: Code is read more than written
2. **Minimal Changes**: Only change what's necessary
3. **Consistency**: Follow existing patterns
4. **Documentation**: All code must be explainable
5. **Simplicity**: Prefer clear over clever

## 📖 Language-Specific Quick Reference

### Python Docstring Template

```python
def function_name(param1: type1, param2: type2) -> return_type:
    """Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
        
    Returns:
        Description of return value.
        
    Raises:
        ErrorType: When this error occurs.
        
    Example:
        >>> function_name(arg1, arg2)
        expected_output
    """
    pass
```

### TypeScript JSDoc Template

```typescript
/**
 * Short description of the function.
 * 
 * Longer description if needed.
 * 
 * @param param1 - Description of param1
 * @param param2 - Description of param2
 * @returns Description of return value
 * @throws {ErrorType} When this error occurs
 * 
 * @example
 * ```typescript
 * functionName(arg1, arg2);
 * // expected output
 * ```
 */
function functionName(param1: Type1, param2: Type2): ReturnType {
  // Implementation
}
```

## 🔧 Recommended Tools

### Python
- **Formatter**: [Black](https://black.readthedocs.io/)
- **Linter**: [Ruff](https://docs.astral.sh/ruff/) or [Pylint](https://pylint.org/)
- **Type Checker**: [mypy](http://mypy-lang.org/)
- **Doc Checker**: [pydocstyle](http://www.pydocstyle.org/)

### TypeScript
- **Formatter**: [Prettier](https://prettier.io/)
- **Linter**: [ESLint](https://eslint.org/)
- **Type Checker**: TypeScript compiler (`tsc`)
- **Doc Generator**: [TypeDoc](https://typedoc.org/)

## 🆘 Getting Help

### Documentation Questions
1. Search this guide
2. Check the specific standard document
3. Review examples in the codebase
4. Open an issue with "question" label

### Process Questions
1. Review [CONTRIBUTING.md](../CONTRIBUTING.md)
2. Check closed/merged PRs for examples
3. Ask in your PR or issue

## 📚 Complete Documentation Index

### Project Documentation
- [README.md](../README.md) - Project overview
- [.gitignore](../.gitignore) - Ignored files and directories

### Standards Documentation
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [CODE_STYLE.md](../CODE_STYLE.md) - Code style standards
- [docs/DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md) - Documentation requirements
- [docs/ONBOARDING.md](ONBOARDING.md) - New contributor guide
- [docs/STANDARDS_REFERENCE.md](STANDARDS_REFERENCE.md) - This document

### Templates
- [.github/pull_request_template.md](../.github/pull_request_template.md) - PR template
- [.github/ISSUE_TEMPLATE/bug_report.md](../.github/ISSUE_TEMPLATE/bug_report.md) - Bug report template
- [.github/ISSUE_TEMPLATE/feature_request.md](../.github/ISSUE_TEMPLATE/feature_request.md) - Feature request template
- [.github/ISSUE_TEMPLATE/documentation.md](../.github/ISSUE_TEMPLATE/documentation.md) - Documentation update template
- [.github/ISSUE_TEMPLATE/question.md](../.github/ISSUE_TEMPLATE/question.md) - Question template

## 🎓 Learning Resources

### Python
- [PEP 8 Style Guide](https://pep8.org/)
- [PEP 257 Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

### TypeScript
- [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [JSDoc Documentation](https://jsdoc.app/)

### Git & GitHub
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## ✅ Pre-Submission Checklist

Before submitting any PR:

- [ ] Read relevant standards documentation
- [ ] Code follows [CODE_STYLE.md](../CODE_STYLE.md)
- [ ] Code is documented per [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md)
- [ ] Changes are manually tested
- [ ] Commit messages follow conventions
- [ ] PR template is complete
- [ ] Related issues are linked

## 🔄 Keeping Standards Updated

These standards are living documents:

- **Suggest Improvements**: Open an issue or PR
- **Discuss Changes**: Use issue discussions
- **Stay Current**: Review standards periodically
- **Update as Needed**: Standards evolve with the project

## 📞 Contact

For questions about these standards:
- Open an issue with the "question" label
- Reference the specific standard document
- Provide context for your question

---

**Remember**: These standards exist to help us build better software together. When in doubt, prioritize readability and maintainability over rigid rule-following.
