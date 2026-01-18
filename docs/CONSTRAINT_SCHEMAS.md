# Constraint YAML Schemas

This document describes the schema and structure for constraint YAML files used in the THC Meal Prep Planner.

## Overview

Constraints define the rules and requirements for meal plan generation. They control:
- Time limits for meal preparation
- Variety requirements and repetition prevention
- No-cook nights and special scheduling
- Meal blocking rules (protein types, cuisines, etc.)
- History integration for long-term variety
- Scoring and quality metrics

## Schema Version

Current version: **1.0**

## Complete Schema

### Week Configuration

Defines the date range for the meal plan.

```yaml
week:
  start_date: "YYYY-MM-DD"  # Week start date (required)
  end_date: "YYYY-MM-DD"    # Week end date (required)
```

**Example:**
```yaml
week:
  start_date: "2026-01-20"
  end_date: "2026-01-26"
```

**Validation:**
- Both dates are required
- Dates must be in ISO format (YYYY-MM-DD)
- `start_date` must not be after `end_date`

---

### Meal Requirements

Specifies how many of each meal type are needed per day.

```yaml
meals_per_day:
  breakfast: <integer>  # Number of breakfasts per day (0+)
  lunch: <integer>      # Number of lunches per day (0+)
  dinner: <integer>     # Number of dinners per day (0+)
  snack: <integer>      # Number of snacks per day (0+)
```

**Example:**
```yaml
meals_per_day:
  breakfast: 1
  lunch: 1
  dinner: 1
  snack: 0
```

**Validation:**
- All values must be non-negative integers
- Setting a value to 0 skips that meal type

---

### Budget Constraints

Optional budget tracking for meal plans.

```yaml
budget:
  max_per_week: <float>      # Maximum weekly budget (optional)
  currency: "<string>"       # Currency code (optional, default: "USD")
  track_spending: <boolean>  # Enable budget tracking (optional)
```

**Example:**
```yaml
budget:
  max_per_week: 150.00
  currency: "USD"
  track_spending: true
```

**Note:** Budget constraints are informational only in the current version.

---

### Time Constraints

Controls maximum preparation time based on day type.

```yaml
time:
  # Maximum prep time on weeknights (Monday-Friday)
  max_weeknight_prep_minutes: <integer>  # Required
  
  # Maximum prep time on weekends (Saturday-Sunday)
  max_weekend_prep_minutes: <integer>    # Required
  
  # No-cook nights configuration (optional)
  no_cook_nights:
    enabled: <boolean>          # Enable no-cook nights
    days: [<string>, ...]       # List of day names
    max_prep_minutes: <integer> # Max prep time for no-cook nights
```

**Example:**
```yaml
time:
  max_weeknight_prep_minutes: 45
  max_weekend_prep_minutes: 180
  no_cook_nights:
    enabled: true
    days:
      - "Wednesday"
    max_prep_minutes: 10
```

**Validation:**
- Time values must be positive integers
- Day names must be full day names (e.g., "Monday", not "Mon")
- Valid day names: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday

---

### Variety Requirements

Controls recipe and cuisine variety across the meal plan.

```yaml
variety:
  # Minimum days before repeating a recipe
  min_days_between_repeats: <integer>     # Default: 3
  
  # Prefer different cuisines throughout the week
  prefer_cuisine_variety: <boolean>       # Default: true
  
  # Minimum unique cuisines per week (optional)
  min_unique_cuisines: <integer>          # Optional
  
  # Avoid consecutive days with same main ingredient (optional)
  avoid_consecutive_ingredients: <boolean> # Optional
```

**Example:**
```yaml
variety:
  min_days_between_repeats: 7
  prefer_cuisine_variety: true
  min_unique_cuisines: 3
  avoid_consecutive_ingredients: true
```

**Validation:**
- `min_days_between_repeats` must be a positive integer
- When combined with history, applies across historical plans too

---

### Meal Blocking Constraints

Prevents repetitive patterns in meal plans.

```yaml
blocking:
  # Protein blocking (optional)
  protein_blocking:
    enabled: <boolean>              # Enable protein blocking
    max_consecutive_days: <integer> # Max consecutive days with same protein
    protein_types: [<string>, ...]  # List of protein types to track
  
  # Cuisine blocking (optional)
  cuisine_blocking:
    enabled: <boolean>              # Enable cuisine blocking
    max_consecutive_days: <integer> # Max consecutive days with same cuisine
  
  # Cooking method blocking (optional)
  cooking_method_blocking:
    enabled: <boolean>              # Enable method blocking
    max_consecutive_days: <integer> # Max consecutive days with same method
    methods: [<string>, ...]        # List of cooking methods to track
```

**Example:**
```yaml
blocking:
  protein_blocking:
    enabled: true
    max_consecutive_days: 1
    protein_types:
      - "Chicken"
      - "Beef"
      - "Fish"
      - "Tofu"
  
  cuisine_blocking:
    enabled: true
    max_consecutive_days: 2
```

**Note:** Blocking constraints require recipes to have corresponding tags:
- Protein: `**Protein**: Chicken` in recipe metadata
- Cuisine: `**Cuisine**: Italian` in recipe metadata
- Cooking Method: `**Method**: Grilled` in recipe metadata

