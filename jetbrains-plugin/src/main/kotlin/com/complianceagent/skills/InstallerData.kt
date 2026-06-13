package com.complianceagent.skills

import com.google.gson.Gson
import com.google.gson.annotations.SerializedName
import java.io.InputStreamReader

private data class InstallManifest(
    @SerializedName("raw_base_url") val rawBaseUrl: String,
    @SerializedName("core_files") val coreFiles: List<String>,
    @SerializedName("skill_files") val skillFiles: List<String>,
    @SerializedName("agent_adapters") val agentAdapters: Map<String, List<String>>,
    @SerializedName("starter_packs") val starterPacks: Map<String, List<String>>,
    @SerializedName("mcp_templates") val mcpTemplates: Map<String, List<String>>,
    @SerializedName("runnable_examples") val runnableExamples: Map<String, List<String>>,
)

object InstallerData {
    private val manifest: InstallManifest by lazy { loadManifest() }

    const val RAW_BASE_URL: String =
        "https://raw.githubusercontent.com/vaquarkhan/compliance-agent-skills/main"

    val coreFiles: List<String> get() = manifest.coreFiles
    val skillFiles: List<String> get() = manifest.skillFiles
    val agentAdapters: Map<String, List<String>> get() = manifest.agentAdapters
    val starterPacks: Map<String, List<String>> get() = manifest.starterPacks
    val mcpTemplates: Map<String, List<String>> get() = manifest.mcpTemplates
    val runnableExamples: Map<String, List<String>> get() = manifest.runnableExamples

    private fun loadManifest(): InstallManifest {
        val stream = InstallerData::class.java.getResourceAsStream("/install-manifest.json")
            ?: error("install-manifest.json missing from plugin resources")
        InputStreamReader(stream, Charsets.UTF_8).use { reader ->
            return Gson().fromJson(reader, InstallManifest::class.java)
        }
    }
}
