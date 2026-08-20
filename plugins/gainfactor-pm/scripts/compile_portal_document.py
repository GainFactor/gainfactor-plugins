#!/usr/bin/env python3
"""Validate and compile a generic Portal Presentation manifest."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CAPABILITIES_PATH = Path(__file__).resolve().parent.parent / "assets/document-review-portal/portal-capabilities.json"
SUPPORTED_MODULES = set(json.loads(CAPABILITIES_PATH.read_text(encoding="utf-8"))["presentationModules"])
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+[\"'][^)]*[\"'])?\)")
PROFILE = re.compile(r"<Profile\b(?P<attributes>.*?)(?:/?>)", re.DOTALL)
PROFILE_IMAGE = re.compile(r"\bimage\s*=\s*\{\{(?P<properties>.*?)\}\}", re.DOTALL)


def jsx_string_property(properties: str, name: str) -> str | None:
    match = re.search(rf"\b{re.escape(name)}\s*:\s*([\"'])(.*?)\1", properties, re.DOTALL)
    return match.group(2).strip() if match else None


def source_images(document: str) -> tuple[dict[str, str], set[str]]:
    candidates = [(alt.strip(), target) for alt, target in IMAGE.findall(document)]
    for profile in PROFILE.finditer(document):
        image = PROFILE_IMAGE.search(profile.group("attributes"))
        if not image:
            continue
        properties = image.group("properties")
        src = jsx_string_property(properties, "src")
        alt = jsx_string_property(properties, "alt")
        if src and alt:
            candidates.append((alt, src))

    images: dict[str, str] = {}
    ambiguous: set[str] = set()
    for alt, src in candidates:
        if not alt:
            continue
        existing = images.get(alt)
        if existing is not None and existing != src:
            ambiguous.add(alt)
        else:
            images[alt] = src
    return images, ambiguous


def load_manifest(path: Path | None) -> dict:
    if path is None:
        return {"schemaVersion": 1, "layout": "document", "modules": []}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Presentation manifest must be a JSON object")
    return value


def resolve_source_images(markdown: str, presentation: dict) -> None:
    images, ambiguous = source_images(markdown)
    for module in presentation.get("modules", []):
        for item in module.get("items", []):
            alt = item.pop("sourceImageAlt", None)
            if alt and not item.get("image"):
                item.setdefault("imageAlt", alt)
                if alt in ambiguous:
                    item["image"] = ""
                    item["_ambiguousImageAlt"] = alt
                else:
                    item["image"] = images.get(alt, "")
                if not item["image"] and alt not in ambiguous:
                    item["_unresolvedImageAlt"] = alt


def validate(presentation: dict) -> list[str]:
    errors: list[str] = []
    if presentation.get("schemaVersion") != 1:
        errors.append("schemaVersion 必须为 1")
    if presentation.get("layout", "document") not in {"document", "report", "reference"}:
        errors.append("layout 必须为 document、report 或 reference")
    modules = presentation.get("modules")
    if not isinstance(modules, list):
        return errors + ["modules 必须为数组"]
    seen: set[str] = set()
    for index, module in enumerate(modules):
        location = f"modules[{index}]"
        if not isinstance(module, dict):
            errors.append(f"{location} 必须为对象")
            continue
        module_id = module.get("id")
        if not isinstance(module_id, str) or not module_id:
            errors.append(f"{location}.id 必须为非空字符串")
        elif module_id in seen:
            errors.append(f"模块 id 重复：{module_id}")
        else:
            seen.add(module_id)
        module_type = module.get("type")
        if module_type not in SUPPORTED_MODULES:
            errors.append(f"{location}.type 不受支持：{module_type}")
            continue
        if module_type in {"metrics", "cards", "steps"} and not isinstance(module.get("items"), list):
            errors.append(f"{location}.items 必须为数组")
        if module_type == "callout" and not isinstance(module.get("content"), str):
            errors.append(f"{location}.content 必须为字符串")
        if module_type == "cards":
            for item_index, item in enumerate(module.get("items", [])):
                if not isinstance(item, dict) or not isinstance(item.get("title"), str):
                    errors.append(f"{location}.items[{item_index}].title 必须为字符串")
                elif item.pop("_ambiguousImageAlt", None):
                    errors.append(f"{location}.items[{item_index}] 的 sourceImageAlt 对应多个不同图片；请使用唯一 alt")
                elif item.pop("_unresolvedImageAlt", None):
                    errors.append(f"{location}.items[{item_index}] 未找到 sourceImageAlt 对应图片")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path, help="Imported Markdown or MDX source")
    parser.add_argument("--presentation", type=Path, help="Optional Portal Presentation JSON")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    if not args.document.is_file():
        parser.error(f"Document does not exist: {args.document}")
    if args.presentation and not args.presentation.is_file():
        parser.error(f"Presentation manifest does not exist: {args.presentation}")
    try:
        presentation = load_manifest(args.presentation)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))
    resolve_source_images(args.document.read_text(encoding="utf-8"), presentation)
    errors = validate(presentation)
    payload = {"presentation": presentation, "errors": errors}
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(serialized, encoding="utf-8")
    else:
        print(serialized, end="")
    if args.validate and errors:
        for error in errors:
            print(f"error: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
