#!/usr/bin/env bash
# GenAI Roadmap — Setup Script
# Makes the repository ready for personal use

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 GenAI Developer Roadmap 2026 — Setup${NC}"
echo "========================================"

# Get user information
read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter your repository name (default: gen-ai-roadmap): " REPO_NAME
REPO_NAME=${REPO_NAME:-gen-ai-roadmap}
read -p "Enter your full name: " FULL_NAME

echo -e "\n${YELLOW}Configuring repository for:${NC}"
echo "  GitHub Username: $GITHUB_USERNAME"
echo "  Repository: $REPO_NAME"
echo "  Full Name: $FULL_NAME"
echo ""

# Update README.md URLs
echo -e "${BLUE}Updating README.md...${NC}"
sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" README.md
sed -i.bak "s/YOUR_REPO_NAME/$REPO_NAME/g" README.md

# Update dashboard HTML
echo -e "${BLUE}Updating dashboard HTML...${NC}"
sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" docs/index.html
sed -i.bak "s/YOUR_REPO_NAME/$REPO_NAME/g" docs/index.html

# Update genai-roadmap.md
echo -e "${BLUE}Updating roadmap metadata...${NC}"
sed -i.bak "s/YOUR_NAME/$FULL_NAME/g" genai-roadmap.md
sed -i.bak "s/YOUR_USERNAME/$GITHUB_USERNAME/g" genai-roadmap.md
sed -i.bak "s/YOUR_REPO_NAME/$REPO_NAME/g" genai-roadmap.md

# Update LICENSE
echo -e "${BLUE}Updating LICENSE...${NC}"
sed -i.bak "s/YOUR_NAME/$FULL_NAME/g" LICENSE

# Copy configuration template
echo -e "${BLUE}Setting up configuration...${NC}"
if [[ ! -f "config.env" ]]; then
    cp templates/config.env.template config.env
    echo -e "${GREEN}✓ Created config.env from template${NC}"
else
    echo -e "${YELLOW}⚠ config.env already exists, skipping${NC}"
fi

# Copy MCP configuration template
mkdir -p .cursor
if [[ ! -f ".cursor/mcp.json" ]]; then
    cp templates/cursor-mcp.json.template .cursor/mcp.json
    echo -e "${GREEN}✓ Created .cursor/mcp.json from template${NC}"
else
    echo -e "${YELLOW}⚠ .cursor/mcp.json already exists, skipping${NC}"
fi

# Clean up backup files
echo -e "${BLUE}Cleaning up...${NC}"
find . -name "*.bak" -delete

echo -e "\n${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Edit config.env with your API keys"
echo "2. Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
echo "3. For local agent: cd projects/local-agent && ./scripts/start_local_agent.sh"
echo "4. Open dashboard: python3 -m http.server 8000 (then visit http://localhost:8000/docs/)"
echo ""
echo -e "${BLUE}Repository is now configured for: https://$GITHUB_USERNAME.github.io/$REPO_NAME/${NC}"
