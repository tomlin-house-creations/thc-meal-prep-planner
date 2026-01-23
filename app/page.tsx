import Link from 'next/link';
import { getLatestMealPlan } from '@/lib/meals';

export default function Home() {
  const mealPlan: ReturnType<typeof getLatestMealPlan> = getLatestMealPlan();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 dark:text-white mb-2">
            🍽️ THC Meal Prep Planner
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Your weekly meal planning companion
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

        {/* Meal Plan Content */}
        {mealPlan ? (
          <div className="space-y-6">
            {/* Week Info */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
              <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-2">
                {mealPlan.title}
              </h2>
              {mealPlan.weekOf && (
                <p className="text-gray-600 dark:text-gray-300">
                  Week of {mealPlan.weekOf}
                </p>
              )}
            </div>

            {/* Days */}
            {mealPlan.days.map((day, index) => (
              <div
                key={index}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6"
              >
                <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-4 border-b-2 border-gray-200 dark:border-gray-700 pb-2">
                  {day.day}
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Breakfast */}
                  <div className="space-y-2">
                    <h4 className="font-semibold text-indigo-600 dark:text-indigo-400">
                      🌅 Breakfast
                    </h4>
                    {day.breakfast ? (
                      <div>
                        <p className="font-medium text-gray-800 dark:text-white">
                          {day.breakfast.name}
                        </p>
                        {day.breakfast.totalTime && (
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            ⏱️ {day.breakfast.totalTime}
                          </p>
                        )}
                      </div>
                    ) : (
                      <p className="text-sm text-gray-500 dark:text-gray-400 italic">
                        No recipe planned
                      </p>
                    )}
                  </div>

                  {/* Lunch */}
                  <div className="space-y-2">
                    <h4 className="font-semibold text-green-600 dark:text-green-400">
                      🌞 Lunch
                    </h4>
                    {day.lunch ? (
                      <div>
                        <p className="font-medium text-gray-800 dark:text-white">
                          {day.lunch.name}
                        </p>
                        {day.lunch.totalTime && (
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            ⏱️ {day.lunch.totalTime}
                          </p>
                        )}
                      </div>
                    ) : (
                      <p className="text-sm text-gray-500 dark:text-gray-400 italic">
                        No recipe planned
                      </p>
                    )}
                  </div>

                  {/* Dinner */}
                  <div className="space-y-2">
                    <h4 className="font-semibold text-orange-600 dark:text-orange-400">
                      🌙 Dinner
                    </h4>
                    {day.dinner ? (
                      <div>
                        <p className="font-medium text-gray-800 dark:text-white">
                          {day.dinner.name}
                        </p>
                        {day.dinner.totalTime && (
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            ⏱️ {day.dinner.totalTime}
                          </p>
                        )}
                      </div>
                    ) : (
                      <p className="text-sm text-gray-500 dark:text-gray-400 italic">
                        No recipe planned
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 text-center">
            <p className="text-gray-600 dark:text-gray-300 text-lg">
              No meal plan available yet.
            </p>
            <p className="text-gray-500 dark:text-gray-400 text-sm mt-2">
              Generate a meal plan using the Python scripts to get started.
            </p>
          </div>
        )}

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
