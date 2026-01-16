# Documentation Standards

This document defines the documentation requirements for the THC Meal Prep Planner project. All code must be explainable and maintainable through proper documentation.

## Table of Contents

- [Philosophy](#philosophy)
- [Python Documentation](#python-documentation)
- [TypeScript/JavaScript Documentation](#typescriptjavascript-documentation)
- [README Requirements](#readme-requirements)
- [API Documentation](#api-documentation)
- [Comments vs Documentation](#comments-vs-documentation)

## Philosophy

Good documentation serves multiple purposes:

1. **Explains Intent**: Why does this code exist?
2. **Describes Behavior**: What does this code do?
3. **Guides Usage**: How should this code be used?
4. **Aids Maintenance**: Helps future developers (including yourself) understand the code

### Core Principles

- **Self-Documenting Code**: Write clear code that minimizes the need for comments
- **Document the Why**: Code shows what and how; documentation explains why
- **Keep It Current**: Update documentation when code changes
- **Be Concise**: Clear and brief is better than long and vague

## Python Documentation

### Docstring Standard

Follow [PEP 257](https://www.python.org/dev/peps/pep-0257/) and [Google Style Python Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

### Module Docstrings

Every Python module should have a docstring at the top:

```python
"""Recipe management module.

This module provides functionality for creating, updating, and managing
recipes in the meal prep planner. It includes validation, storage, and
retrieval operations.

Typical usage example:

    recipe = Recipe(name="Pasta", servings=4)
    recipe.add_ingredient("pasta", 200, "grams")
    recipe.save()
"""
```

### Class Docstrings

Document all classes with their purpose and attributes:

```python
class Recipe:
    """Represents a recipe with ingredients and instructions.
    
    A Recipe contains all information needed to prepare a meal, including
    ingredients, quantities, preparation steps, and nutritional information.
    
    Attributes:
        name: The display name of the recipe.
        servings: Number of servings this recipe produces.
        ingredients: List of Ingredient objects.
        instructions: List of preparation steps as strings.
        prep_time: Preparation time in minutes.
        cook_time: Cooking time in minutes.
        
    Example:
        >>> recipe = Recipe(name="Spaghetti", servings=4)
        >>> recipe.add_ingredient("pasta", 400, "grams")
        >>> recipe.add_instruction("Boil pasta for 10 minutes")
    """
    
    def __init__(self, name: str, servings: int = 1):
        """Initialize a new Recipe.
        
        Args:
            name: The name of the recipe.
            servings: Number of servings (default: 1).
            
        Raises:
            ValueError: If servings is less than 1.
        """
        if servings < 1:
            raise ValueError("Servings must be at least 1")
        self.name = name
        self.servings = servings
        self.ingredients = []
        self.instructions = []
```

### Function/Method Docstrings

Document all public functions and methods:

```python
def calculate_nutrition(recipe: Recipe, servings: int = None) -> NutritionInfo:
    """Calculate nutritional information for a recipe.
    
    Analyzes all ingredients in the recipe and computes total nutritional
    values including calories, protein, carbs, and fats. Optionally scales
    the values based on the number of servings.
    
    Args:
        recipe: The Recipe object to analyze.
        servings: Number of servings to scale to. If None, uses recipe's
            default servings.
            
    Returns:
        A NutritionInfo object containing:
            - calories: Total calories as a float
            - protein: Protein in grams as a float
            - carbs: Carbohydrates in grams as a float
            - fats: Fats in grams as a float
            
    Raises:
        ValueError: If recipe has no ingredients.
        InvalidIngredientError: If any ingredient lacks nutrition data.
        
    Example:
        >>> recipe = Recipe(name="Salad", servings=2)
        >>> recipe.add_ingredient("lettuce", 100, "grams")
        >>> nutrition = calculate_nutrition(recipe)
        >>> print(f"Calories: {nutrition.calories}")
        Calories: 15.0
    """
    if not recipe.ingredients:
        raise ValueError("Recipe must have at least one ingredient")
    
    # Implementation here
    pass
```

### Private Functions

Private functions (prefixed with `_`) should have simpler docstrings:

```python
def _validate_ingredient(ingredient: dict) -> bool:
    """Validate that an ingredient dictionary has required fields.
    
    Args:
        ingredient: Dictionary with 'name', 'quantity', and 'unit' keys.
        
    Returns:
        True if valid, False otherwise.
    """
    required_keys = {'name', 'quantity', 'unit'}
    return all(key in ingredient for key in required_keys)
```

### When to Skip Docstrings

You may skip docstrings for:

- Very simple property getters/setters that are self-explanatory
- Dunder methods that follow Python conventions (`__str__`, `__repr__`, etc.)
- Test functions (use descriptive test names instead)

```python
@property
def total_time(self) -> int:
    """Total time in minutes (prep + cook)."""
    return self.prep_time + self.cook_time

# This is clear enough without a docstring:
@property
def name(self) -> str:
    return self._name
```

## TypeScript/JavaScript Documentation

### JSDoc Standard

Use [JSDoc](https://jsdoc.app/) for all public APIs, interfaces, types, classes, and functions.

### Interface/Type Documentation

Document all exported interfaces and types:

```typescript
/**
 * Represents a recipe with ingredients and preparation steps.
 * 
 * @interface Recipe
 * @property {string} id - Unique identifier for the recipe
 * @property {string} name - Display name of the recipe
 * @property {number} servings - Number of servings produced
 * @property {Ingredient[]} ingredients - List of required ingredients
 * @property {string[]} instructions - Step-by-step preparation instructions
 * @property {number} prepTime - Preparation time in minutes
 * @property {number} cookTime - Cooking time in minutes
 */
interface Recipe {
  id: string;
  name: string;
  servings: number;
  ingredients: Ingredient[];
  instructions: string[];
  prepTime: number;
  cookTime: number;
}

/**
 * Meal type classification.
 * 
 * @typedef {'breakfast' | 'lunch' | 'dinner' | 'snack'} MealType
 */
type MealType = 'breakfast' | 'lunch' | 'dinner' | 'snack';
```

### Class Documentation

Document classes and their methods:

```typescript
/**
 * Service for managing recipes in the meal prep planner.
 * 
 * Handles CRUD operations for recipes, including validation,
 * storage, and retrieval from the backend API.
 * 
 * @class RecipeService
 * 
 * @example
 * const service = new RecipeService();
 * const recipe = await service.getRecipe('recipe-123');
 */
class RecipeService {
  /**
   * Creates a new RecipeService instance.
   * 
   * @param {string} apiBaseUrl - Base URL for the recipe API
   */
  constructor(private apiBaseUrl: string) {}

  /**
   * Retrieves a recipe by its ID.
   * 
   * @param {string} id - The unique identifier of the recipe
   * @returns {Promise<Recipe>} The requested recipe
   * @throws {RecipeNotFoundError} If the recipe doesn't exist
   * @throws {NetworkError} If the API request fails
   * 
   * @example
   * const recipe = await service.getRecipe('recipe-123');
   * console.log(recipe.name);
   */
  async getRecipe(id: string): Promise<Recipe> {
    // Implementation
  }
}
```

### Function Documentation

Document all exported functions:

```typescript
/**
 * Calculates the total nutritional information for a meal plan.
 * 
 * Aggregates nutrition data from all meals in the plan and returns
 * totals for each nutritional category.
 * 
 * @param {MealPlan} plan - The meal plan to analyze
 * @param {NutritionOptions} [options] - Optional calculation settings
 * @param {boolean} [options.includeSnacks=true] - Whether to include snacks
 * @param {boolean} [options.perServing=false] - Calculate per serving
 * @returns {NutritionInfo} Aggregated nutritional information
 * 
 * @throws {ValidationError} If the meal plan is invalid
 * 
 * @example
 * const nutrition = calculatePlanNutrition(myPlan);
 * console.log(`Total calories: ${nutrition.calories}`);
 * 
 * @example
 * // Calculate per serving
 * const perServing = calculatePlanNutrition(myPlan, { perServing: true });
 */
function calculatePlanNutrition(
  plan: MealPlan,
  options?: NutritionOptions
): NutritionInfo {
  // Implementation
}
```

### React Component Documentation

Document React components with props and usage examples:

```typescript
/**
 * Props for the RecipeCard component.
 */
interface RecipeCardProps {
  /** The recipe to display */
  recipe: Recipe;
  /** Callback when the recipe is selected */
  onSelect?: (recipe: Recipe) => void;
  /** Whether the card is currently selected */
  isSelected?: boolean;
  /** Additional CSS class names */
  className?: string;
}

/**
 * Displays a recipe card with summary information.
 * 
 * Shows the recipe name, image, prep time, and servings.
 * Clicking the card triggers the onSelect callback if provided.
 * 
 * @component
 * 
 * @example
 * <RecipeCard
 *   recipe={myRecipe}
 *   onSelect={handleRecipeSelect}
 *   isSelected={selectedId === myRecipe.id}
 * />
 */
export function RecipeCard({
  recipe,
  onSelect,
  isSelected = false,
  className,
}: RecipeCardProps) {
  // Implementation
}
```

### Hook Documentation

Document custom React hooks:

```typescript
/**
 * Custom hook for managing meal plan state.
 * 
 * Provides state and operations for loading, updating, and saving
 * a meal plan. Handles loading states and error handling.
 * 
 * @param {string} planId - The ID of the meal plan to manage
 * @returns {UseMealPlanResult} Meal plan state and operations
 * 
 * @example
 * function MealPlanView({ planId }: { planId: string }) {
 *   const { plan, loading, error, updatePlan } = useMealPlan(planId);
 *   
 *   if (loading) return <Spinner />;
 *   if (error) return <Error message={error.message} />;
 *   
 *   return <MealPlanEditor plan={plan} onUpdate={updatePlan} />;
 * }
 */
function useMealPlan(planId: string): UseMealPlanResult {
  // Implementation
}
```

### When to Skip JSDoc

You may skip JSDoc for:

- Private functions/methods (use inline comments if needed)
- Very simple utility functions where the signature is self-explanatory
- Internal implementation details

```typescript
// Clear from the signature and name, JSDoc would be redundant
function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

// Private helper - inline comment is sufficient
function _sortByDate(items: Item[]): Item[] {
  // Sort items by createdAt descending
  return items.sort((a, b) => b.createdAt - a.createdAt);
}
```

## README Requirements

Every module, package, or significant directory should have a README.md:

### Project Root README

```markdown
# Project Name

Brief description of what this project does.

## Features

- Key feature 1
- Key feature 2
- Key feature 3

## Getting Started

### Prerequisites

- Required software/tools
- Version requirements

### Installation

Step-by-step installation instructions

### Usage

Basic usage examples

## Documentation

Links to additional documentation

## Contributing

Link to CONTRIBUTING.md

## License

License information
```

### Package/Module README

```markdown
# Package/Module Name

What this package does and why it exists.

## Usage

```python
# or TypeScript
from package import Module

# Usage example
```

## API Reference

Brief overview or link to detailed API docs.
```

## API Documentation

For REST APIs, document:

1. **Endpoint**: HTTP method and path
2. **Description**: What the endpoint does
3. **Parameters**: Query params, path params, body
4. **Response**: Success response format
5. **Errors**: Possible error responses
6. **Example**: Request and response example

```markdown
### GET /api/recipes/:id

Retrieves a recipe by ID.

**Parameters:**
- `id` (path, required): Recipe unique identifier

**Response:** `200 OK`
```json
{
  "id": "recipe-123",
  "name": "Spaghetti Carbonara",
  "servings": 4
}
```

**Errors:**
- `404 Not Found`: Recipe doesn't exist
- `500 Internal Server Error`: Server error

**Example:**
```bash
curl https://api.example.com/api/recipes/recipe-123
```
```

## Comments vs Documentation

### Use Documentation (Docstrings/JSDoc) For:

- Public APIs (functions, classes, methods)
- Module/file-level descriptions
- Complex algorithms requiring explanation
- Usage examples
- Parameter descriptions

### Use Inline Comments For:

- Explaining **why** something is done a certain way
- Clarifying complex logic
- Noting important constraints or gotchas
- Temporary notes (TODO, FIXME, HACK)

### Examples

```python
# GOOD: Comment explains WHY
# We use exponential backoff to avoid overwhelming the external API
# which has rate limits of 100 requests per minute
retry_delay = base_delay * (2 ** attempt)

# BAD: Comment just repeats WHAT the code does
# Calculate retry delay by multiplying base delay by 2 to the power of attempt
retry_delay = base_delay * (2 ** attempt)
```

```typescript
// GOOD: Explains non-obvious business logic
// Nutrition values must be recalculated when servings change
// because some ingredients (like salt) don't scale linearly
useEffect(() => {
  recalculateNutrition();
}, [servings]);

// BAD: States the obvious
// Call recalculateNutrition when servings changes
useEffect(() => {
  recalculateNutrition();
}, [servings]);
```

## Documentation Review Checklist

When reviewing documentation, check:

- [ ] All public APIs have docstrings/JSDoc
- [ ] Parameter types and return types are documented
- [ ] Exceptions/errors are documented
- [ ] Complex logic has explanatory comments
- [ ] Usage examples are provided where helpful
- [ ] Documentation is accurate and up-to-date
- [ ] Comments explain "why" not "what"
- [ ] No redundant or obvious comments

## Keeping Documentation Updated

- Update documentation when changing code behavior
- Remove outdated comments and docs
- Review documentation during code reviews
- Mark uncertain docs with TODO or NOTE

## Tools and Automation

### Python

- Use [pydocstyle](http://www.pydocstyle.org/) to check docstring compliance
- Generate HTML docs with [Sphinx](https://www.sphinx-doc.org/)

### TypeScript

- Use [ESLint with JSDoc rules](https://github.com/gajus/eslint-plugin-jsdoc)
- Generate docs with [TypeDoc](https://typedoc.org/)

## Questions?

If you're unsure whether something needs documentation, ask:

1. Would someone unfamiliar with this code understand its purpose?
2. Would I understand this code in 6 months?
3. Are there any non-obvious decisions or constraints?

If the answer to any is "no" or "maybe," add documentation.
