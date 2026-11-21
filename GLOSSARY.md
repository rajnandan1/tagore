# tagore

tagore is a Claude Code plugin that shapes the prose Claude writes, so that the reader understands it on one read.

## Language

**Reply**:
Text that Claude writes to the user inside the session, such as an answer, a question or a status summary at the end of a turn.
_Avoid_: response, chat message, output

**Doc**:
Prose meant for a reader outside the session, whether Claude or the user saves or posts it, such as a PR description, a commit message, a README, a Linear issue or a Slack message. A draft that Claude shows in the session before it is posted is a doc.
_Avoid_: deliverable, document

**Thread comment**:
A comment posted in a PR review, an issue or a chat thread outside the session. It is a doc.
_Avoid_: reply
