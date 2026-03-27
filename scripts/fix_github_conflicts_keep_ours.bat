@echo off
setlocal

set BASE=main
if not "%~1"=="" set BASE=%~1

for /f %%b in ('git rev-parse --abbrev-ref HEAD') do set BRANCH=%%b

echo Branch: %BRANCH% ^| Base: %BASE%
git fetch origin

git merge origin/%BASE%
if errorlevel 1 (
  echo Merge conflicts found. Keeping current-branch version for known files...

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
  git commit -m "Resolve PR conflicts by keeping branch versions for app/docs"
)

git push origin %BRANCH%
if errorlevel 1 exit /b 1

echo Done. Push successful. Refresh PR page.
endlocal
