@echo off
setlocal

for /f %%b in ('git rev-parse --abbrev-ref HEAD') do set BRANCH=%%b

git fetch origin
git pull --rebase origin %BRANCH%
if errorlevel 1 (
  echo ❌ Rebase failed. Resolve conflicts, then run:
  echo    git add ^<files^>
  echo    git rebase --continue
  exit /b 1
)

git push origin %BRANCH%
if errorlevel 1 exit /b 1

echo ✅ Update pushed to origin/%BRANCH%
endlocal
