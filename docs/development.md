# Development

This page is for people who change tagore. It covers the layout of the [tagore repository](https://github.com/rajnandan1/tagore), the tests and the build of this site.

## Layout

Each skill keeps all of its files in its own folder under `skills/`. Its hooks are in that folder too. An output style keeps its files in its own folder under `styles/` in the same way. `.claude-plugin/plugin.json` lists each hook file in its `"hooks"` array and the style file in `"outputStyles"`.

```
.claude-plugin/plugin.json               the plugin manifest
.claude-plugin/marketplace.json          the catalog that /plugin marketplace add reads
skills/fair-copy/SKILL.md                the skill
skills/fair-copy/hooks/                  the Stop hook config
skills/fair-copy/scripts/                the scripts that the skill and the Stop hook run
skills/fair-copy/references/             the pattern list and the notes that the skill reads
skills/fair-copy/tests/                  the tests of the skill
styles/straight-talk/straight-talk.md    the output style
styles/straight-talk/hooks/              the reminder hook config
styles/straight-talk/scripts/            the reminder hook
styles/straight-talk/tests/              the test of the reminder hook
docs/                                    the pages of this site
mkdocs.yml                               the config of this site
.github/workflows/docs.yml               the workflow that publishes this site
evidence/                                the writing samples and scores behind skills/fair-copy/references/models/
```

To add a skill, add a folder `skills/<name>/` with a `SKILL.md`. To add a hook, put its file in that skill's `hooks/` folder and add its path to the `"hooks"` array. To add a style, add a folder `styles/<name>/` with the style file, and set its path in `"outputStyles"` in `plugin.json`, which takes one path or an array of paths. For each release, raise `version` in both `plugin.json` and `marketplace.json`.

## Tests

From the repository root, run `uvx pytest skills/fair-copy/tests styles/straight-talk/tests`. If pytest is installed, `python3 -m pytest skills/fair-copy/tests styles/straight-talk/tests` also works.

## This site

The pages of this site are the Markdown files in `docs/`. MkDocs, a tool that turns Markdown files into a website, builds them with the Material theme. The config is `mkdocs.yml`, and you need `uvx` to run MkDocs.

To see the site while you edit it, run this command from the repository root. It prints the address of the site.

```
uvx --with mkdocs-material==9.8.2 mkdocs serve
```

To build the site into `_site/`, run this command. With `--strict`, the build fails on a broken link between pages.

```
uvx --with mkdocs-material==9.8.2 mkdocs build --strict
```

`docs/logo` is a symbolic link to `assets/logo/`, so the site uses the same logo files as the README.

The workflow `.github/workflows/docs.yml` builds the site and publishes it to GitHub Pages on each push to `main` that changes `docs/`, `assets/logo/`, `mkdocs.yml` or the workflow file.

Material for MkDocs reaches its end of life on May 5, 2027. Its successor, Zensical, reads the same `mkdocs.yml`, but Zensical 0.1.3 does not copy the files behind the `docs/logo` link.
