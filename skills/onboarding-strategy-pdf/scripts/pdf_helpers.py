"""
pdf_helpers.py — Reusable reportlab primitives for onboarding-strategy-pdf

Hormozi-revised visual system: no composite score gauge, no A+ -> F letter grade.
Instead: 1-5 RYG per dimension, primary constraint callout, Calculator Close
dollar figures, Plus/Minus Potential Map.

Helpers are skill-local at v1. If a second skill needs them, promote to
document-skills/pdf/scripts/ads_report_helpers.py per the plan.

Attribution: Color palette, table style conventions, and Drawing/Circle/Rect
patterns adapted from zubair-trabzada/ai-ads-claude (MIT). The composite-score
primitives (draw_score_gauge, score_grade) are NOT ported — rejected after
Hormozi AI notebook consultation on 2026-04-11.
"""

from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.graphics.shapes import Drawing, Rect, Circle, String, Line


# ---------------------------------------------------------------------------
# Color palette — rebrand in one place
# ---------------------------------------------------------------------------
COLORS = {
    "primary":    HexColor("#1a1a2e"),  # Deep navy — headings, titles
    "accent":     HexColor("#2563eb"),  # Bright blue — subheadings, links
    "highlight":  HexColor("#f97316"),  # Orange — constraint callouts, emphasis
    "success":    HexColor("#22c55e"),  # Green — Green band (score 4-5)
    "warning":    HexColor("#eab308"),  # Amber — Yellow band (score 3)
    "danger":     HexColor("#ef4444"),  # Red — Red band (score 1-2), primary constraint
    "light_bg":   HexColor("#f0f4f8"),  # Subtle row backgrounds
    "constraint_bg": HexColor("#fef3c7"),  # Gold — highlights primary constraint row
    "text":       HexColor("#1e293b"),
    "text_light": HexColor("#64748b"),
    "border":     HexColor("#cbd5e1"),
    "white":      white,
    "black":      black,
}


# ---------------------------------------------------------------------------
# Band helpers (1-5 RYG system)
# ---------------------------------------------------------------------------
def score_to_band(score):
    """Convert a 1-5 integer score to band string.

    Red = 1-2 (critical / needs immediate attention)
    Yellow = 3 (average / needs work)
    Green = 4-5 (strong / optimized)
    """
    if score <= 2:
        return "red"
    if score == 3:
        return "yellow"
    return "green"


def band_color(band):
    """Return the reportlab color for a band string."""
    return {
        "red":    COLORS["danger"],
        "yellow": COLORS["warning"],
        "green":  COLORS["success"],
    }.get(band, COLORS["text_light"])


def band_label(band):
    """Return a human-readable label for a band string."""
    return {
        "red":    "Critical",
        "yellow": "Needs Work",
        "green":  "Strong",
    }.get(band, "Unknown")


# ---------------------------------------------------------------------------
# Paragraph styles
# ---------------------------------------------------------------------------
def get_styles():
    """Create custom paragraph styles used across all pages."""
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "OsTitle", parent=base["Title"],
            fontSize=30, textColor=COLORS["primary"],
            spaceAfter=6, fontName="Helvetica-Bold", leading=36,
        ),
        "subtitle": ParagraphStyle(
            "OsSubtitle", parent=base["Normal"],
            fontSize=14, textColor=COLORS["text_light"],
            spaceAfter=6, fontName="Helvetica",
        ),
        "heading": ParagraphStyle(
            "OsHeading", parent=base["Heading1"],
            fontSize=20, textColor=COLORS["primary"],
            spaceBefore=16, spaceAfter=10, fontName="Helvetica-Bold",
        ),
        "subheading": ParagraphStyle(
            "OsSubheading", parent=base["Heading2"],
            fontSize=14, textColor=COLORS["accent"],
            spaceBefore=12, spaceAfter=6, fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "OsBody", parent=base["Normal"],
            fontSize=10, textColor=COLORS["text"],
            spaceAfter=6, fontName="Helvetica", leading=14,
        ),
        "body_small": ParagraphStyle(
            "OsBodySmall", parent=base["Normal"],
            fontSize=8, textColor=COLORS["text"],
            spaceAfter=4, fontName="Helvetica", leading=11,
        ),
        "footer": ParagraphStyle(
            "OsFooter", parent=base["Normal"],
            fontSize=8, textColor=COLORS["text_light"],
            fontName="Helvetica",
        ),
        "constraint_bold": ParagraphStyle(
            "OsConstraintBold", parent=base["Normal"],
            fontSize=16, textColor=COLORS["danger"],
            fontName="Helvetica-Bold", leading=20, spaceAfter=8,
        ),
        "dollar_callout": ParagraphStyle(
            "OsDollarCallout", parent=base["Normal"],
            fontSize=22, textColor=COLORS["highlight"],
            fontName="Helvetica-Bold", leading=26, spaceAfter=6, alignment=1,
        ),
        "dream_quote": ParagraphStyle(
            "OsDreamQuote", parent=base["Normal"],
            fontSize=13, textColor=COLORS["primary"],
            fontName="Helvetica-Oblique", leading=18, spaceAfter=12,
            leftIndent=20, rightIndent=20,
        ),
        "section_intro": ParagraphStyle(
            "OsSectionIntro", parent=base["Normal"],
            fontSize=11, textColor=COLORS["text"],
            fontName="Helvetica", leading=15, spaceAfter=10,
        ),
    }


