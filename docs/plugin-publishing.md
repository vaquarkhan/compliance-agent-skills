# Plugin publishing — VS Code Marketplace & JetBrains Marketplace

Manual publish steps for **Compliance Agent Skills** v1.6.0+.

## Before you publish

1. Bump version everywhere (or run `make sync-version` after editing `VERSION`).
2. Validate: `make validate`
3. Build artifacts (below).
4. Tag and push: `git tag v1.6.0 && git push origin v1.6.0`
5. Create a [GitHub Release](https://github.com/vaquarkhan/compliance-agent-skills/releases/new) and attach:
   - `vscode-extension/compliance-agent-skills-1.6.0.vsix`
   - `jetbrains-plugin/build/distributions/*.zip`

---

## Build artifacts locally

### VS Code (`.vsix`)

```powershell
cd vscode-extension
npm install -g @vscode/vsce
vsce package --no-dependencies
# Output: compliance-agent-skills-1.6.0.vsix
```

> **Note:** Do not set both `"files"` in `package.json` and `.vscodeignore` — VSCE rejects that. This repo uses `.vscodeignore` only.

### JetBrains (`.zip`)

```powershell
cd jetbrains-plugin
.\gradlew.bat buildPlugin    # Windows
# ./gradlew buildPlugin      # macOS/Linux
# Output: build/distributions/Compliance Agent Skills-1.6.0.zip
```

Requires **JDK 17+**. First run downloads the IntelliJ SDK (may take several minutes).

---

## VS Code Marketplace (manual — website)

### One-time setup

1. Create a [Microsoft Partner Center](https://partner.microsoft.com/) account (free).
2. Create a **Publisher** (e.g. `vaquarkhan`) — must match `"publisher"` in `package.json`.
3. Create a [Personal Access Token](https://dev.azure.com/) with **Marketplace → Manage** scope, or use Azure DevOps PAT for VS Marketplace.
4. Alternatively use [Visual Studio Marketplace publisher management](https://marketplace.visualstudio.com/manage).

### Publish via web UI

1. Open [Manage Publishers](https://marketplace.visualstudio.com/managepublishers).
2. Select publisher **vaquarkhan** (or create it).
3. Click **New extension** → **Visual Studio Code**.
4. Choose **Upload** and select `compliance-agent-skills-1.6.0.vsix`.
5. Fill in:
   - **Display name:** Compliance Agent Skills
   - **Description:** (from `vscode-extension/package.json`)
   - **Categories:** Other
   - **Tags:** compliance, hipaa, pci-dss, soc2, agent-skills, …
   - **License:** MIT
   - **Repository:** https://github.com/vaquarkhan/compliance-agent-skills
6. Add **HIPAA / not legal advice** disclaimer in the listing description (see root `README.md`).
7. Submit for **review** (usually 1–3 business days for first publish).

### Publish via CLI (optional)

```powershell
$env:VSCE_PAT = "<your-marketplace-pat>"
cd vscode-extension
vsce publish --no-dependencies
```

Docs: [Publishing Extensions](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)

---

## JetBrains Marketplace (manual — website)

### One-time setup

1. Sign in at [JetBrains Marketplace](https://plugins.jetbrains.com/) with your JetBrains account.
2. Open [Vendor Dashboard](https://plugins.jetbrains.com/author/me).
3. Create a **Plugin** entry (if first time): name **Compliance Agent Skills**, ID `com.complianceagent.skills`.

### Plugin signing (required for Marketplace)

JetBrains requires a signed plugin for public listing.

1. Generate a certificate (once):

   ```powershell
   cd jetbrains-plugin
   .\gradlew.bat signPlugin
   ```

   Set environment variables first (see [JetBrains docs](https://plugins.jetbrains.com/docs/intellij/tools-intellij-platform-gradle-plugin-signing.html)):

   - `JETBRAINS_CERTIFICATE_CHAIN` — cert chain from `certificates.pem`
   - `JETBRAINS_PRIVATE_KEY` — private key
   - `JETBRAINS_PRIVATE_KEY_PASSWORD` — key password

   Or use JetBrains **Plugin Signing** in the vendor portal to upload an unsigned build and sign there (if offered for your account tier).

2. Build signed distribution:

   ```powershell
   .\gradlew.bat buildPlugin signPlugin
   ```

### Publish via web UI

1. Go to [plugins.jetbrains.com/author/me](https://plugins.jetbrains.com/author/me).
2. Select **Compliance Agent Skills** → **Upload new version**.
3. Upload the ZIP from `build/distributions/Compliance Agent Skills-1.6.0.zip`.
4. Set **Change notes** from `CHANGELOG.md` (v1.6.0 section).
5. Set **Compatible IDE builds:** 241+ (see `sinceBuild` in `build.gradle.kts`).
6. Submit for review.

### Publish via CLI (optional)

```powershell
$env:JETBRAINS_MARKETPLACE_TOKEN = "<token from JetBrains Account → Marketplace → Tokens>"
cd jetbrains-plugin
.\gradlew.bat publishPlugin
```

Get token: [Account Settings → Marketplace → Tokens](https://plugins.jetbrains.com/author/me?tab=tokens)

Docs: [Publishing Plugin](https://plugins.jetbrains.com/docs/intellij/publishing-plugin.html)

---

## GitHub release (recommended alongside marketplaces)

1. **Releases** → **Draft a new release**
2. **Tag:** `v1.6.0` (target `main`)
3. **Title:** `v1.6.0 — Engineering hardening & plugin release`
4. Paste `CHANGELOG.md` section for 1.6.0
5. Attach:
   - `compliance-agent-skills-1.6.0.vsix`
   - `Compliance Agent Skills-1.6.0.zip`
6. Publish release

Users can install VSIX manually: **Extensions** → **⋯** → **Install from VSIX…**

JetBrains: **Settings → Plugins → ⚙ → Install Plugin from Disk…**

---

## Version checklist

| File | Field |
|------|--------|
| `VERSION` | `1.6.0` |
| `vscode-extension/package.json` | `"version"` |
| `jetbrains-plugin/gradle.properties` | `pluginVersion` |
| `registry/assets.json` | `"version"` |
| `CITATION.cff` | `version` |
| `CHANGELOG.md` | `[1.6.0]` section |

Run: `python scripts/sync-version.py`

---

## Security pre-publish

Confirm installers do **not**:

- Write outside project/user config directories
- Embed API keys or tokens
- Disable PHI redaction by default

See [SECURITY.md](../SECURITY.md).
