#!/usr/bin/env python3
"""Validate gainfactor-pm traceability metadata.

Examples:
  python3 plugins/gainfactor-pm/scripts/trace_lint.py path/to/PRD.md
  python3 plugins/gainfactor-pm/scripts/trace_lint.py --format json path/to/PRD.md
  python3 plugins/gainfactor-pm/scripts/trace_lint.py --strict path/to/PRD.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required to run trace-lint. Install it with `python3 -m pip install pyyaml`."
    ) from exc


TOOL_VERSION = "1.0.0"
SCHEMA_NAME = "gainfactor-pm-traceability"
ID_PATTERN = re.compile(r"^[A-Z_]+-[A-Z0-9_]+-\d{3}$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
MARKER_BEGIN = "<!-- TRACEABILITY-METADATA:BEGIN -->"
MARKER_END = "<!-- TRACEABILITY-METADATA:END -->"
MARKDOWN_EXTENSIONS = {".md", ".markdown"}
YAML_EXTENSIONS = {".yaml", ".yml"}

ALLOWED_ARTIFACT_TYPES = {
    "BRD",
    "USER_JOURNEY",
    "PRD",
    "API_CONTRACT",
    "HLD",
    "LLD",
    "TEST_STRATEGY",
    "TEST_SPEC",
    "RUNBOOK",
}
ALLOWED_ARTIFACT_STATUS = {"draft", "in_review", "approved", "deprecated", "archived"}
ALLOWED_ENTITY_STATUS = {"proposed", "approved", "deprecated", "replaced"}
ALLOWED_ENTITY_SCOPE = {"in", "out"}
ALLOWED_RELATION_TYPES = {"derived_from", "depends_on", "refines", "verifies", "mitigates"}
ALLOWED_RELATION_STATUS = {"active", "deprecated"}
ALLOWED_WAIVER_STATUS = {"draft", "approved", "expired", "revoked"}
ALLOWED_REQUIREMENT_CLASS = {"functional", "non_functional"}
ALLOWED_PRIORITY = {"P0", "P1", "P2", "P3"}
ALLOWED_RISK_LEVEL = {"critical", "high", "medium", "low"}
ALLOWED_TEST_CASE_LAYER = {"system_integration", "e2e", "regression", "compatibility", "non_functional"}
ALLOWED_AUTOMATION = {"must", "should", "manual_ok"}
ALLOWED_FLOW_KIND = {"user_journey", "system_flow", "state_transition"}
ALLOWED_FLOW_KIND_LLD = ALLOWED_FLOW_KIND | {"module_interaction"}
JOURNEY_ALLOWED_RELATION_TARGET_PREFIXES = ("BRD-", "REQ-", "FLOW-", "JOURNEY-")
HLD_ALLOWED_RELATION_TARGET_PREFIXES = ("REQ-", "BRD-", "JOURNEY-", "PRD-", "API-")
LLD_ALLOWED_RELATION_TARGET_PREFIXES = ("DEC-", "FLOW-", "REQ-", "BRD-", "JOURNEY-", "PRD-", "API-", "HLD-")
REQUIRED_TOP_LEVEL_KEYS = ("schema", "artifact", "entities", "relations", "waivers")
PRD_PROFILE_BUCKETS = (
    "requirements",
    "risks",
    "must_not_regress",
    "external_behaviors",
    "decisions",
    "flows",
    "test_cases",
)
COMMON_PROFILE_BUCKETS = PRD_PROFILE_BUCKETS


@dataclass
class Issue:
    severity: str
    code: str
    path: str
    message: str
    suggestion: str

    def to_json(self) -> dict[str, Any]:
        return {
            "severity": self.severity,
            "code": self.code,
            "path": self.path,
            "message": self.message,
            "suggestion": self.suggestion,
        }


@dataclass
class ArtifactReport:
    path: str
    artifact_id: str | None
    artifact_type: str | None
    profile: str | None
    issues: list[Issue]

    def counts(self) -> dict[str, int]:
        return {
            "errors": sum(1 for issue in self.issues if issue.severity == "error"),
            "warnings": sum(1 for issue in self.issues if issue.severity == "warning"),
            "infos": sum(1 for issue in self.issues if issue.severity == "info"),
        }

    def result(self, strict: bool) -> str:
        counts = self.counts()
        if counts["errors"] > 0:
            return "fail"
        if strict and counts["warnings"] > 0:
            return "fail"
        return "pass"

    def to_json(self, strict: bool) -> dict[str, Any]:
        return {
            "path": self.path,
            "artifact_id": self.artifact_id,
            "artifact_type": self.artifact_type,
            "profile": self.profile,
            "result": self.result(strict),
            "summary": self.counts(),
            "issues": [issue.to_json() for issue in self.issues],
        }


class LintContext:
    def __init__(self, path: Path):
        self.path = path
        self.issues: list[Issue] = []

    def add_issue(self, severity: str, code: str, path: str, message: str, suggestion: str) -> None:
        self.issues.append(Issue(severity, code, path, message, suggestion))


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trace-lint",
        description="Validate gainfactor-pm traceability metadata.",
        epilog=(
            "Examples:\n"
            "  python3 plugins/gainfactor-pm/scripts/trace_lint.py docs/PRD-checkout.md\n"
            "  python3 plugins/gainfactor-pm/scripts/trace_lint.py --format json docs/PRD-checkout.md\n"
            "  python3 plugins/gainfactor-pm/scripts/trace_lint.py --strict docs/PRD-checkout.md"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="+", help="One or more Markdown/YAML files to validate")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )
    parser.add_argument(
        "--profile",
        help="Force a specific profile instead of relying on schema.profile",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as blocking failures",
    )
    return parser.parse_args(argv)


def detect_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in MARKDOWN_EXTENSIONS:
        return "markdown"
    if suffix in YAML_EXTENSIONS:
        return "yaml"
    return "markdown"


def parse_yaml_text(ctx: LintContext, yaml_text: str) -> dict[str, Any] | None:
    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        ctx.add_issue(
            "error",
            "TRACE003",
            "metadata",
            f"YAML 解析失败：{exc}",
            "修正 YAML 语法，确保 metadata block 可被标准 YAML 解析器读取。",
        )
        return None

    if not isinstance(data, dict):
        ctx.add_issue(
            "error",
            "TRACE101",
            "metadata",
            "顶层 metadata 必须解析为 object/mapping。",
            "将 metadata 顶层改为包含 schema/artifact/entities/relations/waivers 的映射对象。",
        )
        return None

    return data


def extract_markdown_metadata(ctx: LintContext, text: str) -> dict[str, Any] | None:
    begin_count = text.count(MARKER_BEGIN)
    end_count = text.count(MARKER_END)
    if begin_count == 0 and end_count == 0:
        ctx.add_issue(
            "error",
            "TRACE001",
            "metadata",
            "TRACEABILITY metadata block 缺失。",
            "在文档中加入 TRACEABILITY-METADATA:BEGIN/END 包裹的 YAML block。",
        )
        return None
    if begin_count != 1 or end_count != 1:
        ctx.add_issue(
            "error",
            "TRACE002",
            "metadata",
            "TRACEABILITY metadata 边界标记不合法，必须且只能各出现一次。",
            "确保文档中只有一组 TRACEABILITY-METADATA:BEGIN/END 标记，且成对出现。",
        )
        return None

    start = text.index(MARKER_BEGIN) + len(MARKER_BEGIN)
    end = text.index(MARKER_END)
    block = text[start:end].strip()
    lines = block.splitlines()
    if len(lines) < 2 or lines[0].strip() != "```yaml" or lines[-1].strip() != "```":
        ctx.add_issue(
            "error",
            "TRACE002",
            "metadata",
            "TRACEABILITY metadata block 必须只包含一个 ```yaml fenced code block。",
            "将标记之间的内容整理为单个 ```yaml ... ``` block，不要混入其他文本。",
        )
        return None
    if any(line.strip().startswith("```") for line in lines[1:-1]):
        ctx.add_issue(
            "error",
            "TRACE002",
            "metadata",
            "TRACEABILITY metadata block 里出现了额外的 fenced code block。",
            "删除 metadata block 内部的多余 fenced code block，只保留单个 YAML block。",
        )
        return None

    return parse_yaml_text(ctx, "\n".join(lines[1:-1]))


def extract_metadata(path: Path, ctx: LintContext) -> dict[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    if detect_kind(path) == "yaml":
        return parse_yaml_text(ctx, text)
    return extract_markdown_metadata(ctx, text)


def is_valid_id(value: Any) -> bool:
    return isinstance(value, str) and bool(ID_PATTERN.fullmatch(value))


def is_valid_date(value: Any) -> bool:
    if isinstance(value, date):
        return True
    if not isinstance(value, str) or not DATE_PATTERN.fullmatch(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def add_missing_field_issue(ctx: LintContext, path: str, code: str, field: str, target: str) -> None:
    ctx.add_issue(
        "error",
        code,
        f"{path}.{field}" if path else field,
        f"{target} 缺少必填字段 `{field}`。",
        f"为 {target} 补齐 `{field}` 字段。",
    )


def validate_required_mapping(
    ctx: LintContext,
    data: Any,
    path: str,
    required_keys: tuple[str, ...],
    code: str,
    target: str,
) -> dict[str, Any] | None:
    if not isinstance(data, dict):
        ctx.add_issue(
            "error",
            code,
            path,
            f"{target} 必须是 mapping。",
            f"将 {target} 改为对象映射，并补齐必填字段。",
        )
        return None
    for key in required_keys:
        if key not in data:
            add_missing_field_issue(ctx, path, code, key, target)
    return data


def validate_schema(ctx: LintContext, schema: Any, forced_profile: str | None) -> str | None:
    schema = validate_required_mapping(ctx, schema, "schema", ("name", "version", "profile"), "TRACE101", "schema")
    if schema is None:
        return forced_profile

    name = schema.get("name")
    if name != SCHEMA_NAME:
        ctx.add_issue(
            "error",
            "TRACE102",
            "schema.name",
            f"schema.name 必须为 `{SCHEMA_NAME}`，当前为 `{name}`。",
            f"将 schema.name 修改为 `{SCHEMA_NAME}`。",
        )

    version = schema.get("version")
    if not is_non_empty_string(version) or not SEMVER_PATTERN.fullmatch(version):
        ctx.add_issue(
            "warning",
            "TRACE104",
            "schema.version",
            "schema.version 建议使用 `x.y.z` 形式的 semver 版本。",
            "将 schema.version 调整为如 `1.0.0` 的格式。",
        )

    declared_profile = schema.get("profile") if isinstance(schema.get("profile"), str) else None
    if forced_profile and declared_profile and forced_profile != declared_profile:
        ctx.add_issue(
            "error",
            "TRACE601",
            "schema.profile",
            f"文档声明的 profile 为 `{declared_profile}`，与命令行强制 profile `{forced_profile}` 不一致。",
            "统一命令行 profile 与文档内 schema.profile。",
        )
        return forced_profile
    return forced_profile or declared_profile


def validate_artifact(ctx: LintContext, artifact: Any) -> tuple[str | None, str | None, set[str]]:
    artifact = validate_required_mapping(
        ctx,
        artifact,
        "artifact",
        ("id", "type", "title", "status", "created_at", "updated_at"),
        "TRACE201",
        "artifact",
    )
    if artifact is None:
        return None, None, set()

    artifact_id = artifact.get("id") if isinstance(artifact.get("id"), str) else None
    artifact_type = artifact.get("type") if isinstance(artifact.get("type"), str) else None
    source_documents: set[str] = set()

    if artifact_id is None or not is_valid_id(artifact_id):
        ctx.add_issue(
            "error",
            "TRACE201",
            "artifact.id",
            "artifact.id 缺失或不符合 ID 规则。",
            "使用如 `PRD-CHECKOUT-001` 的稳定文档 ID。",
        )

    if artifact_type not in ALLOWED_ARTIFACT_TYPES:
        ctx.add_issue(
            "error",
            "TRACE202",
            "artifact.type",
            f"artifact.type 非法：`{artifact_type}`。",
            "将 artifact.type 设置为允许枚举之一。",
        )

    if not is_non_empty_string(artifact.get("title")):
        ctx.add_issue(
            "error",
            "TRACE201",
            "artifact.title",
            "artifact.title 缺失或为空。",
            "填写非空的 artifact.title。",
        )

    if artifact.get("status") not in ALLOWED_ARTIFACT_STATUS:
        ctx.add_issue(
            "error",
            "TRACE201",
            "artifact.status",
            f"artifact.status 非法：`{artifact.get('status')}`。",
            "将 artifact.status 设置为 draft/in_review/approved/deprecated/archived 之一。",
        )

    for key in ("created_at", "updated_at"):
        if not is_valid_date(artifact.get(key)):
            ctx.add_issue(
                "error",
                "TRACE203",
                f"artifact.{key}",
                f"artifact.{key} 必须为合法的 YYYY-MM-DD 日期。",
                f"将 artifact.{key} 调整为合法日期，例如 `2026-03-08`。",
            )

    raw_sources = artifact.get("source_documents", [])
    if raw_sources is None:
        raw_sources = []
    if not isinstance(raw_sources, list) or not all(isinstance(item, str) for item in raw_sources):
        ctx.add_issue(
            "error",
            "TRACE201",
            "artifact.source_documents",
            "artifact.source_documents 必须是字符串数组。",
            "将 artifact.source_documents 改为文档 ID 字符串数组。",
        )
    else:
        source_documents = set(raw_sources)

    return artifact_id, artifact_type, source_documents


def validate_source_refs(ctx: LintContext, entity: dict[str, Any], entity_path: str, entity_id: str, source_documents: set[str]) -> None:
    source_refs = entity.get("source_refs")
    if source_refs is None:
        ctx.add_issue(
            "warning",
            "TRACE303",
            f"{entity_path}.source_refs",
            f"实体 {entity_id} 未声明 source_refs。",
            "为实体补充来源文档、章节或定位信息。",
        )
        return

    if not isinstance(source_refs, list):
        ctx.add_issue(
            "error",
            "TRACE302",
            f"{entity_path}.source_refs",
            f"实体 {entity_id} 的 source_refs 必须是对象数组。",
            "将 source_refs 改为对象数组，并至少包含 artifact_id。",
        )
        return

    for index, ref in enumerate(source_refs):
        ref_path = f"{entity_path}.source_refs[{index}]"
        if not isinstance(ref, dict):
            ctx.add_issue(
                "error",
                "TRACE302",
                ref_path,
                f"实体 {entity_id} 的 source_refs[{index}] 必须是对象。",
                "将 source_refs 中的每一项改为对象，并补齐 artifact_id。",
            )
            continue
        artifact_id = ref.get("artifact_id")
        if not is_non_empty_string(artifact_id):
            add_missing_field_issue(ctx, ref_path, "TRACE302", "artifact_id", f"{entity_id} 的 source_ref")
            continue
        if source_documents and artifact_id not in source_documents:
            ctx.add_issue(
                "warning",
                "TRACE303",
                f"{ref_path}.artifact_id",
                f"实体 {entity_id} 的 source_ref 指向 `{artifact_id}`，但它不在 artifact.source_documents 中。",
                "将该 artifact_id 加入 artifact.source_documents，或修正 source_ref 指向。",
            )


def validate_entities(
    ctx: LintContext,
    entities: Any,
    profile: str | None,
    source_documents: set[str],
) -> tuple[set[str], list[dict[str, Any]]]:
    entities = validate_required_mapping(ctx, entities, "entities", (), "TRACE101", "entities")
    if entities is None:
        return set(), []

    if profile == "prd-profile-v1":
        for bucket in PRD_PROFILE_BUCKETS:
            if bucket not in entities:
                add_missing_field_issue(ctx, "entities", "TRACE602", bucket, "prd-profile-v1 entities")

    entity_ids: set[str] = set()
    requirements: list[dict[str, Any]] = []

    for bucket_name, bucket in entities.items():
        bucket_path = f"entities.{bucket_name}"
        if not isinstance(bucket, list):
            ctx.add_issue(
                "error",
                "TRACE302",
                bucket_path,
                f"{bucket_path} 必须是数组。",
                f"将 {bucket_path} 改为数组；没有内容时使用空数组。",
            )
            continue

        for index, entity in enumerate(bucket):
            entity_path = f"{bucket_path}[{index}]"
            if not isinstance(entity, dict):
                ctx.add_issue(
                    "error",
                    "TRACE302",
                    entity_path,
                    f"{entity_path} 必须是对象。",
                    "将该实体改为对象，并补齐必填字段。",
                )
                continue

            entity_id = entity.get("id")
            if not is_valid_id(entity_id):
                ctx.add_issue(
                    "error",
                    "TRACE302",
                    f"{entity_path}.id",
                    f"{entity_path} 的 id 缺失或不符合 ID 规则。",
                    "为实体分配稳定 ID，例如 `REQ-CHECKOUT-001`。",
                )
            else:
                if entity_id in entity_ids:
                    ctx.add_issue(
                        "error",
                        "TRACE301",
                        f"{entity_path}.id",
                        f"实体 ID 重复：`{entity_id}`。",
                        "确保同一文档中的实体 ID 唯一。",
                    )
                entity_ids.add(entity_id)

            for field in ("title", "statement", "status", "scope"):
                if field not in entity:
                    add_missing_field_issue(ctx, entity_path, "TRACE302", field, f"实体 {entity_id or entity_path}")

            if entity.get("status") is not None and entity.get("status") not in ALLOWED_ENTITY_STATUS:
                ctx.add_issue(
                    "error",
                    "TRACE302",
                    f"{entity_path}.status",
                    f"实体 {entity_id or entity_path} 的 status 非法：`{entity.get('status')}`。",
                    "将 status 设置为 proposed/approved/deprecated/replaced 之一。",
                )

            if entity.get("scope") is not None and entity.get("scope") not in ALLOWED_ENTITY_SCOPE:
                ctx.add_issue(
                    "error",
                    "TRACE302",
                    f"{entity_path}.scope",
                    f"实体 {entity_id or entity_path} 的 scope 非法：`{entity.get('scope')}`。",
                    "将 scope 设置为 `in` 或 `out`。",
                )

            if entity_id:
                validate_source_refs(ctx, entity, entity_path, entity_id, source_documents)

            if bucket_name == "requirements":
                requirements.append(entity)

    return entity_ids, requirements


def validate_prd_profile(
    ctx: LintContext,
    artifact_type: str | None,
    entities: dict[str, Any] | None,
    requirements: list[dict[str, Any]],
) -> None:
    if artifact_type != "PRD":
        ctx.add_issue(
            "error",
            "TRACE601",
            "artifact.type",
            f"`prd-profile-v1` 要求 artifact.type = `PRD`，当前为 `{artifact_type}`。",
            "将 artifact.type 调整为 `PRD`。",
        )

    if not entities:
        return

    if "requirements" not in entities or not isinstance(entities.get("requirements"), list) or len(entities["requirements"]) == 0:
        ctx.add_issue(
            "error",
            "TRACE602",
            "entities.requirements",
            "`prd-profile-v1` 要求至少声明 1 条 requirement。",
            "补充至少 1 条 requirement 到 entities.requirements。",
        )
        return

    for index, requirement in enumerate(requirements):
        req_path = f"entities.requirements[{index}]"
        req_id = requirement.get("id", req_path)
        for field in ("id", "class", "title", "statement", "priority", "status", "scope", "acceptance_criteria"):
            if field not in requirement:
                add_missing_field_issue(ctx, req_path, "TRACE602", field, f"Requirement {req_id}")

        if requirement.get("class") is not None and requirement.get("class") not in ALLOWED_REQUIREMENT_CLASS:
            ctx.add_issue(
                "error",
                "TRACE602",
                f"{req_path}.class",
                f"Requirement {req_id} 的 class 非法：`{requirement.get('class')}`。",
                "将 class 设置为 functional 或 non_functional。",
            )

        if requirement.get("priority") is not None and requirement.get("priority") not in ALLOWED_PRIORITY:
            ctx.add_issue(
                "error",
                "TRACE602",
                f"{req_path}.priority",
                f"Requirement {req_id} 的 priority 非法：`{requirement.get('priority')}`。",
                "将 priority 设置为 P0/P1/P2/P3 之一。",
            )

        acceptance_criteria = requirement.get("acceptance_criteria")
        if acceptance_criteria is None:
            continue
        if (
            not isinstance(acceptance_criteria, list)
            or len(acceptance_criteria) == 0
            or not all(is_non_empty_string(item) for item in acceptance_criteria)
        ):
            ctx.add_issue(
                "error",
                "TRACE602",
                f"{req_path}.acceptance_criteria",
                f"Requirement {req_id} 的 acceptance_criteria 必须是非空字符串数组。",
                "为该 requirement 补齐至少 1 条可测试的 acceptance criteria。",
            )


def validate_profile_buckets(ctx: LintContext, entities: dict[str, Any] | None, code: str, profile_name: str) -> dict[str, Any] | None:
    if not entities:
        return None
    for bucket in COMMON_PROFILE_BUCKETS:
        if bucket not in entities:
            add_missing_field_issue(ctx, "entities", code, bucket, f"{profile_name} entities")
    return entities


def validate_test_strategy_profile(
    ctx: LintContext,
    artifact_type: str | None,
    entities: dict[str, Any] | None,
) -> None:
    if artifact_type != "TEST_STRATEGY":
        ctx.add_issue(
            "error",
            "TRACE603",
            "artifact.type",
            f"`test-strategy-profile-v1` 要求 artifact.type = `TEST_STRATEGY`，当前为 `{artifact_type}`。",
            "将 artifact.type 调整为 `TEST_STRATEGY`。",
        )
    entities = validate_profile_buckets(ctx, entities, "TRACE603", "test-strategy-profile-v1")
    if not entities:
        return

    modeled_count = 0

    for index, risk in enumerate(entities.get("risks", [])):
        risk_path = f"entities.risks[{index}]"
        risk_id = risk.get("id", risk_path) if isinstance(risk, dict) else risk_path
        if not isinstance(risk, dict):
            continue
        modeled_count += 1
        for field in ("id", "title", "statement", "status", "scope", "level"):
            if field not in risk:
                add_missing_field_issue(ctx, risk_path, "TRACE603", field, f"Risk {risk_id}")
        if risk.get("level") is not None and risk.get("level") not in ALLOWED_RISK_LEVEL:
            ctx.add_issue(
                "error",
                "TRACE603",
                f"{risk_path}.level",
                f"Risk {risk_id} 的 level 非法：`{risk.get('level')}`。",
                "将 level 设置为 critical/high/medium/low 之一。",
            )

    for index, item in enumerate(entities.get("must_not_regress", [])):
        item_path = f"entities.must_not_regress[{index}]"
        item_id = item.get("id", item_path) if isinstance(item, dict) else item_path
        if not isinstance(item, dict):
            continue
        modeled_count += 1
        for field in ("id", "title", "statement", "status", "scope", "priority"):
            if field not in item:
                add_missing_field_issue(ctx, item_path, "TRACE603", field, f"Must-not-regress {item_id}")
        if item.get("priority") is not None and item.get("priority") not in ALLOWED_PRIORITY:
            ctx.add_issue(
                "error",
                "TRACE603",
                f"{item_path}.priority",
                f"Must-not-regress {item_id} 的 priority 非法：`{item.get('priority')}`。",
                "将 priority 设置为 P0/P1/P2/P3 之一。",
            )

    for index, behavior in enumerate(entities.get("external_behaviors", [])):
        behavior_path = f"entities.external_behaviors[{index}]"
        behavior_id = behavior.get("id", behavior_path) if isinstance(behavior, dict) else behavior_path
        if not isinstance(behavior, dict):
            continue
        modeled_count += 1
        for field in ("id", "title", "statement", "status", "scope"):
            if field not in behavior:
                add_missing_field_issue(ctx, behavior_path, "TRACE603", field, f"External behavior {behavior_id}")

    if modeled_count == 0:
        ctx.add_issue(
            "error",
            "TRACE603",
            "entities",
            "`test-strategy-profile-v1` 至少应建模 1 条 risk、must-not-regress 或 external behavior。",
            "至少在 risks / must_not_regress / external_behaviors 中填写一条实体。",
        )


def validate_test_spec_profile(
    ctx: LintContext,
    artifact_type: str | None,
    entities: dict[str, Any] | None,
    relations: Any,
) -> None:
    if artifact_type != "TEST_SPEC":
        ctx.add_issue(
            "error",
            "TRACE604",
            "artifact.type",
            f"`test-spec-profile-v1` 要求 artifact.type = `TEST_SPEC`，当前为 `{artifact_type}`。",
            "将 artifact.type 调整为 `TEST_SPEC`。",
        )
    entities = validate_profile_buckets(ctx, entities, "TRACE604", "test-spec-profile-v1")
    if not entities:
        return

    test_cases = entities.get("test_cases")
    if not isinstance(test_cases, list) or len(test_cases) == 0:
        ctx.add_issue(
            "error",
            "TRACE604",
            "entities.test_cases",
            "`test-spec-profile-v1` 要求至少声明 1 条 test case。",
            "补充至少 1 条 `CASE-*` 到 entities.test_cases。",
        )
        return

    outgoing_relations: dict[str, list[dict[str, Any]]] = {}
    if isinstance(relations, list):
        for relation in relations:
            if isinstance(relation, dict) and isinstance(relation.get("from"), str):
                outgoing_relations.setdefault(relation["from"], []).append(relation)

    for index, case in enumerate(test_cases):
        case_path = f"entities.test_cases[{index}]"
        case_id = case.get("id", case_path) if isinstance(case, dict) else case_path
        if not isinstance(case, dict):
            continue
        for field in ("id", "title", "statement", "status", "scope", "layer", "priority"):
            if field not in case:
                add_missing_field_issue(ctx, case_path, "TRACE604", field, f"Test case {case_id}")
        if case.get("layer") is not None and case.get("layer") not in ALLOWED_TEST_CASE_LAYER:
            ctx.add_issue(
                "error",
                "TRACE604",
                f"{case_path}.layer",
                f"Test case {case_id} 的 layer 非法：`{case.get('layer')}`。",
                "将 layer 设置为 system_integration/e2e/regression/compatibility/non_functional 之一。",
            )
        if case.get("priority") is not None and case.get("priority") not in ALLOWED_PRIORITY:
            ctx.add_issue(
                "error",
                "TRACE604",
                f"{case_path}.priority",
                f"Test case {case_id} 的 priority 非法：`{case.get('priority')}`。",
                "将 priority 设置为 P0/P1/P2/P3 之一。",
            )
        if case.get("automation") is not None and case.get("automation") not in ALLOWED_AUTOMATION:
            ctx.add_issue(
                "warning",
                "TRACE605",
                f"{case_path}.automation",
                f"Test case {case_id} 的 automation 非标准：`{case.get('automation')}`。",
                "建议使用 must/should/manual_ok 之一。",
            )

        case_relations = outgoing_relations.get(case.get("id"), [])
        if not any(relation.get("type") in {"verifies", "mitigates"} for relation in case_relations):
            ctx.add_issue(
                "error",
                "TRACE604",
                case_path,
                f"Test case {case_id} 缺少 outgoing verifies/mitigates relation，无法形成追溯闭环。",
                "至少为该 case 建立 1 条 verifies 或 mitigates relation。",
            )


def validate_journey_profile(
    ctx: LintContext,
    artifact_id: str | None,
    artifact_type: str | None,
    source_documents: set[str],
    entities: dict[str, Any] | None,
    relations: Any,
) -> None:
    if artifact_type != "USER_JOURNEY":
        ctx.add_issue(
            "error",
            "TRACE608",
            "artifact.type",
            f"`journey-profile-v1` 要求 artifact.type = `USER_JOURNEY`，当前为 `{artifact_type}`。",
            "将 artifact.type 调整为 `USER_JOURNEY`。",
        )
    if not isinstance(artifact_id, str) or not artifact_id.startswith("JOURNEY-"):
        ctx.add_issue(
            "error",
            "TRACE608",
            "artifact.id",
            f"`journey-profile-v1` 要求 artifact.id 使用 `JOURNEY-` 前缀，当前为 `{artifact_id}`。",
            "将 artifact.id 调整为如 `JOURNEY-CHECKOUT-001` 的稳定文档 ID。",
        )
    if not source_documents:
        ctx.add_issue(
            "error",
            "TRACE608",
            "artifact.source_documents",
            "`journey-profile-v1` 要求至少声明 1 个上游 source document。",
            "为 artifact.source_documents 补充当前使用的 BRD artifact ID。",
        )
    elif not any(doc.startswith("BRD-") for doc in source_documents):
        ctx.add_issue(
            "error",
            "TRACE608",
            "artifact.source_documents",
            "`journey-profile-v1` 要求 artifact.source_documents 至少包含 1 个 `BRD-*` baseline ID。",
            "补充当前 BRD 基线的稳定 artifact ID，例如 `BRD-CHECKOUT-001`。",
        )

    entities = validate_profile_buckets(ctx, entities, "TRACE608", "journey-profile-v1")
    if not entities:
        return

    flows = entities.get("flows")
    if not isinstance(flows, list) or len(flows) == 0:
        ctx.add_issue(
            "error",
            "TRACE608",
            "entities.flows",
            "`journey-profile-v1` 要求至少声明 1 条 `FLOW-*`，用于建模 Journey 基线。",
            "在 entities.flows 中补充至少 1 条 `kind=user_journey` 的 flow。",
        )
        return

    outgoing_relations: dict[str, list[dict[str, Any]]] = {}
    if isinstance(relations, list):
        for relation in relations:
            if isinstance(relation, dict) and isinstance(relation.get("from"), str):
                outgoing_relations.setdefault(relation["from"], []).append(relation)

    for index, flow in enumerate(flows):
        flow_path = f"entities.flows[{index}]"
        flow_id = flow.get("id", flow_path) if isinstance(flow, dict) else flow_path
        if not isinstance(flow, dict):
            continue
        for field in ("id", "title", "statement", "status", "scope", "kind", "priority"):
            if field not in flow:
                add_missing_field_issue(ctx, flow_path, "TRACE608", field, f"Journey flow {flow_id}")
        if flow.get("kind") is not None and flow.get("kind") != "user_journey":
            ctx.add_issue(
                "error",
                "TRACE608",
                f"{flow_path}.kind",
                f"Journey flow {flow_id} 的 kind 必须为 `user_journey`，当前为 `{flow.get('kind')}`。",
                "将 kind 调整为 `user_journey`。",
            )
        if flow.get("priority") is not None and flow.get("priority") not in ALLOWED_PRIORITY:
            ctx.add_issue(
                "error",
                "TRACE608",
                f"{flow_path}.priority",
                f"Journey flow {flow_id} 的 priority 非法：`{flow.get('priority')}`。",
                "将 priority 设置为 P0/P1/P2/P3 之一。",
            )

        flow_relations = outgoing_relations.get(flow.get("id"), [])
        valid_relations = [
            relation for relation in flow_relations
            if relation.get("type") in {"derived_from", "refines", "depends_on"}
        ]
        if not valid_relations:
            ctx.add_issue(
                "error",
                "TRACE608",
                flow_path,
                f"Journey flow {flow_id} 缺少 outgoing derived_from/refines/depends_on relation。",
                "至少为该 Journey flow 建立 1 条 relation，指向 BRD baseline、上游 REQ-* 或相关 FLOW-*。",
            )
            continue
        for relation in valid_relations:
            target = relation.get("to", "")
            if isinstance(target, str) and target in source_documents:
                continue
            if isinstance(target, str) and target.startswith("FLOW-"):
                continue
            if isinstance(target, str) and any(target.startswith(prefix) for prefix in JOURNEY_ALLOWED_RELATION_TARGET_PREFIXES):
                continue
            ctx.add_issue(
                "error",
                "TRACE608",
                flow_path,
                f"Journey flow {flow_id} 的 relation target `{target}` 不是预期的上游对象。",
                "Journey flow 的 relation target 应指向 BRD-* / REQ-* / FLOW-* / JOURNEY-* 或 artifact.source_documents 中已声明的 baseline。",
            )


def validate_hld_profile(
    ctx: LintContext,
    artifact_type: str | None,
    entities: dict[str, Any] | None,
    relations: Any,
) -> None:
    if artifact_type != "HLD":
        ctx.add_issue(
            "error",
            "TRACE606",
            "artifact.type",
            f"`hld-profile-v1` 要求 artifact.type = `HLD`，当前为 `{artifact_type}`。",
            "将 artifact.type 调整为 `HLD`。",
        )
    entities = validate_profile_buckets(ctx, entities, "TRACE606", "hld-profile-v1")
    if not entities:
        return

    outgoing_relations: dict[str, list[dict[str, Any]]] = {}
    if isinstance(relations, list):
        for relation in relations:
            if isinstance(relation, dict) and isinstance(relation.get("from"), str):
                outgoing_relations.setdefault(relation["from"], []).append(relation)

    modeled_count = 0

    for index, decision in enumerate(entities.get("decisions", [])):
        dec_path = f"entities.decisions[{index}]"
        dec_id = decision.get("id", dec_path) if isinstance(decision, dict) else dec_path
        if not isinstance(decision, dict):
            continue
        modeled_count += 1
        for field in ("id", "title", "statement", "status", "scope", "decision", "rationale"):
            if field not in decision:
                add_missing_field_issue(ctx, dec_path, "TRACE606", field, f"Decision {dec_id}")
        dec_relations = outgoing_relations.get(decision.get("id"), [])
        valid_dec_relations = [
            r for r in dec_relations
            if r.get("type") in {"refines", "derived_from"}
        ]
        if not valid_dec_relations:
            ctx.add_issue(
                "error",
                "TRACE606",
                dec_path,
                f"Decision {dec_id} 缺少 outgoing refines/derived_from relation，无法追溯到上游需求。",
                f"至少为该 decision 建立 1 条 refines 或 derived_from relation 指向 REQ-* 或上游 artifact ID。",
            )
        for r in valid_dec_relations:
            target = r.get("to", "")
            if isinstance(target, str) and not any(target.startswith(p) for p in HLD_ALLOWED_RELATION_TARGET_PREFIXES):
                ctx.add_issue(
                    "error",
                    "TRACE606",
                    dec_path,
                    f"Decision {dec_id} 的 relation target `{target}` 不是预期的上游对象（预期 REQ-* 或上游 artifact ID）。",
                    "HLD 的 refines/derived_from 应指向 REQ-* 或上游 artifact（PRD-*/API-*/BRD-* 等）。",
                )

    for index, flow in enumerate(entities.get("flows", [])):
        flow_path = f"entities.flows[{index}]"
        flow_id = flow.get("id", flow_path) if isinstance(flow, dict) else flow_path
        if not isinstance(flow, dict):
            continue
        modeled_count += 1
        for field in ("id", "title", "statement", "status", "scope", "kind"):
            if field not in flow:
                add_missing_field_issue(ctx, flow_path, "TRACE606", field, f"Flow {flow_id}")
        if flow.get("kind") is not None and flow.get("kind") not in ALLOWED_FLOW_KIND:
            ctx.add_issue(
                "error",
                "TRACE606",
                f"{flow_path}.kind",
                f"Flow {flow_id} 的 kind 非法：`{flow.get('kind')}`。",
                "将 kind 设置为 user_journey/system_flow/state_transition 之一。",
            )
        flow_relations = outgoing_relations.get(flow.get("id"), [])
        valid_flow_relations = [
            r for r in flow_relations
            if r.get("type") in {"refines", "derived_from"}
        ]
        if not valid_flow_relations:
            ctx.add_issue(
                "error",
                "TRACE606",
                flow_path,
                f"Flow {flow_id} 缺少 outgoing refines/derived_from relation，无法追溯到上游需求。",
                f"至少为该 flow 建立 1 条 refines 或 derived_from relation 指向 REQ-* 或上游 artifact ID。",
            )
        for r in valid_flow_relations:
            target = r.get("to", "")
            if isinstance(target, str) and not any(target.startswith(p) for p in HLD_ALLOWED_RELATION_TARGET_PREFIXES):
                ctx.add_issue(
                    "error",
                    "TRACE606",
                    flow_path,
                    f"Flow {flow_id} 的 relation target `{target}` 不是预期的上游对象。",
                    "HLD 的 refines/derived_from 应指向 REQ-* 或上游 artifact（PRD-*/API-*/BRD-* 等）。",
                )

    if modeled_count == 0:
        ctx.add_issue(
            "error",
            "TRACE606",
            "entities",
            "`hld-profile-v1` 至少应建模 1 条 decision 或 flow。",
            "至少在 decisions / flows 中填写一条实体。",
        )


def validate_lld_profile(
    ctx: LintContext,
    artifact_type: str | None,
    entities: dict[str, Any] | None,
    relations: Any,
) -> None:
    if artifact_type != "LLD":
        ctx.add_issue(
            "error",
            "TRACE607",
            "artifact.type",
            f"`lld-profile-v1` 要求 artifact.type = `LLD`，当前为 `{artifact_type}`。",
            "将 artifact.type 调整为 `LLD`。",
        )
    entities = validate_profile_buckets(ctx, entities, "TRACE607", "lld-profile-v1")
    if not entities:
        return

    outgoing_relations: dict[str, list[dict[str, Any]]] = {}
    if isinstance(relations, list):
        for relation in relations:
            if isinstance(relation, dict) and isinstance(relation.get("from"), str):
                outgoing_relations.setdefault(relation["from"], []).append(relation)

    modeled_count = 0

    for index, decision in enumerate(entities.get("decisions", [])):
        dec_path = f"entities.decisions[{index}]"
        dec_id = decision.get("id", dec_path) if isinstance(decision, dict) else dec_path
        if not isinstance(decision, dict):
            continue
        modeled_count += 1
        for field in ("id", "title", "statement", "status", "scope", "decision", "rationale"):
            if field not in decision:
                add_missing_field_issue(ctx, dec_path, "TRACE607", field, f"Decision {dec_id}")
        dec_relations = outgoing_relations.get(decision.get("id"), [])
        valid_dec_relations = [
            r for r in dec_relations
            if r.get("type") in {"refines", "derived_from"}
        ]
        if not valid_dec_relations:
            ctx.add_issue(
                "error",
                "TRACE607",
                dec_path,
                f"Decision {dec_id} 缺少 outgoing refines/derived_from relation。",
                f"至少为该 decision 建立 1 条 refines 或 derived_from relation 指向 DEC-*/FLOW-*/REQ-* 或上游 artifact ID。",
            )
        for r in valid_dec_relations:
            target = r.get("to", "")
            if isinstance(target, str) and not any(target.startswith(p) for p in LLD_ALLOWED_RELATION_TARGET_PREFIXES):
                ctx.add_issue(
                    "error",
                    "TRACE607",
                    dec_path,
                    f"Decision {dec_id} 的 relation target `{target}` 不是预期的上游对象。",
                    "LLD 的 refines/derived_from 应指向 DEC-*/FLOW-*/REQ-* 或上游 artifact（HLD-*/PRD-* 等）。",
                )

    for index, flow in enumerate(entities.get("flows", [])):
        flow_path = f"entities.flows[{index}]"
        flow_id = flow.get("id", flow_path) if isinstance(flow, dict) else flow_path
        if not isinstance(flow, dict):
            continue
        modeled_count += 1
        for field in ("id", "title", "statement", "status", "scope", "kind"):
            if field not in flow:
                add_missing_field_issue(ctx, flow_path, "TRACE607", field, f"Flow {flow_id}")
        if flow.get("kind") is not None and flow.get("kind") not in ALLOWED_FLOW_KIND_LLD:
            ctx.add_issue(
                "error",
                "TRACE607",
                f"{flow_path}.kind",
                f"Flow {flow_id} 的 kind 非法：`{flow.get('kind')}`。",
                "将 kind 设置为 user_journey/system_flow/state_transition/module_interaction 之一。",
            )
        flow_relations = outgoing_relations.get(flow.get("id"), [])
        valid_flow_relations = [
            r for r in flow_relations
            if r.get("type") in {"refines", "derived_from"}
        ]
        if not valid_flow_relations:
            ctx.add_issue(
                "error",
                "TRACE607",
                flow_path,
                f"Flow {flow_id} 缺少 outgoing refines/derived_from relation。",
                f"至少为该 flow 建立 1 条 refines 或 derived_from relation 指向 DEC-*/FLOW-*/REQ-* 或上游 artifact ID。",
            )
        for r in valid_flow_relations:
            target = r.get("to", "")
            if isinstance(target, str) and not any(target.startswith(p) for p in LLD_ALLOWED_RELATION_TARGET_PREFIXES):
                ctx.add_issue(
                    "error",
                    "TRACE607",
                    flow_path,
                    f"Flow {flow_id} 的 relation target `{target}` 不是预期的上游对象。",
                    "LLD 的 refines/derived_from 应指向 DEC-*/FLOW-*/REQ-* 或上游 artifact（HLD-*/PRD-* 等）。",
                )

    if modeled_count == 0:
        ctx.add_issue(
            "error",
            "TRACE607",
            "entities",
            "`lld-profile-v1` 至少应建模 1 条 decision 或 flow。",
            "至少在 decisions / flows 中填写一条实体。",
        )


def validate_relations(
    ctx: LintContext,
    relations: Any,
    known_ids: set[str],
    source_documents: set[str],
) -> None:
    if not isinstance(relations, list):
        ctx.add_issue(
            "error",
            "TRACE401",
            "relations",
            "relations 必须是数组。",
            "将 relations 改为数组；没有关系时使用空数组。",
        )
        return

    relation_ids: set[str] = set()
    for index, relation in enumerate(relations):
        relation_path = f"relations[{index}]"
        if not isinstance(relation, dict):
            ctx.add_issue(
                "error",
                "TRACE401",
                relation_path,
                f"{relation_path} 必须是对象。",
                "将 relation 改为对象，并补齐 id/type/from/to。",
            )
            continue

        rel_id = relation.get("id")
        rel_type = relation.get("type")
        rel_from = relation.get("from")
        rel_to = relation.get("to")

        for field in ("id", "type", "from", "to"):
            if field not in relation:
                add_missing_field_issue(ctx, relation_path, "TRACE401", field, f"Relation {rel_id or relation_path}")

        if not is_valid_id(rel_id):
            ctx.add_issue(
                "error",
                "TRACE401",
                f"{relation_path}.id",
                f"Relation {relation_path} 的 id 缺失或不符合 ID 规则。",
                "为 relation 使用如 `REL-CHECKOUT-001` 的稳定 ID。",
            )
        elif rel_id in relation_ids:
            ctx.add_issue(
                "error",
                "TRACE301",
                f"{relation_path}.id",
                f"Relation ID 重复：`{rel_id}`。",
                "确保每条 relation 的 ID 唯一。",
            )
        else:
            relation_ids.add(rel_id)

        if rel_type not in ALLOWED_RELATION_TYPES:
            ctx.add_issue(
                "error",
                "TRACE403",
                f"{relation_path}.type",
                f"Relation {rel_id or relation_path} 的 type 非法：`{rel_type}`。",
                "将 relation.type 设置为 derived_from/depends_on/refines/verifies/mitigates 之一。",
            )

        if relation.get("status") is not None and relation.get("status") not in ALLOWED_RELATION_STATUS:
            ctx.add_issue(
                "warning",
                "TRACE405",
                f"{relation_path}.status",
                f"Relation {rel_id or relation_path} 的 status 非标准：`{relation.get('status')}`。",
                "建议将 relation.status 设置为 active 或 deprecated。",
            )

        if is_non_empty_string(rel_from) and rel_from not in known_ids:
            ctx.add_issue(
                "error",
                "TRACE402",
                f"{relation_path}.from",
                f"Relation {rel_id or relation_path} 的 from 引用不存在：`{rel_from}`。",
                "确保 relation.from 引用当前文档中已声明的本地实体 ID。",
            )
        if is_non_empty_string(rel_to):
            if rel_to in known_ids or rel_to in source_documents:
                pass
            elif is_valid_id(rel_to):
                ctx.add_issue(
                    "info",
                    "TRACE404",
                    f"{relation_path}.to",
                    f"Relation {rel_id or relation_path} 的 to 指向外部对象 `{rel_to}`，将在 trace-build-rtm 中解析。",
                    "确保被引用对象会在后续 RTM 聚合输入中提供。",
                )
            else:
                ctx.add_issue(
                    "error",
                    "TRACE402",
                    f"{relation_path}.to",
                    f"Relation {rel_id or relation_path} 的 to 引用不存在：`{rel_to}`。",
                    "确保 relation.to 引用已声明实体 ID、artifact.source_documents 中的文档 ID，或合法的外部对象 ID。",
                )
        if rel_type == "verifies" and (not isinstance(rel_from, str) or not rel_from.startswith("CASE-")):
            ctx.add_issue(
                "error",
                "TRACE403",
                f"{relation_path}.from",
                f"Relation {rel_id or relation_path} 使用 verifies 时，from 必须是 `CASE-*`。",
                "将 verifies 关系的 from 调整为测试用例 ID。",
            )


def validate_waivers(ctx: LintContext, waivers: Any, known_ids: set[str]) -> None:
    if not isinstance(waivers, list):
        ctx.add_issue(
            "error",
            "TRACE501",
            "waivers",
            "waivers 必须是数组。",
            "将 waivers 改为数组；没有豁免时使用空数组。",
        )
        return

    today = date.today()
    waiver_ids: set[str] = set()
    for index, waiver in enumerate(waivers):
        waiver_path = f"waivers[{index}]"
        if not isinstance(waiver, dict):
            ctx.add_issue(
                "error",
                "TRACE501",
                waiver_path,
                f"{waiver_path} 必须是对象。",
                "将 waiver 改为对象，并补齐 id/target_ids/reason/status。",
            )
            continue

        waiver_id = waiver.get("id")
        if not is_valid_id(waiver_id):
            ctx.add_issue(
                "error",
                "TRACE501",
                f"{waiver_path}.id",
                f"{waiver_path} 的 id 缺失或不符合 ID 规则。",
                "为 waiver 使用如 `WVR-CHECKOUT-001` 的稳定 ID。",
            )
        elif waiver_id in waiver_ids:
            ctx.add_issue(
                "error",
                "TRACE301",
                f"{waiver_path}.id",
                f"Waiver ID 重复：`{waiver_id}`。",
                "确保每条 waiver 的 ID 唯一。",
            )
        else:
            waiver_ids.add(waiver_id)

        for field in ("target_ids", "reason", "status"):
            if field not in waiver:
                add_missing_field_issue(ctx, waiver_path, "TRACE501", field, f"Waiver {waiver_id or waiver_path}")

        status = waiver.get("status")
        if status is not None and status not in ALLOWED_WAIVER_STATUS:
            ctx.add_issue(
                "error",
                "TRACE501",
                f"{waiver_path}.status",
                f"Waiver {waiver_id or waiver_path} 的 status 非法：`{status}`。",
                "将 waiver.status 设置为 draft/approved/expired/revoked 之一。",
            )

        target_ids = waiver.get("target_ids", [])
        if not isinstance(target_ids, list):
            ctx.add_issue(
                "error",
                "TRACE501",
                f"{waiver_path}.target_ids",
                f"Waiver {waiver_id or waiver_path} 的 target_ids 必须是数组。",
                "将 target_ids 改为对象 ID 数组。",
            )
            target_ids = []
        for target_index, target_id in enumerate(target_ids):
            if target_id not in known_ids:
                ctx.add_issue(
                    "error",
                    "TRACE501",
                    f"{waiver_path}.target_ids[{target_index}]",
                    f"Waiver {waiver_id or waiver_path} 指向不存在的对象：`{target_id}`。",
                    "确保 waiver.target_ids 只引用当前文档已声明的对象 ID。",
                )

        approved = status == "approved"
        if approved:
            if not is_non_empty_string(waiver.get("approved_by")) or not is_valid_date(waiver.get("approved_at")):
                ctx.add_issue(
                    "error",
                    "TRACE501",
                    waiver_path,
                    f"Waiver {waiver_id or waiver_path} 已批准，但缺少 approved_by 或 approved_at。",
                    "为 approved waiver 补齐 approved_by 和 approved_at。",
                )
            expires_at = waiver.get("expires_at")
            if expires_at is not None:
                if not is_valid_date(expires_at):
                    ctx.add_issue(
                        "warning",
                        "TRACE502",
                        f"{waiver_path}.expires_at",
                        f"Waiver {waiver_id or waiver_path} 的 expires_at 不是合法日期。",
                        "修正 expires_at 或移除该字段。",
                    )
                elif date.fromisoformat(expires_at) < today:
                    ctx.add_issue(
                        "warning",
                        "TRACE502",
                        f"{waiver_path}.expires_at",
                        f"Waiver {waiver_id or waiver_path} 已过期。",
                        "更新 waiver 状态，或重新审批并延长有效期。",
                    )
        elif status in {"draft", "expired", "revoked"}:
            ctx.add_issue(
                "warning",
                "TRACE502",
                f"{waiver_path}.status",
                f"Waiver {waiver_id or waiver_path} 当前状态为 `{status}`，不会生效。",
                "如需从分母排除该对象，请将 waiver 正式审批为 approved。",
            )


def lint_metadata(path: Path, metadata: dict[str, Any] | None, forced_profile: str | None) -> ArtifactReport:
    ctx = LintContext(path)
    artifact_id: str | None = None
    artifact_type: str | None = None
    profile: str | None = forced_profile

    if metadata is None:
        return ArtifactReport(str(path), artifact_id, artifact_type, profile, ctx.issues)

    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in metadata:
            add_missing_field_issue(ctx, "", "TRACE101", key, "metadata envelope")

    profile = validate_schema(ctx, metadata.get("schema"), forced_profile)
    artifact_id, artifact_type, source_documents = validate_artifact(ctx, metadata.get("artifact"))
    entities_obj = metadata.get("entities")
    entity_ids, requirements = validate_entities(ctx, entities_obj, profile, source_documents)

    if profile == "prd-profile-v1":
        validate_prd_profile(
            ctx,
            artifact_type,
            entities_obj if isinstance(entities_obj, dict) else None,
            requirements,
        )
    elif profile == "journey-profile-v1":
        validate_journey_profile(
            ctx,
            artifact_id,
            artifact_type,
            source_documents,
            entities_obj if isinstance(entities_obj, dict) else None,
            metadata.get("relations"),
        )
    elif profile == "test-strategy-profile-v1":
        validate_test_strategy_profile(
            ctx,
            artifact_type,
            entities_obj if isinstance(entities_obj, dict) else None,
        )
    elif profile == "test-spec-profile-v1":
        validate_test_spec_profile(
            ctx,
            artifact_type,
            entities_obj if isinstance(entities_obj, dict) else None,
            metadata.get("relations"),
        )
    elif profile == "hld-profile-v1":
        validate_hld_profile(
            ctx,
            artifact_type,
            entities_obj if isinstance(entities_obj, dict) else None,
            metadata.get("relations"),
        )
    elif profile == "lld-profile-v1":
        validate_lld_profile(
            ctx,
            artifact_type,
            entities_obj if isinstance(entities_obj, dict) else None,
            metadata.get("relations"),
        )

    validate_relations(ctx, metadata.get("relations"), entity_ids, source_documents)
    validate_waivers(ctx, metadata.get("waivers"), entity_ids)

    return ArtifactReport(str(path), artifact_id, artifact_type, profile, ctx.issues)


def lint_path(path: Path, forced_profile: str | None) -> ArtifactReport:
    pre_ctx = LintContext(path)
    metadata = extract_metadata(path, pre_ctx)
    report = lint_metadata(path, metadata, forced_profile)
    report.issues = pre_ctx.issues + report.issues
    return report


def render_text(reports: list[ArtifactReport], strict: bool) -> str:
    blocks: list[str] = []
    for report in reports:
        counts = report.counts()
        status = "PASS" if report.result(strict) == "pass" else "FAIL"
        block = [
            f"TRACE-LINT RESULT: {status}",
            f"Artifact: {report.artifact_id or '<unknown>'} ({report.artifact_type or '<unknown>'})",
            f"Profile: {report.profile or '<unknown>'}",
            f"Path: {report.path}",
            "",
            f"Errors: {counts['errors']}",
            f"Warnings: {counts['warnings']}",
            f"Infos: {counts['infos']}",
        ]
        for issue in report.issues:
            block.extend(
                [
                    "",
                    f"[{issue.severity.upper()}] {issue.code} {issue.path}",
                    issue.message,
                    f"Suggestion: {issue.suggestion}",
                ]
            )
        blocks.append("\n".join(block))
    return "\n\n".join(blocks)


def render_json(reports: list[ArtifactReport], strict: bool) -> str:
    summary = {
        "artifacts": len(reports),
        "passed": sum(1 for report in reports if report.result(strict) == "pass"),
        "failed": sum(1 for report in reports if report.result(strict) == "fail"),
        "warnings": sum(report.counts()["warnings"] for report in reports),
        "errors": sum(report.counts()["errors"] for report in reports),
    }
    overall_status = "fail" if summary["failed"] > 0 else "pass"
    payload = {
        "tool": "trace-lint",
        "version": TOOL_VERSION,
        "status": overall_status,
        "strict": strict,
        "artifacts": [report.to_json(strict) for report in reports],
        "summary": summary,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def exit_code(reports: list[ArtifactReport], strict: bool) -> int:
    if any(report.result(strict) == "fail" for report in reports):
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    paths = [Path(item).resolve() for item in args.paths]

    for path in paths:
        if not path.exists() or not path.is_file():
            print(f"trace-lint: input file does not exist: {path}", file=sys.stderr)
            return 2

    try:
        reports = [lint_path(path, args.profile) for path in paths]
    except OSError as exc:
        print(f"trace-lint: failed to read input: {exc}", file=sys.stderr)
        return 2

    output = render_json(reports, args.strict) if args.format == "json" else render_text(reports, args.strict)
    print(output)
    return exit_code(reports, args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
