# Templates

Copyable local configuration lives here. Files in this folder must stay safe to commit.

## Files

- `config.env.template` -> copy to root `config.env` for repo-level helper settings.
- `cursor-mcp.json.template` -> copy to `.cursor/mcp.json` for Cursor MCP integration.

## Local Files

The generated files are intentionally ignored by git:

- `config.env`
- `.cursor/`
- `.env`
- project-level `.env` files

Use blank values in templates and put real API keys only in ignored local files.
