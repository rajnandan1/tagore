<h1>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo/tagore-wordmark-dark.svg">
    <img alt="tagore" src="assets/logo/tagore-wordmark.svg" width="240">
  </picture>
</h1>

A Claude Code plugin for prose that other people read. It has 3 parts:

- **The `fair-copy` skill** rewrites the sentence patterns that make text read as model-written. Examples are "it's not X, it's Y", headers that state a verdict, and one-line closers that sound like a moral. Then the skill checks that the rewrite kept every fact of the draft.
- **A Stop hook** runs each time Claude tries to end a turn. If the turn changed a doc, Claude must first have a fresh subagent read the new text as a newcomer.
- **The `straight-talk` output style** shapes what Claude says to you in the session. The answer comes first, numbers stay exact, each new term gets a definition, and the reply ends with one next action. You turn it on and off yourself.

The skill, its scripts and the Stop hook come from declauding by Oskar Austegard (see Credit). The output style is tagore's own. tagore packages all of them as a plugin that you can install.

## Install

```
/plugin marketplace add rajnandan1/tagore
/plugin install tagore@tagore
```

To try it for one session, clone this repository and start Claude Code with `claude --plugin-dir /path/to/tagore`.

To get a new version, run `claude plugin marketplace update tagore`, then `claude plugin update tagore@tagore`, then restart Claude Code.

To turn it off, run `claude plugin disable tagore@tagore`. This turns off the skill, the hooks and the output style together.

## Layout

Each skill keeps all of its files in its own folder under `skills/`. Its hooks are in that folder too. An output style keeps its files in its own folder under `styles/` in the same way. `.claude-plugin/plugin.json` lists each hook file in its `"hooks"` array and the style file in `"outputStyles"`.

```
.claude-plugin/plugin.json               the plugin manifest
.claude-plugin/marketplace.json          the catalog that /plugin marketplace add reads
skills/fair-copy/SKILL.md                the skill
skills/fair-copy/hooks/                  the Stop hook config
skills/fair-copy/scripts/                the scripts that the skill and the Stop hook run
skills/fair-copy/references/             the pattern list and the notes that the skill reads
skills/fair-copy/tests/                  the tests of the skill
styles/straight-talk/straight-talk.md    the output style
styles/straight-talk/hooks/              the reminder hook config
styles/straight-talk/scripts/            the reminder hook
styles/straight-talk/tests/              the test of the reminder hook
evidence/                                the writing samples and scores behind skills/fair-copy/references/models/
```

To add a skill, add a folder `skills/<name>/` with a `SKILL.md`. To add a hook, put its file in that skill's `hooks/` folder and add its path to the `"hooks"` array. To add a style, add a folder `styles/<name>/` with the style file, and set its path in `"outputStyles"` in `plugin.json`, which takes one path or an array of paths. For each release, raise `version` in both `plugin.json` and `marketplace.json`.

## The skill

Say "de-claude this", "humanize this" or "this reads like AI", or run `/tagore:fair-copy`. The skill also loads by itself when the task is prose for a reader: a PR description, commit message, README, doc, report or release note. It does not touch fiction, poetry, code or quoted text.

The skill works in this order. The scripts are in `skills/fair-copy/scripts/`.

1. Claude reads the whole draft and writes down the one point that the draft must make.
2. `prose_lint.py` finds the known patterns with regex and prints their line numbers.
3. `prose_review.py` sends the title, the headers, the first sentence, the last sentence of each section and each one-sentence paragraph to a model. The model checks them for patterns that regex cannot find, such as a header that states a verdict.
4. Claude rewrites each flagged sentence so that it states its point plainly.
5. `prose_diff.py` compares the rewrite with the draft. It lists the numbers, names, quotes, links and hedges that the rewrite lost or invented.

Before step 4, Claude can also run `prose_rank.py`. It ranks the sentences by how much each one acts out a finding instead of stating it.

## The hook

