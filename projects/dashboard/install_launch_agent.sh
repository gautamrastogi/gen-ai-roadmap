#!/bin/zsh
set -euo pipefail

LABEL="com.gautam.genai-roadmap-dashboard"
SOURCE_DIR="/Users/gautam/Documents/dev/gen ai roadmap"
APP_DIR="$HOME/Library/Application Support/GenAIRoadmapDashboard"
TARGET_DIR="$HOME/Library/LaunchAgents"
TARGET_PLIST="$TARGET_DIR/$LABEL.plist"
APP_BUNDLE_DIR="$HOME/Applications/GenAI Roadmap Dashboard.app"
APP_SCRIPT_PATH="$APP_DIR/open_dashboard.applescript"
PYTHON_BIN="/usr/bin/python3"

mkdir -p "$TARGET_DIR"
mkdir -p "$APP_DIR"

cp "$SOURCE_DIR/app.py" "$APP_DIR/app.py"
cp "$SOURCE_DIR/dashboard.html" "$APP_DIR/dashboard.html"
chmod +x "$APP_DIR/app.py"
mkdir -p "$HOME/Applications"

cat > "$TARGET_PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$LABEL</string>
  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON_BIN</string>
    <string>$APP_DIR/app.py</string>
    <string>--host</string>
    <string>127.0.0.1</string>
    <string>--port</string>
    <string>8765</string>
    <string>--open-browser</string>
  </array>
  <key>WorkingDirectory</key>
  <string>$APP_DIR</string>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>$APP_DIR/launchd.out.log</string>
  <key>StandardErrorPath</key>
  <string>$APP_DIR/launchd.err.log</string>
</dict>
</plist>
EOF

launchctl unload "$TARGET_PLIST" >/dev/null 2>&1 || true
launchctl load "$TARGET_PLIST"

cat > "$APP_SCRIPT_PATH" <<EOF
on run
  do shell script "if ! /usr/bin/curl -fsS http://127.0.0.1:8765/healthz >/dev/null 2>&1; then nohup $PYTHON_BIN " & quoted form of POSIX path of "$APP_DIR/app.py" & " --host 127.0.0.1 --port 8765 >/tmp/genai-roadmap-dashboard.manual.out 2>/tmp/genai-roadmap-dashboard.manual.err & fi"
  open location "http://127.0.0.1:8765/"
end run
EOF

/usr/bin/osacompile -o "$APP_BUNDLE_DIR" "$APP_SCRIPT_PATH"

echo "Installed and loaded $LABEL"
echo "Dashboard will start at login on http://127.0.0.1:8765/"
echo "Spotlight app created at $APP_BUNDLE_DIR"
