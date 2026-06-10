#!/usr/bin/env python3
"""
generate_pdf.py — Onboarding Strategy Report PDF generator

Consumes a single JSON input (conforming to templates/report-schema.json) and
produces a client-ready PDF at the specified output path.

Pipeline:
    1. Parse + validate input JSON
    2. Ensure output directory exists (auto-create deliverables/ if missing)
    3. Build reportlab document with 6 or 7 pages:
       Cover -> Diagnostic -> Avatars -> Positioning ->
       [Existing Ads Audit if enabled] ->
       Plus/Minus Map -> 90-Day Roadmap -> Black Book Appendix

Usage:
    python generate_pdf.py --data <input.json> --output <output.pdf>
    python generate_pdf.py --data report.json --output report.pdf --verbose

Hormozi-revised layout: no composite 0-100 score, no A+ -> F grade. Primary
constraint callout + Calculator Close + 1-5 RYG dimensions. See the plan at
~/.claude/plans/zany-sprouting-prism.md Part 1 for the design rationale.
"""

import argparse
import json
import sys
import os
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    )
except ImportError:
    print("Error: reportlab is required. Install with: pip install reportlab", file=sys.stderr)
    sys.exit(1)

# Local import of helpers (same directory)
sys.path.insert(0, str(Path(__file__).parent))
from pdf_helpers import (  # noqa: E402
    COLORS,
    get_styles,
    standard_table_style,
    draw_constraint_callout,
    create_ryg_table,
    create_plus_minus_map,
    score_to_band,
    band_color,
    band_label,
)


# ---------------------------------------------------------------------------
# Data loading + validation
# ---------------------------------------------------------------------------
def load_data(data_path):
    """Load and minimally validate the input JSON."""
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Input data file not found: {data_path}")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("Input JSON must be an object at the top level")
    return data


def ensure_output_dir(output_path):
    """Create the parent directory of the output path if it doesn't exist."""
    parent = Path(output_path).parent
    parent.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------
