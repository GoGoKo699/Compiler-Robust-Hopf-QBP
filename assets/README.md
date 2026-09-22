# Diagram map

[← Repository landing page](../README.md) · [Complete technical narrative](../REVIEW.md)

The diagrams are explanatory views of exact statements in the text.  They do
not replace the operator formulas or register counts.

| Diagram | Used to show |
|---|---|
| [`state-vs-frame.svg`](state-vs-frame.svg) | one initialized state column versus a prescribed state-and-marker completion |
| [`two-qubit-obstruction.svg`](two-qubit-obstruction.svg) | two state-equivalent completions placing the objective response on different marker columns |
| [`strict-zero-echo.svg`](strict-zero-echo.svg) | the chronological borrowed-suffix half-angle echo for one nonfinal depth |
| [`tree-cut-routing.svg`](tree-cut-routing.svg) | conditioned prefix, coherent branch routing, parallel subtree frames, and inverse routing |
| [`literature-lineage.svg`](literature-lineage.svg) | the all-workspace state-preparation line meeting the Hopf differential-frame line |

All SVGs include a title, description, and `viewBox` for accessible GitHub
rendering.  The restrained blue-grey palette is used only for navigation and
structure; mathematical distinctions are also expressed through labels and
layout.

The source equations and proof checkpoints are in
[`REVIEW.md`](../REVIEW.md) and
[`docs/COMPILER_THEOREM.md`](../docs/COMPILER_THEOREM.md).

## Rendering checks

The optional [presentation checker](../scripts/check_presentation.py) renders
all five SVGs at their desktop embedding widths and at a 358-pixel image width.
It measures label containment, label overlap, annotated connector clearance and
visible arrowheads. It also checks that prose and table mathematics survive a
CommonMark handoff and typeset with MathJax, then renders every Markdown page
with tables, images, and display equations at desktop and narrow widths.
Page overflow, missing images, and oversized desktop equations fail the check;
local scrolling of wide tables and narrow-screen display equations is recorded.
Saved page, table, and diagram previews support visual inspection. This models
the documented protected inline syntax with a local reading stylesheet;
it does not reproduce GitHub's private client implementation.

The numerical compiler suite remains independent of these browser dependencies.

```bash
python -m pip install -r requirements-presentation.txt
python -m playwright install chromium
npm install --prefix /tmp/hopf-mathjax --ignore-scripts --no-audit --no-fund mathjax-full@3.2.1
python scripts/check_presentation.py \
  --mathjax /tmp/hopf-mathjax/node_modules/mathjax-full/es5/tex-svg-full.js \
  --output /tmp/hopf-presentation
```

Use `--svg-only` to inspect the diagrams without the optional MathJax bundle.
The browser checker emits previews and measured geometry for inspection.
