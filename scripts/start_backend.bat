@echo off
cd /d %~dp0\..
echo Checking virtual environment...

if not exist "backend\venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found at backend\venv
    echo Please create a virtual environment first:
    echo   cd backend
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    exit /b 1
)

echo ✅ Activating virtual environment...
call backend\venv\Scripts\activate.bat

echo 🚀 Starting FastAPI backend server...
cd backend
python run_dev.py
