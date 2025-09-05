@echo off
REM RareVault Setup Script for Windows
echo 🏺 Setting up RareVault - Vintage Treasures Platform
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!
echo.

REM Setup Backend
echo 🔧 Setting up Backend...
cd backend

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

echo ✅ Backend setup complete!
echo.

REM Setup Frontend
echo 🎨 Setting up Frontend...
cd ..\frontend

REM Install Node.js dependencies
echo Installing Node.js dependencies...
npm install

echo ✅ Frontend setup complete!
echo.

REM Final instructions
echo 🎉 Setup Complete!
echo ==================
echo.
echo Next steps:
echo 1. Set up your MySQL database using the provided SQL script
echo 2. Update backend\.env with your database credentials
echo 3. Start the backend: cd backend ^&^& python run.py
echo 4. Start the frontend: cd frontend ^&^& npm run dev
echo 5. Open http://localhost:3000 in your browser
echo.
echo Happy collecting! 🏺✨
pause
