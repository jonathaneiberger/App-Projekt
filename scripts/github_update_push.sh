#!/usr/bin/env bash
set -euo pipefail

BRANCH="$(git rev-parse --abbrev-ref HEAD)"

git fetch origin
# keep history linear and reduce merge conflicts
if git pull --rebase origin "$BRANCH"; then
  echo "✅ Rebase pull finished"
else
  echo "❌ Rebase failed. Resolve conflicts, then run:"
  echo "   git add <files>"
  echo "   git rebase --continue"
  exit 1
fi

git push origin "$BRANCH"
echo "✅ Update pushed to origin/$BRANCH"
