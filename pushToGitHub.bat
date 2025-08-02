@echo off
echo ========================================
echo MACS - Secure GitHub Push
echo ========================================
echo.

REM Check if we're in the right directory
if not exist "main.py" (
    echo ❌ Error: main.py not found
    echo Please run this script from the MACSv01 folder
    pause
    exit /b 1
)

echo 🔍 Checking Git repository status...

REM Check if Git is initialized
if not exist ".git" (
    echo ❌ No Git repository found
    echo 🔄 Initializing Git repository...
    git init
    if errorlevel 1 (
        echo ❌ Failed to initialize Git repository
        echo 💡 Please install Git first: https://git-scm.com/
        pause
        exit /b 1
    )
    echo ✅ Git repository initialized
)

REM Create/update .gitignore for security
echo 🛡️ Setting up secure .gitignore...
(
echo # Python Virtual Environment - NEVER COMMIT
echo .venv/
echo venv/
echo env/
echo ENV/
echo __pycache__/
echo *.pyc
echo *.pyo
echo *.pyd
echo .Python
echo pip-log.txt
echo pip-delete-this-directory.txt
echo
echo # IDE and Editor files
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo *~
echo .project
echo .pydevproject
echo
echo # Operating System files
echo .DS_Store
echo .DS_Store?
echo ._*
echo .Spotlight-V100
echo .Trashes
echo ehthumbs.db
echo Thumbs.db
echo desktop.ini
echo
echo # Security - NEVER COMMIT THESE!
echo *.key
echo *.pem
echo *.p12
echo *.pfx
echo *.crt
echo *.cer
echo *.der
echo .env
echo .env.local
echo .env.development
echo .env.test
echo .env.production
echo .env.staging
echo config/secrets.json
echo secrets/
echo credentials/
echo auth/
echo tokens/
echo
echo # MACS Security Files - NEVER COMMIT
echo .macs_license
echo .macs_security
echo *.license
echo *.activation
echo security_logs/
echo
echo # Medical Data - PRIVACY PROTECTION
echo patient_data/
echo medical_records/
echo health_data/
echo clinical_data/
echo patient_info/
echo medical_files/
echo *.csv
echo *.xlsx
echo *.xls
echo *.ods
echo *.db
echo *.sqlite
echo *.sqlite3
echo *.mdb
echo *.accdb
echo data/
echo datasets/
echo
echo # Logs and temporary files
echo *.log
echo logs/
echo temp/
echo tmp/
echo cache/
echo .cache/
echo
echo # Distribution and build files
echo dist/
echo build/
echo *.egg-info/
echo .eggs/
echo downloads/
echo .tox/
echo .coverage
echo .pytest_cache/
echo htmlcov/
echo
echo # Backup files
echo *.bak
echo *.backup
echo *.old
echo *.orig
echo *.save
echo
echo # Documentation builds
echo docs/_build/
echo site/
echo
echo # JetBrains IDEs
echo .idea/
echo *.iml
echo *.ipr
echo *.iws
echo
echo # Visual Studio Code
echo .vscode/
echo *.code-workspace
echo
echo # Windows thumbnail cache
echo ehthumbs.db
echo ehthumbs_vista.db
echo
echo # macOS
echo .AppleDouble
echo .LSOverride
echo
echo # Linux
echo *~
echo .fuse_hidden*
echo .directory
echo .Trash-*
echo .nfs*
) > .gitignore

echo ✅ Secure .gitignore created

REM Check Git status
echo.
echo 📊 Git status:
git status --porcelain
if errorlevel 1 (
    echo ❌ Git command failed
    pause
    exit /b 1
)

REM Add files (respecting .gitignore)
echo.
echo 📦 Adding files to Git (excluding sensitive data)...
git add .
if errorlevel 1 (
    echo ❌ Failed to add files
    pause
    exit /b 1
)

REM Show what will be committed
echo.
echo 📋 Files to be committed:
git diff --cached --name-only

REM Get commit message
echo.
set /p commit_message="💬 Enter commit message (or press Enter for default): "
if "%commit_message%"=="" set commit_message=Update MACS - Medical Analysis System

REM Commit changes
echo.
echo 📝 Committing changes...
git commit -m "%commit_message%"
if errorlevel 1 (
    echo ⚠️ Nothing to commit or commit failed
    echo This might be normal if no changes were made
)

REM Check if remote origin exists
echo.
echo 🔗 Checking GitHub remote...
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo ❌ No GitHub remote configured
    echo 🔄 Setting up your GitHub repository...
    echo Repository: https://github.com/hanshendrickx/MAICS-Maintenance-2025-py-niceGUIv11.git
    
    git remote add origin https://github.com/hanshendrickx/MAICS-Maintenance-2025-py-niceGUIv11.git
    if errorlevel 1 (
        echo ❌ Failed to add remote
        echo 💡 Check if the repository exists on GitHub
        pause
        exit /b 1
    ) else (
        echo ✅ GitHub remote added successfully
    )
) else (
    echo ✅ GitHub remote already configured
    for /f "tokens=*" %%i in ('git remote get-url origin') do echo    URL: %%i
)

REM Get current branch
for /f "tokens=*" %%i in ('git branch --show-current') do set current_branch=%%i
if "%current_branch%"=="" set current_branch=main

echo.
echo 🚀 Pushing to GitHub...
echo Branch: %current_branch%
echo Remote: origin

REM Push to GitHub
git push -u origin %current_branch%
if errorlevel 1 (
    echo.
    echo ❌ Push failed! Common solutions:
    echo.
    echo 🔐 Authentication issues:
    echo    - Use Personal Access Token instead of password
    echo    - GitHub Settings → Developer settings → Personal access tokens
    echo    - Or set up SSH keys
    echo.
    echo 🌿 Branch issues:
    echo    - Repository might be empty (first push)
    echo    - Try: git push -u origin %current_branch% --force
    echo.
    echo 🔗 Remote issues:
    echo    - Check repository URL is correct
    echo    - Verify repository exists on GitHub
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo ✅ SUCCESS! MACS pushed to GitHub
    echo ========================================
    echo 🌐 Your secure medical application is now backed up!
    echo 🛡️ Sensitive data excluded by .gitignore
    echo 📦 Ready for collaboration and deployment
    echo.
)

pause
