import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const plansDirectory = path.join(process.cwd(), 'plans');

export interface MealPlanDay {
  day: string;
  breakfast?: {
    name: string;
    prepTime?: string;
    cookTime?: string;
    totalTime?: string;
  };
  lunch?: {
    name: string;
    prepTime?: string;
    cookTime?: string;
    totalTime?: string;
  };
  dinner?: {
    name: string;
    prepTime?: string;
    cookTime?: string;
    totalTime?: string;
  };
}

export interface MealPlan {
  title: string;
  weekOf: string;
  generatedOn?: string;
  days: MealPlanDay[];
  rawContent: string;
}

export interface GroceryItem {
  item: string;
  checked: boolean;
}

export interface GroceryList {
  categories: {
    [category: string]: GroceryItem[];
  };
  rawContent: string;
}

/**
 * Get the latest meal plan from the plans directory
 */
export function getLatestMealPlan(): MealPlan | null {
  try {
    const files = fs.readdirSync(plansDirectory);
    const mealPlanFiles = files
      .filter(file => file.startsWith('meal_plan_') && file.endsWith('.md'))
      .sort()
      .reverse();

    if (mealPlanFiles.length === 0) {
      return null;
    }

    const latestFile = mealPlanFiles[0];
    return getMealPlan(latestFile);
  } catch (error) {
    console.error('Error reading meal plans:', error);
    return null;
  }
}

/**
 * Get a specific meal plan by filename
 */
export function getMealPlan(filename: string): MealPlan | null {
  try {
    const fullPath = path.join(plansDirectory, filename);
    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const { data, content } = matter(fileContents);

    // Parse the markdown content
    const lines = content.split('\n');
    const days: MealPlanDay[] = [];
    let currentDay: MealPlanDay | null = null;
    let currentMeal: 'breakfast' | 'lunch' | 'dinner' | null = null;

    // Extract title and week info from first few lines
    let title = 'Weekly Meal Plan';
    let weekOf = '';
    let generatedOn = '';

    for (const line of lines) {
      // Extract title
      if (line.startsWith('# Weekly Meal Plan')) {
        const match = line.match(/# Weekly Meal Plan for (.+)/);
        if (match) {
          title = `Weekly Meal Plan for ${match[1]}`;
        }
      }

      // Extract week of date
      if (line.includes('**Week of')) {
        const match = line.match(/\*\*Week of (.+) to (.+)\*\*/);
        if (match) {
          weekOf = match[1];
        }
      }

      // Extract generated on date
      if (line.includes('- Generated on:')) {
        generatedOn = line.replace('- Generated on:', '').trim();
      }

      // New day section
      if (line.startsWith('## ') && !line.includes('Meal Plan Quality') && !line.includes('Plan Information')) {
        if (currentDay) {
          days.push(currentDay);
        }
        const dayName = line.replace('## ', '').trim();
        currentDay = { day: dayName };
        currentMeal = null;
      }

      // Meal type
      if (currentDay && line.startsWith('### ')) {
        const mealType = line.replace('### ', '').trim().toLowerCase();
        if (mealType === 'breakfast' || mealType === 'lunch' || mealType === 'dinner') {
          currentMeal = mealType;
        }
      }

      // Helper function to check if a line is a recipe name (not a metadata line)
      const isRecipeName = (line: string): boolean => {
        if (!line.startsWith('**')) return false;
        const excludedKeywords = ['No ', 'Prep Time', 'Cook Time', 'Total Time'];
        return !excludedKeywords.some(keyword => line.includes(keyword));
      };

      // Recipe name
      if (currentDay && currentMeal && isRecipeName(line)) {
        const recipeName = line.replace(/\*\*/g, '').trim();
        if (recipeName && !currentDay[currentMeal]) {
          currentDay[currentMeal] = { name: recipeName };
        }
      }

      // Time info
      if (currentDay && currentMeal && currentDay[currentMeal]) {
        if (line.includes('- Prep Time:')) {
          currentDay[currentMeal]!.prepTime = line.replace('- Prep Time:', '').trim();
        }
        if (line.includes('- Cook Time:')) {
          currentDay[currentMeal]!.cookTime = line.replace('- Cook Time:', '').trim();
        }
        if (line.includes('- Total Time:')) {
          currentDay[currentMeal]!.totalTime = line.replace('- Total Time:', '').trim();
        }
      }
    }

    if (currentDay) {
      days.push(currentDay);
    }

    return {
      title,
      weekOf,
      generatedOn,
      days,
      rawContent: content,
    };
  } catch (error) {
    console.error('Error reading meal plan:', error);
    return null;
  }
}

/**
 * Get the latest grocery list from the plans directory
 */
export function getLatestGroceryList(): GroceryList | null {
  try {
    const files = fs.readdirSync(plansDirectory);
    const groceryFiles = files
      .filter(file => file.startsWith('grocery_list_') && file.endsWith('.md'))
      .sort()
      .reverse();

    if (groceryFiles.length === 0) {
      return null;
    }

    const latestFile = groceryFiles[0];
    return getGroceryList(latestFile);
  } catch (error) {
    console.error('Error reading grocery lists:', error);
    return null;
  }
}

/**
 * Get a specific grocery list by filename
 */
export function getGroceryList(filename: string): GroceryList | null {
  try {
    const fullPath = path.join(plansDirectory, filename);
    const fileContents = fs.readFileSync(fullPath, 'utf8');
    const { content } = matter(fileContents);

    const lines = content.split('\n');
    const categories: { [category: string]: GroceryItem[] } = {};
    let currentCategory = '';

    for (const line of lines) {
      // Category header (## followed by category name)
      if (line.startsWith('## ') && !line.includes('Grocery List')) {
        currentCategory = line.replace('## ', '').trim();
        if (!categories[currentCategory]) {
          categories[currentCategory] = [];
        }
      }

      // Grocery item (- [ ] followed by item)
      if (line.startsWith('- [ ]') && currentCategory) {
        const item = line.replace('- [ ]', '').trim();
        if (item) {
          categories[currentCategory].push({
            item,
            checked: false,
          });
        }
      }
    }

    return {
      categories,
      rawContent: content,
    };
  } catch (error) {
    console.error('Error reading grocery list:', error);
    return null;
  }
}
