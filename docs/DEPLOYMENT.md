# Deployment Guide

This guide explains how to deploy the THC Meal Prep Planner website to GitHub Pages.

## Automatic Deployment (Recommended)

The repository is configured to automatically deploy to GitHub Pages when changes are pushed to the `main` branch.

### Setup GitHub Pages

1. Go to your repository settings
2. Navigate to **Pages** (under "Code and automation")
3. Under "Build and deployment":
   - Source: **GitHub Actions**
4. Save the settings

That's it! The `.github/workflows/deploy-pages.yml` workflow will automatically:
- Build the Next.js site when you push to `main`
- Deploy the static files to GitHub Pages
- Make the site available at: `https://tomlin-house-creations.github.io/thc-meal-prep-planner/`

### Triggering a Deployment

Deployments happen automatically when:
- You push commits to the `main` branch
- You can also manually trigger via **Actions** → **Deploy to GitHub Pages** → **Run workflow**

### Viewing Deployment Status

1. Go to the **Actions** tab in your repository
2. Click on the latest "Deploy to GitHub Pages" workflow run
3. You'll see the build and deploy steps

## Manual Deployment

If you need to deploy manually:

### Step 1: Build the Site

```bash
npm run build
```

This creates an `out/` directory with all static files.

### Step 2: Deploy with GitHub Pages Action

The workflow handles this automatically, but if deploying manually:

```bash
# The out/ directory contains the built site
# Upload these files to your hosting provider
```

## Local Testing

Before deploying, test the production build locally:

```bash
# Build the site
npm run build

# Serve the build
python3 -m http.server -d out 8080

# Visit http://localhost:8080
```

Note: When testing locally, the basePath won't match, so navigation links will include `/thc-meal-prep-planner/`. This is expected and works correctly on GitHub Pages.

## Configuration

The site is configured for GitHub Pages in `next.config.ts`:

```typescript
const nextConfig: NextConfig = {
  output: "export",                              // Static export
  basePath: process.env.NEXT_PUBLIC_BASE_PATH || "",  // GitHub Pages subdirectory
  images: {
    unoptimized: true,                           // Required for static export
  },
  trailingSlash: true,                           // Add trailing slashes
};
```

The `NEXT_PUBLIC_BASE_PATH` environment variable is set in the GitHub Actions workflow to `/thc-meal-prep-planner`. For local development, it defaults to empty string.

### Custom Domain (Optional)

To use a custom domain:

1. Add a `CNAME` file to the `public/` directory with your domain
2. Configure DNS settings with your domain provider
3. Update `basePath` in `next.config.ts` to `""`

## Troubleshooting

### Deployment Failed

Check the Actions tab for error details. Common issues:

- **Build errors**: Fix TypeScript/build errors locally first
- **Permission errors**: Ensure the workflow has write permissions (Settings → Actions → Workflow permissions)

### Site Not Loading

- Verify GitHub Pages is enabled in repository settings
- Check that the deployment was successful in Actions
- Clear browser cache and try again
- Ensure the URL includes the basePath: `/thc-meal-prep-planner/`

### CSS/JS Not Loading

- This usually means the basePath is incorrect
- Verify `next.config.ts` has the correct repository name
- Check browser console for 404 errors

### Meal Plans Not Showing

The site reads from `/plans` directory:
- Ensure `meal_plan_*.md` files exist in the `plans/` folder
- Run `python scripts/generate_meal_plan.py` to create meal plans
- Rebuild and redeploy the site

## Updating Content

To update meal plans and redeploy:

```bash
# Generate new meal plans
python scripts/generate_meal_plan.py

# Commit and push
git add plans/
git commit -m "Update meal plans"
git push origin main

# GitHub Actions will automatically rebuild and deploy
```

## Cost

GitHub Pages is free for public repositories and includes:
- Unlimited bandwidth
- Custom domains (optional)
- HTTPS support

For private repositories, GitHub Pages is available on GitHub Pro, Team, and Enterprise plans.
