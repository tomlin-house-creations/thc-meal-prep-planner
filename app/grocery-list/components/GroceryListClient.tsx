'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import type { GroceryList, GroceryItem } from '@/lib/meals';

interface GroceryListClientProps {
  initialGroceryList: GroceryList | null;
}

export default function GroceryListClient({ initialGroceryList }: GroceryListClientProps) {
  const [checkedItems, setCheckedItems] = useState<{ [key: string]: boolean }>({});
  const [isLoading, setIsLoading] = useState(true);

  // Load checked state from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('groceryChecklist');
    if (saved) {
      try {
        setCheckedItems(JSON.parse(saved));
      } catch (error) {
        console.error('Error loading checked items:', error);
      }
    }
    setIsLoading(false);
  }, []);

  // Save checked state to localStorage whenever it changes
  useEffect(() => {
    if (!isLoading) {
      try {
        localStorage.setItem('groceryChecklist', JSON.stringify(checkedItems));
      } catch (error) {
        console.error('Error saving checked items:', error);
      }
    }
  }, [checkedItems, isLoading]);

  const handleToggle = (itemKey: string) => {
    setCheckedItems(prev => ({
      ...prev,
      [itemKey]: !prev[itemKey],
    }));
  };

  const handleClearAll = () => {
    // TODO: Replace native confirm with a custom modal component for better UX
    if (confirm('Clear all checked items? This cannot be undone.')) {
      setCheckedItems({});
    }
  };

  const getProgress = () => {
    if (!initialGroceryList) return { checked: 0, total: 0, percentage: 0 };
    
    let total = 0;
    let checked = 0;
    
    // Create a set of valid item keys from current grocery list
    const validKeys = new Set<string>();
    Object.entries(initialGroceryList.categories).forEach(([category, items]) => {
      items.forEach((_, index) => {
        const itemKey = `${category}-${index}`;
        validKeys.add(itemKey);
      });
      total += items.length;
    });
    
    // Only count checked items that exist in current grocery list
    Object.entries(checkedItems).forEach(([key, isChecked]) => {
      if (isChecked && validKeys.has(key)) {
        checked++;
      }
    });
    
    return {
      checked,
      total,
      percentage: total > 0 ? Math.round((checked / total) * 100) : 0,
    };
  };

  const progress = getProgress();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-teal-50 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <p className="text-gray-600 dark:text-gray-300">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-teal-50 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 dark:text-white mb-2">
            🛒 Grocery List
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Check off items as you shop
          </p>
        </header>

        {/* Navigation */}
        <nav className="mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/"
                className="px-6 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition-colors text-center"
              >
                <span aria-hidden="true">📅</span> Meal Plan
              </Link>
              <Link
                href="/grocery-list"
                className="px-6 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors text-center"
              >
                <span aria-hidden="true">🛒</span> Grocery List
              </Link>
            </div>
          </div>
        </nav>

        {initialGroceryList ? (
          <div className="space-y-6">
            {/* Progress Bar */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
              <div className="flex justify-between items-center mb-2">
                <h2 className="text-lg font-semibold text-gray-800 dark:text-white">
                  Shopping Progress
                </h2>
                <span className="text-sm text-gray-600 dark:text-gray-300">
                  {progress.checked} / {progress.total} items
                </span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 overflow-hidden">
                <div
                  className="bg-green-600 h-4 transition-all duration-300 ease-out"
                  style={{ width: `${progress.percentage}%` }}
                  role="progressbar"
                  aria-valuenow={progress.percentage}
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-label="Shopping progress"
                />
              </div>
              <p className="text-center mt-2 text-sm text-gray-600 dark:text-gray-300">
                {progress.percentage}% complete
              </p>
            </div>

            {/* Clear Button */}
            {progress.checked > 0 && (
              <div className="flex justify-end">
                <button
                  onClick={handleClearAll}
                  className="px-4 py-2 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition-colors text-sm"
                >
                  Clear All Checked
                </button>
              </div>
            )}

            {/* Categories */}
            {Object.entries(initialGroceryList.categories).map(([category, items]) => (
              <div
                key={category}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6"
              >
                <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4 border-b-2 border-gray-200 dark:border-gray-700 pb-2">
                  {category}
                </h3>
                <div className="space-y-2">
                  {items.map((item, index) => {
                    const itemKey = `${category}-${index}`;
                    const isChecked = checkedItems[itemKey] || false;
                    
                    return (
                      <label
                        key={itemKey}
                        className={`flex items-center p-3 rounded-lg cursor-pointer transition-colors ${
                          isChecked
                            ? 'bg-green-100 dark:bg-green-900/30'
                            : 'hover:bg-gray-100 dark:hover:bg-gray-700'
                        }`}
                      >
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => handleToggle(itemKey)}
                          className="w-5 h-5 text-green-600 rounded focus:ring-2 focus:ring-green-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 cursor-pointer"
                        />
                        <span
                          className={`ml-3 text-gray-800 dark:text-white ${
                            isChecked ? 'line-through opacity-60' : ''
                          }`}
                        >
                          {item.item}
                        </span>
                      </label>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 text-center">
            <p className="text-gray-600 dark:text-gray-300 text-lg">
              No grocery list available yet.
            </p>
            <p className="text-gray-500 dark:text-gray-400 text-sm mt-2">
              Generate a meal plan to create your grocery list.
            </p>
          </div>
        )}

        {/* Info Footer */}
        <div className="mt-8 bg-blue-100 dark:bg-blue-900/30 rounded-lg p-4">
          <p className="text-sm text-blue-800 dark:text-blue-200 text-center">
            ℹ️ Your checked items are saved automatically in your browser's local storage
          </p>
        </div>

        {/* Footer */}
        <footer className="mt-8 text-center text-gray-500 dark:text-gray-400 text-sm">
          <p>
            Built with Next.js • Mobile-first design • Data stored in localStorage
          </p>
        </footer>
      </div>
    </div>
  );
}