def build_cover(data, styles):
    """Page 1 — Dream Translation + Primary Constraint + Calculator Close.

    No composite score, no A+ -> F grade. Replaces zubair's score-gauge cover
    with the Hormozi Calculator Close pattern.
    """
    elements = []
    meta = data.get("report_metadata", {})
    dream = data.get("dream_translation", {})
    diagnostic = data.get("diagnostic", {})

    client_name = meta.get("client_name", "Client")
    prepared_by = meta.get("prepared_by", "")
    report_date = meta.get("report_date", "")
    engagement_type = meta.get("engagement_type", "onboarding_strategy")

    # Top spacer for breathing room
    elements.append(Spacer(1, 0.6 * inch))

    # Title + client name
    elements.append(Paragraph("Onboarding Strategy Report", styles["title"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        f"<font color='{COLORS['accent'].hexval()}'>{client_name}</font>",
        styles["subtitle"]
    ))
    if report_date:
        elements.append(Paragraph(f"Report date: {report_date}", styles["footer"]))
    if prepared_by:
        elements.append(Paragraph(f"Prepared by: {prepared_by}", styles["footer"]))

    elements.append(Spacer(1, 24))

    # Dream Translation — client's exact words
    exact_words = dream.get("client_exact_words")
    if exact_words:
        elements.append(Paragraph("The Dream You Shared With Us", styles["subheading"]))
        elements.append(Paragraph(f"&ldquo;{exact_words}&rdquo;", styles["dream_quote"]))

    elements.append(Spacer(1, 16))

    # Primary Constraint callout (the big centerpiece)
    primary = diagnostic.get("primary_constraint", "")
    monthly = diagnostic.get("monthly_cost_of_constraint_usd", 0)
    annual = diagnostic.get("annual_ignorance_tax_usd", monthly * 12 if monthly else 0)

    if primary:
        callout = draw_constraint_callout(primary, monthly, annual)
        elements.append(callout)

    elements.append(Spacer(1, 16))

    # Rationale line
    rationale = diagnostic.get("primary_constraint_rationale", "")
    if rationale:
        elements.append(Paragraph(
            f"<i>Why this is the one thing:</i> {rationale}",
            styles["section_intro"]
        ))

    return elements


def build_diagnostic(data, styles):
    """Page 2 — 1-5 RYG table across 5 dimensions, primary constraint highlighted."""
    elements = []
    diagnostic = data.get("diagnostic", {})
    dimensions_dict = diagnostic.get("dimensions", {})

    elements.append(Paragraph("Diagnostic: Where You Stand", styles["heading"]))
    elements.append(Paragraph(
        "We scored five dimensions of your paid-ads readiness on a 1&ndash;5 scale. "
        "One dimension is flagged as <b>The Primary Constraint</b> &mdash; the single bottleneck "
        "that, if solved, unlocks the biggest lift for you right now.",
        styles["section_intro"]
    ))
    elements.append(Spacer(1, 12))

    # Normalize dimensions_dict into a list for the RYG table helper
    dimension_list = []
    primary_key = diagnostic.get("primary_constraint", "")
    for key, value in dimensions_dict.items():
        if not isinstance(value, dict):
            continue
        score = value.get("score", 0)
        band = value.get("band") or score_to_band(score)
        dimension_list.append({
            "name": key.replace("_", " ").title(),
            "score": score,
            "band": band,
            "action": value.get("action", ""),
            "is_primary_constraint": (key == primary_key) or value.get("is_primary_constraint", False),
        })

    if dimension_list:
        table = create_ryg_table(dimension_list, styles)
        elements.append(table)

    elements.append(Spacer(1, 18))

    # Calculator Close note (grounds the numbers)
    cc_note = diagnostic.get("calculator_close_note", "")
    if cc_note:
        elements.append(Paragraph("The Calculator Close", styles["subheading"]))
        elements.append(Paragraph(cc_note, styles["body"]))

    return elements


def build_avatars(data, styles):
    """Page 3 — Avatar deep-dive cards with angle THEMES (declarative only)."""
    elements = []
    avatars = data.get("avatars", [])

    elements.append(Paragraph("Who We're Actually Talking To", styles["heading"]))
    elements.append(Paragraph(
        "These are the people your ads will speak to. Each avatar is matched to a specific "
        "awareness and sophistication level &mdash; the creative strategy adapts accordingly.",
        styles["section_intro"]
    ))
    elements.append(Spacer(1, 8))

    if not avatars:
        elements.append(Paragraph(
            "<i>Avatars will be populated from avatar-research output.</i>",
            styles["body"]
        ))
        return elements

    for i, avatar in enumerate(avatars):
        if i > 0:
            elements.append(Spacer(1, 14))

        name = avatar.get("name", f"Avatar {i + 1}")
        awareness = avatar.get("awareness", "")
        sophistication = avatar.get("sophistication", "")

        # Header row
        header_text = f"<b>{name}</b>"
        if awareness or sophistication:
            meta_chip = []
            if awareness:
                meta_chip.append(f"Awareness: {awareness}")
            if sophistication:
                meta_chip.append(f"Sophistication: {sophistication}")
            header_text += f"  <font color='{COLORS['text_light'].hexval()}' size='9'>({' / '.join(meta_chip)})</font>"

        elements.append(Paragraph(header_text, styles["subheading"]))

        # Pains
        pains = avatar.get("top_pains", [])
        if pains:
            elements.append(Paragraph("<b>Top pains:</b>", styles["body_small"]))
            for pain in pains:
                elements.append(Paragraph(f"&bull; {pain}", styles["body_small"]))

        # Buying trigger
        trigger = avatar.get("buying_trigger", "")
        if trigger:
            elements.append(Paragraph(f"<b>Buying trigger:</b> {trigger}", styles["body_small"]))

        # Angle themes (declarative only — no finished copy)
        themes = avatar.get("preview_angles", []) or avatar.get("angle_themes", [])
        if themes:
            elements.append(Paragraph("<b>Angle themes we'll test:</b>", styles["body_small"]))
            for theme in themes:
                elements.append(Paragraph(f"&rarr; {theme}", styles["body_small"]))

    return elements


def build_positioning(data, styles):
    """Page 4 — Strategic Positioning + Mechanism (declarative only)."""
    elements = []
    strategy = data.get("strategy_preview", {})

    elements.append(Paragraph("Strategic Positioning", styles["heading"]))
    elements.append(Spacer(1, 6))

    positioning = strategy.get("positioning_angle", "")
    mechanism = strategy.get("mechanism_name", "")
    wedge = strategy.get("differentiation_wedge", "")

    if mechanism:
        elements.append(Paragraph("The Mechanism", styles["subheading"]))
        elements.append(Paragraph(f"<b>{mechanism}</b>", styles["body"]))
        elements.append(Spacer(1, 8))

    if positioning:
        elements.append(Paragraph("Positioning Angle", styles["subheading"]))
        elements.append(Paragraph(positioning, styles["body"]))
        elements.append(Spacer(1, 8))

    if wedge:
        elements.append(Paragraph("Differentiation Wedge", styles["subheading"]))
        elements.append(Paragraph(wedge, styles["body"]))
        elements.append(Spacer(1, 12))

    # Angle themes per avatar (reiterated here as the strategic preview)
    themes = strategy.get("angle_themes_per_avatar", [])
    if themes:
        elements.append(Paragraph("Angle Themes We'll Test (Preview)", styles["subheading"]))
        for t in themes:
            if isinstance(t, dict):
                avatar_name = t.get("avatar", "")
                theme_list = t.get("themes", [])
                if avatar_name:
                    elements.append(Paragraph(f"<b>{avatar_name}:</b>", styles["body_small"]))
                for theme in theme_list:
                    elements.append(Paragraph(f"&rarr; {theme}", styles["body_small"]))
            else:
                elements.append(Paragraph(f"&rarr; {t}", styles["body_small"]))

    elements.append(Spacer(1, 18))

    # Declarative/procedural footer (explicit withhold statement)
    elements.append(Paragraph(
        "<font color='#64748b' size='9'><i>Execution specifics &mdash; finished headlines, "
        "ad copy, landing pages, and automation logic &mdash; are delivered as part of the engagement. "
        "This page shows the <b>what</b>; the <b>how</b> is the work itself.</i></font>",
        styles["body_small"]
    ))

    return elements


def build_existing_ads_audit(data, styles):
    """Page 5 (conditional) — AAA-framed audit with Zero Blame header."""
    elements = []
    audit = data.get("existing_ads_audit", {})
    if not audit.get("enabled"):
        return elements

    elements.append(Paragraph("Your Current Ads: What We Found", styles["heading"]))

    # Zero Blame frame header
    zb_header = audit.get(
        "zero_blame_header",
        "Nothing that happened before today is anyone's fault. This page exists so we can solve the problem together."
    )
    elements.append(Paragraph(
        f"<font color='{COLORS['accent'].hexval()}'><i>{zb_header}</i></font>",
        styles["section_intro"]
    ))
    elements.append(Spacer(1, 10))

    findings = audit.get("findings_aaa", [])
    if not findings:
        elements.append(Paragraph(
            "<i>No findings enabled for this client.</i>",
            styles["body"]
        ))
        return elements

    for i, f in enumerate(findings, 1):
        elements.append(Paragraph(f"Finding {i}", styles["subheading"]))

        finding_text = f.get("finding", "")
        if finding_text:
            elements.append(Paragraph(f"<b>{finding_text}</b>", styles["body"]))

        ack = f.get("acknowledge", "")
        if ack:
            elements.append(Paragraph(f"<b>Acknowledge:</b> {ack}", styles["body_small"]))

        assoc = f.get("associate", "")
        if assoc:
            elements.append(Paragraph(f"<b>Associate:</b> {assoc}", styles["body_small"]))

        ask = f.get("ask_pivot", "")
        if ask:
            elements.append(Paragraph(f"<b>Ask:</b> {ask}", styles["body_small"]))

        reframe = f.get("skill_deficiency_reframe", "")
        if reframe:
            elements.append(Paragraph(
                f"<font color='{COLORS['accent'].hexval()}'><i>{reframe}</i></font>",
                styles["body_small"]
            ))

        monthly = f.get("monthly_cost_usd", 0)
        if monthly:
            elements.append(Paragraph(
                f"<font color='{COLORS['highlight'].hexval()}'><b>Monthly cost of this gap: ${monthly:,}</b></font>",
                styles["body_small"]
            ))

        elements.append(Spacer(1, 10))

    total = audit.get("total_spend_at_risk_monthly", 0)
    if total:
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(
            f"<b>Total monthly spend currently at risk:</b> "
            f"<font color='{COLORS['highlight'].hexval()}'>${total:,}</font>",
            styles["body"]
        ))

    return elements


