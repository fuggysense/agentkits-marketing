#!/usr/bin/env python3
"""Push a DCT wave's rendered images into Canva as ONE design with one image per page.

Method (validated live 260610, Eugene DCT002 wave 1 -> design DAHMJ4jWRwo, 10 pages):
    1. Stitch the workspace's rendered PNGs into a single lossless PDF
       (`uvx img2pdf` — PNG passthrough, no recompression).
    2. Upload the PDF to the wave's Drive folder via `gws` (creates + link-shares
       the folder if missing) so Canva can fetch it.
    3. Fire a Canva "Create URL Import Job" via `one` — a multi-page PDF imports
       as a multi-page design, one image per page.
    4. Poll the job, verify the page count matches the image count, and patch
       dct.json: canva_design_id, stable canva_link, canva_method,
       creatives_pdf_drive_id, creatives_drive_folder.

Why this method (and not per-image asset uploads): Canva's public API cannot
place elements onto an existing design's pages, and API-uploaded library assets
hide under the editor's Projects tab (NOT Uploads), which confuses reviewers.
The PDF import is the only programmatic way to get every render visible on
pages in one design. See skills/ad-concept-engine/corrections.md (260610).

Gotchas encoded:
    - Canva's URL fetcher needs a clean 200. Use
      `drive.usercontent.google.com/download?id=<ID>&export=download` for the
      PDF (Drive serves it as octet-stream, so pass mime_type=application/pdf).
      `drive.google.com/uc?...` fails with fetch_failed.
    - URL import jobs poll at GET /v1/url-imports/{jobId} — NOT /v1/imports/.
    - Store the stable `https://www.canva.com/design/<ID>/edit` form; the
      API's returned edit_url is tokenised and expires.

Usage:
    python3 scripts/canva_push.py --dct clients/<c>/campaigns/<camp>/dcts/<dct>/dct.json
    python3 scripts/canva_push.py --dct <path> --dry-run
    python3 scripts/canva_push.py --dct <path> --force   # re-import even if a design exists

Idempotent: if dct.json already records a url-import-pdf design, the script
no-ops unless --force (each import creates a NEW design — the old one is
archived in dct.json, never deleted). Prerequisites: `one` (canva connected),
`gws`, `uvx`.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

CANVA_CONNECTION_KEY = "live::canva::default::a7dda6c201db4e75bde87c2493dc017f"
ACT_URL_IMPORT = "conn_mod_def::GJ1DE0VPRlE::RRpB7VW0QDmQuXevitMHRw"   # POST /rest/v1/url-imports
ACT_URL_IMPORT_RESULT = "conn_mod_def::GJ1DFCpxvb8::qAdgE2NuRjqT5A3Xdr3RrQ"  # GET /v1/url-imports/{jobId}
ACT_LIST_PAGES = "conn_mod_def::GJ1DEcegNS8::ZnonuELyT064Q05H-5WBaA"   # GET /v1/designs/{designId}/pages

POLL_INTERVAL_S = 8
POLL_DEADLINE_S = 300


def parse_one_response(stdout: str) -> dict:
    """`one` prints a spinner + 'Response:' before the JSON. Brace-balance it out."""
    anchor = stdout.find("Response:")
    if anchor < 0:
        raise RuntimeError(f"No 'Response:' in `one` output:\n{stdout[-500:]}")
    start = stdout.find("{", anchor)
    depth = 0
    for i, ch in enumerate(stdout[start:], start=start):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return json.loads(stdout[start : i + 1])
    raise RuntimeError(f"Unbalanced JSON in `one` response:\n{stdout[start:][-500:]}")


def one_exec(action: str, data: dict | None = None, path_vars: dict | None = None) -> dict:
    cmd = ["one", "actions", "execute", "canva", action, CANVA_CONNECTION_KEY]
    if data is not None:
        cmd += ["--data", json.dumps(data)]
    if path_vars is not None:
        cmd += ["--path-vars", json.dumps(path_vars)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"`one` exited {r.returncode}: {r.stderr[-300:]}{r.stdout[-300:]}")
    return parse_one_response(r.stdout)


def gws(args: list[str]) -> dict:
    r = subprocess.run(["gws"] + args, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"`gws` exited {r.returncode}: {r.stderr[-300:]}{r.stdout[-300:]}")
    out = r.stdout
    start = out.find("{")
    if start < 0:
        raise RuntimeError(f"No JSON in gws output: {out[-300:]}")
    return json.loads(out[start:])


def build_pdf(images: list[Path], out_pdf: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"pdf [dry-run]: would stitch {len(images)} PNGs -> {out_pdf.name}")
        return
    r = subprocess.run(["uvx", "img2pdf", "--output", str(out_pdf)] + [str(p) for p in images],
                       capture_output=True, text=True, timeout=300)
    if r.returncode != 0 or not out_pdf.exists():
        raise RuntimeError(f"img2pdf failed: {r.stderr[-300:]}")
    print(f"pdf: {out_pdf.name} ({out_pdf.stat().st_size:,} bytes, {len(images)} pages)")


def ensure_drive_folder(dct: dict, dry_run: bool) -> str | None:
    folder_url = dct.get("creatives_drive_folder")
    if folder_url:
        return folder_url.rstrip("/").split("/")[-1]
    if dry_run:
        print("drive [dry-run]: would create + link-share the wave folder")
        return None
    title = f"{dct.get('client', dct.get('campaign', 'client'))} - {dct['dct_id']} Wave Creatives"
    resp = gws(["drive", "files", "create", "--json",
                json.dumps({"name": title, "mimeType": "application/vnd.google-apps.folder"}),
                "--format", "json"])
    folder_id = resp["id"]
    gws(["drive", "permissions", "create",
         "--params", json.dumps({"fileId": folder_id}),
         "--json", json.dumps({"role": "reader", "type": "anyone"}),
         "--format", "json"])
    dct["creatives_drive_folder"] = f"https://drive.google.com/drive/folders/{folder_id}"
    print(f"drive: created shared folder {folder_id}")
    return folder_id


def main() -> int:
    ap = argparse.ArgumentParser(description="Import a DCT wave's renders into Canva as one multi-page design.")
    ap.add_argument("--dct", required=True, help="Path to the workspace dct.json")
    ap.add_argument("--dry-run", action="store_true", help="Preview without building, uploading, or importing.")
    ap.add_argument("--force", action="store_true",
                    help="Re-import even if a url-import-pdf design already exists (creates a NEW design).")
    args = ap.parse_args()

    dct_path = Path(args.dct).resolve()
    if not dct_path.exists():
        raise SystemExit(f"Not found: {dct_path}")
    dct = json.loads(dct_path.read_text())
    if "image_pool" not in dct:
        raise SystemExit("dct.json has no image_pool — this script expects the dct.json (10-5-5) shape.")

    if dct.get("canva_design_id") and str(dct.get("canva_method", "")).startswith("url-import-pdf") and not args.force:
        print(f"canva: design {dct['canva_design_id']} already imported ({dct['canva_link']}) — no-op. "
              f"Use --force to re-import.")
        return 0

    images = []
    for img in dct["image_pool"]["images"]:
        if img.get("status") != "rendered":
            continue
        local = dct_path.parent / img["file"]
        if not local.exists():
            raise SystemExit(f"Rendered image missing on disk: {local}")
        images.append(local)
    if not images:
        raise SystemExit("No rendered images in image_pool — render first (phase_3).")

    pdf_path = dct_path.parent / "images" / f"{dct['dct_id']}-wave-creatives.pdf"
    build_pdf(images, pdf_path, args.dry_run)
    folder_id = ensure_drive_folder(dct, args.dry_run)

    if args.dry_run:
        print(f"canva [dry-run]: would upload PDF to Drive, import as a {len(images)}-page design, "
              f"verify pages, patch dct.json")
        return 0

    resp = gws(["drive", "+upload", str(pdf_path), "--parent", folder_id, "--format", "json"])
    pdf_id = resp["id"]
    pdf_url = f"https://drive.usercontent.google.com/download?id={pdf_id}&export=download"
    print(f"drive: PDF uploaded -> {pdf_id}")

    title = f"{dct.get('client', 'client')}_{dct['dct_id']}_wave-creatives"
    job = one_exec(ACT_URL_IMPORT, data={"title": title, "url": pdf_url, "mime_type": "application/pdf"})
    job_id = (job.get("job") or job)["id"]
    print(f"canva: import job {job_id}")

    design = None
    deadline = time.time() + POLL_DEADLINE_S
    while time.time() < deadline:
        time.sleep(POLL_INTERVAL_S)
        j = (lambda r: r.get("job") or r)(one_exec(ACT_URL_IMPORT_RESULT, path_vars={"jobId": job_id}))
        status = j.get("status")
        if status == "success":
            design = (j.get("result") or {}).get("designs", [None])[0]
            break
        if status == "failed":
            raise SystemExit(f"canva import failed: {j.get('error')}")
    if not design:
        raise SystemExit("canva import poll timed out")

    pages = one_exec(ACT_LIST_PAGES, path_vars={"designId": design["id"]})
    n_pages = len(pages.get("items") or pages.get("pages") or [])
    if n_pages != len(images):
        print(f"WARNING: imported design has {n_pages} pages, expected {len(images)} — inspect before sharing.")

    if dct.get("canva_design_id"):
        dct.setdefault("canva_designs_archived", []).append(
            {"id": dct["canva_design_id"], "link": dct.get("canva_link"),
             "note": f"superseded by re-import {design['id']}"})
    dct["canva_design_id"] = design["id"]
    dct["canva_link"] = f"https://www.canva.com/design/{design['id']}/edit"  # stable, non-expiring form
    dct["canva_method"] = f"url-import-pdf ({n_pages} pages)"
    dct["creatives_pdf_drive_id"] = pdf_id
    dct_path.write_text(json.dumps(dct, indent=2, ensure_ascii=False) + "\n")

    print(f"\nSUMMARY: design={dct['canva_link']} pages={n_pages}/{len(images)} — dct.json patched.")
    print("Sheet CANVA LINK cell takes dct.json's canva_link at the sheet step (or update it manually).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
