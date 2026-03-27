#!/usr/bin/env bash
set -euo pipefail

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
BASE_BRANCH="${1:-main}"

echo "ℹ️ Branch: $BRANCH | Base: $BASE_BRANCH"
git fetch origin

set +e
git merge "origin/$BASE_BRANCH"
MERGE_EXIT=$?
set -e

if [[ $MERGE_EXIT -ne 0 ]]; then
  echo "⚠️ Merge conflicts found. Resolving by keeping current-branch versions for known files..."

  CANDIDATES=(
    "INSTALLATION_DE.md"
    "OfflineArcadeWindows/README.md"
    "OfflineArcadeWindows/app.py"
    "OfflineArcadewindows/README.md"
    "OfflineArcadewindows/app.py"
  )

  for f in "${CANDIDATES[@]}"; do
    if git ls-files --error-unmatch "$f" >/dev/null 2>&1 || [[ -e "$f" ]]; then
      git checkout --ours -- "$f" 2>/dev/null || true
      git add "$f" 2>/dev/null || true
    fi
  done

  # add any remaining files that are already resolved
  git add -A

  if git diff --cached --quiet; then
    echo "❌ Nothing staged after conflict resolution. Please resolve manually."
    exit 1
  fi

  git commit -m "Resolve PR conflicts by keeping branch versions for app/docs"
fi

git push origin "$BRANCH"
echo "✅ Done. Push successful. Refresh PR page."
