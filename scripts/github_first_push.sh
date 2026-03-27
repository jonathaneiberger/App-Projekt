#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: ./scripts/github_first_push.sh <github-repo-url>"
  echo "Example: ./scripts/github_first_push.sh git@github.com:deinuser/offline-arcade.git"
  exit 1
fi

REPO_URL="$1"
BRANCH_NAME="main"

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REPO_URL"
else
  git remote add origin "$REPO_URL"
fi

# rename current branch to main for a clean first push
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$CURRENT_BRANCH" != "$BRANCH_NAME" ]]; then
  git branch -M "$BRANCH_NAME"
fi

git push -u origin "$BRANCH_NAME"
echo "✅ First push complete: $REPO_URL ($BRANCH_NAME)"
