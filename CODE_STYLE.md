# Code Style Guide

This document defines the coding standards and style guidelines for the THC Meal Prep Planner project.

## Table of Contents

- [General Principles](#general-principles)
- [Python Style Guide](#python-style-guide)
- [TypeScript/JavaScript Style Guide](#typescriptjavascript-style-guide)
- [File Organization](#file-organization)
- [Naming Conventions](#naming-conventions)

## General Principles

1. **Readability First**: Code is read more often than it's written
2. **Consistency**: Follow existing patterns in the codebase
3. **Simplicity**: Prefer simple, clear solutions over clever ones
4. **Maintainability**: Write code that's easy to understand and modify
5. **Documentation**: All code must be explainable and well-documented

## Python Style Guide

### Base Standard

Follow [PEP 8](https://pep8.org/) - the official Python style guide.

### Key Requirements

#### Formatting

- **Indentation**: 4 spaces (no tabs)
- **Line Length**: Maximum 88 characters (Black formatter default; note: PEP 8 recommends 79, but we use Black's 88 for better readability)
- **Blank Lines**: 
  - 2 blank lines between top-level functions and classes
  - 1 blank line between methods in a class
- **Imports**: Group in order - standard library, third-party, local
  ```python
  import os
  import sys
  
  import numpy as np
  import pandas as pd
  
  from meal_planner import recipe
  ```

#### Naming Conventions

- **Modules**: `lowercase_with_underscores.py`
- **Classes**: `PascalCase`
- **Functions/Methods**: `lowercase_with_underscores()`
- **Variables**: `lowercase_with_underscores`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Private**: Prefix with single underscore `_private_method()`

#### Type Hints

Always use type hints for function signatures:

```python
def calculate_calories(ingredients: list[dict], servings: int) -> float:
    """Calculate total calories for a recipe.
    
    Args:
        ingredients: List of ingredient dictionaries with 'name' and 'calories'
        servings: Number of servings
        
    Returns:
        Total calories as a float
    """
    total = sum(item['calories'] for item in ingredients)
    return total / servings
```

#### String Formatting

Prefer f-strings for string formatting:

```python
# Good
message = f"Recipe '{recipe_name}' serves {servings} people"

# Avoid
message = "Recipe '{}' serves {} people".format(recipe_name, servings)
message = "Recipe '%s' serves %d people" % (recipe_name, servings)
```

#### Error Handling

Be specific with exception handling:

```python
# Good
try:
    recipe = get_recipe(recipe_id)
except RecipeNotFoundError as e:
    logger.error(f"Recipe {recipe_id} not found: {e}")
    raise

# Avoid
try:
    recipe = get_recipe(recipe_id)
except Exception:
    pass
```

#### Documentation

See [Documentation Standards](docs/DOCUMENTATION_STANDARDS.md) for detailed docstring requirements.

### Recommended Tools

- **Formatter**: [Black](https://black.readthedocs.io/)
- **Linter**: [Ruff](https://docs.astral.sh/ruff/) or [Pylint](https://pylint.org/)
- **Type Checker**: [mypy](http://mypy-lang.org/)

## TypeScript/JavaScript Style Guide

### Base Standard

Follow the [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) with project-specific modifications.

### Key Requirements

#### Formatting

- **Indentation**: 2 spaces (no tabs)
- **Line Length**: Maximum 100 characters
- **Semicolons**: Always use semicolons
- **Quotes**: Prefer single quotes for strings, double quotes for JSX
  ```typescript
  const message = 'Hello world';
  const jsx = <div className="container">Content</div>;
  ```

#### Naming Conventions

- **Files**: 
  - Components: `PascalCase.tsx`
  - Utilities/Services: `camelCase.ts`
  - Types/Interfaces: `PascalCase.types.ts`
- **Classes**: `PascalCase`
- **Interfaces**: `PascalCase` (no "I" prefix)
- **Types**: `PascalCase`
- **Functions**: `camelCase`
- **Variables**: `camelCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: Prefix with `#` (private fields) or `_` (by convention)

#### Type Annotations

Always use TypeScript types, avoid `any`:

```typescript
// Good
interface Recipe {
  id: string;
  name: string;
  ingredients: Ingredient[];
  servings: number;
}

function calculateCalories(recipe: Recipe): number {
  return recipe.ingredients.reduce((sum, ing) => sum + ing.calories, 0);
}

// Avoid
function calculateCalories(recipe: any): any {
  return recipe.ingredients.reduce((sum, ing) => sum + ing.calories, 0);
}
```

#### Interfaces vs Types

- Prefer `interface` for object shapes
- Use `type` for unions, intersections, and primitives

```typescript
// Interfaces for objects
interface MealPlan {
  id: string;
  meals: Meal[];
}

// Types for unions and primitives
type MealType = 'breakfast' | 'lunch' | 'dinner' | 'snack';
type RecipeId = string;
```

#### Arrow Functions

Prefer arrow functions for callbacks and short functions:

```typescript
// Good
const filterVegetarian = recipes.filter(recipe => recipe.isVegetarian);

// For longer functions with multiple statements
const processRecipe = (recipe: Recipe): ProcessedRecipe => {
  const scaled = scaleIngredients(recipe);
  const validated = validateNutrition(scaled);
  return validated;
};
```

#### Async/Await

Prefer async/await over raw promises:

```typescript
// Good
async function fetchRecipe(id: string): Promise<Recipe> {
  try {
    const response = await fetch(`/api/recipes/${id}`);
    return await response.json();
  } catch (error) {
    logger.error('Failed to fetch recipe', error);
    throw error;
  }
}

// Avoid nested promises
function fetchRecipe(id: string): Promise<Recipe> {
  return fetch(`/api/recipes/${id}`)
    .then(response => response.json())
    .then(data => processData(data))
    .catch(error => handleError(error));
}
```

#### Documentation

Use JSDoc for all public functions, classes, and interfaces:

```typescript
/**
 * Calculates the nutritional information for a meal plan.
 * 
 * @param plan - The meal plan to analyze
 * @param options - Optional configuration for calculation
 * @returns Nutritional breakdown by category
 * @throws {ValidationError} If the meal plan is invalid
 */
function calculateNutrition(
  plan: MealPlan,
  options?: NutritionOptions
): NutritionInfo {
  // Implementation
}
```

See [Documentation Standards](docs/DOCUMENTATION_STANDARDS.md) for detailed requirements.

### React/TSX Specific

#### Component Structure

```typescript
interface RecipeCardProps {
  recipe: Recipe;
  onSelect?: (recipe: Recipe) => void;
}

/**
 * Displays a recipe card with basic information.
 */
export function RecipeCard({ recipe, onSelect }: RecipeCardProps) {
  const handleClick = () => {
    onSelect?.(recipe);
  };

  return (
    <div className="recipe-card" onClick={handleClick}>
      <h3>{recipe.name}</h3>
      <p>{recipe.description}</p>
    </div>
  );
}
```

#### Hooks

- Use `use` prefix for custom hooks
- Keep hooks at the top of the component
- Extract complex logic into custom hooks

```typescript
function useMealPlan(planId: string) {
  const [plan, setPlan] = useState<MealPlan | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMealPlan(planId).then(setPlan).finally(() => setLoading(false));
  }, [planId]);

  return { plan, loading };
}
```

### Recommended Tools

- **Formatter**: [Prettier](https://prettier.io/)
- **Linter**: [ESLint](https://eslint.org/)
- **Type Checker**: TypeScript compiler (`tsc`)

## File Organization

### Directory Structure

```
project/
├── src/              # Source code
│   ├── components/   # React components
│   ├── services/     # Business logic and API calls
│   ├── utils/        # Utility functions
│   ├── types/        # TypeScript type definitions
│   └── styles/       # CSS/SCSS files
├── tests/            # Test files (mirror src structure)
├── docs/             # Documentation
└── scripts/          # Build and utility scripts
```

### Module Organization

- One class/component per file
- Group related functionality
- Keep files focused and concise (< 300 lines when possible)

## Naming Conventions

### Be Descriptive

```python
# Good
def calculate_total_calories(recipes: list[Recipe]) -> float:
    pass

# Avoid
def calc(r: list) -> float:
    pass
```

### Use Domain Language

Use terminology from the meal prep/planning domain:

```typescript
// Good
interface Recipe {
  servings: number;
  prepTime: number;
  cookTime: number;
}

// Avoid generic terms
interface Item {
  count: number;
  time1: number;
  time2: number;
}
```

### Boolean Variables

Prefix with `is`, `has`, `should`, `can`:

```python
is_vegetarian = True
has_allergens = False
should_scale_recipe = True
can_prepare = check_ingredients()
```

## Comments

### When to Comment

- **DO**: Explain **why** something is done
- **DON'T**: Explain **what** the code does (code should be self-explanatory)

```python
# Good - explains why
# Use exponential backoff to avoid overwhelming the API
retry_delay = base_delay * (2 ** attempt)

# Bad - just repeats what code says
# Multiply base_delay by 2 to the power of attempt
retry_delay = base_delay * (2 ** attempt)
```

### Complex Logic

Add comments for complex algorithms or business rules:

```typescript
// Complex nutrition calculation based on FDA guidelines
// See: https://www.fda.gov/food/nutrition-facts-label/daily-value
function calculateDailyValue(nutrient: number, type: NutrientType): number {
  // Implementation
}
```

## Code Review Focus Areas

When reviewing code, pay attention to:

1. Adherence to this style guide
2. Code readability and maintainability
3. Appropriate documentation
4. Consistent naming conventions
5. Proper error handling
6. Type safety (TypeScript) or type hints (Python)

## Questions or Suggestions?

This is a living document. If you have suggestions for improvements, please open an issue or PR.
