# Plugin Publishing

Release process for **VS Code extension** and **JetBrains plugin**.

## Versioning

Follow semver aligned with repository tags. Update:

- `CHANGELOG.md`
- `vscode-extension/package.json` → `version`
- `jetbrains-plugin/gradle.properties` → `pluginVersion`
- `registry/assets.json` → `version`

## VS Code extension

```bash
cd vscode-extension
npm install
npm test                    # if tests exist
npx vsce package
npx vsce publish            # requires VSCE_PAT
```

### Marketplace checklist

- [ ] README with HIPAA/PCI/SOC 2 scope disclaimer
- [ ] Icon and license MIT
- [ ] No secrets in `extension.js`

## JetBrains plugin

```bash
cd jetbrains-plugin
./gradlew buildPlugin
./gradlew publishPlugin     # requires PUBLISH_TOKEN
```

### Marketplace checklist

- [ ] `plugin.xml` description and change notes
- [ ] Signed plugin (JetBrains signing cert)
- [ ] Compatible IDE builds range in `gradle.properties`

## Pre-release validation

```bash
python scripts/validate-skills.py
python scripts/validate-assets.py
./bootstrap.sh --dry-run
```

## GitHub release

Attach:

- `.vsix` file
- JetBrains plugin ZIP
- Source tarball

Tag: `v1.0.0`

## Security review

Before publish, confirm installers do not:

- Write outside project/user config dirs
- Embed API keys or tokens
- Disable PHI redaction by default

See [SECURITY.md](../SECURITY.md).
