# Skill Anatomy

How to author and maintain Agent Skills in `skills/*/SKILL.md`.

## Directory structure

```
skills/
└── my-skill-name/
    └── SKILL.md
```

Directory name **must match** frontmatter `name`.

## Required frontmatter

```yaml
---
name: my-skill-name
description: One-line trigger description with "Trigger when..." and "Do not use when..."
---
```

The description drives progressive disclosure — be specific about triggers and anti-triggers.

## Required sections

| Section | Purpose |
| --- | --- |
| `## Overview` | What the skill does, authoritative sources |
| `## When to Use` | Bulleted triggers and explicit exclusions |
| `## Core Process` | Numbered deterministic steps |
| Output artifacts (recommended) | Files produced, templates referenced |

Optional: `## MCP Integration`, `## Evidence`, `## Anti-patterns`

## Writing principles

1. **Deterministic steps** — cite CFR, PCI requirement numbers, or TSC IDs
2. **No invented controls** — if unsure, say "verify with qualified assessor"
3. **Progressive disclosure** — skill loads only when matched
4. **Cross-link** — reference templates in `templates/`, presets, examples

## Validation

```bash
python scripts/validate-skills.py
```

Checks frontmatter, section headers, and name/directory alignment.

## Registry

Add new skills to:

- [skills-index.md](../skills-index.md)
- [registry/assets.json](../registry/assets.json) (starter packs if applicable)

## Example

See [skills/using-compliance-agent-skills/SKILL.md](../skills/using-compliance-agent-skills/SKILL.md) as the canonical template.

## Agent integration

Skills are loaded by `agent.py` via `SkillsCapability(directories=["skills"])`. No code changes needed if frontmatter validates.
