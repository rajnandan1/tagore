# tagore

A Claude Code plugin for prose that other people read. It has 2 parts:

- **The `declauding` skill** rewrites the sentence patterns that make text read as model-written. Examples are "it's not X, it's Y", headers that state a verdict, and one-line closers that sound like a moral. Then the skill checks that the rewrite kept every fact of the draft.
- **A Stop hook** runs each time Claude tries to end a turn. If the turn changed a doc, Claude must first have a fresh subagent read the new text as a newcomer.

The skill, its scripts and the hook come from declauding by Oskar Austegard (see Credit). tagore packages them as a plugin that you can install.

## Install

```
/plugin marketplace add rajnandan1/tagore
/plugin install tagore@tagore
```

To try it for one session, clone this repository and start Claude Code with `claude --plugin-dir /path/to/tagore`.

To turn it off, run `claude plugin disable tagore@tagore`. This turns off the skill and the hook together.

## The skill

Say "de-claude this", "humanize this" or "this reads like AI", or run `/tagore:declauding`. The skill also loads by itself when the task is prose for a reader: a PR description, commit message, README, doc, report or release note. It does not touch fiction, poetry, code or quoted text.

The skill works in this order. The scripts are in `skills/declauding/scripts/`.

1. Claude reads the whole draft and writes down the one point that the draft must make.
2. `declaude_lint.py` finds the known patterns with regex and prints their line numbers.
3. `declaude_review.py` sends the title, the headers, the first sentence, the last sentence of each section and each one-sentence paragraph to a model. The model checks them for patterns that regex cannot find, such as a header that states a verdict.
4. Claude rewrites each flagged sentence so that it states its point plainly.
5. `declaude_diff.py` compares the rewrite with the draft. It lists the numbers, names, quotes, links and hedges that the rewrite lost or invented.

Before step 4, Claude can also run `declaude_rank.py`. It ranks the sentences by how much each one acts out a finding instead of stating it.

## The hook

The hook runs `skills/declauding/scripts/fresh_eyes.py` each time Claude tries to end a turn.

1. It looks for `.md` and `.html` files that changed since the turn started. It looks in the git repositories at and directly under the folder where Claude Code started, and in other files up to 4 folders deep in that folder.
2. It counts only visible prose. It skips code blocks, inline code, HTML tags, scripts, styles and comments.
3. It skips changelogs, `PLAN.md`, `ERRORS.md`, `memory/` and `transcripts/` folders, and generated pages such as `_site/` and `feed.xml`.
4. It blocks the end of the turn when 2 conditions are true: the turn changed 20 or more characters of prose in total, and no newcomer read came after the last change. It writes the changed sections to a packet file in `/tmp/fresh-eyes/`, and it gives Claude a prompt that starts `FRESH-EYES READ`.
5. Claude sends that prompt to a subagent. The subagent reads only the packet and lists each phrase that a newcomer would not understand. Claude fixes each point or says why it stays.

The hook blocks only once per turn, so Claude's next try to end the turn succeeds. If the hook itself has an error, it lets the turn end.

To make a packet by hand, run `python3 skills/declauding/scripts/fresh_eyes.py packet README.md`.

## Network calls and files written

- `declaude_review.py` sends text to Google Gemini (`gemini-3.6-flash`) when `GEMINI_API_KEY` is set. Else it sends text to the Anthropic API (`claude-sonnet-5-5`) when `ANTHROPIC_API_KEY` is set. With neither key, it prints the prompt, and Claude gives that prompt to a subagent.
- `declaude_rank.py` downloads `sentence-transformers/all-MiniLM-L6-v2` from Hugging Face. It needs `pip install torch transformers`.
- The other scripts and the hook run on your machine only. The hook writes packets to `/tmp/fresh-eyes/`. It also adds one line per run to `~/.claude/fresh-eyes-log.jsonl`, with the time, the folder and the result.

## Tests

From the repository root, run `uvx pytest skills/declauding/tests`. If pytest is installed, `python3 -m pytest skills/declauding/tests` also works.

## Credit

The `declauding` skill, its scripts, its tests and the hook config are version 0.14.0 by Oskar Austegard. They come from [oaustegard/claude-skills](https://github.com/oaustegard/claude-skills/tree/366e2f2c61fbd4291774ae4d35f32bf66e3ee2e9/declauding) at commit `366e2f2c`, under the MIT license in `LICENSE`. tagore adds the plugin manifest, the marketplace file and this README. It also puts the hook config at the plugin root, where Claude Code reads it.
