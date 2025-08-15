@echo off
if "%~1"=="" (
    echo Usage: quick-commit.bat "Your commit message"
    echo Example: quick-commit.bat "Fix mobile image sizing"
    exit /b 1
)

echo Adding all changes...
git add .

echo Committing with message: %~1
git commit -m "%~1"

echo Pushing to remote...
git push

echo Done!