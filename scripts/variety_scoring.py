#!/usr/bin/env python3
"""Variety Scoring for Meal Plans

This module calculates variety scores and penalties for meal plans based on:
- Cuisine diversity
- Recipe repetition
- Ingredient diversity
- Constraint violations

Scores help optimize meal plans for maximum variety and compliance.

Author: THC Meal Prep Planner Team
Created: 2026-01-18
"""

from typing import Any, Optional

# Try to import LLM utilities for cuisine classification
try:
    from llm_utils import get_openai_client
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


# ==============================================================================
# SCORING CONFIGURATION
# ==============================================================================

# Scoring weights for different variety factors
SCORING_WEIGHTS = {
    "cuisine_variety": 10,      # Points for each unique cuisine
    "recipe_diversity": 15,     # Points for each unique recipe
    "no_consecutive_repeats": 20,  # Bonus for no back-to-back recipes
}

# Penalty values for constraint violations
PENALTY_VALUES = {
    "recipe_repetition": -10,    # Per repeated recipe within min_days
    "consecutive_same_cuisine": -5,  # Per consecutive day with same cuisine
    "missing_meal": -50,         # Per missing required meal
    "constraint_violation": -20, # Per general constraint violation
}


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================


def classify_cuisine_with_llm(recipe_title: str, ingredients: str = "") -> Optional[str]:
    """Use LLM to classify the cuisine type of a recipe.
    
    Args:
        recipe_title: Title of the recipe
        ingredients: Optional ingredients list as string
        
    Returns:
        Classified cuisine type or None if classification fails
        
    Example:
        cuisine = classify_cuisine_with_llm("Pad Thai", "rice noodles, peanuts...")
        # Returns: "Thai" or "Asian"
    """
    if not LLM_AVAILABLE:
        return None
    
    client = get_openai_client()
    if not client:
        return None
    
    try:
        prompt = f"""Classify the cuisine type of this recipe. Return only the cuisine name (e.g., Italian, Mexican, Asian, American, Mediterranean, etc.).

Recipe: {recipe_title}"""
        
        if ingredients:
            prompt += f"\nKey ingredients: {ingredients}"
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a culinary expert. Classify cuisines accurately and concisely."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=20,
            temperature=0.3,
        )
        
        if response.choices and len(response.choices) > 0:
            cuisine = response.choices[0].message.content
            if cuisine:
                return cuisine.strip()
        
        return None
    except Exception:
        # Silently fail and return None
        return None


# ==============================================================================
# VARIETY SCORING FUNCTIONS
# ==============================================================================


def calculate_cuisine_variety_score(meal_plan: dict[str, Any]) -> dict[str, Any]:
    """Calculate variety score based on cuisine diversity.
    
    Awards points for using different cuisines throughout the week.
    Penalties for consecutive days with the same cuisine.
    Attempts to classify unknown cuisines using LLM if available.
    
    Args:
        meal_plan: The meal plan dictionary
        
    Returns:
        Dictionary with score and details
        
    Example:
        score = calculate_cuisine_variety_score(meal_plan)
        print(f"Cuisine variety score: {score['total']}")
    """
    cuisines = []
    consecutive_penalties = 0
    prev_day_cuisines = set()
    
    # Collect cuisines from each day
    for day_name, meals in meal_plan.get("week", {}).items():
        day_cuisines = set()
        for meal_type, recipe in meals.items():
            cuisine = recipe.get("Cuisine")
            
            # Try to classify unknown cuisines with LLM
            if not cuisine or str(cuisine).strip().lower() in ("unknown", ""):
                recipe_title = recipe.get("title", "")
                # Only attempt classification for actual recipes, not placeholders
                if recipe_title and not recipe_title.startswith("No "):
                    classified = classify_cuisine_with_llm(recipe_title)
                    if classified:
                        cuisine = classified
                    else:
                        cuisine = "Unknown"
                else:
                    cuisine = "Unknown"
            
            # Only add known cuisines to the variety calculation
            if cuisine and str(cuisine).strip().lower() != "unknown":
                cuisines.append(cuisine)
                day_cuisines.add(cuisine)
        
        # Check for consecutive days sharing any cuisine
        if prev_day_cuisines and (prev_day_cuisines & day_cuisines):
            consecutive_penalties += 1
        
        prev_day_cuisines = day_cuisines
    
    # Calculate score - only count known cuisines
    unique_cuisines = len(set(cuisines))
    variety_points = unique_cuisines * SCORING_WEIGHTS["cuisine_variety"]
    penalty_points = consecutive_penalties * PENALTY_VALUES["consecutive_same_cuisine"]
    
    return {
        "total": variety_points + penalty_points,
        "variety_points": variety_points,
        "penalty_points": penalty_points,
        "unique_cuisines": unique_cuisines,
        "total_cuisines": len(cuisines),
        "consecutive_penalties": consecutive_penalties,
    }


