# Quick start

This page installs tagore and uses each of its 3 parts once. You need Claude Code. tagore has 2 hooks, which are commands that Claude Code runs at fixed points in a session. Both hooks need `python3`, and one of them, the Stop hook, uses `git` for files in a git repository.

## 1. Install the plugin

Run these 2 commands in Claude Code:

```
/plugin marketplace add rajnandan1/tagore
/plugin install tagore@tagore
```

To try it for one session, clone the [tagore repository](https://github.com/rajnandan1/tagore) and start Claude Code with `claude --plugin-dir /path/to/tagore`.

## 2. Rewrite a draft with the skill

Give Claude a draft and say "de-claude this", "humanize this" or "this reads like AI", or run `/tagore:fair-copy`. If you paste the draft into the session, Claude returns the rewritten text. If you name a file, Claude rewrites the file in place and reports a summary of the changes.

[The `fair-copy` skill](fair-copy.md) lists the 5 steps that the skill follows.

## 3. Let the Stop hook check a file that Claude changed

Ask Claude to write or change a `.md` or `.html` file. When Claude tries to end the turn, the Stop hook looks for prose that changed during the turn. If 20 or more characters of prose changed, the hook makes Claude send the new text to a subagent. A subagent is a separate Claude that Claude starts for one task, and this one never saw the earlier version of the text. The subagent lists each phrase that a reader new to the project would not understand, and Claude fixes each phrase or says why it stays.

You do nothing in this step. [Hooks](hooks.md#the-stop-hook) says which files count and when the hook stays silent.

## 4. Turn on the output style

Run this command:

```
/output-style tagore:straight-talk
```

From your next message, Claude puts the answer in the first sentence of each reply, keeps numbers exact, defines each new term and ends with one next action. To turn the style off, run `/output-style default`.

[The `straight-talk` output style](straight-talk.md) gives the rules and says how to use the style in every project.

## Update tagore

To get a new version, run `claude plugin marketplace update tagore`, then `claude plugin update tagore@tagore`, then restart Claude Code.

## Turn tagore off

To turn it off, run `claude plugin disable tagore@tagore`. This turns off the skill, the hooks and the output style together.
