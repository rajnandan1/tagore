# tagore logo

tagore is a Claude Code plugin that rewrites agent-written prose for human readers. It takes its name from Rabindranath Tagore, the Bengali poet who won the 1913 Nobel Prize in Literature. In this file, "Tagore" with a capital T is the poet, and "tagore" in lowercase is the plugin.

![The tagore wordmark: the lowercase letters of tagore hang from one red line along their tops](tagore-wordmark.svg)

Bengali script, which Tagore wrote in, hangs most letters from one line along the top. That line is the matra. The wordmark writes `tagore` the same way, so every letter hangs from one red matra. The symbol is the first letter of the wordmark: a `t` whose crossbar is the matra.

![The tagore symbol: a lowercase t whose crossbar is the red matra](tagore-symbol.svg)

The letters of the wordmark were drawn by hand as SVG paths, so no font can type the wordmark.

## Colours

The logo uses four colours. The two reds take their name from laterite, the red soil of Santiniketan, where Tagore built his school. Red is also the colour of an editor's pen, and tagore edits prose the way an editor does.

| Name | HEX | Use |
|---|---|---|
| Ink | `#1F1D1A` | Letters on light backgrounds |
| Paper | `#F4F0E8` | Letters on dark backgrounds |
| Laterite | `#B83A24` | The matra on light backgrounds |
| Laterite light | `#E8694F` | The matra on dark backgrounds |

Laterite has a contrast of 5.7:1 on white and 5.0:1 on Paper. Laterite light has a contrast of 5.9:1 on `#0D1117`, which is the dark background of GitHub, and 5.3:1 on Ink. WCAG 2.1, the Web Content Accessibility Guidelines, asks for at least 3:1 for graphics, so each value passes.

## Files

All the SVG files have a transparent background, except `favicon.svg`.

| File | Use it for |
|---|---|
| `tagore-wordmark.svg` | The main logo on light backgrounds |
| `tagore-wordmark-dark.svg` | The main logo on dark backgrounds |
| `tagore-wordmark-mono.svg` | The main logo in one colour |
| `tagore-symbol.svg` | The `t` alone on light backgrounds, for avatars and small spaces |
| `tagore-symbol-dark.svg` | The `t` alone on dark backgrounds |
| `tagore-symbol-mono.svg` | The `t` alone in one colour |
| `favicon.svg`, `favicon.ico` | Browser tabs. The `.ico` file holds a 16 px and a 32 px icon. |
| `apple-touch-icon.png` | The 180 px home-screen icon for iOS |

The two `-mono` files paint every shape with `currentColor`. To show one in Ink or in Paper, put the SVG inline in the page and set the CSS `color` property to `#1F1D1A` or `#F4F0E8`. As an `<img>`, a `-mono` file shows in pure black, `#000000`.

The favicon and the iOS icon show the `t` on a square tile of Ink. The `t` is in Paper, and its matra is in Laterite light. This `t` has heavier strokes than the `t` in `tagore-symbol.svg`, so that it stays clear at 16 px. The icons look the same on light and dark backgrounds.

## Rules

- Keep empty space around the logo. Around the wordmark, the space on each side must be at least half the height of the wordmark. Around the symbol, it must be at least a quarter of the width of the symbol.
- Do not show the wordmark narrower than 96 px. Do not show the symbol narrower than 24 px. Below 24 px, use `favicon.svg`.
- Use the `-dark` files on dark backgrounds, because the Ink letters disappear on black.
- Put the logo on a plain area of white, Paper, Ink or a dark colour such as `#0D1117`. On Laterite, the red matra disappears. On a photo or a pattern, the thin matra gets lost. In those cases, put a `-mono` file inline: in Paper on Laterite or on a dark photo or pattern, and in Ink on a light photo or pattern.
- Where you cannot put an SVG inline, such as in a GitHub README, use the files that are not `-mono`, on a plain background.
- Do not change the colours or the proportions. Do not add effects, such as shadows, outlines or gradients.

## Snippets

For a web page, first copy `favicon.ico`, `favicon.svg` and `apple-touch-icon.png` to the root folder of the site. Then add these lines to the `<head>` of the page:

```html
<link rel="icon" href="/favicon.ico" sizes="16x16 32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

The README at the root of this repository already uses the `<picture>` block below. It shows `tagore-wordmark-dark.svg` when GitHub uses its dark theme, and `tagore-wordmark.svg` when GitHub uses its light theme. The paths are relative to the root of this repository, so the snippet works only in a file at that root. Anywhere else, use full URLs, such as `https://raw.githubusercontent.com/rajnandan1/tagore/main/assets/logo/tagore-wordmark.svg`.

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/logo/tagore-wordmark-dark.svg">
  <img alt="tagore" src="assets/logo/tagore-wordmark.svg" width="240">
</picture>
```
