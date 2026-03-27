@echo off
setlocal

if "%~1"=="" (
  echo Usage: scripts\github_make_conflict_free_pr.bat ^<repo-url^> [base-branch] [pr-branch]
  exit /b 1
)

set REPO_URL=%~1
set BASE=main
if not "%~2"=="" set BASE=%~2

for /f %%b in ('git rev-parse --abbrev-ref HEAD') do set CURR=%%b
set PR=%CURR%
if not "%~3"=="" set PR=%~3

git remote get-url origin >nul 2>&1
if errorlevel 1 (
  git remote add origin %REPO_URL%
) else (
  git remote set-url origin %REPO_URL%
)

git fetch origin %BASE% %PR%

git checkout %PR%
git rebase -X ours origin/%BASE%
if errorlevel 1 (
  echo Rebase has conflicts, auto-resolving known files...
  git checkout --ours -- INSTALLATION_DE.md 2>nul
  git add INSTALLATION_DE.md 2>nul
  git checkout --ours -- OfflineArcadeWindows\README.md 2>nul
  git add OfflineArcadeWindows\README.md 2>nul
  git checkout --ours -- OfflineArcadeWindows\app.py 2>nul
  git add OfflineArcadeWindows\app.py 2>nul
  git checkout --ours -- OfflineArcadewindows\README.md 2>nul
  git add OfflineArcadewindows\README.md 2>nul
  git checkout --ours -- OfflineArcadewindows\app.py 2>nul
  git add OfflineArcadewindows\app.py 2>nul
  git add -A
  git rebase --continue
  if errorlevel 1 exit /b 1
)

git push --force-with-lease origin %PR%
if errorlevel 1 exit /b 1

echo ✅ PR branch rebased on origin/%BASE% and pushed.
endlocal
