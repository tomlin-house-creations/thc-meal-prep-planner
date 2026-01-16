# Onboarding Guide

Welcome to the THC Meal Prep Planner project! This guide will help you get started as a contributor.

## Table of Contents

- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Standards and Guidelines](#standards-and-guidelines)
- [Getting Help](#getting-help)

## About the Project

THC Meal Prep Planner is a meal planning and preparation application designed to help users:

- Plan weekly meals
- Manage recipes and ingredients
- Generate shopping lists
- Track nutritional information
- Streamline meal preparation

### Technology Stack

- **Backend**: Python (planned)
- **Frontend**: TypeScript/React (planned)
- **Database**: TBD
- **Deployment**: TBD

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Git**: Version control system
  - [Download Git](https://git-scm.com/downloads)
  - Verify: `git --version`

- **Python**: Version 3.9 or higher (for backend development)
  - [Download Python](https://www.python.org/downloads/)
  - Verify: `python --version` or `python3 --version`

- **Node.js**: Version 18 or higher (for frontend development)
  - [Download Node.js](https://nodejs.org/)
  - Verify: `node --version`

- **Package Managers**:
  - pip (comes with Python)
  - npm (comes with Node.js)

### Initial Setup

1. **Fork the Repository**
   
   Visit [https://github.com/tomlin-house-creations/thc-meal-prep-planner](https://github.com/tomlin-house-creations/thc-meal-prep-planner) and click "Fork" in the top-right corner.

2. **Clone Your Fork**
   
   ```bash
   git clone https://github.com/YOUR_USERNAME/thc-meal-prep-planner.git
   cd thc-meal-prep-planner
   ```

3. **Add Upstream Remote**
   
   ```bash
   git remote add upstream https://github.com/tomlin-house-creations/thc-meal-prep-planner.git
   ```

4. **Verify Remotes**
   
   ```bash
   git remote -v
   ```
   
   You should see both `origin` (your fork) and `upstream` (main repository).

## Development Setup

### Backend Setup (Python)

When backend code is added, follow these steps:

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application (exact command will depend on project structure)
python -m backend  # or python app.py, python main.py, etc.
```

### Frontend Setup (TypeScript/React)

When frontend code is added, follow these steps:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# In another terminal, run type checking
npm run type-check
```

### Code Quality Tools

#### Python

```bash
# Install development tools
pip install black ruff mypy pytest

# Format code
black .

# Lint code
ruff check .

# Type check
mypy .

# Run tests
pytest
```

#### TypeScript

```bash
# Install development tools (usually in package.json)
npm install

# Format code
npm run format

# Lint code
npm run lint

# Type check
npm run type-check

# Run tests
npm test
```

## Project Structure

```
thc-meal-prep-planner/
├── docs/                    # Documentation
│   ├── DOCUMENTATION_STANDARDS.md
│   └── ONBOARDING.md
├── backend/                 # Python backend (when added)
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── frontend/                # TypeScript/React frontend (when added)
│   ├── src/
│   ├── tests/
│   └── package.json
├── .github/                 # GitHub configuration
│   └── pull_request_template.md
├── CODE_STYLE.md           # Coding standards
├── CONTRIBUTING.md         # Contribution guidelines
├── README.md               # Project overview
└── .gitignore              # Git ignore rules
```

## Development Workflow

### 1. Stay Synchronized

Before starting work, sync with the main repository:

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/add-recipe-search`
- `fix/nutrition-calculation-bug`
- `docs/api-documentation`

### 3. Make Changes

- Write code following the [Code Style Guide](../CODE_STYLE.md)
- Add documentation per [Documentation Standards](DOCUMENTATION_STANDARDS.md)
- Test your changes manually
- Commit regularly with clear messages

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add recipe search functionality"
```

Follow [conventional commit](https://www.conventionalcommits.org/) format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test changes
- `chore:` Build/tooling changes

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Fill out the PR template
4. Link related issues
5. Submit the PR

### 7. Respond to Review Feedback

- Address reviewer comments
- Push additional commits to the same branch
- Mark conversations as resolved
- Request re-review when ready

## Standards and Guidelines

### Required Reading

Before contributing, review these documents:

1. **[CONTRIBUTING.md](../CONTRIBUTING.md)**: Contribution process and PR guidelines
2. **[CODE_STYLE.md](../CODE_STYLE.md)**: Coding standards for Python and TypeScript
3. **[DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md)**: Documentation requirements

### Key Principles

- **Minimal Changes**: Make the smallest changes necessary
- **Readability**: Write clear, maintainable code
- **Documentation**: All code must be explainable
- **Consistency**: Follow existing patterns
- **Testing**: Manually test all changes

### Quality Checklist

Before submitting a PR, verify:

- [ ] Code follows style guidelines
- [ ] All functions/classes are documented
- [ ] Changes are manually tested
- [ ] Commit messages are clear
- [ ] No unnecessary files are committed
- [ ] PR description is complete

## Common Tasks

### Running the Application Locally

```bash
# Backend (when available)
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py

# Frontend (when available)
cd frontend
npm run dev
```

### Formatting Code

```bash
# Python
black .

# TypeScript
npm run format
```

### Running Tests

```bash
# Python
pytest

# TypeScript
npm test
```

### Viewing Documentation

Most documentation is in Markdown format and can be viewed:
- On GitHub (rendered automatically)
- In your editor (most support Markdown preview)
- Locally with a Markdown viewer

## Getting Help

### Resources

- **Documentation**: Check the `docs/` directory
- **Issues**: Browse existing issues for similar questions
- **Pull Requests**: Review merged PRs for examples

### Asking Questions

If you need help:

1. **Search First**: Check if your question has been answered
   - Review documentation
   - Search closed issues
   - Look at merged PRs

2. **Open an Issue**: Create a new issue with the "question" label
   - Describe what you're trying to do
   - Include relevant context
   - Show what you've already tried

3. **Be Specific**: Good questions get better answers
   - ❌ "How do I add a feature?"
   - ✅ "I want to add recipe search. Should I create a new service or extend RecipeService?"

### Communication Guidelines

- Be respectful and professional
- Assume good intentions
- Provide context in your questions
- Share what you've tried
- Be patient waiting for responses

## Tips for New Contributors

### Start Small

- Fix typos in documentation
- Improve error messages
- Add missing documentation
- Write tests for existing code

### Learn the Codebase

- Read existing code
- Trace through key features
- Understand the architecture
- Ask questions

### Good First Issues

Look for issues labeled:
- `good first issue`
- `documentation`
- `help wanted`

### Code Review is Learning

- Don't take feedback personally
- Ask questions if you don't understand
- Learn from reviewer suggestions
- Review others' PRs to learn

### Continuous Improvement

- Each PR is a learning opportunity
- Apply feedback to future contributions
- Share knowledge with other contributors
- Help improve documentation

## Next Steps

1. **Set up your development environment** following the steps above
2. **Review the standards** (CONTRIBUTING.md, CODE_STYLE.md, etc.)
3. **Find an issue** to work on or explore the codebase
4. **Make your first contribution**!

Welcome to the team! We're excited to have you contribute to THC Meal Prep Planner.

## Questions?

If you have questions about this guide or need help getting started, please open an issue with the "question" label.
