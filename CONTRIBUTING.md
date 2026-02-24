# Contributing to THC Meal Prep Planner

Thank you for your interest in contributing! This project is markdown-first — all data lives in markdown and YAML files, and custom agents handle all computation. There is no application code to build or run.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Markdown Style](#markdown-style)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.

## Ways to Contribute

### Add a Recipe

1. Open an issue with the title: "Add recipe: \<Recipe Name\>"
2. Assign the `recipe-creator` agent — it will create the recipe file and open a PR
3. Review the PR and suggest any changes
4. Merge when satisfied

Alternatively, submit a PR directly with a new file in `recipes/` following the template in `recipes/breakfast-burritos.md`. See [CODE_STYLE.md](CODE_STYLE.md) for markdown formatting standards.

### Improve a User Profile

Edit the relevant file in `profiles/` and open a PR. Profile files are plain markdown — update dietary constraints, preferences, or nutritional goals as needed.

### Add or Refine Constraints

Edit or add YAML files in `constraints/`. See [docs/CONSTRAINT_SCHEMAS.md](docs/CONSTRAINT_SCHEMAS.md) for the schema reference.

### Improve an Agent Prompt

The agent definitions live in `.github/agents/`. Improving the instructions in those files directly improves the quality of generated meal plans, recipes, and grocery lists. Open a PR with your proposed changes and explain the improvement.

### Report a Problem with Agent Output

Open an issue describing the problem with a generated file (meal plan, recipe, grocery list). Link to the relevant file and describe what was incorrect or missing.

## Development Workflow

### Branch Naming Conventions

- `feature/description` — New features or content
- `fix/description` — Corrections to existing content
- `docs/description` — Documentation updates
- `agent/description` — Agent prompt improvements

### Commit Messages

Write clear, concise commit messages:

```
<type>: <short description>
```

**Types:**
- `feat` — New recipe, profile, or agent
- `fix` — Correction to existing content
- `docs` — Documentation changes
- `chore` — Workflow or configuration changes

**Examples:**
```
feat: add chicken tikka masala recipe
fix: correct sodium values in breakfast-burritos.md
docs: update constraint schema documentation
chore: simplify deploy-pages workflow
```

### Making Changes

1. Fork the repository and create a branch
2. Follow the [markdown formatting standards](CODE_STYLE.md)
3. Verify your changes render correctly (preview in GitHub or locally with Jekyll)
4. Submit a pull request using the PR template

## Pull Request Process

### Before Submitting a PR

1. Ensure markdown is well-formatted and all links resolve
2. For recipes, verify all required sections are present (see `CODE_STYLE.md`)
3. For agent prompt changes, describe the improvement and any test cases

### Submitting a PR

1. Push your branch to your fork
2. Open a Pull Request against the `main` branch
3. Fill out the PR template completely
4. Link any related issues

### PR Review

- Reviewers will check markdown formatting, completeness, and accuracy
- For recipes, reviewers will verify the template structure is followed
- For agent prompts, reviewers may test the agent output before approving

## Markdown Style

See [CODE_STYLE.md](CODE_STYLE.md) for detailed markdown formatting standards.

## Questions?

If you have questions, please:

1. Review this guide and related documentation
2. Check existing issues and PRs
3. Open a new issue with the "question" label

Thank you for contributing to THC Meal Prep Planner!
