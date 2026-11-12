# Fable 5.2 samples

These 2 samples back the Fable 5.2 lines in `skills/plain-prose/references/models/fable.md`. They repeat the Fable 5.1 run in `oaustegard/experiments` `model-register-drift/FABLE-ADDENDUM.md` on `claude-fable-5-2`, on 2026-11-12.

## Method

Each sample is one Claude Code print-mode run. The run loaded no user settings, plugins, hooks, MCP servers or tools. A one-line system prompt replaced the Claude Code system prompt. Asked in a separate run, the model said that no style instruction was in its context.

```
claude -p --setting-sources project --model claude-fable-5-2 --effort high \
  --tools "" --strict-mcp-config --no-session-persistence \
  --system-prompt "You are Claude, made by Anthropic." "$PROMPT"
```

The prompt rebuilds the upstream prompt from its description in `model-register-drift/RESULTS.md`. The last sentence is new, because print mode needs the post as the reply:

> Write a blog post titled "Why we removed our cache" for an audience of backend engineers. The premise: we put a Redis read-through cache in front of Postgres, and we removed it after four months because p99 latency got worse. Invent your own numbers and details. Keep it under 900 words. Reply with the post only, in Markdown.

## Scores

`scores.txt` is the output of upstream `model-register-drift/score.py`, pointed at the linter in this repository (version 0.14.0). It scores the 2 Fable 5.2 samples next to the upstream Fable 5.1 and Opus 5 samples, so all rows come from the same linter. The upstream addendum used an older linter, so its numbers differ from these.

| Sample | Lint hits per 1,000 words | Semicolons | Bold list leads | "the one/part that stung" |
| --- | --- | --- | --- | --- |
| fable-5-1-a | 3.05 | 2 | 8 | 1 |
| fable-5-1-b | 9.92 | 2 | 4 | 1 |
| fable-5-2-a | 6.02 | 0 | 10 | 0 |
| fable-5-2-b | 1.20 | 0 | 7 | 0 |

## Limits

- There are 2 samples on 1 prompt. The prompt asks for a blog post about a result that surprised the team, which invites staged reveals more than a reference doc does.
- Upstream sampled Fable 5.1 through the bare API with no system prompt. These runs used Claude Code with a one-line system prompt.
- No blind pairwise judging was run, unlike the upstream addendum.
- The 2 samples invent the same details: June to October, about 2,400 requests per second, `/accounts/:id/summary`, a five-minute TTL and an 82% or 83% hit rate. Upstream saw the same pattern in Fable 5.1, so the 2 samples are less independent than 2 separate drafts.
