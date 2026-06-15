"""Psychological-coverage tally — the one shared engine for v2 `psych_coverage` tags.

Reads the per-angle `psych_coverage` blocks on a 10-5-5 `dct.json` and produces:
  - compute_tally(dct)   → structured aggregate (counts + which angles sit where)
  - format_tally(dct)    → the block-format human read for HITL Gate 1
  - summarize_tally(dct) → a compact one-line aggregate (per-DCT sheet cell)
  - project_angle(pc)    → a compact per-angle cell ("worry→relief · mirror" [+ flag])

Schema reference: docs/methods/psychological-coverage/v2-tag-schema.md
Field shape (optional, per angle):
  psych_coverage: { valence_arc, self_image, real_loud, tripwire, evidence }
    valence_arc : "<from>" (static) or "<from>-><to>" (arc); tokens worry|relief|neutral
    self_image  : "mirror" | "aspiration"
    real_loud   : bool   (opt-in test lane — genuine deadline/runway/quantified-loss urgency)
    tripwire    : null | "fake_loud" | "guilt_duty"   (auto-flag = likely cold-traffic breach)
    evidence    : cited line from the copy (provenance gate)

Client-agnostic. Untagged angles are skipped gracefully; a wave with zero tagged
angles yields an empty tally (callers treat that as "not tagged", not an error).

CLI:  python3 scripts/psych_coverage_tally.py <path/to/dct.json>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

VALENCE_TOKENS = ("worry", "relief", "neutral")
SELF_IMAGE_TOKENS = ("mirror", "aspiration")
TRIPWIRE_TOKENS = ("fake_loud", "guilt_duty")

# Display glyphs. These land only in tooling output + metadata sheet cells —
# never in rendered ad copy — so unicode is safe here (brand copy bans are separate).
_ARROW = "→"  # →


def _angles(dct: dict) -> list[dict]:
    return dct.get("angles", []) if isinstance(dct, dict) else []


def extract(angle: dict) -> dict | None:
    """Return the angle's psych_coverage block, or None if untagged."""
    pc = angle.get("psych_coverage")
    return pc if isinstance(pc, dict) else None


def lead_valence(arc: str) -> str:
    """The token an ad LEADS on — drives the worry/relief spread question."""
    return (arc or "").split("->")[0].strip()


def to_valence(arc: str) -> str:
    """The token an ad ENDS on (== lead when static)."""
    return (arc or "").split("->")[-1].strip()


def resolves_in_ad(arc: str) -> bool:
    """True when a worry-led ad hands over relief inside the ad (not just in the letter)."""
    return "->" in (arc or "") and to_valence(arc) == "relief"


def compute_tally(dct: dict) -> dict:
    """Aggregate the psych_coverage tags across a wave's angles."""
    angles = _angles(dct)
    tagged = [(a.get("id", "?"), extract(a)) for a in angles]
    tagged = [(aid, pc) for aid, pc in tagged if pc is not None]

    valence_lead: dict[str, list[str]] = {t: [] for t in VALENCE_TOKENS}
    self_image: dict[str, list[str]] = {t: [] for t in SELF_IMAGE_TOKENS}
    resolves: list[str] = []
    real_loud: list[str] = []
    tripwire: dict[str, list[str]] = {t: [] for t in TRIPWIRE_TOKENS}
    missing_evidence: list[str] = []
    warnings: list[str] = []

    for aid, pc in tagged:
        arc = pc.get("valence_arc", "")
        lead = lead_valence(arc)
        if lead in valence_lead:
            valence_lead[lead].append(aid)
        elif lead:
            warnings.append(f"{aid}: valence_arc lead '{lead}' not in {{worry, relief, neutral}}")
        else:
            warnings.append(f"{aid}: valence_arc missing")
        if "->" in arc and to_valence(arc) not in VALENCE_TOKENS:
            warnings.append(f"{aid}: valence_arc target '{to_valence(arc)}' not in {{worry, relief, neutral}}")
        if resolves_in_ad(arc):
            resolves.append(aid)
        si = pc.get("self_image", "")
        if si in self_image:
            self_image[si].append(aid)
        else:
            warnings.append(f"{aid}: self_image '{si}' not in {{mirror, aspiration}}")
        if pc.get("real_loud"):
            real_loud.append(aid)
        trip = pc.get("tripwire")
        if trip in tripwire:
            tripwire[trip].append(aid)
        elif trip is not None:
            warnings.append(f"{aid}: tripwire '{trip}' not in {{null, fake_loud, guilt_duty}}")
        if not (pc.get("evidence") or "").strip():
            missing_evidence.append(aid)

    return {
        "dct_id": dct.get("dct_id", ""),
        "n_angles": len(angles),
        "n_tagged": len(tagged),
        "valence_lead": valence_lead,
        "resolves_in_ad": resolves,
        "self_image": self_image,
        "real_loud": real_loud,
        "tripwire": tripwire,
        "missing_evidence": missing_evidence,
        "warnings": warnings,
    }


