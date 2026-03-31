---
source: https://code.claude.com/docs/llms.txt
domain: code.claude.com
crawled_at: 2026-03-31T17:55:59Z
index_hash: 48031774ace2
page_count: 13
---

# code.claude.com — Documentation Taxonomy

Source: `https://code.claude.com/docs/llms.txt`
Crawled: 2026-03-31T17:55:59Z

## Index

```
# Claude Code Docs

## Docs

- [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams.md): Coordinate multiple Claude Code instances working together as a team, with shared tasks, inter-agent messaging, and centralized management.
- [Claude Code on Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock.md): Learn about configuring Claude Code through Amazon Bedrock, including setup, IAM configuration, and troubleshooting.
- [Track team usage with analytics](https://code.claude.com/docs/en/analytics.md): View Claude Code usage metrics, track adoption, and measure engineering velocity in the analytics dashboard.
- [Authentication](https://code.claude.com/docs/en/authentication.md): Log in to Claude Code and configure authentication for individuals, teams, and organizations.
- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices.md): Tips and patterns for getting the most out of Claude Code, from configuring your environment to scaling across parallel sessions.
- [Changelog](https://code.claude.com/docs/en/changelog.md): Release notes for Claude Code, including new features, improvements, and bug fixes by version.
- [Push events into a running session with channels](https://code.claude.com/docs/en/channels.md): Use channels to push messages, alerts, and webhooks into your Claude Code session from an MCP server. Forward CI results, chat messages, and monitoring events so Claude can react while you're away.
- [Channels reference](https://code.claude.com/docs/en/channels-reference.md): Build an MCP server that pushes webhooks, alerts, and chat messages into a Claude Code session. Reference for the channel contract: capability declaration, notification events, reply tools, sender gating, and permission relay.
- [Checkpointing](https://code.claude.com/docs/en/checkpointing.md): Track, rewind, and summarize Claude's edits and conversation to manage session state.
- [Use Claude Code with Chrome (beta)](https://code.claude.com/docs/en/chrome.md): Connect Claude Code to your Chrome browser to test web apps, debug with console logs, automate form filling, and extract data from web pages.
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md): Run Claude Code tasks asynchronously on secure cloud infrastructure
- [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory.md): Where Claude Code reads CLAUDE.md, settings.json, hooks, skills, commands, subagents, rules, and auto memory. Explore the .claude directory in your project and ~/.claude in your home directory.
- [CLI reference](https://code.claude.com/docs/en/cli-reference.md): Complete reference for Claude Code command-line interface, including commands and flags.
- [Code Review](https://code.claude.com/docs/en/code-review.md): Set up automated PR reviews that catch logic errors, security vulnerabilities, and regressions using multi-agent analysis of your full codebase
- [Built-in commands](https://code.claude.com/docs/en/commands.md): Complete reference for built-in commands available in Claude Code.
- [Common workflows](https://code.claude.com/docs/en/common-workflows.md): Step-by-step guides for exploring codebases, fixing bugs, refactoring, testing, and other everyday tasks with Claude Code.
- [Let Claude use your computer from the CLI](https://code.claude.com/docs/en/computer-use.md): Enable computer use in the Claude Code CLI so Claude can open apps, click, type, and see your screen on macOS. Test native apps, debug visual issues, and automate GUI-only tools without leaving your terminal.
- [Explore the context window](https://code.claude.com/docs/en/context-window.md): An interactive simulation of how Claude Code's context window fills during a session. See what loads automatically, what each file read costs, and when rules and hooks fire.
- [Manage costs effectively](https://code.claude.com/docs/en/costs.md): Track token usage, set team spend limits, and reduce Claude Code costs with context management, model selection, extended thinking settings, and preprocessing hooks.
- [Data usage](https://code.claude.com/docs/en/data-usage.md): Learn about Anthropic's data usage policies for Claude
- [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md): Get more out of Claude Code Desktop: computer use, Dispatch sessions from your phone, parallel sessions with Git isolation, visual diff review, app previews, PR monitoring, connectors, and enterprise configuration.
- [Get started with the desktop app](https://code.claude.com/docs/en/desktop-quickstart.md): Install Claude Code on desktop and start your first coding session
- [Development containers](https://code.claude.com/docs/en/devcontainer.md): Learn about the Claude Code development container for teams that need consistent, secure environments.
- [Discover and install prebuilt plugins through marketplaces](https://code.claude.com/docs/en/discover-plugins.md): Find and install plugins from marketplaces to extend Claude Code with new commands, agents, and capabilities.
- [Environment variables](https://code.claude.com/docs/en/env-vars.md): Complete reference for environment variables that control Claude Code behavior.
- [Speed up responses with fast mode](https://code.claude.com/docs/en/fast-mode.md): Get faster Opus 4.6 responses in Claude Code by toggling fast mode.
- [Extend Claude Code](https://code.claude.com/docs/en/features-overview.md): Understand when to use CLAUDE.md, Skills, subagents, hooks, MCP, and plugins.
- [Fullscreen rendering](https://code.claude.com/docs/en/fullscreen.md): Enable a smoother, flicker-free rendering mode with mouse support and stable memory usage in long conversations.
- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions.md): Learn about integrating Claude Code into your development workflow with Claude Code GitHub Actions
- [Claude Code with GitHub Enterprise Server](https://code.claude.com/docs/en/github-enterprise-server.md): Connect Claude Code to your self-hosted GitHub Enterprise Server instance for web sessions, code review, and plugin marketplaces.
- [Claude Code GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd.md): Learn about integrating Claude Code into your development workflow with GitLab CI/CD
- [Claude Code on Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai.md): Learn about configuring Claude Code through Google Vertex AI, including setup, IAM configuration, and troubleshooting.
- [Run Claude Code programmatically](https://code.claude.com/docs/en/headless.md): Use the Agent SDK to run Claude Code programmatically from the CLI, Python, or TypeScript.
- [Hooks reference](https://code.claude.com/docs/en/hooks.md): Reference for Claude Code hook events, configuration schema, JSON input/output formats, exit codes, async hooks, HTTP hooks, prompt hooks, and MCP tool hooks.
- [Automate workflows with hooks](https://code.claude.com/docs/en/hooks-guide.md): Run shell commands automatically when Claude Code edits files, finishes tasks, or needs input. Format code, send notifications, validate commands, and enforce project rules.
- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works.md): Understand the agentic loop, built-in tools, and how Claude Code interacts with your project.
- [Interactive mode](https://code.claude.com/docs/en/interactive-mode.md): Complete reference for keyboard shortcuts, input modes, and interactive features in Claude Code sessions.
- [JetBrains IDEs](https://code.claude.com/docs/en/jetbrains.md): Use Claude Code with JetBrains IDEs including IntelliJ, PyCharm, WebStorm, and more
- [Customize keyboard shortcuts](https://code.claude.com/docs/en/keybindings.md): Customize keyboard shortcuts in Claude Code with a keybindings configuration file.
- [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance.md): Legal agreements, compliance certifications, and security information for Claude Code.
- [LLM gateway configuration](https://code.claude.com/docs/en/llm-gateway.md): Learn how to configure Claude Code to work with LLM gateway solutions. Covers gateway requirements, authentication configuration, model selection, and provider-specific endpoint setup.
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp.md): Learn how to connect Claude Code to your tools with the Model Context Protocol.
- [How Claude remembers your project](https://code.claude.com/docs/en/memory.md): Give Claude persistent instructions with CLAUDE.md files, and let Claude accumulate learnings automatically with auto memory.
- [Claude Code on Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry.md): Learn about configuring Claude Code through Microsoft Foundry, including setup, configuration, and troubleshooting.
- [Model configuration](https://code.claude.com/docs/en/model-config.md): Learn about the Claude Code model configuration, including model aliases like `opusplan`
- [Monitoring](https://code.claude.com/docs/en/monitoring-usage.md): Learn how to enable and configure OpenTelemetry for Claude Code.
- [Enterprise network configuration](https://code.claude.com/docs/en/network-config.md): Configure Claude Code for enterprise environments with proxy servers, custom Certificate Authorities (CA), and mutual Transport Layer Security (mTLS) authentication.
- [Output styles](https://code.claude.com/docs/en/output-styles.md): Adapt Claude Code for uses beyond software engineering
- [Claude Code overview](https://code.claude.com/docs/en/overview.md): Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools. Available in your terminal, IDE, desktop app, and browser.
- [Choose a permission mode](https://code.claude.com/docs/en/permission-modes.md): Switch between supervised editing, read-only planning, and auto mode where a background classifier replaces manual permission prompts. Cycle modes with Shift+Tab in the CLI or use the mode selector in VS Code, Desktop, and claude.ai.
- [Configure permissions](https://code.claude.com/docs/en/permissions.md): Control what Claude Code can access and do with fine-grained permission rules, modes, and managed policies.
- [Platforms and integrations](https://code.claude.com/docs/en/platforms.md): Choose where to run Claude Code and what to connect it to. Compare the CLI, Desktop, VS Code, JetBrains, web, and integrations like Chrome, Slack, and CI/CD.
- [Create and distribute a plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces.md): Build and host plugin marketplaces to distribute Claude Code extensions across teams and communities.
- [Create plugins](https://code.claude.com/docs/en/plugins.md): Create custom plugins to extend Claude Code with skills, agents, hooks, and MCP servers.
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference.md): Complete technical reference for Claude Code plugin system, including schemas, CLI commands, and component specifications.
- [Quickstart](https://code.claude.com/docs/en/quickstart.md): Welcome to Claude Code!
- [Continue local sessions from any device with Remote Control](https://code.claude.com/docs/en/remote-control.md): Continue a local Claude Code session from your phone, tablet, or any browser using Remote Control. Works with claude.ai/code and the Claude mobile app.
- [Sandboxing](https://code.claude.com/docs/en/sandboxing.md): Learn how Claude Code's sandboxed bash tool provides filesystem and network isolation for safer, more autonomous agent execution.
- [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks.md): Use /loop and the cron scheduling tools to run prompts repeatedly, poll for status, or set one-time reminders within a Claude Code session.
- [Security](https://code.claude.com/docs/en/security.md): Learn about Claude Code's security safeguards and best practices for safe usage.
- [Configure server-managed settings (public beta)](https://code.claude.com/docs/en/server-managed-settings.md): Centrally configure Claude Code for your organization through server-delivered settings, without requiring device management infrastructure.
- [Claude Code settings](https://code.claude.com/docs/en/settings.md): Configure Claude Code with global and project-level settings, and environment variables.
- [Advanced setup](https://code.claude.com/docs/en/setup.md): System requirements, platform-specific installation, version management, and uninstallation for Claude Code.
- [Extend Claude with skills](https://code.claude.com/docs/en/skills.md): Create, manage, and share skills to extend Claude's capabilities in Claude Code. Includes custom commands and bundled skills.
- [Claude Code in Slack](https://code.claude.com/docs/en/slack.md): Delegate coding tasks directly from your Slack workspace
- [Customize your status line](https://code.claude.com/docs/en/statusline.md): Configure a custom status bar to monitor context window usage, costs, and git status in Claude Code
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents.md): Create and use specialized AI subagents in Claude Code for task-specific workflows and improved context management.
- [Optimize your terminal setup](https://code.claude.com/docs/en/terminal-config.md): Claude Code works best when your terminal is properly configured. Follow these guidelines to optimize your experience.
- [Enterprise deployment overview](https://code.claude.com/docs/en/third-party-integrations.md): Learn how Claude Code can integrate with various third-party services and infrastructure to meet enterprise deployment requirements.
- [Tools reference](https://code.claude.com/docs/en/tools-reference.md): Complete reference for the tools Claude Code can use, including permission requirements.
- [Troubleshooting](https://code.claude.com/docs/en/troubleshooting.md): Discover solutions to common issues with Claude Code installation and usage.
- [Voice dictation](https://code.claude.com/docs/en/voice-dictation.md): Use push-to-talk voice dictation to speak your prompts instead of typing them in the Claude Code CLI.
- [Use Claude Code in VS Code](https://code.claude.com/docs/en/vs-code.md): Install and configure the Claude Code extension for VS Code. Get AI coding assistance with inline diffs, @-mentions, plan review, and keyboard shortcuts.
- [Schedule tasks on the web](https://code.claude.com/docs/en/web-scheduled-tasks.md): Automate recurring work with cloud scheduled tasks
- [Zero data retention](https://code.claude.com/docs/en/zero-data-retention.md): Learn about Zero Data Retention (ZDR) for Claude Code on Claude for Enterprise, including scope, disabled features, and how to request enablement.
```

## Pages

### tools-reference

URL: https://code.claude.com/docs/en/tools-reference
Hash: c7746913905f

```
Tools reference - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Reference

Tools reference




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Reference


 [/docs/en/cli-reference] 

CLI reference


 [/docs/en/commands] 

Built-in commands


 [/docs/en/env-vars] 

Environment variables


 [/docs/en/tools-reference] 

Tools reference


 [/docs/en/interactive-mode] 

Interactive mode


 [/docs/en/checkpointing] 

Checkpointing


 [/docs/en/hooks] 

Hooks reference


 [/docs/en/plugins-reference] 

Plugins reference


 [/docs/en/channels-reference] 

Channels reference











On this page

 [#bash-tool-behavior] Bash tool behavior
 [#powershell-tool] PowerShell tool
 [#enable-the-powershell-tool] Enable the PowerShell tool
 [#shell-selection-in-settings-hooks-and-skills] Shell selection in settings, hooks, and skills
 [#preview-limitations] Preview limitations
 [#see-also] See also

























Claude Code has access to a set of tools that help it understand and modify your codebase. The tool names below are the exact strings you use in  [/docs/en/permissions#tool-specific-permission-rules] permission rules,  [/docs/en/sub-agents] subagent tool lists, and  [/docs/en/hooks] hook matchers.



ToolDescriptionPermission Required
AgentSpawns a  [/docs/en/sub-agents] subagent with its own context window to handle a taskNo
AskUserQuestionAsks multiple-choice questions to gather requirements or clarify ambiguityNo
BashExecutes shell commands in your environment. See  [#bash-tool-behavior] Bash tool behaviorYes
CronCreateSchedules a recurring or one-shot prompt within the current session (gone when Claude exits). See  [/docs/en/scheduled-tasks] scheduled tasksNo
CronDeleteCancels a scheduled task by IDNo
CronListLists all scheduled tasks in the sessionNo
EditMakes targeted edits to specific filesYes
EnterPlanModeSwitches to plan mode to design an approach before codingNo
EnterWorktreeCreates an isolated  [/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees] git worktree and switches into itNo
ExitPlanModePresents a plan for approval and exits plan modeYes
ExitWorktreeExits a worktree session and returns to the original directoryNo
GlobFinds files based on pattern matchingNo
GrepSearches for patterns in file contentsNo
ListMcpResourcesToolLists resources exposed by connected  [/docs/en/mcp] MCP serversNo
LSPCode intelligence via language servers. Reports type errors and warnings automatically after file edits. Also supports navigation operations: jump to definitions, find references, get type info, list symbols, find implementations, trace call hierarchies. Requires a  [/docs/en/discover-plugins#code-intelligence] code intelligence plugin and its language server binaryNo
NotebookEditModifies Jupyter notebook cellsYes
PowerShellExecutes PowerShell commands on Windows. Opt-in preview. See  [#powershell-tool] PowerShell toolYes
ReadReads the contents of filesNo
ReadMcpResourceToolReads a specific MCP resource by URINo
SkillExecutes a  [/docs/en/skills#control-who-invokes-a-skill] skill within the main conversationYes
TaskCreateCreates a new task in the task listNo
TaskGetRetrieves full details for a specific taskNo
TaskListLists all tasks with their current statusNo
TaskOutput(Deprecated) Retrieves output from a background task. Prefer Read on the task’s output file pathNo
TaskStopKills a running background task by IDNo
TaskUpdateUpdates task status, dependencies, details, or deletes tasksNo
TodoWriteManages the session task checklist. Available in non-interactive mode and the  [/docs/en/headless] Agent SDK; interactive sessions use TaskCreate, TaskGet, TaskList, and TaskUpdate insteadNo
ToolSearchSearches for and loads deferred tools when  [/docs/en/mcp#scale-with-mcp-tool-search] tool search is enabledNo
WebFetchFetches content from a specified URLYes
WebSearchPerforms web searchesYes
WriteCreates or overwrites filesYes



Permission rules can be configured using /permissions or in  [/docs/en/settings#available-settings] permission settings. Also see  [/docs/en/permissions#tool-specific-permission-rules] Tool-specific permission rules.


 [#bash-tool-behavior] ​


Bash tool behavior

The Bash tool runs each command in a separate process with the following persistence behavior:


Working directory persists across commands. Set CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1 to reset to the project directory after each command.

Environment variables do not persist. An export in one command will not be available in the next.

Activate your virtualenv or conda environment before launching Claude Code. To make environment variables persist across Bash commands, set  [/docs/en/env-vars] CLAUDE_ENV_FILE to a shell script before launching Claude Code, or use a  [/docs/en/hooks#persist-environment-variables] SessionStart hook to populate it dynamically.


 [#powershell-tool] ​


PowerShell tool

On Windows, Claude Code can run PowerShell commands natively instead of routing through Git Bash. This is an opt-in preview.


 [#enable-the-powershell-tool] ​


Enable the PowerShell tool

Set CLAUDE_CODE_USE_POWERSHELL_TOOL=1 in your environment or in settings.json:











{
  "env": {
    "CLAUDE_CODE_USE_POWERSHELL_TOOL": "1"
  }
}






Claude Code auto-detects pwsh.exe (PowerShell 7+) with a fallback to powershell.exe (PowerShell 5.1). The Bash tool remains registered alongside the PowerShell tool, so you may need to ask Claude to use PowerShell.


 [#shell-selection-in-settings-hooks-and-skills] ​


Shell selection in settings, hooks, and skills

Three additional settings control where PowerShell is used:


"defaultShell": "powershell" in  [/docs/en/settings#available-settings] settings.json: routes interactive ! commands through PowerShell. Requires the PowerShell tool to be enabled.

"shell": "powershell" on individual  [/docs/en/hooks#command-hook-fields] command hooks: runs that hook in PowerShell. Hooks spawn PowerShell directly, so this works regardless of CLAUDE_CODE_USE_POWERSHELL_TOOL.

shell: powershell in  [/docs/en/skills#frontmatter-reference] skill frontmatter: runs !`command` blocks in PowerShell. Requires the PowerShell tool to be enabled.



 [#preview-limitations] ​


Preview limitations

The PowerShell tool has the following known limitations during the preview:


Auto mode does not work with the PowerShell tool yet

PowerShell profiles are not loaded

Sandboxing is not supported

Only supported on native Windows, not WSL

Git Bash is still required to start Claude Code



 [#see-also] ​


See also



 [/docs/en/permissions] Permissions: permission system, rule syntax, and tool-specific patterns

 [/docs/en/sub-agents] Subagents: configure tool access for subagents

 [/docs/en/hooks-guide] Hooks: run custom commands before or after tool execution




Was this page helpful?


YesNo






 [/docs/en/env-vars] Environment variables [/docs/en/interactive-mode] Interactive mode





⌘I











 [/docs/en/overview] 
 [https://x.com/AnthropicAI]  [https://www.linkedin.com/company/anthropicresearch] 






 [https://www.anthropic.com/company]  [https://www.anthropic.com/careers]  [https://www.anthropic.com/economic-futures]  [https://www.anthropic.com/research]  [https://www.anthropic.com/news]  [https://trust.anthropic.com/]  [https://www.anthropic.com/transparency] 





 [https://www.anthropic.com/supported-countries]  [https://status.anthropic.com/]  [https://support.claude.com/] 





 [https://www.anthropic.com/learn]  [https://claude.com/partners/mcp]  [https://www.claude.com/customers]  [https://www.anthropic.com/engineering]  [https://www.anthropic.com/events]  [https://claude.com/partners/powered-by-claude]  [https://claude.com/partners/services]  [https://claude.com/programs/startups] 





 [#]  [https://www.anthropic.com/legal/privacy]  [https://www.anthropic.com/responsible-disclosure-policy]  [https://www.anthropic.com/legal/aup]  [https://www.anthropic.com/legal/commercial-terms]  [https://www.anthropic.com/legal/consumer-terms] 












Assistant









Responses are generated using AI and may contain mistakes.
```

### sub-agents

URL: https://code.claude.com/docs/en/sub-agents
Hash: bfac97eb4924

```
Create custom subagents - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Agents

Create custom subagents




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Agents


 [/docs/en/sub-agents] 

Create custom subagents


 [/docs/en/agent-teams] 

Run agent teams





Tools and plugins


 [/docs/en/mcp] 

Model Context Protocol (MCP)


 [/docs/en/discover-plugins] 

Discover and install prebuilt plugins


 [/docs/en/plugins] 

Create plugins


 [/docs/en/skills] 

Extend Claude with skills





Automation


 [/docs/en/hooks-guide] 

Automate with hooks


 [/docs/en/channels] 

Push external events to Claude


 [/docs/en/scheduled-tasks] 

Run prompts on a schedule


 [/docs/en/headless] 

Programmatic usage





Troubleshooting


 [/docs/en/troubleshooting] 

Troubleshooting











On this page

 [#built-in-subagents] Built-in subagents
 [#quickstart-create-your-first-subagent] Quickstart: create your first subagent
 [#configure-subagents] Configure subagents
 [#use-the-%2Fagents-command] Use the /agents command
 [#choose-the-subagent-scope] Choose the subagent scope
 [#write-subagent-files] Write subagent files
 [#supported-frontmatter-fields] Supported frontmatter fields
 [#choose-a-model] Choose a model
 [#control-subagent-capabilities] Control subagent capabilities
 [#available-tools] Available tools
 [#restrict-which-subagents-can-be-spawned] Restrict which subagents can be spawned
 [#scope-mcp-servers-to-a-subagent] Scope MCP servers to a subagent
 [#permission-modes] Permission modes
 [#preload-skills-into-subagents] Preload skills into subagents
 [#enable-persistent-memory] Enable persistent memory
 [#conditional-rules-with-hooks] Conditional rules with hooks
 [#disable-specific-subagents] Disable specific subagents
 [#define-hooks-for-subagents] Define hooks for subagents
 [#hooks-in-subagent-frontmatter] Hooks in subagent frontmatter
 [#project-level-hooks-for-subagent-events] Project-level hooks for subagent events
 [#work-with-subagents] Work with subagents
 [#understand-automatic-delegation] Understand automatic delegation
 [#invoke-subagents-explicitly] Invoke subagents explicitly
 [#run-subagents-in-foreground-or-background] Run subagents in foreground or background
 [#common-patterns] Common patterns
 [#isolate-high-volume-operations] Isolate high-volume operations
 [#run-parallel-research] Run parallel research
 [#chain-subagents] Chain subagents
 [#choose-between-subagents-and-main-conversation] Choose between subagents and main conversation
 [#manage-subagent-context] Manage subagent context
 [#resume-subagents] Resume subagents
 [#auto-compaction] Auto-compaction
 [#example-subagents] Example subagents
 [#code-reviewer] Code reviewer
 [#debugger] Debugger
 [#data-scientist] Data scientist
 [#database-query-validator] Database query validator
 [#next-steps] Next steps

























Subagents are specialized AI assistants that handle specific types of tasks. Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions. When Claude encounters a task that matches a subagent’s description, it delegates to that subagent, which works independently and returns results. To see the context savings in practice, the  [/docs/en/context-window] context window visualization walks through a session where a subagent handles research in its own separate window.




If you need multiple agents working in parallel and communicating with each other, see  [/docs/en/agent-teams] agent teams instead. Subagents work within a single session; agent teams coordinate across separate sessions.


Subagents help you:


Preserve context by keeping exploration and implementation out of your main conversation

Enforce constraints by limiting which tools a subagent can use

Reuse configurations across projects with user-level subagents

Specialize behavior with focused system prompts for specific domains

Control costs by routing tasks to faster, cheaper models like Haiku

Claude uses each subagent’s description to decide when to delegate tasks. When you create a subagent, write a clear description so Claude knows when to use it.
Claude Code includes several built-in subagents like Explore, Plan, and general-purpose. You can also create custom subagents to handle specific tasks. This page covers the  [#built-in-subagents] built-in subagents,  [#quickstart-create-your-first-subagent] how to create your own,  [#configure-subagents] full configuration options,  [#work-with-subagents] patterns for working with subagents, and  [#example-subagents] example subagents.


 [#built-in-subagents] ​


Built-in subagents

Claude Code includes built-in subagents that Claude automatically uses when appropriate. Each inherits the parent conversation’s permissions with additional tool restrictions.



 Explore


 Plan


 General-purpose


 Other


A fast, read-only agent optimized for searching and analyzing codebases.

Model: Haiku (fast, low-latency)

Tools: Read-only tools (denied access to Write and Edit tools)

Purpose: File discovery, code search, codebase exploration
Claude delegates to Explore when it needs to search or understand a codebase without making changes. This keeps exploration results out of your main conversation context.When invoking Explore, Claude specifies a thoroughness level: quick for targeted lookups, medium for balanced exploration, or very thorough for comprehensive analysis.

A research agent used during  [/docs/en/common-workflows#use-plan-mode-for-safe-code-analysis] plan mode to gather context before presenting a plan.

Model: Inherits from main conversation

Tools: Read-only tools (denied access to Write and Edit tools)

Purpose: Codebase research for planning
When you’re in plan mode and Claude needs to understand your codebase, it delegates research to the Plan subagent. This prevents infinite nesting (subagents cannot spawn other subagents) while still gathering necessary context.

A capable agent for complex, multi-step tasks that require both exploration and action.

Model: Inherits from main conversation

Tools: All tools

Purpose: Complex research, multi-step operations, code modifications
Claude delegates to general-purpose when the task requires both exploration and modification, complex reasoning to interpret results, or multiple dependent steps.

Claude Code includes additional helper agents for specific tasks. These are typically invoked automatically, so you don’t need to use them directly.


AgentModelWhen Claude uses it
BashInheritsRunning terminal commands in a separate context
statusline-setupSonnetWhen you run /statusline to configure your status line
Claude Code GuideHaikuWhen you ask questions about Claude Code features






Beyond these built-in subagents, you can create your own with custom prompts, tool restrictions, permission modes, hooks, and skills. The following sections show how to get started and customize subagents.


 [#quickstart-create-your-first-subagent] ​


Quickstart: create your first subagent

Subagents are defined in Markdown files with YAML frontmatter. You can  [#write-subagent-files] create them manually or use the /agents command.
This walkthrough guides you through creating a user-level subagent with the /agents command. The subagent reviews code and suggests improvements for the codebase.







1

 [#] 






Open the subagents interface

In Claude Code, run:










/agents














2

 [#] 






Choose a location

Select Create new agent, then choose Personal. This saves the subagent to ~/.claude/agents/ so it’s available in all your projects.








3

 [#] 






Generate with Claude

Select Generate with Claude. When prompted, describe the subagent:










A code improvement agent that scans files and suggests improvements
for readability, performance, and best practices. It should explain
each issue, show the current code, and provide an improved version.





Claude generates the identifier, description, and system prompt for you.








4

 [#] 






Select tools

For a read-only reviewer, deselect everything except Read-only tools. If you keep all tools selected, the subagent inherits all tools available to the main conversation.








5

 [#] 






Select model

Choose which model the subagent uses. For this example agent, select Sonnet, which balances capability and speed for analyzing code patterns.








6

 [#] 






Choose a color

Pick a background color for the subagent. This helps you identify which subagent is running in the UI.








7

 [#] 






Configure memory

Select User scope to give the subagent a  [#enable-persistent-memory] persistent memory directory at ~/.claude/agent-memory/. The subagent uses this to accumulate insights across conversations, such as codebase patterns and recurring issues. Select None if you don’t want the subagent to persist learnings.








8

 [#] 






Save and try it out

Review the configuration summary. Press s or Enter to save, or press e to save and edit the file in your editor. The subagent is available immediately. Try it:










Use the code-improver agent to suggest improvements in this project





Claude delegates to your new subagent, which scans the codebase and returns improvement suggestions.




You now have a subagent you can use in any project on your machine to analyze codebases and suggest improvements.
You can also create subagents manually as Markdown files, define them via CLI flags, or distribute them through plugins. The following sections cover all configuration options.


 [#configure-subagents] ​


Configure subagents



 [#use-the-/agents-command] ​


Use the /agents command

The /agents command provides an interactive interface for managing subagents. Run /agents to:


View all available subagents (built-in, user, project, and plugin)

Create new subagents with guided setup or Claude generation

Edit existing subagent configuration and tool access

Delete custom subagents

See which subagents are active when duplicates exist

This is the recommended way to create and manage subagents. For manual creation or automation, you can also add subagent files directly.
To list all configured subagents from the command line without starting an interactive session, run claude agents. This shows agents grouped by source and indicates which are overridden by higher-priority definitions.


 [#choose-the-subagent-scope] ​


Choose the subagent scope

Subagents are Markdown files with YAML frontmatter. Store them in different locations depending on scope. When multiple subagents share the same name, the higher-priority location wins.



LocationScopePriorityHow to create
--agents CLI flagCurrent session1 (highest)Pass JSON when launching Claude Code
.claude/agents/Current project2Interactive or manual
~/.claude/agents/All your projects3Interactive or manual
Plugin’s agents/ directoryWhere plugin is enabled4 (lowest)Installed with  [/docs/en/plugins] plugins



Project subagents (.claude/agents/) are ideal for subagents specific to a codebase. Check them into version control so your team can use and improve them collaboratively.
User subagents (~/.claude/agents/) are personal subagents available in all your projects.
CLI-defined subagents are passed as JSON when launching Claude Code. They exist only for that session and aren’t saved to disk, making them useful for quick testing or automation scripts. You can define multiple subagents in a single --agents call:











claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'






The --agents flag accepts JSON with the same  [#supported-frontmatter-fields] frontmatter fields as file-based subagents: description, prompt, tools, disallowedTools, model, permissionMode, mcpServers, hooks, maxTurns, skills, initialPrompt, memory, effort, background, and isolation. Use prompt for the system prompt, equivalent to the markdown body in file-based subagents.
Plugin subagents come from  [/docs/en/plugins] plugins you’ve installed. They appear in /agents alongside your custom subagents. See the  [/docs/en/plugins-reference#agents] plugin components reference for details on creating plugin subagents.




For security reasons, plugin subagents do not support the hooks, mcpServers, or permissionMode frontmatter fields. These fields are ignored when loading agents from a plugin. If you need them, copy the agent file into .claude/agents/ or ~/.claude/agents/. You can also add rules to  [/docs/en/settings#permission-settings] permissions.allow in settings.json or settings.local.json, but these rules apply to the entire session, not just the plugin subagent.


Subagent definitions from any of these scopes are also available to  [/docs/en/agent-teams#use-subagent-definitions-for-teammates] agent teams: when spawning a teammate, you can reference a subagent type and the teammate inherits its system prompt, tools, and model.


 [#write-subagent-files] ​


Write subagent files

Subagent files use YAML frontmatter for configuration, followed by the system prompt in Markdown:




Subagents are loaded at session start. If you create a subagent by manually adding a file, restart your session or use /agents to load it immediately.













---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.






The frontmatter defines the subagent’s metadata and configuration. The body becomes the system prompt that guides the subagent’s behavior. Subagents receive only this system prompt (plus basic environment details like working directory), not the full Claude Code system prompt.


 [#supported-frontmatter-fields] ​


Supported frontmatter fields

The following fields can be used in the YAML frontmatter. Only name and description are required.



FieldRequiredDescription
nameYesUnique identifier using lowercase letters and hyphens
descriptionYesWhen Claude should delegate to this subagent
toolsNo [#available-tools] Tools the subagent can use. Inherits all tools if omitted
disallowedToolsNoTools to deny, removed from inherited or specified list
modelNo [#choose-a-model] Model to use: sonnet, opus, haiku, a full model ID (for example, claude-opus-4-6), or inherit. Defaults to inherit
permissionModeNo [#permission-modes] Permission mode: default, acceptEdits, dontAsk, bypassPermissions, or plan
maxTurnsNoMaximum number of agentic turns before the subagent stops
skillsNo [/docs/en/skills] Skills to load into the subagent’s context at startup. The full skill content is injected, not just made available for invocation. Subagents don’t inherit skills from the parent conversation
mcpServersNo [/docs/en/mcp] MCP servers available to this subagent. Each entry is either a server name referencing an already-configured server (e.g., "slack") or an inline definition with the server name as key and a full  [/docs/en/mcp#configure-mcp-servers] MCP server config as value
hooksNo [#define-hooks-for-subagents] Lifecycle hooks scoped to this subagent
memoryNo [#enable-persistent-memory] Persistent memory scope: user, project, or local. Enables cross-session learning
backgroundNoSet to true to always run this subagent as a  [#run-subagents-in-foreground-or-background] background task. Default: false
effortNoEffort level when this subagent is active. Overrides the session effort level. Default: inherits from session. Options: low, medium, high, max (Opus 4.6 only)
isolationNoSet to worktree to run the subagent in a temporary  [/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees] git worktree, giving it an isolated copy of the repository. The worktree is automatically cleaned up if the subagent makes no changes
initialPromptNoAuto-submitted as the first user turn when this agent runs as the main session agent (via --agent or the agent setting).  [/docs/en/commands] Commands and  [/docs/en/skills] skills are processed. Prepended to any user-provided prompt





 [#choose-a-model] ​


Choose a model

The model field controls which  [/docs/en/model-config] AI model the subagent uses:


Model alias: Use one of the available aliases: sonnet, opus, or haiku

Full model ID: Use a full model ID such as claude-opus-4-6 or claude-sonnet-4-6. Accepts the same values as the --model flag

inherit: Use the same model as the main conversation

Omitted: If not specified, defaults to inherit (uses the same model as the main conversation)

When Claude invokes a subagent, it can also pass a model parameter for that specific invocation. Claude Code resolves the subagent’s model in this order:


The  [/docs/en/model-config#environment-variables] CLAUDE_CODE_SUBAGENT_MODEL environment variable, if set

The per-invocation model parameter

The subagent definition’s model frontmatter

The main conversation’s model



 [#control-subagent-capabilities] ​


Control subagent capabilities

You can control what subagents can do through tool access, permission modes, and conditional rules.


 [#available-tools] ​


Available tools

Subagents can use any of Claude Code’s  [/docs/en/tools-reference] internal tools. By default, subagents inherit all tools from the main conversation, including MCP tools.
To restrict tools, use either the tools field (allowlist) or the disallowedTools field (denylist). This example uses tools to exclusively allow Read, Grep, Glob, and Bash. The subagent can’t edit files, write files, or use any MCP tools:











---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---






This example uses disallowedTools to inherit every tool from the main conversation except Write and Edit. The subagent keeps Bash, MCP tools, and everything else:











---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---






If both are set, disallowedTools is applied first, then tools is resolved against the remaining pool. A tool listed in both is removed.


 [#restrict-which-subagents-can-be-spawned] ​


Restrict which subagents can be spawned

When an agent runs as the main thread with claude --agent, it can spawn subagents using the Agent tool. To restrict which subagent types it can spawn, use Agent(agent_type) syntax in the tools field.




In version 2.1.63, the Task tool was renamed to Agent. Existing Task(...) references in settings and agent definitions still work as aliases.













---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---






This is an allowlist: only the worker and researcher subagents can be spawned. If the agent tries to spawn any other type, the request fails and the agent sees only the allowed types in its prompt. To block specific agents while allowing all others, use  [#disable-specific-subagents] permissions.deny instead.
To allow spawning any subagent without restrictions, use Agent without parentheses:











tools: Agent, Read, Bash






If Agent is omitted from the tools list entirely, the agent cannot spawn any subagents. This restriction only applies to agents running as the main thread with claude --agent. Subagents cannot spawn other subagents, so Agent(agent_type) has no effect in subagent definitions.


 [#scope-mcp-servers-to-a-subagent] ​


Scope MCP servers to a subagent

Use the mcpServers field to give a subagent access to  [/docs/en/mcp] MCP servers that aren’t available in the main conversation. Inline servers defined here are connected when the subagent starts and disconnected when it finishes. String references share the parent session’s connection.
Each entry in the list is either an inline server definition or a string referencing an MCP server already configured in your session:











---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.






Inline definitions use the same schema as .mcp.json server entries (stdio, http, sse, ws), keyed by the server name.
To keep an MCP server out of the main conversation entirely and avoid its tool descriptions consuming context there, define it inline here rather than in .mcp.json. The subagent gets the tools; the parent conversation does not.


 [#permission-modes] ​


Permission modes

The permissionMode field controls how the subagent handles permission prompts. Subagents inherit the permission context from the main conversation and can override the mode, except when the parent mode takes precedence as described below.



ModeBehavior
defaultStandard permission checking with prompts
acceptEditsAuto-accept file edits
dontAskAuto-deny permission prompts (explicitly allowed tools still work)
bypassPermissionsSkip permission prompts
planPlan mode (read-only exploration)







Use bypassPermissions with caution. It skips permission prompts, allowing the subagent to execute operations without approval. Writes to .git, .claude, .vscode, and .idea directories still prompt for confirmation, except for .claude/commands, .claude/agents, and .claude/skills. See  [/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode] permission modes for details.


If the parent uses bypassPermissions, this takes precedence and cannot be overridden. If the parent uses  [/docs/en/permission-modes#eliminate-prompts-with-auto-mode] auto mode, the subagent inherits auto mode and any permissionMode in its frontmatter is ignored: the classifier evaluates the subagent’s tool calls with the same block and allow rules as the parent session.


 [#preload-skills-into-subagents] ​


Preload skills into subagents

Use the skills field to inject skill content into a subagent’s context at startup. This gives the subagent domain knowledge without requiring it to discover and load skills during execution.











---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.






The full content of each skill is injected into the subagent’s context, not just made available for invocation. Subagents don’t inherit skills from the parent conversation; you must list them explicitly.




This is the inverse of  [/docs/en/skills#run-skills-in-a-subagent] running a skill in a subagent. With skills in a subagent, the subagent controls the system prompt and loads skill content. With context: fork in a skill, the skill content is injected into the agent you specify. Both use the same underlying system.




 [#enable-persistent-memory] ​


Enable persistent memory

The memory field gives the subagent a persistent directory that survives across conversations. The subagent uses this directory to build up knowledge over time, such as codebase patterns, debugging insights, and architectural decisions.











---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.






Choose a scope based on how broadly the memory should apply:



ScopeLocationUse when
user~/.claude/agent-memory/<name-of-agent>/the subagent should remember learnings across all projects
project.claude/agent-memory/<name-of-agent>/the subagent’s knowledge is project-specific and shareable via version control
local.claude/agent-memory-local/<name-of-agent>/the subagent’s knowledge is project-specific but should not be checked into version control



When memory is enabled:


The subagent’s system prompt includes instructions for reading and writing to the memory directory.

The subagent’s system prompt also includes the first 200 lines or 25KB of MEMORY.md in the memory directory, whichever comes first, with instructions to curate MEMORY.md if it exceeds that limit.

Read, Write, and Edit tools are automatically enabled so the subagent can manage its memory files.


Persistent memory tips




project is the recommended default scope. It makes subagent knowledge shareable via version control. Use user when the subagent’s knowledge is broadly applicable across projects, or local when the knowledge should not be checked into version control.



Ask the subagent to consult its memory before starting work: “Review this PR, and check your memory for patterns you’ve seen before.”



Ask the subagent to update its memory after completing a task: “Now that you’re done, save what you learned to your memory.” Over time, this builds a knowledge base that makes the subagent more effective.



Include memory instructions directly in the subagent’s markdown file so it proactively maintains its own knowledge base:











Update your agent memory as you discover codepaths, patterns, library
locations, and key architectural decisions. This builds up institutional
knowledge across conversations. Write concise notes about what you found
and where.










 [#conditional-rules-with-hooks] ​


Conditional rules with hooks

For more dynamic control over tool usage, use PreToolUse hooks to validate operations before they execute. This is useful when you need to allow some operations of a tool while blocking others.
This example creates a subagent that only allows read-only database queries. The PreToolUse hook runs the script specified in command before each Bash command executes:











---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---






Claude Code  [/docs/en/hooks#pretooluse-input] passes hook input as JSON via stdin to hook commands. The validation script reads this JSON, extracts the Bash command, and  [/docs/en/hooks#exit-code-2-behavior-per-event] exits with code 2 to block write operations:











#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0






See  [/docs/en/hooks#pretooluse-input] Hook input for the complete input schema and  [/docs/en/hooks#exit-code-output] exit codes for how exit codes affect behavior.


 [#disable-specific-subagents] ​


Disable specific subagents

You can prevent Claude from using specific subagents by adding them to the deny array in your  [/docs/en/settings#permission-settings] settings. Use the format Agent(subagent-name) where subagent-name matches the subagent’s name field.











{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}






This works for both built-in and custom subagents. You can also use the --disallowedTools CLI flag:











claude --disallowedTools "Agent(Explore)"






See  [/docs/en/permissions#tool-specific-permission-rules] Permissions documentation for more details on permission rules.


 [#define-hooks-for-subagents] ​


Define hooks for subagents

Subagents can define  [/docs/en/hooks] hooks that run during the subagent’s lifecycle. There are two ways to configure hooks:


In the subagent’s frontmatter: Define hooks that run only while that subagent is active

In settings.json: Define hooks that run in the main session when subagents start or stop



 [#hooks-in-subagent-frontmatter] ​


Hooks in subagent frontmatter

Define hooks directly in the subagent’s markdown file. These hooks only run while that specific subagent is active and are cleaned up when it finishes.
All  [/docs/en/hooks#hook-events] hook events are supported. The most common events for subagents are:



EventMatcher inputWhen it fires
PreToolUseTool nameBefore the subagent uses a tool
PostToolUseTool nameAfter the subagent uses a tool
Stop(none)When the subagent finishes (converted to SubagentStop at runtime)



This example validates Bash commands with the PreToolUse hook and runs a linter after file edits with PostToolUse:











---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---






Stop hooks in frontmatter are automatically converted to SubagentStop events.


 [#project-level-hooks-for-subagent-events] ​


Project-level hooks for subagent events

Configure hooks in settings.json that respond to subagent lifecycle events in the main session.



EventMatcher inputWhen it fires
SubagentStartAgent type nameWhen a subagent begins execution
SubagentStopAgent type nameWhen a subagent completes



Both events support matchers to target specific agent types by name. This example runs a setup script only when the db-agent subagent starts, and a cleanup script when any subagent stops:











{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}






See  [/docs/en/hooks] Hooks for the complete hook configuration format.


 [#work-with-subagents] ​


Work with subagents



 [#understand-automatic-delegation] ​


Understand automatic delegation

Claude automatically delegates tasks based on the task description in your request, the description field in subagent configurations, and current context. To encourage proactive delegation, include phrases like “use proactively” in your subagent’s description field.


 [#invoke-subagents-explicitly] ​


Invoke subagents explicitly

When automatic delegation isn’t enough, you can request a subagent yourself. Three patterns escalate from a one-off suggestion to a session-wide default:


Natural language: name the subagent in your prompt; Claude decides whether to delegate

@-mention: guarantees the subagent runs for one task

Session-wide: the whole session uses that subagent’s system prompt, tool restrictions, and model via the --agent flag or the agent setting

For natural language, there’s no special syntax. Name the subagent and Claude typically delegates:











Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes






@-mention the subagent. Type @ and pick the subagent from the typeahead, the same way you @-mention files. This ensures that specific subagent runs rather than leaving the choice to Claude:











@"code-reviewer (agent)" look at the auth changes






Your full message still goes to Claude, which writes the subagent’s task prompt based on what you asked. The @-mention controls which subagent Claude invokes, not what prompt it receives.
Subagents provided by an enabled  [/docs/en/plugins] plugin appear in the typeahead as <plugin-name>:<agent-name>. You can also type the mention manually without using the picker: @agent-<name> for local subagents, or @agent-<plugin-name>:<agent-name> for plugin subagents.
Run the whole session as a subagent. Pass  [/docs/en/cli-reference] --agent <name> to start a session where the main thread itself takes on that subagent’s system prompt, tool restrictions, and model:











claude --agent code-reviewer






The subagent’s system prompt replaces the default Claude Code system prompt entirely, the same way  [/docs/en/cli-reference] --system-prompt does. CLAUDE.md files and project memory still load through the normal message flow. The agent name appears as @<name> in the startup header so you can confirm it’s active.
This works with built-in and custom subagents, and the choice persists when you resume the session.
For a plugin-provided subagent, pass the scoped name: claude --agent <plugin-name>:<agent-name>.
To make it the default for every session in a project, set agent in .claude/settings.json:











{
  "agent": "code-reviewer"
}






The CLI flag overrides the setting if both are present.


 [#run-subagents-in-foreground-or-background] ​


Run subagents in foreground or background

Subagents can run in the foreground (blocking) or background (concurrent):


Foreground subagents block the main conversation until complete. Permission prompts and clarifying questions (like  [/docs/en/tools-reference] AskUserQuestion) are passed through to you.

Background subagents run concurrently while you continue working. Before launching, Claude Code prompts for any tool permissions the subagent will need, ensuring it has the necessary approvals upfront. Once running, the subagent inherits these permissions and auto-denies anything not pre-approved. If a background subagent needs to ask clarifying questions, that tool call fails but the subagent continues.

If a background subagent fails due to missing permissions, you can start a new foreground subagent with the same task to retry with interactive prompts.
Claude decides whether to run subagents in the foreground or background based on the task. You can also:


Ask Claude to “run this in the background”

Press Ctrl+B to background a running task

To disable all background task functionality, set the CLAUDE_CODE_DISABLE_BACKGROUND_TASKS environment variable to 1. See  [/docs/en/env-vars] Environment variables.


 [#common-patterns] ​


Common patterns



 [#isolate-high-volume-operations] ​


Isolate high-volume operations

One of the most effective uses for subagents is isolating operations that produce large amounts of output. Running tests, fetching documentation, or processing log files can consume significant context. By delegating these to a subagent, the verbose output stays in the subagent’s context while only the relevant summary returns to your main conversation.











Use a subagent to run the test suite and report only the failing tests with their error messages








 [#run-parallel-research] ​


Run parallel research

For independent investigations, spawn multiple subagents to work simultaneously:











Research the authentication, database, and API modules in parallel using separate subagents






Each subagent explores its area independently, then Claude synthesizes the findings. This works best when the research paths don’t depend on each other.




When subagents complete, their results return to your main conversation. Running many subagents that each return detailed results can consume significant context.


For tasks that need sustained parallelism or exceed your context window,  [/docs/en/agent-teams] agent teams give each worker its own independent context.


 [#chain-subagents] ​


Chain subagents

For multi-step workflows, ask Claude to use subagents in sequence. Each subagent completes its task and returns results to Claude, which then passes relevant context to the next subagent.











Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them








 [#choose-between-subagents-and-main-conversation] ​


Choose between subagents and main conversation

Use the main conversation when:


The task needs frequent back-and-forth or iterative refinement

Multiple phases share significant context (planning → implementation → testing)

You’re making a quick, targeted change

Latency matters. Subagents start fresh and may need time to gather context

Use subagents when:


The task produces verbose output you don’t need in your main context

You want to enforce specific tool restrictions or permissions

The work is self-contained and can return a summary

Consider  [/docs/en/skills] Skills instead when you want reusable prompts or workflows that run in the main conversation context rather than isolated subagent context.
For a quick question about something already in your conversation, use  [/docs/en/interactive-mode#side-questions-with-btw] /btw instead of a subagent. It sees your full context but has no tool access, and the answer is discarded rather than added to history.




Subagents cannot spawn other subagents. If your workflow requires nested delegation, use  [/docs/en/skills] Skills or  [#chain-subagents] chain subagents from the main conversation.




 [#manage-subagent-context] ​


Manage subagent context



 [#resume-subagents] ​


Resume subagents

Each subagent invocation creates a new instance with fresh context. To continue an existing subagent’s work instead of starting over, ask Claude to resume it.
Resumed subagents retain their full conversation history, including all previous tool calls, results, and reasoning. The subagent picks up exactly where it stopped rather than starting fresh.
When a subagent completes, Claude receives its agent ID. Claude uses the SendMessage tool with the agent’s ID as the to field to resume it. To resume a subagent, ask Claude to continue the previous work:











Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]






If a stopped subagent receives a SendMessage, it auto-resumes in the background without requiring a new Agent invocation.
You can also ask Claude for the agent ID if you want to reference it explicitly, or find IDs in the transcript files at ~/.claude/projects/{project}/{sessionId}/subagents/. Each transcript is stored as agent-{agentId}.jsonl.
Subagent transcripts persist independently of the main conversation:


Main conversation compaction: When the main conversation compacts, subagent transcripts are unaffected. They’re stored in separate files.

Session persistence: Subagent transcripts persist within their session. You can  [#resume-subagents] resume a subagent after restarting Claude Code by resuming the same session.

Automatic cleanup: Transcripts are cleaned up based on the cleanupPeriodDays setting (default: 30 days).



 [#auto-compaction] ​


Auto-compaction

Subagents support automatic compaction using the same logic as the main conversation. By default, auto-compaction triggers at approximately 95% capacity. To trigger compaction earlier, set CLAUDE_AUTOCOMPACT_PCT_OVERRIDE to a lower percentage (for example, 50). See  [/docs/en/env-vars] environment variables for details.
Compaction events are logged in subagent transcript files:











{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}






The preTokens value shows how many tokens were used before compaction occurred.


 [#example-subagents] ​


Example subagents

These examples demonstrate effective patterns for building subagents. Use them as starting points, or generate a customized version with Claude.




Best practices:

Design focused subagents: each subagent should excel at one specific task

Write detailed descriptions: Claude uses the description to decide when to delegate

Limit tool access: grant only necessary permissions for security and focus

Check into version control: share project subagents with your team





 [#code-reviewer] ​


Code reviewer

A read-only subagent that reviews code without modifying it. This example shows how to design a focused subagent with limited tool access (no Edit or Write) and a detailed prompt that specifies exactly what to look for and how to format output.











---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.








 [#debugger] ​


Debugger

A subagent that can both analyze and fix issues. Unlike the code reviewer, this one includes Edit because fixing bugs requires modifying code. The prompt provides a clear workflow from diagnosis to verification.











---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.








 [#data-scientist] ​


Data scientist

A domain-specific subagent for data analysis work. This example shows how to create subagents for specialized workflows outside of typical coding tasks. It explicitly sets model: sonnet for more capable analysis.











---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.








 [#database-query-validator] ​


Database query validator

A subagent that allows Bash access but validates commands to permit only read-only SQL queries. This example shows how to use PreToolUse hooks for conditional validation when you need finer control than the tools field provides.











---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.






Claude Code  [/docs/en/hooks#pretooluse-input] passes hook input as JSON via stdin to hook commands. The validation script reads this JSON, extracts the command being executed, and checks it against a list of SQL write operations. If a write operation is detected, the script  [/docs/en/hooks#exit-code-2-behavior-per-event] exits with code 2 to block execution and returns an error message to Claude via stderr.
Create the validation script anywhere in your project. The path must match the command field in your hook configuration:











#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0






Make the script executable:











chmod +x ./scripts/validate-readonly-query.sh






The hook receives JSON via stdin with the Bash command in tool_input.command. Exit code 2 blocks the operation and feeds the error message back to Claude. See  [/docs/en/hooks#exit-code-output] Hooks for details on exit codes and  [/docs/en/hooks#pretooluse-input] Hook input for the complete input schema.


 [#next-steps] ​


Next steps

Now that you understand subagents, explore these related features:


 [/docs/en/plugins] Distribute subagents with plugins to share subagents across teams or projects

 [/docs/en/headless] Run Claude Code programmatically with the Agent SDK for CI/CD and automation

 [/docs/en/mcp] Use MCP servers to give subagents access to external tools and data




Was this page helpful?


YesNo






 [/docs/en/agent-teams] Run agent teams





⌘I











 [/docs/en/overview] 
 [https://x.com/AnthropicAI]  [https://www.linkedin.com/company/anthropicresearch] 






 [https://www.anthropic.com/company]  [https://www.anthropic.com/careers]  [https://www.anthropic.com/economic-futures]  [https://www.anthropic.com/research]  [https://www.anthropic.com/news]  [https://trust.anthropic.com/]  [https://www.anthropic.com/transparency] 





 [https://www.anthropic.com/supported-countries]  [https://status.anthropic.com/]  [https://support.claude.com/] 





 [https://www.anthropic.com/learn]  [https://claude.com/partners/mcp]  [https://www.claude.com/customers]  [https://www.anthropic.com/engineering]  [https://www.anthropic.com/events]  [https://claude.com/partners/powered-by-claude]  [https://claude.com/partners/services]  [https://claude.com/programs/startups] 





 [#]  [https://www.anthropic.com/legal/privacy]  [https://www.anthropic.com/responsible-disclosure-policy]  [https://www.anthropic.com/legal/aup]  [https://www.anthropic.com/legal/commercial-terms]  [https://www.anthropic.com/legal/consumer-terms] 












Assistant









Responses are generated using AI and may contain mistakes.
```

### mcp

URL: https://code.claude.com/docs/en/mcp
Hash: 7755566d4d7f

```
Connect Claude Code to tools via MCP - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Tools and plugins

Connect Claude Code to tools via MCP




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Agents


 [/docs/en/sub-agents] 

Create custom subagents


 [/docs/en/agent-teams] 

Run agent teams





Tools and plugins


 [/docs/en/mcp] 

Model Context Protocol (MCP)


 [/docs/en/discover-plugins] 

Discover and install prebuilt plugins


 [/docs/en/plugins] 

Create plugins


 [/docs/en/skills] 

Extend Claude with skills





Automation


 [/docs/en/hooks-guide] 

Automate with hooks


 [/docs/en/channels] 

Push external events to Claude


 [/docs/en/scheduled-tasks] 

Run prompts on a schedule


 [/docs/en/headless] 

Programmatic usage





Troubleshooting


 [/docs/en/troubleshooting] 

Troubleshooting











On this page

 [#what-you-can-do-with-mcp] What you can do with MCP
 [#popular-mcp-servers] Popular MCP servers
 [#installing-mcp-servers] Installing MCP servers
 [#option-1-add-a-remote-http-server] Option 1: Add a remote HTTP server
 [#option-2-add-a-remote-sse-server] Option 2: Add a remote SSE server
 [#option-3-add-a-local-stdio-server] Option 3: Add a local stdio server
 [#managing-your-servers] Managing your servers
 [#dynamic-tool-updates] Dynamic tool updates
 [#push-messages-with-channels] Push messages with channels
 [#plugin-provided-mcp-servers] Plugin-provided MCP servers
 [#mcp-installation-scopes] MCP installation scopes
 [#local-scope] Local scope
 [#project-scope] Project scope
 [#user-scope] User scope
 [#choosing-the-right-scope] Choosing the right scope
 [#scope-hierarchy-and-precedence] Scope hierarchy and precedence
 [#environment-variable-expansion-in-mcp-json] Environment variable expansion in .mcp.json
 [#practical-examples] Practical examples
 [#example-monitor-errors-with-sentry] Example: Monitor errors with Sentry
 [#example-connect-to-github-for-code-reviews] Example: Connect to GitHub for code reviews
 [#example-query-your-postgresql-database] Example: Query your PostgreSQL database
 [#authenticate-with-remote-mcp-servers] Authenticate with remote MCP servers
 [#use-a-fixed-oauth-callback-port] Use a fixed OAuth callback port
 [#use-pre-configured-oauth-credentials] Use pre-configured OAuth credentials
 [#override-oauth-metadata-discovery] Override OAuth metadata discovery
 [#use-dynamic-headers-for-custom-authentication] Use dynamic headers for custom authentication
 [#add-mcp-servers-from-json-configuration] Add MCP servers from JSON configuration
 [#import-mcp-servers-from-claude-desktop] Import MCP servers from Claude Desktop
 [#use-mcp-servers-from-claude-ai] Use MCP servers from Claude.ai
 [#use-claude-code-as-an-mcp-server] Use Claude Code as an MCP server
 [#mcp-output-limits-and-warnings] MCP output limits and warnings
 [#respond-to-mcp-elicitation-requests] Respond to MCP elicitation requests
 [#use-mcp-resources] Use MCP resources
 [#reference-mcp-resources] Reference MCP resources
 [#scale-with-mcp-tool-search] Scale with MCP Tool Search
 [#how-it-works] How it works
 [#for-mcp-server-authors] For MCP server authors
 [#configure-tool-search] Configure tool search
 [#use-mcp-prompts-as-commands] Use MCP prompts as commands
 [#execute-mcp-prompts] Execute MCP prompts
 [#managed-mcp-configuration] Managed MCP configuration
 [#option-1-exclusive-control-with-managed-mcp-json] Option 1: Exclusive control with managed-mcp.json
 [#option-2-policy-based-control-with-allowlists-and-denylists] Option 2: Policy-based control with allowlists and denylists
 [#restriction-options] Restriction options
 [#example-configuration] Example configuration
 [#how-command-based-restrictions-work] How command-based restrictions work
 [#how-url-based-restrictions-work] How URL-based restrictions work
 [#allowlist-behavior-allowedmcpservers] Allowlist behavior (allowedMcpServers)
 [#denylist-behavior-deniedmcpservers] Denylist behavior (deniedMcpServers)
 [#important-notes] Important notes

























Claude Code can connect to hundreds of external tools and data sources through the  [https://modelcontextprotocol.io/introduction] Model Context Protocol (MCP), an open source standard for AI-tool integrations. MCP servers give Claude Code access to your tools, databases, and APIs.


 [#what-you-can-do-with-mcp] ​


What you can do with MCP

With MCP servers connected, you can ask Claude Code to:


Implement features from issue trackers: “Add the feature described in JIRA issue ENG-4521 and create a PR on GitHub.”

Analyze monitoring data: “Check Sentry and Statsig to check the usage of the feature described in ENG-4521.”

Query databases: “Find emails of 10 random users who used feature ENG-4521, based on our PostgreSQL database.”

Integrate designs: “Update our standard email template based on the new Figma designs that were posted in Slack”

Automate workflows: “Create Gmail drafts inviting these 10 users to a feedback session about the new feature.”

React to external events: An MCP server can also act as a  [/docs/en/channels] channel that pushes messages into your session, so Claude reacts to Telegram messages, Discord chats, or webhook events while you’re away.



 [#popular-mcp-servers] ​


Popular MCP servers

Here are some commonly used MCP servers you can connect to Claude Code:




Use third party MCP servers at your own risk - Anthropic has not verified
the correctness or security of all these servers.
Make sure you trust MCP servers you are installing.
Be especially careful when using MCP servers that could fetch untrusted
content, as these can expose you to prompt injection risk.







Need a specific integration?  [https://github.com/modelcontextprotocol/servers] Find hundreds more MCP servers on GitHub, or build your own using the  [https://modelcontextprotocol.io/quickstart/server] MCP SDK.




 [#installing-mcp-servers] ​


Installing MCP servers

MCP servers can be configured in three different ways depending on your needs:


 [#option-1-add-a-remote-http-server] ​


Option 1: Add a remote HTTP server

HTTP servers are the recommended option for connecting to remote MCP servers. This is the most widely supported transport for cloud-based services.











# Basic syntax
claude mcp add --transport http <name> <url>

# Real example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Example with Bearer token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"








 [#option-2-add-a-remote-sse-server] ​


Option 2: Add a remote SSE server





The SSE (Server-Sent Events) transport is deprecated. Use HTTP servers instead, where available.













# Basic syntax
claude mcp add --transport sse <name> <url>

# Real example: Connect to Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Example with authentication header
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"








 [#option-3-add-a-local-stdio-server] ​


Option 3: Add a local stdio server

Stdio servers run as local processes on your machine. They’re ideal for tools that need direct system access or custom scripts.











# Basic syntax
claude mcp add [options] <name> -- <command> [args...]

# Real example: Add Airtable server
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server










Important: Option orderingAll options (--transport, --env, --scope, --header) must come before the server name. The -- (double dash) then separates the server name from the command and arguments that get passed to the MCP server.For example:

claude mcp add --transport stdio myserver -- npx server → runs npx server

claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080 → runs python server.py --port 8080 with KEY=value in environment
This prevents conflicts between Claude’s flags and the server’s flags.




 [#managing-your-servers] ​


Managing your servers

Once configured, you can manage your MCP servers with these commands:











# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# (within Claude Code) Check server status
/mcp








 [#dynamic-tool-updates] ​


Dynamic tool updates

Claude Code supports MCP list_changed notifications, allowing MCP servers to dynamically update their available tools, prompts, and resources without requiring you to disconnect and reconnect. When an MCP server sends a list_changed notification, Claude Code automatically refreshes the available capabilities from that server.


 [#push-messages-with-channels] ​


Push messages with channels

An MCP server can also push messages directly into your session so Claude can react to external events like CI results, monitoring alerts, or chat messages. To enable this, your server declares the claude/channel capability and you opt it in with the --channels flag at startup. See  [/docs/en/channels] Channels to use an officially supported channel, or  [/docs/en/channels-reference] Channels reference to build your own.




Tips:

Use the --scope flag to specify where the configuration is stored:


local (default): Available only to you in the current project (was called project in older versions)

project: Shared with everyone in the project via .mcp.json file

user: Available to you across all projects (was called global in older versions)



Set environment variables with --env flags (for example, --env KEY=value)

Configure MCP server startup timeout using the MCP_TIMEOUT environment variable (for example, MCP_TIMEOUT=10000 claude sets a 10-second timeout)

Claude Code will display a warning when MCP tool output exceeds 10,000 tokens. To increase this limit, set the MAX_MCP_OUTPUT_TOKENS environment variable (for example, MAX_MCP_OUTPUT_TOKENS=50000)

Use /mcp to authenticate with remote servers that require OAuth 2.0 authentication







Windows Users: On native Windows (not WSL), local MCP servers that use npx require the cmd /c wrapper to ensure proper execution.










# This creates command="cmd" which Windows can execute
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package





Without the cmd /c wrapper, you’ll encounter “Connection closed” errors because Windows cannot directly execute npx. (See the note above for an explanation of the -- parameter.)




 [#plugin-provided-mcp-servers] ​


Plugin-provided MCP servers

 [/docs/en/plugins] Plugins can bundle MCP servers, automatically providing tools and integrations when the plugin is enabled. Plugin MCP servers work identically to user-configured servers.
How plugin MCP servers work:


Plugins define MCP servers in .mcp.json at the plugin root or inline in plugin.json

When a plugin is enabled, its MCP servers start automatically

Plugin MCP tools appear alongside manually configured MCP tools

Plugin servers are managed through plugin installation (not /mcp commands)

Example plugin MCP configuration:
In .mcp.json at plugin root:











{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_URL": "${DB_URL}"
      }
    }
  }
}






Or inline in plugin.json:











{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}






Plugin MCP features:


Automatic lifecycle: At session startup, servers for enabled plugins connect automatically. If you enable or disable a plugin during a session, run /reload-plugins to connect or disconnect its MCP servers

Environment variables: use ${CLAUDE_PLUGIN_ROOT} for bundled plugin files and ${CLAUDE_PLUGIN_DATA} for  [/docs/en/plugins-reference#persistent-data-directory] persistent state that survives plugin updates

User environment access: Access to same environment variables as manually configured servers

Multiple transport types: Support stdio, SSE, and HTTP transports (transport support may vary by server)

Viewing plugin MCP servers:











# Within Claude Code, see all MCP servers including plugin ones
/mcp






Plugin servers appear in the list with indicators showing they come from plugins.
Benefits of plugin MCP servers:


Bundled distribution: Tools and servers packaged together

Automatic setup: No manual MCP configuration needed

Team consistency: Everyone gets the same tools when plugin is installed

See the  [/docs/en/plugins-reference#mcp-servers] plugin components reference for details on bundling MCP servers with plugins.


 [#mcp-installation-scopes] ​


MCP installation scopes

MCP servers can be configured at three different scope levels, each serving distinct purposes for managing server accessibility and sharing. Understanding these scopes helps you determine the best way to configure servers for your specific needs.


 [#local-scope] ​


Local scope

Local-scoped servers represent the default configuration level and are stored in ~/.claude.json under your project’s path. These servers remain private to you and are only accessible when working within the current project directory. This scope is ideal for personal development servers, experimental configurations, or servers containing sensitive credentials that shouldn’t be shared.




The term “local scope” for MCP servers differs from general local settings. MCP local-scoped servers are stored in ~/.claude.json (your home directory), while general local settings use .claude/settings.local.json (in the project directory). See  [/docs/en/settings#settings-files] Settings for details on settings file locations.













# Add a local-scoped server (default)
claude mcp add --transport http stripe https://mcp.stripe.com

# Explicitly specify local scope
claude mcp add --transport http stripe --scope local https://mcp.stripe.com








 [#project-scope] ​


Project scope

Project-scoped servers enable team collaboration by storing configurations in a .mcp.json file at your project’s root directory. This file is designed to be checked into version control, ensuring all team members have access to the same MCP tools and services. When you add a project-scoped server, Claude Code automatically creates or updates this file with the appropriate configuration structure.











# Add a project-scoped server
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp






The resulting .mcp.json file follows a standardized format:











{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}






For security reasons, Claude Code prompts for approval before using project-scoped servers from .mcp.json files. If you need to reset these approval choices, use the claude mcp reset-project-choices command.


 [#user-scope] ​


User scope

User-scoped servers are stored in ~/.claude.json and provide cross-project accessibility, making them available across all projects on your machine while remaining private to your user account. This scope works well for personal utility servers, development tools, or services you frequently use across different projects.











# Add a user server
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic








 [#choosing-the-right-scope] ​


Choosing the right scope

Select your scope based on:


Local scope: Personal servers, experimental configurations, or sensitive credentials specific to one project

Project scope: Team-shared servers, project-specific tools, or services required for collaboration

User scope: Personal utilities needed across multiple projects, development tools, or frequently used services





Where are MCP servers stored?

User and local scope: ~/.claude.json (in the mcpServers field or under project paths)

Project scope: .mcp.json in your project root (checked into source control)

Managed: managed-mcp.json in system directories (see  [#managed-mcp-configuration] Managed MCP configuration)





 [#scope-hierarchy-and-precedence] ​


Scope hierarchy and precedence

MCP server configurations follow a clear precedence hierarchy. When servers with the same name exist at multiple scopes, the system resolves conflicts by prioritizing local-scoped servers first, followed by project-scoped servers, and finally user-scoped servers. This design ensures that personal configurations can override shared ones when needed.
If a server is configured both locally and through a  [#use-mcp-servers-from-claude-ai] claude.ai connector, the local configuration takes precedence and the connector entry is skipped.


 [#environment-variable-expansion-in-mcp-json] ​


Environment variable expansion in .mcp.json

Claude Code supports environment variable expansion in .mcp.json files, allowing teams to share configurations while maintaining flexibility for machine-specific paths and sensitive values like API keys.
Supported syntax:


${VAR} - Expands to the value of environment variable VAR

${VAR:-default} - Expands to VAR if set, otherwise uses default

Expansion locations:
Environment variables can be expanded in:


command - The server executable path

args - Command-line arguments

env - Environment variables passed to the server

url - For HTTP server types

headers - For HTTP server authentication

Example with variable expansion:











{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}






If a required environment variable is not set and has no default value, Claude Code will fail to parse the config.


 [#practical-examples] ​


Practical examples



 [#example-monitor-errors-with-sentry] ​


Example: Monitor errors with Sentry












claude mcp add --transport http sentry https://mcp.sentry.dev/mcp






Authenticate with your Sentry account:











/mcp






Then debug production issues:











What are the most common errors in the last 24 hours?

















Show me the stack trace for error ID abc123

















Which deployment introduced these new errors?








 [#example-connect-to-github-for-code-reviews] ​


Example: Connect to GitHub for code reviews












claude mcp add --transport http github https://api.githubcopilot.com/mcp/






Authenticate if needed by selecting “Authenticate” for GitHub:











/mcp






Then work with GitHub:











Review PR #456 and suggest improvements

















Create a new issue for the bug we just found

















Show me all open PRs assigned to me








 [#example-query-your-postgresql-database] ​


Example: Query your PostgreSQL database












claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly: [/cdn-cgi/l/email-protection] [email protected]:5432/analytics"






Then query your database naturally:











What's our total revenue this month?

















Show me the schema for the orders table

















Find customers who haven't made a purchase in 90 days








 [#authenticate-with-remote-mcp-servers] ​


Authenticate with remote MCP servers

Many cloud-based MCP servers require authentication. Claude Code supports OAuth 2.0 for secure connections.







1

 [#] 






Add the server that requires authentication

For example:










claude mcp add --transport http sentry https://mcp.sentry.dev/mcp














2

 [#] 






Use the /mcp command within Claude Code

In Claude code, use the command:










/mcp





Then follow the steps in your browser to login.








Tips:

Authentication tokens are stored securely and refreshed automatically

Use “Clear authentication” in the /mcp menu to revoke access

If your browser doesn’t open automatically, copy the provided URL and open it manually

If the browser redirect fails with a connection error after authenticating, paste the full callback URL from your browser’s address bar into the URL prompt that appears in Claude Code

OAuth authentication works with HTTP servers





 [#use-a-fixed-oauth-callback-port] ​


Use a fixed OAuth callback port

Some MCP servers require a specific redirect URI registered in advance. By default, Claude Code picks a random available port for the OAuth callback. Use --callback-port to fix the port so it matches a pre-registered redirect URI of the form http://localhost:PORT/callback.
You can use --callback-port on its own (with dynamic client registration) or together with --client-id (with pre-configured credentials).











# Fixed callback port with dynamic client registration
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp








 [#use-pre-configured-oauth-credentials] ​


Use pre-configured OAuth credentials

Some MCP servers don’t support automatic OAuth setup via Dynamic Client Registration. If you see an error like “Incompatible auth server: does not support dynamic client registration,” the server requires pre-configured credentials. Claude Code also supports servers that use a Client ID Metadata Document (CIMD) instead of Dynamic Client Registration, and discovers these automatically. If automatic discovery fails, register an OAuth app through the server’s developer portal first, then provide the credentials when adding the server.







1

 [#] 






Register an OAuth app with the server

Create an app through the server’s developer portal and note your client ID and client secret.Many servers also require a redirect URI. If so, choose a port and register a redirect URI in the format http://localhost:PORT/callback. Use that same port with --callback-port in the next step.








2

 [#] 






Add the server with your credentials

Choose one of the following methods. The port used for --callback-port can be any available port. It just needs to match the redirect URI you registered in the previous step.


 claude mcp add


 claude mcp add-json


 claude mcp add-json (callback port only)


 CI / env var


Use --client-id to pass your app’s client ID. The --client-secret flag prompts for the secret with masked input:










claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp







Include the oauth object in the JSON config and pass --client-secret as a separate flag:










claude mcp add-json my-server \
  '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
  --client-secret







Use --callback-port without a client ID to fix the port while using dynamic client registration:










claude mcp add-json my-server \
  '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'







Set the secret via environment variable to skip the interactive prompt:










MCP_CLIENT_SECRET=your-secret claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp

















3

 [#] 






Authenticate in Claude Code

Run /mcp in Claude Code and follow the browser login flow.








Tips:

The client secret is stored securely in your system keychain (macOS) or a credentials file, not in your config

If the server uses a public OAuth client with no secret, use only --client-id without --client-secret

--callback-port can be used with or without --client-id

These flags only apply to HTTP and SSE transports. They have no effect on stdio servers

Use claude mcp get <name> to verify that OAuth credentials are configured for a server





 [#override-oauth-metadata-discovery] ​


Override OAuth metadata discovery

If your MCP server’s standard OAuth metadata endpoints return errors but the server exposes a working OIDC endpoint, you can point Claude Code at a specific metadata URL to bypass the default discovery chain. By default, Claude Code first checks RFC 9728 Protected Resource Metadata at /.well-known/oauth-protected-resource, then falls back to RFC 8414 authorization server metadata at /.well-known/oauth-authorization-server.
Set authServerMetadataUrl in the oauth object of your server’s config in .mcp.json:











{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}






The URL must use https://. This option requires Claude Code v2.1.64 or later.


 [#use-dynamic-headers-for-custom-authentication] ​


Use dynamic headers for custom authentication

If your MCP server uses an authentication scheme other than OAuth (such as Kerberos, short-lived tokens, or an internal SSO), use headersHelper to generate request headers at connection time. Claude Code runs the command and merges its output into the connection headers.











{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}






The command can also be inline:











{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "echo '{\"Authorization\": \"Bearer '\"$(get-token)\"'\"}'"
    }
  }
}






Requirements:


The command must write a JSON object of string key-value pairs to stdout

The command runs in a shell with a 10-second timeout

Dynamic headers override any static headers with the same name

The helper runs fresh on each connection (at session start and on reconnect). There is no caching, so your script is responsible for any token reuse.
Claude Code sets these environment variables when executing the helper:



VariableValue
CLAUDE_CODE_MCP_SERVER_NAMEthe name of the MCP server
CLAUDE_CODE_MCP_SERVER_URLthe URL of the MCP server



Use these to write a single helper script that serves multiple MCP servers.




headersHelper executes arbitrary shell commands. When defined at project or local scope, it only runs after you accept the workspace trust dialog.




 [#add-mcp-servers-from-json-configuration] ​


Add MCP servers from JSON configuration

If you have a JSON configuration for an MCP server, you can add it directly:







1

 [#] 






Add an MCP server from JSON












# Basic syntax
claude mcp add-json <name> '<json>'

# Example: Adding an HTTP server with JSON configuration
claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

# Example: Adding a stdio server with JSON configuration
claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'

# Example: Adding an HTTP server with pre-configured OAuth credentials
claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret














2

 [#] 






Verify the server was added












claude mcp get weather-api














Tips:

Make sure the JSON is properly escaped in your shell

The JSON must conform to the MCP server configuration schema

You can use --scope user to add the server to your user configuration instead of the project-specific one





 [#import-mcp-servers-from-claude-desktop] ​


Import MCP servers from Claude Desktop

If you’ve already configured MCP servers in Claude Desktop, you can import them:







1

 [#] 






Import servers from Claude Desktop












# Basic syntax 
claude mcp add-from-claude-desktop 














2

 [#] 






Select which servers to import

After running the command, you’ll see an interactive dialog that allows you to select which servers you want to import.








3

 [#] 






Verify the servers were imported












claude mcp list 














Tips:

This feature only works on macOS and Windows Subsystem for Linux (WSL)

It reads the Claude Desktop configuration file from its standard location on those platforms

Use the --scope user flag to add servers to your user configuration

Imported servers will have the same names as in Claude Desktop

If servers with the same names already exist, they will get a numerical suffix (for example, server_1)





 [#use-mcp-servers-from-claude-ai] ​


Use MCP servers from Claude.ai

If you’ve logged into Claude Code with a  [https://claude.ai] Claude.ai account, MCP servers you’ve added in Claude.ai are automatically available in Claude Code:







1

 [#] 






Configure MCP servers in Claude.ai

Add servers at  [https://claude.ai/settings/connectors] claude.ai/settings/connectors. On Team and Enterprise plans, only admins can add servers.








2

 [#] 






Authenticate the MCP server

Complete any required authentication steps in Claude.ai.








3

 [#] 






View and manage servers in Claude Code

In Claude Code, use the command:










/mcp





Claude.ai servers appear in the list with indicators showing they come from Claude.ai.




To disable claude.ai MCP servers in Claude Code, set the ENABLE_CLAUDEAI_MCP_SERVERS environment variable to false:











ENABLE_CLAUDEAI_MCP_SERVERS=false claude








 [#use-claude-code-as-an-mcp-server] ​


Use Claude Code as an MCP server

You can use Claude Code itself as an MCP server that other applications can connect to:











# Start Claude as a stdio MCP server
claude mcp serve






You can use this in Claude Desktop by adding this configuration to claude_desktop_config.json:











{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}










Configuring the executable path: The command field must reference the Claude Code executable. If the claude command is not in your system’s PATH, you’ll need to specify the full path to the executable.To find the full path:










which claude





Then use the full path in your configuration:










{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "/full/path/to/claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}





Without the correct executable path, you’ll encounter errors like spawn claude ENOENT.






Tips:

The server provides access to Claude’s tools like View, Edit, LS, etc.

In Claude Desktop, try asking Claude to read files in a directory, make edits, and more.

Note that this MCP server is only exposing Claude Code’s tools to your MCP client, so your own client is responsible for implementing user confirmation for individual tool calls.





 [#mcp-output-limits-and-warnings] ​


MCP output limits and warnings

When MCP tools produce large outputs, Claude Code helps manage the token usage to prevent overwhelming your conversation context:


Output warning threshold: Claude Code displays a warning when any MCP tool output exceeds 10,000 tokens

Configurable limit: You can adjust the maximum allowed MCP output tokens using the MAX_MCP_OUTPUT_TOKENS environment variable

Default limit: The default maximum is 25,000 tokens

To increase the limit for tools that produce large outputs:











# Set a higher limit for MCP tool outputs
export MAX_MCP_OUTPUT_TOKENS=50000
claude






This is particularly useful when working with MCP servers that:


Query large datasets or databases

Generate detailed reports or documentation

Process extensive log files or debugging information





If you frequently encounter output warnings with specific MCP servers, consider increasing the limit or configuring the server to paginate or filter its responses.




 [#respond-to-mcp-elicitation-requests] ​


Respond to MCP elicitation requests

MCP servers can request structured input from you mid-task using elicitation. When a server needs information it can’t get on its own, Claude Code displays an interactive dialog and passes your response back to the server. No configuration is required on your side: elicitation dialogs appear automatically when a server requests them.
Servers can request input in two ways:


Form mode: Claude Code shows a dialog with form fields defined by the server (for example, a username and password prompt). Fill in the fields and submit.

URL mode: Claude Code opens a browser URL for authentication or approval. Complete the flow in the browser, then confirm in the CLI.

To auto-respond to elicitation requests without showing a dialog, use the  [/docs/en/hooks#elicitation] Elicitation hook.
If you’re building an MCP server that uses elicitation, see the  [https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation] MCP elicitation specification for protocol details and schema examples.


 [#use-mcp-resources] ​


Use MCP resources

MCP servers can expose resources that you can reference using @ mentions, similar to how you reference files.


 [#reference-mcp-resources] ​


Reference MCP resources








1

 [#] 






List available resources

Type @ in your prompt to see available resources from all connected MCP servers. Resources appear alongside files in the autocomplete menu.








2

 [#] 






Reference a specific resource

Use the format @server:protocol://resource/path to reference a resource:










Can you analyze @github:issue://123 and suggest a fix?
















Please review the API documentation at @docs:file://api/authentication














3

 [#] 






Multiple resource references

You can reference multiple resources in a single prompt:










Compare @postgres:schema://users with @docs:file://database/user-model














Tips:

Resources are automatically fetched and included as attachments when referenced

Resource paths are fuzzy-searchable in the @ mention autocomplete

Claude Code automatically provides tools to list and read MCP resources when servers support them

Resources can contain any type of content that the MCP server provides (text, JSON, structured data, etc.)





 [#scale-with-mcp-tool-search] ​


Scale with MCP Tool Search

Tool search keeps MCP context usage low by deferring tool definitions until Claude needs them. Only tool names load at session start, so adding more MCP servers has minimal impact on your context window.


 [#how-it-works] ​


How it works

Tool search is enabled by default. MCP tools are deferred rather than loaded into context upfront, and Claude uses a search tool to discover relevant ones when a task needs them. Only the tools Claude actually uses enter context. From your perspective, MCP tools work exactly as before.
If you prefer threshold-based loading, set ENABLE_TOOL_SEARCH=auto to load schemas upfront when they fit within 10% of the context window and defer only the overflow. See  [#configure-tool-search] Configure tool search for all options.


 [#for-mcp-server-authors] ​


For MCP server authors

If you’re building an MCP server, the server instructions field becomes more useful with Tool Search enabled. Server instructions help Claude understand when to search for your tools, similar to how  [/docs/en/skills] skills work.
Add clear, descriptive server instructions that explain:


What category of tasks your tools handle

When Claude should search for your tools

Key capabilities your server provides

Claude Code truncates tool descriptions and server instructions at 2KB each. Keep them concise to avoid truncation, and put critical details near the start.


 [#configure-tool-search] ​


Configure tool search

Tool search is enabled by default: MCP tools are deferred and discovered on demand. When ANTHROPIC_BASE_URL points to a non-first-party host, tool search is disabled by default because most proxies do not forward tool_reference blocks. Set ENABLE_TOOL_SEARCH explicitly if your proxy does. This feature requires models that support tool_reference blocks: Sonnet 4 and later, or Opus 4 and later. Haiku models do not support tool search.
Control tool search behavior with the ENABLE_TOOL_SEARCH environment variable:



ValueBehavior
(unset)All MCP tools deferred and loaded on demand. Falls back to loading upfront when ANTHROPIC_BASE_URL is a non-first-party host
trueAll MCP tools deferred, including for non-first-party ANTHROPIC_BASE_URL
autoThreshold mode: tools load upfront if they fit within 10% of the context window, deferred otherwise
auto:<N>Threshold mode with a custom percentage, where <N> is 0-100 (e.g., auto:5 for 5%)
falseAll MCP tools loaded upfront, no deferral














# Use a custom 5% threshold
ENABLE_TOOL_SEARCH=auto:5 claude

# Disable tool search entirely
ENABLE_TOOL_SEARCH=false claude






Or set the value in your  [/docs/en/settings#available-settings] settings.json env field.
You can also disable the MCPSearch tool specifically using the disallowedTools setting:











{
  "permissions": {
    "deny": ["MCPSearch"]
  }
}








 [#use-mcp-prompts-as-commands] ​


Use MCP prompts as commands

MCP servers can expose prompts that become available as commands in Claude Code.


 [#execute-mcp-prompts] ​


Execute MCP prompts








1

 [#] 






Discover available prompts

Type / to see all available commands, including those from MCP servers. MCP prompts appear with the format /mcp__servername__promptname.








2

 [#] 






Execute a prompt without arguments












/mcp__github__list_prs














3

 [#] 






Execute a prompt with arguments

Many prompts accept arguments. Pass them space-separated after the command:










/mcp__github__pr_review 456
















/mcp__jira__create_issue "Bug in login flow" high














Tips:

MCP prompts are dynamically discovered from connected servers

Arguments are parsed based on the prompt’s defined parameters

Prompt results are injected directly into the conversation

Server and prompt names are normalized (spaces become underscores)





 [#managed-mcp-configuration] ​


Managed MCP configuration

For organizations that need centralized control over MCP servers, Claude Code supports two configuration options:


Exclusive control with managed-mcp.json: Deploy a fixed set of MCP servers that users cannot modify or extend

Policy-based control with allowlists/denylists: Allow users to add their own servers, but restrict which ones are permitted

These options allow IT administrators to:


Control which MCP servers employees can access: Deploy a standardized set of approved MCP servers across the organization

Prevent unauthorized MCP servers: Restrict users from adding unapproved MCP servers

Disable MCP entirely: Remove MCP functionality completely if needed



 [#option-1-exclusive-control-with-managed-mcp-json] ​


Option 1: Exclusive control with managed-mcp.json

When you deploy a managed-mcp.json file, it takes exclusive control over all MCP servers. Users cannot add, modify, or use any MCP servers other than those defined in this file. This is the simplest approach for organizations that want complete control.
System administrators deploy the configuration file to a system-wide directory:


macOS: /Library/Application Support/ClaudeCode/managed-mcp.json

Linux and WSL: /etc/claude-code/managed-mcp.json

Windows: C:\Program Files\ClaudeCode\managed-mcp.json





These are system-wide paths (not user home directories like ~/Library/...) that require administrator privileges. They are designed to be deployed by IT administrators.


The managed-mcp.json file uses the same format as a standard .mcp.json file:











{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}








 [#option-2-policy-based-control-with-allowlists-and-denylists] ​


Option 2: Policy-based control with allowlists and denylists

Instead of taking exclusive control, administrators can allow users to configure their own MCP servers while enforcing restrictions on which servers are permitted. This approach uses allowedMcpServers and deniedMcpServers in the  [/docs/en/settings#settings-files] managed settings file.




Choosing between options: Use Option 1 (managed-mcp.json) when you want to deploy a fixed set of servers with no user customization. Use Option 2 (allowlists/denylists) when you want to allow users to add their own servers within policy constraints.




 [#restriction-options] ​


Restriction options

Each entry in the allowlist or denylist can restrict servers in three ways:


By server name (serverName): Matches the configured name of the server

By command (serverCommand): Matches the exact command and arguments used to start stdio servers

By URL pattern (serverUrl): Matches remote server URLs with wildcard support

Important: Each entry must have exactly one of serverName, serverCommand, or serverUrl.


 [#example-configuration] ​


Example configuration












{
  "allowedMcpServers": [
    // Allow by server name
    { "serverName": "github" },
    { "serverName": "sentry" },

    // Allow by exact command (for stdio servers)
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverCommand": ["python", "/usr/local/bin/approved-server.py"] },

    // Allow by URL pattern (for remote servers)
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ],
  "deniedMcpServers": [
    // Block by server name
    { "serverName": "dangerous-server" },

    // Block by exact command (for stdio servers)
    { "serverCommand": ["npx", "-y", "unapproved-package"] },

    // Block by URL pattern (for remote servers)
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}








 [#how-command-based-restrictions-work] ​


How command-based restrictions work

Exact matching:


Command arrays must match exactly - both the command and all arguments in the correct order

Example: ["npx", "-y", "server"] will NOT match ["npx", "server"] or ["npx", "-y", "server", "--flag"]

Stdio server behavior:


When the allowlist contains any serverCommand entries, stdio servers must match one of those commands

Stdio servers cannot pass by name alone when command restrictions are present

This ensures administrators can enforce which commands are allowed to run

Non-stdio server behavior:


Remote servers (HTTP, SSE, WebSocket) use URL-based matching when serverUrl entries exist in the allowlist

If no URL entries exist, remote servers fall back to name-based matching

Command restrictions do not apply to remote servers



 [#how-url-based-restrictions-work] ​


How URL-based restrictions work

URL patterns support wildcards using * to match any sequence of characters. This is useful for allowing entire domains or subdomains.
Wildcard examples:


https://mcp.company.com/* - Allow all paths on a specific domain

https://*.example.com/* - Allow any subdomain of example.com

http://localhost:*/* - Allow any port on localhost

Remote server behavior:


When the allowlist contains any serverUrl entries, remote servers must match one of those URL patterns

Remote servers cannot pass by name alone when URL restrictions are present

This ensures administrators can enforce which remote endpoints are allowed







Example: URL-only allowlist













{
  "allowedMcpServers": [
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ]
}





Result:

HTTP server at https://mcp.company.com/api: ✅ Allowed (matches URL pattern)

HTTP server at https://api.internal.corp/mcp: ✅ Allowed (matches wildcard subdomain)

HTTP server at https://external.com/mcp: ❌ Blocked (doesn’t match any URL pattern)

Stdio server with any command: ❌ Blocked (no name or command entries to match)








Example: Command-only allowlist













{
  "allowedMcpServers": [
    { "serverCommand": ["npx", "-y", "approved-package"] }
  ]
}





Result:

Stdio server with ["npx", "-y", "approved-package"]: ✅ Allowed (matches command)

Stdio server with ["node", "server.js"]: ❌ Blocked (doesn’t match command)

HTTP server named “my-api”: ❌ Blocked (no name entries to match)








Example: Mixed name and command allowlist













{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverCommand": ["npx", "-y", "approved-package"] }
  ]
}





Result:

Stdio server named “local-tool” with ["npx", "-y", "approved-package"]: ✅ Allowed (matches command)

Stdio server named “local-tool” with ["node", "server.js"]: ❌ Blocked (command entries exist but doesn’t match)

Stdio server named “github” with ["node", "server.js"]: ❌ Blocked (stdio servers must match commands when command entries exist)

HTTP server named “github”: ✅ Allowed (matches name)

HTTP server named “other-api”: ❌ Blocked (name doesn’t match)








Example: Name-only allowlist













{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "internal-tool" }
  ]
}





Result:

Stdio server named “github” with any command: ✅ Allowed (no command restrictions)

Stdio server named “internal-tool” with any command: ✅ Allowed (no command restrictions)

HTTP server named “github”: ✅ Allowed (matches name)

Any server named “other”: ❌ Blocked (name doesn’t match)




 [#allowlist-behavior-allowedmcpservers] ​


Allowlist behavior (allowedMcpServers)



undefined (default): No restrictions - users can configure any MCP server

Empty array []: Complete lockdown - users cannot configure any MCP servers

List of entries: Users can only configure servers that match by name, command, or URL pattern



 [#denylist-behavior-deniedmcpservers] ​


Denylist behavior (deniedMcpServers)



undefined (default): No servers are blocked

Empty array []: No servers are blocked

List of entries: Specified servers are explicitly blocked across all scopes



 [#important-notes] ​


Important notes



Option 1 and Option 2 can be combined: If managed-mcp.json exists, it has exclusive control and users cannot add servers. Allowlists/denylists still apply to the managed servers themselves.

Denylist takes absolute precedence: If a server matches a denylist entry (by name, command, or URL), it will be blocked even if it’s on the allowlist

Name-based, command-based, and URL-based restrictions work together: a server passes if it matches either a name entry, a command entry, or a URL pattern (unless blocked by denylist)





When using managed-mcp.json: Users cannot add MCP servers through claude mcp add or configuration files. The allowedMcpServers and deniedMcpServers settings still apply to filter which managed servers are actually loaded.





Was this page helpful?


YesNo






 [/docs/en/agent-teams] Run agent teams [/docs/en/discover-plugins] Discover and install prebuilt plugins





⌘I











 [/docs/en/overview] 
 [https://x.com/AnthropicAI]  [https://www.linkedin.com/company/anthropicresearch] 






 [https://www.anthropic.com/company]  [https://www.anthropic.com/careers]  [https://www.anthropic.com/economic-futures]  [https://www.anthropic.com/research]  [https://www.anthropic.com/news]  [https://trust.anthropic.com/]  [https://www.anthropic.com/transparency] 





 [https://www.anthropic.com/supported-countries]  [https://status.anthropic.com/]  [https://support.claude.com/] 





 [https://www.anthropic.com/learn]  [https://claude.com/partners/mcp]  [https://www.claude.com/customers]  [https://www.anthropic.com/engineering]  [https://www.anthropic.com/events]  [https://claude.com/partners/powered-by-claude]  [https://claude.com/partners/services]  [https://claude.com/programs/startups] 





 [#]  [https://www.anthropic.com/legal/privacy]  [https://www.anthropic.com/responsible-disclosure-policy]  [https://www.anthropic.com/legal/aup]  [https://www.anthropic.com/legal/commercial-terms]  [https://www.anthropic.com/legal/consumer-terms] 












Assistant









Responses are generated using AI and may contain mistakes.
```

### skills

URL: https://code.claude.com/docs/en/skills
Hash: 3861b3001513

```
Extend Claude with skills - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Tools and plugins

Extend Claude with skills




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Agents


 [/docs/en/sub-agents] 

Create custom subagents


 [/docs/en/agent-teams] 

Run agent teams





Tools and plugins


 [/docs/en/mcp] 

Model Context Protocol (MCP)


 [/docs/en/discover-plugins] 

Discover and install prebuilt plugins


 [/docs/en/plugins] 

Create plugins


 [/docs/en/skills] 

Extend Claude with skills





Automation


 [/docs/en/hooks-guide] 

Automate with hooks


 [/docs/en/channels] 

Push external events to Claude


 [/docs/en/scheduled-tasks] 

Run prompts on a schedule


 [/docs/en/headless] 

Programmatic usage





Troubleshooting


 [/docs/en/troubleshooting] 

Troubleshooting











On this page

 [#bundled-skills] Bundled skills
 [#getting-started] Getting started
 [#create-your-first-skill] Create your first skill
 [#where-skills-live] Where skills live
 [#automatic-discovery-from-nested-directories] Automatic discovery from nested directories
 [#skills-from-additional-directories] Skills from additional directories
 [#configure-skills] Configure skills
 [#types-of-skill-content] Types of skill content
 [#frontmatter-reference] Frontmatter reference
 [#available-string-substitutions] Available string substitutions
 [#add-supporting-files] Add supporting files
 [#control-who-invokes-a-skill] Control who invokes a skill
 [#restrict-tool-access] Restrict tool access
 [#pass-arguments-to-skills] Pass arguments to skills
 [#advanced-patterns] Advanced patterns
 [#inject-dynamic-context] Inject dynamic context
 [#run-skills-in-a-subagent] Run skills in a subagent
 [#example-research-skill-using-explore-agent] Example: Research skill using Explore agent
 [#restrict-claude%E2%80%99s-skill-access] Restrict Claude’s skill access
 [#share-skills] Share skills
 [#generate-visual-output] Generate visual output
 [#troubleshooting] Troubleshooting
 [#skill-not-triggering] Skill not triggering
 [#skill-triggers-too-often] Skill triggers too often
 [#skill-descriptions-are-cut-short] Skill descriptions are cut short
 [#related-resources] Related resources

























Skills extend what Claude can do. Create a SKILL.md file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with /skill-name.




For built-in commands like /help and /compact, see the  [/docs/en/commands] built-in commands reference.Custom commands have been merged into skills. A file at .claude/commands/deploy.md and a skill at .claude/skills/deploy/SKILL.md both create /deploy and work the same way. Your existing .claude/commands/ files keep working. Skills add optional features: a directory for supporting files, frontmatter to  [#control-who-invokes-a-skill] control whether you or Claude invokes them, and the ability for Claude to load them automatically when relevant.


Claude Code skills follow the  [https://agentskills.io] Agent Skills open standard, which works across multiple AI tools. Claude Code extends the standard with additional features like  [#control-who-invokes-a-skill] invocation control,  [#run-skills-in-a-subagent] subagent execution, and  [#inject-dynamic-context] dynamic context injection.


 [#bundled-skills] ​


Bundled skills

Bundled skills ship with Claude Code and are available in every session. Unlike  [/docs/en/commands] built-in commands, which execute fixed logic directly, bundled skills are prompt-based: they give Claude a detailed playbook and let it orchestrate the work using its tools. This means bundled skills can spawn parallel agents, read files, and adapt to your codebase.
You invoke bundled skills the same way as any other skill: type / followed by the skill name. In the table below, <arg> indicates a required argument and [arg] indicates an optional one.



SkillPurpose
/batch <instruction>Orchestrate large-scale changes across a codebase in parallel. Researches the codebase, decomposes the work into 5 to 30 independent units, and presents a plan. Once approved, spawns one background agent per unit in an isolated  [/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees] git worktree. Each agent implements its unit, runs tests, and opens a pull request. Requires a git repository. Example: /batch migrate src/ from Solid to React
/claude-apiLoad Claude API reference material for your project’s language (Python, TypeScript, Java, Go, Ruby, C#, PHP, or cURL) and Agent SDK reference for Python and TypeScript. Covers tool use, streaming, batches, structured outputs, and common pitfalls. Also activates automatically when your code imports anthropic, @anthropic-ai/sdk, or claude_agent_sdk
/debug [description]Enable debug logging for the current session and troubleshoot issues by reading the session debug log. Debug logging is off by default unless you started with claude --debug, so running /debug mid-session starts capturing logs from that point forward. Optionally describe the issue to focus the analysis
/loop [interval] <prompt>Run a prompt repeatedly on an interval while the session stays open. Useful for polling a deployment, babysitting a PR, or periodically re-running another skill. Example: /loop 5m check if the deploy finished. See  [/docs/en/scheduled-tasks] Run prompts on a schedule
/simplify [focus]Review your recently changed files for code reuse, quality, and efficiency issues, then fix them. Spawns three review agents in parallel, aggregates their findings, and applies fixes. Pass text to focus on specific concerns: /simplify focus on memory efficiency





 [#getting-started] ​


Getting started



 [#create-your-first-skill] ​


Create your first skill

This example creates a skill that teaches Claude to explain code using visual diagrams and analogies. Since it uses default frontmatter, Claude can load it automatically when you ask how something works, or you can invoke it directly with /explain-code.







1

 [#] 






Create the skill directory

Create a directory for the skill in your personal skills folder. Personal skills are available across all your projects.










mkdir -p ~/.claude/skills/explain-code














2

 [#] 






Write SKILL.md

Every skill needs a SKILL.md file with two parts: YAML frontmatter (between --- markers) that tells Claude when to use the skill, and markdown content with instructions Claude follows when the skill is invoked. The name field becomes the /slash-command, and the description helps Claude decide when to load it automatically.Create ~/.claude/skills/explain-code/SKILL.md:










---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
---

When explaining code, always include:

1. **Start with an analogy**: Compare the code to something from everyday life
2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
3. **Walk through the code**: Explain step-by-step what happens
4. **Highlight a gotcha**: What's a common mistake or misconception?

Keep explanations conversational. For complex concepts, use multiple analogies.














3

 [#] 






Test the skill

You can test it two ways:Let Claude invoke it automatically by asking something that matches the description:










How does this code work?





Or invoke it directly with the skill name:










/explain-code src/auth/login.ts





Either way, Claude should include an analogy and ASCII diagram in its explanation.






 [#where-skills-live] ​


Where skills live

Where you store a skill determines who can use it:



LocationPathApplies to
EnterpriseSee  [/docs/en/settings#settings-files] managed settingsAll users in your organization
Personal~/.claude/skills/<skill-name>/SKILL.mdAll your projects
Project.claude/skills/<skill-name>/SKILL.mdThis project only
Plugin<plugin>/skills/<skill-name>/SKILL.mdWhere plugin is enabled



When skills share the same name across levels, higher-priority locations win: enterprise > personal > project. Plugin skills use a plugin-name:skill-name namespace, so they cannot conflict with other levels. If you have files in .claude/commands/, those work the same way, but if a skill and a command share the same name, the skill takes precedence.


 [#automatic-discovery-from-nested-directories] ​


Automatic discovery from nested directories

When you work with files in subdirectories, Claude Code automatically discovers skills from nested .claude/skills/ directories. For example, if you’re editing a file in packages/frontend/, Claude Code also looks for skills in packages/frontend/.claude/skills/. This supports monorepo setups where packages have their own skills.
Each skill is a directory with SKILL.md as the entrypoint:











my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute






The SKILL.md contains the main instructions and is required. Other files are optional and let you build more powerful skills: templates for Claude to fill in, example outputs showing the expected format, scripts Claude can execute, or detailed reference documentation. Reference these files from your SKILL.md so Claude knows what they contain and when to load them. See  [#add-supporting-files] Add supporting files for more details.




Files in .claude/commands/ still work and support the same  [#frontmatter-reference] frontmatter. Skills are recommended since they support additional features like supporting files.




 [#skills-from-additional-directories] ​


Skills from additional directories

Skills defined in .claude/skills/ within directories added via --add-dir are loaded automatically and picked up by live change detection, so you can edit them during a session without restarting.




CLAUDE.md files from --add-dir directories are not loaded by default. To load them, set CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1. See  [/docs/en/memory#load-from-additional-directories] Load from additional directories.




 [#configure-skills] ​


Configure skills

Skills are configured through YAML frontmatter at the top of SKILL.md and the markdown content that follows.


 [#types-of-skill-content] ​


Types of skill content

Skill files can contain any instructions, but thinking about how you want to invoke them helps guide what to include:
Reference content adds knowledge Claude applies to your current work. Conventions, patterns, style guides, domain knowledge. This content runs inline so Claude can use it alongside your conversation context.











---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation






Task content gives Claude step-by-step instructions for a specific action, like deployments, commits, or code generation. These are often actions you want to invoke directly with /skill-name rather than letting Claude decide when to run them. Add disable-model-invocation: true to prevent Claude from triggering it automatically.











---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target






Your SKILL.md can contain anything, but thinking through how you want the skill invoked (by you, by Claude, or both) and where you want it to run (inline or in a subagent) helps guide what to include. For complex skills, you can also  [#add-supporting-files] add supporting files to keep the main skill focused.


 [#frontmatter-reference] ​


Frontmatter reference

Beyond the markdown content, you can configure skill behavior using YAML frontmatter fields between --- markers at the top of your SKILL.md file:











---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read, Grep
---

Your skill instructions here...






All fields are optional. Only description is recommended so Claude knows when to use the skill.



FieldRequiredDescription
nameNoDisplay name for the skill. If omitted, uses the directory name. Lowercase letters, numbers, and hyphens only (max 64 characters).
descriptionRecommendedWhat the skill does and when to use it. Claude uses this to decide when to apply the skill. If omitted, uses the first paragraph of markdown content. Front-load the key use case: descriptions longer than 250 characters are truncated in the skill listing to reduce context usage.
argument-hintNoHint shown during autocomplete to indicate expected arguments. Example: [issue-number] or [filename] [format].
disable-model-invocationNoSet to true to prevent Claude from automatically loading this skill. Use for workflows you want to trigger manually with /name. Default: false.
user-invocableNoSet to false to hide from the / menu. Use for background knowledge users shouldn’t invoke directly. Default: true.
allowed-toolsNoTools Claude can use without asking permission when this skill is active.
modelNoModel to use when this skill is active.
effortNo [/docs/en/model-config#adjust-effort-level] Effort level when this skill is active. Overrides the session effort level. Default: inherits from session. Options: low, medium, high, max (Opus 4.6 only).
contextNoSet to fork to run in a forked subagent context.
agentNoWhich subagent type to use when context: fork is set.
hooksNoHooks scoped to this skill’s lifecycle. See  [/docs/en/hooks#hooks-in-skills-and-agents] Hooks in skills and agents for configuration format.
pathsNoGlob patterns that limit when this skill is activated. Accepts a comma-separated string or a YAML list. When set, Claude loads the skill automatically only when working with files matching the patterns. Uses the same format as  [/docs/en/memory#path-specific-rules] path-specific rules.
shellNoShell to use for !`command` blocks in this skill. Accepts bash (default) or powershell. Setting powershell runs inline shell commands via PowerShell on Windows. Requires CLAUDE_CODE_USE_POWERSHELL_TOOL=1.





 [#available-string-substitutions] ​


Available string substitutions

Skills support string substitution for dynamic values in the skill content:



VariableDescription
$ARGUMENTSAll arguments passed when invoking the skill. If $ARGUMENTS is not present in the content, arguments are appended as ARGUMENTS: <value>.
$ARGUMENTS[N]Access a specific argument by 0-based index, such as $ARGUMENTS[0] for the first argument.
$NShorthand for $ARGUMENTS[N], such as $0 for the first argument or $1 for the second.
${CLAUDE_SESSION_ID}The current session ID. Useful for logging, creating session-specific files, or correlating skill output with sessions.
${CLAUDE_SKILL_DIR}The directory containing the skill’s SKILL.md file. For plugin skills, this is the skill’s subdirectory within the plugin, not the plugin root. Use this in bash injection commands to reference scripts or files bundled with the skill, regardless of the current working directory.



Example using substitutions:











---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS








 [#add-supporting-files] ​


Add supporting files

Skills can include multiple files in their directory. This keeps SKILL.md focused on the essentials while letting Claude access detailed reference material only when needed. Large reference docs, API specifications, or example collections don’t need to load into context every time the skill runs.











my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)






Reference supporting files from SKILL.md so Claude knows what each file contains and when to load it:











## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)










Keep SKILL.md under 500 lines. Move detailed reference material to separate files.




 [#control-who-invokes-a-skill] ​


Control who invokes a skill

By default, both you and Claude can invoke any skill. You can type /skill-name to invoke it directly, and Claude can load it automatically when relevant to your conversation. Two frontmatter fields let you restrict this:



disable-model-invocation: true: Only you can invoke the skill. Use this for workflows with side effects or that you want to control timing, like /commit, /deploy, or /send-slack-message. You don’t want Claude deciding to deploy because your code looks ready.



user-invocable: false: Only Claude can invoke the skill. Use this for background knowledge that isn’t actionable as a command. A legacy-system-context skill explains how an old system works. Claude should know this when relevant, but /legacy-system-context isn’t a meaningful action for users to take.


This example creates a deploy skill that only you can trigger. The disable-model-invocation: true field prevents Claude from running it automatically:











---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded






Here’s how the two fields affect invocation and context loading:



FrontmatterYou can invokeClaude can invokeWhen loaded into context
(default)YesYesDescription always in context, full skill loads when invoked
disable-model-invocation: trueYesNoDescription not in context, full skill loads when you invoke
user-invocable: falseNoYesDescription always in context, full skill loads when invoked







In a regular session, skill descriptions are loaded into context so Claude knows what’s available, but full skill content only loads when invoked.  [/docs/en/sub-agents#preload-skills-into-subagents] Subagents with preloaded skills work differently: the full skill content is injected at startup.




 [#restrict-tool-access] ​


Restrict tool access

Use the allowed-tools field to limit which tools Claude can use when a skill is active. This skill creates a read-only mode where Claude can explore files but not modify them:











---
name: safe-reader
description: Read files without making changes
allowed-tools: Read, Grep, Glob
---








 [#pass-arguments-to-skills] ​


Pass arguments to skills

Both you and Claude can pass arguments when invoking a skill. Arguments are available via the $ARGUMENTS placeholder.
This skill fixes a GitHub issue by number. The $ARGUMENTS placeholder gets replaced with whatever follows the skill name:











---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit






When you run /fix-issue 123, Claude receives “Fix GitHub issue 123 following our coding standards…”
If you invoke a skill with arguments but the skill doesn’t include $ARGUMENTS, Claude Code appends ARGUMENTS: <your input> to the end of the skill content so Claude still sees what you typed.
To access individual arguments by position, use $ARGUMENTS[N] or the shorter $N:











---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.






Running /migrate-component SearchBar React Vue replaces $ARGUMENTS[0] with SearchBar, $ARGUMENTS[1] with React, and $ARGUMENTS[2] with Vue. The same skill using the $N shorthand:











---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.








 [#advanced-patterns] ​


Advanced patterns



 [#inject-dynamic-context] ​


Inject dynamic context

The !`<command>` syntax runs shell commands before the skill content is sent to Claude. The command output replaces the placeholder, so Claude receives actual data, not the command itself.
This skill summarizes a pull request by fetching live PR data with the GitHub CLI. The !`gh pr diff` and other commands run first, and their output gets inserted into the prompt:











---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...






When this skill runs:


Each !`<command>` executes immediately (before Claude sees anything)

The output replaces the placeholder in the skill content

Claude receives the fully-rendered prompt with actual PR data

This is preprocessing, not something Claude executes. Claude only sees the final result.




To enable  [/docs/en/common-workflows#use-extended-thinking-thinking-mode] extended thinking in a skill, include the word “ultrathink” anywhere in your skill content.




 [#run-skills-in-a-subagent] ​


Run skills in a subagent

Add context: fork to your frontmatter when you want a skill to run in isolation. The skill content becomes the prompt that drives the subagent. It won’t have access to your conversation history.




context: fork only makes sense for skills with explicit instructions. If your skill contains guidelines like “use these API conventions” without a task, the subagent receives the guidelines but no actionable prompt, and returns without meaningful output.


Skills and  [/docs/en/sub-agents] subagents work together in two directions:



ApproachSystem promptTaskAlso loads
Skill with context: forkFrom agent type (Explore, Plan, etc.)SKILL.md contentCLAUDE.md
Subagent with skills fieldSubagent’s markdown bodyClaude’s delegation messagePreloaded skills + CLAUDE.md



With context: fork, you write the task in your skill and pick an agent type to execute it. For the inverse (defining a custom subagent that uses skills as reference material), see  [/docs/en/sub-agents#preload-skills-into-subagents] Subagents.


 [#example-research-skill-using-explore-agent] ​


Example: Research skill using Explore agent

This skill runs research in a forked Explore agent. The skill content becomes the task, and the agent provides read-only tools optimized for codebase exploration:











---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references






When this skill runs:


A new isolated context is created

The subagent receives the skill content as its prompt (“Research $ARGUMENTS thoroughly…”)

The agent field determines the execution environment (model, tools, and permissions)

Results are summarized and returned to your main conversation

The agent field specifies which subagent configuration to use. Options include built-in agents (Explore, Plan, general-purpose) or any custom subagent from .claude/agents/. If omitted, uses general-purpose.


 [#restrict-claude’s-skill-access] ​


Restrict Claude’s skill access

By default, Claude can invoke any skill that doesn’t have disable-model-invocation: true set. Skills that define allowed-tools grant Claude access to those tools without per-use approval when the skill is active. Your  [/docs/en/permissions] permission settings still govern baseline approval behavior for all other tools. Built-in commands like /compact and /init are not available through the Skill tool.
Three ways to control which skills Claude can invoke:
Disable all skills by denying the Skill tool in /permissions:











# Add to deny rules:
Skill






Allow or deny specific skills using  [/docs/en/permissions] permission rules:











# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)






Permission syntax: Skill(name) for exact match, Skill(name *) for prefix match with any arguments.
Hide individual skills by adding disable-model-invocation: true to their frontmatter. This removes the skill from Claude’s context entirely.




The user-invocable field only controls menu visibility, not Skill tool access. Use disable-model-invocation: true to block programmatic invocation.




 [#share-skills] ​


Share skills

Skills can be distributed at different scopes depending on your audience:


Project skills: Commit .claude/skills/ to version control

Plugins: Create a skills/ directory in your  [/docs/en/plugins] plugin

Managed: Deploy organization-wide through  [/docs/en/settings#settings-files] managed settings



 [#generate-visual-output] ​


Generate visual output

Skills can bundle and run scripts in any language, giving Claude capabilities beyond what’s possible in a single prompt. One powerful pattern is generating visual output: interactive HTML files that open in your browser for exploring data, debugging, or creating reports.
This example creates a codebase explorer: an interactive tree view where you can expand and collapse directories, see file sizes at a glance, and identify file types by color.
Create the Skill directory:











mkdir -p ~/.claude/skills/codebase-visualizer/scripts






Create ~/.claude/skills/codebase-visualizer/SKILL.md. The description tells Claude when to activate this Skill, and the instructions tell Claude to run the bundled script:











---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python *)
---

# Codebase Visualizer

Generate an interactive HTML tree view that shows your project's file structure with collapsible directories.

## Usage

Run the visualization script from your project root:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

This creates `codebase-map.html` in the current directory and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder






Create ~/.claude/skills/codebase-visualizer/scripts/visualize.py. This script scans a directory tree and generates a self-contained HTML file with:


A summary sidebar showing file count, directory count, total size, and number of file types

A bar chart breaking down the codebase by file type (top 8 by size)

A collapsible tree where you can expand and collapse directories, with color-coded file type indicators

The script requires Python but uses only built-in libraries, so there are no packages to install:











#!/usr/bin/env python3
"""Generate an interactive collapsible tree visualization of a codebase."""

import json
import sys
import webbrowser
from pathlib import Path
from collections import Counter

IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]
    colors = {
        '.js': '#f7df1e', '.ts': '#3178c6', '.py': '#3776ab', '.go': '#00add8',
        '.rs': '#dea584', '.rb': '#cc342d', '.css': '#264de4', '.html': '#e34c26',
        '.json': '#6b7280', '.md': '#083fa1', '.yaml': '#cb171e', '.yml': '#cb171e',
        '.mdx': '#083fa1', '.tsx': '#3178c6', '.jsx': '#61dafb', '.sh': '#4eaa25',
    }
    lang_bars = "".join(
        f'<div class="bar-row"><span class="bar-label">{ext}</span>'
        f'<div class="bar" style="width:{(size/total_size)*100}%;background:{colors.get(ext,"#6b7280")}"></div>'
        f'<span class="bar-pct">{(size/total_size)*100:.1f}%</span></div>'
        for ext, size in sorted_exts
    )
    def fmt(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.1f} MB"

    html = f'''<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"><title>Codebase Explorer</title>
  <style>
    body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
    .container {{ display: flex; height: 100vh; }}
    .sidebar {{ width: 280px; background: #252542; padding: 20px; border-right: 1px solid #3d3d5c; overflow-y: auto; flex-shrink: 0; }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 10px 0; font-size: 18px; }}
    h2 {{ margin: 20px 0 10px 0; font-size: 14px; color: #888; text-transform: uppercase; }}
    .stat {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #3d3d5c; }}
    .stat-value {{ font-weight: bold; }}
    .bar-row {{ display: flex; align-items: center; margin: 6px 0; }}
    .bar-label {{ width: 55px; font-size: 12px; color: #aaa; }}
    .bar {{ height: 18px; border-radius: 3px; }}
    .bar-pct {{ margin-left: 8px; font-size: 12px; color: #666; }}
    .tree {{ list-style: none; padding-left: 20px; }}
    details {{ cursor: pointer; }}
    summary {{ padding: 4px 8px; border-radius: 4px; }}
    summary:hover {{ background: #2d2d44; }}
    .folder {{ color: #ffd700; }}
    .file {{ display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; }}
    .file:hover {{ background: #2d2d44; }}
    .size {{ color: #888; margin-left: auto; font-size: 12px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
  </style>
</head><body>
  <div class="container">
    <div class="sidebar">
      <h1>📊 Summary</h1>
      <div class="stat"><span>Files</span><span class="stat-value">{stats["files"]:,}</span></div>
      <div class="stat"><span>Directories</span><span class="stat-value">{stats["dirs"]:,}</span></div>
      <div class="stat"><span>Total size</span><span class="stat-value">{fmt(data["size"])}</span></div>
      <div class="stat"><span>File types</span><span class="stat-value">{len(stats["extensions"])}</span></div>
      <h2>By file type</h2>
      {lang_bars}
    </div>
    <div class="main">
      <h1>📁 {data["name"]}</h1>
      <ul class="tree" id="root"></ul>
    </div>
  </div>
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `<summary><span class="folder">📁 ${{node.name}}</span><span class="size">${{fmt(node.size)}}</span></summary>`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `<span class="dot" style="background:${{colors[node.ext]||'#6b7280'}}"></span>${{node.name}}<span class="size">${{fmt(node.size)}}</span>`;
        parent.appendChild(li);
      }}
    }}
    data.children.forEach(c => render(c, document.getElementById('root')));
  </script>
</body></html>'''
    output.write_text(html)

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')



See all 131 lines


To test, open Claude Code in any project and ask “Visualize this codebase.” Claude runs the script, generates codebase-map.html, and opens it in your browser.
This pattern works for any visual output: dependency graphs, test coverage reports, API documentation, or database schema visualizations. The bundled script does the heavy lifting while Claude handles orchestration.


 [#troubleshooting] ​


Troubleshooting



 [#skill-not-triggering] ​


Skill not triggering

If Claude doesn’t use your skill when expected:


Check the description includes keywords users would naturally say

Verify the skill appears in What skills are available?

Try rephrasing your request to match the description more closely

Invoke it directly with /skill-name if the skill is user-invocable



 [#skill-triggers-too-often] ​


Skill triggers too often

If Claude uses your skill when you don’t want it:


Make the description more specific

Add disable-model-invocation: true if you only want manual invocation



 [#skill-descriptions-are-cut-short] ​


Skill descriptions are cut short

Skill descriptions are loaded into context so Claude knows what’s available. All skill names are always included, but if you have many skills, descriptions are shortened to fit the character budget, which can strip the keywords Claude needs to match your request. The budget scales dynamically at 1% of the context window, with a fallback of 8,000 characters.
To raise the limit, set the SLASH_COMMAND_TOOL_CHAR_BUDGET environment variable. Or trim descriptions at the source: front-load the key use case, since each entry is capped at 250 characters regardless of budget.


 [#related-resources] ​


Related resources



 [/docs/en/sub-agents] Subagents: delegate tasks to specialized agents

 [/docs/en/plugins] Plugins: package and distribute skills with other extensions

 [/docs/en/hooks] Hooks: automate workflows around tool events

 [/docs/en/memory] Memory: manage CLAUDE.md files for persistent context

 [/docs/en/commands] Built-in commands: reference for built-in / commands

 [/docs/en/permissions] Permissions: control tool and skill access




Was this page helpful?


YesNo






 [/docs/en/plugins] Create plugins [/docs/en/hooks-guide] Automate with hooks





⌘I











 [/docs/en/overview] 
 [https://x.com/AnthropicAI]  [https://www.linkedin.com/company/anthropicresearch] 






 [https://www.anthropic.com/company]  [https://www.anthropic.com/careers]  [https://www.anthropic.com/economic-futures]  [https://www.anthropic.com/research]  [https://www.anthropic.com/news]  [https://trust.anthropic.com/]  [https://www.anthropic.com/transparency] 





 [https://www.anthropic.com/supported-countries]  [https://status.anthropic.com/]  [https://support.claude.com/] 





 [https://www.anthropic.com/learn]  [https://claude.com/partners/mcp]  [https://www.claude.com/customers]  [https://www.anthropic.com/engineering]  [https://www.anthropic.com/events]  [https://claude.com/partners/powered-by-claude]  [https://claude.com/partners/services]  [https://claude.com/programs/startups] 





 [#]  [https://www.anthropic.com/legal/privacy]  [https://www.anthropic.com/responsible-disclosure-policy]  [https://www.anthropic.com/legal/aup]  [https://www.anthropic.com/legal/commercial-terms]  [https://www.anthropic.com/legal/consumer-terms] 












Assistant









Responses are generated using AI and may contain mistakes.
```

### hooks

URL: https://code.claude.com/docs/en/hooks
Hash: b6e81a5a2c37

```
Hooks reference - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Reference

Hooks reference




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Reference


 [/docs/en/cli-reference] 

CLI reference


 [/docs/en/commands] 

Built-in commands


 [/docs/en/env-vars] 

Environment variables


 [/docs/en/tools-reference] 

Tools reference


 [/docs/en/interactive-mode] 

Interactive mode


 [/docs/en/checkpointing] 

Checkpointing


 [/docs/en/hooks] 

Hooks reference


 [/docs/en/plugins-reference] 

Plugins reference


 [/docs/en/channels-reference] 

Channels reference











On this page

 [#hook-lifecycle] Hook lifecycle
 [#how-a-hook-resolves] How a hook resolves
 [#configuration] Configuration
 [#hook-locations] Hook locations
 [#matcher-patterns] Matcher patterns
 [#match-mcp-tools] Match MCP tools
 [#hook-handler-fields] Hook handler fields
 [#common-fields] Common fields
 [#command-hook-fields] Command hook fields
 [#http-hook-fields] HTTP hook fields
 [#prompt-and-agent-hook-fields] Prompt and agent hook fields
 [#reference-scripts-by-path] Reference scripts by path
 [#hooks-in-skills-and-agents] Hooks in skills and agents
 [#the-%2Fhooks-menu] The /hooks menu
 [#disable-or-remove-hooks] Disable or remove hooks
 [#hook-input-and-output] Hook input and output
 [#common-input-fields] Common input fields
 [#exit-code-output] Exit code output
 [#exit-code-2-behavior-per-event] Exit code 2 behavior per event
 [#http-response-handling] HTTP response handling
 [#json-output] JSON output
 [#decision-control] Decision control
 [#hook-events] Hook events
 [#sessionstart] SessionStart
 [#sessionstart-input] SessionStart input
 [#sessionstart-decision-control] SessionStart decision control
 [#persist-environment-variables] Persist environment variables
 [#instructionsloaded] InstructionsLoaded
 [#instructionsloaded-input] InstructionsLoaded input
 [#instructionsloaded-decision-control] InstructionsLoaded decision control
 [#userpromptsubmit] UserPromptSubmit
 [#userpromptsubmit-input] UserPromptSubmit input
 [#userpromptsubmit-decision-control] UserPromptSubmit decision control
 [#pretooluse] PreToolUse
 [#pretooluse-input] PreToolUse input
 [#pretooluse-decision-control] PreToolUse decision control
 [#permissionrequest] PermissionRequest
 [#permissionrequest-input] PermissionRequest input
 [#permissionrequest-decision-control] PermissionRequest decision control
 [#permission-update-entries] Permission update entries
 [#posttooluse] PostToolUse
 [#posttooluse-input] PostToolUse input
 [#posttooluse-decision-control] PostToolUse decision control
 [#posttoolusefailure] PostToolUseFailure
 [#posttoolusefailure-input] PostToolUseFailure input
 [#posttoolusefailure-decision-control] PostToolUseFailure decision control
 [#notification] Notification
 [#notification-input] Notification input
 [#subagentstart] SubagentStart
 [#subagentstart-input] SubagentStart input
 [#subagentstop] SubagentStop
 [#subagentstop-input] SubagentStop input
 [#taskcreated] TaskCreated
 [#taskcreated-input] TaskCreated input
 [#taskcreated-decision-control] TaskCreated decision control
 [#taskcompleted] TaskCompleted
 [#taskcompleted-input] TaskCompleted input
 [#taskcompleted-decision-control] TaskCompleted decision control
 [#stop] Stop
 [#stop-input] Stop input
 [#stop-decision-control] Stop decision control
 [#stopfailure] StopFailure
 [#stopfailure-input] StopFailure input
 [#teammateidle] TeammateIdle
 [#teammateidle-input] TeammateIdle input
 [#teammateidle-decision-control] TeammateIdle decision control
 [#configchange] ConfigChange
 [#configchange-input] ConfigChange input
 [#configchange-decision-control] ConfigChange decision control
 [#cwdchanged] CwdChanged
 [#cwdchanged-input] CwdChanged input
 [#cwdchanged-output] CwdChanged output
 [#filechanged] FileChanged
 [#filechanged-input] FileChanged input
 [#filechanged-output] FileChanged output
 [#worktreecreate] WorktreeCreate
 [#worktreecreate-input] WorktreeCreate input
 [#worktreecreate-output] WorktreeCreate output
 [#worktreeremove] WorktreeRemove
 [#worktreeremove-input] WorktreeRemove input
 [#precompact] PreCompact
 [#precompact-input] PreCompact input
 [#postcompact] PostCompact
 [#postcompact-input] PostCompact input
 [#sessionend] SessionEnd
 [#sessionend-input] SessionEnd input
 [#elicitation] Elicitation
 [#elicitation-input] Elicitation input
 [#elicitation-output] Elicitation output
 [#elicitationresult] ElicitationResult
 [#elicitationresult-input] ElicitationResult input
 [#elicitationresult-output] ElicitationResult output
 [#prompt-based-hooks] Prompt-based hooks
 [#how-prompt-based-hooks-work] How prompt-based hooks work
 [#prompt-hook-configuration] Prompt hook configuration
 [#response-schema] Response schema
 [#example-multi-criteria-stop-hook] Example: Multi-criteria Stop hook
 [#agent-based-hooks] Agent-based hooks
 [#how-agent-hooks-work] How agent hooks work
 [#agent-hook-configuration] Agent hook configuration
 [#run-hooks-in-the-background] Run hooks in the background
 [#configure-an-async-hook] Configure an async hook
 [#how-async-hooks-execute] How async hooks execute
 [#example-run-tests-after-file-changes] Example: run tests after file changes
 [#limitations] Limitations
 [#security-considerations] Security considerations
 [#disclaimer] Disclaimer
 [#security-best-practices] Security best practices
 [#windows-powershell-tool] Windows PowerShell tool
 [#debug-hooks] Debug hooks





























For a quickstart guide with examples, see  [/docs/en/hooks-guide] Automate workflows with hooks.


Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code’s lifecycle. Use this reference to look up event schemas, configuration options, JSON input/output formats, and advanced features like async hooks, HTTP hooks, and MCP tool hooks. If you’re setting up hooks for the first time, start with the  [/docs/en/hooks-guide] guide instead.


 [#hook-lifecycle] ​


Hook lifecycle

Hooks fire at specific points during a Claude Code session. When an event fires and a matcher matches, Claude Code passes JSON context about the event to your hook handler. For command hooks, input arrives on stdin. For HTTP hooks, it arrives as the POST request body. Your handler can then inspect the input, take action, and optionally return a decision. Some events fire once per session, while others fire repeatedly inside the agentic loop:













The table below summarizes when each event fires. The  [#hook-events] Hook events section documents the full input schema and decision control options for each one.



EventWhen it fires
SessionStartWhen a session begins or resumes
UserPromptSubmitWhen you submit a prompt, before Claude processes it
PreToolUseBefore a tool call executes. Can block it
PermissionRequestWhen a permission dialog appears
PostToolUseAfter a tool call succeeds
PostToolUseFailureAfter a tool call fails
NotificationWhen Claude Code sends a notification
SubagentStartWhen a subagent is spawned
SubagentStopWhen a subagent finishes
TaskCreatedWhen a task is being created via TaskCreate
TaskCompletedWhen a task is being marked as completed
StopWhen Claude finishes responding
StopFailureWhen the turn ends due to an API error. Output and exit code are ignored
TeammateIdleWhen an  [/docs/en/agent-teams] agent team teammate is about to go idle
InstructionsLoadedWhen a CLAUDE.md or .claude/rules/*.md file is loaded into context. Fires at session start and when files are lazily loaded during a session
ConfigChangeWhen a configuration file changes during a session
CwdChangedWhen the working directory changes, for example when Claude executes a cd command. Useful for reactive environment management with tools like direnv
FileChangedWhen a watched file changes on disk. The matcher field specifies which filenames to watch
WorktreeCreateWhen a worktree is being created via --worktree or isolation: "worktree". Replaces default git behavior
WorktreeRemoveWhen a worktree is being removed, either at session exit or when a subagent finishes
PreCompactBefore context compaction
PostCompactAfter context compaction completes
ElicitationWhen an MCP server requests user input during a tool call
ElicitationResultAfter a user responds to an MCP elicitation, before the response is sent back to the server
SessionEndWhen a session terminates





 [#how-a-hook-resolves] ​


How a hook resolves

To see how these pieces fit together, consider this PreToolUse hook that blocks destructive shell commands. The matcher narrows to Bash tool calls and the if condition narrows further to commands starting with rm, so block-rm.sh only spawns when both filters match:











{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}






The script reads the JSON input from stdin, extracts the command, and returns a permissionDecision of "deny" if it contains rm -rf:











#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # allow the command
fi






Now suppose Claude Code decides to run Bash "rm -rf /tmp/build". Here’s what happens:


















1

 [#] 






Event fires

The PreToolUse event fires. Claude Code sends the tool input as JSON on stdin to the hook:










{ "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }














2

 [#] 






Matcher checks

The matcher "Bash" matches the tool name, so this hook group activates. If you omit the matcher or use "*", the group activates on every occurrence of the event.








3

 [#] 






If condition checks

The if condition "Bash(rm *)" matches because the command starts with rm, so this handler spawns. If the command had been npm test, the if check would fail and block-rm.sh would never run, avoiding the process spawn overhead. The if field is optional; without it, every handler in the matched group runs.








4

 [#] 






Hook handler runs

The script inspects the full command and finds rm -rf, so it prints a decision to stdout:










{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook"
  }
}





If the command had been a safer rm variant like rm file.txt, the script would hit exit 0 instead, which tells Claude Code to allow the tool call with no further action.








5

 [#] 






Claude Code acts on the result

Claude Code reads the JSON decision, blocks the tool call, and shows Claude the reason.




The  [#configuration] Configuration section below documents the full schema, and each  [#hook-events] hook event section documents what input your command receives and what output it can return.


 [#configuration] ​


Configuration

Hooks are defined in JSON settings files. The configuration has three levels of nesting:


Choose a  [#hook-events] hook event to respond to, like PreToolUse or Stop

Add a  [#matcher-patterns] matcher group to filter when it fires, like “only for the Bash tool”

Define one or more  [#hook-handler-fields] hook handlers to run when matched

See  [#how-a-hook-resolves] How a hook resolves above for a complete walkthrough with an annotated example.




This page uses specific terms for each level: hook event for the lifecycle point, matcher group for the filter, and hook handler for the shell command, HTTP endpoint, prompt, or agent that runs. “Hook” on its own refers to the general feature.




 [#hook-locations] ​


Hook locations

Where you define a hook determines its scope:



LocationScopeShareable
~/.claude/settings.jsonAll your projectsNo, local to your machine
.claude/settings.jsonSingle projectYes, can be committed to the repo
.claude/settings.local.jsonSingle projectNo, gitignored
Managed policy settingsOrganization-wideYes, admin-controlled
 [/docs/en/plugins] Plugin hooks/hooks.jsonWhen plugin is enabledYes, bundled with the plugin
 [/docs/en/skills] Skill or  [/docs/en/sub-agents] agent frontmatterWhile the component is activeYes, defined in the component file



For details on settings file resolution, see  [/docs/en/settings] settings. Enterprise administrators can use allowManagedHooksOnly to block user, project, and plugin hooks. See  [/docs/en/settings#hook-configuration] Hook configuration.


 [#matcher-patterns] ​


Matcher patterns

The matcher field is a regex string that filters when hooks fire. Use "*", "", or omit matcher entirely to match all occurrences. Each event type matches on a different field:



EventWhat the matcher filtersExample matcher values
PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequesttool nameBash, Edit|Write, mcp__.*
SessionStarthow the session startedstartup, resume, clear, compact
SessionEndwhy the session endedclear, resume, logout, prompt_input_exit, bypass_permissions_disabled, other
Notificationnotification typepermission_prompt, idle_prompt, auth_success, elicitation_dialog
SubagentStartagent typeBash, Explore, Plan, or custom agent names
PreCompact, PostCompactwhat triggered compactionmanual, auto
SubagentStopagent typesame values as SubagentStart
ConfigChangeconfiguration sourceuser_settings, project_settings, local_settings, policy_settings, skills
CwdChangedno matcher supportalways fires on every directory change
FileChangedfilename (basename of the changed file).envrc, .env, any filename you want to watch
StopFailureerror typerate_limit, authentication_failed, billing_error, invalid_request, server_error, max_output_tokens, unknown
InstructionsLoadedload reasonsession_start, nested_traversal, path_glob_match, include, compact
ElicitationMCP server nameyour configured MCP server names
ElicitationResultMCP server namesame values as Elicitation
UserPromptSubmit, Stop, TeammateIdle, TaskCreated, TaskCompleted, WorktreeCreate, WorktreeRemoveno matcher supportalways fires on every occurrence



The matcher is a regex, so Edit|Write matches either tool and Notebook.* matches any tool starting with Notebook. The matcher runs against a field from the  [#hook-input-and-output] JSON input that Claude Code sends to your hook on stdin. For tool events, that field is tool_name. Each  [#hook-events] hook event section lists the full set of matcher values and the input schema for that event.
This example runs a linting script only when Claude writes or edits a file:











{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}






UserPromptSubmit, Stop, TeammateIdle, TaskCreated, TaskCompleted, WorktreeCreate, WorktreeRemove, and CwdChanged don’t support matchers and always fire on every occurrence. If you add a matcher field to these events, it is silently ignored.
For tool events, you can filter more narrowly by setting the  [#common-fields] if field on individual hook handlers. if uses  [/docs/en/permissions] permission rule syntax to match against the tool name and arguments together, so "Bash(git *)" runs only for git commands and "Edit(*.ts)" runs only for TypeScript files.


 [#match-mcp-tools] ​


Match MCP tools

 [/docs/en/mcp] MCP server tools appear as regular tools in tool events (PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest), so you can match them the same way you match any other tool name.
MCP tools follow the naming pattern mcp__<server>__<tool>, for example:


mcp__memory__create_entities: Memory server’s create entities tool

mcp__filesystem__read_file: Filesystem server’s read file tool

mcp__github__search_repositories: GitHub server’s search tool

Use regex patterns to target specific MCP tools or groups of tools:


mcp__memory__.* matches all tools from the memory server

mcp__.*__write.* matches any tool containing “write” from any server

This example logs all memory server operations and validates write operations from any MCP server:











{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}








 [#hook-handler-fields] ​


Hook handler fields

Each object in the inner hooks array is a hook handler: the shell command, HTTP endpoint, LLM prompt, or agent that runs when the matcher matches. There are four types:


 [#command-hook-fields] Command hooks (type: "command"): run a shell command. Your script receives the event’s  [#hook-input-and-output] JSON input on stdin and communicates results back through exit codes and stdout.

 [#http-hook-fields] HTTP hooks (type: "http"): send the event’s JSON input as an HTTP POST request to a URL. The endpoint communicates results back through the response body using the same  [#json-output] JSON output format as command hooks.

 [#prompt-and-agent-hook-fields] Prompt hooks (type: "prompt"): send a prompt to a Claude model for single-turn evaluation. The model returns a yes/no decision as JSON. See  [#prompt-based-hooks] Prompt-based hooks.

 [#prompt-and-agent-hook-fields] Agent hooks (type: "agent"): spawn a subagent that can use tools like Read, Grep, and Glob to verify conditions before returning a decision. See  [#agent-based-hooks] Agent-based hooks.



 [#common-fields] ​


Common fields

These fields apply to all hook types:



FieldRequiredDescription
typeyes"command", "http", "prompt", or "agent"
ifnoPermission rule syntax to filter when this hook runs, such as "Bash(git *)" or "Edit(*.ts)". The hook only spawns if the tool call matches the pattern. Only evaluated on tool events: PreToolUse, PostToolUse, PostToolUseFailure, and PermissionRequest. On other events, a hook with if set never runs. Uses the same syntax as  [/docs/en/permissions] permission rules
timeoutnoSeconds before canceling. Defaults: 600 for command, 30 for prompt, 60 for agent
statusMessagenoCustom spinner message displayed while the hook runs
oncenoIf true, runs only once per session then is removed. Skills only, not agents. See  [#hooks-in-skills-and-agents] Hooks in skills and agents





 [#command-hook-fields] ​


Command hook fields

In addition to the  [#common-fields] common fields, command hooks accept these fields:



FieldRequiredDescription
commandyesShell command to execute
asyncnoIf true, runs in the background without blocking. See  [#run-hooks-in-the-background] Run hooks in the background
shellnoShell to use for this hook. Accepts "bash" (default) or "powershell". Setting "powershell" runs the command via PowerShell on Windows. Does not require CLAUDE_CODE_USE_POWERSHELL_TOOL since hooks spawn PowerShell directly





 [#http-hook-fields] ​


HTTP hook fields

In addition to the  [#common-fields] common fields, HTTP hooks accept these fields:



FieldRequiredDescription
urlyesURL to send the POST request to
headersnoAdditional HTTP headers as key-value pairs. Values support environment variable interpolation using $VAR_NAME or ${VAR_NAME} syntax. Only variables listed in allowedEnvVars are resolved
allowedEnvVarsnoList of environment variable names that may be interpolated into header values. References to unlisted variables are replaced with empty strings. Required for any env var interpolation to work



Claude Code sends the hook’s  [#hook-input-and-output] JSON input as the POST request body with Content-Type: application/json. The response body uses the same  [#json-output] JSON output format as command hooks.
Error handling differs from command hooks: non-2xx responses, connection failures, and timeouts all produce non-blocking errors that allow execution to continue. To block a tool call or deny a permission, return a 2xx response with a JSON body containing decision: "block" or a hookSpecificOutput with permissionDecision: "deny".
This example sends PreToolUse events to a local validation service, authenticating with a token from the MY_TOKEN environment variable:











{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}








 [#prompt-and-agent-hook-fields] ​


Prompt and agent hook fields

In addition to the  [#common-fields] common fields, prompt and agent hooks accept these fields:



FieldRequiredDescription
promptyesPrompt text to send to the model. Use $ARGUMENTS as a placeholder for the hook input JSON
modelnoModel to use for evaluation. Defaults to a fast model



All matching hooks run in parallel, and identical handlers are deduplicated automatically. Command hooks are deduplicated by command string, and HTTP hooks are deduplicated by URL. Handlers run in the current directory with Claude Code’s environment. The $CLAUDE_CODE_REMOTE environment variable is set to "true" in remote web environments and not set in the local CLI.


 [#reference-scripts-by-path] ​


Reference scripts by path

Use environment variables to reference hook scripts relative to the project or plugin root, regardless of the working directory when the hook runs:


$CLAUDE_PROJECT_DIR: the project root. Wrap in quotes to handle paths with spaces.

${CLAUDE_PLUGIN_ROOT}: the plugin’s installation directory, for scripts bundled with a  [/docs/en/plugins] plugin. Changes on each plugin update.

${CLAUDE_PLUGIN_DATA}: the plugin’s  [/docs/en/plugins-reference#persistent-data-directory] persistent data directory, for dependencies and state that should survive plugin updates.




 Project scripts


 Plugin scripts


This example uses $CLAUDE_PROJECT_DIR to run a style checker from the project’s .claude/hooks/ directory after any Write or Edit tool call:










{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
          }
        ]
      }
    ]
  }
}







Define plugin hooks in hooks/hooks.json with an optional top-level description field. When a plugin is enabled, its hooks merge with your user and project hooks.This example runs a formatting script bundled with the plugin:










{
  "description": "Automatic code formatting",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}





See the  [/docs/en/plugins-reference#hooks] plugin components reference for details on creating plugin hooks.





 [#hooks-in-skills-and-agents] ​


Hooks in skills and agents

In addition to settings files and plugins, hooks can be defined directly in  [/docs/en/skills] skills and  [/docs/en/sub-agents] subagents using frontmatter. These hooks are scoped to the component’s lifecycle and only run when that component is active.
All hook events are supported. For subagents, Stop hooks are automatically converted to SubagentStop since that is the event that fires when a subagent completes.
Hooks use the same configuration format as settings-based hooks but are scoped to the component’s lifetime and cleaned up when it finishes.
This skill defines a PreToolUse hook that runs a security validation script before each Bash command:











---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---






Agents use the same format in their YAML frontmatter.


 [#the-/hooks-menu] ​


The /hooks menu

Type /hooks in Claude Code to open a read-only browser for your configured hooks. The menu shows every hook event with a count of configured hooks, lets you drill into matchers, and shows the full details of each hook handler. Use it to verify configuration, check which settings file a hook came from, or inspect a hook’s command, prompt, or URL.
The menu displays all four hook types: command, prompt, agent, and http. Each hook is labeled with a [type] prefix and a source indicating where it was defined:


User: from ~/.claude/settings.json

Project: from .claude/settings.json

Local: from .claude/settings.local.json

Plugin: from a plugin’s hooks/hooks.json

Session: registered in memory for the current session

Built-in: registered internally by Claude Code

Selecting a hook opens a detail view showing its event, matcher, type, source file, and the full command, prompt, or URL. The menu is read-only: to add, modify, or remove hooks, edit the settings JSON directly or ask Claude to make the change.


 [#disable-or-remove-hooks] ​


Disable or remove hooks

To remove a hook, delete its entry from the settings JSON file.
To temporarily disable all hooks without removing them, set "disableAllHooks": true in your settings file. There is no way to disable an individual hook while keeping it in the configuration.
The disableAllHooks setting respects the managed settings hierarchy. If an administrator has configured hooks through managed policy settings, disableAllHooks set in user, project, or local settings cannot disable those managed hooks. Only disableAllHooks set at the managed settings level can disable managed hooks.
Direct edits to hooks in settings files are normally picked up automatically by the file watcher.


 [#hook-input-and-output] ​


Hook input and output

Command hooks receive JSON data via stdin and communicate results through exit codes, stdout, and stderr. HTTP hooks receive the same JSON as the POST request body and communicate results through the HTTP response body. This section covers fields and behavior common to all events. Each event’s section under  [#hook-events] Hook events includes its specific input schema and decision control options.


 [#common-input-fields] ​


Common input fields

Hook events receive these fields as JSON, in addition to event-specific fields documented in each  [#hook-events] hook event section. For command hooks, this JSON arrives via stdin. For HTTP hooks, it arrives as the POST request body.



FieldDescription
session_idCurrent session identifier
transcript_pathPath to conversation JSON
cwdCurrent working directory when the hook is invoked
permission_modeCurrent  [/docs/en/permissions#permission-modes] permission mode: "default", "plan", "acceptEdits", "auto", "dontAsk", or "bypassPermissions". Not all events receive this field: see each event’s JSON example below to check
hook_event_nameName of the event that fired



When running with --agent or inside a subagent, two additional fields are included:



FieldDescription
agent_idUnique identifier for the subagent. Present only when the hook fires inside a subagent call. Use this to distinguish subagent hook calls from main-thread calls.
agent_typeAgent name (for example, "Explore" or "security-reviewer"). Present when the session uses --agent or the hook fires inside a subagent. For subagents, the subagent’s type takes precedence over the session’s --agent value.



For example, a PreToolUse hook for a Bash command receives this on stdin:











{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}






The tool_name and tool_input fields are event-specific. Each  [#hook-events] hook event section documents the additional fields for that event.


 [#exit-code-output] ​


Exit code output

The exit code from your hook command tells Claude Code whether the action should proceed, be blocked, or be ignored.
Exit 0 means success. Claude Code parses stdout for  [#json-output] JSON output fields. JSON output is only processed on exit 0. For most events, stdout is only shown in verbose mode (Ctrl+O). The exceptions are UserPromptSubmit and SessionStart, where stdout is added as context that Claude can see and act on.
Exit 2 means a blocking error. Claude Code ignores stdout and any JSON in it. Instead, stderr text is fed back to Claude as an error message. The effect depends on the event: PreToolUse blocks the tool call, UserPromptSubmit rejects the prompt, and so on. See  [#exit-code-2-behavior-per-event] exit code 2 behavior for the full list.
Any other exit code is a non-blocking error. stderr is shown in verbose mode (Ctrl+O) and execution continues.
For example, a hook command script that blocks dangerous Bash commands:











#!/bin/bash
# Reads JSON input from stdin, checks the command
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Blocking error: tool call is prevented
fi

exit 0  # Success: tool call proceeds








 [#exit-code-2-behavior-per-event] ​


Exit code 2 behavior per event

Exit code 2 is the way a hook signals “stop, don’t do this.” The effect depends on the event, because some events represent actions that can be blocked (like a tool call that hasn’t happened yet) and others represent things that already happened or can’t be prevented.



Hook eventCan block?What happens on exit 2
PreToolUseYesBlocks the tool call
PermissionRequestYesDenies the permission
UserPromptSubmitYesBlocks prompt processing and erases the prompt
StopYesPrevents Claude from stopping, continues the conversation
SubagentStopYesPrevents the subagent from stopping
TeammateIdleYesPrevents the teammate from going idle (teammate continues working)
TaskCreatedYesRolls back the task creation
TaskCompletedYesPrevents the task from being marked as completed
ConfigChangeYesBlocks the configuration change from taking effect (except policy_settings)
StopFailureNoOutput and exit code are ignored
PostToolUseNoShows stderr to Claude (tool already ran)
PostToolUseFailureNoShows stderr to Claude (tool already failed)
NotificationNoShows stderr to user only
SubagentStartNoShows stderr to user only
SessionStartNoShows stderr to user only
SessionEndNoShows stderr to user only
CwdChangedNoShows stderr to user only
FileChangedNoShows stderr to user only
PreCompactNoShows stderr to user only
PostCompactNoShows stderr to user only
ElicitationYesDenies the elicitation
ElicitationResultYesBlocks the response (action becomes decline)
WorktreeCreateYesAny non-zero exit code causes worktree creation to fail
WorktreeRemoveNoFailures are logged in debug mode only
InstructionsLoadedNoExit code is ignored





 [#http-response-handling] ​


HTTP response handling

HTTP hooks use HTTP status codes and response bodies instead of exit codes and stdout:


2xx with an empty body: success, equivalent to exit code 0 with no output

2xx with a plain text body: success, the text is added as context

2xx with a JSON body: success, parsed using the same  [#json-output] JSON output schema as command hooks

Non-2xx status: non-blocking error, execution continues

Connection failure or timeout: non-blocking error, execution continues

Unlike command hooks, HTTP hooks cannot signal a blocking error through status codes alone. To block a tool call or deny a permission, return a 2xx response with a JSON body containing the appropriate decision fields.


 [#json-output] ​


JSON output

Exit codes let you allow or block, but JSON output gives you finer-grained control. Instead of exiting with code 2 to block, exit 0 and print a JSON object to stdout. Claude Code reads specific fields from that JSON to control behavior, including  [#decision-control] decision control for blocking, allowing, or escalating to the user.




You must choose one approach per hook, not both: either use exit codes alone for signaling, or exit 0 and print JSON for structured control. Claude Code only processes JSON on exit 0. If you exit 2, any JSON is ignored.


Your hook’s stdout must contain only the JSON object. If your shell profile prints text on startup, it can interfere with JSON parsing. See  [/docs/en/hooks-guide#json-validation-failed] JSON validation failed in the troubleshooting guide.
The JSON object supports three kinds of fields:


Universal fields like continue work across all events. These are listed in the table below.

Top-level decision and reason are used by some events to block or provide feedback.

hookSpecificOutput is a nested object for events that need richer control. It requires a hookEventName field set to the event name.




FieldDefaultDescription
continuetrueIf false, Claude stops processing entirely after the hook runs. Takes precedence over any event-specific decision fields
stopReasonnoneMessage shown to the user when continue is false. Not shown to Claude
suppressOutputfalseIf true, hides stdout from verbose mode output
systemMessagenoneWarning message shown to the user



To stop Claude entirely regardless of event type:











{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }








 [#decision-control] ​


Decision control

Not every event supports blocking or controlling behavior through JSON. The events that do each use a different set of fields to express that decision. Use this table as a quick reference before writing a hook:



EventsDecision patternKey fields
UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SubagentStop, ConfigChangeTop-level decisiondecision: "block", reason
TeammateIdle, TaskCreated, TaskCompletedExit code or continue: falseExit code 2 blocks the action with stderr feedback. JSON {"continue": false, "stopReason": "..."} also stops the teammate entirely, matching Stop hook behavior
PreToolUsehookSpecificOutputpermissionDecision (allow/deny/ask), permissionDecisionReason
PermissionRequesthookSpecificOutputdecision.behavior (allow/deny)
WorktreeCreatepath returnCommand hook prints path on stdout; HTTP hook returns hookSpecificOutput.worktreePath. Hook failure or missing path fails creation
ElicitationhookSpecificOutputaction (accept/decline/cancel), content (form field values for accept)
ElicitationResulthookSpecificOutputaction (accept/decline/cancel), content (form field values override)
WorktreeRemove, Notification, SessionEnd, PreCompact, PostCompact, InstructionsLoaded, StopFailure, CwdChanged, FileChangedNoneNo decision control. Used for side effects like logging or cleanup



Here are examples of each pattern in action:



 Top-level decision


 PreToolUse


 PermissionRequest


Used by UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SubagentStop, and ConfigChange. The only value is "block". To allow the action to proceed, omit decision from your JSON, or exit 0 without any JSON at all:










{
  "decision": "block",
  "reason": "Test suite must pass before proceeding"
}







Uses hookSpecificOutput for richer control: allow, deny, or escalate to the user. You can also modify tool input before it runs or inject additional context for Claude. See  [#pretooluse-decision-control] PreToolUse decision control for the full set of options.










{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Database writes are not allowed"
  }
}







Uses hookSpecificOutput to allow or deny a permission request on behalf of the user. When allowing, you can also modify the tool’s input or apply permission rules so the user isn’t prompted again. See  [#permissionrequest-decision-control] PermissionRequest decision control for the full set of options.










{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}









For extended examples including Bash command validation, prompt filtering, and auto-approval scripts, see  [/docs/en/hooks-guide#what-you-can-automate] What you can automate in the guide and the  [https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py] Bash command validator reference implementation.


 [#hook-events] ​


Hook events

Each event corresponds to a point in Claude Code’s lifecycle where hooks can run. The sections below are ordered to match the lifecycle: from session setup through the agentic loop to session end. Each section describes when the event fires, what matchers it supports, the JSON input it receives, and how to control behavior through output.


 [#sessionstart] ​


SessionStart

Runs when Claude Code starts a new session or resumes an existing session. Useful for loading development context like existing issues or recent changes to your codebase, or setting up environment variables. For static context that does not require a script, use  [/docs/en/memory] CLAUDE.md instead.
SessionStart runs on every session, so keep these hooks fast. Only type: "command" hooks are supported.
The matcher value corresponds to how the session was initiated:



MatcherWhen it fires
startupNew session
resume--resume, --continue, or /resume
clear/clear
compactAuto or manual compaction





 [#sessionstart-input] ​


SessionStart input

In addition to the  [#common-input-fields] common input fields, SessionStart hooks receive source, model, and optionally agent_type. The source field indicates how the session started: "startup" for new sessions, "resume" for resumed sessions, "clear" after /clear, or "compact" after compaction. The model field contains the model identifier. If you start Claude Code with claude --agent <name>, an agent_type field contains the agent name.











{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}








 [#sessionstart-decision-control] ​


SessionStart decision control

Any text your hook script prints to stdout is added as context for Claude. In addition to the  [#json-output] JSON output fields available to all hooks, you can return these event-specific fields:



FieldDescription
additionalContextString added to Claude’s context. Multiple hooks’ values are concatenated














{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}








 [#persist-environment-variables] ​


Persist environment variables

SessionStart hooks have access to the CLAUDE_ENV_FILE environment variable, which provides a file path where you can persist environment variables for subsequent Bash commands.
To set individual environment variables, write export statements to CLAUDE_ENV_FILE. Use append (>>) to preserve variables set by other hooks:











#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0






To capture all environment changes from setup commands, compare the exported variables before and after:











#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# Run your setup commands that modify the environment
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0






Any variables written to this file will be available in all subsequent Bash commands that Claude Code executes during the session.




CLAUDE_ENV_FILE is available for SessionStart,  [#cwdchanged] CwdChanged, and  [#filechanged] FileChanged hooks. Other hook types do not have access to this variable.




 [#instructionsloaded] ​


InstructionsLoaded

Fires when a CLAUDE.md or .claude/rules/*.md file is loaded into context. This event fires at session start for eagerly-loaded files and again later when files are lazily loaded, for example when Claude accesses a subdirectory that contains a nested CLAUDE.md or when conditional rules with paths: frontmatter match. The hook does not support blocking or decision control. It runs asynchronously for observability purposes.
The matcher runs against load_reason. For example, use "matcher": "session_start" to fire only for files loaded at session start, or "matcher": "path_glob_match|nested_traversal" to fire only for lazy loads.


 [#instructionsloaded-input] ​


InstructionsLoaded input

In addition to the  [#common-input-fields] common input fields, InstructionsLoaded hooks receive these fields:



FieldDescription
file_pathAbsolute path to the instruction file that was loaded
memory_typeScope of the file: "User", "Project", "Local", or "Managed"
load_reasonWhy the file was loaded: "session_start", "nested_traversal", "path_glob_match", "include", or "compact". The "compact" value fires when instruction files are re-loaded after a compaction event
globsPath glob patterns from the file’s paths: frontmatter, if any. Present only for path_glob_match loads
trigger_file_pathPath to the file whose access triggered this load, for lazy loads
parent_file_pathPath to the parent instruction file that included this one, for include loads














{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}








 [#instructionsloaded-decision-control] ​


InstructionsLoaded decision control

InstructionsLoaded hooks have no decision control. They cannot block or modify instruction loading. Use this event for audit logging, compliance tracking, or observability.


 [#userpromptsubmit] ​


UserPromptSubmit

Runs when the user submits a prompt, before Claude processes it. This allows you
to add additional context based on the prompt/conversation, validate prompts, or
block certain types of prompts.


 [#userpromptsubmit-input] ​


UserPromptSubmit input

In addition to the  [#common-input-fields] common input fields, UserPromptSubmit hooks receive the prompt field containing the text the user submitted.











{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}








 [#userpromptsubmit-decision-control] ​


UserPromptSubmit decision control

UserPromptSubmit hooks can control whether a user prompt is processed and add context. All  [#json-output] JSON output fields are available.
There are two ways to add context to the conversation on exit code 0:


Plain text stdout: any non-JSON text written to stdout is added as context

JSON with additionalContext: use the JSON format below for more control. The additionalContext field is added as context

Plain stdout is shown as hook output in the transcript. The additionalContext field is added more discretely.
To block a prompt, return a JSON object with decision set to "block":



FieldDescription
decision"block" prevents the prompt from being processed and erases it from context. Omit to allow the prompt to proceed
reasonShown to the user when decision is "block". Not added to context
additionalContextString added to Claude’s context














{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}










The JSON format isn’t required for simple use cases. To add context, you can print plain text to stdout with exit code 0. Use JSON when you need to
block prompts or want more structured control.




 [#pretooluse] ​


PreToolUse

Runs after Claude creates tool parameters and before processing the tool call. Matches on tool name: Bash, Edit, Write, Read, Glob, Grep, Agent, WebFetch, WebSearch, AskUserQuestion, ExitPlanMode, and any  [#match-mcp-tools] MCP tool names.
Use  [#pretooluse-decision-control] PreToolUse decision control to allow, deny, or ask for permission to use the tool.


 [#pretooluse-input] ​


PreToolUse input

In addition to the  [#common-input-fields] common input fields, PreToolUse hooks receive tool_name, tool_input, and tool_use_id. The tool_input fields depend on the tool:

Bash

Executes shell commands.



FieldTypeExampleDescription
commandstring"npm test"The shell command to execute
descriptionstring"Run test suite"Optional description of what the command does
timeoutnumber120000Optional timeout in milliseconds
run_in_backgroundbooleanfalseWhether to run the command in background




Write

Creates or overwrites a file.



FieldTypeExampleDescription
file_pathstring"/path/to/file.txt"Absolute path to the file to write
contentstring"file content"Content to write to the file




Edit

Replaces a string in an existing file.



FieldTypeExampleDescription
file_pathstring"/path/to/file.txt"Absolute path to the file to edit
old_stringstring"original text"Text to find and replace
new_stringstring"replacement text"Replacement text
replace_allbooleanfalseWhether to replace all occurrences




Read

Reads file contents.



FieldTypeExampleDescription
file_pathstring"/path/to/file.txt"Absolute path to the file to read
offsetnumber10Optional line number to start reading from
limitnumber50Optional number of lines to read




Glob

Finds files matching a glob pattern.



FieldTypeExampleDescription
patternstring"**/*.ts"Glob pattern to match files against
pathstring"/path/to/dir"Optional directory to search in. Defaults to current working directory




Grep

Searches file contents with regular expressions.



FieldTypeExampleDescription
patternstring"TODO.*fix"Regular expression pattern to search for
pathstring"/path/to/dir"Optional file or directory to search in
globstring"*.ts"Optional glob pattern to filter files
output_modestring"content""content", "files_with_matches", or "count". Defaults to "files_with_matches"
-ibooleantrueCase insensitive search
multilinebooleanfalseEnable multiline matching




WebFetch

Fetches and processes web content.



FieldTypeExampleDescription
urlstring"https://example.com/api"URL to fetch content from
promptstring"Extract the API endpoints"Prompt to run on the fetched content




WebSearch

Searches the web.



FieldTypeExampleDescription
querystring"react hooks best practices"Search query
allowed_domainsarray["docs.example.com"]Optional: only include results from these domains
blocked_domainsarray["spam.example.com"]Optional: exclude results from these domains




Agent

Spawns a  [/docs/en/sub-agents] subagent.



FieldTypeExampleDescription
promptstring"Find all API endpoints"The task for the agent to perform
descriptionstring"Find API endpoints"Short description of the task
subagent_typestring"Explore"Type of specialized agent to use
modelstring"sonnet"Optional model alias to override the default




AskUserQuestion

Asks the user one to four multiple-choice questions.



FieldTypeExampleDescription
questionsarray[{"question": "Which framework?", "header": "Framework", "options": [{"label": "React"}], "multiSelect": false}]Questions to present, each with a question string, short header, options array, and optional multiSelect flag
answersobject{"Which framework?": "React"}Optional. Maps question text to the selected option label. Multi-select answers join labels with commas. Claude does not set this field; supply it via updatedInput to answer programmatically





 [#pretooluse-decision-control] ​


PreToolUse decision control

PreToolUse hooks can control whether a tool call proceeds. Unlike other hooks that use a top-level decision field, PreToolUse returns its decision inside a hookSpecificOutput object. This gives it richer control: three outcomes (allow, deny, or ask) plus the ability to modify tool input before execution.



FieldDescription
permissionDecision"allow" skips the permission prompt. "deny" prevents the tool call. "ask" prompts the user to confirm.  [/docs/en/permissions#manage-permissions] Deny and ask rules still apply when a hook returns "allow"
permissionDecisionReasonFor "allow" and "ask", shown to the user but not Claude. For "deny", shown to Claude
updatedInputModifies the tool’s input parameters before ex

[... truncated at 50KB ...]
```

### headless

URL: https://code.claude.com/docs/en/headless
Hash: 8ce00486084c

```
Run Claude Code programmatically - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Automation

Run Claude Code programmatically




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Agents


 [/docs/en/sub-agents] 

Create custom subagents


 [/docs/en/agent-teams] 

Run agent teams





Tools and plugins


 [/docs/en/mcp] 

Model Context Protocol (MCP)


 [/docs/en/discover-plugins] 

Discover and install prebuilt plugins


 [/docs/en/plugins] 

Create plugins


 [/docs/en/skills] 

Extend Claude with skills





Automation


 [/docs/en/hooks-guide] 

Automate with hooks


 [/docs/en/channels] 

Push external events to Claude


 [/docs/en/scheduled-tasks] 

Run prompts on a schedule


 [/docs/en/headless] 

Programmatic usage





Troubleshooting


 [/docs/en/troubleshooting] 

Troubleshooting











On this page

 [#basic-usage] Basic usage
 [#start-faster-with-bare-mode] Start faster with bare mode
 [#examples] Examples
 [#get-structured-output] Get structured output
 [#stream-responses] Stream responses
 [#auto-approve-tools] Auto-approve tools
 [#create-a-commit] Create a commit
 [#customize-the-system-prompt] Customize the system prompt
 [#continue-conversations] Continue conversations
 [#next-steps] Next steps

























The  [https://platform.claude.com/docs/en/agent-sdk/overview] Agent SDK gives you the same tools, agent loop, and context management that power Claude Code. It’s available as a CLI for scripts and CI/CD, or as  [https://platform.claude.com/docs/en/agent-sdk/python] Python and  [https://platform.claude.com/docs/en/agent-sdk/typescript] TypeScript packages for full programmatic control.




The CLI was previously called “headless mode.” The -p flag and all CLI options work the same way.


To run Claude Code programmatically from the CLI, pass -p with your prompt and any  [/docs/en/cli-reference] CLI options:











claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"






This page covers using the Agent SDK via the CLI (claude -p). For the Python and TypeScript SDK packages with structured outputs, tool approval callbacks, and native message objects, see the  [https://platform.claude.com/docs/en/agent-sdk/overview] full Agent SDK documentation.


 [#basic-usage] ​


Basic usage

Add the -p (or --print) flag to any claude command to run it non-interactively. All  [/docs/en/cli-reference] CLI options work with -p, including:


--continue for  [#continue-conversations] continuing conversations

--allowedTools for  [#auto-approve-tools] auto-approving tools

--output-format for  [#get-structured-output] structured output

This example asks Claude a question about your codebase and prints the response:











claude -p "What does the auth module do?"








 [#start-faster-with-bare-mode] ​


Start faster with bare mode

Add --bare to reduce startup time by skipping auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md. Without it, claude -p loads the same  [/docs/en/how-claude-code-works#the-context-window] context an interactive session would, including anything configured in the working directory or ~/.claude.
Bare mode is useful for CI and scripts where you need the same result on every machine. A hook in a teammate’s ~/.claude or an MCP server in the project’s .mcp.json won’t run, because bare mode never reads them. Only flags you pass explicitly take effect.
This example runs a one-off summarize task in bare mode and pre-approves the Read tool so the call completes without a permission prompt:











claude --bare -p "Summarize this file" --allowedTools "Read"






In bare mode Claude has access to the Bash, file read, and file edit tools. Pass any context you need with a flag:



To loadUse
System prompt additions--append-system-prompt, --append-system-prompt-file
Settings--settings <file-or-json>
MCP servers--mcp-config <file-or-json>
Custom agents--agents <json>
A plugin directory--plugin-dir <path>



Bare mode skips OAuth and keychain reads. Anthropic authentication must come from ANTHROPIC_API_KEY or an apiKeyHelper in the JSON passed to --settings. Bedrock, Vertex, and Foundry use their usual provider credentials.




--bare is the recommended mode for scripted and SDK calls, and will become the default for -p in a future release.




 [#examples] ​


Examples

These examples highlight common CLI patterns. For CI and other scripted calls, add  [#start-faster-with-bare-mode] --bare so they don’t pick up whatever happens to be configured locally.


 [#get-structured-output] ​


Get structured output

Use --output-format to control how responses are returned:


text (default): plain text output

json: structured JSON with result, session ID, and metadata

stream-json: newline-delimited JSON for real-time streaming

This example returns a project summary as JSON with session metadata, with the text result in the result field:











claude -p "Summarize this project" --output-format json






To get output conforming to a specific schema, use --output-format json with --json-schema and a  [https://json-schema.org/] JSON Schema definition. The response includes metadata about the request (session ID, usage, etc.) with the structured output in the structured_output field.
This example extracts function names and returns them as an array of strings:











claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'










Use a tool like  [https://jqlang.github.io/jq/] jq to parse the response and extract specific fields:










# Extract the text result
claude -p "Summarize this project" --output-format json | jq -r '.result'

# Extract structured output
claude -p "Extract function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
  | jq '.structured_output'










 [#stream-responses] ​


Stream responses

Use --output-format stream-json with --verbose and --include-partial-messages to receive tokens as they’re generated. Each line is a JSON object representing an event:











claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages






The following example uses  [https://jqlang.github.io/jq/] jq to filter for text deltas and display just the streaming text. The -r flag outputs raw strings (no quotes) and -j joins without newlines so tokens stream continuously:











claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'






When an API request fails with a retryable error, Claude Code emits a system/api_retry event before retrying. You can use this to surface retry progress or implement custom backoff logic.



FieldTypeDescription
type"system"message type
subtype"api_retry"identifies this as a retry event
attemptintegercurrent attempt number, starting at 1
max_retriesintegertotal retries permitted
retry_delay_msintegermilliseconds until the next attempt
error_statusinteger or nullHTTP status code, or null for connection errors with no HTTP response
errorstringerror category: authentication_failed, billing_error, rate_limit, invalid_request, server_error, max_output_tokens, or unknown
uuidstringunique event identifier
session_idstringsession the event belongs to



For programmatic streaming with callbacks and message objects, see  [https://platform.claude.com/docs/en/agent-sdk/streaming-output] Stream responses in real-time in the Agent SDK documentation.


 [#auto-approve-tools] ​


Auto-approve tools

Use --allowedTools to let Claude use certain tools without prompting. This example runs a test suite and fixes failures, allowing Claude to execute Bash commands and read/edit files without asking for permission:











claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"








 [#create-a-commit] ​


Create a commit

This example reviews staged changes and creates a commit with an appropriate message:











claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"






The --allowedTools flag uses  [/docs/en/settings#permission-rule-syntax] permission rule syntax. The trailing  * enables prefix matching, so Bash(git diff *) allows any command starting with git diff. The space before * is important: without it, Bash(git diff*) would also match git diff-index.




User-invoked  [/docs/en/skills] skills like /commit and  [/docs/en/commands] built-in commands are only available in interactive mode. In -p mode, describe the task you want to accomplish instead.




 [#customize-the-system-prompt] ​


Customize the system prompt

Use --append-system-prompt to add instructions while keeping Claude Code’s default behavior. This example pipes a PR diff to Claude and instructs it to review for security vulnerabilities:











gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json






See  [/docs/en/cli-reference#system-prompt-flags] system prompt flags for more options including --system-prompt to fully replace the default prompt.


 [#continue-conversations] ​


Continue conversations

Use --continue to continue the most recent conversation, or --resume with a session ID to continue a specific conversation. This example runs a review, then sends follow-up prompts:











# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue






If you’re running multiple conversations, capture the session ID to resume a specific one:











session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"








 [#next-steps] ​


Next steps



 [https://platform.claude.com/docs/en/agent-sdk/quickstart] Agent SDK quickstart: build your first agent with Python or TypeScript

 [/docs/en/cli-reference] CLI reference: all CLI flags and options

 [/docs/en/github-actions] GitHub Actions: use the Agent SDK in GitHub workflows

 [/docs/en/gitlab-ci-cd] GitLab CI/CD: use the Agent SDK in GitLab pipelines




Was this page helpful?


YesNo






 [/docs/en/scheduled-tasks] Run prompts on a schedule [/docs/en/troubleshooting] Troubleshooting





⌘I











 [/docs/en/overview] 
 [https://x.com/AnthropicAI]  [https://www.linkedin.com/company/anthropicresearch] 






 [https://www.anthropic.com/company]  [https://www.anthropic.com/careers]  [https://www.anthropic.com/economic-futures]  [https://www.anthropic.com/research]  [https://www.anthropic.com/news]  [https://trust.anthropic.com/]  [https://www.anthropic.com/transparency] 





 [https://www.anthropic.com/supported-countries]  [https://status.anthropic.com/]  [https://support.claude.com/] 





 [https://www.anthropic.com/learn]  [https://claude.com/partners/mcp]  [https://www.claude.com/customers]  [https://www.anthropic.com/engineering]  [https://www.anthropic.com/events]  [https://claude.com/partners/powered-by-claude]  [https://claude.com/partners/services]  [https://claude.com/programs/startups] 





 [#]  [https://www.anthropic.com/legal/privacy]  [https://www.anthropic.com/responsible-disclosure-policy]  [https://www.anthropic.com/legal/aup]  [https://www.anthropic.com/legal/commercial-terms]  [https://www.anthropic.com/legal/consumer-terms] 












Assistant









Responses are generated using AI and may contain mistakes.
```

### permissions

URL: https://code.claude.com/docs/en/permissions
Hash: fca8c3b5fc31

```
Configure permissions - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Configuration

Configure permissions




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Configuration


 [/docs/en/settings] 

Settings


 [/docs/en/permissions] 

Permissions


 [/docs/en/sandboxing] 

Sandboxing


 [/docs/en/terminal-config] 

Terminal configuration


 [/docs/en/fullscreen] 

Fullscreen rendering


 [/docs/en/model-config] 

Model configuration


 [/docs/en/fast-mode] 

Speed up responses with fast mode


 [/docs/en/voice-dictation] 

Voice dictation


 [/docs/en/output-styles] 

Output styles


 [/docs/en/statusline] 

Customize status line


 [/docs/en/keybindings] 

Customize keyboard shortcuts











On this page

 [#permission-system] Permission system
 [#manage-permissions] Manage permissions
 [#permission-modes] Permission modes
 [#permission-rule-syntax] Permission rule syntax
 [#match-all-uses-of-a-tool] Match all uses of a tool
 [#use-specifiers-for-fine-grained-control] Use specifiers for fine-grained control
 [#wildcard-patterns] Wildcard patterns
 [#tool-specific-permission-rules] Tool-specific permission rules
 [#bash] Bash
 [#read-and-edit] Read and Edit
 [#webfetch] WebFetch
 [#mcp] MCP
 [#agent-subagents] Agent (subagents)
 [#extend-permissions-with-hooks] Extend permissions with hooks
 [#working-directories] Working directories
 [#how-permissions-interact-with-sandboxing] How permissions interact with sandboxing
 [#managed-settings] Managed settings
 [#managed-only-settings] Managed-only settings
 [#configure-the-auto-mode-classifier] Configure the auto mode classifier
 [#define-trusted-infrastructure] Define trusted infrastructure
 [#override-the-block-and-allow-rules] Override the block and allow rules
 [#inspect-the-defaults-and-your-effective-config] Inspect the defaults and your effective config
 [#settings-precedence] Settings precedence
 [#example-configurations] Example configurations
 [#see-also] See also

























Claude Code supports fine-grained permissions so that you can specify exactly what the agent is allowed to do and what it cannot. Permission settings can be checked into version control and distributed to all developers in your organization, as well as customized by individual developers.


 [#permission-system] ​


Permission system

Claude Code uses a tiered permission system to balance power and safety:



Tool typeExampleApproval required”Yes, don’t ask again” behavior
Read-onlyFile reads, GrepNoN/A
Bash commandsShell executionYesPermanently per project directory and command
File modificationEdit/write filesYesUntil session end





 [#manage-permissions] ​


Manage permissions

You can view and manage Claude Code’s tool permissions with /permissions. This UI lists all permission rules and the settings.json file they are sourced from.


Allow rules let Claude Code use the specified tool without manual approval.

Ask rules prompt for confirmation whenever Claude Code tries to use the specified tool.

Deny rules prevent Claude Code from using the specified tool.

Rules are evaluated in order: deny -> ask -> allow. The first matching rule wins, so deny rules always take precedence.


 [#permission-modes] ​


Permission modes

Claude Code supports several permission modes that control how tools are approved. See  [/docs/en/permission-modes] Permission modes for when to use each one. Set the defaultMode in your  [/docs/en/settings#settings-files] settings files:



ModeDescription
defaultStandard behavior: prompts for permission on first use of each tool
acceptEditsAutomatically accepts file edit permissions for the session
planPlan Mode: Claude can analyze but not modify files or execute commands
autoAuto-approves tool calls with background safety checks that verify actions align with your request. Currently a research preview
dontAskAuto-denies tools unless pre-approved via /permissions or permissions.allow rules
bypassPermissionsSkips permission prompts except for writes to protected directories (see warning below)







bypassPermissions mode skips permission prompts. Writes to .git, .claude, .vscode, and .idea directories still prompt for confirmation to prevent accidental corruption of repository state and local configuration. Writes to .claude/commands, .claude/agents, and .claude/skills are exempt and do not prompt, because Claude routinely writes there when creating skills, subagents, and commands. Only use this mode in isolated environments like containers or VMs where Claude Code cannot cause damage. Administrators can prevent this mode by setting disableBypassPermissionsMode to "disable" in  [#managed-settings] managed settings.


To prevent bypassPermissions or auto mode from being used, set permissions.disableBypassPermissionsMode or disableAutoMode to "disable" in any  [/docs/en/settings#settings-files] settings file. These are most useful in  [#managed-settings] managed settings where they cannot be overridden.


 [#permission-rule-syntax] ​


Permission rule syntax

Permission rules follow the format Tool or Tool(specifier).


 [#match-all-uses-of-a-tool] ​


Match all uses of a tool

To match all uses of a tool, use just the tool name without parentheses:



RuleEffect
BashMatches all Bash commands
WebFetchMatches all web fetch requests
ReadMatches all file reads



Bash(*) is equivalent to Bash and matches all Bash commands.


 [#use-specifiers-for-fine-grained-control] ​


Use specifiers for fine-grained control

Add a specifier in parentheses to match specific tool uses:



RuleEffect
Bash(npm run build)Matches the exact command npm run build
Read(./.env)Matches reading the .env file in the current directory
WebFetch(domain:example.com)Matches fetch requests to example.com





 [#wildcard-patterns] ​


Wildcard patterns

Bash rules support glob patterns with *. Wildcards can appear at any position in the command. This configuration allows npm and git commit commands while blocking git push:











{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}






The space before * matters: Bash(ls *) matches ls -la but not lsof, while Bash(ls*) matches both. The legacy :* suffix syntax is equivalent to  * but is deprecated.


 [#tool-specific-permission-rules] ​


Tool-specific permission rules



 [#bash] ​


Bash

Bash permission rules support wildcard matching with *. Wildcards can appear at any position in the command, including at the beginning, middle, or end:


Bash(npm run build) matches the exact Bash command npm run build

Bash(npm run test *) matches Bash commands starting with npm run test

Bash(npm *) matches any command starting with npm 

Bash(* install) matches any command ending with  install

Bash(git * main) matches commands like git checkout main, git merge main

When * appears at the end with a space before it (like Bash(ls *)), it enforces a word boundary, requiring the prefix to be followed by a space or end-of-string. For example, Bash(ls *) matches ls -la but not lsof. In contrast, Bash(ls*) without a space matches both ls -la and lsof because there’s no word boundary constraint.




Claude Code is aware of shell operators (like &&) so a prefix match rule like Bash(safe-cmd *) won’t give it permission to run the command safe-cmd && other-cmd.


When you approve a compound command with “Yes, don’t ask again”, Claude Code saves a separate rule for each subcommand that requires approval, rather than a single rule for the full compound string. For example, approving git status && npm test saves a rule for npm test, so future npm test invocations are recognized regardless of what precedes the &&. Subcommands like cd into a subdirectory generate their own Read rule for that path. Up to 5 rules may be saved for a single compound command.




Bash permission patterns that try to constrain command arguments are fragile. For example, Bash(curl http://github.com/ *) intends to restrict curl to GitHub URLs, but won’t match variations like:

Options before URL: curl -X GET http://github.com/...

Different protocol: curl https://github.com/...

Redirects: curl -L http://bit.ly/xyz (redirects to github)

Variables: URL=http://github.com && curl $URL

Extra spaces: curl  http://github.com
For more reliable URL filtering, consider:

Restrict Bash network tools: use deny rules to block curl, wget, and similar commands, then use the WebFetch tool with WebFetch(domain:github.com) permission for allowed domains

Use PreToolUse hooks: implement a hook that validates URLs in Bash commands and blocks disallowed domains

Instructing Claude Code about your allowed curl patterns via CLAUDE.md
Note that using WebFetch alone does not prevent network access. If Bash is allowed, Claude can still use curl, wget, or other tools to reach any URL.




 [#read-and-edit] ​


Read and Edit

Edit rules apply to all built-in tools that edit files. Claude makes a best-effort attempt to apply Read rules to all built-in tools that read files like Grep and Glob.




Read and Edit deny rules apply to Claude’s built-in file tools, not to Bash subprocesses. A Read(./.env) deny rule blocks the Read tool but does not prevent cat .env in Bash. For OS-level enforcement that blocks all processes from accessing a path,  [/docs/en/sandboxing] enable the sandbox.


Read and Edit rules both follow the  [https://git-scm.com/docs/gitignore] gitignore specification with four distinct pattern types:



PatternMeaningExampleMatches
//pathAbsolute path from filesystem rootRead(//Users/alice/secrets/**)/Users/alice/secrets/**
~/pathPath from home directoryRead(~/Documents/*.pdf)/Users/alice/Documents/*.pdf
/pathPath relative to project rootEdit(/src/**/*.ts)<project root>/src/**/*.ts
path or ./pathPath relative to current directoryRead(*.env)<cwd>/*.env







A pattern like /Users/alice/file is NOT an absolute path. It’s relative to the project root. Use //Users/alice/file for absolute paths.


On Windows, paths are normalized to POSIX form before matching. C:\Users\alice becomes /c/Users/alice, so use //c/**/.env to match .env files anywhere on that drive. To match across all drives, use //**/.env.
Examples:


Edit(/docs/**): edits in <project>/docs/ (NOT /docs/ and NOT <project>/.claude/docs/)

Read(~/.zshrc): reads your home directory’s .zshrc

Edit(//tmp/scratch.txt): edits the absolute path /tmp/scratch.txt

Read(src/**): reads from <current-directory>/src/





In gitignore patterns, * matches files in a single directory while ** matches recursively across directories. To allow all file access, use just the tool name without parentheses: Read, Edit, or Write.




 [#webfetch] ​


WebFetch



WebFetch(domain:example.com) matches fetch requests to example.com



 [#mcp] ​


MCP



mcp__puppeteer matches any tool provided by the puppeteer server (name configured in Claude Code)

mcp__puppeteer__* wildcard syntax that also matches all tools from the puppeteer server

mcp__puppeteer__puppeteer_navigate matches the puppeteer_navigate tool provided by the puppeteer server



 [#agent-subagents] ​


Agent (subagents)

Use Agent(AgentName) rules to control which  [/docs/en/sub-agents] subagents Claude can use:


Agent(Explore) matches the Explore subagent

Agent(Plan) matches the Plan subagent

Agent(my-custom-agent) matches a custom subagent named my-custom-agent

Add these rules to the deny array in your settings or use the --disallowedTools CLI flag to disable specific agents. To disable the Explore agent:











{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}








 [#extend-permissions-with-hooks] ​


Extend permissions with hooks

 [/docs/en/hooks-guide] Claude Code hooks provide a way to register custom shell commands to perform permission evaluation at runtime. When Claude Code makes a tool call, PreToolUse hooks run before the permission prompt. The hook output can deny the tool call, force a prompt, or skip the prompt to let the call proceed.
Skipping the prompt does not bypass permission rules. Deny and ask rules are still evaluated after a hook returns "allow", so a matching deny rule still blocks the call. This preserves the deny-first precedence described in  [#manage-permissions] Manage permissions, including deny rules set in managed settings.
A blocking hook also takes precedence over allow rules. A hook that exits with code 2 stops the tool call before permission rules are evaluated, so the block applies even when an allow rule would otherwise let the call proceed. To run all Bash commands without prompts except for a few you want blocked, add "Bash" to your allow list and register a PreToolUse hook that rejects those specific commands. See  [/docs/en/hooks-guide#block-edits-to-protected-files] Block edits to protected files for a hook script you can adapt.


 [#working-directories] ​


Working directories

By default, Claude has access to files in the directory where it was launched. You can extend this access:


During startup: use --add-dir <path> CLI argument

During session: use /add-dir command

Persistent configuration: add to additionalDirectories in  [/docs/en/settings#settings-files] settings files

Files in additional directories follow the same permission rules as the original working directory: they become readable without prompts, and file editing permissions follow the current permission mode.


 [#how-permissions-interact-with-sandboxing] ​


How permissions interact with sandboxing

Permissions and  [/docs/en/sandboxing] sandboxing are complementary security layers:


Permissions control which tools Claude Code can use and which files or domains it can access. They apply to all tools (Bash, Read, Edit, WebFetch, MCP, and others).

Sandboxing provides OS-level enforcement that restricts the Bash tool’s filesystem and network access. It applies only to Bash commands and their child processes.

Use both for defense-in-depth:


Permission deny rules block Claude from even attempting to access restricted resources

Sandbox restrictions prevent Bash commands from reaching resources outside defined boundaries, even if a prompt injection bypasses Claude’s decision-making

Filesystem restrictions in the sandbox use Read and Edit deny rules, not separate sandbox configuration

Network restrictions combine WebFetch permission rules with the sandbox’s allowedDomains list



 [#managed-settings] ​


Managed settings

For organizations that need centralized control over Claude Code configuration, administrators can deploy managed settings that cannot be overridden by user or project settings. These policy settings follow the same format as regular settings files and can be delivered through MDM/OS-level policies, managed settings files, or  [/docs/en/server-managed-settings] server-managed settings. See  [/docs/en/settings#settings-files] settings files for delivery mechanisms and file locations.


 [#managed-only-settings] ​


Managed-only settings

Some settings are only effective in managed settings:



SettingDescription
allowManagedPermissionRulesOnlyWhen true, prevents user and project settings from defining allow, ask, or deny permission rules. Only rules in managed settings apply
allowManagedHooksOnlyWhen true, prevents loading of user, project, and plugin hooks. Only managed hooks and SDK hooks are allowed
allowManagedMcpServersOnlyWhen true, only allowedMcpServers from managed settings are respected. deniedMcpServers still merges from all sources. See  [/docs/en/mcp#managed-mcp-configuration] Managed MCP configuration
allowedChannelPluginsAllowlist of channel plugins that may push messages. Replaces the default Anthropic allowlist when set. Requires channelsEnabled: true. See  [/docs/en/channels#restrict-which-channel-plugins-can-run] Restrict which channel plugins can run
blockedMarketplacesBlocklist of marketplace sources. Blocked sources are checked before downloading, so they never touch the filesystem. See  [/docs/en/plugin-marketplaces#managed-marketplace-restrictions] managed marketplace restrictions
sandbox.network.allowManagedDomainsOnlyWhen true, only allowedDomains and WebFetch(domain:...) allow rules from managed settings are respected. Non-allowed domains are blocked automatically without prompting the user. Denied domains still merge from all sources
sandbox.filesystem.allowManagedReadPathsOnlyWhen true, only allowRead paths from managed settings are respected. allowRead entries from user, project, and local settings are ignored
strictKnownMarketplacesControls which plugin marketplaces users can add. See  [/docs/en/plugin-marketplaces#managed-marketplace-restrictions] managed marketplace restrictions







Access to  [/docs/en/remote-control] Remote Control and  [/docs/en/claude-code-on-the-web] web sessions is not controlled by a managed settings key. On Team and Enterprise plans, an admin enables or disables these features in  [https://claude.ai/admin-settings/claude-code] Claude Code admin settings.




 [#configure-the-auto-mode-classifier] ​


Configure the auto mode classifier

 [/docs/en/permission-modes#eliminate-prompts-with-auto-mode] Auto mode uses a classifier model to decide whether each action is safe to run without prompting. Out of the box it trusts only the working directory and, if present, the current repo’s remotes. Actions like pushing to your company’s source control org or writing to a team cloud bucket will be blocked as potential data exfiltration. The autoMode settings block lets you tell the classifier which infrastructure your organization trusts.
The classifier reads autoMode from user settings, .claude/settings.local.json, and managed settings. It does not read from shared project settings in .claude/settings.json, because a checked-in repo could otherwise inject its own allow rules.



ScopeFileUse for
One developer~/.claude/settings.jsonPersonal trusted infrastructure
One project, one developer.claude/settings.local.jsonPer-project trusted buckets or services, gitignored
Organization-wideManaged settingsTrusted infrastructure enforced for all developers



Entries from each scope are combined. A developer can extend environment, allow, and soft_deny with personal entries but cannot remove entries that managed settings provide. Because allow rules act as exceptions to block rules inside the classifier, a developer-added allow entry can override an organization soft_deny entry: the combination is additive, not a hard policy boundary. If you need a rule that developers cannot work around, use permissions.deny in managed settings instead, which blocks actions before the classifier is consulted.


 [#define-trusted-infrastructure] ​


Define trusted infrastructure

For most organizations, autoMode.environment is the only field you need to set. It tells the classifier which repos, buckets, and domains are trusted, without touching the built-in block and allow rules. The classifier uses environment to decide what “external” means: any destination not listed is a potential exfiltration target.











{
  "autoMode": {
    "environment": [
      "Source control: github.example.com/acme-corp and all repos under it",
      "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
      "Trusted internal domains: *.corp.example.com, api.internal.example.com",
      "Key internal services: Jenkins at ci.example.com, Artifactory at artifacts.example.com"
    ]
  }
}






Entries are prose, not regex or tool patterns. The classifier reads them as natural-language rules. Write them the way you would describe your infrastructure to a new engineer. A thorough environment section covers:


Organization: your company name and what Claude Code is primarily used for, like software development, infrastructure automation, or data engineering

Source control: every GitHub, GitLab, or Bitbucket org your developers push to

Cloud providers and trusted buckets: bucket names or prefixes that Claude should be able to read from and write to

Trusted internal domains: hostnames for APIs, dashboards, and services inside your network, like *.internal.example.com

Key internal services: CI, artifact registries, internal package indexes, incident tooling

Additional context: regulated-industry constraints, multi-tenant infrastructure, or compliance requirements that affect what the classifier should treat as risky

A useful starting template: fill in the bracketed fields and remove any lines that don’t apply:











{
  "autoMode": {
    "environment": [
      "Organization: {COMPANY_NAME}. Primary use: {PRIMARY_USE_CASE, e.g. software development, infrastructure automation}",
      "Source control: {SOURCE_CONTROL, e.g. GitHub org github.example.com/acme-corp}",
      "Cloud provider(s): {CLOUD_PROVIDERS, e.g. AWS, GCP, Azure}",
      "Trusted cloud buckets: {TRUSTED_BUCKETS, e.g. s3://acme-builds, gs://acme-datasets}",
      "Trusted internal domains: {TRUSTED_DOMAINS, e.g. *.internal.example.com, api.example.com}",
      "Key internal services: {SERVICES, e.g. Jenkins at ci.example.com, Artifactory at artifacts.example.com}",
      "Additional context: {EXTRA, e.g. regulated industry, multi-tenant infrastructure, compliance requirements}"
    ]
  }
}






The more specific context you give, the better the classifier can distinguish routine internal operations from exfiltration attempts.
You don’t need to fill everything in at once. A reasonable rollout: start with the defaults and add your source control org and key internal services, which resolves the most common false positives like pushing to your own repos. Add trusted domains and cloud buckets next. Fill the rest as blocks come up.


 [#override-the-block-and-allow-rules] ​


Override the block and allow rules

Two additional fields let you replace the classifier’s built-in rule lists: autoMode.soft_deny controls what gets blocked, and autoMode.allow controls which exceptions apply. Each is an array of prose descriptions, read as natural-language rules.
Inside the classifier, the precedence is: soft_deny rules block first, then allow rules override as exceptions, then explicit user intent overrides both. If the user’s message directly and specifically describes the exact action Claude is about to take, the classifier allows it even if a soft_deny rule matches. General requests don’t count: asking Claude to “clean up the repo” does not authorize force-pushing, but asking Claude to “force-push this branch” does.
To loosen: remove rules from soft_deny when the defaults block something your pipeline already guards against with PR review, CI, or staging environments, or add to allow when the classifier repeatedly flags a routine pattern the default exceptions don’t cover. To tighten: add to soft_deny for risks specific to your environment that the defaults miss, or remove from allow to hold a default exception to the block rules. In all cases, run claude auto-mode defaults to get the full default lists, then copy and edit: never start from an empty list.











{
  "autoMode": {
    "environment": [
      "Source control: github.example.com/acme-corp and all repos under it"
    ],
    "allow": [
      "Deploying to the staging namespace is allowed: staging is isolated from production and resets nightly",
      "Writing to s3://acme-scratch/ is allowed: ephemeral bucket with a 7-day lifecycle policy"
    ],
    "soft_deny": [
      "Never run database migrations outside the migrations CLI, even against dev databases",
      "Never modify files under infra/terraform/prod/: production infrastructure changes go through the review workflow",
      "...copy full default soft_deny list here first, then add your rules..."
    ]
  }
}










Setting allow or soft_deny replaces the entire default list for that section. If you set soft_deny with a single entry, every built-in block rule is discarded: force push, data exfiltration, curl | bash, production deploys, and all other default block rules become allowed. To customize safely, run claude auto-mode defaults to print the built-in rules, copy them into your settings file, then review each rule against your own pipeline and risk tolerance. Only remove rules for risks your infrastructure already mitigates.


The three sections are evaluated independently, so setting environment alone leaves the default allow and soft_deny lists intact.


 [#inspect-the-defaults-and-your-effective-config] ​


Inspect the defaults and your effective config

Because setting allow or soft_deny replaces the defaults, start any customization by copying the full default lists. Three CLI subcommands help you inspect and validate:











claude auto-mode defaults  # the built-in environment, allow, and soft_deny rules
claude auto-mode config    # what the classifier actually uses: your settings where set, defaults otherwise
claude auto-mode critique  # get AI feedback on your custom allow and soft_deny rules






Save the output of claude auto-mode defaults to a file, edit the lists to match your policy, and paste the result into your settings file. After saving, run claude auto-mode config to confirm the effective rules are what you expect. If you’ve written custom rules, claude auto-mode critique reviews them and flags entries that are ambiguous, redundant, or likely to cause false positives.


 [#settings-precedence] ​


Settings precedence

Permission rules follow the same  [/docs/en/settings#settings-precedence] settings precedence as all other Claude Code settings:


Managed settings: cannot be overridden by any other level, including command line arguments

Command line arguments: temporary session overrides

Local project settings (.claude/settings.local.json)

Shared project settings (.claude/settings.json)

User settings (~/.claude/settings.json)

If a tool is denied at any level, no other level can allow it. For example, a managed settings deny cannot be overridden by --allowedTools, and --disallowedTools can add restrictions beyond what managed settings define.
If a permission is allowed in user settings but denied in project settings, the project setting takes precedence and the permission is blocked.


 [#example-configurations] ​


Example configurations

This  [https://github.com/anthropics/claude-code/tree/main/examples/settings] repository includes starter settings configurations for common deployment scenarios. Use these as starting points and adjust them to fit your needs.


 [#see-also] ​


See also



 [/docs/en/settings] Settings: complete configuration reference including the permission settings table

 [/docs/en/sandboxing] Sandboxing: OS-level filesystem and network isolation for Bash commands

 [/docs/en/authentication] Authentication: set up user access to Claude Code

 [/docs/en/security] Security: security safeguards and best practices

 [/docs/en/hooks-guide] Hooks: automate workflows and extend permission evaluation




Was this page helpful?


YesNo






 [/docs/en/settings] Settings [/docs/en/sandboxing] Sandboxing





⌘I











 [/docs/en/overview] 
 [https://x.com/AnthropicAI]  [https://www.linkedin.com/company/anthropicresearch] 






 [https://www.anthropic.com/company]  [https://www.anthropic.com/careers]  [https://www.anthropic.com/economic-futures]  [https://www.anthropic.com/research]  [https://www.anthropic.com/news]  [https://trust.anthropic.com/]  [https://www.anthropic.com/transparency] 





 [https://www.anthropic.com/supported-countries]  [https://status.anthropic.com/]  [https://support.claude.com/] 





 [https://www.anthropic.com/learn]  [https://claude.com/partners/mcp]  [https://www.claude.com/customers]  [https://www.anthropic.com/engineering]  [https://www.anthropic.com/events]  [https://claude.com/partners/powered-by-claude]  [https://claude.com/partners/services]  [https://claude.com/programs/startups] 





 [#]  [https://www.anthropic.com/legal/privacy]  [https://www.anthropic.com/responsible-disclosure-policy]  [https://www.anthropic.com/legal/aup]  [https://www.anthropic.com/legal/commercial-terms]  [https://www.anthropic.com/legal/consumer-terms] 












Assistant









Responses are generated using AI and may contain mistakes.
```

### settings

URL: https://code.claude.com/docs/en/settings
Hash: c7cc3c7dfdb4

```
Claude Code settings - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Configuration

Claude Code settings




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Configuration


 [/docs/en/settings] 

Settings


 [/docs/en/permissions] 

Permissions


 [/docs/en/sandboxing] 

Sandboxing


 [/docs/en/terminal-config] 

Terminal configuration


 [/docs/en/fullscreen] 

Fullscreen rendering


 [/docs/en/model-config] 

Model configuration


 [/docs/en/fast-mode] 

Speed up responses with fast mode


 [/docs/en/voice-dictation] 

Voice dictation


 [/docs/en/output-styles] 

Output styles


 [/docs/en/statusline] 

Customize status line


 [/docs/en/keybindings] 

Customize keyboard shortcuts











On this page

 [#configuration-scopes] Configuration scopes
 [#available-scopes] Available scopes
 [#when-to-use-each-scope] When to use each scope
 [#how-scopes-interact] How scopes interact
 [#what-uses-scopes] What uses scopes
 [#settings-files] Settings files
 [#available-settings] Available settings
 [#global-config-settings] Global config settings
 [#worktree-settings] Worktree settings
 [#permission-settings] Permission settings
 [#permission-rule-syntax] Permission rule syntax
 [#sandbox-settings] Sandbox settings
 [#sandbox-path-prefixes] Sandbox path prefixes
 [#attribution-settings] Attribution settings
 [#file-suggestion-settings] File suggestion settings
 [#hook-configuration] Hook configuration
 [#settings-precedence] Settings precedence
 [#verify-active-settings] Verify active settings
 [#key-points-about-the-configuration-system] Key points about the configuration system
 [#system-prompt] System prompt
 [#excluding-sensitive-files] Excluding sensitive files
 [#subagent-configuration] Subagent configuration
 [#plugin-configuration] Plugin configuration
 [#plugin-settings] Plugin settings
 [#enabledplugins] enabledPlugins
 [#extraknownmarketplaces] extraKnownMarketplaces
 [#strictknownmarketplaces] strictKnownMarketplaces
 [#managing-plugins] Managing plugins
 [#environment-variables] Environment variables
 [#tools-available-to-claude] Tools available to Claude
 [#see-also] See also

























Claude Code offers a variety of settings to configure its behavior to meet your needs. You can configure Claude Code by running the /config command when using the interactive REPL, which opens a tabbed Settings interface where you can view status information and modify configuration options.


 [#configuration-scopes] ​


Configuration scopes

Claude Code uses a scope system to determine where configurations apply and who they’re shared with. Understanding scopes helps you decide how to configure Claude Code for personal use, team collaboration, or enterprise deployment.


 [#available-scopes] ​


Available scopes




ScopeLocationWho it affectsShared with team?
ManagedServer-managed settings, plist / registry, or system-level managed-settings.jsonAll users on the machineYes (deployed by IT)
User~/.claude/ directoryYou, across all projectsNo
Project.claude/ in repositoryAll collaborators on this repositoryYes (committed to git)
Local.claude/settings.local.jsonYou, in this repository onlyNo (gitignored)





 [#when-to-use-each-scope] ​


When to use each scope

Managed scope is for:


Security policies that must be enforced organization-wide

Compliance requirements that can’t be overridden

Standardized configurations deployed by IT/DevOps

User scope is best for:


Personal preferences you want everywhere (themes, editor settings)

Tools and plugins you use across all projects

API keys and authentication (stored securely)

Project scope is best for:


Team-shared settings (permissions, hooks, MCP servers)

Plugins the whole team should have

Standardizing tooling across collaborators

Local scope is best for:


Personal overrides for a specific project

Testing configurations before sharing with the team

Machine-specific settings that won’t work for others



 [#how-scopes-interact] ​


How scopes interact

When the same setting is configured in multiple scopes, more specific scopes take precedence:


Managed (highest) - can’t be overridden by anything

Command line arguments - temporary session overrides

Local - overrides project and user settings

Project - overrides user settings

User (lowest) - applies when nothing else specifies the setting

For example, if a permission is allowed in user settings but denied in project settings, the project setting takes precedence and the permission is blocked.


 [#what-uses-scopes] ​


What uses scopes

Scopes apply to many Claude Code features:



FeatureUser locationProject locationLocal location
Settings~/.claude/settings.json.claude/settings.json.claude/settings.local.json
Subagents~/.claude/agents/.claude/agents/None
MCP servers~/.claude.json.mcp.json~/.claude.json (per-project)
Plugins~/.claude/settings.json.claude/settings.json.claude/settings.local.json
CLAUDE.md~/.claude/CLAUDE.mdCLAUDE.md or .claude/CLAUDE.mdNone






 [#settings-files] ​


Settings files

The settings.json file is the official mechanism for configuring Claude
Code through hierarchical settings:



User settings are defined in ~/.claude/settings.json and apply to all
projects.



Project settings are saved in your project directory:


.claude/settings.json for settings that are checked into source control and shared with your team

.claude/settings.local.json for settings that are not checked in, useful for personal preferences and experimentation. Claude Code will configure git to ignore .claude/settings.local.json when it is created.




Managed settings: For organizations that need centralized control, Claude Code supports multiple delivery mechanisms for managed settings. All use the same JSON format and cannot be overridden by user or project settings:



Server-managed settings: delivered from Anthropic’s servers via the Claude.ai admin console. See  [/docs/en/server-managed-settings] server-managed settings.



MDM/OS-level policies: delivered through native device management on macOS and Windows:


macOS: com.anthropic.claudecode managed preferences domain (deployed via configuration profiles in Jamf, Kandji, or other MDM tools)

Windows: HKLM\SOFTWARE\Policies\ClaudeCode registry key with a Settings value (REG_SZ or REG_EXPAND_SZ) containing JSON (deployed via Group Policy or Intune)

Windows (user-level): HKCU\SOFTWARE\Policies\ClaudeCode (lowest policy priority, only used when no admin-level source exists)




File-based: managed-settings.json and managed-mcp.json deployed to system directories:


macOS: /Library/Application Support/ClaudeCode/

Linux and WSL: /etc/claude-code/

Windows: C:\Program Files\ClaudeCode\





The legacy Windows path C:\ProgramData\ClaudeCode\managed-settings.json is no longer supported as of v2.1.75. Administrators who deployed settings to that location must migrate files to C:\Program Files\ClaudeCode\managed-settings.json.


File-based managed settings also support a drop-in directory at managed-settings.d/ in the same system directory alongside managed-settings.json. This lets separate teams deploy independent policy fragments without coordinating edits to a single file.
Following the systemd convention, managed-settings.json is merged first as the base, then all *.json files in the drop-in directory are sorted alphabetically and merged on top. Later files override earlier ones for scalar values; arrays are concatenated and de-duplicated; objects are deep-merged. Hidden files starting with . are ignored.
Use numeric prefixes to control merge order, for example 10-telemetry.json and 20-security.json.


See  [/docs/en/permissions#managed-only-settings] managed settings and  [/docs/en/mcp#managed-mcp-configuration] Managed MCP configuration for details.




Managed deployments can also restrict plugin marketplace additions using
strictKnownMarketplaces. For more information, see  [/docs/en/plugin-marketplaces#managed-marketplace-restrictions] Managed marketplace restrictions.





Other configuration is stored in ~/.claude.json. This file contains your preferences (theme, notification settings, editor mode), OAuth session,  [/docs/en/mcp] MCP server configurations for user and local scopes, per-project state (allowed tools, trust settings), and various caches. Project-scoped MCP servers are stored separately in .mcp.json.






Claude Code automatically creates timestamped backups of configuration files and retains the five most recent backups to prevent data loss.





Example settings.json











{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}






The $schema line in the example above points to the  [https://json.schemastore.org/claude-code-settings.json] official JSON schema for Claude Code settings. Adding it to your settings.json enables autocomplete and inline validation in VS Code, Cursor, and any other editor that supports JSON schema validation.


 [#available-settings] ​


Available settings

settings.json supports a number of options:



KeyDescriptionExample
apiKeyHelperCustom script, to be executed in /bin/sh, to generate an auth value. This value will be sent as X-Api-Key and Authorization: Bearer headers for model requests/bin/generate_temp_api_key.sh
autoMemoryDirectoryCustom directory for  [/docs/en/memory#storage-location] auto memory storage. Accepts ~/-expanded paths. Not accepted in project settings (.claude/settings.json) to prevent shared repos from redirecting memory writes to sensitive locations. Accepted from policy, local, and user settings"~/my-memory-dir"
cleanupPeriodDaysSessions inactive for longer than this period are deleted at startup (default: 30 days).

Setting to 0 deletes all existing transcripts at startup and disables session persistence entirely. No new .jsonl files are written, /resume shows no conversations, and hooks receive an empty transcript_path.20
companyAnnouncementsAnnouncement to display to users at startup. If multiple announcements are provided, they will be cycled through at random.["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]
envEnvironment variables that will be applied to every session{"FOO": "bar"}
attributionCustomize attribution for git commits and pull requests. See  [#attribution-settings] Attribution settings{"commit": "🤖 Generated with Claude Code", "pr": ""}
includeCoAuthoredByDeprecated: Use attribution instead. Whether to include the co-authored-by Claude byline in git commits and pull requests (default: true)false
includeGitInstructionsInclude built-in commit and PR workflow instructions and the git status snapshot in Claude’s system prompt (default: true). Set to false to remove both, for example when using your own git workflow skills. The CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS environment variable takes precedence over this setting when setfalse
permissionsSee table below for structure of permissions.
autoModeCustomize what the  [/docs/en/permission-modes#eliminate-prompts-with-auto-mode] auto mode classifier blocks and allows. Contains environment, allow, and soft_deny arrays of prose rules. See  [/docs/en/permissions#configure-the-auto-mode-classifier] Configure the auto mode classifier. Not read from shared project settings{"environment": ["Trusted repo: github.example.com/acme"]}
disableAutoModeSet to "disable" to prevent  [/docs/en/permission-modes#eliminate-prompts-with-auto-mode] auto mode from being activated. Removes auto from the Shift+Tab cycle and rejects --permission-mode auto at startup. Most useful in  [/docs/en/permissions#managed-settings] managed settings where users cannot override it"disable"
useAutoModeDuringPlanWhether plan mode uses auto mode semantics when auto mode is available. Default: true. Not read from shared project settings. Appears in /config as “Use auto mode during plan”false
disableDeepLinkRegistrationSet to "disable" to prevent Claude Code from registering the claude-cli:// protocol handler with the operating system on startup. Deep links let external tools open a Claude Code session with a pre-filled prompt via claude-cli://open?q=.... Useful in environments where protocol handler registration is restricted or managed separately"disable"
hooksConfigure custom commands to run at lifecycle events. See  [/docs/en/hooks] hooks documentation for formatSee  [/docs/en/hooks] hooks
defaultShellDefault shell for input-box ! commands. Accepts "bash" (default) or "powershell". Setting "powershell" routes interactive ! commands through PowerShell on Windows. Requires CLAUDE_CODE_USE_POWERSHELL_TOOL=1. See  [/docs/en/tools-reference#powershell-tool] PowerShell tool"powershell"
disableAllHooksDisable all  [/docs/en/hooks] hooks and any custom  [/docs/en/statusline] status linetrue
allowManagedHooksOnly(Managed settings only) Prevent loading of user, project, and plugin hooks. Only allows managed hooks and SDK hooks. See  [#hook-configuration] Hook configurationtrue
allowedHttpHookUrlsAllowlist of URL patterns that HTTP hooks may target. Supports * as a wildcard. When set, hooks with non-matching URLs are blocked. Undefined = no restriction, empty array = block all HTTP hooks. Arrays merge across settings sources. See  [#hook-configuration] Hook configuration["https://hooks.example.com/*"]
httpHookAllowedEnvVarsAllowlist of environment variable names HTTP hooks may interpolate into headers. When set, each hook’s effective allowedEnvVars is the intersection with this list. Undefined = no restriction. Arrays merge across settings sources. See  [#hook-configuration] Hook configuration["MY_TOKEN", "HOOK_SECRET"]
allowManagedPermissionRulesOnly(Managed settings only) Prevent user and project settings from defining allow, ask, or deny permission rules. Only rules in managed settings apply. See  [/docs/en/permissions#managed-only-settings] Managed-only settingstrue
allowManagedMcpServersOnly(Managed settings only) Only allowedMcpServers from managed settings are respected. deniedMcpServers still merges from all sources. Users can still add MCP servers, but only the admin-defined allowlist applies. See  [/docs/en/mcp#managed-mcp-configuration] Managed MCP configurationtrue
modelOverride the default model to use for Claude Code"claude-sonnet-4-6"
availableModelsRestrict which models users can select via /model, --model, Config tool, or ANTHROPIC_MODEL. Does not affect the Default option. See  [/docs/en/model-config#restrict-model-selection] Restrict model selection["sonnet", "haiku"]
modelOverridesMap Anthropic model IDs to provider-specific model IDs such as Bedrock inference profile ARNs. Each model picker entry uses its mapped value when calling the provider API. See  [/docs/en/model-config#override-model-ids-per-version] Override model IDs per version{"claude-opus-4-6": "arn:aws:bedrock:..."}
effortLevelPersist the  [/docs/en/model-config#adjust-effort-level] effort level across sessions. Accepts "low", "medium", or "high". Written automatically when you run /effort low, /effort medium, or /effort high. Supported on Opus 4.6 and Sonnet 4.6"medium"
otelHeadersHelperScript to generate dynamic OpenTelemetry headers. Runs at startup and periodically (see  [/docs/en/monitoring-usage#dynamic-headers] Dynamic headers)/bin/generate_otel_headers.sh
statusLineConfigure a custom status line to display context. See  [/docs/en/statusline] statusLine documentation{"type": "command", "command": "~/.claude/statusline.sh"}
fileSuggestionConfigure a custom script for @ file autocomplete. See  [#file-suggestion-settings] File suggestion settings{"type": "command", "command": "~/.claude/file-suggestion.sh"}
respectGitignoreControl whether the @ file picker respects .gitignore patterns. When true (default), files matching .gitignore patterns are excluded from suggestionsfalse
outputStyleConfigure an output style to adjust the system prompt. See  [/docs/en/output-styles] output styles documentation"Explanatory"
agentRun the main thread as a named subagent. Applies that subagent’s system prompt, tool restrictions, and model. See  [/docs/en/sub-agents#invoke-subagents-explicitly] Invoke subagents explicitly"code-reviewer"
forceLoginMethodUse claudeai to restrict login to Claude.ai accounts, console to restrict login to Claude Console (API usage billing) accountsclaudeai
forceLoginOrgUUIDSpecify the UUID of an organization to automatically select it during login, bypassing the organization selection step. Requires forceLoginMethod to be set"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
enableAllProjectMcpServersAutomatically approve all MCP servers defined in project .mcp.json filestrue
enabledMcpjsonServersList of specific MCP servers from .mcp.json files to approve["memory", "github"]
disabledMcpjsonServersList of specific MCP servers from .mcp.json files to reject["filesystem"]
channelsEnabled(Managed settings only) Allow  [/docs/en/channels] channels for Team and Enterprise users. Unset or false blocks channel message delivery regardless of what users pass to --channelstrue
allowedChannelPlugins(Managed settings only) Allowlist of channel plugins that may push messages. Replaces the default Anthropic allowlist when set. Undefined = fall back to the default, empty array = block all channel plugins. Requires channelsEnabled: true. See  [/docs/en/channels#restrict-which-channel-plugins-can-run] Restrict which channel plugins can run[{ "marketplace": "claude-plugins-official", "plugin": "telegram" }]
allowedMcpServersWhen set in managed-settings.json, allowlist of MCP servers users can configure. Undefined = no restrictions, empty array = lockdown. Applies to all scopes. Denylist takes precedence. See  [/docs/en/mcp#managed-mcp-configuration] Managed MCP configuration[{ "serverName": "github" }]
deniedMcpServersWhen set in managed-settings.json, denylist of MCP servers that are explicitly blocked. Applies to all scopes including managed servers. Denylist takes precedence over allowlist. See  [/docs/en/mcp#managed-mcp-configuration] Managed MCP configuration[{ "serverName": "filesystem" }]
strictKnownMarketplacesWhen set in managed-settings.json, allowlist of plugin marketplaces users can add. Undefined = no restrictions, empty array = lockdown. Applies to marketplace additions only. See  [/docs/en/plugin-marketplaces#managed-marketplace-restrictions] Managed marketplace restrictions[{ "source": "github", "repo": "acme-corp/plugins" }]
blockedMarketplaces(Managed settings only) Blocklist of marketplace sources. Blocked sources are checked before downloading, so they never touch the filesystem. See  [/docs/en/plugin-marketplaces#managed-marketplace-restrictions] Managed marketplace restrictions[{ "source": "github", "repo": "untrusted/plugins" }]
pluginTrustMessage(Managed settings only) Custom message appended to the plugin trust warning shown before installation. Use this to add organization-specific context, for example to confirm that plugins from your internal marketplace are vetted."All plugins from our marketplace are approved by IT"
awsAuthRefreshCustom script that modifies the .aws directory (see  [/docs/en/amazon-bedrock#advanced-credential-configuration] advanced credential configuration)aws sso login --profile myprofile
awsCredentialExportCustom script that outputs JSON with AWS credentials (see  [/docs/en/amazon-bedrock#advanced-credential-configuration] advanced credential configuration)/bin/generate_aws_grant.sh
alwaysThinkingEnabledEnable  [/docs/en/common-workflows#use-extended-thinking-thinking-mode] extended thinking by default for all sessions. Typically configured via the /config command rather than editing directlytrue
plansDirectoryCustomize where plan files are stored. Path is relative to project root. Default: ~/.claude/plans"./plans"
showClearContextOnPlanAcceptShow the “clear context” option on the plan accept screen. Defaults to false. Set to true to restore the optiontrue
spinnerVerbsCustomize the action verbs shown in the spinner and turn duration messages. Set mode to "replace" to use only your verbs, or "append" to add them to the defaults{"mode": "append", "verbs": ["Pondering", "Crafting"]}
languageConfigure Claude’s preferred response language (e.g., "japanese", "spanish", "french"). Claude will respond in this language by default. Also sets the  [/docs/en/voice-dictation#change-the-dictation-language] voice dictation language"japanese"
voiceEnabledEnable push-to-talk  [/docs/en/voice-dictation] voice dictation. Written automatically when you run /voice. Requires a Claude.ai accounttrue
autoUpdatesChannelRelease channel to follow for updates. Use "stable" for a version that is typically about one week old and skips versions with major regressions, or "latest" (default) for the most recent release"stable"
spinnerTipsEnabledShow tips in the spinner while Claude is working. Set to false to disable tips (default: true)false
spinnerTipsOverrideOverride spinner tips with custom strings. tips: array of tip strings. excludeDefault: if true, only show custom tips; if false or absent, custom tips are merged with built-in tips{ "excludeDefault": true, "tips": ["Use our internal tool X"] }
prefersReducedMotionReduce or disable UI animations (spinners, shimmer, flash effects) for accessibilitytrue
fastModePerSessionOptInWhen true, fast mode does not persist across sessions. Each session starts with fast mode off, requiring users to enable it with /fast. The user’s fast mode preference is still saved. See  [/docs/en/fast-mode#require-per-session-opt-in] Require per-session opt-intrue
feedbackSurveyRateProbability (0–1) that the  [/docs/en/data-usage#session-quality-surveys] session quality survey appears when eligible. Set to 0 to suppress entirely. Useful when using Bedrock, Vertex, or Foundry where the default sample rate does not apply0.05





 [#global-config-settings] ​


Global config settings

These settings are stored in ~/.claude.json rather than settings.json. Adding them to settings.json will trigger a schema validation error.



KeyDescriptionExample
autoConnectIdeAutomatically connect to a running IDE when Claude Code starts from an external terminal. Default: false. Appears in /config as Auto-connect to IDE (external terminal) when running outside a VS Code or JetBrains terminaltrue
autoInstallIdeExtensionAutomatically install the Claude Code IDE extension when running from a VS Code terminal. Default: true. Appears in /config as Auto-install IDE extension when running inside a VS Code or JetBrains terminal. You can also set the  [/docs/en/env-vars] CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL environment variablefalse
editorModeKey binding mode for the input prompt: "normal" or "vim". Default: "normal". Written automatically when you run /vim. Appears in /config as Key binding mode"vim"
showTurnDurationShow turn duration messages after responses, e.g. “Cooked for 1m 6s”. Default: true. Appears in /config as Show turn durationfalse
terminalProgressBarEnabledShow the terminal progress bar in supported terminals: ConEmu, Ghostty 1.2.0+, and iTerm2 3.6.6+. Default: true. Appears in /config as Terminal progress barfalse
teammateModeHow  [/docs/en/agent-teams] agent team teammates display: auto (picks split panes in tmux or iTerm2, in-process otherwise), in-process, or tmux. See  [/docs/en/agent-teams#choose-a-display-mode] choose a display mode"in-process"





 [#worktree-settings] ​


Worktree settings

Configure how --worktree creates and manages git worktrees. Use these settings to reduce disk usage and startup time in large monorepos.



KeyDescriptionExample
worktree.symlinkDirectoriesDirectories to symlink from the main repository into each worktree to avoid duplicating large directories on disk. No directories are symlinked by default["node_modules", ".cache"]
worktree.sparsePathsDirectories to check out in each worktree via git sparse-checkout (cone mode). Only the listed paths are written to disk, which is faster in large monorepos["packages/my-app", "shared/utils"]



To copy gitignored files like .env into new worktrees, use a  [/docs/en/common-workflows#copy-gitignored-files-to-worktrees] .worktreeinclude file in your project root instead of a setting.


 [#permission-settings] ​


Permission settings




KeysDescriptionExample
allowArray of permission rules to allow tool use. See  [#permission-rule-syntax] Permission rule syntax below for pattern matching details[ "Bash(git diff *)" ]
askArray of permission rules to ask for confirmation upon tool use. See  [#permission-rule-syntax] Permission rule syntax below[ "Bash(git push *)" ]
denyArray of permission rules to deny tool use. Use this to exclude sensitive files from Claude Code access. See  [#permission-rule-syntax] Permission rule syntax and  [/docs/en/permissions#tool-specific-permission-rules] Bash permission limitations[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]
additionalDirectoriesAdditional  [/docs/en/permissions#working-directories] working directories that Claude has access to[ "../docs/" ]
defaultModeDefault  [/docs/en/permission-modes] permission mode when opening Claude Code. Valid values: default, acceptEdits, plan, auto, dontAsk, bypassPermissions. The --permission-mode CLI flag overrides this setting for a single session"acceptEdits"
disableBypassPermissionsModeSet to "disable" to prevent bypassPermissions mode from being activated. Disables the --dangerously-skip-permissions flag. Most useful in  [/docs/en/permissions#managed-settings] managed settings where users cannot override it"disable"





 [#permission-rule-syntax] ​


Permission rule syntax

Permission rules follow the format Tool or Tool(specifier). Rules are evaluated in order: deny rules first, then ask, then allow. The first matching rule wins.
Quick examples:



RuleEffect
BashMatches all Bash commands
Bash(npm run *)Matches commands starting with npm run
Read(./.env)Matches reading the .env file
WebFetch(domain:example.com)Matches fetch requests to example.com



For the complete rule syntax reference, including wildcard behavior, tool-specific patterns for Read, Edit, WebFetch, MCP, and Agent rules, and security limitations of Bash patterns, see  [/docs/en/permissions#permission-rule-syntax] Permission rule syntax.


 [#sandbox-settings] ​


Sandbox settings

Configure advanced sandboxing behavior. Sandboxing isolates bash commands from your filesystem and network. See  [/docs/en/sandboxing] Sandboxing for details.



KeysDescriptionExample
enabledEnable bash sandboxing (macOS, Linux, and WSL2). Default: falsetrue
failIfUnavailableExit with an error at startup if sandbox.enabled is true but the sandbox cannot start (missing dependencies, unsupported platform, or platform restrictions). When false (default), a warning is shown and commands run unsandboxed. Intended for managed settings deployments that require sandboxing as a hard gatetrue
autoAllowBashIfSandboxedAuto-approve bash commands when sandboxed. Default: truetrue
excludedCommandsCommands that should run outside of the sandbox["git", "docker"]
allowUnsandboxedCommandsAllow commands to run outside the sandbox via the dangerouslyDisableSandbox parameter. When set to false, the dangerouslyDisableSandbox escape hatch is completely disabled and all commands must run sandboxed (or be in excludedCommands). Useful for enterprise policies that require strict sandboxing. Default: truefalse
filesystem.allowWriteAdditional paths where sandboxed commands can write. Arrays are merged across all settings scopes: user, project, and managed paths are combined, not replaced. Also merged with paths from Edit(...) allow permission rules. See  [#sandbox-path-prefixes] path prefixes below.["/tmp/build", "~/.kube"]
filesystem.denyWritePaths where sandboxed commands cannot write. Arrays are merged across all settings scopes. Also merged with paths from Edit(...) deny permission rules.["/etc", "/usr/local/bin"]
filesystem.denyReadPaths where sandboxed commands cannot read. Arrays are merged across all settings scopes. Also merged with paths from Read(...) deny permission rules.["~/.aws/credentials"]
filesystem.allowReadPaths to re-allow reading within denyRead regions. Takes precedence over denyRead. Arrays are merged across all settings scopes. Use this to create workspace-only read access patterns.["."]
filesystem.allowManagedReadPathsOnly(Managed settings only) Only allowRead paths from managed settings are respected. allowRead entries from user, project, and local settings are ignored. Default: falsetrue
network.allowUnixSocketsUnix socket paths accessible in sandbox (for SSH agents, etc.)["~/.ssh/agent-socket"]
network.allowAllUnixSocketsAllow all Unix socket connections in sandbox. Default: falsetrue
network.allowLocalBindingAllow binding to localhost ports (macOS only). Default: falsetrue
network.allowedDomainsArray of domains to allow for outbound network traffic. Supports wildcards (e.g., *.example.com).["github.com", "*.npmjs.org"]
network.allowManagedDomainsOnly(Managed settings only) Only allowedDomains and WebFetch(domain:...) allow rules from managed settings are respected. Domains from user, project, and local settings are ignored. Non-allowed domains are blocked automatically without prompting the user. Denied domains are still respected from all sources. Default: falsetrue
network.httpProxyPortHTTP proxy port used if you wish to bring your own proxy. If not specified, Claude will run its own proxy.8080
network.socksProxyPortSOCKS5 proxy port used if you wish to bring your own proxy. If not specified, Claude will run its own proxy.8081
enableWeakerNestedSandboxEnable weaker sandbox for unprivileged Docker environments (Linux and WSL2 only). Reduces security. Default: falsetrue
enableWeakerNetworkIsolation(macOS only) Allow access to the system TLS trust service (com.apple.trustd.agent) in the sandbox. Required for Go-based tools like gh, gcloud, and terraform to verify TLS certificates when using httpProxyPort with a MITM proxy and custom CA. Reduces security by opening a potential data exfiltration path. Default: falsetrue





 [#sandbox-path-prefixes] ​


Sandbox path prefixes

Paths in filesystem.allowWrite, filesystem.denyWrite, filesystem.denyRead, and filesystem.allowRead support these prefixes:



PrefixMeaningExample
/Absolute path from filesystem root/tmp/build stays /tmp/build
~/Relative to home directory~/.kube becomes $HOME/.kube
./ or no prefixRelative to the project root for project settings, or to ~/.claude for user settings./output in .claude/settings.json resolves to <project-root>/output



The older //path prefix for absolute paths still works. If you previously used single-slash /path expecting project-relative resolution, switch to ./path. This syntax differs from  [/docs/en/permissions#read-and-edit] Read and Edit permission rules, which use //path for absolute and /path for project-relative. Sandbox filesystem paths use standard conventions: /tmp/build is an absolute path.
Configuration example:











{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "allowUnixSockets": [
        "/var/run/docker.sock"
      ],
      "allowLocalBinding": true
    }
  }
}






Filesystem and network restrictions can be configured in two ways that are merged together:


sandbox.filesystem settings (shown above): Control paths at the OS-level sandbox boundary. These restrictions apply to all subprocess commands (e.g., kubectl, terraform, npm), not just Claude’s file tools.

Permission rules: Use Edit allow/deny rules to control Claude’s file tool access, Read deny rules to block reads, and WebFetch allow/deny rules to control network domains. Paths from these rules are also merged into the sandbox configuration.



 [#attribution-settings] ​


Attribution settings

Claude Code adds attribution to git commits and pull requests. These are configured separately:


Commits use  [https://git-scm.com/docs/git-interpret-trailers] git trailers (like Co-Authored-By) by default,  which can be customized or disabled

Pull request descriptions are plain text




KeysDescription
commitAttribution for git commits, including any trailers. Empty string hides commit attribution
prAttribution for pull request descriptions. Empty string hides pull request attribution



Default commit attribution:











🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 < [/cdn-cgi/l/email-protection] [email protected]>






Default pull request attribution:











🤖 Generated with [Claude Code](https://claude.com/claude-code)






Example:











{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI < [/cdn-cgi/l/email-protection] [email protected]>",
    "pr": ""
  }
}










The attribution setting takes precedence over the deprecated includeCoAuthoredBy setting. To hide all attribution, set commit and pr to empty strings.




 [#file-suggestion-settings] ​


File suggestion settings

Configure a custom command for @ file path autocomplete. The built-in file suggestion uses fast filesystem traversal, but large monorepos may benefit from project-specific indexing such as a pre-built file index or custom tooling.











{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}






The command runs with the same environment variables as  [/docs/en/hooks] hooks, including CLAUDE_PROJECT_DIR. It receives JSON via stdin with a query field:











{"query": "src/comp"}






Output newline-separated file paths to stdout (currently limited to 15):











src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx






Example:











#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20








 [#hook-configuration] ​


Hook configuration

These settings control which hooks are allowed to run and what HTTP hooks can access. The allowManagedHooksOnly setting can only be configured in  [#settings-files] managed settings. The URL and env var allowlists can be set at any settings level and merge across sources.
Behavior when allowManagedHooksOnly is true:


Managed hooks and SDK hooks are loaded

User hooks, project hooks, and plugin hooks are blocked

Restrict HTTP hook URLs:
Limit which URLs HTTP hooks can target. Supports * as a wildcard for matching. When the array is defined, HTTP hooks targeting non-matching URLs are silently blocked.











{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}






Restrict HTTP hook environment variables:
Limit which environment variable names HTTP hooks can interpolate into header values. Each hook’s effective allowedEnvVars is the intersection of its own list and this setting.











{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}








 [#settings-precedence] ​


Settings precedence

Settings apply in order of precedence. From highest to lowest:



Managed settings ( [/docs/en/server-managed-settings] server-managed,  [#configuration-scopes] MDM/OS-level policies, or  [/docs/en/settings#settings-files] managed settings)


Policies deployed by IT through server delivery, MDM configuration profiles, registry policies, or managed settings files

Cannot be overridden by any other level, including command line arguments

Within the managed tier, precedence is: server-managed > MDM/OS-level policies > file-based (managed-settings.d/*.json + managed-settings.json) > HKCU registry (Windows only). Only one managed source is used; sources do not merge across tiers. Within the file-based tier, drop-in files and the base file are merged together.




Command line arguments


Temporary overrides for a specific session




Local project settings (.claude/settings.local.json)


Personal project-specific settings




Shared project settings (.claude/settings.json)


Team-shared project settings in source control




User settings (~/.claude/settings.json)


Personal global settings



This hierarchy ensures that organizational policies are always enforced while still allowing teams and individuals to customize their experience. The same precedence applies whether you run Claude Code from the CLI, the  [/docs/en/vs-code] VS Code extension, or a  [/docs/en/jetbrains] JetBrains IDE.
For example, if your user settings allow Bash(npm run *) but a project’s shared settings deny it, the project setting takes precedence and the command is blocked.




Array settings merge across scopes. When the same array-valued setting (such as sandbox.filesystem.allowWrite or permissions.allow) appears in multiple scopes, the arrays are concatenated and deduplicated, not replaced. This means lower-priority scopes can add entries without overriding those set by higher-priority scopes, and vice versa. For example, if managed settings set allowWrite to ["/opt/company-tools"] and a user adds ["~/.kube"], both paths are included in the final configuration.




 [#verify-active-settings] ​


Verify active settings

Run /status inside Claude Code to see which settings sources are active and where they come from. The output shows each configuration layer (managed, user, project) along with its origin, such as Enterprise managed settings (remote), Enterprise managed settings (plist), Enterprise managed settings (HKLM), or Enterprise managed settings (file). If a settings file contains errors, /status reports the issue so you can fix it.


 [#key-points-about-the-configuration-system] ​


Key points about the configuration system



Memory files (CLAUDE.md): Contain instructions and context that Claude loads at startup

Settings files (JSON): Configure permissions, environment variables, and tool behavior

Skills: Custom prompts that can be invoked with /skill-name or loaded by Claude automatically

MCP servers: Extend Claude Code with additional tools and integrations

Precedence: Higher-level configurations (Managed) override lower-level ones (User/Project)

Inheritance: Settings are merged, with more specific settings adding to or overriding broader ones



 [#system-prompt] ​


System prompt

Claude Code’s internal system prompt is not published. To add custom instructions, use CLAUDE.md files or the --append-system-prompt flag.


 [#excluding-sensitive-files] ​


Excluding sensitive files

To prevent Claude Code from accessing files containing sensitive information like API keys, secrets, and environment files, use the permissions.deny setting in your .claude/settings.json file:











{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}






This replaces the deprecated ignorePatterns configuration. Files matching these patterns are excluded from file discovery and search results, and read operations on these files are denied.


 [#subagent-configuration] ​


Subagent configuration

Claude Code supports custom AI subagents that can be configured at both user and project levels. These subagents are stored as Markdown files with YAML frontmatter:


User subagents: ~/.claude/agents/ - Available across all your projects

Project subagents: .claude/agents/ - Specific to your project and can be shared with your team

Subagent files define specialized AI assistants with custom prompts and tool permissions. Learn more about creating and using subagents in the  [/docs/en/sub-agents] subagents documentation.


 [#plugin-configuration] ​


Plugin configuration

Claude Code supports a plugin system that lets you extend functionality with skills, agents, hooks, and MCP servers. Plugins are distributed through marketplaces and can be configured at both user and repository levels.


 [#plugin-settings] ​


Plugin settings

Plugin-related settings in settings.json:











{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": "github",
      "repo": "acme-corp/claude-plugins"
    }
  }
}








 [#enabledplugins] ​


enabledPlugins

Controls which plugins are enabled. Format: "plugin-name@marketplace-name": true/false
Scopes:


User settings (~/.claude/settings.json): Personal plugin preferences

Project settings (.claude/settings.json): Project-specific plugins shared with team

Local settings (.claude/settings.local.json): Per-machine overrides (not committed)

Managed settings (managed-settings.json): Organization-wide policy overrides that block installation at all scopes and hide the plugin from the marketplace

Example:











{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}








 [#extraknownmarketplaces] ​


extraKnownMarketplaces

Defines additional marketplaces that should be made available for the repository. Typically used in repository-level settings to ensure team members have access to required plugin sources.
When a repository includes extraKnownMarketplaces:


Team members are prompted to install the marketplace when they trust the folder

Team members are then prompted to install plugins from that marketplace

Users can skip unwanted marketplaces or plugins (stored in user settings)

Installation respects trust boundaries and requires explicit consent

Example:











{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}






Marketplace source types:


github: GitHub repository (uses repo)

git: Any git URL (uses url)

directory: Local filesystem path (uses path, for development only)

hostPattern: regex pattern to match marketplace hosts (uses hostPattern)

settings: inline marketplace declared directly in settings.json without a separate hosted repository (uses name and plugins)

Use source: 'settings' to declare a small set of plugins inline without setting up a hosted marketplace repository. Plugins listed here must reference external sources such as GitHub or npm. You still need to enable each plugin separately in enabledPlugins.











{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}








 [#strictknownmarketplaces] ​


strictKnownMarketplaces

Managed settings only: Controls which plugin marketplaces users are allowed to add. This setting can only be configured in  [/docs/en/settings#settings-files] managed settings and provides administrators with strict control over marketplace sources.
Managed settings file locations:


macOS: /Library/Application Support/ClaudeCode/managed-settings.json

Linux and WSL: /etc/claude-code/managed-settings.json

Windows: C:\Program Files\ClaudeCode\managed-settings.json

Key characteristics:


Only available in managed settings (managed-settings.json)

Cannot be overridden by user or project settings (highest precedence)

Enforced BEFORE network/filesystem operations (blocked sources never execute)

Uses exact matching for source specifications (including ref, path for git sources), except hostPattern, which uses regex matching

Allowlist behavior:


undefined (default): No restrictions - users can add any marketplace

Empty array []: Complete lockdown - users cannot add any new marketplaces

List of sources: Users can only add marketplaces that match exactly

All supported source types:
The allowlist supports multiple marketplace source types. Most sources use exact matching, while hostPattern uses regex matching against the marketplace host.


GitHub repositories:












{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }






Fields: repo (required), ref (optional: branch/tag/SHA), path (optional: subdirectory)


Git repositories:












{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh:// [/cdn-cgi/l/email-protection] [email protected]/plugins.git", "ref": "v3.1", "path": "approved" }






Fields: url (required), ref (optional: branch/tag/SHA), path (optional: subdirectory)


URL-based marketplaces:












{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }






Fields: url (required), headers (optional: HTTP headers for authenticated access)




URL-based marketplaces only download the marketplace.json file. They do not download plugin files from the server. Plugins in URL-based marketplaces must use external sources (GitHub, npm, or git URLs) rather than relative paths. For plugins with relative paths, use a Git-based marketplace instead. See  [/docs/en/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces] Troubleshooting for details.




NPM packages:












{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }






Fields: package (required, supports scoped packages)


File paths:












{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }






Fields: path (required: absolute path to marketplace.json file)


Directory paths:












{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }






Fields: path (required: absolute path to directory containing .claude-plugin/marketplace.json)


Host pattern matching:












{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }






Fields: hostPattern (required: regex pattern to match against the marketplace host)
Use host pattern matching when you want to allow all marketplaces from a specific host without enumerating each repository individually. This is useful for organizations with internal GitHub Enterprise or GitLab servers where developers create their own marketplaces.
Host extraction by source type:


github: always matches against github.com

git: extracts hostname from the URL (supports both HTTPS and SSH formats)

url: extracts hostname from the URL

npm, file, directory: not supported for host pattern matching

Configuration examples:
Example: allow specific marketplaces only:











{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}






Example - Disable all marketplace additions:











{
  "strictKnownMarketplaces": []
}






Example: allow all marketplaces from an internal git server:











{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}






Exact matching requirements:
Marketplace sources must match exactly for a user’s addition to be allowed. For git-based sources (github and git), this includes all optional fields:


The repo or url must match exactly

The ref field must match exactly (or both be undefined)

The path field must match exactly (or both be undefined)

Examples of sources that do NOT match:











// These are DIFFERENT sources:
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// These are also DIFFERENT:
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }






Comparison with extraKnownMarketplaces:



AspectstrictKnownMarketplacesextraKnownMarketplaces
PurposeOrganizati

[... truncated at 50KB ...]
```

### cli-reference

URL: https://code.claude.com/docs/en/cli-reference
Hash: e88ef12d2c73

```
CLI reference - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Reference

CLI reference




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Reference


 [/docs/en/cli-reference] 

CLI reference


 [/docs/en/commands] 

Built-in commands


 [/docs/en/env-vars] 

Environment variables


 [/docs/en/tools-reference] 

Tools reference


 [/docs/en/interactive-mode] 

Interactive mode


 [/docs/en/checkpointing] 

Checkpointing


 [/docs/en/hooks] 

Hooks reference


 [/docs/en/plugins-reference] 

Plugins reference


 [/docs/en/channels-reference] 

Channels reference











On this page

 [#cli-commands] CLI commands
 [#cli-flags] CLI flags
 [#system-prompt-flags] System prompt flags
 [#see-also] See also



























 [#cli-commands] ​


CLI commands

You can start sessions, pipe content, resume conversations, and manage updates with these commands:



CommandDescriptionExample
claudeStart interactive sessionclaude
claude "query"Start interactive session with initial promptclaude "explain this project"
claude -p "query"Query via SDK, then exitclaude -p "explain this function"
cat file | claude -p "query"Process piped contentcat logs.txt | claude -p "explain"
claude -cContinue most recent conversation in current directoryclaude -c
claude -c -p "query"Continue via SDKclaude -c -p "Check for type errors"
claude -r "<session>" "query"Resume session by ID or nameclaude -r "auth-refactor" "Finish this PR"
claude updateUpdate to latest versionclaude update
claude auth loginSign in to your Anthropic account. Use --email to pre-fill your email address, --sso to force SSO authentication, and --console to sign in with Anthropic Console for API usage billing instead of a Claude subscriptionclaude auth login --console
claude auth logoutLog out from your Anthropic accountclaude auth logout
claude auth statusShow authentication status as JSON. Use --text for human-readable output. Exits with code 0 if logged in, 1 if notclaude auth status
claude agentsList all configured  [/docs/en/sub-agents] subagents, grouped by sourceclaude agents
claude auto-mode defaultsPrint the built-in  [/docs/en/permission-modes#eliminate-prompts-with-auto-mode] auto mode classifier rules as JSON. Use claude auto-mode config to see your effective config with settings appliedclaude auto-mode defaults > rules.json
claude mcpConfigure Model Context Protocol (MCP) serversSee the  [/docs/en/mcp] Claude Code MCP documentation.
claude pluginManage Claude Code  [/docs/en/plugins] plugins. Alias: claude plugins. See  [/docs/en/plugins-reference#cli-commands-reference] plugin reference for subcommandsclaude plugin install code-review@claude-plugins-official
claude remote-controlStart a  [/docs/en/remote-control] Remote Control server to control Claude Code from Claude.ai or the Claude app. Runs in server mode (no local interactive session). See  [/docs/en/remote-control#server-mode] Server mode flagsclaude remote-control --name "My Project"





 [#cli-flags] ​


CLI flags

Customize Claude Code’s behavior with these command-line flags:



FlagDescriptionExample
--add-dirAdd additional working directories for Claude to access (validates each path exists as a directory)claude --add-dir ../apps ../lib
--agentSpecify an agent for the current session (overrides the agent setting)claude --agent my-custom-agent
--agentsDefine custom subagents dynamically via JSON. Uses the same field names as subagent  [/docs/en/sub-agents#supported-frontmatter-fields] frontmatter, plus a prompt field for the agent’s instructionsclaude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'
--allow-dangerously-skip-permissionsAdd bypassPermissions to the Shift+Tab mode cycle without starting in it. Lets you begin in a different mode like plan and switch to bypassPermissions later. See  [/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode] permission modesclaude --permission-mode plan --allow-dangerously-skip-permissions
--allowedToolsTools that execute without prompting for permission. See  [/docs/en/settings#permission-rule-syntax] permission rule syntax for pattern matching. To restrict which tools are available, use --tools instead"Bash(git log *)" "Bash(git diff *)" "Read"
--append-system-promptAppend custom text to the end of the default system promptclaude --append-system-prompt "Always use TypeScript"
--append-system-prompt-fileLoad additional system prompt text from a file and append to the default promptclaude --append-system-prompt-file ./extra-rules.txt
--bareMinimal mode: skip auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md so scripted calls start faster. Claude has access to Bash, file read, and file edit tools. Sets  [/docs/en/env-vars] CLAUDE_CODE_SIMPLE. See  [/docs/en/headless#start-faster-with-bare-mode] bare modeclaude --bare -p "query"
--betasBeta headers to include in API requests (API key users only)claude --betas interleaved-thinking
--channels(Research preview) MCP servers whose  [/docs/en/channels] channel notifications Claude should listen for in this session. Space-separated list of plugin:<name>@<marketplace> entries. Requires Claude.ai authenticationclaude --channels plugin:my-notifier@my-marketplace
--chromeEnable  [/docs/en/chrome] Chrome browser integration for web automation and testingclaude --chrome
--continue, -cLoad the most recent conversation in the current directoryclaude --continue
--dangerously-load-development-channelsEnable  [/docs/en/channels-reference#test-during-the-research-preview] channels that are not on the approved allowlist, for local development. Accepts plugin:<name>@<marketplace> and server:<name> entries. Prompts for confirmationclaude --dangerously-load-development-channels server:webhook
--dangerously-skip-permissionsSkip permission prompts. Equivalent to --permission-mode bypassPermissions. See  [/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode] permission modes for what this does and does not skipclaude --dangerously-skip-permissions
--debugEnable debug mode with optional category filtering (for example, "api,hooks" or "!statsig,!file")claude --debug "api,mcp"
--disable-slash-commandsDisable all skills and commands for this sessionclaude --disable-slash-commands
--disallowedToolsTools that are removed from the model’s context and cannot be used"Bash(git log *)" "Bash(git diff *)" "Edit"
--effortSet the  [/docs/en/model-config#adjust-effort-level] effort level for the current session. Options: low, medium, high, max (Opus 4.6 only). Session-scoped and does not persist to settingsclaude --effort high
--fallback-modelEnable automatic fallback to specified model when default model is overloaded (print mode only)claude -p --fallback-model sonnet "query"
--fork-sessionWhen resuming, create a new session ID instead of reusing the original (use with --resume or --continue)claude --resume abc123 --fork-session
--from-prResume sessions linked to a specific GitHub PR. Accepts a PR number or URL. Sessions are automatically linked when created via gh pr createclaude --from-pr 123
--ideAutomatically connect to IDE on startup if exactly one valid IDE is availableclaude --ide
--initRun initialization hooks and start interactive modeclaude --init
--init-onlyRun initialization hooks and exit (no interactive session)claude --init-only
--include-partial-messagesInclude partial streaming events in output (requires --print and --output-format=stream-json)claude -p --output-format stream-json --include-partial-messages "query"
--input-formatSpecify input format for print mode (options: text, stream-json)claude -p --output-format json --input-format stream-json
--json-schemaGet validated JSON output matching a JSON Schema after agent completes its workflow (print mode only, see  [https://platform.claude.com/docs/en/agent-sdk/structured-outputs] structured outputs)claude -p --json-schema '{"type":"object","properties":{...}}' "query"
--maintenanceRun maintenance hooks and exitclaude --maintenance
--max-budget-usdMaximum dollar amount to spend on API calls before stopping (print mode only)claude -p --max-budget-usd 5.00 "query"
--max-turnsLimit the number of agentic turns (print mode only). Exits with an error when the limit is reached. No limit by defaultclaude -p --max-turns 3 "query"
--mcp-configLoad MCP servers from JSON files or strings (space-separated)claude --mcp-config ./mcp.json
--modelSets the model for the current session with an alias for the latest model (sonnet or opus) or a model’s full nameclaude --model claude-sonnet-4-6
--name, -nSet a display name for the session, shown in /resume and the terminal title. You can resume a named session with claude --resume <name>. 

 [/docs/en/commands] /rename changes the name mid-session and also shows it on the prompt barclaude -n "my-feature-work"
--no-chromeDisable  [/docs/en/chrome] Chrome browser integration for this sessionclaude --no-chrome
--no-session-persistenceDisable session persistence so sessions are not saved to disk and cannot be resumed (print mode only)claude -p --no-session-persistence "query"
--output-formatSpecify output format for print mode (options: text, json, stream-json)claude -p "query" --output-format json
--enable-auto-modeUnlock  [/docs/en/permission-modes#eliminate-prompts-with-auto-mode] auto mode in the Shift+Tab cycle. Requires a Team, Enterprise, or API plan and Claude Sonnet 4.6 or Opus 4.6claude --enable-auto-mode
--permission-modeBegin in a specified  [/docs/en/permission-modes] permission mode. Accepts default, acceptEdits, plan, auto, dontAsk, or bypassPermissions. Overrides defaultMode from settings filesclaude --permission-mode plan
--permission-prompt-toolSpecify an MCP tool to handle permission prompts in non-interactive modeclaude -p --permission-prompt-tool mcp_auth_tool "query"
--plugin-dirLoad plugins from a directory for this session only. Each flag takes one path. Repeat the flag for multiple directories: --plugin-dir A --plugin-dir Bclaude --plugin-dir ./my-plugins
--print, -pPrint response without interactive mode (see  [https://platform.claude.com/docs/en/agent-sdk/overview] Agent SDK documentation for programmatic usage details)claude -p "query"
--remoteCreate a new  [/docs/en/claude-code-on-the-web] web session on claude.ai with the provided task descriptionclaude --remote "Fix the login bug"
--remote-control, --rcStart an interactive session with  [/docs/en/remote-control#interactive-session] Remote Control enabled so you can also control it from claude.ai or the Claude app. Optionally pass a name for the sessionclaude --remote-control "My Project"
--resume, -rResume a specific session by ID or name, or show an interactive picker to choose a sessionclaude --resume auth-refactor
--session-idUse a specific session ID for the conversation (must be a valid UUID)claude --session-id "550e8400-e29b-41d4-a716-446655440000"
--setting-sourcesComma-separated list of setting sources to load (user, project, local)claude --setting-sources user,project
--settingsPath to a settings JSON file or a JSON string to load additional settings fromclaude --settings ./settings.json
--strict-mcp-configOnly use MCP servers from --mcp-config, ignoring all other MCP configurationsclaude --strict-mcp-config --mcp-config ./mcp.json
--system-promptReplace the entire system prompt with custom textclaude --system-prompt "You are a Python expert"
--system-prompt-fileLoad system prompt from a file, replacing the default promptclaude --system-prompt-file ./custom-prompt.txt
--teleportResume a  [/docs/en/claude-code-on-the-web] web session in your local terminalclaude --teleport
--teammate-modeSet how  [/docs/en/agent-teams] agent team teammates display: auto (default), in-process, or tmux. See  [/docs/en/agent-teams#set-up-agent-teams] set up agent teamsclaude --teammate-mode in-process
--toolsRestrict which built-in tools Claude can use. Use "" to disable all, "default" for all, or tool names like "Bash,Edit,Read"claude --tools "Bash,Edit,Read"
--verboseEnable verbose logging, shows full turn-by-turn outputclaude --verbose
--version, -vOutput the version numberclaude -v
--worktree, -wStart Claude in an isolated  [/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees] git worktree at <repo>/.claude/worktrees/<name>. If no name is given, one is auto-generatedclaude -w feature-auth
--tmuxCreate a tmux session for the worktree. Requires --worktree. Uses iTerm2 native panes when available; pass --tmux=classic for traditional tmuxclaude -w feature-auth --tmux





 [#system-prompt-flags] ​


System prompt flags

Claude Code provides four flags for customizing the system prompt. All four work in both interactive and non-interactive modes.



FlagBehaviorExample
--system-promptReplaces the entire default promptclaude --system-prompt "You are a Python expert"
--system-prompt-fileReplaces with file contentsclaude --system-prompt-file ./prompts/review.txt
--append-system-promptAppends to the default promptclaude --append-system-prompt "Always use TypeScript"
--append-system-prompt-fileAppends file contents to the default promptclaude --append-system-prompt-file ./style-rules.txt



--system-prompt and --system-prompt-file are mutually exclusive. The append flags can be combined with either replacement flag.
For most use cases, use an append flag. Appending preserves Claude Code’s built-in capabilities while adding your requirements. Use a replacement flag only when you need complete control over the system prompt.


 [#see-also] ​


See also



 [/docs/en/chrome] Chrome extension - Browser automation and web testing

 [/docs/en/interactive-mode] Interactive mode - Shortcuts, input modes, and interactive features

 [/docs/en/quickstart] Quickstart guide - Getting started with Claude Code

 [/docs/en/common-workflows] Common workflows - Advanced workflows and patterns

 [/docs/en/settings] Settings - Configuration options

 [https://platform.claude.com/docs/en/agent-sdk/overview] Agent SDK documentation - Programmatic usage and integrations




Was this page helpful?


YesNo






 [/docs/en/commands] Built-in commands





⌘I











 [/docs/en/overview] 
 [https://x.com/AnthropicAI]  [https://www.linkedin.com/company/anthropicresearch] 






 [https://www.anthropic.com/company]  [https://www.anthropic.com/careers]  [https://www.anthropic.com/economic-futures]  [https://www.anthropic.com/research]  [https://www.anthropic.com/news]  [https://trust.anthropic.com/]  [https://www.anthropic.com/transparency] 





 [https://www.anthropic.com/supported-countries]  [https://status.anthropic.com/]  [https://support.claude.com/] 





 [https://www.anthropic.com/learn]  [https://claude.com/partners/mcp]  [https://www.claude.com/customers]  [https://www.anthropic.com/engineering]  [https://www.anthropic.com/events]  [https://claude.com/partners/powered-by-claude]  [https://claude.com/partners/services]  [https://claude.com/programs/startups] 





 [#]  [https://www.anthropic.com/legal/privacy]  [https://www.anthropic.com/responsible-disclosure-policy]  [https://www.anthropic.com/legal/aup]  [https://www.anthropic.com/legal/commercial-terms]  [https://www.anthropic.com/legal/consumer-terms] 












Assistant









Responses are generated using AI and may contain mistakes.
```

### agent-teams

URL: https://code.claude.com/docs/en/agent-teams
Hash: 8fc718d5d9bd

```
Orchestrate teams of Claude Code sessions - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Agents

Orchestrate teams of Claude Code sessions




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Agents


 [/docs/en/sub-agents] 

Create custom subagents


 [/docs/en/agent-teams] 

Run agent teams





Tools and plugins


 [/docs/en/mcp] 

Model Context Protocol (MCP)


 [/docs/en/discover-plugins] 

Discover and install prebuilt plugins


 [/docs/en/plugins] 

Create plugins


 [/docs/en/skills] 

Extend Claude with skills





Automation


 [/docs/en/hooks-guide] 

Automate with hooks


 [/docs/en/channels] 

Push external events to Claude


 [/docs/en/scheduled-tasks] 

Run prompts on a schedule


 [/docs/en/headless] 

Programmatic usage





Troubleshooting


 [/docs/en/troubleshooting] 

Troubleshooting











On this page

 [#when-to-use-agent-teams] When to use agent teams
 [#compare-with-subagents] Compare with subagents
 [#enable-agent-teams] Enable agent teams
 [#start-your-first-agent-team] Start your first agent team
 [#control-your-agent-team] Control your agent team
 [#choose-a-display-mode] Choose a display mode
 [#specify-teammates-and-models] Specify teammates and models
 [#require-plan-approval-for-teammates] Require plan approval for teammates
 [#talk-to-teammates-directly] Talk to teammates directly
 [#assign-and-claim-tasks] Assign and claim tasks
 [#shut-down-teammates] Shut down teammates
 [#clean-up-the-team] Clean up the team
 [#enforce-quality-gates-with-hooks] Enforce quality gates with hooks
 [#how-agent-teams-work] How agent teams work
 [#how-claude-starts-agent-teams] How Claude starts agent teams
 [#architecture] Architecture
 [#use-subagent-definitions-for-teammates] Use subagent definitions for teammates
 [#permissions] Permissions
 [#context-and-communication] Context and communication
 [#token-usage] Token usage
 [#use-case-examples] Use case examples
 [#run-a-parallel-code-review] Run a parallel code review
 [#investigate-with-competing-hypotheses] Investigate with competing hypotheses
 [#best-practices] Best practices
 [#give-teammates-enough-context] Give teammates enough context
 [#choose-an-appropriate-team-size] Choose an appropriate team size
 [#size-tasks-appropriately] Size tasks appropriately
 [#wait-for-teammates-to-finish] Wait for teammates to finish
 [#start-with-research-and-review] Start with research and review
 [#avoid-file-conflicts] Avoid file conflicts
 [#monitor-and-steer] Monitor and steer
 [#troubleshooting] Troubleshooting
 [#teammates-not-appearing] Teammates not appearing
 [#too-many-permission-prompts] Too many permission prompts
 [#teammates-stopping-on-errors] Teammates stopping on errors
 [#lead-shuts-down-before-work-is-done] Lead shuts down before work is done
 [#orphaned-tmux-sessions] Orphaned tmux sessions
 [#limitations] Limitations
 [#next-steps] Next steps





























Agent teams are experimental and disabled by default. Enable them by adding CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS to your  [/docs/en/settings] settings.json or environment. Agent teams have  [#limitations] known limitations around session resumption, task coordination, and shutdown behavior.


Agent teams let you coordinate multiple Claude Code instances working together. One session acts as the team lead, coordinating work, assigning tasks, and synthesizing results. Teammates work independently, each in its own context window, and communicate directly with each other.
Unlike  [/docs/en/sub-agents] subagents, which run within a single session and can only report back to the main agent, you can also interact with individual teammates directly without going through the lead.




Agent teams require Claude Code v2.1.32 or later. Check your version with claude --version.


This page covers:


 [#when-to-use-agent-teams] When to use agent teams, including best use cases and how they compare with subagents

 [#start-your-first-agent-team] Starting a team

 [#control-your-agent-team] Controlling teammates, including display modes, task assignment, and delegation

 [#best-practices] Best practices for parallel work



 [#when-to-use-agent-teams] ​


When to use agent teams

Agent teams are most effective for tasks where parallel exploration adds real value. See  [#use-case-examples] use case examples for full scenarios. The strongest use cases are:


Research and review: multiple teammates can investigate different aspects of a problem simultaneously, then share and challenge each other’s findings

New modules or features: teammates can each own a separate piece without stepping on each other

Debugging with competing hypotheses: teammates test different theories in parallel and converge on the answer faster

Cross-layer coordination: changes that span frontend, backend, and tests, each owned by a different teammate

Agent teams add coordination overhead and use significantly more tokens than a single session. They work best when teammates can operate independently. For sequential tasks, same-file edits, or work with many dependencies, a single session or  [/docs/en/sub-agents] subagents are more effective.


 [#compare-with-subagents] ​


Compare with subagents

Both agent teams and  [/docs/en/sub-agents] subagents let you parallelize work, but they operate differently. Choose based on whether your workers need to communicate with each other:


















SubagentsAgent teams
ContextOwn context window; results return to the callerOwn context window; fully independent
CommunicationReport results back to the main agent onlyTeammates message each other directly
CoordinationMain agent manages all workShared task list with self-coordination
Best forFocused tasks where only the result mattersComplex work requiring discussion and collaboration
Token costLower: results summarized back to main contextHigher: each teammate is a separate Claude instance



Use subagents when you need quick, focused workers that report back. Use agent teams when teammates need to share findings, challenge each other, and coordinate on their own.


 [#enable-agent-teams] ​


Enable agent teams

Agent teams are disabled by default. Enable them by setting the CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS environment variable to 1, either in your shell environment or through  [/docs/en/settings] settings.json:



settings.json











{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}








 [#start-your-first-agent-team] ​


Start your first agent team

After enabling agent teams, tell Claude to create an agent team and describe the task and the team structure you want in natural language. Claude creates the team, spawns teammates, and coordinates work based on your prompt.
This example works well because the three roles are independent and can explore the problem without waiting on each other:











I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles: one
teammate on UX, one on technical architecture, one playing devil's advocate.






From there, Claude creates a team with a  [/docs/en/interactive-mode#task-list] shared task list, spawns teammates for each perspective, has them explore the problem, synthesizes findings, and attempts to  [#clean-up-the-team] clean up the team when finished.
The lead’s terminal lists all teammates and what they’re working on. Use Shift+Down to cycle through teammates and message them directly. After the last teammate, Shift+Down wraps back to the lead.
If you want each teammate in its own split pane, see  [#choose-a-display-mode] Choose a display mode.


 [#control-your-agent-team] ​


Control your agent team

Tell the lead what you want in natural language. It handles team coordination, task assignment, and delegation based on your instructions.


 [#choose-a-display-mode] ​


Choose a display mode

Agent teams support two display modes:


In-process: all teammates run inside your main terminal. Use Shift+Down to cycle through teammates and type to message them directly. Works in any terminal, no extra setup required.

Split panes: each teammate gets its own pane. You can see everyone’s output at once and click into a pane to interact directly. Requires tmux, or iTerm2.





tmux has known limitations on certain operating systems and traditionally works best on macOS. Using tmux -CC in iTerm2 is the suggested entrypoint into tmux.


The default is "auto", which uses split panes if you’re already running inside a tmux session, and in-process otherwise. The "tmux" setting enables split-pane mode and auto-detects whether to use tmux or iTerm2 based on your terminal. To override, set teammateMode in your  [/docs/en/settings#global-config-settings] global config at ~/.claude.json:











{
  "teammateMode": "in-process"
}






To force in-process mode for a single session, pass it as a flag:











claude --teammate-mode in-process






Split-pane mode requires either  [https://github.com/tmux/tmux/wiki] tmux or iTerm2 with the  [https://github.com/mkusaka/it2] it2 CLI. To install manually:


tmux: install through your system’s package manager. See the  [https://github.com/tmux/tmux/wiki/Installing] tmux wiki for platform-specific instructions.

iTerm2: install the  [https://github.com/mkusaka/it2] it2 CLI, then enable the Python API in iTerm2 → Settings → General → Magic → Enable Python API.



 [#specify-teammates-and-models] ​


Specify teammates and models

Claude decides the number of teammates to spawn based on your task, or you can specify exactly what you want:











Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.








 [#require-plan-approval-for-teammates] ​


Require plan approval for teammates

For complex or risky tasks, you can require teammates to plan before implementing. The teammate works in read-only plan mode until the lead approves their approach:











Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.






When a teammate finishes planning, it sends a plan approval request to the lead. The lead reviews the plan and either approves it or rejects it with feedback. If rejected, the teammate stays in plan mode, revises based on the feedback, and resubmits. Once approved, the teammate exits plan mode and begins implementation.
The lead makes approval decisions autonomously. To influence the lead’s judgment, give it criteria in your prompt, such as “only approve plans that include test coverage” or “reject plans that modify the database schema.”


 [#talk-to-teammates-directly] ​


Talk to teammates directly

Each teammate is a full, independent Claude Code session. You can message any teammate directly to give additional instructions, ask follow-up questions, or redirect their approach.


In-process mode: use Shift+Down to cycle through teammates, then type to send them a message. Press Enter to view a teammate’s session, then Escape to interrupt their current turn. Press Ctrl+T to toggle the task list.

Split-pane mode: click into a teammate’s pane to interact with their session directly. Each teammate has a full view of their own terminal.



 [#assign-and-claim-tasks] ​


Assign and claim tasks

The shared task list coordinates work across the team. The lead creates tasks and teammates work through them. Tasks have three states: pending, in progress, and completed. Tasks can also depend on other tasks: a pending task with unresolved dependencies cannot be claimed until those dependencies are completed.
The lead can assign tasks explicitly, or teammates can self-claim:


Lead assigns: tell the lead which task to give to which teammate

Self-claim: after finishing a task, a teammate picks up the next unassigned, unblocked task on its own

Task claiming uses file locking to prevent race conditions when multiple teammates try to claim the same task simultaneously.


 [#shut-down-teammates] ​


Shut down teammates

To gracefully end a teammate’s session:











Ask the researcher teammate to shut down






The lead sends a shutdown request. The teammate can approve, exiting gracefully, or reject with an explanation.


 [#clean-up-the-team] ​


Clean up the team

When you’re done, ask the lead to clean up:











Clean up the team






This removes the shared team resources. When the lead runs cleanup, it checks for active teammates and fails if any are still running, so shut them down first.




Always use the lead to clean up. Teammates should not run cleanup because their team context may not resolve correctly, potentially leaving resources in an inconsistent state.




 [#enforce-quality-gates-with-hooks] ​


Enforce quality gates with hooks

Use  [/docs/en/hooks] hooks to enforce rules when teammates finish work or tasks are created or completed:


 [/docs/en/hooks#teammateidle] TeammateIdle: runs when a teammate is about to go idle. Exit with code 2 to send feedback and keep the teammate working.

 [/docs/en/hooks#taskcreated] TaskCreated: runs when a task is being created. Exit with code 2 to prevent creation and send feedback.

 [/docs/en/hooks#taskcompleted] TaskCompleted: runs when a task is being marked complete. Exit with code 2 to prevent completion and send feedback.



 [#how-agent-teams-work] ​


How agent teams work

This section covers the architecture and mechanics behind agent teams. If you want to start using them, see  [#control-your-agent-team] Control your agent team above.


 [#how-claude-starts-agent-teams] ​


How Claude starts agent teams

There are two ways agent teams get started:


You request a team: give Claude a task that benefits from parallel work and explicitly ask for an agent team. Claude creates one based on your instructions.

Claude proposes a team: if Claude determines your task would benefit from parallel work, it may suggest creating a team. You confirm before it proceeds.

In both cases, you stay in control. Claude won’t create a team without your approval.


 [#architecture] ​


Architecture

An agent team consists of:



ComponentRole
Team leadThe main Claude Code session that creates the team, spawns teammates, and coordinates work
TeammatesSeparate Claude Code instances that each work on assigned tasks
Task listShared list of work items that teammates claim and complete
MailboxMessaging system for communication between agents



See  [#choose-a-display-mode] Choose a display mode for display configuration options. Teammate messages arrive at the lead automatically.
The system manages task dependencies automatically. When a teammate completes a task that other tasks depend on, blocked tasks unblock without manual intervention.
Teams and tasks are stored locally:


Team config: ~/.claude/teams/{team-name}/config.json

Task list: ~/.claude/tasks/{team-name}/

Claude Code generates both of these automatically when you create a team and updates them as teammates join, go idle, or leave. The team config holds runtime state such as session IDs and tmux pane IDs, so don’t edit it by hand or pre-author it: your changes are overwritten on the next state update.
To define reusable teammate roles, use  [#use-subagent-definitions-for-teammates] subagent definitions instead.
The team config contains a members array with each teammate’s name, agent ID, and agent type. Teammates can read this file to discover other team members.
There is no project-level equivalent of the team config. A file like .claude/teams/teams.json in your project directory is not recognized as configuration; Claude treats it as an ordinary file.


 [#use-subagent-definitions-for-teammates] ​


Use subagent definitions for teammates

When spawning a teammate, you can reference a  [/docs/en/sub-agents] subagent type from any  [/docs/en/sub-agents#choose-the-subagent-scope] subagent scope: project, user, plugin, or CLI-defined. The teammate inherits that subagent’s system prompt, tools, and model. This lets you define a role once, such as a security-reviewer or test-runner, and reuse it both as a delegated subagent and as an agent team teammate.
To use a subagent definition, mention it by name when asking Claude to spawn the teammate:











Spawn a teammate using the security-reviewer agent type to audit the auth module.








 [#permissions] ​


Permissions

Teammates start with the lead’s permission settings. If the lead runs with --dangerously-skip-permissions, all teammates do too. After spawning, you can change individual teammate modes, but you can’t set per-teammate modes at spawn time.


 [#context-and-communication] ​


Context and communication

Each teammate has its own context window. When spawned, a teammate loads the same project context as a regular session: CLAUDE.md, MCP servers, and skills. It also receives the spawn prompt from the lead. The lead’s conversation history does not carry over.
How teammates share information:


Automatic message delivery: when teammates send messages, they’re delivered automatically to recipients. The lead doesn’t need to poll for updates.

Idle notifications: when a teammate finishes and stops, they automatically notify the lead.

Shared task list: all agents can see task status and claim available work.

Teammate messaging:


message: send a message to one specific teammate

broadcast: send to all teammates simultaneously. Use sparingly, as costs scale with team size.



 [#token-usage] ​


Token usage

Agent teams use significantly more tokens than a single session. Each teammate has its own context window, and token usage scales with the number of active teammates. For research, review, and new feature work, the extra tokens are usually worthwhile. For routine tasks, a single session is more cost-effective. See  [/docs/en/costs#agent-team-token-costs] agent team token costs for usage guidance.


 [#use-case-examples] ​


Use case examples

These examples show how agent teams handle tasks where parallel exploration adds value.


 [#run-a-parallel-code-review] ​


Run a parallel code review

A single reviewer tends to gravitate toward one type of issue at a time. Splitting review criteria into independent domains means security, performance, and test coverage all get thorough attention simultaneously. The prompt assigns each teammate a distinct lens so they don’t overlap:











Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.






Each reviewer works from the same PR but applies a different filter. The lead synthesizes findings across all three after they finish.


 [#investigate-with-competing-hypotheses] ​


Investigate with competing hypotheses

When the root cause is unclear, a single agent tends to find one plausible explanation and stop looking. The prompt fights this by making teammates explicitly adversarial: each one’s job is not only to investigate its own theory but to challenge the others’.











Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.






The debate structure is the key mechanism here. Sequential investigation suffers from anchoring: once one theory is explored, subsequent investigation is biased toward it.
With multiple independent investigators actively trying to disprove each other, the theory that survives is much more likely to be the actual root cause.


 [#best-practices] ​


Best practices



 [#give-teammates-enough-context] ​


Give teammates enough context

Teammates load project context automatically, including CLAUDE.md, MCP servers, and skills, but they don’t inherit the lead’s conversation history. See  [#context-and-communication] Context and communication for details. Include task-specific details in the spawn prompt:











Spawn a security reviewer teammate with the prompt: "Review the authentication module
at src/auth/ for security vulnerabilities. Focus on token handling, session
management, and input validation. The app uses JWT tokens stored in
httpOnly cookies. Report any issues with severity ratings."








 [#choose-an-appropriate-team-size] ​


Choose an appropriate team size

There’s no hard limit on the number of teammates, but practical constraints apply:


Token costs scale linearly: each teammate has its own context window and consumes tokens independently. See  [/docs/en/costs#agent-team-token-costs] agent team token costs for details.

Coordination overhead increases: more teammates means more communication, task coordination, and potential for conflicts

Diminishing returns: beyond a certain point, additional teammates don’t speed up work proportionally

Start with 3-5 teammates for most workflows. This balances parallel work with manageable coordination. The examples in this guide use 3-5 teammates because that range works well across different task types.
Having 5-6  [/docs/en/agent-teams#architecture] tasks per teammate keeps everyone productive without excessive context switching. If you have 15 independent tasks, 3 teammates is a good starting point.
Scale up only when the work genuinely benefits from having teammates work simultaneously. Three focused teammates often outperform five scattered ones.


 [#size-tasks-appropriately] ​


Size tasks appropriately



Too small: coordination overhead exceeds the benefit

Too large: teammates work too long without check-ins, increasing risk of wasted effort

Just right: self-contained units that produce a clear deliverable, such as a function, a test file, or a review





The lead breaks work into tasks and assigns them to teammates automatically. If it isn’t creating enough tasks, ask it to split the work into smaller pieces. Having 5-6 tasks per teammate keeps everyone productive and lets the lead reassign work if someone gets stuck.




 [#wait-for-teammates-to-finish] ​


Wait for teammates to finish

Sometimes the lead starts implementing tasks itself instead of waiting for teammates. If you notice this:











Wait for your teammates to complete their tasks before proceeding








 [#start-with-research-and-review] ​


Start with research and review

If you’re new to agent teams, start with tasks that have clear boundaries and don’t require writing code: reviewing a PR, researching a library, or investigating a bug. These tasks show the value of parallel exploration without the coordination challenges that come with parallel implementation.


 [#avoid-file-conflicts] ​


Avoid file conflicts

Two teammates editing the same file leads to overwrites. Break the work so each teammate owns a different set of files.


 [#monitor-and-steer] ​


Monitor and steer

Check in on teammates’ progress, redirect approaches that aren’t working, and synthesize findings as they come in. Letting a team run unattended for too long increases the risk of wasted effort.


 [#troubleshooting] ​


Troubleshooting



 [#teammates-not-appearing] ​


Teammates not appearing

If teammates aren’t appearing after you ask Claude to create a team:


In in-process mode, teammates may already be running but not visible. Press Shift+Down to cycle through active teammates.

Check that the task you gave Claude was complex enough to warrant a team. Claude decides whether to spawn teammates based on the task.

If you explicitly requested split panes, ensure tmux is installed and available in your PATH:











which tmux








For iTerm2, verify the it2 CLI is installed and the Python API is enabled in iTerm2 preferences.



 [#too-many-permission-prompts] ​


Too many permission prompts

Teammate permission requests bubble up to the lead, which can create friction. Pre-approve common operations in your  [/docs/en/permissions] permission settings before spawning teammates to reduce interruptions.


 [#teammates-stopping-on-errors] ​


Teammates stopping on errors

Teammates may stop after encountering errors instead of recovering. Check their output using Shift+Down in in-process mode or by clicking the pane in split mode, then either:


Give them additional instructions directly

Spawn a replacement teammate to continue the work



 [#lead-shuts-down-before-work-is-done] ​


Lead shuts down before work is done

The lead may decide the team is finished before all tasks are actually complete. If this happens, tell it to keep going. You can also tell the lead to wait for teammates to finish before proceeding if it starts doing work instead of delegating.


 [#orphaned-tmux-sessions] ​


Orphaned tmux sessions

If a tmux session persists after the team ends, it may not have been fully cleaned up. List sessions and kill the one created by the team:











tmux ls
tmux kill-session -t <session-name>








 [#limitations] ​


Limitations

Agent teams are experimental. Current limitations to be aware of:


No session resumption with in-process teammates: /resume and /rewind do not restore in-process teammates. After resuming a session, the lead may attempt to message teammates that no longer exist. If this happens, tell the lead to spawn new teammates.

Task status can lag: teammates sometimes fail to mark tasks as completed, which blocks dependent tasks. If a task appears stuck, check whether the work is actually done and update the task status manually or tell the lead to nudge the teammate.

Shutdown can be slow: teammates finish their current request or tool call before shutting down, which can take time.

One team per session: a lead can only manage one team at a time. Clean up the current team before starting a new one.

No nested teams: teammates cannot spawn their own teams or teammates. Only the lead can manage the team.

Lead is fixed: the session that creates the team is the lead for its lifetime. You can’t promote a teammate to lead or transfer leadership.

Permissions set at spawn: all teammates start with the lead’s permission mode. You can change individual teammate modes after spawning, but you can’t set per-teammate modes at spawn time.

Split panes require tmux or iTerm2: the default in-process mode works in any terminal. Split-pane mode isn’t supported in VS Code’s integrated terminal, Windows Terminal, or Ghostty.





CLAUDE.md works normally: teammates read CLAUDE.md files from their working directory. Use this to provide project-specific guidance to all teammates.




 [#next-steps] ​


Next steps

Explore related approaches for parallel work and delegation:


Lightweight delegation:  [/docs/en/sub-agents] subagents spawn helper agents for research or verification within your session, better for tasks that don’t need inter-agent coordination

Manual parallel sessions:  [/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees] Git worktrees let you run multiple Claude Code sessions yourself without automated team coordination

Compare approaches: see the  [/docs/en/features-overview#compare-similar-features] subagent vs agent team comparison for a side-by-side breakdown




Was this page helpful?


YesNo






 [/docs/en/sub-agents] Create custom subagents [/docs/en/mcp] Model Context Protocol (MCP)





⌘I











 [/docs/en/overview] 
 [https://x.com/AnthropicAI]  [https://www.linkedin.com/company/anthropicresearch] 






 [https://www.anthropic.com/company]  [https://www.anthropic.com/careers]  [https://www.anthropic.com/economic-futures]  [https://www.anthropic.com/research]  [https://www.anthropic.com/news]  [https://trust.anthropic.com/]  [https://www.anthropic.com/transparency] 





 [https://www.anthropic.com/supported-countries]  [https://status.anthropic.com/]  [https://support.claude.com/] 





 [https://www.anthropic.com/learn]  [https://claude.com/partners/mcp]  [https://www.claude.com/customers]  [https://www.anthropic.com/engineering]  [https://www.anthropic.com/events]  [https://claude.com/partners/powered-by-claude]  [https://claude.com/partners/services]  [https://claude.com/programs/startups] 





 [#]  [https://www.anthropic.com/legal/privacy]  [https://www.anthropic.com/responsible-disclosure-policy]  [https://www.anthropic.com/legal/aup]  [https://www.anthropic.com/legal/commercial-terms]  [https://www.anthropic.com/legal/consumer-terms] 












Assistant









Responses are generated using AI and may contain mistakes.
```

### plugins

URL: https://code.claude.com/docs/en/plugins
Hash: b092cb8b51a9

```
Create plugins - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Tools and plugins

Create plugins




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Agents


 [/docs/en/sub-agents] 

Create custom subagents


 [/docs/en/agent-teams] 

Run agent teams





Tools and plugins


 [/docs/en/mcp] 

Model Context Protocol (MCP)


 [/docs/en/discover-plugins] 

Discover and install prebuilt plugins


 [/docs/en/plugins] 

Create plugins


 [/docs/en/skills] 

Extend Claude with skills





Automation


 [/docs/en/hooks-guide] 

Automate with hooks


 [/docs/en/channels] 

Push external events to Claude


 [/docs/en/scheduled-tasks] 

Run prompts on a schedule


 [/docs/en/headless] 

Programmatic usage





Troubleshooting


 [/docs/en/troubleshooting] 

Troubleshooting











On this page

 [#when-to-use-plugins-vs-standalone-configuration] When to use plugins vs standalone configuration
 [#quickstart] Quickstart
 [#prerequisites] Prerequisites
 [#create-your-first-plugin] Create your first plugin
 [#plugin-structure-overview] Plugin structure overview
 [#develop-more-complex-plugins] Develop more complex plugins
 [#add-skills-to-your-plugin] Add Skills to your plugin
 [#add-lsp-servers-to-your-plugin] Add LSP servers to your plugin
 [#ship-default-settings-with-your-plugin] Ship default settings with your plugin
 [#organize-complex-plugins] Organize complex plugins
 [#test-your-plugins-locally] Test your plugins locally
 [#debug-plugin-issues] Debug plugin issues
 [#share-your-plugins] Share your plugins
 [#submit-your-plugin-to-the-official-marketplace] Submit your plugin to the official marketplace
 [#convert-existing-configurations-to-plugins] Convert existing configurations to plugins
 [#migration-steps] Migration steps
 [#what-changes-when-migrating] What changes when migrating
 [#next-steps] Next steps
 [#for-plugin-users] For plugin users
 [#for-plugin-developers] For plugin developers

























Plugins let you extend Claude Code with custom functionality that can be shared across projects and teams. This guide covers creating your own plugins with skills, agents, hooks, and MCP servers.
Looking to install existing plugins? See  [/docs/en/discover-plugins] Discover and install plugins. For complete technical specifications, see  [/docs/en/plugins-reference] Plugins reference.


 [#when-to-use-plugins-vs-standalone-configuration] ​


When to use plugins vs standalone configuration

Claude Code supports two ways to add custom skills, agents, and hooks:



ApproachSkill namesBest for
Standalone (.claude/ directory)/helloPersonal workflows, project-specific customizations, quick experiments
Plugins (directories with .claude-plugin/plugin.json)/plugin-name:helloSharing with teammates, distributing to community, versioned releases, reusable across projects



Use standalone configuration when:


You’re customizing Claude Code for a single project

The configuration is personal and doesn’t need to be shared

You’re experimenting with skills or hooks before packaging them

You want short skill names like /hello or /deploy

Use plugins when:


You want to share functionality with your team or community

You need the same skills/agents across multiple projects

You want version control and easy updates for your extensions

You’re distributing through a marketplace

You’re okay with namespaced skills like /my-plugin:hello (namespacing prevents conflicts between plugins)





Start with standalone configuration in .claude/ for quick iteration, then  [#convert-existing-configurations-to-plugins] convert to a plugin when you’re ready to share.




 [#quickstart] ​


Quickstart

This quickstart walks you through creating a plugin with a custom skill. You’ll create a manifest (the configuration file that defines your plugin), add a skill, and test it locally using the --plugin-dir flag.


 [#prerequisites] ​


Prerequisites



Claude Code  [/docs/en/quickstart#step-1-install-claude-code] installed and authenticated

Claude Code version 1.0.33 or later (run claude --version to check)





If you don’t see the /plugin command, update Claude Code to the latest version. See  [/docs/en/troubleshooting] Troubleshooting for upgrade instructions.




 [#create-your-first-plugin] ​


Create your first plugin








1

 [#] 






Create the plugin directory

Every plugin lives in its own directory containing a manifest and your skills, agents, or hooks. Create one now:










mkdir my-first-plugin














2

 [#] 






Create the plugin manifest

The manifest file at .claude-plugin/plugin.json defines your plugin’s identity: its name, description, and version. Claude Code uses this metadata to display your plugin in the plugin manager.Create the .claude-plugin directory inside your plugin folder:










mkdir my-first-plugin/.claude-plugin





Then create my-first-plugin/.claude-plugin/plugin.json with this content:


my-first-plugin/.claude-plugin/plugin.json











{
"name": "my-first-plugin",
"description": "A greeting plugin to learn the basics",
"version": "1.0.0",
"author": {
"name": "Your Name"
}
}








FieldPurpose
nameUnique identifier and skill namespace. Skills are prefixed with this (e.g., /my-first-plugin:hello).
descriptionShown in the plugin manager when browsing or installing plugins.
versionTrack releases using  [/docs/en/plugins-reference#version-management] semantic versioning.
authorOptional. Helpful for attribution.


For additional fields like homepage, repository, and license, see the  [/docs/en/plugins-reference#plugin-manifest-schema] full manifest schema.








3

 [#] 






Add a skill

Skills live in the skills/ directory. Each skill is a folder containing a SKILL.md file. The folder name becomes the skill name, prefixed with the plugin’s namespace (hello/ in a plugin named my-first-plugin creates /my-first-plugin:hello).Create a skill directory in your plugin folder:










mkdir -p my-first-plugin/skills/hello





Then create my-first-plugin/skills/hello/SKILL.md with this content:


my-first-plugin/skills/hello/SKILL.md











---
description: Greet the user with a friendly message
disable-model-invocation: true
---

Greet the user warmly and ask how you can help them today.














4

 [#] 






Test your plugin

Run Claude Code with the --plugin-dir flag to load your plugin:










claude --plugin-dir ./my-first-plugin





Once Claude Code starts, try your new skill:










/my-first-plugin:hello





You’ll see Claude respond with a greeting. Run /help to see your skill listed under the plugin namespace.



Why namespacing? Plugin skills are always namespaced (like /my-first-plugin:hello) to prevent conflicts when multiple plugins have skills with the same name.To change the namespace prefix, update the name field in plugin.json.










5

 [#] 






Add skill arguments

Make your skill dynamic by accepting user input. The $ARGUMENTS placeholder captures any text the user provides after the skill name.Update your SKILL.md file:


my-first-plugin/skills/hello/SKILL.md











---
description: Greet the user with a personalized message
---

# Hello Skill

Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.





Run /reload-plugins to pick up the changes, then try the skill with your name:










/my-first-plugin:hello Alex





Claude will greet you by name. For more on passing arguments to skills, see  [/docs/en/skills#pass-arguments-to-skills] Skills.




You’ve successfully created and tested a plugin with these key components:


Plugin manifest (.claude-plugin/plugin.json): describes your plugin’s metadata

Skills directory (skills/): contains your custom skills

Skill arguments ($ARGUMENTS): captures user input for dynamic behavior





The --plugin-dir flag is useful for development and testing. When you’re ready to share your plugin with others, see  [/docs/en/plugin-marketplaces] Create and distribute a plugin marketplace.




 [#plugin-structure-overview] ​


Plugin structure overview

You’ve created a plugin with a skill, but plugins can include much more: custom agents, hooks, MCP servers, and LSP servers.




Common mistake: Don’t put commands/, agents/, skills/, or hooks/ inside the .claude-plugin/ directory. Only plugin.json goes inside .claude-plugin/. All other directories must be at the plugin root level.





DirectoryLocationPurpose
.claude-plugin/Plugin rootContains plugin.json manifest (optional if components use default locations)
commands/Plugin rootSkills as Markdown files
agents/Plugin rootCustom agent definitions
skills/Plugin rootAgent Skills with SKILL.md files
hooks/Plugin rootEvent handlers in hooks.json
.mcp.jsonPlugin rootMCP server configurations
.lsp.jsonPlugin rootLSP server configurations for code intelligence
settings.jsonPlugin rootDefault  [/docs/en/settings] settings applied when the plugin is enabled







Next steps: Ready to add more features? Jump to  [#develop-more-complex-plugins] Develop more complex plugins to add agents, hooks, MCP servers, and LSP servers. For complete technical specifications of all plugin components, see  [/docs/en/plugins-reference] Plugins reference.




 [#develop-more-complex-plugins] ​


Develop more complex plugins

Once you’re comfortable with basic plugins, you can create more sophisticated extensions.


 [#add-skills-to-your-plugin] ​


Add Skills to your plugin

Plugins can include  [/docs/en/skills] Agent Skills to extend Claude’s capabilities. Skills are model-invoked: Claude automatically uses them based on the task context.
Add a skills/ directory at your plugin root with Skill folders containing SKILL.md files:











my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md






Each SKILL.md needs frontmatter with name and description fields, followed by instructions:











---
name: code-review
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage






After installing the plugin, run /reload-plugins to load the Skills. For complete Skill authoring guidance including progressive disclosure and tool restrictions, see  [/docs/en/skills] Agent Skills.


 [#add-lsp-servers-to-your-plugin] ​


Add LSP servers to your plugin





For common languages like TypeScript, Python, and Rust, install the pre-built LSP plugins from the official marketplace. Create custom LSP plugins only when you need support for languages not already covered.


LSP (Language Server Protocol) plugins give Claude real-time code intelligence. If you need to support a language that doesn’t have an official LSP plugin, you can create your own by adding an .lsp.json file to your plugin:



.lsp.json











{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}






Users installing your plugin must have the language server binary installed on their machine.
For complete LSP configuration options, see  [/docs/en/plugins-reference#lsp-servers] LSP servers.


 [#ship-default-settings-with-your-plugin] ​


Ship default settings with your plugin

Plugins can include a settings.json file at the plugin root to apply default configuration when the plugin is enabled. Currently, only the agent key is supported.
Setting agent activates one of the plugin’s  [/docs/en/sub-agents] custom agents as the main thread, applying its system prompt, tool restrictions, and model. This lets a plugin change how Claude Code behaves by default when enabled.



settings.json











{
  "agent": "security-reviewer"
}






This example activates the security-reviewer agent defined in the plugin’s agents/ directory. Settings from settings.json take priority over settings declared in plugin.json. Unknown keys are silently ignored.


 [#organize-complex-plugins] ​


Organize complex plugins

For plugins with many components, organize your directory structure by functionality. For complete directory layouts and organization patterns, see  [/docs/en/plugins-reference#plugin-directory-structure] Plugin directory structure.


 [#test-your-plugins-locally] ​


Test your plugins locally

Use the --plugin-dir flag to test plugins during development. This loads your plugin directly without requiring installation.











claude --plugin-dir ./my-plugin






When a --plugin-dir plugin has the same name as an installed marketplace plugin, the local copy takes precedence for that session. This lets you test changes to a plugin you already have installed without uninstalling it first. Marketplace plugins force-enabled by managed settings are the only exception and cannot be overridden.
As you make changes to your plugin, run /reload-plugins to pick up the updates without restarting. This reloads plugins, skills, agents, hooks, plugin MCP servers, and plugin LSP servers. Test your plugin components:


Try your skills with /plugin-name:skill-name

Check that agents appear in /agents

Verify hooks work as expected





You can load multiple plugins at once by specifying the flag multiple times:










claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two










 [#debug-plugin-issues] ​


Debug plugin issues

If your plugin isn’t working as expected:


Check the structure: Ensure your directories are at the plugin root, not inside .claude-plugin/

Test components individually: Check each command, agent, and hook separately

Use validation and debugging tools: See  [/docs/en/plugins-reference#debugging-and-development-tools] Debugging and development tools for CLI commands and troubleshooting techniques



 [#share-your-plugins] ​


Share your plugins

When your plugin is ready to share:


Add documentation: Include a README.md with installation and usage instructions

Version your plugin: Use  [/docs/en/plugins-reference#version-management] semantic versioning in your plugin.json

Create or use a marketplace: Distribute through  [/docs/en/plugin-marketplaces] plugin marketplaces for installation

Test with others: Have team members test the plugin before wider distribution

Once your plugin is in a marketplace, others can install it using the instructions in  [/docs/en/discover-plugins] Discover and install plugins.


 [#submit-your-plugin-to-the-official-marketplace] ​


Submit your plugin to the official marketplace

To submit a plugin to the official Anthropic marketplace, use one of the in-app submission forms:


Claude.ai:  [https://claude.ai/settings/plugins/submit] claude.ai/settings/plugins/submit

Console:  [https://platform.claude.com/plugins/submit] platform.claude.com/plugins/submit





For complete technical specifications, debugging techniques, and distribution strategies, see  [/docs/en/plugins-reference] Plugins reference.




 [#convert-existing-configurations-to-plugins] ​


Convert existing configurations to plugins

If you already have skills or hooks in your .claude/ directory, you can convert them into a plugin for easier sharing and distribution.


 [#migration-steps] ​


Migration steps








1

 [#] 






Create the plugin structure

Create a new plugin directory:










mkdir -p my-plugin/.claude-plugin





Create the manifest file at my-plugin/.claude-plugin/plugin.json:


my-plugin/.claude-plugin/plugin.json











{
  "name": "my-plugin",
  "description": "Migrated from standalone configuration",
  "version": "1.0.0"
}














2

 [#] 






Copy your existing files

Copy your existing configurations to the plugin directory:










# Copy commands
cp -r .claude/commands my-plugin/

# Copy agents (if any)
cp -r .claude/agents my-plugin/

# Copy skills (if any)
cp -r .claude/skills my-plugin/














3

 [#] 






Migrate hooks

If you have hooks in your settings, create a hooks directory:










mkdir my-plugin/hooks





Create my-plugin/hooks/hooks.json with your hooks configuration. Copy the hooks object from your .claude/settings.json or settings.local.json, since the format is the same. The command receives hook input as JSON on stdin, so use jq to extract the file path:


my-plugin/hooks/hooks.json











{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
      }
    ]
  }
}














4

 [#] 






Test your migrated plugin

Load your plugin to verify everything works:










claude --plugin-dir ./my-plugin





Test each component: run your commands, check agents appear in /agents, and verify hooks trigger correctly.






 [#what-changes-when-migrating] ​


What changes when migrating




Standalone (.claude/)Plugin
Only available in one projectCan be shared via marketplaces
Files in .claude/commands/Files in plugin-name/commands/
Hooks in settings.jsonHooks in hooks/hooks.json
Must manually copy to shareInstall with /plugin install







After migrating, you can remove the original files from .claude/ to avoid duplicates. The plugin version will take precedence when loaded.




 [#next-steps] ​


Next steps

Now that you understand Claude Code’s plugin system, here are suggested paths for different goals:


 [#for-plugin-users] ​


For plugin users



 [/docs/en/discover-plugins] Discover and install plugins: browse marketplaces and install plugins

 [/docs/en/discover-plugins#configure-team-marketplaces] Configure team marketplaces: set up repository-level plugins for your team



 [#for-plugin-developers] ​


For plugin developers



 [/docs/en/plugin-marketplaces] Create and distribute a marketplace: package and share your plugins

 [/docs/en/plugins-reference] Plugins reference: complete technical specifications

Dive deeper into specific plugin components:


 [/docs/en/skills] Skills: skill development details

 [/docs/en/sub-agents] Subagents: agent configuration and capabilities

 [/docs/en/hooks] Hooks: event handling and automation

 [/docs/en/mcp] MCP: external tool integration






Was this page helpful?


YesNo






 [/docs/en/discover-plugins] Discover and install prebuilt plugins [/docs/en/skills] Extend Claude with skills





⌘I











 [/docs/en/overview] 
 [https://x.com/AnthropicAI]  [https://www.linkedin.com/company/anthropicresearch] 






 [https://www.anthropic.com/company]  [https://www.anthropic.com/careers]  [https://www.anthropic.com/economic-futures]  [https://www.anthropic.com/research]  [https://www.anthropic.com/news]  [https://trust.anthropic.com/]  [https://www.anthropic.com/transparency] 





 [https://www.anthropic.com/supported-countries]  [https://status.anthropic.com/]  [https://support.claude.com/] 





 [https://www.anthropic.com/learn]  [https://claude.com/partners/mcp]  [https://www.claude.com/customers]  [https://www.anthropic.com/engineering]  [https://www.anthropic.com/events]  [https://claude.com/partners/powered-by-claude]  [https://claude.com/partners/services]  [https://claude.com/programs/startups] 





 [#]  [https://www.anthropic.com/legal/privacy]  [https://www.anthropic.com/responsible-disclosure-policy]  [https://www.anthropic.com/legal/aup]  [https://www.anthropic.com/legal/commercial-terms]  [https://www.anthropic.com/legal/consumer-terms] 












Assistant









Responses are generated using AI and may contain mistakes.
```

### memory

URL: https://code.claude.com/docs/en/memory
Hash: 5c7d95fc48b2

```
How Claude remembers your project - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Use Claude Code

How Claude remembers your project




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Getting started


 [/docs/en/overview] 

Overview


 [/docs/en/quickstart] 

Quickstart


 [/docs/en/changelog] 

Changelog





Core concepts


 [/docs/en/how-claude-code-works] 

How Claude Code works


 [/docs/en/features-overview] 

Extend Claude Code


 [/docs/en/claude-directory] 

Explore the .claude directory


 [/docs/en/context-window] 

Explore the context window





Use Claude Code


 [/docs/en/memory] 

Store instructions and memories


 [/docs/en/permission-modes] 

Permission modes


 [/docs/en/common-workflows] 

Common workflows


 [/docs/en/best-practices] 

Best practices





Platforms and integrations


 [/docs/en/platforms] 

Overview


 [/docs/en/remote-control] 

Remote Control



Claude Code on the web


Claude Code on desktop

 [/docs/en/chrome] 

Chrome extension (beta)


 [/docs/en/computer-use] 

Computer use (preview)


 [/docs/en/vs-code] 

Visual Studio Code


 [/docs/en/jetbrains] 

JetBrains IDEs



Code review & CI/CD

 [/docs/en/slack] 

Claude Code in Slack











On this page

 [#claude-md-vs-auto-memory] CLAUDE.md vs auto memory
 [#claude-md-files] CLAUDE.md files
 [#choose-where-to-put-claude-md-files] Choose where to put CLAUDE.md files
 [#set-up-a-project-claude-md] Set up a project CLAUDE.md
 [#write-effective-instructions] Write effective instructions
 [#import-additional-files] Import additional files
 [#agents-md] AGENTS.md
 [#how-claude-md-files-load] How CLAUDE.md files load
 [#load-from-additional-directories] Load from additional directories
 [#organize-rules-with-claude%2Frules%2F] Organize rules with .claude/rules/
 [#set-up-rules] Set up rules
 [#path-specific-rules] Path-specific rules
 [#share-rules-across-projects-with-symlinks] Share rules across projects with symlinks
 [#user-level-rules] User-level rules
 [#manage-claude-md-for-large-teams] Manage CLAUDE.md for large teams
 [#deploy-organization-wide-claude-md] Deploy organization-wide CLAUDE.md
 [#exclude-specific-claude-md-files] Exclude specific CLAUDE.md files
 [#auto-memory] Auto memory
 [#enable-or-disable-auto-memory] Enable or disable auto memory
 [#storage-location] Storage location
 [#how-it-works] How it works
 [#audit-and-edit-your-memory] Audit and edit your memory
 [#view-and-edit-with-%2Fmemory] View and edit with /memory
 [#troubleshoot-memory-issues] Troubleshoot memory issues
 [#claude-isn%E2%80%99t-following-my-claude-md] Claude isn’t following my CLAUDE.md
 [#i-don%E2%80%99t-know-what-auto-memory-saved] I don’t know what auto memory saved
 [#my-claude-md-is-too-large] My CLAUDE.md is too large
 [#instructions-seem-lost-after-%2Fcompact] Instructions seem lost after /compact
 [#related-resources] Related resources

























Each Claude Code session begins with a fresh context window. Two mechanisms carry knowledge across sessions:


CLAUDE.md files: instructions you write to give Claude persistent context

Auto memory: notes Claude writes itself based on your corrections and preferences

This page covers how to:


 [#claude-md-files] Write and organize CLAUDE.md files

 [#organize-rules-with-claude/rules/] Scope rules to specific file types with .claude/rules/

 [#auto-memory] Configure auto memory so Claude takes notes automatically

 [#troubleshoot-memory-issues] Troubleshoot when instructions aren’t being followed



 [#claude-md-vs-auto-memory] ​


CLAUDE.md vs auto memory

Claude Code has two complementary memory systems. Both are loaded at the start of every conversation. Claude treats them as context, not enforced configuration. The more specific and concise your instructions, the more consistently Claude follows them.



CLAUDE.md filesAuto memory
Who writes itYouClaude
What it containsInstructions and rulesLearnings and patterns
ScopeProject, user, or orgPer working tree
Loaded intoEvery sessionEvery session (first 200 lines or 25KB)
Use forCoding standards, workflows, project architectureBuild commands, debugging insights, preferences Claude discovers



Use CLAUDE.md files when you want to guide Claude’s behavior. Auto memory lets Claude learn from your corrections without manual effort.
Subagents can also maintain their own auto memory. See  [/docs/en/sub-agents#enable-persistent-memory] subagent configuration for details.


 [#claude-md-files] ​


CLAUDE.md files

CLAUDE.md files are markdown files that give Claude persistent instructions for a project, your personal workflow, or your entire organization. You write these files in plain text; Claude reads them at the start of every session.


 [#choose-where-to-put-claude-md-files] ​


Choose where to put CLAUDE.md files

CLAUDE.md files can live in several locations, each with a different scope. More specific locations take precedence over broader ones.



ScopeLocationPurposeUse case examplesShared with
Managed policy• macOS: /Library/Application Support/ClaudeCode/CLAUDE.md
• Linux and WSL: /etc/claude-code/CLAUDE.md
• Windows: C:\Program Files\ClaudeCode\CLAUDE.mdOrganization-wide instructions managed by IT/DevOpsCompany coding standards, security policies, compliance requirementsAll users in organization
Project instructions./CLAUDE.md or ./.claude/CLAUDE.mdTeam-shared instructions for the projectProject architecture, coding standards, common workflowsTeam members via source control
User instructions~/.claude/CLAUDE.mdPersonal preferences for all projectsCode styling preferences, personal tooling shortcutsJust you (all projects)



CLAUDE.md files in the directory hierarchy above the working directory are loaded in full at launch. CLAUDE.md files in subdirectories load on demand when Claude reads files in those directories. See  [#how-claude-md-files-load] How CLAUDE.md files load for the full resolution order.
For large projects, you can break instructions into topic-specific files using  [#organize-rules-with-claude/rules/] project rules. Rules let you scope instructions to specific file types or subdirectories.


 [#set-up-a-project-claude-md] ​


Set up a project CLAUDE.md

A project CLAUDE.md can be stored in either ./CLAUDE.md or ./.claude/CLAUDE.md. Create this file and add instructions that apply to anyone working on the project: build and test commands, coding standards, architectural decisions, naming conventions, and common workflows. These instructions are shared with your team through version control, so focus on project-level standards rather than personal preferences.




Run /init to generate a starting CLAUDE.md automatically. Claude analyzes your codebase and creates a file with build commands, test instructions, and project conventions it discovers. If a CLAUDE.md already exists, /init suggests improvements rather than overwriting it. Refine from there with instructions Claude wouldn’t discover on its own.Set CLAUDE_CODE_NEW_INIT=true to enable an interactive multi-phase flow. /init asks which artifacts to set up: CLAUDE.md files, skills, and hooks. It then explores your codebase with a subagent, fills in gaps via follow-up questions, and presents a reviewable proposal before writing any files.




 [#write-effective-instructions] ​


Write effective instructions

CLAUDE.md files are loaded into the context window at the start of every session, consuming tokens alongside your conversation. The  [/docs/en/context-window] context window visualization shows where CLAUDE.md loads relative to the rest of the startup context. Because they’re context rather than enforced configuration, how you write instructions affects how reliably Claude follows them. Specific, concise, well-structured instructions work best.
Size: target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence. If your instructions are growing large, split them using  [#import-additional-files] imports or  [#organize-rules-with-claude/rules/] .claude/rules/ files.
Structure: use markdown headers and bullets to group related instructions. Claude scans structure the same way readers do: organized sections are easier to follow than dense paragraphs.
Specificity: write instructions that are concrete enough to verify. For example:


“Use 2-space indentation” instead of “Format code properly”

“Run npm test before committing” instead of “Test your changes”

“API handlers live in src/api/handlers/” instead of “Keep files organized”

Consistency: if two rules contradict each other, Claude may pick one arbitrarily. Review your CLAUDE.md files, nested CLAUDE.md files in subdirectories, and  [#organize-rules-with-claude/rules/] .claude/rules/ periodically to remove outdated or conflicting instructions. In monorepos, use  [#exclude-specific-claude-md-files] claudeMdExcludes to skip CLAUDE.md files from other teams that aren’t relevant to your work.


 [#import-additional-files] ​


Import additional files

CLAUDE.md files can import additional files using @path/to/import syntax. Imported files are expanded and loaded into context at launch alongside the CLAUDE.md that references them.
Both relative and absolute paths are allowed. Relative paths resolve relative to the file containing the import, not the working directory. Imported files can recursively import other files, with a maximum depth of five hops.
To pull in a README, package.json, and a workflow guide, reference them with @ syntax anywhere in your CLAUDE.md:











See @README for project overview and @package.json for available npm commands for this project.

# Additional Instructions
- git workflow @docs/git-instructions.md






For personal preferences you don’t want to check in, import a file from your home directory. The import goes in the shared CLAUDE.md, but the file it points to stays on your machine:











# Individual Preferences
- @~/.claude/my-project-instructions.md










The first time Claude Code encounters external imports in a project, it shows an approval dialog listing the files. If you decline, the imports stay disabled and the dialog does not appear again.


For a more structured approach to organizing instructions, see  [#organize-rules-with-claude/rules/] .claude/rules/.


 [#agents-md] ​


AGENTS.md

Claude Code reads CLAUDE.md, not AGENTS.md. If your repository already uses AGENTS.md for other coding agents, create a CLAUDE.md that imports it so both tools read the same instructions without duplicating them. You can also add Claude-specific instructions below the import. Claude loads the imported file at session start, then appends the rest:



CLAUDE.md











@AGENTS.md

## Claude Code

Use plan mode for changes under `src/billing/`.








 [#how-claude-md-files-load] ​


How CLAUDE.md files load

Claude Code reads CLAUDE.md files by walking up the directory tree from your current working directory, checking each directory along the way. This means if you run Claude Code in foo/bar/, it loads instructions from both foo/bar/CLAUDE.md and foo/CLAUDE.md.
Claude also discovers CLAUDE.md files in subdirectories under your current working directory. Instead of loading them at launch, they are included when Claude reads files in those subdirectories.
If you work in a large monorepo where other teams’ CLAUDE.md files get picked up, use  [#exclude-specific-claude-md-files] claudeMdExcludes to skip them.
Block-level HTML comments (<!-- maintainer notes -->) in CLAUDE.md files are stripped before the content is injected into Claude’s context. Use them to leave notes for human maintainers without spending context tokens on them. Comments inside code blocks are preserved. When you open a CLAUDE.md file directly with the Read tool, comments remain visible.


 [#load-from-additional-directories] ​


Load from additional directories

The --add-dir flag gives Claude access to additional directories outside your main working directory. By default, CLAUDE.md files from these directories are not loaded.
To also load CLAUDE.md files from additional directories, including CLAUDE.md, .claude/CLAUDE.md, and .claude/rules/*.md, set the CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD environment variable:











CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config








 [#organize-rules-with-claude/rules/] ​


Organize rules with .claude/rules/

For larger projects, you can organize instructions into multiple files using the .claude/rules/ directory. This keeps instructions modular and easier for teams to maintain. Rules can also be  [#path-specific-rules] scoped to specific file paths, so they only load into context when Claude works with matching files, reducing noise and saving context space.




Rules load into context every session or when matching files are opened. For task-specific instructions that don’t need to be in context all the time, use  [/docs/en/skills] skills instead, which only load when you invoke them or when Claude determines they’re relevant to your prompt.




 [#set-up-rules] ​


Set up rules

Place markdown files in your project’s .claude/rules/ directory. Each file should cover one topic, with a descriptive filename like testing.md or api-design.md. All .md files are discovered recursively, so you can organize rules into subdirectories like frontend/ or backend/:











your-project/
├── .claude/
│   ├── CLAUDE.md           # Main project instructions
│   └── rules/
│       ├── code-style.md   # Code style guidelines
│       ├── testing.md      # Testing conventions
│       └── security.md     # Security requirements






Rules without  [#path-specific-rules] paths frontmatter are loaded at launch with the same priority as .claude/CLAUDE.md.


 [#path-specific-rules] ​


Path-specific rules

Rules can be scoped to specific files using YAML frontmatter with the paths field. These conditional rules only apply when Claude is working with files matching the specified patterns.











---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules

- All API endpoints must include input validation
- Use the standard error response format
- Include OpenAPI documentation comments






Rules without a paths field are loaded unconditionally and apply to all files. Path-scoped rules trigger when Claude reads files matching the pattern, not on every tool use.
Use glob patterns in the paths field to match files by extension, directory, or any combination:



PatternMatches
**/*.tsAll TypeScript files in any directory
src/**/*All files under src/ directory
*.mdMarkdown files in the project root
src/components/*.tsxReact components in a specific directory



You can specify multiple patterns and use brace expansion to match multiple extensions in one pattern:











---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---








 [#share-rules-across-projects-with-symlinks] ​


Share rules across projects with symlinks

The .claude/rules/ directory supports symlinks, so you can maintain a shared set of rules and link them into multiple projects. Symlinks are resolved and loaded normally, and circular symlinks are detected and handled gracefully.
This example links both a shared directory and an individual file:











ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md








 [#user-level-rules] ​


User-level rules

Personal rules in ~/.claude/rules/ apply to every project on your machine. Use them for preferences that aren’t project-specific:











~/.claude/rules/
├── preferences.md    # Your personal coding preferences
└── workflows.md      # Your preferred workflows






User-level rules are loaded before project rules, giving project rules higher priority.


 [#manage-claude-md-for-large-teams] ​


Manage CLAUDE.md for large teams

For organizations deploying Claude Code across teams, you can centralize instructions and control which CLAUDE.md files are loaded.


 [#deploy-organization-wide-claude-md] ​


Deploy organization-wide CLAUDE.md

Organizations can deploy a centrally managed CLAUDE.md that applies to all users on a machine. This file cannot be excluded by individual settings.







1

 [#] 






Create the file at the managed policy location



macOS: /Library/Application Support/ClaudeCode/CLAUDE.md

Linux and WSL: /etc/claude-code/CLAUDE.md

Windows: C:\Program Files\ClaudeCode\CLAUDE.md









2

 [#] 






Deploy with your configuration management system

Use MDM, Group Policy, Ansible, or similar tools to distribute the file across developer machines. See  [/docs/en/permissions#managed-settings] managed settings for other organization-wide configuration options.




A managed CLAUDE.md and  [/docs/en/settings#settings-files] managed settings serve different purposes. Use settings for technical enforcement and CLAUDE.md for behavioral guidance:



ConcernConfigure in
Block specific tools, commands, or file pathsManaged settings: permissions.deny
Enforce sandbox isolationManaged settings: sandbox.enabled
Environment variables and API provider routingManaged settings: env
Authentication method and organization lockManaged settings: forceLoginMethod, forceLoginOrgUUID
Code style and quality guidelinesManaged CLAUDE.md
Data handling and compliance remindersManaged CLAUDE.md
Behavioral instructions for ClaudeManaged CLAUDE.md



Settings rules are enforced by the client regardless of what Claude decides to do. CLAUDE.md instructions shape Claude’s behavior but are not a hard enforcement layer.


 [#exclude-specific-claude-md-files] ​


Exclude specific CLAUDE.md files

In large monorepos, ancestor CLAUDE.md files may contain instructions that aren’t relevant to your work. The claudeMdExcludes setting lets you skip specific files by path or glob pattern.
This example excludes a top-level CLAUDE.md and a rules directory from a parent folder. Add it to .claude/settings.local.json so the exclusion stays local to your machine:











{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}






Patterns are matched against absolute file paths using glob syntax. You can configure claudeMdExcludes at any  [/docs/en/settings#settings-files] settings layer: user, project, local, or managed policy. Arrays merge across layers.
Managed policy CLAUDE.md files cannot be excluded. This ensures organization-wide instructions always apply regardless of individual settings.


 [#auto-memory] ​


Auto memory

Auto memory lets Claude accumulate knowledge across sessions without you writing anything. Claude saves notes for itself as it works: build commands, debugging insights, architecture notes, code style preferences, and workflow habits. Claude doesn’t save something every session. It decides what’s worth remembering based on whether the information would be useful in a future conversation.




Auto memory requires Claude Code v2.1.59 or later. Check your version with claude --version.




 [#enable-or-disable-auto-memory] ​


Enable or disable auto memory

Auto memory is on by default. To toggle it, open /memory in a session and use the auto memory toggle, or set autoMemoryEnabled in your project settings:











{
  "autoMemoryEnabled": false
}






To disable auto memory via environment variable, set CLAUDE_CODE_DISABLE_AUTO_MEMORY=1.


 [#storage-location] ​


Storage location

Each project gets its own memory directory at ~/.claude/projects/<project>/memory/. The <project> path is derived from the git repository, so all worktrees and subdirectories within the same repo share one auto memory directory. Outside a git repo, the project root is used instead.
To store auto memory in a different location, set autoMemoryDirectory in your user or local settings:











{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}






This setting is accepted from policy, local, and user settings. It is not accepted from project settings (.claude/settings.json) to prevent a shared project from redirecting auto memory writes to sensitive locations.
The directory contains a MEMORY.md entrypoint and optional topic files:











~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index, loaded into every session
├── debugging.md       # Detailed notes on debugging patterns
├── api-conventions.md # API design decisions
└── ...                # Any other topic files Claude creates






MEMORY.md acts as an index of the memory directory. Claude reads and writes files in this directory throughout your session, using MEMORY.md to keep track of what’s stored where.
Auto memory is machine-local. All worktrees and subdirectories within the same git repository share one auto memory directory. Files are not shared across machines or cloud environments.


 [#how-it-works] ​


How it works

The first 200 lines of MEMORY.md, or the first 25KB, whichever comes first, are loaded at the start of every conversation. Content beyond that threshold is not loaded at session start. Claude keeps MEMORY.md concise by moving detailed notes into separate topic files.
This limit applies only to MEMORY.md. CLAUDE.md files are loaded in full regardless of length, though shorter files produce better adherence.
Topic files like debugging.md or patterns.md are not loaded at startup. Claude reads them on demand using its standard file tools when it needs the information.
Claude reads and writes memory files during your session. When you see “Writing memory” or “Recalled memory” in the Claude Code interface, Claude is actively updating or reading from ~/.claude/projects/<project>/memory/.


 [#audit-and-edit-your-memory] ​


Audit and edit your memory

Auto memory files are plain markdown you can edit or delete at any time. Run  [#view-and-edit-with-memory] /memory to browse and open memory files from within a session.


 [#view-and-edit-with-/memory] ​


View and edit with /memory

The /memory command lists all CLAUDE.md and rules files loaded in your current session, lets you toggle auto memory on or off, and provides a link to open the auto memory folder. Select any file to open it in your editor.
When you ask Claude to remember something, like “always use pnpm, not npm” or “remember that the API tests require a local Redis instance,” Claude saves it to auto memory. To add instructions to CLAUDE.md instead, ask Claude directly, like “add this to CLAUDE.md,” or edit the file yourself via /memory.


 [#troubleshoot-memory-issues] ​


Troubleshoot memory issues

These are the most common issues with CLAUDE.md and auto memory, along with steps to debug them.


 [#claude-isn’t-following-my-claude-md] ​


Claude isn’t following my CLAUDE.md

CLAUDE.md content is delivered as a user message after the system prompt, not as part of the system prompt itself. Claude reads it and tries to follow it, but there’s no guarantee of strict compliance, especially for vague or conflicting instructions.
To debug:


Run /memory to verify your CLAUDE.md files are being loaded. If a file isn’t listed, Claude can’t see it.

Check that the relevant CLAUDE.md is in a location that gets loaded for your session (see  [#choose-where-to-put-claude-md-files] Choose where to put CLAUDE.md files).

Make instructions more specific. “Use 2-space indentation” works better than “format code nicely.”

Look for conflicting instructions across CLAUDE.md files. If two files give different guidance for the same behavior, Claude may pick one arbitrarily.

For instructions you want at the system prompt level, use  [/docs/en/cli-reference#system-prompt-flags] --append-system-prompt. This must be passed every invocation, so it’s better suited to scripts and automation than interactive use.




Use the  [/docs/en/hooks#instructionsloaded] InstructionsLoaded hook to log exactly which instruction files are loaded, when they load, and why. This is useful for debugging path-specific rules or lazy-loaded files in subdirectories.




 [#i-don’t-know-what-auto-memory-saved] ​


I don’t know what auto memory saved

Run /memory and select the auto memory folder to browse what Claude has saved. Everything is plain markdown you can read, edit, or delete.


 [#my-claude-md-is-too-large] ​


My CLAUDE.md is too large

Files over 200 lines consume more context and may reduce adherence. Move detailed content into separate files referenced with @path imports (see  [#import-additional-files] Import additional files), or split your instructions across .claude/rules/ files.


 [#instructions-seem-lost-after-/compact] ​


Instructions seem lost after /compact

CLAUDE.md fully survives compaction. After /compact, Claude re-reads your CLAUDE.md from disk and re-injects it fresh into the session. If an instruction disappeared after compaction, it was given only in conversation, not written to CLAUDE.md. Add it to CLAUDE.md to make it persist across sessions.
See  [#write-effective-instructions] Write effective instructions for guidance on size, structure, and specificity.


 [#related-resources] ​


Related resources



 [/docs/en/skills] Skills: package repeatable workflows that load on demand

 [/docs/en/settings] Settings: configure Claude Code behavior with settings files

 [/docs/en/sessions] Manage sessions: manage context, resume conversations, and run parallel sessions

 [/docs/en/sub-agents#enable-persistent-memory] Subagent memory: let subagents maintain their own auto memory




Was this page helpful?


YesNo






 [/docs/en/context-window] Explore the context window [/docs/en/permission-modes] Permission modes





⌘I











 [/docs/en/overview] 
 [https://x.com/AnthropicAI]  [https://www.linkedin.com/company/anthropicresearch] 






 [https://www.anthropic.com/company]  [https://www.anthropic.com/careers]  [https://www.anthropic.com/economic-futures]  [https://www.anthropic.com/research]  [https://www.anthropic.com/news]  [https://trust.anthropic.com/]  [https://www.anthropic.com/transparency] 





 [https://www.anthropic.com/supported-countries]  [https://status.anthropic.com/]  [https://support.claude.com/] 





 [https://www.anthropic.com/learn]  [https://claude.com/partners/mcp]  [https://www.claude.com/customers]  [https://www.anthropic.com/engineering]  [https://www.anthropic.com/events]  [https://claude.com/partners/powered-by-claude]  [https://claude.com/partners/services]  [https://claude.com/programs/startups] 





 [#]  [https://www.anthropic.com/legal/privacy]  [https://www.anthropic.com/responsible-disclosure-policy]  [https://www.anthropic.com/legal/aup]  [https://www.anthropic.com/legal/commercial-terms]  [https://www.anthropic.com/legal/consumer-terms] 












Assistant









Responses are generated using AI and may contain mistakes.
```

### env-vars

URL: https://code.claude.com/docs/en/env-vars
Hash: 0c39f6f1d8c1

```
Environment variables - Claude Code Docs


 [#content-area] Skip to main content










 [/docs/en/overview] Claude Code Docs home page




English




Search...

⌘KAsk AI


 [https://platform.claude.com/] 
 [https://claude.ai/code] 
 [https://claude.ai/code] 





Search...



Navigation


Reference

Environment variables




 [/docs/en/overview] Getting started

 [/docs/en/sub-agents] Build with Claude Code

 [/docs/en/third-party-integrations] Deployment

 [/docs/en/setup] Administration

 [/docs/en/settings] Configuration

 [/docs/en/cli-reference] Reference

 [/docs/en/legal-and-compliance] Resources
















Reference


 [/docs/en/cli-reference] 

CLI reference


 [/docs/en/commands] 

Built-in commands


 [/docs/en/env-vars] 

Environment variables


 [/docs/en/tools-reference] 

Tools reference


 [/docs/en/interactive-mode] 

Interactive mode


 [/docs/en/checkpointing] 

Checkpointing


 [/docs/en/hooks] 

Hooks reference


 [/docs/en/plugins-reference] 

Plugins reference


 [/docs/en/channels-reference] 

Channels reference











On this page

 [#see-also] See also

























Claude Code supports the following environment variables to control its behavior. Set them in your shell before launching claude, or configure them in  [/docs/en/settings#available-settings] settings.json under the env key to apply them to every session or roll them out across your team.



VariablePurpose
ANTHROPIC_API_KEYAPI key sent as X-Api-Key header. When set, this key is used instead of your Claude Pro, Max, Team, or Enterprise subscription even if you are logged in. In non-interactive mode (-p), the key is always used when present. In interactive mode, you are prompted to approve the key once before it overrides your subscription. To use your subscription instead, run unset ANTHROPIC_API_KEY
ANTHROPIC_AUTH_TOKENCustom value for the Authorization header (the value you set here will be prefixed with Bearer )
ANTHROPIC_BASE_URLOverride the API endpoint to route requests through a proxy or gateway. When set to a non-first-party host,  [/docs/en/mcp#scale-with-mcp-tool-search] MCP tool search is disabled by default. Set ENABLE_TOOL_SEARCH=true if your proxy forwards tool_reference blocks
ANTHROPIC_CUSTOM_HEADERSCustom headers to add to requests (Name: Value format, newline-separated for multiple headers)
ANTHROPIC_CUSTOM_MODEL_OPTIONModel ID to add as a custom entry in the /model picker. Use this to make a non-standard or gateway-specific model selectable without replacing built-in aliases. See  [/docs/en/model-config#add-a-custom-model-option] Model configuration
ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTIONDisplay description for the custom model entry in the /model picker. Defaults to Custom model (<model-id>) when not set
ANTHROPIC_CUSTOM_MODEL_OPTION_NAMEDisplay name for the custom model entry in the /model picker. Defaults to the model ID when not set
ANTHROPIC_DEFAULT_HAIKU_MODELSee  [/docs/en/model-config#environment-variables] Model configuration
ANTHROPIC_DEFAULT_HAIKU_MODEL_DESCRIPTIONSee  [/docs/en/model-config#customize-pinned-model-display-and-capabilities] Model configuration
ANTHROPIC_DEFAULT_HAIKU_MODEL_NAMESee  [/docs/en/model-config#customize-pinned-model-display-and-capabilities] Model configuration
ANTHROPIC_DEFAULT_HAIKU_MODEL_SUPPORTED_CAPABILITIESSee  [/docs/en/model-config#customize-pinned-model-display-and-capabilities] Model configuration
ANTHROPIC_DEFAULT_OPUS_MODELSee  [/docs/en/model-config#environment-variables] Model configuration
ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTIONSee  [/docs/en/model-config#customize-pinned-model-display-and-capabilities] Model configuration
ANTHROPIC_DEFAULT_OPUS_MODEL_NAMESee  [/docs/en/model-config#customize-pinned-model-display-and-capabilities] Model configuration
ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIESSee  [/docs/en/model-config#customize-pinned-model-display-and-capabilities] Model configuration
ANTHROPIC_DEFAULT_SONNET_MODELSee  [/docs/en/model-config#environment-variables] Model configuration
ANTHROPIC_DEFAULT_SONNET_MODEL_DESCRIPTIONSee  [/docs/en/model-config#customize-pinned-model-display-and-capabilities] Model configuration
ANTHROPIC_DEFAULT_SONNET_MODEL_NAMESee  [/docs/en/model-config#customize-pinned-model-display-and-capabilities] Model configuration
ANTHROPIC_DEFAULT_SONNET_MODEL_SUPPORTED_CAPABILITIESSee  [/docs/en/model-config#customize-pinned-model-display-and-capabilities] Model configuration
ANTHROPIC_FOUNDRY_API_KEYAPI key for Microsoft Foundry authentication (see  [/docs/en/microsoft-foundry] Microsoft Foundry)
ANTHROPIC_FOUNDRY_BASE_URLFull base URL for the Foundry resource (for example, https://my-resource.services.ai.azure.com/anthropic). Alternative to ANTHROPIC_FOUNDRY_RESOURCE (see  [/docs/en/microsoft-foundry] Microsoft Foundry)
ANTHROPIC_FOUNDRY_RESOURCEFoundry resource name (for example, my-resource). Required if ANTHROPIC_FOUNDRY_BASE_URL is not set (see  [/docs/en/microsoft-foundry] Microsoft Foundry)
ANTHROPIC_MODELName of the model setting to use (see  [/docs/en/model-config#environment-variables] Model Configuration)
ANTHROPIC_SMALL_FAST_MODEL[DEPRECATED] Name of  [/docs/en/costs] Haiku-class model for background tasks
ANTHROPIC_SMALL_FAST_MODEL_AWS_REGIONOverride AWS region for the Haiku-class model when using Bedrock
AWS_BEARER_TOKEN_BEDROCKBedrock API key for authentication (see  [https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/] Bedrock API keys)
BASH_DEFAULT_TIMEOUT_MSDefault timeout for long-running bash commands
BASH_MAX_OUTPUT_LENGTHMaximum number of characters in bash outputs before they are middle-truncated
BASH_MAX_TIMEOUT_MSMaximum timeout the model can set for long-running bash commands
CLAUDECODESet to 1 in shell environments Claude Code spawns (Bash tool, tmux sessions). Not set in  [/docs/en/hooks] hooks or  [/docs/en/statusline] status line commands. Use to detect when a script is running inside a shell spawned by Claude Code
CLAUDE_AUTOCOMPACT_PCT_OVERRIDESet the percentage of context capacity (1-100) at which auto-compaction triggers. By default, auto-compaction triggers at approximately 95% capacity. Use lower values like 50 to compact earlier. Values above the default threshold have no effect. Applies to both main conversations and subagents. This percentage aligns with the context_window.used_percentage field available in  [/docs/en/statusline] status line
CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIRReturn to the original working directory after each Bash command
CLAUDE_CODE_ACCOUNT_UUIDAccount UUID for the authenticated user. Used by SDK callers to provide account information synchronously, avoiding a race condition where early telemetry events lack account metadata. Requires CLAUDE_CODE_USER_EMAIL and CLAUDE_CODE_ORGANIZATION_UUID to also be set
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MDSet to 1 to load CLAUDE.md files from directories specified with --add-dir. By default, additional directories do not load memory files
CLAUDE_CODE_AUTO_COMPACT_WINDOWSet the context capacity in tokens used for auto-compaction calculations. Defaults to the model’s context window: 200K for standard models or 1M for  [/docs/en/model-config#extended-context] extended context models. Use a lower value like 500000 on a 1M model to treat the window as 500K for compaction purposes. The value is capped at the model’s actual context window. CLAUDE_AUTOCOMPACT_PCT_OVERRIDE is applied as a percentage of this value. Setting this variable decouples the compaction threshold from the status line’s used_percentage, which always uses the model’s full context window
CLAUDE_CODE_API_KEY_HELPER_TTL_MSInterval in milliseconds at which credentials should be refreshed (when using  [/docs/en/settings#available-settings] apiKeyHelper)
CLAUDE_CODE_CLIENT_CERTPath to client certificate file for mTLS authentication
CLAUDE_CODE_CLIENT_KEYPath to client private key file for mTLS authentication
CLAUDE_CODE_CLIENT_KEY_PASSPHRASEPassphrase for encrypted CLAUDE_CODE_CLIENT_KEY (optional)
CLAUDE_CODE_DISABLE_1M_CONTEXTSet to 1 to disable  [/docs/en/model-config#extended-context] 1M context window support. When set, 1M model variants are unavailable in the model picker. Useful for enterprise environments with compliance requirements
CLAUDE_CODE_DISABLE_ADAPTIVE_THINKINGSet to 1 to disable  [/docs/en/model-config#adjust-effort-level] adaptive reasoning for Opus 4.6 and Sonnet 4.6. When disabled, these models fall back to the fixed thinking budget controlled by MAX_THINKING_TOKENS
CLAUDE_CODE_DISABLE_AUTO_MEMORYSet to 1 to disable  [/docs/en/memory#auto-memory] auto memory. Set to 0 to force auto memory on during the gradual rollout. When disabled, Claude does not create or load auto memory files
CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONSSet to 1 to remove built-in commit and PR workflow instructions and the git status snapshot from Claude’s system prompt. Useful when using your own git workflow skills. Takes precedence over the  [/docs/en/settings#available-settings] includeGitInstructions setting when set
CLAUDE_CODE_DISABLE_BACKGROUND_TASKSSet to 1 to disable all background task functionality, including the run_in_background parameter on Bash and subagent tools, auto-backgrounding, and the Ctrl+B shortcut
CLAUDE_CODE_DISABLE_CRONSet to 1 to disable  [/docs/en/scheduled-tasks] scheduled tasks. The /loop skill and cron tools become unavailable and any already-scheduled tasks stop firing, including tasks that are already running mid-session
CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETASSet to 1 to strip Anthropic-specific anthropic-beta request headers and beta tool-schema fields (such as defer_loading and eager_input_streaming) from API requests. Use this when a proxy gateway rejects requests with errors like “Unexpected value(s) for the anthropic-beta header” or “Extra inputs are not permitted”. Standard fields (name, description, input_schema, cache_control) are preserved.
CLAUDE_CODE_DISABLE_FAST_MODESet to 1 to disable  [/docs/en/fast-mode] fast mode
CLAUDE_CODE_DISABLE_FEEDBACK_SURVEYSet to 1 to disable the “How is Claude doing?” session quality surveys. Surveys are also disabled when DISABLE_TELEMETRY or CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC is set. See  [/docs/en/data-usage#session-quality-surveys] Session quality surveys
CLAUDE_CODE_DISABLE_MOUSESet to 1 to disable mouse tracking in  [/docs/en/fullscreen] fullscreen rendering. Keyboard scrolling with PgUp and PgDn still works. Use this to keep your terminal’s native copy-on-select behavior
CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFICEquivalent of setting DISABLE_AUTOUPDATER, DISABLE_FEEDBACK_COMMAND, DISABLE_ERROR_REPORTING, and DISABLE_TELEMETRY
CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACKSet to 1 to disable the non-streaming fallback when a streaming request fails mid-stream. Streaming errors propagate to the retry layer instead. Useful when a proxy or gateway causes the fallback to produce duplicate tool execution
CLAUDE_CODE_DISABLE_TERMINAL_TITLESet to 1 to disable automatic terminal title updates based on conversation context
CLAUDE_CODE_EFFORT_LEVELSet the effort level for supported models. Values: low, medium, high, max (Opus 4.6 only), or auto to use the model default. Takes precedence over /effort and the effortLevel setting. See  [/docs/en/model-config#adjust-effort-level] Adjust effort level
CLAUDE_CODE_ENABLE_PROMPT_SUGGESTIONSet to false to disable prompt suggestions (the “Prompt suggestions” toggle in /config). These are the grayed-out predictions that appear in your prompt input after Claude responds. See  [/docs/en/interactive-mode#prompt-suggestions] Prompt suggestions
CLAUDE_CODE_ENABLE_TASKSSet to true to enable the task tracking system in non-interactive mode (the -p flag). Tasks are on by default in interactive mode. See  [/docs/en/interactive-mode#task-list] Task list
CLAUDE_CODE_ENABLE_TELEMETRYSet to 1 to enable OpenTelemetry data collection for metrics and logging. Required before configuring OTel exporters. See  [/docs/en/monitoring-usage] Monitoring
CLAUDE_CODE_EXIT_AFTER_STOP_DELAYTime in milliseconds to wait after the query loop becomes idle before automatically exiting. Useful for automated workflows and scripts using SDK mode
CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMSSet to 1 to enable  [/docs/en/agent-teams] agent teams. Agent teams are experimental and disabled by default
CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENSOverride the default token limit for file reads. Useful when you need to read larger files in full
CLAUDE_CODE_IDE_SKIP_AUTO_INSTALLSkip auto-installation of IDE extensions. Equivalent to setting  [/docs/en/settings#global-config-settings] autoInstallIdeExtension to false
CLAUDE_CODE_MAX_OUTPUT_TOKENSSet the maximum number of output tokens for most requests. Defaults and caps vary by model; see  [https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison] max output tokens. Increasing this value reduces the effective context window available before  [/docs/en/costs#reduce-token-usage] auto-compaction triggers.
CLAUDE_CODE_NEW_INITSet to true to make /init run an interactive setup flow. The flow asks which files to generate, including CLAUDE.md, skills, and hooks, before exploring the codebase and writing them. Without this variable, /init generates a CLAUDE.md automatically without prompting.
CLAUDE_CODE_NO_FLICKERSet to 1 to enable  [/docs/en/fullscreen] fullscreen rendering, a research preview that reduces flicker and keeps memory flat in long conversations
CLAUDE_CODE_ORGANIZATION_UUIDOrganization UUID for the authenticated user. Used by SDK callers to provide account information synchronously. Requires CLAUDE_CODE_ACCOUNT_UUID and CLAUDE_CODE_USER_EMAIL to also be set
CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MSInterval for refreshing dynamic OpenTelemetry headers in milliseconds (default: 1740000 / 29 minutes). See  [/docs/en/monitoring-usage#dynamic-headers] Dynamic headers
CLAUDE_CODE_PLAN_MODE_REQUIREDAuto-set to true on  [/docs/en/agent-teams] agent team teammates that require plan approval. Read-only: set by Claude Code when spawning teammates. See  [/docs/en/agent-teams#require-plan-approval-for-teammates] require plan approval
CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MSTimeout in milliseconds for git operations when installing or updating plugins (default: 120000). Increase this value for large repositories or slow network connections. See  [/docs/en/plugin-marketplaces#git-operations-time-out] Git operations time out
CLAUDE_CODE_PLUGIN_SEED_DIRPath to one or more read-only plugin seed directories, separated by : on Unix or ; on Windows. Use this to bundle a pre-populated plugins directory into a container image. Claude Code registers marketplaces from these directories at startup and uses pre-cached plugins without re-cloning. See  [/docs/en/plugin-marketplaces#pre-populate-plugins-for-containers] Pre-populate plugins for containers
CLAUDE_CODE_PROXY_RESOLVES_HOSTSSet to true to allow the proxy to perform DNS resolution instead of the caller. Opt-in for environments where the proxy should handle hostname resolution
CLAUDE_CODE_SCROLL_SPEEDSet the mouse wheel scroll multiplier in  [/docs/en/fullscreen#adjust-wheel-scroll-speed] fullscreen rendering. Accepts values from 1 to 20. Set to 3 to match vim if your terminal sends one wheel event per notch without amplification
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MSMaximum time in milliseconds for  [/docs/en/hooks#sessionend] SessionEnd hooks to complete (default: 1500). Applies to session exit, /clear, and switching sessions via interactive /resume. Per-hook timeout values are also capped by this budget
CLAUDE_CODE_SHELLOverride automatic shell detection. Useful when your login shell differs from your preferred working shell (for example, bash vs zsh)
CLAUDE_CODE_SHELL_PREFIXCommand prefix to wrap all bash commands (for example, for logging or auditing). Example: /path/to/logger.sh will execute /path/to/logger.sh <command>
CLAUDE_CODE_SIMPLESet to 1 to run with a minimal system prompt and only the Bash, file read, and file edit tools. MCP tools from --mcp-config are still available. Disables auto-discovery of hooks, skills, plugins, MCP servers, auto memory, and CLAUDE.md. The  [/docs/en/headless#start-faster-with-bare-mode] --bare CLI flag sets this
CLAUDE_CODE_SKIP_BEDROCK_AUTHSkip AWS authentication for Bedrock (for example, when using an LLM gateway)
CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORSSet to 1 to allow  [/docs/en/fast-mode] fast mode when the organization status check fails due to a network error. Useful when a corporate proxy blocks the status endpoint. The API still enforces organization-level disable separately
CLAUDE_CODE_SKIP_FOUNDRY_AUTHSkip Azure authentication for Microsoft Foundry (for example, when using an LLM gateway)
CLAUDE_CODE_SKIP_VERTEX_AUTHSkip Google authentication for Vertex (for example, when using an LLM gateway)
CLAUDE_CODE_SUBAGENT_MODELSee  [/docs/en/model-config] Model configuration
CLAUDE_CODE_SUBPROCESS_ENV_SCRUBSet to 1 to strip Anthropic and cloud provider credentials from subprocess environments (Bash tool, hooks, MCP stdio servers). The parent Claude process keeps these credentials for API calls, but child processes cannot read them, reducing exposure to prompt injection attacks that attempt to exfiltrate secrets via shell expansion. claude-code-action sets this automatically when allowed_non_write_users is configured
CLAUDE_CODE_TASK_LIST_IDShare a task list across sessions. Set the same ID in multiple Claude Code instances to coordinate on a shared task list. See  [/docs/en/interactive-mode#task-list] Task list
CLAUDE_CODE_TEAM_NAMEName of the agent team this teammate belongs to. Set automatically on  [/docs/en/agent-teams] agent team members
CLAUDE_CODE_TMPDIROverride the temp directory used for internal temp files. Claude Code appends /claude/ to this path. Default: /tmp on Unix/macOS, os.tmpdir() on Windows
CLAUDE_CODE_USER_EMAILEmail address for the authenticated user. Used by SDK callers to provide account information synchronously. Requires CLAUDE_CODE_ACCOUNT_UUID and CLAUDE_CODE_ORGANIZATION_UUID to also be set
CLAUDE_CODE_USE_BEDROCKUse  [/docs/en/amazon-bedrock] Bedrock
CLAUDE_CODE_USE_FOUNDRYUse  [/docs/en/microsoft-foundry] Microsoft Foundry
CLAUDE_CODE_USE_POWERSHELL_TOOLSet to 1 to enable the PowerShell tool on Windows (opt-in preview). When enabled, Claude can run PowerShell commands natively instead of routing through Git Bash. Only supported on native Windows, not WSL. See  [/docs/en/tools-reference#powershell-tool] PowerShell tool
CLAUDE_CODE_USE_VERTEXUse  [/docs/en/google-vertex-ai] Vertex
CLAUDE_CONFIG_DIRCustomize where Claude Code stores its configuration and data files
CLAUDE_ENV_FILEPath to a shell script that Claude Code sources before each Bash command. Use to persist virtualenv or conda activation across commands. Also populated dynamically by  [/docs/en/hooks#persist-environment-variables] SessionStart,  [/docs/en/hooks#cwdchanged] CwdChanged, and  [/docs/en/hooks#filechanged] FileChanged hooks
CLAUDE_STREAM_IDLE_TIMEOUT_MSTimeout in milliseconds before the streaming idle watchdog closes a stalled connection. Default: 90000 (90 seconds). Increase this value if long-running tools or slow networks cause premature timeout errors
DISABLE_AUTOUPDATERSet to 1 to disable automatic updates.
DISABLE_COST_WARNINGSSet to 1 to disable cost warning messages
DISABLE_ERROR_REPORTINGSet to 1 to opt out of Sentry error reporting
DISABLE_FEEDBACK_COMMANDSet to 1 to disable the /feedback command. The older name DISABLE_BUG_COMMAND is also accepted
DISABLE_INSTALLATION_CHECKSSet to 1 to disable installation warnings. Use only when manually managing the installation location, as this can mask issues with standard installations
DISABLE_PROMPT_CACHINGSet to 1 to disable prompt caching for all models (takes precedence over per-model settings)
DISABLE_PROMPT_CACHING_HAIKUSet to 1 to disable prompt caching for Haiku models
DISABLE_PROMPT_CACHING_OPUSSet to 1 to disable prompt caching for Opus models
DISABLE_PROMPT_CACHING_SONNETSet to 1 to disable prompt caching for Sonnet models
DISABLE_TELEMETRYSet to 1 to opt out of Statsig telemetry (note that Statsig events do not include user data like code, file paths, or bash commands)
ENABLE_CLAUDEAI_MCP_SERVERSSet to false to disable  [/docs/en/mcp#use-mcp-servers-from-claude-ai] claude.ai MCP servers in Claude Code. Enabled by default for logged-in users
ENABLE_TOOL_SEARCHControls  [/docs/en/mcp#scale-with-mcp-tool-search] MCP tool search. Unset: all MCP tools deferred by default, but loaded upfront when ANTHROPIC_BASE_URL points to a non-first-party host. Values: true (always defer including proxies), auto (threshold mode: load upfront if tools fit within 10% of context), auto:N (custom threshold, e.g., auto:5 for 5%), false (load all upfront)
FORCE_AUTOUPDATE_PLUGINSSet to true to force plugin auto-updates even when the main auto-updater is disabled via DISABLE_AUTOUPDATER
HTTP_PROXYSpecify HTTP proxy server for network connections
HTTPS_PROXYSpecify HTTPS proxy server for network connections
IS_DEMOSet to true to enable demo mode: hides email and organization from the UI, skips onboarding, and hides internal commands. Useful for streaming or recording sessions
MAX_MCP_OUTPUT_TOKENSMaximum number of tokens allowed in MCP tool responses. Claude Code displays a warning when output exceeds 10,000 tokens (default: 25000)
MAX_THINKING_TOKENSOverride the  [https://platform.claude.com/docs/en/build-with-claude/extended-thinking] extended thinking token budget. The ceiling is the model’s  [https://platform.claude.com/docs/en/about-claude/models/overview#latest-models-comparison] max output tokens minus one. Set to 0 to disable thinking entirely. On models with adaptive reasoning (Opus 4.6, Sonnet 4.6), the budget is ignored unless adaptive reasoning is disabled via CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING
MCP_CLIENT_SECRETOAuth client secret for MCP servers that require  [/docs/en/mcp#use-pre-configured-oauth-credentials] pre-configured credentials. Avoids the interactive prompt when adding a server with --client-secret
MCP_OAUTH_CALLBACK_PORTFixed port for the OAuth redirect callback, as an alternative to --callback-port when adding an MCP server with  [/docs/en/mcp#use-pre-configured-oauth-credentials] pre-configured credentials
MCP_TIMEOUTTimeout in milliseconds for MCP server startup
MCP_TOOL_TIMEOUTTimeout in milliseconds for MCP tool execution
NO_PROXYList of domains and IPs to which requests will be directly issued, bypassing proxy
SLASH_COMMAND_TOOL_CHAR_BUDGETOverride the character budget for skill metadata shown to the  [/docs/en/skills#control-who-invokes-a-skill] Skill tool. The budget scales dynamically at 1% of the context window, with a fallback of 8,000 characters. Legacy name kept for backwards compatibility
USE_BUILTIN_RIPGREPSet to 0 to use system-installed rg instead of rg included with Claude Code
VERTEX_REGION_CLAUDE_3_5_HAIKUOverride region for Claude 3.5 Haiku when using Vertex AI
VERTEX_REGION_CLAUDE_3_7_SONNETOverride region for Claude 3.7 Sonnet when using Vertex AI
VERTEX_REGION_CLAUDE_4_0_OPUSOverride region for Claude 4.0 Opus when using Vertex AI
VERTEX_REGION_CLAUDE_4_0_SONNETOverride region for Claude 4.0 Sonnet when using Vertex AI
VERTEX_REGION_CLAUDE_4_1_OPUSOverride region for Claude 4.1 Opus when using Vertex AI





 [#see-also] ​


See also



 [/docs/en/settings] Settings: configure environment variables in settings.json so they apply to every session

 [/docs/en/cli-reference] CLI reference: launch-time flags

 [/docs/en/network-config] Network configuration: proxy and TLS setup




Was this page helpful?


YesNo






 [/docs/en/commands] Built-in commands [/docs/en/tools-reference] Tools reference





⌘I











 [/docs/en/overview] 
 [https://x.com/AnthropicAI]  [https://www.linkedin.com/company/anthropicresearch] 






 [https://www.anthropic.com/company]  [https://www.anthropic.com/careers]  [https://www.anthropic.com/economic-futures]  [https://www.anthropic.com/research]  [https://www.anthropic.com/news]  [https://trust.anthropic.com/]  [https://www.anthropic.com/transparency] 





 [https://www.anthropic.com/supported-countries]  [https://status.anthropic.com/]  [https://support.claude.com/] 





 [https://www.anthropic.com/learn]  [https://claude.com/partners/mcp]  [https://www.claude.com/customers]  [https://www.anthropic.com/engineering]  [https://www.anthropic.com/events]  [https://claude.com/partners/powered-by-claude]  [https://claude.com/partners/services]  [https://claude.com/programs/startups] 





 [#]  [https://www.anthropic.com/legal/privacy]  [https://www.anthropic.com/responsible-disclosure-policy]  [https://www.anthropic.com/legal/aup]  [https://www.anthropic.com/legal/commercial-terms]  [https://www.anthropic.com/legal/consumer-terms] 












Assistant









Responses are generated using AI and may contain mistakes.
```

---

Crawl complete: 13 pages fetched, 0 errors
