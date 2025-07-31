@echo off
setlocal enabledelayedexpansion

:: ── Initialize error counter ────────────────────────────────────────────────
set "ERRORS=0"

:: ── Appearance ───────────────────────────────────────────────────────────────
color 0A
title MAICS.app - Medical AI Complaints ^& Signs

:: ── Setup timestamped log file ───────────────────────────────────────────────
set "ROOT=%USERPROFILE%\envs\Maintenance_MainW"
if not exist "%ROOT%" mkdir "%ROOT%"

for /f "tokens=1-3 delims=/ " %%A in ("%date%") do (
  set "MM=%%A" & set "DD=%%B" & set "YYYY=%%C"
)
for /f "tokens=1-3 delims=:." %%A in ("%time%") do (
  set "HH=%%A" & set "MN=%%B" & set "SS=%%C"
)
set "timestamp=%YYYY%-%MM%-%DD%_%HH%-%MN%-%SS%"
set "logfile=%ROOT%\cleanup_scan_%timestamp%.txt"

:: ── Header ─────────────────────────────────────────────────────────────────
echo ===============================================================================
echo                   MAICS.app - Medical AI Complaints ^& Signs
echo                    Dev Environment Cleanup Scanner
echo ===============================================================================

echo Starting scan at %date% %time% > "%logfile%"
echo =============================================================================== >> "%logfile%"

:: ── [1/8] Python Installations ─────────────────────────────────────────────────
echo [1/8] Scanning Python installations...
echo [1/8] Scanning Python installations... >> "%logfile%"

echo   • Checking for Python executable...
set "REAL_PY="

:: Try to find real Python (not WindowsApps shim)
for /f "delims=" %%P in ('where python 2^>nul ^| findstr /i /v "WindowsApps"') do (
  set "REAL_PY=%%P"
  goto :got_py
)

:: If no real python found, check common locations
if not defined REAL_PY (
  echo   • Only WindowsApps shim found; checking install directories...
  echo   ⚠ Only WindowsApps shim found; checking known install dirs >> "%logfile%"
  for %%P in (
    "%LOCALAPPDATA%\Programs\Python\Python*\python.exe"
    "%ProgramFiles%\Python*\python.exe"
    "%ProgramFiles(x86)%\Python*\python.exe"
  ) do if exist "%%P" (
    set "REAL_PY=%%P"
    goto :got_py
  )
)

:: Try py launcher as last resort
if not defined REAL_PY (
  echo   • Trying py launcher...
  where py >nul 2>&1 && set "REAL_PY=py"
)

:got_py
if not defined REAL_PY (
  echo   ❌ No Python detected - continuing scan anyway
  echo   ❌ No Python detected, continuing scan anyway >> "%logfile%"
  set /a ERRORS+=1
  set "REAL_PY=python"
) else (
  echo   ✓ Python found: %REAL_PY%
  echo   ✓ Using Python: %REAL_PY% >> "%logfile%"
  "%REAL_PY%" --version >> "%logfile%" 2>&1
)

:: ── [2/8] pip & Package Managers ──────────────────────────────────────────────
echo [2/8] Scanning pip and package managers...
echo. >> "%logfile%"
echo [2/8] Scanning pip and other package managers... >> "%logfile%"

echo   • Checking pip...
echo   • Checking pip via python -m pip... >> "%logfile%"
if defined REAL_PY (
  "%REAL_PY%" -m pip --version >> "%logfile%" 2>&1 && (
    echo     ✓ pip module works
    echo     ✓ pip module works      >> "%logfile%"
  ) || (
    echo     ✗ pip module failed
    echo     ✗ pip module failed      >> "%logfile%"
    set /a ERRORS+=1
  )
) else (
  echo     ✗ No Python found for pip check
  echo     ✗ No Python found for pip check >> "%logfile%"
  set /a ERRORS+=1
)

