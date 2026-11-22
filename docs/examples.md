# Examples

Each example on this page comes from a real run of tagore on 2026-11-22. The runs used Claude Code 2.1.330 in print mode, which is the `claude -p` command, with the model `claude-fable-5-2`. Each run started in an empty folder and loaded the tagore plugin at version 0.4.0. [How the runs were made](#how-the-runs-were-made) gives the commands and what else each run loaded.

The page uses 4 runs: 1 for the skill, 1 for the Stop hook and 2 for the output style. No example was picked from several runs. One run shows what a part does. It does not measure how often the part does it.

## The `fair-copy` skill

The draft is the first 9 lines of `evidence/model-register-drift/samples/opus-4-8-a.md`, a blog post that the model Opus 4.8 wrote. The message to Claude was `de-claude this file: draft.md`. The words "de-claude this" call the skill.

The draft before the run:

````` { .text .wrap }
--8<-- "evidence/examples/skill-before.txt"
`````

The draft after the run:

````` { .text .wrap }
--8<-- "evidence/examples/skill-after.txt"
`````

The skill runs 2 scripts on the text, and [The `fair-copy` skill](fair-copy.md) says where they fit in its 5 steps. `prose_lint.py` finds the known sentence patterns that make text read as model-written. `prose_diff.py` compares the rewrite with the draft and lists what the rewrite lost or invented. They gave these results:

- `prose_lint.py` found 3 patterns in the draft: an em dash that holds back the end of a sentence, the header "Why we removed our cache", and 3 em dashes in 183 words. In the rewrite it found 1 pattern, the header. Claude kept the header, and its reply below gives the reason.
- `prose_diff.py` reported 1 finding: the draft has 4 negations and the rewrite has 3. The script counts negations because a lost "not" can turn a claim around. Here the cause is the new wording of "Not because Redis failed, and not because…", as the reply below says. The script reported no lost or new number, name, quote or link.

This is the reply that Claude gave after the rewrite, in full:

````` { .text .wrap }
--8<-- "evidence/examples/skill-report.txt"
`````

The reply names the one sentence that Claude cut. It also reports a problem in the draft itself: the draft gives 2 values for the p99 latency without the cache, 120ms and 110ms. Claude left both values for the author to check.

## The Stop hook

The Stop hook runs each time Claude tries to end a turn. If the turn changed prose in a `.md` or `.html` file, the hook makes Claude send the new text to a subagent that never saw the earlier version. This check is the newcomer read.

This example is a second run, with the same draft and the same message. The first run used the flag `--no-session-persistence`, so Claude Code saved no transcript. The Stop hook reads the transcript to find what the turn changed. Without the transcript it had an error and let the turn end, as [Hooks](hooks.md#the-stop-hook) says it does. The second run left that flag out.

Before the hook ran, Claude tried to end the turn without a newcomer read. Its reply said: "I did the structural review myself rather than with the skill's script, and skipped the newcomer read because the draft is a new post and not a revision of an existing doc."

The Stop hook blocked the end of the turn and gave Claude this message:

````` { .text .wrap }
--8<-- "evidence/examples/hook-message.txt"
`````

Claude sent that prompt to a subagent on Sonnet. This is the report of the subagent:

````` { .text .wrap }
--8<-- "evidence/examples/hook-reader.txt"
`````

After the report, Claude gave this reply:

````` { .text .wrap }
--8<-- "evidence/examples/hook-reply-after.txt"
`````

Claude changed no text after the read, because each open point needs a fact that only the author has. The read gave the author 4 points to answer. Claude had already found 1 of them, the 2 values for p99. The hook puts the changed text in one file, the packet, for the subagent to read. In this run the packet held 2 files: the rewrite, and `draft.orig.md`, a copy of the first draft that Claude saved before the rewrite. So the first part of the report is about the first draft, and the second part is about the rewrite.

## The `straight-talk` output style

One prompt went to Claude 2 times: once with the `outputStyle` setting at `default`, and once with it at `tagore:straight-talk`. The setting is in the `.claude/settings.local.json` file of the folder where the run starts. Claude had no tools in these 2 runs. The prompt:

````` { .text .wrap }
--8<-- "evidence/examples/style-prompt.txt"
`````

The reply with the style off:

````` { .text .wrap }
--8<-- "evidence/examples/style-off.txt"
`````

The reply with the style on:

````` { .text .wrap }
--8<-- "evidence/examples/style-on.txt"
`````

Both replies put the answer in the first sentence. They differ in 4 ways:

- **Definition:** with the style on, the reply says what a sequential scan is where the term first appears: "Postgres reads the whole table (a sequential scan)". With the style off, the reply uses the term with no definition.
- **Guess:** with the style on, the reply marks its guess and says what confirms it: "This is a guess until you see the query plan, because I have not seen the query or the schema."
- **Number:** with the style off, the reply says "a large fraction of the table". With the style on, it says "roughly under 5 to 10 percent".
- **Ending:** with the style off, the reply ends with an offer: "If you paste the query and its `EXPLAIN (ANALYZE, BUFFERS)` output, I can tell you which index shape fits." With the style on, it ends with one action for the user, on a line that starts with "Next:".

## The reminder hook

While the style is on, the reminder hook adds one line to what Claude reads each time you send a message. The hook is the script `styles/straight-talk/scripts/style_reminder.py`. This example runs the script by hand in the 2 folders of the output style example: the folder with the style off and the folder with the style on. In the folder with the style off, the script prints nothing. In the folder with the style on, it prints this line:

````` { .text .wrap }
--8<-- "evidence/examples/reminder-on.txt"
`````

## How the runs were made

The 2 runs for the output style used this command. Each ran in a folder whose `.claude/settings.local.json` file sets `outputStyle`. `<repo>` is the path of a clone of the tagore repository, and `<prompt>` is the prompt above.

```
claude -p --plugin-dir <repo> --setting-sources project,local \
  --model claude-fable-5-2 --strict-mcp-config --no-session-persistence \
  --output-format stream-json --verbose --tools "" -- "<prompt>"
```

The run for the skill used this command, in a folder that held only `draft.md`:

```
claude -p --plugin-dir <repo> --setting-sources project,local \
  --model claude-fable-5-2 --strict-mcp-config --no-session-persistence \
  --output-format stream-json --verbose --permission-mode acceptEdits \
  --allowedTools "Read" "Edit" "Write" "Glob" "Grep" "Bash(python3:*)" \
  "Agent" "Task" "Skill" -- "de-claude this file: draft.md"
```

The run for the Stop hook used the same command with 2 differences: it has no `--no-session-persistence` flag, and its list of allowed tools also has `"Bash(cp:*)"`.

The example for the reminder hook used this command in each of the 2 folders:

```
printf '{"cwd": "%s"}' "$PWD" | python3 <repo>/styles/straight-talk/scripts/style_reminder.py
```

These facts limit what the examples show:

- **Settings:** `--setting-sources project,local` keeps the user's own settings out of a run. One more run, which is not an example on this page, asked Claude with the style off what its context held. Claude answered that it held no output style, no `CLAUDE.md` file and no user writing rule.
- **Other plugins:** each run also loaded the built-in plugins of Claude Code and `orca-agent-view`, a plugin of the terminal app that started the runs.
- **Model APIs:** `prose_review.py` is the script of the skill that can send parts of a draft to a model API. It needs the `GEMINI_API_KEY` or the `ANTHROPIC_API_KEY` environment variable, and neither was set. So no script sent text to a model API. In the run for the skill and in the run for the Stop hook, Claude did not run `prose_review.py` and checked the headers and the first and last sentences itself.
- **First attempt:** one attempt before these runs ended with an argument error before any model call, because the prompt had no `--` in front of it.
- **Files:** `evidence/examples/` in the tagore repository holds the text of each block on this page. The raw output of the runs is not in the repository, because it holds paths and session IDs of the machine that ran them.
