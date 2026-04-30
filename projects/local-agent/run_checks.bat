@echo off
REM Local Agent — Windows Check Script

REM Get script directory and project root
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

REM Configurable base directory for MCP server
if "%MCP_BASE_DIR%"=="" set "MCP_BASE_DIR=%SCRIPT_DIR%"

set "VENV_PY=%MCP_BASE_DIR%.venv\Scripts\python.exe"
set "TEST_SCRIPT=%MCP_BASE_DIR%test_mcp.py"

if not exist "%VENV_PY%" (
    echo Missing venv Python at: %VENV_PY%
    echo Run: python -m venv %MCP_BASE_DIR%.venv ^&^& %MCP_BASE_DIR%.venv\Scripts\pip install -r %MCP_BASE_DIR%requirements.txt
    pause
    exit /b 1
)

echo Running local-agent smoke checks...
"%VENV_PY%" "%TEST_SCRIPT%"
echo All checks completed.
pause