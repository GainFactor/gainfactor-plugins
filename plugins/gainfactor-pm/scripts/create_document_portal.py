#!/usr/bin/env python3
"""Create or extend a document review portal from the bundled UI template."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = PLUGIN_ROOT / "assets" / "document-review-portal"
MANIFEST_NAME = ".gainfactor-documents.json"
LAUNCHER_SCRIPT = "portal-control.py"
GROUPS = {
    "product-requirements": {
        "title": "产品需求",
        "types": {
            "PRODUCT-DEFINITION",
            "USER-PERSONA",
            "COMPETITIVE-ANALYSIS",
            "BRD",
            "PRD",
            "USER-JOURNEY",
        },
    },
    "technical-design": {"title": "技术设计", "types": {"API", "API-CONTRACT", "HLD", "LLD"}},
    "quality-delivery": {
        "title": "质量与交付",
        "types": {"TEST-STRATEGY", "TEST-SPEC", "RUNBOOK"},
    },
    "other": {"title": "其他文档", "types": set()},
}


def default_slug(path: Path) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
    return slug or "document"


def load_manifest(target: Path) -> dict:
    path = target / MANIFEST_NAME
    if not path.exists():
        return {"documents": {}}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("documents"), dict):
        raise ValueError(f"Invalid portal manifest: {path}")
    return value


def default_group(document_type: str) -> str:
    normalized = re.sub(r"[ _]+", "-", document_type.strip().upper())
    for group, config in GROUPS.items():
        if normalized in config["types"]:
            return group
    return "other"


def write_navigation(target: Path, manifest: dict) -> None:
    docs_root = target / "content/docs"
    active_groups: dict[str, list[str]] = {}
    for route, document in manifest["documents"].items():
        group = document["group"]
        active_groups.setdefault(group, []).append(Path(route).name)

    root_pages = ["index"]
    for group in GROUPS:
        pages = active_groups.get(group)
        if not pages:
            continue
        root_pages.append(group)
        group_root = docs_root / group
        group_root.mkdir(parents=True, exist_ok=True)
        (group_root / "meta.json").write_text(
            json.dumps(
                {"title": GROUPS[group]["title"], "pages": pages},
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )

    (docs_root / "meta.json").write_text(
        json.dumps({"pages": root_pages}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_portal_data(target: Path, manifest: dict) -> None:
    serialized = json.dumps(manifest, ensure_ascii=False, indent=2)
    (target / MANIFEST_NAME).write_text(serialized + "\n", encoding="utf-8")
    (target / "lib/portal-data.generated.ts").write_text(
        "import type { PortalData } from './portal-data';\n\n"
        f"export const portalData: PortalData = {serialized};\n",
        encoding="utf-8",
    )
    write_navigation(target, manifest)


def install_launchers(target: Path) -> None:
    scripts_directory = target / "scripts"
    scripts_directory.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TEMPLATE_ROOT / "scripts" / LAUNCHER_SCRIPT, scripts_directory / LAUNCHER_SCRIPT)
    launchers = {
        "打开文档门户.command": "open",
        "关闭文档门户.command": "stop",
    }
    for filename, action in launchers.items():
        launcher = target / filename
        launcher.write_text(
            "#!/bin/zsh\n"
            "PORTAL_DIR=\"${0:A:h}\"\n"
            f'exec python3 "$PORTAL_DIR/scripts/{LAUNCHER_SCRIPT}" {action} "$PORTAL_DIR"\n',
            encoding="utf-8",
        )
        launcher.chmod(0o755)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", type=Path, help="Markdown or MDX document")
    parser.add_argument("target", type=Path, help="Portal output directory")
    parser.add_argument("--slug", default="", help="Stable URL slug inside the portal")
    parser.add_argument("--type", dest="document_type", default="文档")
    parser.add_argument("--collection", default="产品文档")
    parser.add_argument("--group", choices=GROUPS, help="Optional navigation group override")
    parser.add_argument("--version", default="")
    parser.add_argument("--status", default="待评审")
    parser.add_argument("--owner", default="未指定")
    parser.add_argument("--updated", default=date.today().isoformat())
    parser.add_argument("--review", type=Path, help="Optional structured review JSON")
    parser.add_argument("--presentation", type=Path, help="Generic Portal Presentation JSON")
    parser.add_argument("--rich", action="store_true", help="Require a valid presentation manifest")
    args = parser.parse_args()
    if args.rich and not args.presentation:
        parser.error("--rich requires --presentation=<portal-presentation.json>")

    document = args.document.resolve()
    target = args.target.resolve()
    slug = args.slug.strip("/") or default_slug(document)
    if not document.is_file():
        parser.error(f"Document does not exist: {document}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        parser.error("Slug must contain lowercase letters, digits, and hyphens")

    if not target.exists() or not any(target.iterdir()):
        shutil.copytree(
            TEMPLATE_ROOT,
            target,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("node_modules", ".next", ".source", "out", "*.tsbuildinfo"),
        )
    elif not (target / MANIFEST_NAME).is_file():
        parser.error(f"Target is not a GainFactor document portal: {target}")

    manifest = load_manifest(target)
    existing_route = next(
        (
            route
            for route, value in manifest["documents"].items()
            if value.get("sourceSlug") == slug or route == slug
        ),
        None,
    )
    existing_document = manifest["documents"].get(existing_route, {})
    group = existing_document.get("group") or args.group or default_group(args.document_type)
    route = existing_route or f"{group}/{slug}"
    if existing_route and "/" not in existing_route:
        route = f"{group}/{slug}"
        legacy_path = target / f"content/docs/{existing_route}.mdx"
        migrated_path = target / f"content/docs/{route}.mdx"
        migrated_path.parent.mkdir(parents=True, exist_ok=True)
        if legacy_path.is_file():
            legacy_path.replace(migrated_path)
        manifest["documents"].pop(existing_route)
    output_path = f"content/docs/{route}.mdx"
    (target / output_path).parent.mkdir(parents=True, exist_ok=True)
    command = [
        "node",
        "scripts/import-document.mjs",
        str(document),
        output_path,
    ]
    subprocess.run(command, cwd=target, check=True)
    compile_command = [
            "python3",
            str(PLUGIN_ROOT / "scripts/compile_portal_document.py"),
            str(target / output_path),
        ]
    if args.presentation:
        compile_command.append(f"--presentation={args.presentation.resolve()}")
    if args.rich:
        compile_command.append("--validate")
    compiled = subprocess.run(
        compile_command,
        check=True,
        capture_output=True,
        text=True,
    )
    presentation_payload = json.loads(compiled.stdout)

    review = {"conclusion": "尚未生成评审结果", "issues": []}
    if args.review:
        review_path = args.review.resolve()
        if not review_path.is_file():
            parser.error(f"Review JSON does not exist: {review_path}")
        review = json.loads(review_path.read_text(encoding="utf-8"))
        if not isinstance(review.get("conclusion"), str) or not isinstance(review.get("issues"), list):
            parser.error("Review JSON must contain a string conclusion and an issues array")
        for issue in review["issues"]:
            required = ("id", "severity", "title", "sectionId")
            if not isinstance(issue, dict) or any(not isinstance(issue.get(key), str) for key in required):
                parser.error(f"Each review issue must contain string fields: {', '.join(required)}")
            if issue["severity"] not in {"P0", "P1", "P2"}:
                parser.error("Review issue severity must be P0, P1, or P2")

    manifest["documents"][route] = {
        "sourceSlug": slug,
        "group": group,
        "documentType": args.document_type,
        "collection": args.collection,
        "version": args.version or "—",
        "status": args.status,
        "owner": args.owner,
        "updated": args.updated,
        "presentation": presentation_payload["presentation"],
        "review": review,
    }
    write_portal_data(target, manifest)
    install_launchers(target)
    print(f"Added {args.document_type} document at /docs/{route}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