def calculate_recipe_diversity_score(meal_plan: dict[str, Any]) -> dict[str, Any]:
    """Calculate variety score based on recipe diversity.
    
    Awards points for using different recipes throughout the week.
    
    Args:
        meal_plan: The meal plan dictionary
        
    Returns:
        Dictionary with score and details
        
    Example:
        score = calculate_recipe_diversity_score(meal_plan)
        print(f"Recipe diversity score: {score['total']}")
    """
    recipes = []
    
    # Collect all recipes used, excluding placeholder entries
    for day_name, meals in meal_plan.get("week", {}).items():
        for meal_type, recipe in meals.items():
            recipe_title = recipe.get("title")
            # Skip placeholder meals whose titles start with "No "
            # (e.g., "No breakfast recipe available")
            if recipe_title and not recipe_title.startswith("No "):
                recipes.append(recipe_title)
    
    # Calculate score
    unique_recipes = len(set(recipes))
    total_meals = len(recipes)
    diversity_points = unique_recipes * SCORING_WEIGHTS["recipe_diversity"]
    
    # Bonus if no recipe is repeated
    no_repeats_bonus = 0
    if unique_recipes == total_meals and total_meals > 0:
        no_repeats_bonus = SCORING_WEIGHTS["no_consecutive_repeats"]
    
    return {
        "total": diversity_points + no_repeats_bonus,
        "diversity_points": diversity_points,
        "no_repeats_bonus": no_repeats_bonus,
        "unique_recipes": unique_recipes,
        "total_meals": total_meals,
        "repetition_count": total_meals - unique_recipes,
    }


def calculate_repetition_penalties(
    meal_plan: dict[str, Any],
    recently_used_recipes: list[str],
    min_days_between_repeats: int = 3,
) -> dict[str, Any]:
    """Calculate penalties for recipe repetition violations.
    
    Applies penalties for using recipes that were used too recently
    based on the minimum days between repeats constraint.
    
    Args:
        meal_plan: The meal plan dictionary
        recently_used_recipes: List of recipe filenames used recently
        min_days_between_repeats: Minimum days required between repeats
        
    Returns:
        Dictionary with penalty score and details
        
    Example:
        penalties = calculate_repetition_penalties(
            meal_plan,
            ["breakfast-burritos.md"],
            min_days_between_repeats=3
        )
    """
    violations = []
    
    # Check each recipe in the current plan
    for day_name, meals in meal_plan.get("week", {}).items():
        for meal_type, recipe in meals.items():
            recipe_filename = recipe.get("filename")
            if recipe_filename and recipe_filename in recently_used_recipes:
                violations.append({
                    "day": day_name,
                    "meal_type": meal_type,
                    "recipe": recipe.get("title"),
                    "filename": recipe_filename,
                })
    
    # Calculate penalty
    penalty_points = len(violations) * PENALTY_VALUES["recipe_repetition"]
    
    return {
        "total": penalty_points,
        "violation_count": len(violations),
        "violations": violations,
        "min_days_required": min_days_between_repeats,
    }