---

### History Integration

Enables tracking and using historical meal plans for variety.

```yaml
history:
  enabled: <boolean>        # Enable history integration (default: false)
  ttl_days: <integer>       # Days to keep history (default: 30)
  directory: "<string>"     # History directory path (default: "history")
  auto_save: <boolean>      # Auto-save plans to history (default: false)
```

**Example:**
```yaml
history:
  enabled: true
  ttl_days: 30
  directory: "history"
  auto_save: true
```

**Validation:**
- `ttl_days` must be a positive integer
- Directory path is relative to project root
- History files are stored as JSON

---

### Nutritional Balance

Optional nutritional targets (informational only).

```yaml
nutrition:
  balance_macros: <boolean>     # Try to balance macros (optional)
  target_calories_per_day: <integer>  # Target daily calories (optional)
  
  # Target macro ratios (optional)
  target_macros:
    protein: <integer>  # Percentage of calories from protein
    carbs: <integer>    # Percentage of calories from carbs
    fat: <integer>      # Percentage of calories from fat
```

**Example:**
```yaml
nutrition:
  balance_macros: true
  target_calories_per_day: 2000
  target_macros:
    protein: 30
    carbs: 40
    fat: 30
```

**Note:** Nutritional constraints are informational in the current version.

---

### Scoring and Penalties

Controls variety scoring and quality metrics.

```yaml
scoring:
  enabled: <boolean>                # Enable scoring (default: false)
  min_acceptable_score: <integer>   # Minimum acceptable score (optional)
  show_detailed_breakdown: <boolean> # Show detailed score breakdown (default: false)
```

**Example:**
```yaml
scoring:
  enabled: true
  min_acceptable_score: 50
  show_detailed_breakdown: true
```

**Scoring Components:**

1. **Cuisine Variety Score**
   - +10 points per unique cuisine
   - -5 points per consecutive day with same cuisine

2. **Recipe Diversity Score**
   - +15 points per unique recipe
   - +20 bonus if no recipes are repeated

3. **Repetition Penalties**
   - -10 points per recipe repeated within `min_days_between_repeats`

4. **Constraint Violation Penalties**
   - -50 points per missing required meal
   - -20 points per general constraint violation

**Grade Scale:**
- A+ : 200+ points
- A  : 150-199 points
- B  : 100-149 points
- C  : 50-99 points
- D  : 0-49 points
- F  : Below 0 points

---

## Complete Example

Here's a complete constraint file with all sections:

```yaml
# Enhanced Meal Plan Constraints

week:
  start_date: "2026-01-20"
  end_date: "2026-01-26"

meals_per_day:
  breakfast: 1
  lunch: 1
  dinner: 1
  snack: 0

budget:
  max_per_week: 150.00
  currency: "USD"
  track_spending: true

time:
  max_weeknight_prep_minutes: 45
  max_weekend_prep_minutes: 180
  no_cook_nights:
    enabled: true
    days:
      - "Wednesday"
    max_prep_minutes: 10

variety:
  min_days_between_repeats: 7
  prefer_cuisine_variety: true
  min_unique_cuisines: 3
  avoid_consecutive_ingredients: true

blocking:
  protein_blocking:
    enabled: true
    max_consecutive_days: 1
    protein_types:
      - "Chicken"
      - "Beef"
      - "Fish"
      - "Tofu"
  
  cuisine_blocking:
    enabled: true
    max_consecutive_days: 2

history:
  enabled: true
  ttl_days: 30
  directory: "history"
  auto_save: true

nutrition:
  balance_macros: true
  target_calories_per_day: 2000
  target_macros:
    protein: 30
    carbs: 40
    fat: 30

scoring:
  enabled: true
  min_acceptable_score: 50
  show_detailed_breakdown: true
```

---

## Using Constraints

### Loading Constraints in Python

```python
import yaml
from pathlib import Path

# Load constraints
constraints_path = Path("constraints/sample_constraints.yaml")
with open(constraints_path, "r") as f:
    constraints = yaml.safe_load(f)

# Access constraint values
max_time = constraints["time"]["max_weeknight_prep_minutes"]
min_variety = constraints["variety"]["min_days_between_repeats"]
```

### Validating Constraints

The meal plan generator validates constraints at runtime:
- Missing required fields raise `KeyError`
- Invalid data types raise `ValueError`
- Invalid date ranges are caught and reported

---

## Best Practices

1. **Start Simple**: Begin with basic constraints (time, variety) and add complexity as needed
2. **Test Incrementally**: Add one constraint type at a time and verify it works
3. **Use History**: Enable history tracking for better long-term variety
4. **Monitor Scores**: Use scoring to identify when you need more recipe variety
5. **Document Custom Constraints**: If you add new constraint types, document them

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-18 | Initial schema documentation |

---

## See Also

- [Sample Constraints](../constraints/sample_constraints.yaml) - Basic constraint example
- [Enhanced Constraints](../constraints/enhanced_constraints.yaml) - Advanced constraint example
- [Product Requirements Document](PRD.md) - Overall product requirements
