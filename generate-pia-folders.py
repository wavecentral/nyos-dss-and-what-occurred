#!/usr/bin/env python3
"""Generate per-request directory landing pages under pia-requests/.

For each entry in REQUESTS below, creates pia-requests/NN-slug/index.html with:
- Request metadata (title, status, date range, filing details)
- Prominent CTA linking to the request PDF (draft or final)
- Documents-received directory: empty-state card or a list of received records
- Links back to the PIA tracker and the main report

To record records as NYOS produces them: append to the request's "documents"
list (see schema in REQUESTS below) and re-run with --force.

Usage:
    python3 generate-pia-folders.py            # writes pages that don't exist
    python3 generate-pia-folders.py --force    # overwrite existing pages
    python3 generate-pia-folders.py --dry-run  # preview without writing
"""

from __future__ import annotations

import argparse
from pathlib import Path
from string import Template

REPO_ROOT = Path(__file__).resolve().parent
OUT_BASE = REPO_ROOT / "pia-requests"


# ---------------------------------------------------------------------------
# Per-request data
# ---------------------------------------------------------------------------

REQUESTS = [
    {
        "num": "01",
        "slug": "seay-engagement",
        "keystone": True,
        "title": "Dr.&nbsp;Seay's interim engagement &amp; payments to Leadership4School / DSS",
        "subtitle": "The contract that governs his $0-on-the-990 tenure, and every payment that flowed to him or his affiliated entities.",
        "status_class": "submitted",
        "status_label": "Submitted",
        "date_range": "Engagement: Feb&nbsp;13&nbsp;&ndash;&nbsp;Jun&nbsp;27,&nbsp;2024. Payments and vendor records: Jul&nbsp;1,&nbsp;2023 through the date of NYOS's response.",
        "filed_on": "May&nbsp;7,&nbsp;2026",
        "response_due_by": "approximately May&nbsp;21,&nbsp;2026",
        "pdf_url": "../../pia-01-seay-engagement_redacted.pdf",
        "pdf_label": "View Submitted Request",
        "pdf_aside": "Signed and filed with NYOS &middot; email and phone redacted in this public copy",
        "doc_status": "submitted_no_docs",
        "documents": [],
    },
    {
        "num": "02",
        "slug": "board-minutes-seay-tenure",
        "title": "Board minutes, certified agendas &amp; executive sessions &mdash; Seay tenure",
        "subtitle": "Everything in the open and closed record of the four months he ran the school.",
        "status_class": "formulating",
        "status_label": "Formulating",
        "date_range": "Feb&nbsp;13&nbsp;&ndash;&nbsp;Jun&nbsp;27,&nbsp;2024.",
        "pdf_url": "../../pia-02-board-minutes-seay-tenure_draft.pdf",
        "pdf_label": "View Draft Request",
        "pdf_aside": "Working draft &middot; DRAFT watermark, contact info redacted",
        "doc_status": "not_submitted",
        "documents": [],
    },
    {
        "num": "03",
        "slug": "dss-contract-votes",
        "title": "DSS contract votes &mdash; Dec&nbsp;10,&nbsp;2024 &amp; Jul&nbsp;24,&nbsp;2025",
        "subtitle": "What trustees actually saw before they voted on each DSS engagement.",
        "status_class": "formulating",
        "status_label": "Formulating",
        "date_range": "Dec&nbsp;10,&nbsp;2024 and Jul&nbsp;24,&nbsp;2025 (and the days immediately preceding each meeting at which packets were distributed).",
        "pdf_url": "../../pia-03-dss-contract-votes_draft.pdf",
        "pdf_label": "View Draft Request",
        "pdf_aside": "Working draft &middot; DRAFT watermark, contact info redacted",
        "doc_status": "not_submitted",
        "documents": [],
    },
    {
        "num": "04",
        "slug": "coi-disclosures",
        "title": "Conflict-of-interest disclosures, FY&nbsp;2023&nbsp;&ndash;&nbsp;FY&nbsp;2025",
        "subtitle": "The actual forms that NYOS's &ldquo;voluntary disclosure&rdquo; framework produces.",
        "status_class": "formulating",
        "status_label": "Formulating",
        "date_range": "Jul&nbsp;1,&nbsp;2022&nbsp;&ndash;&nbsp;Jun&nbsp;30,&nbsp;2025 (FY&nbsp;2023&nbsp;&ndash;&nbsp;FY&nbsp;2025).",
        "pdf_url": "../../pia-04-coi-disclosures_draft.pdf",
        "pdf_label": "View Draft Request",
        "pdf_aside": "Working draft &middot; DRAFT watermark, contact info redacted",
        "doc_status": "not_submitted",
        "documents": [],
    },
    {
        "num": "05",
        "slug": "vendor-contracts",
        "title": "All vendor contracts for financial, accounting, IT &amp; audit services",
        "subtitle": "The full back-office vendor map, in one request.",
        "status_class": "formulating",
        "status_label": "Formulating",
        "date_range": "Jul&nbsp;1,&nbsp;2023 through the date of NYOS's response.",
        "pdf_url": "../../pia-05-vendor-contracts_draft.pdf",
        "pdf_label": "View Draft Request",
        "pdf_aside": "Working draft &middot; DRAFT watermark, contact info redacted",
        "doc_status": "not_submitted",
        "documents": [],
    },
    {
        "num": "06",
        "slug": "board-training-oct-2025",
        "title": "October&nbsp;24,&nbsp;2025 board training &mdash; engagement records",
        "subtitle": "Who paid Dr. Seay for his return to NYOS sixteen months after his interim role ended.",
        "status_class": "formulating",
        "status_label": "Formulating",
        "date_range": "Approx. Aug&nbsp;1,&nbsp;2025 through the date of NYOS's response.",
        "pdf_url": "../../pia-06-board-training-oct-2025_draft.pdf",
        "pdf_label": "View Draft Request",
        "pdf_aside": "Working draft &middot; DRAFT watermark, contact info redacted",
        "doc_status": "not_submitted",
        "documents": [],
    },
    {
        "num": "07",
        "slug": "dss-golf-sponsorship",
        "title": "DSS golf tournament sponsorship records",
        "subtitle": "The financial relationship that exists outside the contract column.",
        "status_class": "formulating",
        "status_label": "Formulating",
        "date_range": "Sep&nbsp;1,&nbsp;2025 through the date of NYOS's response.",
        "pdf_url": "../../pia-07-dss-golf-sponsorship_draft.pdf",
        "pdf_label": "View Draft Request",
        "pdf_aside": "Working draft &middot; DRAFT watermark, contact info redacted",
        "doc_status": "not_submitted",
        "documents": [],
    },
    {
        "num": "08",
        "slug": "independent-audit",
        "title": "Independent audit and management letter",
        "subtitle": "The auditor's view of the related-party question.",
        "status_class": "formulating",
        "status_label": "Formulating",
        "date_range": "FY&nbsp;2023 (audit filed 2024) through the most recently completed audit.",
        "pdf_url": "../../pia-08-independent-audit_draft.pdf",
        "pdf_label": "View Draft Request",
        "pdf_aside": "Working draft &middot; DRAFT watermark, contact info redacted",
        "doc_status": "not_submitted",
        "documents": [],
    },
    {
        "num": "09",
        "slug": "audit-corrective-action-plan",
        "title": "The audit &ldquo;corrective action plan&rdquo;",
        "subtitle": "What the DSS &ldquo;audit support&rdquo; contract was actually engaged to support.",
        "status_class": "formulating",
        "status_label": "Formulating",
        "date_range": "Apr&nbsp;1,&nbsp;2024 through the date of NYOS's response.",
        "pdf_url": "../../pia-09-audit-corrective-action-plan_draft.pdf",
        "pdf_label": "View Draft Request",
        "pdf_aside": "Working draft &middot; DRAFT watermark, contact info redacted",
        "doc_status": "not_submitted",
        "documents": [],
    },
]


