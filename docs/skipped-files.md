# Files that the Stop hook skips

[The Stop hook](hooks.md#the-stop-hook) looks for `.md` and `.html` files that changed during a turn. It skips the files, the folders and the parts of files on this page. The command `fresh_eyes.py packet`, which makes a packet by hand, leaves out the same files and folders. The name match ignores case, except for 9 names that match only in capital letters. The third item under Files lists those 9 names.

## Files

- Files whose names start with `CHANGELOG`, `CHANGES`, `HISTORY` or `NEWS`, and the files `failure-modes.md`, `PLAN.md` and `ERRORS.md`.
- Files written for agents to read, in any folder: `CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md`, `AGENT.md`, `AGENTS.override.md`, `AGENTS.local.md`, `GEMINI.md`, `QWEN.md`, `WARP.md`, `CRUSH.md`, `CONVENTIONS.md`, `CONTEXT.md`, `CONTEXT-MAP.md`, `GLOSSARY.md`, `GLOSSARY-MAP.md`, `SKILL.md`, `copilot-instructions.md`, `replit.md`, `OpenCode.md`, `global_rules.md`, `memory_summary.md`, `raw_memories.md`, `.hermes.md`, `.aider.chat.history.md`, and every `*.instructions.md`, `*.prompt.md`, `*.agent.md` and `*.chatmode.md` file.
- 9 more files written for agents, which match only when the name is in capital letters: `MEMORY.md`, `SOUL.md`, `IDENTITY.md`, `BOOT.md`, `DREAMS.md`, `HEARTBEAT.md`, `HERMES.md`, `BUGBOT.md` and `POWER.md`. A file such as `docs/memory.md` still counts as a doc.
- The generated pages `tools.html` and `blog/index.html`.

## Folders

- Everything in a `memory/`, `transcripts/`, `_site/` or `node_modules/` folder.
- Everything in a folder of files written for agents: `.scratch/`, `.agents/`, `.agent/`, `_agents/`, `_agent/`, `.claude/`, `docs/agents/`, `docs/adr/`, `output-styles/`, `memory-bank/`, `.codex/`, `.gemini/`, `.opencode/`, `.cline/`, `.clinerules/`, `.roo/`, `.augment/`, `.kilo/`, `.kilocode/`, `.devin/`, `.junie/`, `.specify/`, `.serena/`, `.pi/`, `.factory/`, `.qwen/`, `.crush/`, `.ruler/`, `.idx/`, `.cursor/rules/`, `.cursor/commands/`, `.cursor/agents/`, `.cursor/skills/`, `.github/instructions/`, `.github/agents/`, `.github/skills/`, `.github/prompts/`, `.github/chatmodes/`, `.windsurf/rules/`, `.windsurf/workflows/`, `.windsurf/skills/`, `.kiro/steering/`, `.kiro/agents/`, `.kiro/prompts/`, `.kiro/skills/`, `.amazonq/rules/`, `.trae/rules/`, `.continue/rules/`, `.openhands/microagents/`, `.tabnine/guidelines/`, `.aiassistant/rules/`, `.qoder/rules/`, `.vibe/prompts/`, `.ai/guidelines/` and `.ai/skills/`.

## Parts of files

- The text from a heading named Log, Changelog, Change log, History or Release notes to the end of the file, and the text between `<!--gen:NAME-->` and `<!--/gen:NAME-->`, for any `NAME`.
