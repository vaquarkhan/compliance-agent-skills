const vscode = require("vscode");
const fs = require("fs");
const path = require("path");
const https = require("https");

const DEFAULT_RAW_BASE_URL =
  "https://raw.githubusercontent.com/vaquarkhan/compliance-agent-skills/main";

function loadManifest(context) {
  const candidates = [
    path.join(context.extensionPath, "install-manifest.json"),
    path.resolve(context.extensionPath, "..", "registry", "install-manifest.json")
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      return JSON.parse(fs.readFileSync(candidate, "utf8"));
    }
  }
  throw new Error(
    "install-manifest.json not found. Reinstall the extension or clone the full repository."
  );
}

function manifestFiles(manifest) {
  return {
    core: manifest.core_files || [],
    skills: manifest.skill_files || [],
    adapters: manifest.agent_adapters || {},
    starterPacks: manifest.starter_packs || {},
    mcp: manifest.mcp_templates || {},
    examples: manifest.runnable_examples || {}
  };
}

function activate(context) {
  const manifest = loadManifest(context);
  const files = manifestFiles(manifest);

  context.subscriptions.push(
    vscode.commands.registerCommand("complianceAgentSkills.installFullToolkit", async () => {
      const root = getWorkspaceRoot();
      if (!root) return;
      const all = [
        ...files.core,
        ...files.skills,
        ...Object.values(files.adapters).flat(),
        ...Object.values(files.starterPacks).flat(),
        ...Object.values(files.mcp).flat(),
        "mcp/README.md"
      ];
      await installFiles(context, root, manifest, dedupe(all), "full toolkit");
    }),
    vscode.commands.registerCommand("complianceAgentSkills.installCorePack", async () => {
      const root = getWorkspaceRoot();
      if (!root) return;
      await installFiles(context, root, manifest, dedupe([...files.core, ...files.skills]), "core pack");
    }),
    vscode.commands.registerCommand("complianceAgentSkills.installAgentAdapters", async () => {
      const root = getWorkspaceRoot();
      if (!root) return;
      const choices = [...Object.keys(files.adapters), "All"];
      const picked = await vscode.window.showQuickPick(choices, {
        placeHolder: "Choose which agent adapters to install"
      });
      if (!picked) return;
      const selected =
        picked === "All" ? dedupe(Object.values(files.adapters).flat()) : files.adapters[picked];
      await installFiles(context, root, manifest, selected, `${picked} adapters`);
    }),
    vscode.commands.registerCommand("complianceAgentSkills.installStarterPack", async () => {
      const root = getWorkspaceRoot();
      if (!root) return;
      const picked = await vscode.window.showQuickPick(Object.keys(files.starterPacks), {
        placeHolder: "Choose a starter pack"
      });
      if (!picked) return;
      await installFiles(context, root, manifest, files.starterPacks[picked], `${picked} starter pack`);
    }),
    vscode.commands.registerCommand("complianceAgentSkills.installMcpTemplates", async () => {
      const root = getWorkspaceRoot();
      if (!root) return;
      const choices = [...Object.keys(files.mcp), "All"];
      const picked = await vscode.window.showQuickPick(choices, {
        placeHolder: "Choose MCP templates to install"
      });
      if (!picked) return;
      const selected =
        picked === "All"
          ? dedupe(["mcp/README.md", ...Object.values(files.mcp).flat()])
          : ["mcp/README.md", ...files.mcp[picked]];
      await installFiles(context, root, manifest, selected, `${picked} MCP templates`);
    }),
    vscode.commands.registerCommand("complianceAgentSkills.scaffoldRunnableExample", async () => {
      const root = getWorkspaceRoot();
      if (!root) return;
      const picked = await vscode.window.showQuickPick(Object.keys(files.examples), {
        placeHolder: "Choose a runnable example to scaffold"
      });
      if (!picked) return;
      await installFiles(context, root, manifest, files.examples[picked], `${picked} example`);
    })
  );
}

function deactivate() {}

function getWorkspaceRoot() {
  const folders = vscode.workspace.workspaceFolders;
  if (!folders || folders.length === 0) {
    vscode.window.showErrorMessage("Open a workspace folder before installing the skill pack.");
    return null;
  }
  return folders[0].uri.fsPath;
}

async function installFiles(context, workspaceRoot, manifest, relativePaths, label) {
  const collisions = [];
  for (const relativePath of relativePaths) {
    const targetPath = path.join(workspaceRoot, relativePath);
    if (fs.existsSync(targetPath)) {
      collisions.push(relativePath);
    }
  }

  let overwrite = false;
  if (collisions.length > 0) {
    const choice = await vscode.window.showWarningMessage(
      `${collisions.length} file(s) already exist for ${label}. Overwrite them?`,
      { modal: true },
      "Overwrite",
      "Skip Existing",
      "Cancel"
    );
    if (choice === "Cancel" || !choice) return;
    overwrite = choice === "Overwrite";
  }

  const installed = [];
  const skipped = [];

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: `Installing ${label}`,
      cancellable: false
    },
    async (progress) => {
      for (let i = 0; i < relativePaths.length; i++) {
        const relativePath = relativePaths[i];
        progress.report({
          message: relativePath,
          increment: 100 / relativePaths.length
        });

        const targetPath = path.join(workspaceRoot, relativePath);
        if (fs.existsSync(targetPath) && !overwrite) {
          skipped.push(relativePath);
          continue;
        }

        const content = await loadAsset(context, manifest, relativePath);
        await fs.promises.mkdir(path.dirname(targetPath), { recursive: true });
        await fs.promises.writeFile(targetPath, content, "utf8");
        installed.push(relativePath);
      }
    }
  );

  const parts = [`Installed ${installed.length} file(s) for ${label}.`];
  if (skipped.length > 0) {
    parts.push(`Skipped ${skipped.length} existing file(s).`);
  }
  vscode.window.showInformationMessage(parts.join(" "));
}

async function loadAsset(context, manifest, relativePath) {
  const localCandidates = [
    path.resolve(context.extensionPath, "..", relativePath),
    path.join(context.extensionPath, "resources", relativePath)
  ];

  for (const candidate of localCandidates) {
    if (fs.existsSync(candidate)) {
      return fs.promises.readFile(candidate, "utf8");
    }
  }

  const config = vscode.workspace.getConfiguration("complianceAgentSkills");
  const rawBaseUrl = config.get("rawBaseUrl", manifest.raw_base_url || DEFAULT_RAW_BASE_URL);
  const url = `${String(rawBaseUrl).replace(/\/$/, "")}/${relativePath.replace(/\\/g, "/")}`;
  return downloadText(url);
}

function downloadText(url) {
  return new Promise((resolve, reject) => {
    https
      .get(url, (response) => {
        if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
          resolve(downloadText(response.headers.location));
          return;
        }
        if (response.statusCode !== 200) {
          reject(new Error(`Failed to download ${url}: ${response.statusCode}`));
          return;
        }
        const chunks = [];
        response.on("data", (chunk) => chunks.push(chunk));
        response.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
      })
      .on("error", reject);
  });
}

function dedupe(items) {
  return [...new Set(items)];
}

module.exports = { activate, deactivate };
