# THC Meal Prep Planner

A comprehensive meal planning and preparation application designed to simplify weekly meal planning, recipe management, and grocery shopping.

## Overview

THC Meal Prep Planner helps users plan their meals efficiently by providing tools to:

- 📅 Plan weekly meals with a visual calendar interface
- 📖 Manage and organize recipes with ingredients and instructions
- 🛒 Generate automated shopping lists from meal plans
- 📊 Track nutritional information for recipes and meal plans
- ⏱️ Estimate preparation and cooking times

## Features

### Current Status

This project is in early development. The following features are planned:

- **Recipe Management**: Create, edit, and organize recipes
- **Meal Planning**: Weekly meal calendar with drag-and-drop interface
- **Shopping Lists**: Auto-generated lists based on selected meals
- **Nutrition Tracking**: Calculate nutritional values for recipes and plans
- **Meal Prep Guides**: Step-by-step preparation workflows

## Technology Stack

- **Backend**: Python (planned)
- **Frontend**: TypeScript/React (planned)
- **Database**: TBD
- **Deployment**: TBD

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/tomlin-house-creations/thc-meal-prep-planner.git
cd thc-meal-prep-planner

# Install Python dependencies
pip install -r requirements.txt
```

### Quick Start: Generate a Meal Plan

Try out the meal plan generator to see the system in action:

```bash
# Run the meal plan generator
python scripts/generate_meal_plan.py
```

**What this does:**
- Loads a sample user profile from `profiles/ashuah.md`
- Reads available recipes from `recipes/`
- Applies constraints from `constraints/sample_constraints.yaml`
- Generates a weekly meal plan in `plans/meal_plan_YYYY-MM-DD.md`

**To customize:**
- Add more recipes to `recipes/` folder (use `breakfast-burritos.md` as a template)
- Create your own profile in `profiles/` folder
- Adjust planning rules in `constraints/sample_constraints.yaml`

The script includes thorough ELI5 (Explain Like I'm 5) documentation, making it perfect for learning how the system works!

## Documentation

### Getting Started
- **[Onboarding Guide](docs/ONBOARDING.md)**: Getting started as a contributor
- **[Contributing Guide](CONTRIBUTING.md)**: How to contribute to this project

### Standards & Guidelines  
- **[Code Style Guide](CODE_STYLE.md)**: Coding standards for Python and TypeScript
- **[Documentation Standards](docs/DOCUMENTATION_STANDARDS.md)**: Documentation requirements

### Project Planning
- **[Milestones Summary](docs/MILESTONES_SUMMARY.md)**: Quick reference for project status
- **[Product Requirements Document](docs/PRD.md)**: Detailed product requirements and specifications
- **[Project Roadmap](docs/ROADMAP.md)**: Development milestones and timeline
- **[Milestone Tracking Guide](docs/MILESTONE_TRACKING.md)**: How to use the milestone system

## Contributing

We welcome contributions from the community! Please follow these steps:

1. Read the [Contributing Guide](CONTRIBUTING.md)
2. Review the [Code Style Guide](CODE_STYLE.md) and [Documentation Standards](docs/DOCUMENTATION_STANDARDS.md)
3. Fork the repository and create a feature branch
4. Make your changes following our standards
5. Submit a pull request using the PR template

### Development Standards

This project maintains high standards for code quality and documentation:

- **Code Style**: Follow language-specific style guides (PEP 8 for Python, Google Style for TypeScript)
- **Documentation**: All code must be explainable with proper docstrings and comments
- **Testing**: While CI testing is not required, all changes must be manually tested
- **Code Review**: All PRs require review and must meet quality standards

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Project Structure

```
thc-meal-prep-planner/
├── docs/                    # Documentation
├── profiles/                # User profiles and preferences
├── recipes/                 # Recipe database
├── constraints/             # Planning constraints (dietary, budget, time)
├── calendars/               # Meal calendars and schedules
├── history/                 # Historical meal planning data
├── plans/                   # Generated meal plans and shopping lists
├── scripts/                 # Utility scripts
├── site/                    # Built static site files
├── .github/                 # GitHub templates and workflows
│   └── workflows/           # CI/CD workflows
├── CODE_STYLE.md           # Coding standards
├── CONTRIBUTING.md         # Contribution guidelines
├── pyproject.toml          # Python project configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Roadmap

For detailed project milestones, timeline, and release planning, see the [Project Roadmap](docs/ROADMAP.md).

**Quick Overview**:

- [x] Phase 1: Foundation & Documentation - In Progress
- [ ] Phase 2: Repository Infrastructure
- [ ] Phase 3: Backend Development
- [ ] Phase 4: Frontend Development
- [ ] Phase 5: CI/CD & Quality Assurance
- [ ] Phase 6: MVP Release
- [ ] Phase 7: v1.0 Release
- [ ] Phase 8: Future Enhancements

## License

This project license will be determined.

## Contact

For questions or suggestions, please open an issue on GitHub.

## Acknowledgments

Thank you to all contributors who help make this project better!

---

**Note**: This project is under active development. Features and documentation will be updated as development progresses.
