<h1>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/tagore-wordmark-dark.svg">
    <img alt="tagore" src="assets/logo/tagore-wordmark.svg" width="240">
  </picture>
</h1>

A Claude Code plugin for prose that other people read. It has 2 parts:

- **The `plain-prose` skill** rewrites the sentence patterns that make text read as model-written. Examples are "it's not X, it's Y", headers that state a verdict, and one-line closers that sound like a moral. Then the skill checks that the rewrite kept every fact of the draft.
- **A Stop hook** runs each time Claude tries to end a turn. If the turn changed a doc, Claude must first have a fresh subagent read the new text as a newcomer.

The skill, its scripts and the hook come from declauding by Oskar Austegard (see Credit). tagore packages them as a plugin that you can install.

## Install

```
/plugin marketplace add rajnandan1/tagore
/plugin install tagore@tagore
```

To try it for one session, clone this repository and start Claude Code with `claude --plugin-dir /path/to/tagore`.

To get a new version, run `claude plugin marketplace update tagore`, then `claude plugin update tagore@tagore`, then restart Claude Code.

To turn it off, run `claude plugin disable tagore@tagore`. This turns off the skill and the hook together.

## Layout

Each skill keeps all of its files in its own folder under `skills/`. Its hooks are in that folder too. `.claude-plugin/plugin.json` lists each hook file in its `"hooks"` array.

```
.claude-plugin/plugin.json        the plugin manifest
.claude-plugin/marketplace.json   the catalog that /plugin marketplace add reads
skills/plain-prose/SKILL.md       the skill
skills/plain-prose/hooks/         the Stop hook config
skills/plain-prose/scripts/       the scripts that the skill and the hook run
skills/plain-prose/references/    the pattern list and the notes that the skill reads
skills/plain-prose/tests/         the tests
evidence/                         the writing samples and scores behind skills/plain-prose/references/models/
```

To add a skill, add a folder `skills/<name>/` with a `SKILL.md`. To add a hook, put its file in that skill's `hooks/` folder and add its path to the `"hooks"` array. For each release, raise `version` in both `plugin.json` and `marketplace.json`.

## The skill

Say "de-claude this", "humanize this" or "this reads like AI", or run `/tagore:plain-prose`. The skill also loads by itself when the task is prose for a reader: a PR description, commit message, README, doc, report or release note. It does not touch fiction, poetry, code or quoted text.

The skill works in this order. The scripts are in `skills/plain-prose/scripts/`.

1. Claude reads the whole draft and writes down the one point that the draft must make.
2. `declaude_lint.py` finds the known patterns with regex and prints their line numbers.
3. `declaude_review.py` sends the title, the headers, the first sentence, the last sentence of each section and each one-sentence paragraph to a model. The model checks them for patterns that regex cannot find, such as a header that states a verdict.
4. Claude rewrites each flagged sentence so that it states its point plainly.
5. `declaude_diff.py` compares the rewrite with the draft. It lists the numbers, names, quotes, links and hedges that the rewrite lost or invented.

Before step 4, Claude can also run `declaude_rank.py`. It ranks the sentences by how much each one acts out a finding instead of stating it.

## The hook

The hook runs `skills/plain-prose/scripts/fresh_eyes.py` each time Claude tries to end a turn. A turn starts with your last message. If the turn changed prose in a doc, the hook makes Claude send that prose to a subagent that never saw the earlier version. This check is the newcomer read. The hook needs `python3`, and it uses `git` for files in a git repository.

1. It looks for `.md` and `.html` files that changed during the turn. In a git repository, it counts commits made during the turn, uncommitted edits and new files. It checks the repository in the folder where Claude Code started and each repository one folder below it. Outside git repositories, it checks files saved during the turn, up to 4 folders deep in the folder where Claude Code started.
2. Only visible prose counts. Code blocks, inline code, HTML tags, scripts, styles and HTML comments do not count.
3. It skips these files and parts of files. The name match ignores case.
   - Files whose names start with `CHANGELOG`, `CHANGES`, `HISTORY` or `NEWS`, and the files `failure-modes.md`, `PLAN.md` and `ERRORS.md`.
   - Everything in a `memory/`, `transcripts/`, `_site/` or `node_modules/` folder.
   - Files written for agents to read, in any folder: `CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md`, `AGENT.md`, `AGENTS.override.md`, `GEMINI.md`, `QWEN.md`, `WARP.md`, `CRUSH.md`, `CONVENTIONS.md`, `CONTEXT.md`, `CONTEXT-MAP.md`, `GLOSSARY.md`, `GLOSSARY-MAP.md`, `SKILL.md`, `copilot-instructions.md` and every `*.instructions.md` file.
   - Everything in a folder of files written for agents: `.scratch/`, `.agents/`, `.claude/`, `docs/agents/`, `docs/adr/`, `.cursor/rules/`, `.github/instructions/`, `.github/agents/`, `.github/skills/`, `.github/prompts/`, `.windsurf/rules/`, `.kiro/steering/`, `.clinerules/`, `.junie/`, `.roo/rules/`, `.amazonq/rules/`, `.augment/rules/`, `.kilocode/rules/`, `.trae/rules/`, `.continue/rules/`, `.openhands/microagents/` and `.idx/`.
   - The generated pages `tools.html` and `blog/index.html`.
   - The text from a heading named Log, Changelog, Change log, History or Release notes to the end of the file, and the text between `<!--gen:NAME-->` and `<!--/gen:NAME-->`, for any `NAME`.
