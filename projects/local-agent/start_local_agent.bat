@echo off
REM Local Agent MCP Server — Windows Startup Script

REM Get script directory and project root
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."

REM Configurable base directory for MCP server
if "%MCP_BASE_DIR%"=="" set "MCP_BASE_DIR=%SCRIPT_DIR%"

set "VENV_DIR=%MCP_BASE_DIR%.venv"
set "PYTHON_BIN=%VENV_DIR%\Scripts\python.exe"
set "REQ_FILE=%MCP_BASE_DIR%requirements.txt"
set "SERVER_FILE=%MCP_BASE_DIR%mcp_server.py"

set "WORKSPACE_ROOT=%PROJECT_ROOT%"
if "%LOCAL_MODEL_BASE_URL%"=="" set "LOCAL_MODEL_BASE_URL=http://127.0.0.1:1234"

if not exist "%PYTHON_BIN%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

echo Installing/updating local-agent dependencies...
"%PYTHON_BIN%" -m pip install --upgrade pip >nul
"%PYTHON_BIN%" -m pip install -r "%REQ_FILE%" >nul

echo Starting MCP server...
echo LOCAL_MODEL_BASE_URL=%LOCAL_MODEL_BASE_URL%
"%PYTHON_BIN%" "%SERVER_FILE%"
