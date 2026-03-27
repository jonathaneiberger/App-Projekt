@echo off
setlocal

if "%~1"=="" (
  echo Usage: scripts\github_first_push.bat ^<github-repo-url^>
  echo Example: scripts\github_first_push.bat https://github.com/deinuser/offline-arcade.git
  exit /b 1
)

set REPO_URL=%~1

git remote get-url origin >nul 2>&1
if errorlevel 1 (
  git remote add origin %REPO_URL%
) else (
  git remote set-url origin %REPO_URL%
)

git branch -M main
git push -u origin main
if errorlevel 1 exit /b 1

echo ✅ First push complete: %REPO_URL% (main)
endlocal