4. It blocks the end of the turn when 2 conditions are true: 20 or more characters of prose were added, removed or rewritten in total across all changed files, and Claude did not send a subagent a prompt that contains `FRESH-EYES READ` after the last change. The hook writes a packet file to `/tmp/fresh-eyes/`. For a Markdown file, the packet holds each changed section whole. For an HTML file, it holds the visible text within 25 lines of each change. Then the hook gives Claude the `FRESH-EYES READ` prompt to send.
5. Claude sends that prompt to a subagent. The subagent reads only the packet and lists each phrase that a newcomer would not understand. Claude fixes each phrase or says why it stays.

The hook blocks at most once per turn. If Claude tries to end the turn again without the read, the turn ends. If the hook itself has an error, it lets the turn end.

To make a packet of a whole `.md` or `.html` file at any time, run `python3 skills/plain-prose/scripts/fresh_eyes.py packet <file>` from the root of a clone of this repository. The command prints the packet path and the prompt. Give that prompt to a subagent to get the newcomer read.

## Network calls and files written

- `declaude_review.py` sends text to Google Gemini (`gemini-3.6-flash`) when `GEMINI_API_KEY` is set. Else it sends text to the Anthropic API (`claude-sonnet-5-5`) when `ANTHROPIC_API_KEY` is set. With neither key, it prints the prompt, and Claude gives that prompt to a subagent.
- `declaude_rank.py` downloads `sentence-transformers/all-MiniLM-L6-v2` from Hugging Face. It needs `pip install torch transformers`.
- The other scripts and the hook run on your machine only. The hook writes packets to `/tmp/fresh-eyes/`. It also adds one line per run to `~/.claude/fresh-eyes-log.jsonl`, with the time, the folder and the result.

## Tests

From the repository root, run `uvx pytest skills/plain-prose/tests`. If pytest is installed, `python3 -m pytest skills/plain-prose/tests` also works.

## Credit

The `plain-prose` skill is declauding version 0.14.0 by Oskar Austegard, with its scripts, tests and hook config. It comes from [oaustegard/claude-skills](https://github.com/oaustegard/claude-skills/tree/366e2f2c61fbd4291774ae4d35f32bf66e3ee2e9/declauding) at commit `366e2f2c`, under the MIT license in `LICENSE`. tagore adds the plugin manifest, the marketplace file, this README, `evidence/README.md` and the Fable 5.2 samples in `evidence/fable-5-2/`.

`evidence/model-register-drift/` is a copy of the samples and scores by Oskar Austegard in [oaustegard/experiments](https://github.com/oaustegard/experiments/tree/1f3e6192b4d1f5ddbe1104eecbfd5a5b5c0f7b45/model-register-drift) at commit `1f3e6192`, under the MIT license in its own `LICENSE`. `evidence/README.md` says what the copy holds and how it differs from upstream.

tagore changes 5 things in the declauding files from `oaustegard/claude-skills`. The `SKILL.md`, `hooks/`, `references/`, `scripts/` and `tests/` paths in this list are inside `skills/plain-prose/`.

1. The folder is `skills/plain-prose/`, not `declauding/`.
2. In `SKILL.md`, the `name`, the title and the `/mnt/skills/user/` path say `plain-prose`.
3. In `hooks/hooks.json`, the script path says `plain-prose`.
4. `references/models/fable.md` also covers Fable 5.2, and the model table in `SKILL.md` names it.
5. `scripts/fresh_eyes.py` also skips the files and folders written for agents that step 3 of "The hook" above lists, and `tests/test_fresh_eyes.py` checks that it does.

The script names (`declaude_*.py`) and the other reference files keep the upstream names. So an upstream update needs only these 5 changes again, plus a merge of `references/models/fable.md`, `scripts/fresh_eyes.py` or `tests/test_fresh_eyes.py` if upstream changes one of those files.