def project_angle(pc: dict | None) -> str:
    """Compact per-angle cell, e.g. 'worry→relief · mirror' (+ ' · real-loud' / ' · ⚠fake_loud')."""
    if not pc:
        return ""
    arc = (pc.get("valence_arc") or "").replace("->", _ARROW)
    si = pc.get("self_image", "")
    parts = [p for p in (arc, si) if p]
    cell = " · ".join(parts)
    flags = []
    if pc.get("real_loud"):
        flags.append("real-loud")
    if pc.get("tripwire"):
        flags.append(f"⚠{pc['tripwire']}")  # ⚠
    if flags:
        cell = f"{cell} · {' '.join(flags)}" if cell else " ".join(flags)
    return cell


def summarize_tally(dct: dict) -> str:
    """One-line per-DCT aggregate for a sheet cell.

    e.g. 'worry×4 relief×1 · mirror×3 asp×2 · real-loud:0 · trip:clean'
    Empty string when the wave carries no psych tags (caller writes nothing).
    """
    t = compute_tally(dct)
    if t["n_tagged"] == 0:
        return ""
    vl = t["valence_lead"]
    si = t["self_image"]
    val = " ".join(f"{k}×{len(v)}" for k, v in vl.items() if v)  # ×
    img = " ".join(
        f"{ {'mirror':'mirror','aspiration':'asp'}[k] }×{len(v)}"
        for k, v in si.items() if v
    )
    rl = f"real-loud:{len(t['real_loud'])}"
    n_trip = sum(len(v) for v in t["tripwire"].values())
    trip = "trip:clean" if n_trip == 0 else "trip:" + ",".join(
        f"{k}({len(v)})" for k, v in t["tripwire"].items() if v
    )
    return f"{val} · {img} · {rl} · {trip}"


def _ids(lst: list[str]) -> str:
    return ", ".join(lst) if lst else "none"


