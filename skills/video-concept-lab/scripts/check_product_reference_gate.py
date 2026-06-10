#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def image_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate product references before product-inclusive image generation.")
    parser.add_argument("--client", required=True, help="Client folder, e.g. clients/takekine")
    parser.add_argument("--product", required=True, help="Product asset folder slug, e.g. ferrovia")
    args = parser.parse_args()

    root = Path(args.client) / "_brand" / "brand-assets" / args.product
    manifest = root / "product-reference-manifest.json"
    pack_refs = image_files(root / "product-packshots") + image_files(root / "packaging")
    strip_refs = image_files(root / "strip-references")

    errors = []
    if not manifest.exists():
        errors.append(f"missing manifest: {manifest}")
    else:
        try:
            data = json.loads(manifest.read_text())
        except Exception as exc:  # pragma: no cover - diagnostic script
            errors.append(f"manifest is not valid JSON: {exc}")
        else:
            for ref in data.get("references", []):
                rel = ref.get("path")
                if not rel:
                    errors.append("manifest reference missing path")
                    continue
                if not (root / rel).exists():
                    errors.append(f"manifest reference missing on disk: {root / rel}")

    if not pack_refs:
        errors.append(f"missing product pack/packaging image under {root}/product-packshots or {root}/packaging")
    if not strip_refs:
        errors.append(f"missing strip reference image under {root}/strip-references")

    if errors:
        print("PRODUCT_REFERENCE_GATE=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PRODUCT_REFERENCE_GATE=PASS")
    print(f"manifest={manifest}")
    print(f"packaging_or_packshot_refs={len(pack_refs)}")
    print(f"strip_refs={len(strip_refs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
