#!/usr/bin/env python3
"""History Utilities for Meal Planning

This module handles tracking and managing meal plan history to:
- Prevent recipe repetition across weeks
- Support variety scoring
- Enable TTL (time-to-live) for history entries
- Track recipe usage patterns

Author: THC Meal Prep Planner Team
Created: 2026-01-18
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional


# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Default TTL for history entries (in days)
# History older than this will be ignored
DEFAULT_HISTORY_TTL_DAYS = 30

# History file format version for future compatibility
HISTORY_FILE_VERSION = "1.0"


# ==============================================================================
# HISTORY LOGGING FUNCTIONS
# ==============================================================================


def save_plan_to_history(
    meal_plan: dict[str, Any],
    history_dir: Path,
    ttl_days: int = DEFAULT_HISTORY_TTL_DAYS,
) -> Path:
    """Save a meal plan to the history directory.
    
    This creates a JSON record of the meal plan for future reference.
    The history is used to prevent recipe repetition and track variety.
    
    Args:
        meal_plan: The meal plan dictionary to save
        history_dir: Directory where history files are stored
        ttl_days: Time-to-live for this history entry (default: 30 days)
        
    Returns:
        Path to the created history file
        
    Example:
        history_file = save_plan_to_history(
            meal_plan,
            Path("history/"),
            ttl_days=30
        )
        print(f"Saved history to {history_file}")
    """
    # Ensure history directory exists
    history_dir.mkdir(parents=True, exist_ok=True)
    
    # Create history entry with metadata
    history_entry = {
        "version": HISTORY_FILE_VERSION,
        "created_at": datetime.now().isoformat(),
        "ttl_days": ttl_days,
        "expires_at": (datetime.now() + timedelta(days=ttl_days)).isoformat(),
        "week_start": meal_plan.get("week_start"),
        "week_end": meal_plan.get("week_end"),
        "profile_name": meal_plan.get("profile_name"),
        "meals": {},
    }
    
    # Extract recipe information from the meal plan
    for day_name, meals in meal_plan.get("week", {}).items():
        history_entry["meals"][day_name] = {}
        for meal_type, recipe in meals.items():
            # Store key recipe information
            history_entry["meals"][day_name][meal_type] = {
                "title": recipe.get("title"),
                "filename": recipe.get("filename"),
                "category": recipe.get("Category"),
                "cuisine": recipe.get("Cuisine"),
            }
    
    # Create filename based on week start date
    week_start = meal_plan.get("week_start", datetime.now().strftime("%Y-%m-%d"))
    filename = f"history_{week_start}.json"
    history_path = history_dir / filename
    
    # Save to JSON file
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history_entry, f, indent=2, ensure_ascii=False)
    
    return history_path


# ==============================================================================
# HISTORY READING FUNCTIONS
# ==============================================================================


def load_history_entries(
    history_dir: Path,
    include_expired: bool = False,
) -> list[dict[str, Any]]:
    """Load all history entries from the history directory.
    
    This reads all JSON history files and optionally filters out expired ones.
    
    Args:
        history_dir: Directory containing history files
        include_expired: Whether to include expired history entries (default: False)
        
    Returns:
        List of history entry dictionaries, sorted by date (newest first)
        
    Example:
        history = load_history_entries(Path("history/"))
        print(f"Found {len(history)} recent meal plans")
    """
    if not history_dir.exists():
        return []
    
    entries = []
    now = datetime.now()
    
    # Read all JSON files in the history directory
    for history_file in history_dir.glob("history_*.json"):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                entry = json.load(f)
            
            # Check if entry is expired
            if not include_expired:
                expires_at_str = entry.get("expires_at")
                if expires_at_str:
                    expires_at = datetime.fromisoformat(expires_at_str)
                    if now > expires_at:
                        continue  # Skip expired entry
            
            entries.append(entry)
            
        except (json.JSONDecodeError, ValueError) as e:
            # Log warning but continue processing other files
            print(f"⚠️  Warning: Could not read history file {history_file.name}: {e}")
            continue
    
    # Sort by week_start date (newest first)
    entries.sort(
        key=lambda x: x.get("week_start", ""), 
        reverse=True
    )
    
    return entries


def get_recently_used_recipes(
    history_dir: Path,
    days_back: int = DEFAULT_HISTORY_TTL_DAYS,
) -> list[dict[str, Any]]:
    """Get list of recently used recipes from history.
    
    This retrieves all recipes used in the specified time period,
    useful for enforcing repeat separation constraints.
    
    Args:
        history_dir: Directory containing history files
        days_back: How many days back to look (default: 30)
        
    Returns:
        List of dictionaries with recipe info and usage dates
        
    Example:
        recent = get_recently_used_recipes(Path("history/"), days_back=14)
        for recipe in recent:
            print(f"{recipe['title']} used on {recipe['date']}")
    """
    entries = load_history_entries(history_dir, include_expired=False)
    recently_used = []
    cutoff_date = datetime.now() - timedelta(days=days_back)
    
    for entry in entries:
        week_start_str = entry.get("week_start")
        if not week_start_str:
            continue
        
        # Parse week start date
        try:
            week_start = datetime.strptime(week_start_str, "%Y-%m-%d")
        except ValueError:
            continue
        
        # Skip if too old
        if week_start < cutoff_date:
            continue
        
        # Extract all recipes from this week
        for day_name, meals in entry.get("meals", {}).items():
            for meal_type, recipe_info in meals.items():
                if recipe_info.get("filename"):
                    recently_used.append({
                        "title": recipe_info.get("title"),
                        "filename": recipe_info.get("filename"),
                        "category": recipe_info.get("category"),
                        "cuisine": recipe_info.get("cuisine"),
                        "date": week_start_str,
                        "day": day_name,
                        "meal_type": meal_type,
                    })
    
    return recently_used


def get_recipe_last_used(
    recipe_filename: str,
    history_dir: Path,
) -> Optional[str]:
    """Get the date when a recipe was last used.
    
    Args:
        recipe_filename: Filename of the recipe to check
        history_dir: Directory containing history files
        
    Returns:
        ISO date string of last use, or None if never used
        
    Example:
        last_used = get_recipe_last_used("breakfast-burritos.md", Path("history/"))
        if last_used:
            print(f"Recipe last used on {last_used}")
    """
    recent_recipes = get_recently_used_recipes(history_dir)
    
    # Find the most recent use of this recipe
    for recipe in recent_recipes:
        if recipe.get("filename") == recipe_filename:
            return recipe.get("date")
    
    return None


def days_since_recipe_used(
    recipe_filename: str,
    history_dir: Path,
    reference_date: Optional[datetime] = None,
) -> Optional[int]:
    """Calculate how many days since a recipe was last used.
    
    Args:
        recipe_filename: Filename of the recipe to check
        history_dir: Directory containing history files
        reference_date: Reference date (default: today)
        
    Returns:
        Number of days since last use, or None if never used
        
    Example:
        days = days_since_recipe_used("breakfast-burritos.md", Path("history/"))
        if days and days < 7:
            print("Recipe was used recently, consider variety")
    """
    last_used_str = get_recipe_last_used(recipe_filename, history_dir)
    if not last_used_str:
        return None
    
    if reference_date is None:
        reference_date = datetime.now()
    
    try:
        last_used = datetime.strptime(last_used_str, "%Y-%m-%d")
        delta = reference_date - last_used
        return delta.days
    except ValueError:
        return None
