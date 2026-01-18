#!/usr/bin/env python3
"""Grocery List Generator Module

This module provides functionality to generate organized shopping lists from meal plans.
It parses ingredients from recipes, merges duplicate items, quantifies totals, and
categorizes them for efficient shopping.

Key Features:
- Parse ingredients from recipe markdown files
- Extract and normalize quantities with units
- Merge duplicate ingredients across multiple recipes
- Categorize items by grocery store section (Produce, Meat, Dairy, etc.)
- Generate clean, Alexa-friendly Markdown with checkboxes

Typical usage:
    from grocery_list_generator import generate_grocery_list_from_recipes
    from pathlib import Path

    recipes = ["breakfast-burritos", "fish-tacos"]
    grocery_list = generate_grocery_list_from_recipes(recipes, Path("recipes/"))
    print(grocery_list)

Author: THC Meal Prep Planner Team
Created: 2026-01-18
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from fractions import Fraction

# ==============================================================================
# CATEGORY DEFINITIONS - Grocery store sections for ingredient organization
# ==============================================================================

# Keywords for categorizing ingredients into grocery store sections
# Each category contains common ingredients and keywords found in that section
CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "Produce": [
        "lettuce",
        "spinach",
        "arugula",
        "greens",
        "salad",
        "tomato",
        "cucumber",
        "onion",
        "garlic",
        "bell pepper",
        "carrot",
        "celery",
        "broccoli",
        "cauliflower",
        "cabbage",
        "potato",
        "sweet potato",
        "avocado",
        "lime",
        "lemon",
        "apple",
        "banana",
        "berry",
        "berries",
        "fruit",
        "cilantro",
        "parsley",
        "basil",
        "herb",
        "kale",
        "zucchini",
        "squash",
        "mushroom",
        "pea",
    ],
    "Meat": [
        "chicken",
        "beef",
        "pork",
        "turkey",
        "sausage",
        "bacon",
        "ham",
        "lamb",
        "steak",
        "ground beef",
        "fish",
        "salmon",
        "tuna",
        "tilapia",
        "cod",
        "mahi-mahi",
        "shrimp",
        "seafood",
    ],
    "Dairy": [
        "milk",
        "cream",
        "cheese",
        "cheddar",
        "mozzarella",
        "parmesan",
        "feta",
        "yogurt",
        "butter",
        "egg",
        "sour cream",
        "cottage cheese",
    ],
    "Pantry": [
        "oil",
        "olive oil",
        "vegetable oil",
        "vinegar",
        "flour",
        "sugar",
        "salt",
        "black pepper",
        "white pepper",
        "cayenne pepper",
        "red pepper flakes",
        "spice",
        "seasoning",
        "rice",
        "pasta",
        "quinoa",
        "oats",
        "cereal",
        "can",
        "canned",
        "beans",
        "black beans",
        "chickpeas",
        "stock",
        "broth",
        "sauce",
        "salsa",
        "hot sauce",
        "honey",
        "maple syrup",
        "peanut butter",
        "cumin",
        "paprika",
        "chili powder",
        "garlic powder",
        "mustard",
        "ketchup",
        "mayo",
        "mayonnaise",
        "soy sauce",
        "balsamic",
        "dijon",
    ],
    "Frozen": [
        "frozen",
        "ice cream",
        "frozen vegetables",
        "frozen fruit",
        "popsicle",
    ],
    "Bakery": [
        "bread",
        "tortilla",
        "tortillas",
        "bagel",
        "muffin",
        "roll",
        "bun",
        "pita",
        "naan",
    ],
}


# ==============================================================================
# INGREDIENT PARSING - Extract and normalize ingredient information
# ==============================================================================


def clean_ingredient_name(name: str) -> str:
    """Clean ingredient name by removing parenthetical notes and extra details.

    Removes common recipe notes like "(optional)", "(about X cups)", "(diced)",
    and standardizes ingredient names for better merging.

    Args:
        name: Raw ingredient name from recipe

    Returns:
        Cleaned ingredient name

    Examples:
        >>> clean_ingredient_name("onion, diced (about 1/2 cup)")
        'onion'
        >>> clean_ingredient_name("cilantro, chopped (optional)")
        'cilantro'
    """
    # Remove parenthetical notes
    name = re.sub(r"\([^)]*\)", "", name)

    # Remove common descriptors after commas
    name = re.sub(
        r",\s*(diced|chopped|sliced|minced|halved|thinly sliced|optional|for serving|drained and rinsed).*$",
        "",
        name,
    )

    # Remove "to taste" phrases
    name = re.sub(r"\s+to taste.*$", "", name, flags=re.IGNORECASE)

    # Remove "and X" suffix (e.g., "salt and pepper" -> "salt")
    # This helps merge seasoning combinations
    # Match multi-word phrases after "and" by being greedy
    name = re.sub(r"\s+and\s+.+$", "", name)

    # Handle "juice of X" format - extract just the citrus
    juice_match = re.match(r"juice of \d+\s+(.+)", name, flags=re.IGNORECASE)
    if juice_match:
        # Convert "juice of 1 lime" to "lime juice"
        return juice_match.group(1) + " juice"

    # Remove qualifier words at the beginning (fresh, dried, etc.)
    name = re.sub(
        r"^(fresh|dried|frozen|canned|shredded|chopped|sliced|diced|minced)\s+",
        "",
        name,
        flags=re.IGNORECASE,
    )

    # Clean up extra whitespace
    name = " ".join(name.split())

    return name.strip()


def parse_ingredient_line(line: str) -> Optional[Tuple[str, str, str]]:
    """Parse an ingredient line to extract quantity, unit, and name.

    This function handles various ingredient formats commonly found in recipes:
    - "2 cups flour"
    - "1/2 teaspoon salt"
    - "3-4 tablespoons olive oil"
    - "8 large eggs"
    - "Salt and pepper to taste"

    Args:
        line: A single ingredient line from a recipe (e.g., "2 cups flour")

    Returns:
        A tuple of (quantity, unit, ingredient_name) or None if parsing fails.
        - quantity: String representation of amount (e.g., "2", "1/2", "3-4")
        - unit: Unit of measurement (e.g., "cups", "tsp") or "" if none
        - ingredient_name: Name of ingredient (e.g., "flour", "salt")

    Examples:
        >>> parse_ingredient_line("2 cups flour")
        ('2', 'cups', 'flour')
        >>> parse_ingredient_line("1/2 teaspoon salt")
        ('1/2', 'teaspoon', 'salt')
        >>> parse_ingredient_line("Salt to taste")
        ('1', '', 'salt')
    """
    # Remove leading bullets, dashes, and whitespace
    line = re.sub(r"^[-•*]\s*", "", line.strip())

    # Skip empty lines or section headers
    if not line or line.startswith("#"):
        return None

    # Common measurement units - check if present to distinguish from ingredient names
    common_units = {
        "tbsp",
        "tbs",
        "tb",
        "tsp",
        "ts",
        # Note: 't' is intentionally omitted as it's too ambiguous and could match
        # unrelated words in ingredient names. Users should use 'tsp' or 'ts' instead.
        "cup",
        "cups",
        "c",
        "oz",
        "ounce",
        "ounces",
        "lb",
        "lbs",
        "pound",
        "pounds",
        "g",
        "gram",
        "grams",
        "kg",
        "ml",
        "l",
        "can",
        "cans",
        "jar",
        "jars",
        "package",
        "packages",
        "box",
        "boxes",
        "large",
        "medium",
        "small",
        "whole",
        "tablespoon",
        "tablespoons",
        "teaspoon",
        "teaspoons",
        "clove",
        "cloves",
        "count",
    }

    # Try pattern with explicit unit first
    # Matches: "2 cups flour" or "1/2 tsp salt"
    pattern_with_unit = r"^([\d./\-]+(?:\s+to\s+[\d./\-]+)?)\s+(\S+)\s+(.+)$"
    match = re.match(pattern_with_unit, line)

    if match:
        quantity = match.group(1).strip()
        potential_unit = match.group(2).strip()
        potential_name = match.group(3).strip()

        # Check if the second word is actually a measurement unit
        if potential_unit.lower() in common_units:
            # It's a unit! Clean and return
            name = clean_ingredient_name(potential_name)
            return (quantity, potential_unit, name)
        else:
            # Not a unit - the whole "unit + name" is the ingredient name
            full_name = f"{potential_unit} {potential_name}"
            name = clean_ingredient_name(full_name)
            return (quantity, "", name)

    # If no match, treat as ingredient without quantity
    cleaned_name = clean_ingredient_name(line)
    return ("1", "", cleaned_name)


def normalize_unit(unit: str) -> str:
    """Normalize unit abbreviations to standard forms.

    Converts common abbreviations and variations to standardized units
    for consistent grouping and display.

    Note: In recipes, capital 'T' is often used for tablespoon, lowercase 't' for teaspoon.
    However, we normalize case-insensitively to handle various styles.

    Args:
        unit: Unit string to normalize (e.g., "tbsp", "T", "tablespoon")

    Returns:
        Normalized unit string (e.g., "tablespoon", "cup", "teaspoon")

    Examples:
        >>> normalize_unit("tbsp")
        'tablespoon'
        >>> normalize_unit("c")
        'cup'
        >>> normalize_unit("oz")
        'ounce'
    """
    unit_lower = unit.lower()

    # Tablespoon variations
    # Note: Including just lowercase since we normalize via .lower() above
    if unit_lower in ["tbsp", "tbs", "tb", "tablespoon", "tablespoons"]:
        return "tablespoon"

    # Teaspoon variations
    # Note: 't' is intentionally omitted as it's too ambiguous
    if unit_lower in ["tsp", "ts", "teaspoon", "teaspoons"]:
        return "teaspoon"

    # Cup variations
    if unit_lower in ["c", "cup", "cups"]:
        return "cup"

    # Ounce variations
    if unit_lower in ["oz", "ounce", "ounces"]:
        return "ounce"

    # Pound variations
    if unit_lower in ["lb", "lbs", "pound", "pounds"]:
        return "pound"

    # Gram variations
    if unit_lower in ["g", "gram", "grams"]:
        return "gram"

    # Can variations
    if unit_lower in ["can", "cans"]:
        return "can"

    # Count-based (for eggs, items, etc.) - return empty string to merge better
    if unit_lower in ["large", "medium", "small", "whole", "count"]:
        return ""

    # Return as-is if no normalization needed
    return unit_lower if unit_lower else ""


def parse_quantity_range(quantity_str: str) -> float:
    """Parse a quantity string to a numeric value.

    Handles various quantity formats including fractions, ranges, and decimals.
    For ranges (e.g., "2-3"), returns the midpoint.

    Args:
        quantity_str: String representation of quantity (e.g., "2", "1/2", "2-3")

    Returns:
        Numeric value as float

    Examples:
        >>> parse_quantity_range("2")
        2.0
        >>> parse_quantity_range("1/2")
        0.5
        >>> parse_quantity_range("2-3")
        2.5
    """
    quantity_str = quantity_str.strip()

    # Handle ranges (e.g., "2-3", "1-2")
    if "-" in quantity_str and "to" not in quantity_str.lower():
        parts = quantity_str.split("-")
        if len(parts) == 2:
            try:
                low = float(Fraction(parts[0].strip()))
                high = float(Fraction(parts[1].strip()))
                return (low + high) / 2
            except (ValueError, ZeroDivisionError):
                return 1.0

    # Handle "X to Y" format
    if "to" in quantity_str.lower():
        parts = re.split(r"\s+to\s+", quantity_str.lower())
        if len(parts) == 2:
            try:
                low = float(Fraction(parts[0].strip()))
                high = float(Fraction(parts[1].strip()))
                return (low + high) / 2
            except (ValueError, ZeroDivisionError):
                return 1.0

    # Handle fractions and decimals
    try:
        return float(Fraction(quantity_str))
    except (ValueError, ZeroDivisionError):
        return 1.0


def categorize_ingredient(ingredient_name: str) -> str:
    """Categorize an ingredient into a grocery store section.

    Uses keyword matching to determine which section of the grocery store
    an ingredient belongs to (e.g., Produce, Meat, Dairy).

    Categories are checked in priority order to handle ambiguous matches:
    1. Bakery (tortillas, bread) - checked first for specific items
    2. Meat - specific protein items
    3. Dairy - eggs, milk, cheese
    4. Pantry - dried/canned goods, spices, oils
    5. Frozen - frozen items
    6. Produce - fresh vegetables and fruits (checked later to avoid conflicts)
    7. Other - fallback for unmatched items

    Args:
        ingredient_name: Name of the ingredient to categorize

    Returns:
        Category name (e.g., "Produce", "Meat", "Dairy", "Other")

    Examples:
        >>> categorize_ingredient("fresh tomatoes")
        'Produce'
        >>> categorize_ingredient("chicken breast")
        'Meat'
        >>> categorize_ingredient("cheddar cheese")
        'Dairy'
        >>> categorize_ingredient("corn tortillas")
        'Bakery'
    """
    ingredient_lower = ingredient_name.lower()

    # Check categories in priority order to avoid ambiguous matches
    # Order matters! More specific categories should be checked first
    priority_order = ["Bakery", "Meat", "Dairy", "Frozen", "Pantry", "Produce"]

    for category in priority_order:
        if category in CATEGORY_KEYWORDS:
            keywords = CATEGORY_KEYWORDS[category]
            for keyword in keywords:
                if keyword in ingredient_lower:
                    return category

    # Default to "Other" if no category match found
    return "Other"


# ==============================================================================
# RECIPE PARSING - Load and extract ingredients from recipe files
# ==============================================================================


def load_recipe_ingredients(recipe_path: Path) -> List[Tuple[str, str, str]]:
    """Load and parse ingredients from a recipe markdown file.

    Reads a recipe file and extracts all ingredients from the ## Ingredients
    section. Handles subsections like "For the Filling", "For Assembly", etc.

    Args:
        recipe_path: Path to the recipe markdown file

    Returns:
        List of tuples (quantity, unit, ingredient_name) for each ingredient

    Raises:
        FileNotFoundError: If recipe file doesn't exist

    Examples:
        >>> ingredients = load_recipe_ingredients(Path("recipes/pasta.md"))
        >>> len(ingredients) > 0
        True
    """
    if not recipe_path.exists():
        raise FileNotFoundError(f"Recipe file not found: {recipe_path}")

    ingredients: List[Tuple[str, str, str]] = []
    in_ingredients_section = False

    with open(recipe_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Check if we're entering the Ingredients section
            if line.startswith("## Ingredients"):
                in_ingredients_section = True
                continue

            # Check if we've left the Ingredients section (next ## header)
            if (
                in_ingredients_section
                and line.startswith("## ")
                and "Ingredients" not in line
            ):
                break

            # Skip subsection headers (### For the Filling, etc.)
            if in_ingredients_section and line.startswith("###"):
                continue

            # Parse ingredient lines (start with - or *)
            if in_ingredients_section and (
                line.startswith("-") or line.startswith("*")
            ):
                parsed = parse_ingredient_line(line)
                if parsed:
                    ingredients.append(parsed)

    return ingredients


# ==============================================================================
# GROCERY LIST GENERATION - Merge, quantify, and organize ingredients
# ==============================================================================


def merge_ingredients(
    all_ingredients: List[Tuple[str, str, str]],
) -> Dict[str, Dict[str, float]]:
    """Merge and quantify duplicate ingredients across recipes.

    Combines ingredients with the same name and unit, summing their quantities.
    For example, "2 cups flour" + "1 cup flour" = "3 cups flour".

    Args:
        all_ingredients: List of (quantity, unit, name) tuples from all recipes

    Returns:
        Dictionary mapping ingredient names to {unit: total_quantity} dicts

    Examples:
        >>> ingredients = [("2", "cup", "flour"), ("1", "cup", "flour")]
        >>> merged = merge_ingredients(ingredients)
        >>> merged["flour"]["cup"]
        3.0
    """
    merged: Dict[str, Dict[str, float]] = {}

    for quantity_str, unit, name in all_ingredients:
        # Normalize the ingredient name (lowercase, strip extra whitespace)
        name_clean = " ".join(name.lower().split())

        # Normalize the unit
        unit_norm = normalize_unit(unit)

        # Parse quantity to numeric value
        quantity = parse_quantity_range(quantity_str)

        # Initialize ingredient entry if not exists
        if name_clean not in merged:
            merged[name_clean] = {}

        # Add or update quantity for this unit
        if unit_norm not in merged[name_clean]:
            merged[name_clean][unit_norm] = 0.0

        merged[name_clean][unit_norm] += quantity

    return merged


def format_quantity(quantity: float) -> str:
    """Format a numeric quantity as a readable string.

    Converts decimal quantities to fractions where appropriate for better
    readability (e.g., 0.5 -> "1/2", 2.5 -> "2 1/2").

    Args:
        quantity: Numeric quantity value

    Returns:
        Formatted string representation

    Examples:
        >>> format_quantity(2.0)
        '2'
        >>> format_quantity(0.5)
        '1/2'
        >>> format_quantity(2.5)
        '2 1/2'
    """
    # If it's a whole number, return as integer
    if quantity == int(quantity):
        return str(int(quantity))

    # Try to convert to fraction for common values
    frac = Fraction(quantity).limit_denominator(16)

    # If the fraction is a good representation, use it
    if abs(float(frac) - quantity) < 0.01:
        if frac.numerator > frac.denominator:
            # Mixed number (e.g., 2 1/2)
            whole = frac.numerator // frac.denominator
            remainder = frac.numerator % frac.denominator
            if remainder == 0:
                return str(whole)
            return f"{whole} {remainder}/{frac.denominator}"
        else:
            # Simple fraction (e.g., 1/2)
            return f"{frac.numerator}/{frac.denominator}"

    # Fall back to decimal with one decimal place
    return f"{quantity:.1f}"


def pluralize_unit(unit: str, quantity: float) -> str:
    """Pluralize a unit based on quantity.

    Adds 's' to unit names when quantity is greater than 1, following
    common English pluralization rules for measurement units.

    Args:
        unit: Unit name (e.g., "cup", "tablespoon")
        quantity: Numeric quantity

    Returns:
        Pluralized unit if quantity > 1, otherwise singular form.
        Returns empty string if unit is empty.

    Examples:
        >>> pluralize_unit("cup", 2.0)
        'cups'
        >>> pluralize_unit("cup", 1.0)
        'cup'
        >>> pluralize_unit("tablespoon", 0.5)
        'tablespoon'
        >>> pluralize_unit("", 5.0)
        ''
        >>> pluralize_unit("cloves", 2.0)
        'cloves'
    """
    # Return empty string if unit is empty (ingredient counted by item)
    if not unit:
        return ""

    # Don't pluralize if quantity is 1 or less
    if quantity <= 1:
        return unit

    # Don't add 's' if already plural (ends with 's')
    if unit.endswith("s"):
        return unit

    # Most units just add 's'
    return f"{unit}s"


def generate_grocery_list_from_recipes(
    recipe_names: List[str], recipes_dir: Path
) -> str:
    """Generate a formatted grocery list from a list of recipes.

    This is the main function that orchestrates the grocery list generation:
    1. Load ingredients from all specified recipes
    2. Merge duplicate ingredients and sum quantities
    3. Categorize ingredients by grocery store section
    4. Format as clean Markdown with checkboxes

    Args:
        recipe_names: List of recipe names (e.g., ["breakfast-burritos", "fish-tacos"])
        recipes_dir: Path to the recipes directory

    Returns:
        Formatted grocery list as Markdown string with checkboxes

    Examples:
        >>> recipes = ["breakfast-burritos", "fish-tacos"]
        >>> grocery_list = generate_grocery_list_from_recipes(recipes, Path("recipes"))
        >>> "## Produce" in grocery_list
        True
    """
    all_ingredients: List[Tuple[str, str, str]] = []

    # Load ingredients from all recipes
    for recipe_name in recipe_names:
        # Handle both with and without .md extension
        recipe_filename = (
            recipe_name if recipe_name.endswith(".md") else f"{recipe_name}.md"
        )
        recipe_path = recipes_dir / recipe_filename

        try:
            ingredients = load_recipe_ingredients(recipe_path)
            all_ingredients.extend(ingredients)
        except FileNotFoundError:
            print(f"Warning: Recipe file not found: {recipe_path}")
            continue

    if not all_ingredients:
        return "# Grocery List\n\nNo ingredients found in the specified recipes.\n"

    # Merge duplicate ingredients
    merged = merge_ingredients(all_ingredients)

    # Categorize ingredients
    categorized: Dict[str, List[Tuple[str, str, float]]] = {
        "Produce": [],
        "Meat": [],
        "Dairy": [],
        "Pantry": [],
        "Frozen": [],
        "Bakery": [],
        "Other": [],
    }

    for ingredient_name, units_dict in merged.items():
        category = categorize_ingredient(ingredient_name)

        for unit, quantity in units_dict.items():
            categorized[category].append((ingredient_name, unit, quantity))

    # Sort ingredients within each category alphabetically
    for category in categorized:
        categorized[category].sort(key=lambda x: x[0])

    # Generate formatted Markdown output
    output_lines = ["# Grocery List\n"]

    # Add each category that has items
    for category in ["Produce", "Meat", "Dairy", "Pantry", "Frozen", "Bakery", "Other"]:
        items = categorized[category]
        if not items:
            continue

        output_lines.append(f"## {category}\n")

        for ingredient_name, unit, quantity in items:
            qty_str = format_quantity(quantity)

            # Pluralize unit based on quantity
            unit_display = pluralize_unit(unit, quantity)

            # Format: "- [ ] 2 cups flour" or "- [ ] 8 eggs" (no unit)
            if unit_display:
                output_lines.append(f"- [ ] {qty_str} {unit_display} {ingredient_name}")
            else:
                output_lines.append(f"- [ ] {qty_str} {ingredient_name}")

        output_lines.append("")  # Blank line after each category

    return "\n".join(output_lines)


def generate_grocery_list_from_meal_plan(meal_plan_path: Path) -> str:
    """Generate a grocery list from a meal plan markdown file.

    Parses a meal plan file to extract all recipe names, then generates
    a comprehensive grocery list for all meals in the plan.

    Args:
        meal_plan_path: Path to the meal plan markdown file

    Returns:
        Formatted grocery list as Markdown string

    Raises:
        FileNotFoundError: If meal plan file doesn't exist

    Examples:
        >>> plan_path = Path("plans/meal_plan_2026-01-20.md")
        >>> grocery_list = generate_grocery_list_from_meal_plan(plan_path)
        >>> "# Grocery List" in grocery_list
        True
    """
    if not meal_plan_path.exists():
        raise FileNotFoundError(f"Meal plan file not found: {meal_plan_path}")

    # Extract recipe names from meal plan
    recipe_names: List[str] = []

    with open(meal_plan_path, "r", encoding="utf-8") as f:
        content = f.read()

        # Pattern to match recipe names (markdown bold headers like **Breakfast Burritos**)
        # These appear as meal titles in the meal plan
        pattern = r"\*\*([^*]+)\*\*"
        matches = re.findall(pattern, content)

        for match in matches:
            # Skip non-recipe headers (like day names, metadata)
            if match.strip() and not any(
                skip in match.lower()
                for skip in [
                    "no ",
                    "recipe available",
                    "breakfast",
                    "lunch",
                    "dinner",
                    "prep time",
                    "cook time",
                    "total time",
                ]
            ):
                # Convert to filename format (e.g., "Breakfast Burritos" -> "breakfast-burritos")
                recipe_filename = match.strip().lower().replace(" ", "-")
                if recipe_filename not in recipe_names:
                    recipe_names.append(recipe_filename)

    # Get recipes directory (assuming it's at same level as plans directory)
    recipes_dir = meal_plan_path.parent.parent / "recipes"

    # Generate grocery list
    return generate_grocery_list_from_recipes(recipe_names, recipes_dir)


# ==============================================================================
# MAIN ENTRY POINT - For testing and standalone usage
# ==============================================================================


if __name__ == "__main__":
    """Test the grocery list generator with sample recipes."""

    # Get the script's directory and navigate to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    recipes_dir = project_root / "recipes"

    # Test with a few sample recipes
    test_recipes = ["breakfast-burritos", "fish-tacos", "grilled-chicken-salad"]

    print("=" * 80)
    print("GROCERY LIST GENERATOR - TEST OUTPUT")
    print("=" * 80)
    print()

    grocery_list = generate_grocery_list_from_recipes(test_recipes, recipes_dir)
    print(grocery_list)

    print("=" * 80)
    print("TEST COMPLETED")
    print("=" * 80)
