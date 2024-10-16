@echo off
setlocal enabledelayedexpansion

rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in the PATH. Please install Python first.
    exit /b 1
)

rem Check if pip is installed
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed. Installing pip...

    rem Download get-pip.py to install pip
    powershell -Command "Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py"
    
    rem Install pip
    python get-pip.py
    
    rem Delete get-pip.py after installation
    del get-pip.py
)

rem Verify pip installation
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Failed to install pip. Please check the installation.
    exit /b 1
)

rem Install required Python packages from requirements.txt
if exist "requirements.txt" (
    echo Installing Python packages from requirements.txt...
    python -m pip install -r requirements.txt
) else (
    echo requirements.txt not found. Please make sure it exists in this directory.
    exit /b 1
)

rem Check if Python script exists
if not exist "irrational_search.py" (
    echo Python script irrational_search.py not found. Please ensure it is in this directory.
    exit /b 1
)

rem Execute the Python script
echo Running Python script...
python irrational_search.py

pause