def format_tally(dct: dict, label: str = "") -> str:
    """Block-format human read for HITL Gate 1 — the 'stare at the white space' moment."""
    t = compute_tally(dct)
    dct_id = t["dct_id"] or "DCT?"
    head = f"{dct_id}" + (f' — "{label}"' if label else "") + f" ({t['n_tagged']}/{t['n_angles']} angles tagged)"
    if t["n_tagged"] == 0:
        return f"{head}\n  (no psych_coverage tags — run the tagging pass to get a coverage read)"

    vl = t["valence_lead"]
    si = t["self_image"]
    n_rl = len(t["real_loud"])
    n_trip = sum(len(v) for v in t["tripwire"].values())

    lines = [
        "=" * 60,
        head,
        "=" * 60,
        "",
        "Valence (lead -> in-ad arc):",
    ]
    for tok in VALENCE_TOKENS:
        if vl[tok]:
            lines.append(f"  {tok}-led ......... {_ids(vl[tok]):<24} ({len(vl[tok])})")
    lines.append(
        f"  resolves in-ad ... {_ids(t['resolves_in_ad']):<24} ({len(t['resolves_in_ad'])})"
        "   <- worry-led ads that hand over relief; rest leave it to the letter"
    )
    lines += ["", "Self-image:"]
    for tok in SELF_IMAGE_TOKENS:
        if si[tok]:
            lines.append(f"  {tok} ........... {_ids(si[tok]):<24} ({len(si[tok])})")
    if not any(si.values()):
        lines.append("  (none tagged)")
    elif sum(1 for v in si.values() if v) == 1:
        lines.append("  ^ collapsed to ONE self-image — the other door is shut")

    lines += ["", "Test lane (real-loud, opt-in):"]
    if n_rl:
        lines.append(f"  present .......... {_ids(t['real_loud'])} ({n_rl})")
    else:
        lines.append(
            "  count ............ 0   <- WHITE SPACE *if* the offer permits life-trigger "
            "urgency (deadline/runway/quantified loss). Off-limits if the contract forbids urgency."
        )

    lines += ["", "Tripwires (auto-flag):"]
    for tok in TRIPWIRE_TOKENS:
        hits = t["tripwire"][tok]
        flag = "OK" if not hits else f"BREACH -> {_ids(hits)}"
        lines.append(f"  {tok} ....... {len(hits)}   {flag}")

    n_ok_ev = t["n_tagged"] - len(t["missing_evidence"])
    prov = f"\nProvenance: {n_ok_ev}/{t['n_tagged']} carry cited evidence"
    if t["missing_evidence"]:
        prov += f"  (MISSING: {_ids(t['missing_evidence'])})"
    else:
        prov += " — all clean"
    lines.append(prov)
    if t.get("warnings"):
        lines.append("\n⚠ MALFORMED TAGS (out-of-vocab tokens — fix before trusting the read):")  # ⚠
        for w in t["warnings"]:
            lines.append(f"  - {w}")
    return "\n".join(lines)


REPO_ROOT = Path(__file__).resolve().parent.parent


