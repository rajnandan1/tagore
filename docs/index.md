# ![tagore](logo/tagore-wordmark.svg#only-light){ width="240" } ![tagore](logo/tagore-wordmark-dark.svg#only-dark){ width="240" }

tagore is a Claude Code plugin for prose that other people read. It has 3 parts:

- **[The `fair-copy` skill](fair-copy.md)** rewrites the sentence patterns that make text read as model-written. Examples are "it's not X, it's Y", headers that state a verdict, and one-line closers that sound like a moral. Then the skill checks that the rewrite kept every fact of the draft.
- **[A Stop hook](hooks.md#the-stop-hook)** runs each time Claude tries to end a turn. If the turn changed a doc, Claude must first have a fresh subagent read the new text as a newcomer.
- **[The `straight-talk` output style](straight-talk.md)** shapes what Claude says to you in the session. The answer comes first, numbers stay exact, each new term gets a definition, and the reply ends with one next action. You turn it on and off yourself.

The skill, its scripts and the Stop hook come from declauding by Oskar Austegard (see [Credit](https://github.com/rajnandan1/tagore#credit)). The output style is tagore's own. tagore packages all of them as a plugin that you can install.

## Install

Run these 2 commands in Claude Code:

```
/plugin marketplace add rajnandan1/tagore
/plugin install tagore@tagore
```

Then open [Quick start](quick-start.md), which uses each of the 3 parts once. To see which part works on which text, read [How it works](how-it-works.md).
