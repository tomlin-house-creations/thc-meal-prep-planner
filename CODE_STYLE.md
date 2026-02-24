# Code Style Guide

This document defines the formatting standards for the THC Meal Prep Planner project. Since this is a markdown-first project, these standards focus on markdown and YAML formatting.

## Table of Contents

- [General Principles](#general-principles)
- [Markdown Formatting](#markdown-formatting)
- [Recipe File Standards](#recipe-file-standards)
- [Profile File Standards](#profile-file-standards)
- [Constraint File Standards](#constraint-file-standards)
- [Agent Prompt Standards](#agent-prompt-standards)

## General Principles

1. **Readability First**: Files are read by both humans and agents — clarity matters
2. **Consistency**: Follow the patterns established in existing files
3. **Completeness**: All required sections must be present
4. **Accuracy**: Data (nutritional values, quantities, instructions) must be correct

## Markdown Formatting

### Headings

- Use ATX-style headings (`#`, `##`, `###`) — not underline style
- One blank line before and after each heading
- Use sentence case for headings (capitalize only the first word and proper nouns)

### Lists

- Use `-` for unordered list items (not `*` or `+`)
- Use `1.` for ordered list items (numbered steps)
- One blank line before and after a list block when it follows a paragraph

### Tables

- Always include a header row and separator row
- Align separator dashes with column width for readability
- Left-align text columns; right-align number columns where appropriate

### Links

- Use relative links for files within the repository: `[Recipe Name](../recipes/recipe-file.md)`
- Use descriptive link text — never bare URLs as link text

### Checkboxes

- Use `- [ ]` for unchecked items and `- [x]` for checked items
- Grocery lists and checklists should always use checkboxes

### Code Blocks

- Use fenced code blocks with a language identifier when applicable
- Use inline code (backticks) for file paths, command names, and values

## Recipe File Standards

All recipe files in `recipes/` must follow the structure established in `recipes/breakfast-burritos.md`.

### Required Sections (in order)

1. `# Recipe Name` — H1 title, matches the filename (kebab-case → Title Case)
2. `## Recipe Information` — Category, Servings, Prep Time, Cook Time, Total Time, Difficulty
3. `## Tags` — Bullet list of relevant tags
4. `## Description` — 2–4 sentence description
5. `## Ingredients` — Grouped by component with precise measurements
6. `## Instructions` — Numbered steps (`### Step N: ...`)
7. `## Nutritional Information (per serving)` — All required nutrients
8. `## Dietary Information` — Vegetarian, Vegan, Gluten-Free, Dairy-Free, Nut-Free
9. `## Variations` — At least 2–3 variations or substitutions
10. `## Storage and Reheating` — Refrigeration, freezing, and reheating
11. `## Tips and Notes` — Practical tips
12. `## Serving Suggestions` — How to serve and pair

### File Naming

- Use kebab-case: `chicken-tikka-masala.md`, `overnight-oats.md`
- Keep names concise and descriptive
- No dates or version numbers in filenames

### Nutritional Values

All nutritional sections must include (per serving):
- Calories (kcal)
- Protein (g)
- Carbohydrates (g)
- Fat (g)
- Fiber (g)
- Sodium (mg)
- Sugar (g)

### Tags

Use consistent tag vocabulary. Common tags:

| Category   | Tags |
|------------|------|
| Meal type  | `breakfast`, `lunch`, `dinner`, `snack`, `dessert` |
| Dietary    | `vegetarian`, `vegan`, `gluten-free`, `dairy-free`, `nut-free`, `low-sodium`, `high-protein` |
| Prep style | `meal-prep-friendly`, `freezer-friendly`, `one-pot`, `sheet-pan`, `no-cook` |
| Time       | `30-minutes-or-less`, `under-1-hour` |
| Audience   | `kid-friendly`, `family-friendly` |
| Difficulty | `easy`, `intermediate`, `advanced` |

## Profile File Standards

Profile files in `profiles/` should follow the structure in `profiles/ashuah.md`.

### Required Sections

- `## Basic Information` — Name, creation/update dates
- `## Dietary Constraints` — Hard restrictions (allergies, medical requirements)
- `## Dietary Preferences` — Preferred cuisines, excluded ingredients, serving size
- `## Nutritional Goals` — Daily macro targets
- `## Preferences` — Meal type preferences, cooking constraints, flavor preferences
- `## Allergen Information` — Allergies, intolerances, cross-contamination concerns

## Constraint File Standards

Constraint files in `constraints/` are YAML. Follow the schema documented in [docs/CONSTRAINT_SCHEMAS.md](docs/CONSTRAINT_SCHEMAS.md).

- Use 2-space indentation
- Add comments (`#`) to explain non-obvious constraint values
- Group related constraints under logical keys

## Agent Prompt Standards

Agent definition files in `.github/agents/` are markdown files that instruct Copilot agents.

### Structure

Each agent file should include:
1. A brief description of the agent's role
2. **Your Task** section — what the agent produces
3. **Instructions** section — numbered steps the agent must follow
4. **Output Requirements** section — format, quality, and commit requirements

### Writing Style

- Use imperative language ("Read the profile", "Generate a markdown file")
- Be explicit about file paths and naming conventions
- Provide example output structures using fenced code blocks
- State non-negotiable requirements clearly (e.g., allergen compliance)

## Questions or Suggestions?

This is a living document. If you have suggestions for improvements, please open an issue or PR.
