@echo off
echo Checking virtual environment...

if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found at backend\venv
    echo Please create a virtual environment first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    exit /b 1
)

echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

echo 🚀 Starting FastAPI backend server...
python run_dev.py