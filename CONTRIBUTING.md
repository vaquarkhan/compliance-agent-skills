# Contributing

Thank you for helping improve compliance-agent-skills. This repository supports deterministic USA compliance auditing for AI agent workflows—accuracy and traceability matter more than speed.

## How to contribute

1. **Fork and branch** from `main` using a descriptive name (`feat/soc2-cc7-log-samples`, `fix/presidio-entity-list`).
2. **Install locally** with `./bootstrap.sh` or `.\bootstrap.ps1`.
3. **Validate** before opening a PR:
   ```bash
   python scripts/validate-skills.py
   python scripts/validate-assets.py
   python scripts/validate-plugin-manifest.py
   ```
4. **Keep skills deterministic** — do not add steps that require the model to invent regulatory requirements. Cite CFR, PCI-DSS, or AICPA TSC references where applicable.
5. **Never commit real PHI, PAN, or production credentials.** Use synthetic fixtures in `examples/`.

## Skill authoring

See [docs/skill-anatomy.md](docs/skill-anatomy.md). Every skill must include YAML frontmatter (`name`, `description`) and sections: Overview, When to Use, Core Process, Output Artifacts.

## Commit messages

- Write clear, human-authored commit messages describing **why** the change was made.
- **Do not** add tool or vendor attribution lines (`Made-with: Cursor`, `Co-authored-by: Cursor`, `Made by Cursor Agent`, etc.).
- **Do not** mention AI coding assistants in commit bodies unless documenting a deliberate project workflow decision.

## Pull request checklist

- [ ] Skill validation passes (`python scripts/validate-skills.py`)
- [ ] Asset registry paths exist (`python scripts/validate-assets.py`)
- [ ] Plugin manifest in sync (`python scripts/validate-plugin-manifest.py`)
- [ ] No secrets or real regulated data in diffs
- [ ] No Cursor/vendor attribution in commits or PR description
- [ ] CHANGELOG updated for user-visible changes

## Code of conduct

Be respectful and professional. Compliance work often involves sensitive organizational context—treat issue reports and PR discussions as confidential unless the reporter opts into public discussion.