# ---------------------------------------------------------------------------
# Inline SVG icons (kept inline so each landing page stays self-contained)
# ---------------------------------------------------------------------------

SVG_FOLDER = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" '
    'width="56" height="56" aria-hidden="true">'
    '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z"/>'
    "</svg>"
)
SVG_DOC = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" '
    'width="18" height="18" aria-hidden="true">'
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>'
    '<path d="M14 2v6h6"/>'
    "</svg>"
)


# ---------------------------------------------------------------------------
# CSS (shared, embedded in each landing page so each stays self-contained)
# ---------------------------------------------------------------------------

CSS = """:root{--ink:#1a1a1a;--ink-2:#4a4a4a;--ink-3:#6e6e6e;--paper:#faf9f7;--paper-warm:#f3f1ec;--rule:#d4d0c8;--rule-heavy:#1a1a1a;--accent:#8b2500;--accent-hover:#a83a14;--display:'Playfair Display',Georgia,serif;--body:'Source Serif 4',Georgia,serif;--sans:'DM Sans',-apple-system,sans-serif;--mono:'JetBrains Mono','Courier New',monospace}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:17px;scroll-behavior:smooth}
@media(min-width:768px){html{font-size:18px}}
body{font-family:var(--body);color:var(--ink);background:var(--paper);line-height:1.7;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid transparent;transition:border-color .15s ease}
a:hover{border-bottom-color:var(--accent)}
.container{max-width:760px;margin:0 auto;padding:0 1.25rem}
.container--full{max-width:1100px}
.topbar{border-bottom:1px solid var(--rule);padding:.6rem 0;font-family:var(--sans);font-size:.72rem;color:var(--ink-3);letter-spacing:.04em;text-transform:uppercase}
.topbar .container{display:flex;justify-content:space-between;align-items:center;max-width:1100px;flex-wrap:wrap;gap:.5rem}
.topbar a{color:var(--ink-3);border-bottom:1px solid transparent}
.topbar a:hover{color:var(--ink);border-bottom-color:var(--ink-3)}
.masthead{text-align:center;padding:1.4rem 0 1.1rem;border-bottom:3px double var(--rule-heavy)}
.masthead__title{font-family:var(--display);font-size:1.05rem;font-weight:400;letter-spacing:.35em;text-transform:uppercase;color:var(--ink)}
.masthead__sub{font-family:var(--sans);font-size:.65rem;color:var(--ink-3);letter-spacing:.08em;text-transform:uppercase;margin-top:.25rem}
.hero{padding:2.4rem 0 2.1rem;border-bottom:1px solid var(--rule);background:#fff}
.hero__num{font-family:var(--mono);font-size:.78rem;color:var(--accent);letter-spacing:.04em;font-weight:500;text-transform:uppercase;display:inline-block;margin-bottom:.6rem}
.hero__keystone{display:inline-block;font-family:var(--sans);font-size:.6rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);background:#fff;border:1px solid var(--accent);padding:.18rem .55rem;border-radius:2px;margin-left:.55rem;vertical-align:middle}
.hero__status{display:inline-block;font-family:var(--sans);font-size:.66rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:.26rem .65rem;border-radius:3px;margin-bottom:.8rem;margin-left:.5rem;vertical-align:middle}
.status--submitted{background:#e0f0ff;color:#2a6fa8}
.status--formulating{background:#fdf8e8;color:#8a7420}
.status--identified{background:#e8e6f0;color:#5a5278}
.status--resubmitted{background:#fff0e0;color:#a86a2a}
.status--received-awaiting{background:#e8f5e8;color:#3a7a3a}
.status--received-delayed{background:#fce8e8;color:#a03030}
.status--docs-received{background:#d5f0d5;color:#2a6a2a}
.hero__title{font-family:var(--display);font-size:2rem;font-weight:900;line-height:1.18;color:var(--ink);margin:.3rem 0 .7rem}
@media(max-width:600px){.hero__title{font-size:1.5rem}}
.hero__sub{font-family:var(--body);font-size:1.02rem;color:var(--ink-2);line-height:1.5;font-style:italic;max-width:600px}
article{padding:2.4rem 0 2.4rem}
section.block{margin-bottom:2.4rem}
section.block:last-child{margin-bottom:0}
h2.section-head{font-family:var(--display);font-size:1.35rem;font-weight:700;color:var(--ink);margin-bottom:.55rem;padding-bottom:.55rem;border-bottom:1px solid var(--rule)}
.section-intro{font-size:.95rem;color:var(--ink-2);margin-bottom:.4rem;line-height:1.6}
.cta-row{margin:1.25rem 0 .55rem}
.cta-button{display:inline-flex;align-items:center;gap:.65rem;background:var(--accent);color:#fff;font-family:var(--sans);font-weight:700;font-size:.95rem;padding:.85rem 1.4rem;border-radius:4px;letter-spacing:.02em;text-decoration:none;border:none;border-bottom:1px solid transparent;transition:background .15s ease,transform .12s ease;box-shadow:0 1px 0 rgba(0,0,0,.06)}
.cta-button:hover{background:var(--accent-hover);color:#fff;border-bottom-color:transparent;transform:translateY(-1px)}
.cta-button .icon{display:inline-flex;line-height:1}
.cta-aside{font-family:var(--sans);font-size:.78rem;color:var(--ink-3);margin-top:.55rem}
.meta{font-family:var(--sans);font-size:.85rem;color:var(--ink-2);background:var(--paper-warm);padding:.95rem 1.15rem;border-radius:4px;margin:1.4rem 0 0;line-height:1.55;border:1px solid var(--rule)}
.meta__row{display:grid;grid-template-columns:130px 1fr;gap:.85rem;align-items:start;margin-bottom:.55rem}
.meta__row:last-child{margin-bottom:0}
@media(max-width:560px){.meta__row{grid-template-columns:1fr;gap:.15rem}}
.meta__label{font-family:var(--sans);font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);font-weight:600;padding-top:.18rem}
.meta__value{font-size:.92rem;color:var(--ink);line-height:1.5}
.docs-empty{border:2px dashed var(--rule);border-radius:6px;padding:2.4rem 1.5rem;text-align:center;background:#fff;margin-top:.5rem}
.docs-empty__icon{color:var(--ink-3);opacity:.5;margin-bottom:.65rem;display:inline-block}
.docs-empty__title{font-family:var(--display);font-size:1.15rem;font-weight:700;color:var(--ink-2);margin-bottom:.5rem}
.docs-empty__msg{font-family:var(--sans);font-size:.86rem;color:var(--ink-3);max-width:480px;margin:0 auto;line-height:1.6}
.docs-list{list-style:none;padding:0;margin:.5rem 0 0}
.docs-list__item{display:grid;grid-template-columns:auto 1fr auto;gap:.85rem;align-items:center;border:1px solid var(--rule);background:#fff;padding:.8rem 1rem;border-radius:4px;margin-bottom:.55rem;font-family:var(--sans)}
.docs-list__icon{color:var(--accent);display:inline-flex}
.docs-list__name{font-weight:600;font-size:.92rem;color:var(--ink);border-bottom:1px solid transparent}
.docs-list__name:hover{border-bottom-color:var(--accent);color:var(--accent)}
.docs-list__meta{font-size:.74rem;color:var(--ink-3);margin-top:.18rem}
.docs-list__action{font-size:.78rem;color:var(--accent);font-weight:600;border-bottom:1px solid transparent;white-space:nowrap}
.docs-list__action:hover{border-bottom-color:var(--accent)}
.docs-note{font-family:var(--sans);font-size:.78rem;color:var(--ink-3);margin-top:1rem;font-style:italic;text-align:center}
.site-footer{border-top:3px double var(--rule-heavy);padding:1.5rem 0 2rem;text-align:center;font-family:var(--sans);font-size:.7rem;color:var(--ink-3);line-height:1.7;margin-top:3rem}
.site-footer a{color:var(--ink-3)}"""


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------

