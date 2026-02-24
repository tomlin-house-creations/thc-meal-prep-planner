# THC Meal Prep Planner

A markdown-first meal planning system powered by GitHub Copilot custom agents. All data lives in markdown and YAML files; custom agents handle all computation by reading and writing those files directly.

## Overview

THC Meal Prep Planner helps users plan their meals efficiently by:

- 📅 Generating weekly meal plans tailored to user profiles and dietary constraints
- 📖 Maintaining a recipe library in plain markdown
- 🛒 Producing consolidated, department-organized grocery lists
- 📊 Tracking nutritional information against personal goals
- 🤖 Using Copilot custom agents for all "computation" — no servers or scripts needed

## How It Works

The workflow is simple:

1. **Open an issue** describing what you need (e.g., "Generate a meal plan for ashuah for next week")
2. **Assign the appropriate agent** (see [Agents](#agents) below)
3. **Review the PR** the agent creates with the generated markdown files
4. **Merge** — GitHub Pages auto-deploys the updated content

No local setup, no dependencies, no Python, no Node.js.

## Agents

Custom agents live in `.github/agents/`. Each agent reads and writes markdown files directly in the repository.

### 🍽️ Meal Planner (`meal-planner`)

Generates a complete weekly meal plan.

**To use**: Open an issue with a title like:
> "Generate meal plan for ashuah — week of 2026-03-03"

The agent will:
- Read the specified profile from `profiles/`
- Read all recipes from `recipes/`
- Apply constraints from `constraints/sample_constraints.yaml`
- Check `history/` to avoid repetition
- Create `plans/meal_plan_YYYY-MM-DD.md` with a full weekly breakdown, nutritional summary, and grocery list
- Copy to `history/` for future variety tracking

### 🧑‍🍳 Recipe Creator (`recipe-creator`)

Creates a new recipe file in `recipes/`.

**To use**: Open an issue with a title like:
> "Add recipe: Chicken Tikka Masala"

The agent will:
- Follow the template format from `recipes/breakfast-burritos.md`
- Include all required sections (ingredients, instructions, nutritional info, dietary info, etc.)
- Calculate nutritional estimates per serving
- Save the file as `recipes/chicken-tikka-masala.md`

### 🛒 Grocery List (`grocery-list`)

Generates a consolidated, organized shopping list from a meal plan.

**To use**: Open an issue with a title like:
> "Generate grocery list for plans/meal_plan_2026-03-03.md"

The agent will:
- Read the specified meal plan
- Cross-reference full recipes for complete ingredient lists
- Consolidate and sum duplicate ingredients
- Organize by grocery store department (Produce, Proteins, Dairy, Pantry, etc.)
- Save as `plans/grocery_list_YYYY-MM-DD.md`

### 📊 Nutrition Calculator (`nutrition-calculator`)

Analyzes recipes or meal plans for nutritional content.

**To use**: Open an issue with a title like:
> "Calculate nutrition for recipes/veggie-stir-fry.md"
> "Add nutritional summary to plans/meal_plan_2026-03-03.md for ashuah"

The agent will:
- Calculate per-serving nutritional values (calories, protein, carbs, fat, fiber, sodium)
- Compare against user profile goals from `profiles/`
- Update the recipe's Nutritional Information section, or add a summary to the meal plan

## Project Structure

```
thc-meal-prep-planner/
├── .github/
│   ├── agents/                  # Custom agent definitions
│   │   ├── meal-planner.md
│   │   ├── recipe-creator.md
│   │   ├── grocery-list.md
│   │   └── nutrition-calculator.md
│   ├── ISSUE_TEMPLATE/          # GitHub issue templates
│   └── workflows/
│       └── deploy-pages.yml     # Jekyll-based GitHub Pages deployment
├── recipes/                     # Recipe library (Markdown)
├── profiles/                    # User profiles and dietary preferences (Markdown)
├── constraints/                 # Planning constraints (YAML)
├── calendars/                   # Meal calendars
├── history/                     # Historical meal plans for variety tracking
├── plans/                       # Generated meal plans and grocery lists (Markdown)
├── docs/                        # Project documentation
├── scripts/                     # Reserved for future lightweight utility scripts
└── README.md
```

## Technology Stack

- **Data**: Markdown files + YAML constraints
- **Agents**: GitHub Copilot Custom Agents (`.github/agents/`)
- **Deployment**: GitHub Pages with Jekyll (no build step required)
- **Workflow**: GitHub Issues → Agent PR → Review → Merge → Auto-deploy

## Contributing

Contributions are welcome! The primary ways to contribute are:

- **Add recipes**: Create a new issue and use the `recipe-creator` agent, or submit a PR with a new recipe in `recipes/` following the template in `recipes/breakfast-burritos.md`
- **Improve profiles**: Update or add user profiles in `profiles/`
- **Refine constraints**: Improve or add constraint files in `constraints/`
- **Improve agent prompts**: Update the agent definitions in `.github/agents/` to produce better output

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Documentation

- **[Contributing Guide](CONTRIBUTING.md)**: How to contribute to this project
- **[Code Style Guide](CODE_STYLE.md)**: Markdown formatting standards
- **[Constraint Schemas](docs/CONSTRAINT_SCHEMAS.md)**: YAML constraint file format
- **[Project Roadmap](docs/ROADMAP.md)**: Development milestones and plans

## Roadmap

- [x] Phase 1: Markdown-first architecture with custom agents
- [ ] Phase 2: Expand recipe library
- [ ] Phase 3: Add more user profiles
- [ ] Phase 4: Refine agent prompts based on real-world usage
- [ ] Phase 5: Jekyll theme and navigation improvements for GitHub Pages

## License

This project license will be determined.

## Contact

For questions or suggestions, please open an issue on GitHub.
