@echo off

:: Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python 3.x and try again.
    exit /b
)

:: Check if the virtual environment folder exists
if not exist venv (
    echo Virtual environment not found. Creating a new one...
    python -m venv venv
    if ERRORLEVEL 1 (
        echo Failed to create virtual environment.
        exit /b
    )
)

:: Upgrade pip
echo Upgrading pip...
venv\Scripts\python -m pip install --upgrade pip
if ERRORLEVEL 1 (
    echo Failed to upgrade pip.
    exit /b
)

:: Install dependencies
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    venv\Scripts\python -m pip install -r requirements.txt
    if ERRORLEVEL 1 (
        echo Failed to install dependencies.
        exit /b
    )
) else (
    echo requirements.txt not found. Please add the file and try again.
    exit /b
)

:: Ask the user if they want to run the project
set /p RUN_PROJECT="Do you want to run the project now? (y/n): "
if /i "%RUN_PROJECT%"=="y" (
    echo Running the project...
    venv\Scripts\python app.py
) else (
    echo Skipping project execution.
)

:: Pause at the end
pause
