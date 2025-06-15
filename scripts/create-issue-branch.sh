#!/bin/bash

# Script to create properly named branches for GitHub issues
# Usage: ./scripts/create-issue-branch.sh <issue_number> [branch_prefix]

set -e

if [ $# -lt 1 ]; then
  echo "Usage: $0 <issue_number> [branch_prefix]"
  echo "Example: $0 3 hw2"
  exit 1
fi

ISSUE_NUMBER=$1
BRANCH_PREFIX=${2:-"issue"}

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
  echo "❌ GitHub CLI (gh) is required but not installed."
  echo "Install it from: https://cli.github.com/"
  exit 1
fi

echo "🔍 Fetching issue #$ISSUE_NUMBER details..."

# Get issue details
ISSUE_DATA=$(gh issue view $ISSUE_NUMBER --json title,body)
ISSUE_TITLE=$(echo "$ISSUE_DATA" | jq -r '.title')

if [ "$ISSUE_TITLE" = "null" ]; then
  echo "❌ Issue #$ISSUE_NUMBER not found"
  exit 1
fi

# Create branch name from issue title
CLEAN_TITLE=$(echo "$ISSUE_TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-zA-Z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g' | cut -c1-50)
BRANCH_NAME="${BRANCH_PREFIX}-${ISSUE_NUMBER}-${CLEAN_TITLE}"

echo "📋 Issue: #$ISSUE_NUMBER - $ISSUE_TITLE"
echo "🌿 Branch: $BRANCH_NAME"

# Check if branch already exists
if git show-ref --verify --quiet refs/heads/$BRANCH_NAME; then
  echo "⚠️  Branch $BRANCH_NAME already exists locally"
  read -p "Switch to existing branch? (y/N): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    git checkout $BRANCH_NAME
    echo "✅ Switched to existing branch: $BRANCH_NAME"
  fi
else
  # Create new branch
  git checkout -b $BRANCH_NAME
  echo "✅ Created new branch: $BRANCH_NAME"
fi

# Generate PR template
cat > PR_TEMPLATE_${ISSUE_NUMBER}.md << EOF
# PR for Issue #${ISSUE_NUMBER}: ${ISSUE_TITLE}

## Summary
<!-- Brief description of what this PR accomplishes -->

Closes #${ISSUE_NUMBER}

## Changes Made
<!-- List the main changes/features implemented -->
- [ ] Change 1
- [ ] Change 2
- [ ] Change 3

## Test Plan
<!-- How to test the changes -->
- [ ] Test case 1
- [ ] Test case 2
- [ ] Test case 3

## Additional Notes
<!-- Any additional context or notes -->

---
🤖 Generated with [Claude Code](https://claude.ai/code)
EOF

echo "📝 Created PR template: PR_TEMPLATE_${ISSUE_NUMBER}.md"
echo ""
echo "🚀 Next steps:"
echo "1. Make your changes"
echo "2. Commit with: git commit -m \"Brief description"
echo ""
echo "🤖 Generated with [Claude Code](https://claude.ai/code)"
echo ""
echo "Co-Authored-By: Claude <noreply@anthropic.com>\""
echo "3. Push: git push -u origin $BRANCH_NAME"
echo "4. Create PR: gh pr create --title \"$ISSUE_TITLE\" --body-file PR_TEMPLATE_${ISSUE_NUMBER}.md"