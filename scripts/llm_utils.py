#!/usr/bin/env python3
"""LLM Utility Module for Meal Suggestions

This module provides utilities for integrating Large Language Models (LLMs)
into the meal planning process. It uses OpenAI's GPT models to generate
creative meal suggestions while ensuring compliance with hard constraints.

Key Features:
-------------
- Secure API key management via environment variables
- Prompt engineering optimized for meal suggestions
- Constraint-aware meal generation
- Graceful fallback when API is unavailable
- Comprehensive error handling

How It Works:
-------------
1. The LLM receives context about user preferences and constraints
2. It generates creative meal suggestions based on this context
3. The suggestions are validated against hard rules in the code
4. Only compliant suggestions are used in the meal plan

Environment Setup:
------------------
Set the OPENAI_API_KEY environment variable:
    export OPENAI_API_KEY="sk-..."

Or in GitHub Actions, add it as a repository secret:
    Settings -> Secrets and variables -> Actions -> New repository secret
    Name: OPENAI_API_KEY
    Value: sk-...

Then reference it in your workflow:
    env:
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

Author: THC Meal Prep Planner Team
Created: 2026-01-18
"""

import os
from typing import Any, Optional

# Try to import OpenAI, but don't fail if it's not available
# This allows the script to run without LLM features if the package isn't installed
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = None  # type: ignore


# ==============================================================================
# CONFIGURATION - Settings for the LLM integration
# ==============================================================================

# Default model to use for meal suggestions
# gpt-3.5-turbo is cost-effective and fast, suitable for meal planning tasks
DEFAULT_MODEL = "gpt-3.5-turbo"

# Maximum number of tokens in the response
# This controls the length of the LLM's suggestions
# For meal names, we don't need long responses
MAX_TOKENS = 150

# Temperature controls creativity (0.0 = deterministic, 1.0 = very creative)
# 0.7 provides a good balance between creativity and consistency
TEMPERATURE = 0.7

# Maximum length for user-provided strings to prevent prompt injection
# This limits the size of meal names, dietary restrictions, etc. in prompts
MAX_INPUT_LENGTH = 500


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================


def sanitize_input(text: str, max_length: int = MAX_INPUT_LENGTH) -> str:
    """Sanitize user-provided text before including in LLM prompts.
    
    This prevents prompt injection attacks and ensures safe input by:
    - Removing potentially harmful characters
    - Limiting input length
    - Normalizing whitespace
    
    Args:
        text: The text to sanitize
        max_length: Maximum allowed length (default: MAX_INPUT_LENGTH)
        
    Returns:
        Sanitized text safe for use in prompts
        
    Example:
        safe_text = sanitize_input("User's dietary preference")
        # Returns clean text without potentially harmful content
    """
    if not text:
        return ""
    
    # Convert to string and strip
    text = str(text).strip()
    
    # Limit length to prevent abuse
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove or escape potentially problematic characters
    # Keep alphanumeric, spaces, common punctuation, but remove control chars
    allowed_chars = set(
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        " .,;:!?-'\"()/&"
    )
    sanitized = "".join(c for c in text if c in allowed_chars)
    
    # Normalize whitespace
    sanitized = " ".join(sanitized.split())
    
    return sanitized


def is_llm_available() -> bool:
    """Check if LLM features are available.
    
    This checks two things:
    1. Is the OpenAI package installed?
    2. Is an API key configured?
    
    Returns:
        True if LLM can be used, False otherwise
        
    Example:
        if is_llm_available():
            suggestion = get_meal_suggestion(...)
        else:
            print("LLM features disabled - using deterministic selection")
    """
    # Check if OpenAI package is installed
    if not OPENAI_AVAILABLE:
        return False
    
    # Check if API key is configured
    api_key = os.environ.get("OPENAI_API_KEY")
    return api_key is not None and api_key.strip() != ""


def get_openai_client() -> Optional[OpenAI]:
    """Create and return an OpenAI client instance.
    
    This function safely creates an OpenAI client, handling cases where:
    - The OpenAI package is not installed
    - The API key is not configured
    - The API key is invalid
    
    Returns:
        OpenAI client if available, None otherwise
        
    Example:
        client = get_openai_client()
        if client:
            # Use the client
            response = client.chat.completions.create(...)
    """
    if not is_llm_available():
        return None
    
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        return client
    except Exception as e:
        print(f"⚠️  Warning: Failed to create OpenAI client: {e}")
        return None


