# Hooks

A hook is a command that Claude Code runs at a fixed point in a session. tagore has 2 hooks:

- [The Stop hook](#the-stop-hook) runs each time Claude tries to end a turn. If the turn changed a doc, the hook makes Claude send the new text to a fresh subagent.
- [The reminder hook](#the-reminder-hook) runs each time you send a message. While the `straight-talk` output style is on, it reminds Claude of 4 rules of the style.

Both hooks are on while the plugin is enabled.

## The Stop hook

The Stop hook runs `skills/fair-copy/scripts/fresh_eyes.py` each time Claude tries to end a turn. A turn starts with your last message. If the turn changed prose in a doc, the hook makes Claude send that prose to a subagent that never saw the earlier version. This check is the newcomer read. The hook needs `python3`, and it uses `git` for files in a git repository.

1. It looks for `.md` and `.html` files that changed during the turn. In a git repository, it counts commits made during the turn, uncommitted edits and new files. It checks the repository in the folder where Claude Code started and each repository one folder below it. Outside git repositories, it checks files saved during the turn, up to 4 folders deep in the folder where Claude Code started.
2. Only visible prose counts. Code blocks, inline code, HTML tags, scripts, styles and HTML comments do not count.
3. It skips some files, folders and parts of files. Examples are changelogs, generated pages, `CLAUDE.md` and everything in `.claude/`. [Files that the Stop hook skips](skipped-files.md) gives the full list.
4. It blocks the end of the turn when 2 conditions are true: 20 or more characters of prose were added, removed or rewritten in total across all changed files, and Claude did not send a subagent a prompt that contains `FRESH-EYES READ` after the last change. The hook writes a packet file to `/tmp/fresh-eyes/`. For a Markdown file, the packet holds each changed section whole. For an HTML file, it holds the visible text within 25 lines of each change. Then the hook gives Claude the `FRESH-EYES READ` prompt to send.
5. Claude sends that prompt to a subagent. The subagent runs on Sonnet 5.5. To use another model, name it in your message to Claude, such as "do the newcomer read on Opus". The subagent reads only the packet and lists each phrase that a newcomer would not understand. Claude fixes each phrase or says why it stays.

The hook blocks at most once per turn. If Claude tries to end the turn again without the read, the turn ends. If the hook itself has an error, it lets the turn end.

To make a packet of a whole `.md` or `.html` file at any time, run `python3 skills/fair-copy/scripts/fresh_eyes.py packet <file>` from the root of a clone of the [tagore repository](https://github.com/rajnandan1/tagore). The command prints the packet path and the prompt. Give that prompt to a subagent to get the newcomer read.

## The reminder hook

Claude reads the [`straight-talk` output style](straight-talk.md) at the start of a session, and in a long session it can drift away from the rules. Claude Code already adds a short line on each turn that says the style is active (seen on Claude Code 2.1.330). The reminder hook adds a second line, which names 4 rules:

```
straight-talk is on: answer first, keep numbers and conditions exact, define each new term, and finish with one next action.
```

The hook runs `styles/straight-talk/scripts/style_reminder.py` each time you send a message. It needs `python3`. It prints the line only when the `outputStyle` setting is `tagore:straight-talk`. Claude Code adds the line to what Claude reads, and it does not show the line to you. To find that setting, it reads these 3 files in order and takes the first one that sets `outputStyle`:

1. `.claude/settings.local.json` in the project
2. `.claude/settings.json` in the project
3. `~/.claude/settings.json`, or `settings.json` in the folder that the `CLAUDE_CONFIG_DIR` environment variable names, when it is set

The hook has a limit in 3 cases. It cannot see a style that an organization policy sets, a style that another plugin turns on for every user, or a style that the `--settings` flag sets on the command line. In those cases it can print the line although `straight-talk` is not the active style, or stay silent although it is. If the hook has an error, it prints nothing, and your message goes through. The hook has no switch of its own. It is on while the plugin is enabled, and outside those 3 cases it stays silent while the style is off.