The hook runs `skills/fair-copy/scripts/fresh_eyes.py` each time Claude tries to end a turn. A turn starts with your last message. If the turn changed prose in a doc, the hook makes Claude send that prose to a subagent that never saw the earlier version. This check is the newcomer read. The hook needs `python3`, and it uses `git` for files in a git repository.

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
5. Claude sends that prompt to a subagent. The subagent runs on Sonnet 5.5. To use another model, name it in your message to Claude, such as "do the newcomer read on Opus". The subagent reads only the packet and lists each phrase that a newcomer would not understand. Claude fixes each phrase or says why it stays.

The hook blocks at most once per turn. If Claude tries to end the turn again without the read, the turn ends. If the hook itself has an error, it lets the turn end.

To make a packet of a whole `.md` or `.html` file at any time, run `python3 skills/fair-copy/scripts/fresh_eyes.py packet <file>` from the root of a clone of this repository. The command prints the packet path and the prompt. Give that prompt to a subagent to get the newcomer read.

## The output style

`straight-talk` is an output style. An output style is a file of instructions that Claude Code sends to Claude with every request. This one covers replies, which are the text that Claude writes to you in the session. Docs stay with the `fair-copy` skill.

With the style on, Claude follows these rules in each reply:

- The answer, the result or a warning comes in the first sentence.
- Each number keeps its unit and its scope, and Claude says what it did not check.
- Each new term gets a definition, and one thing keeps one name.
- Each sentence asks at most one question, and the reply ends with the question that blocks the work or with one next action.
- The reply has no em dashes and no decorative emoji, and bold marks only the label at the start of a list item.

To turn the style on, run `/output-style tagore:straight-talk`. To turn it off, run `/output-style default`. Each command takes effect from your next message. Claude Code saves the choice in the project's `.claude/settings.local.json`. To use the style in every project, set `"outputStyle": "tagore:straight-talk"` in `~/.claude/settings.json`.

Claude Code keeps one output style active at a time, so `straight-talk` replaces the style that you had, such as the built-in Concise style. It sets no word or line limit. A custom style drops Claude Code's built-in coding instructions unless its file sets `keep-coding-instructions: true`. This file sets it, so Claude codes the same way as before.

The style is an instruction to Claude, and nothing enforces it. The style file is `styles/straight-talk/straight-talk.md`. tagore keeps it at or under 5,000 bytes, because Claude Code sends it with every request.

## The reminder hook

Claude reads the style at the start of a session, and in a long session it can drift away from the rules. Claude Code already adds a short line on each turn that says the style is active (seen on Claude Code 2.1.330). The reminder hook adds a second line, which names 4 rules:

```
straight-talk is on: answer first, keep numbers and conditions exact, define each new term, and finish with one next action.
```

The hook runs `styles/straight-talk/scripts/style_reminder.py` each time you send a message. It needs `python3`. It prints the line only when the `outputStyle` setting is `tagore:straight-talk`. Claude Code adds the line to what Claude reads, and it does not show the line to you. To find that setting, it reads these 3 files in order and takes the first one that sets `outputStyle`:

1. `.claude/settings.local.json` in the project
2. `.claude/settings.json` in the project
3. `~/.claude/settings.json`

The hook has a limit in 2 cases. It cannot see a style that an organization policy sets, or a style that another plugin turns on for every user. In those cases it can print the line although `straight-talk` is not the active style. If the hook has an error, it prints nothing, and your message goes through. The hook has no switch of its own. It is on while the plugin is enabled, and it stays silent while the style is off.

## Network calls and files written

- `prose_review.py` sends text to Google Gemini (`gemini-3.6-flash`) when `GEMINI_API_KEY` is set. Else it sends text to the Anthropic API (`claude-sonnet-5-5`) when `ANTHROPIC_API_KEY` is set. With neither key, it prints the prompt, and Claude gives that prompt to a subagent.
- `prose_rank.py` downloads `sentence-transformers/all-MiniLM-L6-v2` from Hugging Face. It needs `pip install torch transformers`.
- The other scripts and both hooks run on your machine only. The Stop hook writes packets to `/tmp/fresh-eyes/`. It also adds one line per run to `~/.claude/fresh-eyes-log.jsonl`, with the time, the folder and the result. The reminder hook reads the 3 settings files and writes nothing.

