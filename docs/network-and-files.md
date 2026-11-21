# Network calls and files written

- `prose_review.py` sends text to Google Gemini (`gemini-3.6-flash`) when `GEMINI_API_KEY` is set. Else it sends text to the Anthropic API (`claude-sonnet-5-5`) when `ANTHROPIC_API_KEY` is set. With neither key, it prints the prompt, and Claude gives that prompt to a subagent.
- `prose_rank.py` downloads `sentence-transformers/all-MiniLM-L6-v2` from Hugging Face. It needs `pip install torch transformers`.
- The other scripts and both hooks run on your machine only. The Stop hook writes packets to `/tmp/fresh-eyes/`. It also adds one line per run to `~/.claude/fresh-eyes-log.jsonl`, with the time, the folder and the result. The reminder hook reads the 3 settings files and writes nothing.

[The `fair-copy` skill](fair-copy.md) says which text `prose_review.py` sends. [Hooks](hooks.md#the-stop-hook) says what a packet holds.
