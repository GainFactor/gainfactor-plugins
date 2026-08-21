#!/usr/bin/env python3
"""Migrate the removed document portal components to the v2 composition API."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REMOVED_TAGS = (
    "Profile",
    "InfoGrid",
    "ContentPanel",
    "GroupedBoard",
    "StructuredSteps",
    "JourneyStep",
    "NodeGraph",
)


def _tag_end(source: str, start: int) -> int:
    braces = 0
    quote: str | None = None
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in "\"'`":
            quote = char
        elif char == "{":
            braces += 1
        elif char == "}":
            braces -= 1
        elif char == ">" and braces == 0:
            return index + 1
    raise ValueError(f"Unterminated JSX tag at offset {start}")


def _prop_span(attributes: str, name: str) -> tuple[int, int, str] | None:
    match = re.search(rf"(?<![\w-]){re.escape(name)}\s*=\s*", attributes)
    if not match:
        return None
    value_start = match.end()
    if value_start >= len(attributes):
        return None
    opener = attributes[value_start]
    if opener in "\"'":
        end = value_start + 1
        while end < len(attributes):
            if attributes[end] == opener and attributes[end - 1] != "\\":
                end += 1
                break
            end += 1
    elif opener == "{":
        depth = 1
        quote: str | None = None
        escaped = False
        end = value_start + 1
        while end < len(attributes) and depth:
            char = attributes[end]
            if quote:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == quote:
                    quote = None
            elif char in "\"'`":
                quote = char
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            end += 1
    else:
        found = re.search(r"\s|/", attributes[value_start:])
        end = value_start + (found.start() if found else len(attributes) - value_start)
    return match.start(), end, attributes[value_start:end]


def _expression(value: str) -> str:
    value = value.strip()
    return value[1:-1].strip() if value.startswith("{") and value.endswith("}") else value


def _remove_props(attributes: str, names: tuple[str, ...]) -> tuple[str, dict[str, str]]:
    values: dict[str, str] = {}
    spans: list[tuple[int, int]] = []
    for name in names:
        result = _prop_span(attributes, name)
        if result:
            start, end, value = result
            values[name] = value
            spans.append((start, end))
    for start, end in sorted(spans, reverse=True):
        attributes = attributes[:start] + attributes[end:]
    attributes = re.sub(r"[ \t]+\n", "\n", attributes)
    attributes = re.sub(r" {2,}", " ", attributes)
    return attributes.strip(), values


def _replace_opening_tags(source: str, name: str, build) -> str:
    cursor = 0
    while True:
        match = re.search(rf"<{name}\b", source[cursor:])
        if not match:
            return source
        start = cursor + match.start()
        end = _tag_end(source, start)
        original = source[start:end]
        replacement = build(original)
        source = source[:start] + replacement + source[end:]
        cursor = start + len(replacement)


def _migrate_panel(tag: str) -> str:
    attributes = tag[len("<ContentPanel") : -1]
    self_closing = attributes.rstrip().endswith("/")
    attributes = attributes.rstrip().removesuffix("/")
    kept, values = _remove_props(attributes, ("fields", "sections", "notice", "tags", "layout", "href"))
    children: list[str] = []
    if "tags" in values:
        tags = _expression(values["tags"])
        children.append(f'<FieldList items={{[{{ label: "标签", value: ({tags}).join(" · ") }}]}} />')
    if "fields" in values:
        children.append(f'<FieldList items={{{_expression(values["fields"])}}} />')
    if "sections" in values:
        sections = _expression(values["sections"])
        children.append(
            "{(" + sections + ").map((section) => ("
            '<section key={section.id ?? section.title}><h4>{section.title}</h4><div>{section.content}</div></section>'
            "))}"
        )
    if "notice" in values:
        notice = _expression(values["notice"])
        children.append(
            "{(() => { const notice = " + notice
            + '; return <Callout type={notice.tone === "warning" ? "warn" : notice.tone} title={notice.label}>{notice.content}</Callout>; })()}'
        )
    opening = f"<Panel{(' ' + kept) if kept else ''}>"
    body = ("\n" + "\n".join(children)) if children else ""
    return opening + body + ("\n</Panel>" if self_closing else "")


def _migrate_profile(tag: str) -> str:
    attributes = tag[len("<Profile") : -1]
    attributes = attributes.rstrip().removesuffix("/")
    kept, values = _remove_props(attributes, ("role", "summary", "badge", "tags", "highlights", "facts"))
    mapped: list[str] = []
    for old_name, new_name in (("role", "identity"), ("summary", "situation"), ("badge", "priority")):
        if old_name in values:
            mapped.append(f"{new_name}={values[old_name]}")
    traits = values.get("tags") or values.get("highlights")
    if traits:
        mapped.append(f"traits={traits}")
    if "facts" in values:
        mapped.append(f"facts={values['facts']}")
    props = " ".join(part for part in (kept, *mapped) if part)
    return f"<PersonaBrief{(' ' + props) if props else ''} />"


def _migrate_steps(tag: str) -> str:
    attributes = tag[len("<StructuredSteps") : -1].rstrip().removesuffix("/")
    _, values = _remove_props(attributes, ("items", "icon"))
    items = _expression(values["items"])
    return (
        "<Steps>\n{(" + items + ").map((item, index) => (\n"
        "  <Step key={item.id ?? index}>\n"
        "    <h3>{item.title}</h3>\n"
        "    <div>{item.content}</div>\n"
        "    {item.fields?.length ? <FieldList items={item.fields} /> : null}\n"
        "  </Step>\n"
        "))}\n</Steps>"
    )


def _migrate_board(tag: str) -> str:
    attributes = tag[len("<GroupedBoard") : -1].rstrip().removesuffix("/")
    kept, values = _remove_props(attributes, ("groups", "label"))
    groups = _expression(values["groups"])
    title = values.get("label")
    title_prop = f" label={title}" if title else ""
    return (
        f"<Board{title_prop}{(' ' + kept) if kept else ''} groups={{({groups}).map((group) => ({{\n"
        "  id: group.id,\n  title: group.title,\n  icon: group.icon,\n"
        '  tone: ({ p0: "critical", p1: "warning", p2: "info" })[group.tone] ?? "neutral",\n'
        "  description: group.description,\n"
        "  children: <div>{group.items?.map((item, index) => <article key={item.id ?? item.title ?? index}><h4>{item.title}</h4>{item.description ? <p>{item.description}</p> : null}{item.fields?.length ? <FieldList items={item.fields} /> : null}{item.tags?.length ? <p>{item.tags.join(\" · \")}</p> : null}</article>)}</div>\n"
        "}))} />"
    )


def migrate(source: str) -> str:
    source = re.sub(r"<InfoGrid\b", '<FieldList variant="grid"', source)
    source = re.sub(r"<JourneyStep\b", "<EvidenceStep", source)
    source = source.replace("</JourneyStep>", "</EvidenceStep>")
    source = _replace_opening_tags(source, "Profile", _migrate_profile)
    source = source.replace("</Profile>", "")
    source = _replace_opening_tags(source, "ContentPanel", _migrate_panel)
    source = source.replace("</ContentPanel>", "</Panel>")
    source = _replace_opening_tags(source, "StructuredSteps", _migrate_steps)
    source = _replace_opening_tags(source, "GroupedBoard", _migrate_board)
    return source


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    failed = False
    for path in args.paths:
        original = path.read_text(encoding="utf-8")
        migrated = migrate(original)
        remaining = sorted({tag for tag in REMOVED_TAGS if re.search(rf"<{tag}\b", migrated)})
        if remaining:
            raise SystemExit(f"{path}: automatic migration unavailable for {', '.join(remaining)}")
        if migrated != original:
            if args.check:
                print(f"needs migration: {path}")
                failed = True
            else:
                path.write_text(migrated, encoding="utf-8")
                print(f"migrated: {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
