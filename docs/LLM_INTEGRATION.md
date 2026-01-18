# LLM Integration Guide

This guide explains how to use the LLM (Large Language Model) integration in the THC Meal Prep Planner.

## Overview

The meal plan generator can optionally use OpenAI's GPT models to provide creative meal suggestions while ensuring all suggestions comply with your constraints and preferences.

## How It Works

### Architecture

The LLM integration follows a **hybrid approach**:

1. **LLM Generates Ideas**: GPT suggests creative meal names based on:
   - User dietary restrictions and preferences
   - Time constraints (weeknight vs weekend)
   - Recently used meals (to avoid repetition)
   - Meal type (breakfast, lunch, dinner)

2. **Code Enforces Rules**: All suggestions must pass validation:
   - Time constraints (max prep time)
   - Recipe availability in the database
   - Variety requirements (no repetition)
   - Category matching (breakfast/lunch/dinner)

3. **Graceful Fallback**: If LLM is unavailable or fails:
   - The system automatically falls back to deterministic recipe selection
   - No functionality is lost
   - Users are notified of the LLM status

### Key Features

- ✅ **Secure**: API key stored in environment variables or GitHub secrets
- ✅ **Optional**: Works perfectly without LLM features
- ✅ **Safe**: All suggestions validated against hard constraints
- ✅ **Robust**: Comprehensive error handling with graceful degradation
- ✅ **Transparent**: Clear status messages about LLM availability

## Setup Instructions

### Local Development

