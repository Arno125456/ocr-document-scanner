@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  OCR Document Scanner - Quick Deploy
echo  GitHub User: Arno125456
echo ========================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/
    pause
    exit /b 1
)

echo Step 1: Initialize Git Repository
echo ----------------------------------
if not exist .git (
    git init
    echo [OK] Git repository initialized!
) else (
    echo [OK] Git repository already exists.
)
echo.

echo Step 2: Add all files
echo ---------------------
git add .
echo [OK] Files added!
echo.

echo Step 3: Commit changes
echo ----------------------
git commit -m "Ready for deployment - OCR Document Scanner by Arno125456"
echo [OK] Changes committed!
echo.

echo ========================================
echo  Step 4: Create GitHub Repository
echo ========================================
echo.
echo 1. Go to: https://github.com/new
echo 2. Repository name: ocr-document-scanner
echo 3. Make it Public or Private (your choice)
echo 4. Click "Create repository"
echo.
pause

echo.
echo ========================================
echo  Step 5: Push to GitHub
echo ========================================
echo.

REM Try to push, if it fails, help user set up remote
git remote -v | findstr origin >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Setting up remote repository...
    echo.
    echo Run this command (replace with your actual repo URL):
    echo.
    echo git remote add origin https://github.com/Arno125456/ocr-document-scanner.git
    echo git branch -M main
    echo git push -u origin main
    echo.
    pause
) else (
    echo Pushing to GitHub...
    git branch -M main 2>nul
    git push -u origin main
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Successfully pushed to GitHub!
    ) else (
        echo.
        echo Push failed. Try running manually:
        echo git remote add origin https://github.com/Arno125456/ocr-document-scanner.git
        echo git push -u origin main
        echo.
        pause
    )
)

echo.
echo ========================================
echo  NEXT STEPS:
echo ========================================
echo.
echo  Your code is ready on GitHub!
echo.
echo  DEPLOY BACKEND (Render):
echo  1. Go to: https://render.com
echo  2. Sign in with GitHub
echo  3. Click "New +" ^> "Blueprint"
echo  4. Select "ocr-document-scanner" repository
echo  5. Click "Apply"
echo  6. Wait 3-5 minutes
echo  7. Copy your backend URL
echo.
echo  DEPLOY FRONTEND (Vercel):
echo  1. Go to: https://vercel.com
echo  2. Sign in with GitHub
echo  3. Click "Add New..." ^> "Project"
echo  4. Import "ocr-document-scanner"
echo  5. Set Root Directory: frontend
echo  6. Add Environment Variable:
echo     VITE_API_URL = https://YOUR-BACKEND-URL.onrender.com
echo  7. Click "Deploy"
echo.
echo  See DEPLOYMENT.md for detailed instructions!
echo ========================================
echo.
echo  GitHub Repository:
echo  https://github.com/Arno125456/ocr-document-scanner
echo.
pause
