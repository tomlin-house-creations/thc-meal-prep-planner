# Website Development Guide

This guide explains how to develop and work with the Next.js static website for the THC Meal Prep Planner.

## Overview

The website is built with:
- **Next.js 16** - React framework with static export capability
- **React 19** - UI library
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS v4** - Utility-first CSS framework
- **gray-matter** - Markdown front-matter parser

The site reads meal plans and grocery lists from the `/plans` directory and displays them in a mobile-friendly interface.

## Prerequisites

- Node.js 18 or higher
- npm (comes with Node.js)

## Installation

From the repository root:

```bash
# Install dependencies
npm install
```

## Development

### Running the Development Server

```bash
npm run dev
```

The development server will start at `http://localhost:3000`. The site will automatically reload when you make changes to the code.

**Note**: For local development, the basePath is empty by default. To test with the GitHub Pages basePath:

```bash
NEXT_PUBLIC_BASE_PATH=/thc-meal-prep-planner npm run dev
```

### Project Structure

```
/
├── app/                          # Next.js App Router pages
│   ├── layout.tsx               # Root layout component
│   ├── page.tsx                 # Home page (meal plan viewer)
│   ├── globals.css              # Global styles
│   └── grocery-list/            # Grocery list page
│       ├── page.tsx             # Server component (data fetching)
│       └── components/
│           └── GroceryListClient.tsx  # Client component (interactive UI)
├── lib/
│   └── meals.ts                 # Utilities for parsing meal plans/grocery lists
├── plans/                        # Markdown files (meal plans & grocery lists)
├── next.config.ts               # Next.js configuration
├── tailwind.config.ts           # Tailwind CSS configuration
├── tsconfig.json                # TypeScript configuration
└── package.json                 # Dependencies and scripts
```

## Building for Production

### Static Export

The site is configured for static export, which generates HTML files that can be hosted on GitHub Pages or any static hosting service.

```bash
# Build the static site
npm run build
```

This creates an `out/` directory with all static files ready for deployment.

### Testing the Production Build

You can test the production build locally using a simple HTTP server:

```bash
# Using Python
python3 -m http.server -d out 8000

# Using Node.js http-server (install with: npm install -g http-server)
npx http-server out -p 8000
```

Then visit `http://localhost:8000` in your browser.

## How It Works

### Data Flow

1. **Meal Plans**: The site reads `/plans/meal_plan_*.md` files
2. **Grocery Lists**: The site reads `/plans/grocery_list_*.md` files
3. **Parsing**: The `lib/meals.ts` module parses Markdown and extracts structured data
4. **Rendering**: React components render the data in a mobile-friendly UI
5. **State**: Grocery list checkboxes save state to browser localStorage

### Server vs Client Components

- **Server Components** (default): Run at build time, can access the file system
  - `app/page.tsx` - Fetches meal plan data
  - `app/grocery-list/page.tsx` - Fetches grocery list data
  
- **Client Components** (`'use client'`): Run in the browser, can use hooks and interactivity
  - `app/grocery-list/components/GroceryListClient.tsx` - Interactive checklist with localStorage

### Responsive Design

The UI is mobile-first and responsive:
- **Mobile**: Single column layout, touch-friendly checkboxes
- **Tablet**: Optimized spacing, larger touch targets
- **Desktop**: Multi-column meal display, optimized reading width

## Key Features

### Meal Plan Viewer

- Displays the latest weekly meal plan from `/plans`
- Shows breakfast, lunch, and dinner for each day
- Includes prep time, cook time, and total time
- Mobile-responsive card layout

### Grocery List Checklist

- Interactive checklist with localStorage persistence
- Progress bar showing completion percentage
- Categories (Produce, Dairy, Pantry, etc.)
- "Clear All Checked" functionality
- Checked items are saved automatically in the browser

### Dark Mode

The site supports both light and dark themes based on system preferences:
- Uses CSS custom properties for theming
- Automatically switches based on `prefers-color-scheme`

## Configuration

### GitHub Pages

The site is configured for GitHub Pages deployment with:

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  output: "export",                                  // Enable static export
  basePath: process.env.NODE_ENV === "production" 
    ? "/thc-meal-prep-planner" 
    : "",                                            // GitHub Pages subdirectory
  images: {
    unoptimized: true,                              // Required for static export
  },
  trailingSlash: true,                              // Add trailing slashes to URLs
};
```

### Tailwind CSS

Tailwind v4 is configured with:
- Support for dark mode via `prefers-color-scheme`
- Custom color scheme using CSS variables
- PostCSS integration via `@tailwindcss/postcss`

## Common Tasks

### Adding a New Page

1. Create a new directory under `app/`:
   ```bash
   mkdir app/my-page
   ```

2. Add a `page.tsx` file:
   ```tsx
   export default function MyPage() {
     return <div>My Page Content</div>;
   }
   ```

3. The page will be available at `/my-page`

### Styling Components

Use Tailwind utility classes:

```tsx
<div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
  <h2 className="text-2xl font-bold text-gray-800 dark:text-white">
    Title
  </h2>
</div>
```

### Parsing New Markdown Formats

Update `lib/meals.ts` to add new parsing functions:

```typescript
export function parseNewFormat(filename: string) {
  const fullPath = path.join(plansDirectory, filename);
  const fileContents = fs.readFileSync(fullPath, 'utf8');
  const { data, content } = matter(fileContents);
  // Your parsing logic here
  return parsedData;
}
```

## Troubleshooting

### Build Errors

**Error: Module not found: Can't resolve 'fs'**
- Solution: Make sure server-side code (using fs, path) is in Server Components, not Client Components
- Client Components must have `'use client'` at the top
- Server Components should NOT import client-only hooks (useState, useEffect)

**Error: Tailwind CSS PostCSS plugin**
- Solution: Make sure `@tailwindcss/postcss` is installed and configured in `postcss.config.mjs`

### Development Issues

**Changes not reflecting**
- Hard refresh: `Cmd/Ctrl + Shift + R`
- Clear Next.js cache: `rm -rf .next`
- Restart dev server: `npm run dev`

**localStorage not working**
- localStorage only works in the browser (Client Components)
- Check browser console for errors
- Verify the browser supports localStorage

## Deployment

See the [GitHub Pages Deployment Guide](../docs/DEPLOYMENT.md) for deployment instructions.

## Further Reading

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