def calculate_constraint_penalties(
    meal_plan: dict[str, Any],
    constraints: dict[str, Any],
) -> dict[str, Any]:
    """Calculate penalties for constraint violations.
    
    Checks for missing required meals and variety constraint violations.
    
    Args:
        meal_plan: The meal plan dictionary
        constraints: The constraints dictionary
        
    Returns:
        Dictionary with penalty score and details
        
    Example:
        penalties = calculate_constraint_penalties(meal_plan, constraints)
    """
    violations = []
    missing_meals = 0
    variety_violations = 0
    
    # Get required meals per day
    meals_per_day = constraints.get("meals_per_day", {})
    
    # Check each day for missing meals
    for day_name, meals in meal_plan.get("week", {}).items():
        for meal_type, required_count in meals_per_day.items():
            if required_count > 0:
                meal = meals.get(meal_type, {})
                # Check if meal is missing or is a placeholder
                title = meal.get("title", "")
                if not meal or (isinstance(title, str) and title.startswith("No ")):
                    missing_meals += 1
                    violations.append({
                        "type": "missing_meal",
                        "day": day_name,
                        "meal_type": meal_type,
                    })
    
    # Check variety constraints
    variety_config = constraints.get("variety", {})
    
    # Check min_unique_cuisines constraint
    min_unique_cuisines = variety_config.get("min_unique_cuisines")
    if min_unique_cuisines:
        cuisines = set()
        for day_name, meals in meal_plan.get("week", {}).items():
            for meal_type, recipe in meals.items():
                cuisine = recipe.get("Cuisine")
                if cuisine and str(cuisine).strip().lower() != "unknown":
                    cuisines.add(cuisine)
        
        if len(cuisines) < min_unique_cuisines:
            variety_violations += 1
            violations.append({
                "type": "insufficient_cuisine_variety",
                "expected": min_unique_cuisines,
                "actual": len(cuisines),
            })
    
    # Check avoid_consecutive_ingredients constraint
    # DISABLED: This feature is disabled pending a more comprehensive implementation
    # that properly parses ingredient lists rather than just checking protein.
    # The current simplified implementation essentially duplicates protein blocking.
    # TODO: Re-enable with proper ingredient parsing in future iteration
    if False and variety_config.get("avoid_consecutive_ingredients", False):
        prev_ingredients = set()
        for day_name, meals in meal_plan.get("week", {}).items():
            day_ingredients = set()
            for meal_type, recipe in meals.items():
                # Extract main ingredients (this is a simplified version)
                # In a full implementation, you'd parse the ingredients list
                protein = recipe.get("Protein")
                if protein:
                    day_ingredients.add(protein.lower())
            
            # Check for consecutive day overlap
            if prev_ingredients and (prev_ingredients & day_ingredients):
                variety_violations += 1
                violations.append({
                    "type": "consecutive_ingredients",
                    "day": day_name,
                    "ingredients": list(prev_ingredients & day_ingredients),
                })
            
            prev_ingredients = day_ingredients
    
    # Calculate penalty
    penalty_points = (
        missing_meals * PENALTY_VALUES["missing_meal"]
        + variety_violations * PENALTY_VALUES["constraint_violation"]
    )
    
    return {
        "total": penalty_points,
        "missing_meals": missing_meals,
        "variety_violations": variety_violations,
        "violations": violations,
    }


# ==============================================================================
# COMPREHENSIVE SCORING
# ==============================================================================


def calculate_meal_plan_score(
    meal_plan: dict[str, Any],
    constraints: dict[str, Any],
    recently_used_recipes: list[str] = None,
) -> dict[str, Any]:
    """Calculate comprehensive variety score for a meal plan.
    
    This is the main scoring function that combines all variety metrics
    and penalties to produce an overall meal plan quality score.
    
    Higher scores indicate better variety and constraint compliance.
    
    Args:
        meal_plan: The meal plan dictionary
        constraints: The constraints dictionary
        recently_used_recipes: List of recently used recipe filenames
        
    Returns:
        Dictionary with total score and detailed breakdown
        
    Example:
        score = calculate_meal_plan_score(meal_plan, constraints)
        print(f"Overall plan score: {score['total_score']}")
        print(f"Grade: {score['grade']}")
    """
    if recently_used_recipes is None:
        recently_used_recipes = []
    
    # Calculate individual scores
    cuisine_score = calculate_cuisine_variety_score(meal_plan)
    recipe_score = calculate_recipe_diversity_score(meal_plan)
    
    # Calculate penalties
    min_days = constraints.get("variety", {}).get("min_days_between_repeats", 3)
    repetition_penalty = calculate_repetition_penalties(
        meal_plan,
        recently_used_recipes,
        min_days,
    )
    constraint_penalty = calculate_constraint_penalties(meal_plan, constraints)
    
    # Calculate total score
    total_score = (
        cuisine_score["total"]
        + recipe_score["total"]
        + repetition_penalty["total"]
        + constraint_penalty["total"]
    )
    
    # Determine grade based on score
    if total_score >= 200:
        grade = "A+"
    elif total_score >= 150:
        grade = "A"
    elif total_score >= 100:
        grade = "B"
    elif total_score >= 50:
        grade = "C"
    elif total_score >= 0:
        grade = "D"
    else:
        grade = "F"
    
    return {
        "total_score": total_score,
        "grade": grade,
        "cuisine_variety": cuisine_score,
        "recipe_diversity": recipe_score,
        "repetition_penalties": repetition_penalty,
        "constraint_penalties": constraint_penalty,
    }


