#!/usr/bin/env python3
"""Meal Plan Generator - ELI5 Version

This script creates a weekly meal plan by selecting recipes based on user profiles
and constraints. Think of it like a smart assistant that helps you plan what to
eat for the week!

What does this script do?
-------------------------
1. Reads your profile (who you are, what you like/dislike)
2. Loads available recipes (meals you can make)
3. Reads constraints (rules for planning, like time limits)
4. Creates a weekly meal plan (7 days of breakfast, lunch, dinner)
5. Saves the plan as a Markdown file

How to use this script:
-----------------------
    python scripts/generate_meal_plan.py

That's it! The script will:
- Use the sample profile in profiles/ashuah.md
- Look at all recipes in the recipes/ folder
- Follow rules in constraints/sample_constraints.yaml
- Create a meal plan in plans/meal_plan_YYYY-MM-DD.md

What is ELI5?
-------------
ELI5 means "Explain Like I'm 5" - we use simple language and lots of comments
so anyone can understand how this works, even if you're new to programming!

Author: THC Meal Prep Planner Team
Created: 2026-01-18
"""

# ==============================================================================
# IMPORTS - These are tools from other Python libraries we need
# ==============================================================================

import os  # For working with files and folders
import re  # For finding patterns in text (like extracting recipe info)
import yaml  # For reading YAML configuration files
from datetime import datetime, timedelta  # For working with dates
from pathlib import Path  # For handling file paths in a smart way
from typing import Any  # For type hints (helps catch bugs)


# ==============================================================================
# HELPER FUNCTIONS - Small functions that do one specific job
# ==============================================================================