PAGE_TEMPLATE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PIA Request $num &mdash; Records folder &middot; The Interim Pipeline</title>
<meta name="description" content="Records folder for Public Information Act Request $num &mdash; $title_plain">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
$css
</style>
<script type="text/javascript">
    (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "wnk9fpk31j");
</script>
</head>
<body>

<div class="topbar">
<div class="container container--full">
<span><a href="../../pia-requests.html">&larr; PIA Tracker</a> &middot; <a href="../../index.html">The Interim Pipeline</a></span>
<span>Records Folder</span>
</div>
</div>

<header class="masthead">
<div class="container">
<h1 class="masthead__title">Public Interest Report</h1>
<p class="masthead__sub">A Community-Driven Investigation into Charter School Governance</p>
</div>
</header>

<section class="hero">
<div class="container">
<div>
<span class="hero__num">PIA Request #$num</span>$keystone_chip
<span class="hero__status status--$status_class">$status_label</span>
</div>
<h2 class="hero__title">$title</h2>
<p class="hero__sub">$subtitle</p>
</div>
</section>

<article>
<div class="container">

<section class="block">
<h2 class="section-head">The original request</h2>
<p class="section-intro">$request_intro</p>

<div class="cta-row">
<a class="cta-button" href="$pdf_url" target="_blank" rel="noopener">
<span class="icon">$svg_doc</span> $pdf_label (PDF)
</a>
</div>
<p class="cta-aside">$pdf_aside</p>