# ---------------------------------------------------------------------------
# Table style factory
# ---------------------------------------------------------------------------
def standard_table_style(extra=None):
    """Base TableStyle with header, alternating rows, grid, padding.

    Pass `extra` (a list of style commands) to layer per-use customizations
    such as highlighting the primary-constraint row.
    """
    cmds = [
        ("BACKGROUND",   (0, 0), (-1, 0),  COLORS["primary"]),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  COLORS["white"]),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, -1), 9),
        ("GRID",         (0, 0), (-1, -1), 0.5, COLORS["border"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLORS["white"], COLORS["light_bg"]]),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",   (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",  (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    if extra:
        cmds.extend(extra)
    return TableStyle(cmds)


# ---------------------------------------------------------------------------
# Constraint Callout (Page 1 Cover) — Hormozi Calculator Close
# ---------------------------------------------------------------------------
def draw_constraint_callout(dimension_name, monthly_usd, annual_usd, width=500, height=170):
    """Cover-page element: large red/orange callout showing THE primary
    constraint + monthly and annual Ignorance Tax dollar figures.

    Replaces the rejected circular score gauge. Renders as a Drawing
    containing a bordered box with three text tiers.
    """
    d = Drawing(width, height)

    # Outer border (subtle red/orange frame)
    d.add(Rect(2, 2, width - 4, height - 4,
               fillColor=COLORS["light_bg"],
               strokeColor=COLORS["danger"],
               strokeWidth=2, rx=8, ry=8))

    # Top label — "The One Constraint"
    d.add(String(width / 2, height - 28, "THE ONE CONSTRAINT",
                 fontSize=10, fillColor=COLORS["text_light"],
                 textAnchor="middle", fontName="Helvetica-Bold"))

    # Dimension name (bold, dark)
    display_name = dimension_name.replace("_", " ").title()
    d.add(String(width / 2, height - 58, display_name,
                 fontSize=22, fillColor=COLORS["primary"],
                 textAnchor="middle", fontName="Helvetica-Bold"))

    # Monthly cost (big, orange)
    monthly_str = _format_usd(monthly_usd)
    d.add(String(width / 2, height - 96, f"{monthly_str} / month",
                 fontSize=26, fillColor=COLORS["highlight"],
                 textAnchor="middle", fontName="Helvetica-Bold"))

    # Annual cost (smaller, subdued)
    annual_str = _format_usd(annual_usd)
    d.add(String(width / 2, height - 122, f"Annual Ignorance Tax: {annual_str}",
                 fontSize=11, fillColor=COLORS["text"],
                 textAnchor="middle", fontName="Helvetica"))

    # Bottom note line
    d.add(String(width / 2, height - 146, "This is what it costs to not solve this one thing.",
                 fontSize=9, fillColor=COLORS["text_light"],
                 textAnchor="middle", fontName="Helvetica-Oblique"))

    return d


def _format_usd(amount):
    """Format a number as USD with thousands separators."""
    try:
        return f"${int(round(float(amount))):,}"
    except (TypeError, ValueError):
        return "$0"


# ---------------------------------------------------------------------------
# RYG Diagnostic Table (Page 2)
# ---------------------------------------------------------------------------
def create_ryg_table(dimensions, styles):
    """Render the Page 2 diagnostic as a reportlab Table.

    `dimensions` is a list of dicts, each shaped:
        {
            "name": "Creative Direction",
            "score": 2,                # int 1-5
            "band": "red",             # red / yellow / green
            "action": "Rebuild creative from sophistication audit",
            "is_primary_constraint": True,
        }

    The primary-constraint row is visually highlighted with a gold background
    + bold border. All rows use the band color for the score pill and label.
    """
    header = ["Dimension", "Score", "Band", "Prescribed Action"]
    rows = [header]

    for dim in dimensions:
        name = dim.get("name", "")
        score = dim.get("score", 0)
        band = dim.get("band") or score_to_band(score)
        action = dim.get("action", "")
        label = band_label(band)

        # Score cell shows "3 / 5" with band color
        score_cell = f"{score} / 5"
        band_cell = label

        rows.append([
            Paragraph(f"<b>{name}</b>", styles["body"]),
            score_cell,
            band_cell,
            Paragraph(action, styles["body_small"]),
        ])

    table = Table(rows, colWidths=[140, 60, 90, 210])

    # Build style extras: color the score + band cells per row, and
    # highlight the primary-constraint row.
    extra = [
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]

    for i, dim in enumerate(dimensions, start=1):
        band = dim.get("band") or score_to_band(dim.get("score", 0))
        color = band_color(band)
        extra.append(("TEXTCOLOR", (1, i), (2, i), color))
        extra.append(("FONTNAME", (1, i), (2, i), "Helvetica-Bold"))

        if dim.get("is_primary_constraint"):
            extra.append(("BACKGROUND", (0, i), (-1, i), COLORS["constraint_bg"]))
            extra.append(("LINEABOVE", (0, i), (-1, i), 1.5, COLORS["highlight"]))
            extra.append(("LINEBELOW", (0, i), (-1, i), 1.5, COLORS["highlight"]))

    table.setStyle(standard_table_style(extra))
    return table


# ---------------------------------------------------------------------------
# Plus/Minus Potential Map (Page 6)
# ---------------------------------------------------------------------------
def create_plus_minus_map(work_with_us, stay_current, styles):
    """Two-column visual contrasting future states.

    `work_with_us` and `stay_current` are dicts shaped:
        {"more": ["item1", "item2"], "less": ["item3"]}

    Returns a reportlab Table.
    """
    def _build_column(payload, title, accent_color):
        lines = [Paragraph(f"<b><font color='{accent_color.hexval()}'>{title}</font></b>", styles["subheading"])]
        more = payload.get("more", [])
        less = payload.get("less", [])
        if more:
            lines.append(Paragraph("<b>More of:</b>", styles["body"]))
            for item in more:
                lines.append(Paragraph(f"+ {item}", styles["body_small"]))
        if less:
            lines.append(Paragraph("<b>Less of:</b>", styles["body"]))
            for item in less:
                lines.append(Paragraph(f"- {item}", styles["body_small"]))
        return lines

    left_col = _build_column(work_with_us, "Work With Us", COLORS["success"])
    right_col = _build_column(stay_current, "Stay Current Path", COLORS["danger"])

    # Balance column heights by padding shorter column with Spacers
    # (simplified: just let reportlab handle uneven heights)
    data = [[left_col, right_col]]
    table = Table(data, colWidths=[245, 245])
    table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, COLORS["border"]),
        ("LINEBEFORE", (1, 0), (1, 0), 1, COLORS["border"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("BACKGROUND", (0, 0), (0, 0), HexColor("#f0fdf4")),  # Subtle green tint
        ("BACKGROUND", (1, 0), (1, 0), HexColor("#fef2f2")),  # Subtle red tint
    ]))
    return table


