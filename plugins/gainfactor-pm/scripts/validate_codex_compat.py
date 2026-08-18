#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required to validate skills. Install it with `python3 -m pip install pyyaml`."
    ) from exc


REQUIRED_FRONTMATTER_KEYS = {"name", "description"}
REQUIRED_INTERFACE_KEYS = {
    "display_name",
    "short_description",
    "default_prompt",
    "icon_small",
    "icon_large",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Codex metadata for gainfactor-pm skills."
    )
    parser.add_argument(
        "--all-plugins",
        action="store_true",
        help="Validate every plugin under the repository plugins directory.",
    )
    return parser.parse_args()


def load_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")

    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError as exc:
        raise ValueError("SKILL.md frontmatter is incomplete") from exc

    data = yaml.safe_load(frontmatter)
    if not isinstance(data, dict):
        raise ValueError("SKILL.md frontmatter must parse to a mapping")

    missing = sorted(REQUIRED_FRONTMATTER_KEYS - data.keys())
    if missing:
        raise ValueError(f"SKILL.md missing frontmatter keys: {', '.join(missing)}")
    return data


def validate_openai_yaml(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if not openai_yaml.exists():
        return [f"missing {openai_yaml.relative_to(skill_dir)}"]

    data = yaml.safe_load(openai_yaml.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return ["agents/openai.yaml must parse to a mapping"]

    interface = data.get("interface")
    if not isinstance(interface, dict):
        return ["agents/openai.yaml missing interface mapping"]

    missing = sorted(REQUIRED_INTERFACE_KEYS - interface.keys())
    for key in missing:
        errors.append(f"agents/openai.yaml missing interface.{key}")

    for icon_key in ("icon_small", "icon_large"):
        rel = interface.get(icon_key)
        if not isinstance(rel, str) or not rel.strip():
            continue
        icon_path = (skill_dir / rel).resolve()
        if not icon_path.exists():
            errors.append(f"{icon_key} points to missing file: {rel}")

    return errors


def iter_skill_dirs(skills_roots: list[Path]):
    for skills_root in skills_roots:
        for path in sorted(skills_root.iterdir()):
            if path.is_dir() and (path / "SKILL.md").exists():
                yield path


def main() -> int:
    args = parse_args()
    plugin_root = Path(__file__).resolve().parents[1]
    repo_root = Path(__file__).resolve().parents[3]
    if args.all_plugins:
        skills_roots = sorted(
            path for path in (repo_root / "plugins").glob("*/skills") if path.is_dir()
        )
        scope = repo_root / "plugins"
    else:
        skills_roots = [plugin_root / "skills"]
        scope = plugin_root / "skills"

    errors: list[str] = []
    validated = 0

    for skill_dir in iter_skill_dirs(skills_roots):
        validated += 1
        skill_errors: list[str] = []
        try:
            load_frontmatter(skill_dir / "SKILL.md")
        except Exception as exc:  # pragma: no cover
            skill_errors.append(str(exc))

        skill_errors.extend(validate_openai_yaml(skill_dir))

        if skill_errors:
            rel = skill_dir.relative_to(repo_root)
            for error in skill_errors:
                errors.append(f"{rel}: {error}")

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {validated} Codex-compatible skills under {scope}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