echo   • Checking pipx...
echo   • Checking pipx... >> "%logfile%"
where pipx >nul 2>&1 && (
  echo     ✓ pipx found
  echo     ✓ pipx found           >> "%logfile%"
  pipx --version                >> "%logfile%" 2>&1
) || (
  echo     ✗ pipx not found
  echo     ✗ pipx not found       >> "%logfile%"
)

echo   • Checking uv...
echo   • Checking uv... >> "%logfile%"
where uv >nul 2>&1 && (
  echo     ✓ uv found
  echo     ✓ uv found             >> "%logfile%"
  uv --version                   >> "%logfile%" 2>&1
) || (
  echo     ✗ uv not found (needed for Python 3.13.x)
  echo     ✗ uv not found         >> "%logfile%"
)

echo   • Checking conda...
echo   • Checking conda... >> "%logfile%"
where conda >nul 2>&1 && (
  echo     ✓ conda found
  echo     ✓ conda found          >> "%logfile%"
  conda --version                >> "%logfile%" 2>&1
) || (
  echo     ✗ conda not found
  echo     ✗ conda not found      >> "%logfile%"
)

:: ── [3/8] Virtual Environments ────────────────────────────────────────────────
echo [3/8] Scanning Virtual Environments...
echo. >> "%logfile%"
echo [3/8] Scanning Virtual Environments... >> "%logfile%"

echo   • Searching for virtual environments...
set "VENV_COUNT=0"
for /d /r "%USERPROFILE%\envs" %%D in (.venv* venv* env*) do (
  if exist "%%D\Scripts\activate.bat" (
    echo   ✓ Found: %%D
    echo   ✓ Virtual-env found: %%D >> "%logfile%"
    set /a VENV_COUNT+=1
  )
)

if %VENV_COUNT%==0 (
  echo   ✗ No virtual environments found
  echo   ✗ No virtual environments found >> "%logfile%"
) else (
  echo   ✓ Found %VENV_COUNT% virtual environment(s)
  echo   ✓ Found %VENV_COUNT% virtual environment(s) >> "%logfile%"
)

:: ── [4/8] NiceGUI Projects ─────────────────────────────────────────────────────
echo [4/8] Scanning for NiceGUI...
echo. >> "%logfile%"
echo [4/8] Scanning for NiceGUI installations ^& projects... >> "%logfile%"

echo   • Checking global NiceGUI installation...
if defined REAL_PY (
  "%REAL_PY%" -m pip show nicegui >nul 2>&1 && (
    echo   ✓ NiceGUI installed globally
    echo   ✓ NiceGUI installed globally >> "%logfile%"
    "%REAL_PY%" -m pip show nicegui   >> "%logfile%" 2>&1
  ) || (
    echo   ✗ NiceGUI not installed globally
    echo   ✗ NiceGUI not installed globally >> "%logfile%"
  )
) else (
  echo   ✗ Cannot check NiceGUI - no Python found
  echo   ✗ Cannot check NiceGUI - no Python found >> "%logfile%"
)

echo   • Searching for NiceGUI projects...
echo   • Searching for Python files importing "nicegui"... >> "%logfile%"
set "NICEGUI_COUNT=0"
for /r "%USERPROFILE%" %%F in (*.py) do (
  findstr /l "import nicegui" "%%F" >nul 2>&1 && (
    echo   ✓ Found: %%F
    echo   ✓ NiceGUI project found: %%F >> "%logfile%"
    set /a NICEGUI_COUNT+=1
  )
)

if %NICEGUI_COUNT%==0 (
  echo   ✗ No NiceGUI projects found
  echo   ✗ No NiceGUI projects found >> "%logfile%"
) else (
  echo   ✓ Found %NICEGUI_COUNT% NiceGUI project(s)
  echo   ✓ Found %NICEGUI_COUNT% NiceGUI project(s) >> "%logfile%"
)

:: ── [5/8] Development Tools ───────────────────────────────────────────────────
echo [5/8] Scanning development tools...
echo. >> "%logfile%"
echo [5/8] Scanning development tools... >> "%logfile%"