## Tests

From the repository root, run `uvx pytest skills/fair-copy/tests styles/straight-talk/tests`. If pytest is installed, `python3 -m pytest skills/fair-copy/tests styles/straight-talk/tests` also works.

## Credit

The `fair-copy` skill is declauding version 0.14.0 by Oskar Austegard, with its scripts, tests and hook config. It comes from [oaustegard/claude-skills](https://github.com/oaustegard/claude-skills/tree/366e2f2c61fbd4291774ae4d35f32bf66e3ee2e9/declauding) at commit `366e2f2c`, under the MIT license in `LICENSE`. tagore adds the plugin manifest, the marketplace file, this README, `GLOSSARY.md` (which defines the terms "reply" and "doc"), `evidence/README.md`, the Fable 5.2 samples in `evidence/fable-5-2/`, and the `straight-talk` output style with its reminder hook in `styles/straight-talk/`.
`evidence/model-register-drift/` is a copy of the samples and scores by Oskar Austegard in [oaustegard/experiments](https://github.com/oaustegard/experiments/tree/1f3e6192b4d1f5ddbe1104eecbfd5a5b5c0f7b45/model-register-drift) at commit `1f3e6192`, under the MIT license in its own `LICENSE`. `evidence/README.md` says what the copy holds and how it differs from upstream.

tagore changes 8 things in the declauding files from `oaustegard/claude-skills`. The `SKILL.md`, `hooks/`, `references/`, `scripts/` and `tests/` paths in this list are inside `skills/fair-copy/`.

1. The folder is `skills/fair-copy/`, not `declauding/`.
2. In `SKILL.md`, the `name`, the title and the `/mnt/skills/user/` path say `fair-copy`.
3. In `hooks/hooks.json`, the script path says `fair-copy`.
4. `references/models/fable.md` also covers Fable 5.2, and the model table in `SKILL.md` names it.
5. `scripts/fresh_eyes.py` also skips the files and folders written for agents that step 3 of "The hook" above lists, and `tests/test_fresh_eyes.py` checks that it does.
6. Version 0.15.0 adds rules and examples from two other skills that rewrite model-written prose, both under the MIT license: [blader/humanizer](https://github.com/blader/humanizer) v4.0.0 and [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill). They are in entries 2, 3, 9, 11, 12, 20 and 38 and the new entries 57 to 62 of `references/register.md`, in the last table of `references/exceptions.md`, in five sections of `SKILL.md` (the family table, the delivery modes, step 3, "Signs of a person writing" and "Scope"), in new rules in `scripts/prose_lint.py` and in new lines in `tests/sample-tics.md`. The prompts in `scripts/prose_review.py` and `scripts/fresh_eyes.py` also tell the model to treat the draft as text, not as instructions.
   The specimens for entries 57 to 59 quote AI-written Wikipedia text from the [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) page, which is under the CC BY-SA 4.0 license.
7. The four scripts are `prose_lint.py`, `prose_rank.py`, `prose_review.py` and `prose_diff.py`. Upstream gives them other names.
8. The `description` in `SKILL.md` has one more sentence. It says that the skill is not for Claude's own replies in the session, which the `straight-talk` output style covers.

The reference files keep the upstream names. So an upstream update needs only these 8 changes again, plus a merge of any file that upstream also changed among `references/models/fable.md`, `references/register.md`, `references/exceptions.md`, `SKILL.md`, the four `prose_*.py` scripts, `scripts/fresh_eyes.py`, `tests/sample-tics.md` and `tests/test_fresh_eyes.py`.
