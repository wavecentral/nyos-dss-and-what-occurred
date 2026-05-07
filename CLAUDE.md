# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a software project**. It is a single-page investigative report — "The Interim Pipeline" — published as a static site on GitHub Pages at `wavecentral.github.io/nyos-dss-and-what-occurred`. The deliverable is journalism, not code. Editorial accuracy and sourcing discipline matter more than anything technical.

The report investigates undisclosed ties between NYOS Charter School's interim leadership and Dynamic Support Solutions (DSS). It is timed against a NYOS board meeting on **May 12, 2026**.

## Repository layout

- `index.html` — the entire report. Self-contained: inline CSS in `<style>`, minimal inline JS (scroll progress bar only). No external assets beyond Google Fonts.
- `README.md` — the GitHub-facing repo description. Mirrors a subset of `index.html` content (Purpose, Primary Sources, Key Findings, PIA Tracker, Legal Notice).
- `.nojekyll` — disables Jekyll on GitHub Pages. **Do not delete.**

There is no `package.json`, no build, no tests, no linter, no CI. Edits to `index.html` ship the moment they're pushed to `main`.

## Editorial rules (most important section)

These rules govern content changes. Treat them as load-bearing — violating them undermines the report's credibility and legal posture.

1. **Confirmed vs. Unconfirmed must stay visually and verbally distinct.** The report uses three evidence-box styles (`.evidence-box`, `.evidence-box--caution`, `.evidence-box--unconfirmed`) and two timeline styles (`li.unconfirmed` with `tl-tag--unconfirmed`). Never relabel an unconfirmed item as confirmed without a citable public source. Never strip the "Unconfirmed" tag.
2. **Every factual claim about a person or entity needs a footnote.** Footnotes are `<sup class="fn-ref"><a href="#fnN">N</a></sup>` pointing to `<li id="fnN">` entries in the `<ol class="footnotes">`. If you add a claim, add the source. Footnote numbers are referenced by ID, not order — but keep them ordered for readers.
3. **Frame open questions as questions, not accusations.** The report is "journalistic in nature, not advocacy material" and "does not allege criminal conduct" (see README Legal Notice and the methodology box). Phrasing matters.
4. **Keep `index.html` and `README.md` in sync** for overlapping content: Key Findings, PIA tracker statuses, "Last updated" date. The HTML has `<time datetime="YYYY-MM-DD">` near the top; README has a `Last updated:` line at the bottom.
5. **PIA tracker statuses use a fixed vocabulary.** Status keys: Identified, Formulating, Submitted, Re-submitted, Response Received / Awaiting Documents, Response Received / Delayed, Documents Received. CSS classes mirror these (`.status--identified`, `.status--formulating`, etc.). Don't invent new statuses.
6. **The author is Mark Garcia with contributions from fellow NYOS parents.** Bylines and attribution language is set; don't rewrite.

## Working in `index.html`

- The file is monolithic by design — one HTML file is the publishing surface. Don't refactor it into multiple files, a static site generator, or a JS framework unless explicitly asked. Splitting breaks the single-file portability that lets contributors archive/email/screenshot the whole report.
- CSS uses semantic custom properties on `:root` (`--accent`, `--confirmed-bg`, `--unconfirmed-border`, etc.). Reuse tokens; don't hard-code colors.
- Typography stack: Playfair Display (display), Source Serif 4 (body), DM Sans (sans/UI), JetBrains Mono (numbers in tables). The compensation table relies on `.num` (mono, right-aligned) and `.zero` (accent color) — preserve when editing.
- Print styles exist (`@media print`); test print preview if you change layout-affecting CSS.
- Non-breaking spaces (`&nbsp;`) appear inside names like "Dr.&nbsp;Seay" to prevent line-break orphans. Keep them.

## Deployment

GitHub Pages serves from `main`. Push to deploy. There is no preview environment — proofread before pushing. To preview locally, open `index.html` directly in a browser, or `python3 -m http.server` from the repo root.

## Domain glossary (so you don't have to re-derive it)

- **NYOS** — Not Your Ordinary School Charter School (Austin, TX, ~1,800 students, ~$20M budget).
- **DSS / Dynamic Support Solutions** — Dallas-based back-office services firm for charter schools. `dssedu.com` and `charterschoolsconsulting.com` are both DSS properties.
- **Dr. Alan Seay** — Was NYOS Interim Executive Director Feb–Jun 2024; simultaneously listed as "Special Advisor, School Leadership" at DSS. Central subject of the report.
- **Dr. Mechiel Rozas** — Permanent NYOS Superintendent from June 2024.
- **Leadership4School LLC** — Dr. Seay's consulting entity, hypothesized intermediary for his NYOS compensation (his Form 990 reportable comp from NYOS is $0).
- **PIA** — Texas Public Information Act (Government Code Ch. 552); the legal mechanism for the records requests in the tracker.
- **Form 990** — IRS nonprofit tax return; the primary documentary source for confirmed compensation/vendor claims.
