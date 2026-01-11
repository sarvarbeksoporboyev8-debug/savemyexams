#!/bin/bash
# Trigger GitHub Actions workflow using GitHub CLI

echo "Triggering SaveMyExams scraper workflow..."
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed"
    echo ""
    echo "Install it:"
    echo "  Linux: sudo apt install gh"
    echo "  Mac: brew install gh"
    echo "  Or visit: https://cli.github.com/"
    echo ""
    echo "Then authenticate: gh auth login"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI"
    echo ""
    echo "Run: gh auth login"
    exit 1
fi

# Trigger the workflow
echo "Triggering workflow..."
gh workflow run scrape.yml

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Workflow triggered successfully!"
    echo ""
    echo "View status:"
    echo "  gh run list --workflow=scrape.yml"
    echo ""
    echo "Or visit:"
    echo "  https://github.com/sarvarbeksoporboyev8-debug/savemyexams/actions"
else
    echo ""
    echo "❌ Failed to trigger workflow"
    echo ""
    echo "Try manually:"
    echo "  https://github.com/sarvarbeksoporboyev8-debug/savemyexams/actions"
fi