<div class="meta">
<div class="meta__row">
<div class="meta__label">Date range</div>
<div class="meta__value">$date_range</div>
</div>
$filed_meta_row
$response_meta_row
</div>
</section>

<section class="block">
<h2 class="section-head">Documents received from NYOS</h2>
$docs_section
$docs_note
</section>

</div>
</article>

<footer class="site-footer">
<div class="container">
<p>&copy; 2026 Mark Garcia and contributing NYOS parents. Published in the public interest.<br>
This page is not affiliated with NYOS Charter School, Dynamic Support Solutions, or Leadership4School LLC.<br>
Corrections and additional documentation: <a href="https://github.com/wavecentral/nyos-dss-and-what-occurred/issues">github.com/wavecentral/nyos-dss-and-what-occurred</a></p>
</div>
</footer>

</body>
</html>
""")


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def _strip_html_entities(s: str) -> str:
    """Light entity decode for the meta description / title attribute."""
    return (
        s.replace("&nbsp;", " ")
        .replace("&amp;", "&")
        .replace("&mdash;", "—")
        .replace("&ndash;", "–")
        .replace("&middot;", "·")
        .replace("&ldquo;", "“")
        .replace("&rdquo;", "”")
        .replace("&rarr;", "→")
        .replace("&larr;", "←")
        .replace("&hellip;", "…")
    )


def build_docs_section(req: dict) -> str:
    if req["documents"]:
        items = []
        for d in req["documents"]:
            size = d.get("size", "")
            sep = " &middot; " if size else ""
            items.append(
                f"""<li class="docs-list__item">
