@echo off
echo 🚀 Setting up ChromaCraft Development Environment...
echo.

echo 📦 Installing frontend dependencies...
cd frontend
call pnpm install
cd ..

echo 🐍 Setting up Python backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

cd ..

echo.
echo ✅ Setup complete!
echo.
echo To start development:
echo   pnpm run dev
echo.
echo Or use the shortcut:
echo   dev.bat