def discover_client_dcts(client_slug: str, campaign_slug: str | None = None) -> list[tuple[Path, dict]]:
    """Every dct.json manifest (with an angles[] array) for a client, optionally one campaign.
    Used by the cross-wave 'prior coverage' report so a new wave can be generated into the gaps."""
    base = REPO_ROOT / "clients" / client_slug / "campaigns"
    if campaign_slug:
        base = base / campaign_slug
    if not base.exists():
        return []
    out: list[tuple[Path, dict]] = []
    for p in sorted(base.rglob("dct.json")):
        try:
            d = json.loads(p.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(d.get("angles"), list):
            out.append((p, d))
    return out


def cross_wave_tally(dcts: list[dict]) -> dict:
    """Aggregate compute_tally across many waves — the client's coverage history."""
    agg = {
        "n_waves": 0, "n_tagged_waves": 0, "n_angles": 0, "n_tagged_angles": 0,
        "valence_lead": {t: 0 for t in VALENCE_TOKENS},
        "self_image": {t: 0 for t in SELF_IMAGE_TOKENS},
        "real_loud": 0,
        "tripwire": {t: 0 for t in TRIPWIRE_TOKENS},
        "per_wave": [], "warnings": [],
    }
    for d in dcts:
        t = compute_tally(d)
        agg["n_waves"] += 1
        agg["n_angles"] += t["n_angles"]
        if t["n_tagged"] == 0:
            agg["per_wave"].append({"dct_id": t["dct_id"], "tagged": 0, "n": t["n_angles"], "summary": ""})
            continue
        agg["n_tagged_waves"] += 1
        agg["n_tagged_angles"] += t["n_tagged"]
        for k in VALENCE_TOKENS:
            agg["valence_lead"][k] += len(t["valence_lead"][k])
        for k in SELF_IMAGE_TOKENS:
            agg["self_image"][k] += len(t["self_image"][k])
        agg["real_loud"] += len(t["real_loud"])
        for k in TRIPWIRE_TOKENS:
            agg["tripwire"][k] += len(t["tripwire"][k])
        agg["warnings"] += t["warnings"]
        agg["per_wave"].append({"dct_id": t["dct_id"], "tagged": t["n_tagged"], "n": t["n_angles"], "summary": summarize_tally(d)})
    return agg


def format_cross_wave(agg: dict, client: str) -> str:
    """The 'prior coverage + white-space' report — run BEFORE picking a new wave's angles."""
    n = agg["n_tagged_angles"]
    lines = [
        "=" * 64,
        f"PRIOR COVERAGE — {client}  ({agg['n_tagged_waves']}/{agg['n_waves']} waves tagged · {n} tagged angles)",
        "=" * 64,
    ]
    if n == 0:
        lines.append("\nNo tagged waves yet — no history to compare against. Tag this wave to start it.")
        return "\n".join(lines)

    vl, si = agg["valence_lead"], agg["self_image"]
    lines += ["", "Valence-lead (all waves):"]
    for tok in VALENCE_TOKENS:
        if vl[tok]:
            lines.append(f"  {tok:<8} {vl[tok]:>3}  ({round(100 * vl[tok] / n)}%)")
    lines += ["", "Self-image (all waves):"]
    for tok in SELF_IMAGE_TOKENS:
        lines.append(f"  {tok:<10} {si[tok]:>3}  ({round(100 * si[tok] / n)}%)")
    n_trip = sum(agg["tripwire"].values())
    lines += [
        "",
        f"Real-loud test lane: {agg['real_loud']}/{n} angles ever",
        f"Tripwires (historical): {'none' if not n_trip else ', '.join(f'{k}×{v}' for k, v in agg['tripwire'].items() if v)}",
        "",
        "Per wave:",
    ]
    for w in agg["per_wave"]:
        if w["tagged"] == 0:
            lines.append(f"  {w['dct_id'] or '(no id)':<12} untagged ({w['n']} angles)")
        else:
            lines.append(f"  {w['dct_id']:<12} {w['summary']}")

    flags = []
    if agg["real_loud"] == 0:
        flags.append("real-loud lane NEVER tested — if offer.md §Urgency permits life-trigger/runway urgency, this is the clearest white space to test.")
    if si["aspiration"] == 0:
        flags.append("aspiration self-image NEVER used — every angle casts who-they-are-now; the aspiration door is shut.")
    elif si["aspiration"] / n < 0.25:
        flags.append(f"aspiration self-image thin ({round(100 * si['aspiration'] / n)}%) — the set leans mirror; a who-they-want-to-be angle is under-covered.")
    if vl["relief"] == 0 and vl["worry"]:
        flags.append("no relief-led angle ever — everything opens on worry; a calm/relief-led entry may reach higher-awareness or warmer readers.")
    if agg["warnings"]:
        flags.append(f"{len(agg['warnings'])} malformed tag(s) in history — fix before trusting this rollup.")
    lines += ["", "WHITE SPACE / flags:"]
    lines += [f"  - {f}" for f in flags] if flags else ["  - none obvious — coverage is broad."]
    return "\n".join(lines)


def _main(argv: list[str]) -> int:
    # cross-wave 'prior coverage' mode: --client <slug> [--campaign <slug>]
    if argv and argv[0] == "--client":
        if len(argv) < 2:
            print("usage: python3 scripts/psych_coverage_tally.py --client <slug> [--campaign <slug>]", file=sys.stderr)
            return 2
        client = argv[1]
        campaign = None
        if "--campaign" in argv:
            i = argv.index("--campaign")
            if i + 1 >= len(argv):
                print("--campaign requires a value (the campaign slug)", file=sys.stderr)
                return 2
            campaign = argv[i + 1]
        dcts = [d for _, d in discover_client_dcts(client, campaign)]
        if not dcts:
            where = f" campaign '{campaign}'" if campaign else ""
            print(f"no dct.json manifests found for client '{client}'{where}", file=sys.stderr)
            return 2
        print(format_cross_wave(cross_wave_tally(dcts), client))
        return 0

    # single-wave mode: <path/to/dct.json>
    if len(argv) != 1:
        print("usage: python3 scripts/psych_coverage_tally.py <path/to/dct.json>"
              "   |   --client <slug> [--campaign <slug>]", file=sys.stderr)
        return 2
    p = Path(argv[0])
    if not p.exists():
        print(f"no such file: {p}", file=sys.stderr)
        return 2
    dct = json.loads(p.read_text())
    label = (dct.get("avatar", "") or "").split(":")[0].strip()
    print(format_tally(dct, label=label))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
