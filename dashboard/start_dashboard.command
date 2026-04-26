#!/bin/zsh
APP_DIR="$HOME/Library/Application Support/GenAIRoadmapDashboard"
if [ -f "$APP_DIR/app.py" ]; then
  cd "$APP_DIR"
  exec /usr/bin/python3 app.py --open-browser
fi
cd "/Users/gautam/Documents/dev/gen ai roadmap"
exec /usr/bin/python3 app.py --open-browser
