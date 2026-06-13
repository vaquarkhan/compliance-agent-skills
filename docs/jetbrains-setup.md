# JetBrains Setup

Install and build the **compliance-agent-skills** JetBrains plugin from `jetbrains-plugin/`.

## Prerequisites

- JDK 17+
- Gradle (wrapper included)

## Build

```bash
cd jetbrains-plugin
./gradlew buildPlugin        # Unix
.\gradlew.bat buildPlugin    # Windows
```

Output: `jetbrains-plugin/build/distributions/compliance-agent-skills-*.zip`

## Install in IDE

1. **Settings → Plugins → ⚙ → Install from Disk**
2. Select the built ZIP
3. Restart IDE

## Plugin actions

The plugin provides installer actions (see `InstallerActions.kt`):

- Copy skills to project resources
- Open preset and template directories
- Launch validation scripts

## Project integration

After install, open a project containing `AGENTS.md` and `skills/`. The plugin detects compliance-agent-skills layouts and offers quick actions from the tools menu.

## Python agent

Run the agent from PyCharm terminal:

```bash
pip install -r requirements.txt
python agent.py "Audit IAM for SOC 2 CC6.2"
```

Configure a Python run configuration pointing to `agent.py`.

## See also

- [jetbrains-plugin/README.md](../jetbrains-plugin/README.md)
- [plugin-publishing.md](plugin-publishing.md)