<span class="docs-list__icon">{SVG_DOC}</span>
<div>
<a class="docs-list__name" href="{d['url']}" target="_blank" rel="noopener">{d['name']}</a>
<div class="docs-list__meta">{size}{sep}Received {d['received']}</div>
</div>
<a class="docs-list__action" href="{d['url']}" target="_blank" rel="noopener">Download &rarr;</a>
</li>"""
            )
        return f'<ul class="docs-list">{"".join(items)}</ul>'

    if req["doc_status"] == "submitted_no_docs":
        title = "Awaiting NYOS response"
        msg = (
            f'Submitted to NYOS on <strong>{req["filed_on"]}</strong>. '
            f'Under Texas Government Code §&nbsp;552.221(d), NYOS has 10 business days '
            f'(through {req["response_due_by"]}) either to produce the records, '
            f'certify a date by which production will occur, or seek an Attorney General '
            f'ruling for any portion claimed exempt.'
        )
    else:
        title = "Not yet submitted"
        msg = (
            "This request has not yet been submitted to NYOS. The draft is being "
            "finalized; the PDF above is the working language. Once filed, NYOS will "
            "have 10 business days under §&nbsp;552.221(d) to respond."
        )

    return (
        f'<div class="docs-empty">'
        f'<div class="docs-empty__icon">{SVG_FOLDER}</div>'
        f'<div class="docs-empty__title">{title}</div>'
        f'<p class="docs-empty__msg">{msg}</p>'
        f'</div>'
    )


def build_request_intro(req: dict) -> str:
    if req["status_class"] == "submitted":
        return (
            "The Texas Public Information Act request as drafted and signed, then "
            "submitted to NYOS. The PDF below is the operative copy of the request."
        )
    return (
        "The Texas Public Information Act request as currently drafted. The PDF below "
        "is a working draft &mdash; once finalized, this page will be updated with the "
        "submission date and a link to the signed copy."
    )


def render(req: dict) -> str:
    filed_meta = ""
    if req.get("filed_on"):
        filed_meta = (
            '<div class="meta__row">'
            '<div class="meta__label">Filed</div>'
            f'<div class="meta__value">{req["filed_on"]}</div>'
            '</div>'
        )
    response_meta = ""
    if req.get("response_due_by"):
        response_meta = (
            '<div class="meta__row">'
            '<div class="meta__label">Response due</div>'
            f'<div class="meta__value">{req["response_due_by"]}</div>'
            '</div>'
        )

    docs_note = ""
    if not req["documents"]:
        docs_note = (
            '<p class="docs-note">When records are produced, they will appear here in the '
            'order received, with timestamps.</p>'
        )

    keystone_chip = (
        '<span class="hero__keystone">Keystone request</span>' if req.get("keystone") else ""
    )

    return PAGE_TEMPLATE.substitute(
        num=req["num"],
        title=req["title"],
        title_plain=_strip_html_entities(req["title"]),
        subtitle=req["subtitle"],
        status_class=req["status_class"],
        status_label=req["status_label"],
        keystone_chip=keystone_chip,
        date_range=req["date_range"],
        pdf_url=req["pdf_url"],
        pdf_label=req["pdf_label"],
        pdf_aside=req["pdf_aside"],
        filed_meta_row=filed_meta,
        response_meta_row=response_meta,
        request_intro=build_request_intro(req),
        docs_section=build_docs_section(req),
        docs_note=docs_note,
        css=CSS,
        svg_doc=SVG_DOC,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing landing pages.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be created without writing.")
    args = parser.parse_args()

    OUT_BASE.mkdir(exist_ok=True)
    for req in REQUESTS:
        folder = OUT_BASE / f"{req['num']}-{req['slug']}"
        folder.mkdir(exist_ok=True)
        target = folder / "index.html"
        if target.exists() and not args.force:
            print(f"  skip (exists): {target.relative_to(REPO_ROOT)}")
            continue
        if args.dry_run:
            print(f"  would write: {target.relative_to(REPO_ROOT)}")
            continue
        target.write_text(render(req), encoding="utf-8")
        print(f"  wrote: {target.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
