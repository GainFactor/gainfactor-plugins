#!/usr/bin/env python3
"""Validate and compile a generic Portal Presentation manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CAPABILITIES_PATH = Path(__file__).resolve().parent.parent / "assets/document-review-portal/portal-capabilities.json"
CAPABILITIES = json.loads(CAPABILITIES_PATH.read_text(encoding="utf-8"))
SUPPORTED_MODULES = set(CAPABILITIES["presentationModules"])
REMOVED_COMPONENTS = CAPABILITIES.get("removedComponents", {})
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+[\"'][^)]*[\"'])?\)")
PERSONA_BRIEF_IMAGE = re.compile(r"\bimage\s*=\s*\{\{(?P<properties>.*?)\}\}", re.DOTALL)
CITATION = re.compile(r"<Citation\b[^>]*\bsource\s*=\s*([\"'])(?P<id>.*?)\1[^>]*/?>", re.DOTALL)
SOURCE = re.compile(r"<Source\b[^>]*\bid\s*=\s*([\"'])(?P<id>.*?)\1[^>]*>", re.DOTALL)
INFOGRAPHIC = re.compile(r"<Infographic\b(?P<attributes>.*?)/>", re.DOTALL)
INFOGRAPHIC_SYNTAX = re.compile(
    r'''\bsyntax\s*=\s*(?:"(?P<double>.*?)"|'(?P<single>.*?)'|\{\s*`(?P<template>.*?)`\s*\})''',
    re.DOTALL,
)
INFOGRAPHIC_FENCE = re.compile(r"^```infographic\s*$", re.MULTILINE)
SCREENSHOT = re.compile(r"<Screenshot\b(?P<attributes>.*?)/>", re.DOTALL)
FIELD_LIST = re.compile(r"<FieldList\b(?P<attributes>.*?)/>", re.DOTALL)


def jsx_string_property(properties: str, name: str) -> str | None:
    match = re.search(rf"\b{re.escape(name)}\s*:\s*([\"'])(.*?)\1", properties, re.DOTALL)
    return match.group(2).strip() if match else None


def source_images(document: str) -> tuple[dict[str, str], set[str]]:
    candidates = [(alt.strip(), target) for alt, target in IMAGE.findall(document)]
    for image in PERSONA_BRIEF_IMAGE.finditer(document):
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


def validate_document(document: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for component, replacement in REMOVED_COMPONENTS.items():
        for match in re.finditer(rf"<{re.escape(component)}\b", document):
            line = document.count("\n", 0, match.start()) + 1
            errors.append(f"第 {line} 行使用已移除组件 {component}；请改用 {replacement}")
    citation_ids = [match.group("id").strip() for match in CITATION.finditer(document)]
    source_ids = [match.group("id").strip() for match in SOURCE.finditer(document)]
    duplicates = sorted({source_id for source_id in source_ids if source_ids.count(source_id) > 1})
    missing = sorted(set(citation_ids) - set(source_ids))
    orphaned = sorted(set(source_ids) - set(citation_ids))
    if duplicates:
        errors.append(f"来源 ID 重复：{', '.join(duplicates)}")
    if missing:
        errors.append(f"引用目标不存在：{', '.join(missing)}")
    if orphaned:
        errors.append(f"存在孤立来源：{', '.join(orphaned)}")
    for field_list_index, field_list in enumerate(FIELD_LIST.finditer(document), start=1):
        long_values = [value for _, value in re.findall(r"\bvalue\s*:\s*([\"'])(.*?)\1", field_list.group("attributes"), re.DOTALL) if len(value.strip()) > 80]
        if long_values:
            warnings.append(f"FieldList[{field_list_index}] 包含超过 80 字的字段；请改为 Panel 正文或分节正文")
    infographics = list(INFOGRAPHIC.finditer(document))
    if INFOGRAPHIC_FENCE.search(document) and not infographics:
        errors.append("fenced Infographic 只会显示代码；请使用 <Infographic syntax={`...`} /> 渲染图形")
    for infographic_index, infographic in enumerate(infographics, start=1):
        if not re.match(r"<Infographic[ \t]+syntax\s*=", infographic.group(0)):
            errors.append(
                f"Infographic[{infographic_index}] syntax 必须紧跟在组件名同一行，避免 MDX 改写 DSL 缩进"
            )
        syntax_match = INFOGRAPHIC_SYNTAX.search(infographic.group("attributes"))
        if not syntax_match:
            errors.append(
                f"Infographic[{infographic_index}] syntax 必须是静态字符串；多行 DSL 使用 syntax={{`...`}}"
            )
            continue
        syntax = next(value for value in syntax_match.groupdict().values() if value is not None).strip()
        first_line = syntax.splitlines()[0] if syntax else ""
        if not re.fullmatch(r"infographic [a-z0-9]+(?:-[a-z0-9]+)*", first_line):
            errors.append(f"Infographic[{infographic_index}] 第一行必须是 infographic <template-name>")
        if re.search(r"(?:https?://|ref:(?:url|remote|search):)", syntax, re.IGNORECASE):
            errors.append(f"Infographic[{infographic_index}] 不允许远程资源")
        syntax_lines = syntax.splitlines()
        if len(syntax_lines) > 1 and syntax_lines[1] != "  data":
            errors.append(
                f"Infographic[{infographic_index}] MDX 模板字符串中的 data 必须缩进两格，以补偿 MDX 编译时的缩进移除"
            )
    for screenshot_index, screenshot in enumerate(SCREENSHOT.finditer(document), start=1):
        attributes = screenshot.group("attributes")
        if not re.search(r"\bsrc\s*=\s*([\"']).+?\1", attributes, re.DOTALL):
            errors.append(f"Screenshot[{screenshot_index}] src 必须是非空字符串")
        if not re.search(r"\bcaption\s*=\s*([\"']).+?\1", attributes, re.DOTALL):
            warnings.append(f"Screenshot[{screenshot_index}] 缺少 caption；请补充截图说明")
    return errors, warnings


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
    document = args.document.read_text(encoding="utf-8")
    resolve_source_images(document, presentation)
    document_errors, warnings = validate_document(document)
    errors = validate(presentation) + document_errors
    payload = {"presentation": presentation, "errors": errors, "warnings": warnings}
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(serialized, encoding="utf-8")
    else:
        print(serialized, end="")
    if args.validate and errors:
        for error in errors:
            print(f"error: {error}")
        return 1
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
