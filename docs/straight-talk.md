# The `straight-talk` output style

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

In a long session, Claude can drift away from the rules of the style. [The reminder hook](hooks.md#the-reminder-hook) adds one line on each turn to bring them back.