def build_meal_suggestion_prompt(
    meal_type: str,
    profile: dict[str, Any],
    constraints: dict[str, Any],
    is_weeknight: bool,
    recently_used_meals: list[str],
) -> str:
    """Build a prompt for the LLM to generate meal suggestions.
    
    This function creates a detailed prompt that gives the LLM context about:
    - What meal type we need (breakfast, lunch, dinner)
    - User dietary preferences and restrictions
    - Time constraints (weeknight vs weekend)
    - Meals we've used recently (to avoid repetition)
    
    The prompt is engineered to get focused, practical responses from the LLM.
    
    Args:
        meal_type: Type of meal (breakfast, lunch, dinner)
        profile: User profile with preferences and restrictions
        constraints: Planning constraints (time limits, etc.)
        is_weeknight: True if planning for a weeknight, False for weekend
        recently_used_meals: List of meal names used recently
        
    Returns:
        A formatted prompt string ready to send to the LLM
        
    Example:
        prompt = build_meal_suggestion_prompt(
            "dinner",
            {"Name": "John", "Dietary Restrictions": "vegetarian"},
            {"time": {"max_weeknight_prep_minutes": 45}},
            True,
            ["Pasta Primavera", "Veggie Stir Fry"]
        )
    """
    # Extract time constraint
    time_constraints = constraints.get("time", {})
    if is_weeknight:
        max_time = time_constraints.get("max_weeknight_prep_minutes", 45)
        time_context = "weeknight"
    else:
        max_time = time_constraints.get("max_weekend_prep_minutes", 180)
        time_context = "weekend"
    
    # Extract and sanitize dietary info from profile
    dietary_restrictions = sanitize_input(
        profile.get("Dietary Restrictions", "None")
    )
    food_preferences = sanitize_input(
        profile.get("Food Preferences", "")
    )
    
    # Sanitize meal type
    meal_type_safe = sanitize_input(meal_type)
    
    # Build the prompt
    prompt = f"""You are a creative meal planning assistant. Suggest a {meal_type_safe} meal idea.

Context:
- Meal type: {meal_type}
- Day type: {time_context}
- Maximum preparation time: {max_time} minutes
- Dietary restrictions: {dietary_restrictions}
- Food preferences: {food_preferences}

"""
    
    # Add recently used meals to avoid repetition
    # Sanitize each meal name to prevent prompt injection
    if recently_used_meals:
        sanitized_meals = [sanitize_input(meal) for meal in recently_used_meals]
        # Filter out empty strings after sanitization
        sanitized_meals = [m for m in sanitized_meals if m]
        if sanitized_meals:
            prompt += f"Recently used meals (please avoid): {', '.join(sanitized_meals)}\n\n"
    
    prompt += """Please suggest ONE specific meal name only. Keep it simple and practical.
Format: Just the meal name, nothing else.
Example: "Chicken Teriyaki with Rice" or "Veggie Omelet"

Meal suggestion:"""
    
    return prompt


# ==============================================================================
# MAIN LLM FUNCTIONS
# ==============================================================================


def get_meal_suggestion(
    meal_type: str,
    profile: dict[str, Any],
    constraints: dict[str, Any],
    is_weeknight: bool,
    recently_used_meals: Optional[list[str]] = None,
) -> Optional[str]:
    """Get a meal suggestion from the LLM.
    
    This is the main function for getting LLM-powered meal suggestions.
    It handles the entire flow:
    1. Check if LLM is available
    2. Build an appropriate prompt
    3. Call the OpenAI API
    4. Extract and clean the response
    5. Handle errors gracefully
    
    The function always returns None if:
    - LLM is not available (no API key or package not installed)
    - An error occurs during the API call
    - The API returns an invalid response
    
    Args:
        meal_type: Type of meal to suggest (breakfast, lunch, dinner)
        profile: User profile dictionary
        constraints: Planning constraints dictionary
        is_weeknight: True for weeknight, False for weekend
        recently_used_meals: Optional list of meal names to avoid
        
    Returns:
        A meal name suggestion as a string, or None if unavailable/error
        
    Example:
        suggestion = get_meal_suggestion(
            "dinner",
            user_profile,
            planning_constraints,
            is_weeknight=True,
            recently_used_meals=["Pasta", "Tacos"]
        )
        
        if suggestion:
            print(f"LLM suggests: {suggestion}")
        else:
            print("Using deterministic recipe selection")
    """
    # Default to empty list if None
    if recently_used_meals is None:
        recently_used_meals = []
    
    # Check if LLM features are available
    client = get_openai_client()
    if not client:
        return None
    
    try:
        # Build the prompt
        prompt = build_meal_suggestion_prompt(
            meal_type,
            profile,
            constraints,
            is_weeknight,
            recently_used_meals,
        )
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful meal planning assistant. "
                               "Provide concise, practical meal suggestions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
        )
        
        # Extract the suggestion from the response
        if response.choices and len(response.choices) > 0:
            suggestion = response.choices[0].message.content
            if suggestion:
                # Clean up the suggestion more robustly
                # Remove various quote types and extra whitespace
                suggestion = suggestion.strip()
                # Remove common quote patterns
                for quote_char in ['"', "'", '"', '"', "'", "'"]:
                    suggestion = suggestion.strip(quote_char)
                # Final whitespace normalization
                suggestion = " ".join(suggestion.split())
                return suggestion if suggestion else None
        
        return None
        
    except Exception as e:
        # Log the error but don't crash - gracefully degrade to non-LLM mode
        print(f"⚠️  Warning: LLM suggestion failed: {e}")
        return None


def get_llm_status_message() -> str:
    """Get a user-friendly status message about LLM availability.
    
    This is useful for displaying to users so they know whether
    LLM features are active or not.
    
    Returns:
        A descriptive status message
        
    Example:
        print(get_llm_status_message())
        # Output: "🤖 LLM-powered suggestions: ENABLED"
        # or:     "🔒 LLM-powered suggestions: DISABLED (no API key)"
    """
    if not OPENAI_AVAILABLE:
        return "🔒 LLM-powered suggestions: DISABLED (OpenAI package not installed)"
    
    if not os.environ.get("OPENAI_API_KEY"):
        return "🔒 LLM-powered suggestions: DISABLED (no API key configured)"
    
    return "🤖 LLM-powered suggestions: ENABLED"
