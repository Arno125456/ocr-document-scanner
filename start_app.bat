@echo off
echo Starting OCR Document Categorizer Application...
echo.

REM Check if backend directory exists
if not exist "backend" (
    echo Error: backend directory not found!
    pause
    exit /b 1
)

REM Change to backend directory
cd backend

REM Start the FastAPI server
echo Starting backend server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
uvicorn main:app --reload

pause