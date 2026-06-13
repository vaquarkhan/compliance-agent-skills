# VS Code Setup

Install compliance-agent-skills for **VS Code** and **GitHub Copilot**.

## Extension install

### From source

```bash
cd vscode-extension
npm install
npx vsce package
code --install-extension compliance-agent-skills-*.vsix
```

### Bootstrap

```bash
./bootstrap.sh --target vscode
```

Installs Copilot instructions to `.github/copilot-instructions.md`.

## Copilot instructions

The file [.github/copilot-instructions.md](../.github/copilot-instructions.md) directs Copilot to:

- Route to compliance skills
- Enforce PHI redaction awareness
- Follow audit lifecycle commands

## Recommended extensions

- Python
- YAML
- GitHub Copilot

## Workspace settings (optional)

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "files.associations": {
    "*.mdc": "markdown"
  }
}
```

## Running validation

Use VS Code terminal:

```bash
python scripts/validate-skills.py
python scripts/validate-assets.py
```

## MCP

VS Code MCP support varies by version. Merge `mcp/*.mcp.json` when MCP is available in your Copilot/agent setup.

## See also

- [vscode-extension/README.md](../vscode-extension/README.md)
- [plugin-publishing.md](plugin-publishing.md)
