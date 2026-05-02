@echo off
REM GenAI Roadmap — Windows Setup Script
REM Makes the repository ready for personal use

echo 🚀 GenAI Developer Roadmap 2026 — Setup
echo ========================================

REM Get user information
set /p GITHUB_USERNAME="Enter your GitHub username: "
set /p REPO_NAME="Enter your repository name (default: gen-ai-roadmap): "
if "%REPO_NAME%"=="" set REPO_NAME=gen-ai-roadmap
set /p FULL_NAME="Enter your full name: "

echo.
echo Configuring repository for:
echo   GitHub Username: %GITHUB_USERNAME%
echo   Repository: %REPO_NAME%
echo   Full Name: %FULL_NAME%
echo.

REM Update README.md URLs
echo Updating README.md...
powershell -Command "(Get-Content README.md) -replace 'YOUR_USERNAME', '%GITHUB_USERNAME%' | Set-Content README.md"
powershell -Command "(Get-Content README.md) -replace 'YOUR_REPO_NAME', '%REPO_NAME%' | Set-Content README.md"

REM Update dashboard HTML
echo Updating dashboard HTML...
powershell -Command "(Get-Content docs/index.html) -replace 'YOUR_USERNAME', '%GITHUB_USERNAME%' | Set-Content docs/index.html"
powershell -Command "(Get-Content docs/index.html) -replace 'YOUR_REPO_NAME', '%REPO_NAME%' | Set-Content docs/index.html"

REM Update genai-roadmap.md
echo Updating roadmap metadata...
powershell -Command "(Get-Content genai-roadmap.md) -replace 'YOUR_NAME', '%FULL_NAME%' | Set-Content genai-roadmap.md"
powershell -Command "(Get-Content genai-roadmap.md) -replace 'YOUR_USERNAME', '%GITHUB_USERNAME%' | Set-Content genai-roadmap.md"
powershell -Command "(Get-Content genai-roadmap.md) -replace 'YOUR_REPO_NAME', '%REPO_NAME%' | Set-Content genai-roadmap.md"

REM Update LICENSE
echo Updating LICENSE...
powershell -Command "(Get-Content LICENSE) -replace 'YOUR_NAME', '%FULL_NAME%' | Set-Content LICENSE"

REM Copy configuration template
echo Setting up configuration...
if not exist "config.env" (
    copy templates\config.env.template config.env
    echo ✓ Created config.env from template
) else (
    echo ⚠ config.env already exists, skipping
)

REM Copy MCP configuration template
if not exist ".cursor" mkdir .cursor
if not exist ".cursor\mcp.json" (
    copy templates\cursor-mcp.json.template .cursor\mcp.json
    echo ✓ Created .cursor\mcp.json from template
) else (
    echo ⚠ .cursor\mcp.json already exists, skipping
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit config.env with your API keys
echo 2. Run: python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt
echo 3. For local agent: cd projects\local-agent && scripts\start_local_agent.bat
echo 4. Open dashboard: python -m http.server 8000 (then visit http://localhost:8000/docs/)
echo.
echo Repository is now configured for: https://%GITHUB_USERNAME%.github.io/%REPO_NAME%
pause
