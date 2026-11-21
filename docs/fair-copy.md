# The `fair-copy` skill

A skill is a folder of instructions and scripts that Claude loads for one kind of task. The `fair-copy` skill rewrites the sentence patterns that make text read as model-written. Examples are "it's not X, it's Y", headers that state a verdict, and one-line closers that sound like a moral. Then the skill checks that the rewrite kept every fact of the draft.

## Call the skill

Say "de-claude this", "humanize this" or "this reads like AI", or run `/tagore:fair-copy`. The skill also loads by itself when the task is prose for a reader: a PR description, commit message, README, doc, report or release note. It does not touch fiction, poetry, code or quoted text.

## The 5 steps of the skill

The skill works in this order. The scripts are in `skills/fair-copy/scripts/`.

1. Claude reads the whole draft and writes down the one point that the draft must make.
2. `prose_lint.py` finds the known patterns with regex and prints their line numbers.
3. `prose_review.py` sends the title, the headers, the first sentence, the last sentence of each section and each one-sentence paragraph to a model. The model checks them for patterns that regex cannot find, such as a header that states a verdict.
4. Claude rewrites each flagged sentence so that it states its point plainly.
5. `prose_diff.py` compares the rewrite with the draft. It lists the numbers, names, quotes, links and hedges that the rewrite lost or invented.

Before step 4, Claude can also run `prose_rank.py`. It ranks the sentences by how much each one acts out a finding instead of stating it.

Step 3 sends text to a model API when an API key is set. `prose_rank.py` downloads a model from Hugging Face. [Network calls and files written](network-and-files.md) gives the details.
