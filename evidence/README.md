# Evidence

The `plain-prose` skill rewrites the sentence patterns that make text read as written by a model. Upstream, the skill is called declauding. Each file in `skills/plain-prose/references/models/` tells the skill which of those patterns one Claude model family writes most. This folder holds the writing samples and the scores behind those files.

## What is here

- `model-register-drift/` is a copy of the [model-register-drift](https://github.com/oaustegard/experiments/tree/1f3e6192b4d1f5ddbe1104eecbfd5a5b5c0f7b45/model-register-drift) folder of `oaustegard/experiments` at commit `1f3e6192`, by Oskar Austegard, under the MIT license in `model-register-drift/LICENSE`. Its `RESULTS.md` gives the method and the results, and its `FABLE-ADDENDUM.md` covers Fable 5.1. `blind/` holds 10 of the samples under shuffled names (`blind_key.json` maps them) for the blind judging that `RESULTS.md` describes. The other files are the scripts, inputs and outputs of the scoring and the judging that `RESULTS.md` describes, and `ERRORS.md` lists what went wrong during the upstream runs. The copy is the same as the upstream folder, with 2 differences:
  - It adds `LICENSE` from the root of `oaustegard/experiments`.
  - `score.py` runs the linter of this repository, `skills/plain-prose/scripts/declaude_lint.py`. It finds that file from its own location, so it works from any folder. Upstream it runs `/mnt/skills/user/declauding/scripts/declaude_lint.py`.

  One upstream script does not work here: `fetch_samples.py` downloads the samples from issue 244 of `oaustegard/claude-workspace`, which is a private repository. You do not need it, because the samples are already in `samples/`. `ISSUE-244.md` is the upstream copy of that issue.
- `fable-5-2/` holds 2 Fable 5.2 samples, made for tagore on 2026-11-12. Its `README.md` gives the method and the limits.

Each sample is one blog post, "Why we removed our cache", by one model. The Haiku, Opus and Sonnet samples answer the original prompt from issue 244. The Fable 5.1 samples answer a prompt that upstream rebuilt from its description in `RESULTS.md`, and the Fable 5.2 samples answer a prompt rebuilt the same way, as `fable-5-2/README.md` says. The original prompt is in none of these files.

| Model | Samples |
| --- | --- |
| Haiku 4.5 | `model-register-drift/samples/haiku-4-5-a.md`, `haiku-4-5-b.md` |
| Opus 4.6 | `model-register-drift/samples/opus-4-6-a.md` |
| Opus 4.8 | `model-register-drift/samples/opus-4-8-a.md`, `opus-4-8-b.md` |
| Opus 5 | `model-register-drift/samples/opus-5-a.md`, `opus-5-b.md` |
| Sonnet 4.6 | `model-register-drift/samples/sonnet-4-6-a.md`, `sonnet-4-6-b.md` |
| Sonnet 5 | `model-register-drift/samples/sonnet-5-a.md` |
| Fable 5.1 | `model-register-drift/samples/fable-5-1-a.md`, `fable-5-1-b.md` |
| Fable 5.2 | `fable-5-2/fable-5-2-a.md`, `fable-5-2-b.md` |

Two cautions apply to the upstream write-ups:

- The score tables in `RESULTS.md` and `FABLE-ADDENDUM.md` come from earlier runs with other linter versions, so the same sample has different numbers in each table and in a new run. Compare only samples that you score in the same run.
- `RESULTS.md` opens with a hand count that its section "Adjudicated register violations" later retracts. The mechanical scan from `score.py` is the part that stands.

## Add your own run

Run these steps from the root of this repository.

1. Make a folder for the model, for example `evidence/opus-5-5/`.
2. Get 2 or more samples. Use the prompt and the `claude -p` command in `evidence/fable-5-2/README.md`, with `--model` set to the model that you test. That prompt is the rebuilt one, so your samples compare most directly with the Fable samples. Save the replies in the new folder, with the folder name as the prefix: `opus-5-5-a.md`, `opus-5-5-b.md` and so on.
3. Write a `README.md` in the new folder with the method and the limits, as `evidence/fable-5-2/README.md` does.
4. Score the new samples next to older samples, in one run. `score.py` scores every `.md` file in one folder, including notes such as the `README.md` from step 3, so first copy only the samples that you want to compare into an empty folder. This example compares Opus 5.5 with Opus 5, because the 2 models share one model file. The Opus 5 samples answer the original prompt, so say in your `README.md` that the prompts differ:

   ```
   d=$(mktemp -d)
   cp evidence/opus-5-5/opus-5-5-?.md evidence/model-register-drift/samples/opus-5-?.md "$d"
   python3 evidence/model-register-drift/score.py "$d" > evidence/opus-5-5/scores.txt
   ```

   The columns of `scores.txt` are these:
   - `words` is the number of words of prose, without code blocks and headers.
   - `hits` is the number of linter hits, without the hits about the whole post.
   - `per1k` is `hits` per 1,000 words, so a lower number means fewer model-written patterns.
   - `staging` counts, per 1,000 words, the hits of the staging family of patterns in `skills/plain-prose/references/register.md`, and `flat` counts the hits of its encyclopedic family. Some linter categories, such as `flat-certainty`, `reversal` and `totalizing`, are in neither list in `score.py`, so the 2 columns can add up to less than `per1k`.
   - `struct` is the number of hits about the whole post, such as headers.
   - `dash/150` is the number of em dashes per 150 words.
   - `short%` is the percentage of sentences with 5 words or fewer.
   - `1-sent` is the number of paragraphs that are one sentence long, not counting list items, tables and quotes.
5. Find the model file for your model in the model table of `skills/plain-prose/SKILL.md`. For Opus 5.5, it is `skills/plain-prose/references/models/opus-5.md`. If the table says "not yet profiled", add a new file and a row to that table.
6. Write what the samples show into that file, as `skills/plain-prose/references/models/fable.md` does for Fable 5.2. Then name your folder in the `Evidence:` paragraph at the end of the file, for example: "Opus 5.5, `evidence/opus-5-5/` in the tagore repository (two samples, 2026-11-13, the rebuilt cache prompt)."
7. Add a row for the model to the table in this README.
