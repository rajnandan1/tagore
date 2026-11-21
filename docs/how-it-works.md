# How it works

tagore sorts the prose that Claude writes into 2 kinds, and each part of tagore works on one kind.

- A **reply** is text that Claude writes to you inside the session, such as an answer, a question or a status summary at the end of a turn.
- A **doc** is prose meant for a reader outside the session, such as a PR description, a commit message, a README, a Linear issue or a Slack message. A draft that Claude shows in the session before it is posted is a doc.

## What each part works on

tagore has 3 parts: the `fair-copy` skill, the Stop hook and the `straight-talk` output style. The output style comes with a second hook, the reminder hook.

| Part | Text that it works on | When it runs |
|---|---|---|
| [The `fair-copy` skill](fair-copy.md) | Docs | When you ask for it, and by itself when the task is prose for a reader |
| [The Stop hook](hooks.md#the-stop-hook) | `.md` and `.html` files that changed during the turn | Each time Claude tries to end a turn |
| [The `straight-talk` output style](straight-talk.md) | Replies | With every request, while the style is on |
| [The reminder hook](hooks.md#the-reminder-hook) | Replies | Each time you send a message, while the `outputStyle` setting is `tagore:straight-talk` |

The Stop hook sees a doc only when the doc is a `.md` or `.html` file. It does not see a doc that Claude posts, such as a PR description.

## How tagore checks a doc

1. Claude writes a draft.
2. The `fair-copy` skill looks for the sentence patterns that make text read as model-written. A script finds the known patterns with regex. A model checks the title, the headers, the first sentence, the last sentence of each section and each one-sentence paragraph for patterns that regex cannot find. [Network calls and files written](network-and-files.md) says which model.
3. Claude rewrites each flagged sentence so that it states its point plainly.
4. The script `prose_diff.py` compares the rewrite with the draft. It lists the numbers, names, quotes, links and hedges that the rewrite lost or invented. A hedge is a phrase that limits how sure a claim is.
5. When Claude tries to end the turn, the Stop hook checks whether the turn changed prose in a `.md` or `.html` file. If it did, a subagent that never saw the earlier version reads the new text as a newcomer. The subagent lists each phrase that a newcomer would not understand, and Claude fixes each phrase or says why it stays.

[The `fair-copy` skill](fair-copy.md) gives steps 2 to 4 in full. The skill and the Stop hook check different things. The skill checks how each sentence sounds and that the rewrite kept every fact of the draft. The Stop hook checks that a reader with no context understands the text.

## How tagore shapes a reply

An output style is a file of instructions that Claude Code sends to Claude with every request. While the `straight-talk` style is on, those instructions tell Claude how to write each reply: the answer comes first, numbers stay exact, each new term gets a definition, and the reply ends with one next action.

The style is an instruction to Claude, and nothing enforces it. In a long session, Claude can drift away from the rules. So the reminder hook adds one line that names 4 of the rules each time you send a message. [Hooks](hooks.md#the-reminder-hook) shows that line.
