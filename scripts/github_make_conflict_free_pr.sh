#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./scripts/github_make_conflict_free_pr.sh <repo-url> [base-branch] [pr-branch]
# Example:
#   ./scripts/github_make_conflict_free_pr.sh git@github.com:user/repo.git main work

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <repo-url> [base-branch] [pr-branch]"
  exit 1
fi

REPO_URL="$1"
BASE_BRANCH="${2:-main}"
PR_BRANCH="${3:-$(git rev-parse --abbrev-ref HEAD)}"

if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REPO_URL"
else
  git remote add origin "$REPO_URL"
fi

git fetch origin "$BASE_BRANCH" "$PR_BRANCH" || true

# ensure we are on PR branch
CURRENT="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$CURRENT" != "$PR_BRANCH" ]]; then
  git checkout "$PR_BRANCH"
fi

# Rebase with "ours" preference for fast conflict resolution in docs/app files
set +e
git rebase -X ours "origin/$BASE_BRANCH"
REB=$?
set -e

if [[ $REB -ne 0 ]]; then
  echo "⚠️ Rebase paused because of hard conflict. Auto-resolving known files..."
  for f in INSTALLATION_DE.md OfflineArcadeWindows/README.md OfflineArcadeWindows/app.py OfflineArcadewindows/README.md OfflineArcadewindows/app.py; do
    git checkout --ours -- "$f" 2>/dev/null || true
    git add "$f" 2>/dev/null || true
  done
  git add -A
  git rebase --continue || {
    echo "❌ Could not finish rebase automatically. Resolve manually then push."
    exit 1
  }
fi

git push --force-with-lease origin "$PR_BRANCH"
echo "✅ PR branch is now rebased on origin/$BASE_BRANCH and pushed (conflicts should disappear)."