def build_plus_minus_map(data, styles):
    """Page 6 — Plus/Minus Potential Map (two-column future-state visual)."""
    elements = []
    pm = data.get("plus_minus_map", {})

    elements.append(Paragraph("The Two Paths Forward", styles["heading"]))
    elements.append(Paragraph(
        "Two futures. The choice is yours.",
        styles["section_intro"]
    ))
    elements.append(Spacer(1, 10))

    work_with_us = pm.get("work_with_us", {"more": [], "less": []})
    stay_current = pm.get("stay_current", {"more": [], "less": []})

    if work_with_us.get("more") or work_with_us.get("less") or stay_current.get("more") or stay_current.get("less"):
        table = create_plus_minus_map(work_with_us, stay_current, styles)
        elements.append(table)
    else:
        elements.append(Paragraph(
            "<i>Plus/Minus map will be populated from avatar pains and dream outcomes.</i>",
            styles["body"]
        ))

    return elements


def build_roadmap(data, styles):
    """Page 7 — Activation / Value / Lock-In phased roadmap + BAMFAM."""
    elements = []
    roadmap = data.get("ninety_day_roadmap", {})
    bamfam = data.get("next_meeting_bamfam", {})

    elements.append(Paragraph("Your Next 90 Days", styles["heading"]))

    expectation = roadmap.get("expectation_language", {})
    anchor_note = expectation.get("example", "")
    if anchor_note:
        elements.append(Paragraph(
            f"<i>{anchor_note}</i>",
            styles["section_intro"]
        ))
    elements.append(Spacer(1, 10))

    # Three phases
    phases = [
        ("activation_days_1_30", "Activation", "Days 1-30"),
        ("value_days_31_60", "Value", "Days 31-60"),
        ("lock_in_days_61_90", "Lock-In", "Days 61-90"),
    ]

    rows = [["Phase", "Focus", "What You'll See"]]
    for key, phase_name, day_range in phases:
        phase = roadmap.get(key, {})
        focus = phase.get("focus", "")

        what_you_see = []
        for field in ("micro_promises_first_48h", "activation_points", "deliverables",
                      "documented_wins"):
            items = phase.get(field, [])
            if items:
                for item in items:
                    what_you_see.append(f"- {item}")

        quick_win = phase.get("quick_win_target")
        if quick_win:
            what_you_see.insert(0, f"Quick win: {quick_win}")

        rows.append([
            Paragraph(f"<b>{phase_name}</b><br/><font size='8' color='#64748b'>{day_range}</font>", styles["body_small"]),
            Paragraph(focus, styles["body_small"]),
            Paragraph("<br/>".join(what_you_see) if what_you_see else "&mdash;", styles["body_small"]),
        ])

    table = Table(rows, colWidths=[100, 150, 250])
    table.setStyle(standard_table_style([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 18))

    # BAMFAM prompt
    prompt_text = bamfam.get("prompt_text", "Next meeting booked for: ______________________")
    purpose = bamfam.get("purpose", "")

    elements.append(Paragraph("Next Meeting", styles["subheading"]))
    elements.append(Paragraph(
        f"<b>{prompt_text}</b>",
        styles["body"]
    ))
    if purpose:
        elements.append(Paragraph(
            f"<font color='{COLORS['text_light'].hexval()}' size='9'><i>Purpose: {purpose}</i></font>",
            styles["body_small"]
        ))

    return elements


def build_black_book_appendix(data, styles):
    """Appendix — Black Book handoff list with perceived-value annotations."""
    elements = []
    bb = data.get("black_book_handoff", {})
    assets = bb.get("assets_included", [])
    if not assets:
        return elements

    elements.append(Paragraph("What You'll Receive In Your First Week", styles["heading"]))
    elements.append(Paragraph(
        "These assets are yours as part of the engagement. Many of them would cost "
        "thousands of dollars or hundreds of hours to build from scratch.",
        styles["section_intro"]
    ))
    elements.append(Spacer(1, 10))

    rows = [["Asset", "Perceived Value"]]
    total = 0
    for a in assets:
        name = a.get("name", "")
        value = a.get("perceived_value_usd", 0)
        try:
            total += int(value)
        except (TypeError, ValueError):
            pass
        rows.append([
            Paragraph(name, styles["body"]),
            Paragraph(f"${int(value):,}" if value else "&mdash;", styles["body"]),
        ])

    total_from_data = bb.get("total_perceived_value_usd", total)
    rows.append([
        Paragraph("<b>Total perceived value</b>", styles["body"]),
        Paragraph(f"<b>${int(total_from_data):,}</b>", styles["body"]),
    ])

    table = Table(rows, colWidths=[350, 150])
    table.setStyle(standard_table_style([
        ("BACKGROUND", (0, -1), (-1, -1), COLORS["constraint_bg"]),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
    ]))
    elements.append(table)

    return elements


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------
def generate(data, output_path, verbose=False):
    """Build the full PDF from the loaded data dict."""
    ensure_output_dir(output_path)

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
        title="Onboarding Strategy Report",
        author=data.get("report_metadata", {}).get("prepared_by", ""),
    )

    styles = get_styles()
    elements = []

    def _append_page(builder, label):
        if verbose:
            print(f"  building: {label}", file=sys.stderr)
        elements.extend(builder(data, styles))

    _append_page(build_cover, "Cover")
    elements.append(PageBreak())

    _append_page(build_diagnostic, "Diagnostic")
    elements.append(PageBreak())

    _append_page(build_avatars, "Avatars")
    elements.append(PageBreak())

    _append_page(build_positioning, "Positioning")
    elements.append(PageBreak())

    if data.get("existing_ads_audit", {}).get("enabled"):
        _append_page(build_existing_ads_audit, "Existing Ads Audit")
        elements.append(PageBreak())
    elif verbose:
        print("  skipping: Existing Ads Audit (disabled)", file=sys.stderr)

    _append_page(build_plus_minus_map, "Plus/Minus Map")
    elements.append(PageBreak())

    _append_page(build_roadmap, "90-Day Roadmap")

    # Black Book appendix — only add page break + page if there are assets
    bb_assets = data.get("black_book_handoff", {}).get("assets_included", [])
    if bb_assets:
        elements.append(PageBreak())
        _append_page(build_black_book_appendix, "Black Book Appendix")

    doc.build(elements)

    if verbose:
        print(f"  wrote: {output_path}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Generate an Onboarding Strategy Report PDF from a structured JSON input.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  generate_pdf.py --data test.json --output test.pdf
  generate_pdf.py --data clients/neezanizam/deliverables/strategy-260411.json \\
                  --output clients/neezanizam/deliverables/strategy-260411.pdf
""",
    )
    parser.add_argument("--data", required=True,
                        help="Path to the input JSON file (see templates/report-schema.json)")
    parser.add_argument("--output", required=True,
                        help="Path to the output PDF file (directories will be auto-created)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print build progress to stderr")

    args = parser.parse_args()

    try:
        data = load_data(args.data)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"Error loading input data: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        generate(data, args.output, verbose=args.verbose)
    except Exception as e:
        print(f"Error generating PDF: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc(file=sys.stderr)
        sys.exit(2)

    print(f"OK wrote {args.output}")


if __name__ == "__main__":
    main()