echo   • Checking VS Code...
where code >nul 2>&1 && (
  echo   ✓ VS Code found
  echo   ✓ code found            >> "%logfile%"
  code --version               >> "%logfile%" 2>&1
) || (
  echo   ✗ VS Code not found
  echo   ✗ code not found        >> "%logfile%"
)

echo   • Checking Git...
where git >nul 2>&1 && (
  echo   ✓ Git found
  echo   ✓ git found            >> "%logfile%"
  git --version               >> "%logfile%" 2>&1
) || (
  echo   ✗ Git not found
  echo   ✗ git not found        >> "%logfile%"
)

echo   • Checking Node.js...
where node >nul 2>&1 && (
  echo   ✓ Node.js found
  echo   ✓ node found            >> "%logfile%"
  node --version               >> "%logfile%" 2>&1
) || (
  echo   ✗ Node.js not found
  echo   ✗ node not found        >> "%logfile%"
)

:: ── [6/8] Global pip Packages ─────────────────────────────────────────────────
echo [6/8] Listing global packages...
echo. >> "%logfile%"
echo [6/8] Listing global pip packages... >> "%logfile%"

if defined REAL_PY (
  echo   • Getting package list...
  "%REAL_PY%" -m pip list          >> "%logfile%" 2>&1
  echo   ✓ Package list saved to log file
) else (
  echo   ✗ Cannot list packages - no Python found
  echo   ✗ Cannot list packages - no Python found >> "%logfile%"
)

:: ── [7/8] Project Files ───────────────────────────────────────────────────────
echo [7/8] Scanning project files...
echo. >> "%logfile%"
echo [7/8] Scanning for project files (requirements.txt, setup.py, etc.)... >> "%logfile%"

echo   • Searching for Python project files...
set "PROJECT_COUNT=0"
for /r "%USERPROFILE%" %%F in (requirements.txt setup.py pyproject.toml main.py app.py) do (
  echo   ✓ Found: %%F
  echo   ✓ Project file: %%F >> "%logfile%"
  set /a PROJECT_COUNT+=1
)

if %PROJECT_COUNT%==0 (
  echo   ✗ No project files found
  echo   ✗ No project files found >> "%logfile%"
) else (
  echo   ✓ Found %PROJECT_COUNT% project file(s)
  echo   ✓ Found %PROJECT_COUNT% project file(s) >> "%logfile%"
)

:: ── [8/8] Cleanup Recommendations ─────────────────────────────────────────────
echo [8/8] Generating recommendations...
echo. >> "%logfile%"
echo [8/8] Cleanup recommendations: >> "%logfile%"
(
  echo  1. Uninstall Windows-Store Python shims; keep only Python 3.13.x installer.
  echo  2. Remove unwanted virtual environments under "%USERPROFILE%\envs".
  echo  3. Favor uv/pipx for global tools; avoid global pip installs.
  echo  4. Install uv if missing: curl -LsSf https://astral.sh/uv/install.sh ^| sh
  echo  5. Recreate projects in fresh venv via: uv venv .venv ^&^& .venv\Scripts\activate.bat
) >> "%logfile%"

:: ── Final Summary ────────────────────────────────────────────────────────────
:final_summary
echo.
echo ===============================================================================
echo                             SCAN COMPLETE
echo ===============================================================================
echo.
echo ✓ Detailed scan results saved to:
echo   %logfile%
echo.

if "%ERRORS%"=="0" (
  echo *** SUCCESS: All checks passed! Ready for Python 3.13.x setup ***
  echo.
  color 0A
) else (
  echo *** WARNING: %ERRORS% issue(s) detected. Review recommendations. ***
  echo.
  color 0E
)

echo NEXT STEPS:
echo 1. Review the detailed log file
echo 2. Install missing tools (especially 'uv' for Python 3.13.x)
echo 3. Clean up old virtual environments
echo 4. Set up fresh MAICS.app project structure
echo.

echo Opening log file in 3 seconds...
timeout /t 3 /nobreak >nul
notepad "%logfile%"

pause

