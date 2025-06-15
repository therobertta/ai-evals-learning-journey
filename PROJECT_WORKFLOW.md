# Project Workflow Guide

## Overview
This document outlines the automated GitHub workflow for managing issues, branches, pull requests, and project status updates.

## 🔄 Automated Workflow

### 1. Issue Creation → Branch → PR → Merge → Project Update

```mermaid
graph LR
    A[Create Issue] → B[Create Branch] → C[Make Changes] → D[Create PR] → E[Merge PR] → F[Auto Update Project]
```

### 2. Creating Branches for Issues

#### Option A: Using the Helper Script (Recommended)
```bash
# Create branch for issue #3 with prefix 'hw2'
./scripts/create-issue-branch.sh 3 hw2

# This creates branch: hw2-3-conduct-axial-coding-and-refine-failure-mode-taxonomy
```

#### Option B: Manual Creation
```bash
# Follow naming convention: prefix-issueNumber-cleanTitle
git checkout -b hw2-3-conduct-axial-coding-and-refine-failure-mode-taxonomy
```

### 3. Creating Pull Requests

**Always include issue reference in PR body:**
```markdown
## Summary
Brief description of changes

Closes #3

## Changes Made
- Feature 1
- Feature 2

🤖 Generated with [Claude Code](https://claude.ai/code)
```

### 4. Automatic Project Status Updates

When a PR is merged, the GitHub Action automatically:
- Detects the referenced issue number (from "Closes #N")
- Updates the GitHub Project status to "Done"
- Adds a comment to the issue with merge details

## 🛠 GitHub Actions

### PR Merge Project Update
**File:** `.github/workflows/pr-merge-project-update.yml`

**Triggers:** When a PR is merged
**Actions:**
1. Extracts issue number from PR body
2. Finds the issue in the "AI Evals HW" project
3. Updates status to "Done"
4. Comments on the issue

### Issue Branch Helper  
**File:** `.github/workflows/issue-branch-helper.yml`

**Triggers:** Manual workflow dispatch
**Actions:**
1. Creates properly named branch
2. Generates PR template

## 📋 Project States

| Status | Description | Trigger |
|--------|-------------|---------|
| **Todo** | Issue created, not started | Manual |
| **In Progress** | Work has begun | Manual |
| **Human Review** | PR created, awaiting review | Manual/Auto |
| **Done** | PR merged, work complete | **Automatic** |

## 🎯 Best Practices

### Branch Naming Convention
Format: `{prefix}-{issueNumber}-{cleanTitle}`

Examples:
- `hw2-2-perform-open-coding-analysis-on-bot-traces`
- `feature-5-add-export-functionality`
- `bugfix-8-fix-authentication-error`

### Commit Messages
```
Brief description of changes

Detailed explanation if needed.

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### PR Requirements
- Must reference issue with "Closes #N"
- Include clear summary and test plan
- Follow template structure

## 🔧 Setup Requirements

### Repository Permissions
The GitHub Actions require:
- `contents: read` - Read repository content
- `issues: write` - Comment on issues
- `projects: write` - Update project status

### Project Configuration
- Project ID: `PVT_kwDOCyai2s4A7gSA` (AI Evals HW)
- Status Field ID: `PVTSSF_lADOCyai2s4A7gSAzgvyG5I`
- Done Option ID: `98236657`

## 🧪 Testing the Workflow

To test the automatic status update:
1. Create a test issue
2. Create branch and make changes
3. Create PR with "Closes #N" in body
4. Merge the PR
5. Verify issue status changes to "Done"
6. Check that comment was added to issue

## 🚨 Troubleshooting

### Common Issues
1. **Action fails to find issue:** Check PR body format
2. **Can't update project:** Verify permissions and project IDs
3. **Branch creation fails:** Ensure issue exists and title is valid

### Manual Override
If automatic update fails, manually update project status:
```bash
gh api graphql --field query='mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: "PVT_kwDOCyai2s4A7gSA"
    itemId: "ITEM_ID_HERE"
    fieldId: "PVTSSF_lADOCyai2s4A7gSAzgvyG5I"
    value: { singleSelectOptionId: "98236657" }
  }) { projectV2Item { id } }
}'
```