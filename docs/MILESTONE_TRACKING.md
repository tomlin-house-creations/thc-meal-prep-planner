# Milestone Tracking Guide

This guide explains how to use the milestone tracking system for the THC Meal Prep Planner project.

## Overview

The milestone tracking system helps organize and monitor progress toward MVP, v1.0, and future releases. It consists of:

1. **[Project Roadmap](ROADMAP.md)**: Master document with all milestones
2. **[Product Requirements Document (PRD)](PRD.md)**: Detailed requirements and specifications
3. **GitHub Issues**: Individual milestone and task tracking
4. **Milestone Template**: Standardized format for milestone issues

## Document Hierarchy

```
PRD.md (What we're building and why)
  └── ROADMAP.md (When and how we're building it)
        └── GitHub Milestone Issues (Detailed tracking)
              └── GitHub Feature/Task Issues (Individual work items)
```

## Using the Roadmap

### Viewing Progress

1. Open [docs/ROADMAP.md](ROADMAP.md)
2. Check the "Progress Overview" section for current phase
3. Review phase-specific sections for detailed task lists
4. Look for `[x]` (completed) vs `[ ]` (pending) items

### Updating the Roadmap

1. Mark items as complete by changing `[ ]` to `[x]`
2. Update "Current Status" in each phase section
3. Update "Last Updated" date at bottom of document
4. Submit changes via pull request

## Creating Milestone Issues

### When to Create a Milestone Issue

Create a milestone issue when:
- Starting work on a new phase or major feature
- You need to track multiple related tasks
- The milestone involves multiple contributors
- Progress needs to be communicated to stakeholders

### How to Create a Milestone Issue

1. Go to GitHub Issues → New Issue
2. Select "Milestone Tracker" template
3. Fill in all sections:
   - **Milestone Name**: Descriptive name (e.g., "Phase 2: Repository Infrastructure")
   - **Target Date**: Realistic completion date or TBD
   - **Priority**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
   - **Phase**: MVP, v1.0, or Future
   - **Success Criteria**: Clear, measurable goals
   - **Task Checklist**: Specific tasks to complete
   - **Dependencies**: What it depends on and what depends on it

4. Add appropriate labels:
   - `milestone`
   - `tracking`
   - Phase label (`mvp`, `v1.0`, `future`)
   - Component label if applicable (`backend`, `frontend`, `docs`)

5. Link related issues using "Related Issues" section

### Example Milestone Issue

```markdown
---
name: Milestone Tracker
title: '[MILESTONE] Phase 2: Repository Infrastructure'
labels: milestone, tracking, mvp
---

## Milestone Information

**Milestone Name**: Phase 2: Repository Infrastructure
**Target Date**: 2026-02-15
**Priority**: P0 (Critical)
**Phase**: MVP

## Milestone Description

Set up the complete project structure for both backend (Python) 
and frontend (React/TypeScript) with all necessary development 
tools and configurations.

## Success Criteria

- [x] Backend directory structure created
- [x] Frontend directory structure created  
- [ ] All development tools configured
- [ ] Documentation updated

## Tasks and Sub-Issues

### Related Issues
- #15: Initialize Python backend structure
- #16: Initialize React/TypeScript frontend
- #17: Configure development tools

...
```

## Milestone Workflow

### 1. Planning Phase
- Review PRD and Roadmap
- Identify milestone scope
- Create milestone issue
- Break down into sub-issues/tasks
- Estimate timeline
- Identify dependencies

### 2. Execution Phase
- Work on tasks in priority order
- Update task checklist as items complete
- Update progress percentage
- Add updates to "Recent Updates" section
- Link PRs to related tasks

### 3. Review Phase
- Verify all success criteria met
- Review completion of all tasks
- Update roadmap document
- Close milestone issue
- Conduct retrospective (for major milestones)

## Priority Levels

**P0 - Critical**: Must-have for release, blocks other work
- Example: Core data models, essential API endpoints

**P1 - High**: Important for release, significantly impacts functionality
- Example: LLM integration, user authentication

**P2 - Medium**: Nice to have, enhances experience
- Example: Advanced filtering, keyboard shortcuts

**P3 - Low**: Future enhancement, not blocking
- Example: Themes, social features

## Milestone Labels

Use these labels to organize milestone issues:

### Phase Labels
- `mvp`: Part of MVP release
- `v1.0`: Part of v1.0 release  
- `future`: Future enhancement

### Status Labels
- `in-progress`: Currently being worked on
- `blocked`: Waiting on dependencies
- `completed`: All tasks finished

### Component Labels
- `backend`: Backend/Python work
- `frontend`: Frontend/React work
- `docs`: Documentation
- `infrastructure`: Build/CI/CD/DevOps

## Tracking Progress

### Updating Milestone Issues

Update milestone issues regularly (at least weekly):

1. Update task checklist
2. Update completion percentage
3. Add recent updates
4. Document blockers if any
5. Update target date if needed

### Progress Reporting

For major milestones, provide updates in:
- Milestone issue comments
- Project README
- Team meetings/communications
- Roadmap document

### Completion Criteria

A milestone is complete when:
- All tasks in checklist are done
- All success criteria are met
- Related documentation is updated
- Changes are merged to main branch
- No critical bugs remain

## Best Practices

### Do's ✅
- Keep milestone scope focused and achievable
- Update progress regularly
- Link all related issues and PRs
- Document blockers and risks
- Break large milestones into smaller ones
- Review and update target dates realistically
- Celebrate milestone completions

### Don'ts ❌
- Don't let milestones become stale without updates
- Don't create milestone issues for small tasks (use regular issues)
- Don't mark milestones complete with outstanding issues
- Don't skip documenting progress
- Don't ignore dependencies
- Don't set unrealistic deadlines

## Milestone Templates

### Quick Checklist Template

```markdown
## Milestone: [Name]
**Target**: [Date]
**Status**: [Not Started/In Progress/Complete]

### Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

### Progress
- Completed: X/Y tasks
- Blockers: [None/List]
```

### Monthly Review Template

```markdown
## Monthly Milestone Review - [Month Year]

### Completed Milestones
- [x] Milestone 1
- [x] Milestone 2

### In Progress  
- [ ] Milestone 3 (75% complete)
- [ ] Milestone 4 (25% complete)

### Upcoming
- [ ] Milestone 5 (starts [date])
- [ ] Milestone 6 (starts [date])

### Highlights
- Key achievement 1
- Key achievement 2

### Challenges
- Challenge 1 and resolution
- Challenge 2 and plan
```

## References

- **[Project Roadmap](ROADMAP.md)**: Detailed milestone breakdown
- **[PRD](PRD.md)**: Product requirements and specifications
- **[CONTRIBUTING.md](../CONTRIBUTING.md)**: Contribution guidelines
- **GitHub Projects**: Visual milestone tracking (if configured)

## Questions?

If you have questions about milestone tracking:
1. Review this guide and the roadmap
2. Check existing milestone issues for examples
3. Open a discussion issue with the `question` label

---

**Last Updated**: January 17, 2026  
**Maintained By**: Project Team