def parse_markdown_file(file_path: Path) -> dict[str, Any]:
    """Read a Markdown file and extract information from it.

    This function is like reading a recipe card - it finds all the important
    information and organizes it so we can use it later.

    Args:
        file_path: The location of the Markdown file to read

    Returns:
        A dictionary (like a labeled box) containing all the extracted info

    Example:
        If we have a recipe file with:
            # Recipe Name
            - **Category**: Breakfast
            - **Prep Time**: 15 minutes

        We'll extract: {'title': 'Recipe Name', 'Category': 'Breakfast', ...}
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Create a box to store all the information we find
    data = {}

    # Find the title (the first big heading with # in Markdown)
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if title_match:
        data["title"] = title_match.group(1).strip()

    # Find all the bullet points with bold labels like "- **Key**: Value"
    # This pattern looks complicated, but it just finds text like:
    # - **Category**: Breakfast
    pattern = r"^-\s+\*\*([^*]+)\*\*:\s+(.+)$"
    for match in re.finditer(pattern, content, re.MULTILINE):
        key = match.group(1).strip()
        value = match.group(2).strip()
        data[key] = value

    # Store the full content too, in case we need it later
    data["content"] = content

    return data


def load_profile(profile_path: Path) -> dict[str, Any]:
    """Load a user profile from a Markdown file.

    A profile tells us about the person we're planning meals for:
    - What they can't eat (allergies)
    - What they prefer not to eat
    - How many people they're feeding
    - Their nutritional goals

    Args:
        profile_path: Where to find the profile file

    Returns:
        Dictionary with all the profile information

    Example:
        profile = load_profile(Path("profiles/ashuah.md"))
        print(profile['Name'])  # "Ashuah Patel"
    """
    print(f"📋 Loading profile from {profile_path.name}...")
    return parse_markdown_file(profile_path)


def load_recipes(recipes_dir: Path) -> list[dict[str, Any]]:
    """Load all recipe files from the recipes directory.

    This function looks through the recipes folder and reads every recipe file
    it finds. Each recipe becomes a dictionary with all its information.

    Args:
        recipes_dir: The folder where recipe files are stored

    Returns:
        A list of recipe dictionaries, one for each recipe file

    Example:
        recipes = load_recipes(Path("recipes/"))
        print(f"Found {len(recipes)} recipes!")
    """
    print(f"📖 Loading recipes from {recipes_dir}...")
    recipes = []

    # Look at every file in the recipes folder
    for recipe_file in recipes_dir.glob("*.md"):
        # Skip special files that aren't recipes
        if recipe_file.name == ".gitkeep":
            continue

        # Read the recipe and add it to our list
        recipe = parse_markdown_file(recipe_file)
        recipe["filename"] = recipe_file.name
        recipes.append(recipe)

    print(f"   Found {len(recipes)} recipe(s)")
    return recipes


def load_constraints(constraints_path: Path) -> dict[str, Any]:
    """Load planning constraints from a YAML file.

    Constraints are the rules we follow when making the meal plan:
    - How much time do we have for cooking?
    - What's our budget?
    - How many meals do we need?

    Args:
        constraints_path: Where to find the constraints file

    Returns:
        Dictionary with all the constraint rules

    Example:
        constraints = load_constraints(Path("constraints/sample_constraints.yaml"))
        max_time = constraints['time']['max_weeknight_prep_minutes']
    """
    print(f"⚙️  Loading constraints from {constraints_path.name}...")
    with open(constraints_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def is_recipe_suitable(
    recipe: dict[str, Any], profile: dict[str, Any], is_weeknight: bool, constraints: dict[str, Any]
) -> bool:
    """Check if a recipe is suitable for a person and day.

    This is like asking: "Can this person eat this meal on this day?"
    We check things like:
    - Does it take too long to cook for a weeknight?
    - Does it contain ingredients the person is allergic to?

    Args:
        recipe: The recipe we're considering
        profile: The person's profile (allergies, preferences)
        is_weeknight: Is this a weeknight (Mon-Fri) or weekend?
        constraints: The planning rules

    Returns:
        True if the recipe is OK to use, False if not

    Example:
        if is_recipe_suitable(recipe, profile, True, constraints):
            print("This recipe works for a weeknight!")
    """
    # For this simple version, we just check cooking time
    # In a real version, we'd also check for allergies, dietary restrictions, etc.

    # Get the time limit based on whether it's a weeknight or weekend
    if is_weeknight:
        max_time = constraints["time"]["max_weeknight_prep_minutes"]
    else:
        max_time = constraints["time"]["max_weekend_prep_minutes"]

    # Try to get the total time from the recipe
    # If the recipe doesn't have time info, assume it fits within weeknight constraints
    # (This is a reasonable default since most quick recipes don't specify time)
    default_time = constraints["time"]["max_weeknight_prep_minutes"]
    total_time_str = recipe.get("Total Time", f"{default_time} minutes")

    # Extract the number of minutes from strings like "35 minutes"
    time_match = re.search(r"(\d+)", total_time_str)
    if time_match:
        recipe_time = int(time_match.group(1))
        if recipe_time > max_time:
            return False  # Too long to cook!

    return True  # Recipe is suitable!


def generate_meal_plan(
    profile: dict[str, Any],
    recipes: list[dict[str, Any]],
    constraints: dict[str, Any],
) -> dict[str, Any]:
    """Generate a weekly meal plan.

    This is the main function that creates the meal plan! It picks recipes
    for each day of the week, making sure they fit the constraints.

    The algorithm is simple for this demo version:
    1. For each day of the week
    2. For each meal type (breakfast, lunch, dinner)
    3. Pick a suitable recipe
    4. Try not to repeat recipes too soon

    Args:
        profile: The person's profile
        recipes: List of available recipes
        constraints: Planning rules

    Returns:
        A dictionary with the complete meal plan

    Example:
        plan = generate_meal_plan(profile, recipes, constraints)
        print(plan['week']['Monday']['breakfast']['title'])
    """
    print("\n🎯 Generating meal plan...")

    # Get the start and end dates for the week
    start_date = datetime.strptime(constraints["week"]["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(constraints["week"]["end_date"], "%Y-%m-%d")

    # Create the structure to hold our meal plan
    meal_plan = {
        "profile_name": profile.get("Name", "Unknown"),
        "week_start": start_date.strftime("%Y-%m-%d"),
        "week_end": end_date.strftime("%Y-%m-%d"),
        "week": {},  # This will hold all the daily meals
    }

    # Keep track of recently used recipes to avoid repetition
    recently_used = []

    # Day names for display
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Loop through each day of the week
    current_date = start_date
    for day_name in days:
        # Is this a weeknight? (Monday = 0, Sunday = 6)
        is_weeknight = current_date.weekday() < 5  # Monday-Friday

        # Create a place to store today's meals
        daily_meals = {}

        # For each meal type (breakfast, lunch, dinner)
        meal_types = ["breakfast", "lunch", "dinner"]
        for meal_type in meal_types:
            # How many of this meal type do we need?
            needed = constraints["meals_per_day"].get(meal_type, 0)

            if needed > 0:
                # Find a suitable recipe for this meal
                # Filter recipes by category
                suitable_recipes = [
                    r
                    for r in recipes
                    if r.get("Category", "").lower() == meal_type
                    and is_recipe_suitable(r, profile, is_weeknight, constraints)
                    and r.get("filename") not in recently_used
                ]

                # If we have suitable recipes, pick the first one
                # (In a real version, we might randomize or optimize this)
                if suitable_recipes:
                    chosen_recipe = suitable_recipes[0]
                    daily_meals[meal_type] = chosen_recipe

                    # Remember we used this recipe
                    recently_used.append(chosen_recipe.get("filename"))

                    # Keep the recently_used list from getting too long
                    # Use the variety constraint to determine how long to track
                    max_recently_used = constraints.get("variety", {}).get(
                        "min_days_between_repeats", 3
                    )
                    if len(recently_used) > max_recently_used:
                        recently_used.pop(0)
                else:
                    # No suitable recipes found - note this in the plan
                    daily_meals[meal_type] = {
                        "title": f"No {meal_type} recipe available",
                        "note": "Consider adding more recipes to the database",
                    }

        # Add today's meals to the weekly plan
        meal_plan["week"][day_name] = daily_meals

        # Move to the next day
        current_date += timedelta(days=1)

    print("   ✅ Meal plan generated successfully!")
    return meal_plan


def format_meal_plan_as_markdown(meal_plan: dict[str, Any]) -> str:
    """Convert a meal plan to a nice Markdown format for saving.

    This takes our meal plan data and turns it into a readable Markdown
    document that looks nice and is easy to read.

    Args:
        meal_plan: The complete meal plan dictionary

    Returns:
        A string containing the formatted Markdown

    Example:
        markdown = format_meal_plan_as_markdown(plan)
        print(markdown)  # Shows the nicely formatted plan
    """
    lines = []

    # Add a title
    lines.append(f"# Weekly Meal Plan for {meal_plan['profile_name']}")
    lines.append("")
    lines.append(
        f"**Week of {meal_plan['week_start']} to {meal_plan['week_end']}**"
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Add each day's meals
    for day_name, meals in meal_plan["week"].items():
        lines.append(f"## {day_name}")
        lines.append("")

        # Add each meal type
        for meal_type in ["breakfast", "lunch", "dinner"]:
            if meal_type in meals:
                meal = meals[meal_type]
                lines.append(f"### {meal_type.title()}")
                lines.append("")
                lines.append(f"**{meal.get('title', 'No recipe')}**")

                # Add extra details if available
                if "Prep Time" in meal:
                    lines.append(f"- Prep Time: {meal['Prep Time']}")
                if "Cook Time" in meal:
                    lines.append(f"- Cook Time: {meal['Cook Time']}")
                if "Total Time" in meal:
                    lines.append(f"- Total Time: {meal['Total Time']}")
                if "note" in meal:
                    lines.append(f"- *Note: {meal['note']}*")

                lines.append("")

        lines.append("---")
        lines.append("")

    # Add a footer with generation info
    lines.append("## Plan Information")
    lines.append("")
    lines.append(f"- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("- Generated by: THC Meal Prep Planner")
    lines.append(
        "- Script: `scripts/generate_meal_plan.py`"
    )
    lines.append("")

    return "\n".join(lines)


def save_meal_plan(meal_plan: dict[str, Any], output_dir: Path) -> Path:
    """Save the meal plan to a Markdown file.

    This writes the meal plan to a file so you can read it later or share it.

    Args:
        meal_plan: The complete meal plan
        output_dir: Where to save the file

    Returns:
        The path where the file was saved

    Example:
        file_path = save_meal_plan(plan, Path("plans/"))
        print(f"Saved to {file_path}")
    """
    # Create a filename with the date
    filename = f"meal_plan_{meal_plan['week_start']}.md"
    output_path = output_dir / filename

    # Convert to Markdown and save
    markdown_content = format_meal_plan_as_markdown(meal_plan)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"💾 Saved meal plan to {output_path}")
    return output_path


# ==============================================================================
# MAIN FUNCTION - This is where the program starts
# ==============================================================================


def main() -> None:
    """Main function that runs the meal plan generator.

    This is the "control center" that coordinates all the other functions.
    It loads the data, generates the plan, and saves the result.

    When you run this script, this is the function that executes.
    """
    print("=" * 70)
    print("🍽️  THC Meal Prep Planner - Meal Plan Generator")
    print("=" * 70)
    print()

    # Figure out where all the files are
    # We use Path(__file__) to find where this script is located
    # Then we go up one level (.parent) to get to the project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Define the paths to all the folders we need
    profiles_dir = project_root / "profiles"
    recipes_dir = project_root / "recipes"
    constraints_dir = project_root / "constraints"
    plans_dir = project_root / "plans"

    # Make sure the plans directory exists
    plans_dir.mkdir(exist_ok=True)

    try:
        # Step 1: Load the user profile
        # For this demo, we'll use Ashuah's profile
        profile_path = profiles_dir / "ashuah.md"
        profile = load_profile(profile_path)

        # Step 2: Load all available recipes
        recipes = load_recipes(recipes_dir)

        if not recipes:
            print("❌ Error: No recipes found! Please add recipe files to the recipes/ folder.")
            return

        # Step 3: Load the constraints
        constraints_path = constraints_dir / "sample_constraints.yaml"
        constraints = load_constraints(constraints_path)

        # Step 4: Generate the meal plan
        meal_plan = generate_meal_plan(profile, recipes, constraints)

        # Step 5: Save the meal plan
        output_path = save_meal_plan(meal_plan, plans_dir)

        # Success! Tell the user what happened
        print()
        print("=" * 70)
        print("✨ Success! Your meal plan is ready!")
        print("=" * 70)
        print()
        print(f"📄 View your meal plan: {output_path}")
        print()
        print("Next steps:")
        print("  1. Open the meal plan file to see your weekly schedule")
        print("  2. Add more recipes to the recipes/ folder for more variety")
        print("  3. Try creating a different profile in profiles/")
        print("  4. Adjust constraints in constraints/sample_constraints.yaml")
        print()

    except FileNotFoundError as e:
        print(f"❌ Error: Could not find required file: {e}")
        print("   Make sure all necessary files exist in their folders.")
    except Exception as e:
        print(f"❌ Error: Something went wrong: {e}")
        print("   Please check your input files and try again.")


# ==============================================================================
# SCRIPT ENTRY POINT
# ==============================================================================

# This special condition checks if this file is being run directly
# (not imported as a module by another script)
if __name__ == "__main__":
    main()