# ---------------------------------------------------------------------------
# Generic horizontal bar chart (kept from zubair, repurposed)
# ---------------------------------------------------------------------------
def create_bar_chart(categories, scores, max_score=5, width=470, height=180):
    """Horizontal bar chart used as a general utility.

    Defaults to max_score=5 for the 1-5 RYG system (NOT the 0-100 composite
    score rejected after Hormozi consultation). Can be used for ancillary
    visuals like the Plus/Minus Map density chart if desired.
    """
    d = Drawing(width, height)

    bar_height = 20
    gap = 10
    max_bar_width = width - 190
    start_y = height - 25
    label_x = 5
    bar_x = 165

    for i, (cat, score) in enumerate(zip(categories, scores)):
        y = start_y - i * (bar_height + gap)

        d.add(String(label_x, y + 5, str(cat)[:25],
                     fontSize=9, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica"))

        d.add(Rect(bar_x, y, max_bar_width, bar_height,
                   fillColor=COLORS["light_bg"], strokeColor=None, rx=3))

        bar_width = max((float(score) / max_score) * max_bar_width, 2)
        color = band_color(score_to_band(int(round(score))))
        d.add(Rect(bar_x, y, bar_width, bar_height,
                   fillColor=color, strokeColor=None, rx=3))

        d.add(String(bar_x + max_bar_width + 10, y + 5, f"{score}/{max_score}",
                     fontSize=10, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica-Bold"))

    return d