def format_score_summary(score: dict[str, Any]) -> str:
    """Format a score dictionary into a human-readable summary.
    
    Args:
        score: Score dictionary from calculate_meal_plan_score()
        
    Returns:
        Formatted string for display in meal plans
        
    Example:
        summary = format_score_summary(score)
        print(summary)
    """
    lines = []
    lines.append("## Meal Plan Quality Score")
    lines.append("")
    lines.append(f"**Overall Score**: {score['total_score']} ({score['grade']})")
    lines.append("")
    
    # Cuisine variety
    cuisine = score["cuisine_variety"]
    lines.append("### Cuisine Variety")
    lines.append(f"- Unique cuisines: {cuisine['unique_cuisines']}")
    lines.append(f"- Variety points: +{cuisine['variety_points']}")
    if cuisine['consecutive_penalties'] > 0:
        lines.append(f"- Consecutive cuisine penalties: {cuisine['penalty_points']}")
    lines.append(f"- **Subtotal**: {cuisine['total']}")
    lines.append("")
    
    # Recipe diversity
    recipe = score["recipe_diversity"]
    lines.append("### Recipe Diversity")
    lines.append(f"- Unique recipes: {recipe['unique_recipes']} / {recipe['total_meals']}")
    lines.append(f"- Diversity points: +{recipe['diversity_points']}")
    if recipe['no_repeats_bonus'] > 0:
        lines.append(f"- No repeats bonus: +{recipe['no_repeats_bonus']}")
    lines.append(f"- **Subtotal**: {recipe['total']}")
    lines.append("")
    
    # Repetition penalties
    rep = score["repetition_penalties"]
    if rep['violation_count'] > 0:
        lines.append("### Repetition Penalties")
        lines.append(f"- Violations: {rep['violation_count']}")
        lines.append(f"- Minimum days required: {rep['min_days_required']}")
        for v in rep['violations']:
            lines.append(f"  - {v['day']} {v['meal_type']}: {v['recipe']}")
        lines.append(f"- **Subtotal**: {rep['total']}")
        lines.append("")
    
    # Constraint penalties
    const = score["constraint_penalties"]
    has_missing_meals = const.get('missing_meals', 0) > 0
    has_variety_violations = const.get('variety_violations', 0) > 0
    
    if has_missing_meals or has_variety_violations:
        lines.append("### Constraint Violations")
        
        if has_missing_meals:
            lines.append(f"- Missing meals: {const['missing_meals']}")
            for v in const.get('violations', []):
                if v.get('type') == 'missing_meal':
                    lines.append(f"  - {v['day']} {v['meal_type']}")
        
        if has_variety_violations:
            lines.append(f"- Variety violations: {const.get('variety_violations', 0)}")
            for v in const.get('violations', []):
                if v.get('type') == 'insufficient_cuisine_variety':
                    lines.append(f"  - Insufficient cuisine variety: {v.get('actual', 0)} < {v.get('expected', 0)} required")
                elif v.get('type') == 'consecutive_ingredients':
                    ingredients = ', '.join(v.get('ingredients', []))
                    lines.append(f"  - Consecutive ingredients on {v.get('day')}: {ingredients}")
        
        lines.append(f"- **Subtotal**: {const['total']}")
        lines.append("")
    
    return "\n".join(lines)
