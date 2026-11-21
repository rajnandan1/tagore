# Fable 5.1 and Fable 5.2

Each version was sampled twice on one prompt. Fable 5.2 drafts carry less of the
register than Fable 5.1 drafts: fewer lint hits, no em dashes, no semicolons, and
no "the one that stung". Anthropic's testers rated Fable 5.2's writing above Fable
5.1's and similar in clarity to Opus 5.5's.

## Editing a draft Fable wrote

Expect a light pass, mostly headers and typography.

1. Remove bold from list-item leads and from the takeaway line at the end of a
   list; Fable puts its maxims there (entries 29, 30, 12). Fable 5.2 still bolds
   every lead, but the lead is usually a full sentence that states a cause: *Large
   values stalled Redis.* Unbold it and keep the sentence. In a closing checklist,
   the maxim moves to the sentence after the lead: *A blended median will always
   flatter a cache.* Cut it, or replace it with the measured fact.
2. Rewrite an "X, not Y" closer as a plain statement (entries 2 and 12). Fable
   5.1 wrote one in each sample; Fable 5.2 wrote none.
3. Search for "the one that stung" and "the part that stung" and cut the
   designation (entry 3). The linter catches "the part that" but not "the one
   that". Fable 5.1 used it in both samples; Fable 5.2 in neither.
4. On a Fable 5.2 draft, read the headers yourself. The linter flags every
   "What…" and "Why…" header as coy, but most are plain labels: *Why p99 got
   worse*. Rewrite only the header that teases a reveal: *What the dashboard hid*
   (entry 7).
5. On a Fable 5.2 draft, check the line that sets up a reversal: *We announced
   the win and moved on.* Cut it when the next paragraph states the reversal
   anyway (entries 1 and 8). Keep it when it carries a fact, such as how long
   the wrong reading lasted.
6. On a Fable 5.2 draft, find the sentences where a tool or a number acts: *A
   cache earns its place*, *The cache hid a problem*. Say who did what instead
   (entry 4).
7. Keep a Fable 5.2 closing sentence that states a fact about the case: *Neither
   was true for us.* Both samples ended with a list of conditions and one short
   sentence of this kind. It states a fact, so it is earned (see Earned
   exceptions).

## Running the pass as Fable

Fable 5.1: not observed. Use the general workflow.

Fable 5.2: not observed in a pass. Anthropic documents one risk: Fable 5.2
follows writing rules closely, so a hard limit on sentence length makes its prose
choppy. Apply each register entry as a test of the sentence in front of you, not
as a rule for every sentence. After the pass, read the rewrite once against
Overcorrection and entries 15 and 53 to 56: runs of short sentences of one
length, dropped *that*, stacked nouns. If the session also carries a house style
guide, check that the two rule sets did not stack into fragments.

Evidence: Fable 5.1, `oaustegard/experiments` `model-register-drift/FABLE-ADDENDUM.md`
(two samples, reconstructed prompt). Fable 5.2, `evidence/fable-5-2/` in the
tagore repository (two samples, 2026-11-12, same prompt, not blind-judged), and
Anthropic's [Prompting Claude Fable 5.2](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2).