1. **Obtain an OpenAI API Key**
   - Go to [OpenAI Platform](https://platform.openai.com/)
   - Sign up or log in
   - Navigate to API Keys section
   - Create a new API key
   - Copy the key (starts with `sk-`)

2. **Set the Environment Variable**

   **Linux/macOS:**
   ```bash
   export OPENAI_API_KEY="sk-your-api-key-here"
   ```

   **Windows (PowerShell):**
   ```powershell
   $env:OPENAI_API_KEY="sk-your-api-key-here"
   ```

   **Windows (Command Prompt):**
   ```cmd
   set OPENAI_API_KEY=sk-your-api-key-here
   ```

3. **Verify Installation**
   ```bash
   pip install -r requirements.txt
   python scripts/generate_meal_plan.py
   ```

   You should see: `🤖 LLM-powered suggestions: ENABLED`

### GitHub Actions

To enable LLM features in CI/CD workflows:

1. **Add Repository Secret**
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key (e.g., `sk-...`)
   - Click **Add secret**

2. **Workflow Configuration**
   
   The workflow is already configured in `.github/workflows/ci.yml`:
   
   ```yaml
   env:
     OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
   ```

3. **Verify in Workflow Runs**
   
   Check the workflow logs for:
   ```
   🤖 LLM-powered suggestions: ENABLED
   ```

## Usage

### Running with LLM

When the API key is configured, the generator will:

```bash
python scripts/generate_meal_plan.py
```

Sample output:
```
======================================================================
🍽️  THC Meal Prep Planner - Meal Plan Generator
======================================================================

🤖 LLM-powered suggestions: ENABLED

📋 Loading profile from ashuah.md...
📖 Loading recipes from /home/runner/work/thc-meal-prep-planner/thc-meal-prep-planner/recipes...
   Found 5 recipe(s)
⚙️  Loading constraints from sample_constraints.yaml...

🎯 Generating meal plan...
   🤖 LLM suggested 'Veggie Scramble', matched with recipe: Vegetable Scramble
   🤖 LLM suggested 'Chicken Teriyaki Bowl' (no matching recipe, using: Grilled Chicken)
   ✅ Meal plan generated successfully!
```

### Running without LLM

Simply don't set the API key:

```bash
unset OPENAI_API_KEY
python scripts/generate_meal_plan.py
```

Output will show:
```
🔒 LLM-powered suggestions: DISABLED (no API key configured)
```

The generator will use random selection from available recipes.

## Technical Details

### LLM Module (`scripts/llm_utils.py`)

#### Main Functions

1. **`is_llm_available() -> bool`**
   - Checks if OpenAI package is installed and API key is set
   - Used to determine if LLM features can be used

2. **`get_openai_client() -> Optional[OpenAI]`**
   - Creates and returns OpenAI client
   - Returns None if unavailable
   - Handles initialization errors gracefully

3. **`get_meal_suggestion(...) -> Optional[str]`**
   - Main function for getting LLM suggestions
   - Returns meal name or None
   - Parameters:
     - `meal_type`: "breakfast", "lunch", or "dinner"
     - `profile`: User profile dictionary
     - `constraints`: Constraint dictionary
     - `is_weeknight`: Boolean for weeknight vs weekend
     - `recently_used_meals`: List of recent meal names

4. **`get_llm_status_message() -> str`**
   - Returns user-friendly status message
   - Useful for displaying LLM availability to users

### Integration in Meal Generator

The `select_meal_with_llm()` function in `generate_meal_plan.py`:

1. Filters recipes by constraints (hard rules)
2. Attempts to get LLM suggestion
3. Tries to match LLM suggestion with available recipes
4. Falls back to random selection if no match
5. Returns compliant recipe or None

## Configuration

### LLM Settings

Edit `scripts/llm_utils.py` to customize:

```python
# Model to use (default: gpt-3.5-turbo)
DEFAULT_MODEL = "gpt-3.5-turbo"

# Max tokens in response (default: 150)
MAX_TOKENS = 150

# Temperature/creativity (0.0-1.0, default: 0.7)
TEMPERATURE = 0.7
```

### Cost Optimization

To minimize API costs:

1. **Use gpt-3.5-turbo**: Much cheaper than GPT-4
2. **Low MAX_TOKENS**: We only need meal names (150 tokens)
3. **Smart Caching**: LLM only called when generating new plans
4. **Graceful Fallback**: No repeated calls on failure

### Prompt Engineering

The prompt template in `build_meal_suggestion_prompt()` provides:

- Clear context about meal type and time constraints
- Dietary restrictions and preferences
- Recently used meals to avoid
- Instruction for concise, practical responses

Example prompt:
```
You are a creative meal planning assistant. Suggest a dinner meal idea.

Context:
- Meal type: dinner
- Day type: weeknight
- Maximum preparation time: 45 minutes
- Dietary restrictions: None
- Food preferences: Mediterranean cuisine

Recently used meals (please avoid): Pasta Carbonara, Grilled Salmon

Please suggest ONE specific meal name only. Keep it simple and practical.
Format: Just the meal name, nothing else.
Example: "Chicken Teriyaki with Rice" or "Veggie Omelet"

Meal suggestion:
```

## Security Best Practices

### ✅ DO:
- Store API key in environment variables
- Use GitHub secrets for CI/CD
- Add `.env` files to `.gitignore`
- Rotate API keys regularly
- Monitor API usage on OpenAI dashboard

### ❌ DON'T:
- Commit API keys to version control
- Share API keys in plain text
- Use API keys in client-side code
- Log API keys in application logs

## Troubleshooting

### Issue: "LLM-powered suggestions: DISABLED (OpenAI package not installed)"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "LLM-powered suggestions: DISABLED (no API key configured)"

**Solution:**
```bash
export OPENAI_API_KEY="sk-your-key"
```

### Issue: "Warning: LLM suggestion failed: Connection error"

**Possible causes:**
- No internet connection
- OpenAI API is down
- Invalid API key
- API rate limit exceeded

**Solution:**
The script will continue with deterministic selection. Check:
1. Internet connectivity
2. API key validity
3. OpenAI status page
4. API usage limits

### Issue: LLM suggestions don't match any recipes

**Expected behavior:**
The system will note the suggestion but use a random recipe:
```
🤖 LLM suggested 'Exotic Dish' (no matching recipe, using: Available Recipe)
```

**To improve matching:**
1. Add more recipes to your database
2. The LLM will learn from your recipe names over time
3. Matching is fuzzy (checks for word overlap)

## Future Enhancements

Potential improvements:

- [ ] Fine-tune prompt based on user feedback
- [ ] Add semantic search for better recipe matching
- [ ] Cache LLM responses to reduce API calls
- [ ] Support for custom LLM providers (Azure OpenAI, Anthropic)
- [ ] A/B testing of prompts for better suggestions
- [ ] User feedback loop to improve suggestions

## FAQs

**Q: Is the OpenAI API key required?**
A: No, the meal planner works perfectly without it. LLM is an optional enhancement.

**Q: What does the LLM integration cost?**
A: Using gpt-3.5-turbo with our settings costs approximately $0.002 per meal plan (assuming 21 meals). Very affordable!

**Q: Can I use a different LLM provider?**
A: Currently only OpenAI is supported, but the design allows for easy extension to other providers.

**Q: Does the LLM have access to my recipes?**
A: No, the LLM only sees generic information (meal type, constraints, preferences). Recipe matching happens locally.

**Q: What happens if the LLM suggests something I can't make?**
A: The system validates all suggestions against your available recipes and constraints. Invalid suggestions are ignored.

## Support

For issues or questions:
1. Check this documentation
2. Review the code comments in `scripts/llm_utils.py`
3. Open an issue on GitHub

---

**Last Updated**: 2026-01-18
**Version**: 1.0
