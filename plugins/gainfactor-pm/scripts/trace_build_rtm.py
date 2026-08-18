#!/usr/bin/env python3
"""Build an aggregated RTM from gainfactor-pm traceability metadata.

Examples:
  python3 plugins/gainfactor-pm/scripts/trace_build_rtm.py docs/PRD.md docs/Test-Strategy.md docs/Test-Spec.md
  python3 plugins/gainfactor-pm/scripts/trace_build_rtm.py --format json docs/*.md
  python3 plugins/gainfactor-pm/scripts/trace_build_rtm.py --strict docs/*.md
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import trace_lint


TOOL_VERSION = "1.0.0"
ARTIFACT_PREFIXES = ("BRD-", "JOURNEY-", "PRD-", "API-", "HLD-", "LLD-", "TSTRAT-", "TSPEC-", "RUNBOOK-")
ENTITY_PREFIXES = ("REQ-", "RISK-", "MR-", "BEH-", "DEC-", "FLOW-", "CASE-", "WVR-", "REL-")
MATRIX_BUCKETS = ("requirements", "risks", "must_not_regress", "external_behaviors", "decisions", "flows", "test_cases")


@dataclass
class BuildIssue:
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


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trace-build-rtm",
        description="Build an aggregated RTM from gainfactor-pm traceability metadata.",
        epilog=(
            "Examples:\n"
            "  python3 plugins/gainfactor-pm/scripts/trace_build_rtm.py docs/PRD.md docs/Test-Strategy.md docs/Test-Spec.md\n"
            "  python3 plugins/gainfactor-pm/scripts/trace_build_rtm.py --format json docs/PRD.md docs/Test-Spec.md\n"
            "  python3 plugins/gainfactor-pm/scripts/trace_build_rtm.py --strict docs/*.md"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="+", help="One or more Markdown/YAML files to aggregate")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail when any input produces trace-lint warnings",
    )
    return parser.parse_args(argv)


def load_metadata(path: Path) -> dict[str, Any]:
    ctx = trace_lint.LintContext(path)
    metadata = trace_lint.extract_metadata(path, ctx)
    if metadata is None:
        raise ValueError(f"Failed to parse metadata from {path}")
    return metadata


def is_entity_id(identifier: str) -> bool:
    return identifier.startswith(ENTITY_PREFIXES)


def is_artifact_id(identifier: str) -> bool:
    return identifier.startswith(ARTIFACT_PREFIXES)


def is_active_waiver(waiver: dict[str, Any]) -> bool:
    if waiver.get("status") != "approved":
        return False
    expires_at = waiver.get("expires_at")
    if expires_at is None:
        return True
    if isinstance(expires_at, date):
        return expires_at >= date.today()
    if isinstance(expires_at, str):
        try:
            return date.fromisoformat(expires_at) >= date.today()
        except ValueError:
            return False
    return False


def build_issue(severity: str, code: str, path: str, message: str, suggestion: str) -> BuildIssue:
    return BuildIssue(severity, code, path, message, suggestion)


def aggregate(
    metadata_entries: list[tuple[Path, dict[str, Any]]],
) -> tuple[dict[str, Any], list[BuildIssue]]:
    issues: list[BuildIssue] = []
    artifacts: dict[str, dict[str, Any]] = {}
    entities: dict[str, dict[str, Any]] = {}
    relations: list[dict[str, Any]] = []
    waivers: list[dict[str, Any]] = []

    for path, metadata in metadata_entries:
        schema = metadata["schema"]
        artifact = metadata["artifact"]
        artifact_id = artifact["id"]
        artifact_entry = {
            "id": artifact_id,
            "type": artifact["type"],
            "title": artifact.get("title"),
            "status": artifact.get("status"),
            "profile": schema.get("profile"),
            "path": str(path),
            "source_documents": list(artifact.get("source_documents", []) or []),
        }
        if artifact_id in artifacts:
            issues.append(
                build_issue(
                    "error",
                    "RTM001",
                    str(path),
                    f"Artifact ID 重复：`{artifact_id}`。",
                    "确保聚合输入中的 artifact.id 全局唯一。",
                )
            )
        else:
            artifacts[artifact_id] = artifact_entry

        raw_entities = metadata.get("entities", {})
        for bucket_name, bucket in raw_entities.items():
            if not isinstance(bucket, list):
                continue
            for index, entity in enumerate(bucket):
                if not isinstance(entity, dict):
                    continue
                entity_id = entity.get("id")
                if not isinstance(entity_id, str):
                    continue
                entity_entry = {
                    "id": entity_id,
                    "bucket": bucket_name,
                    "artifact_id": artifact_id,
                    "artifact_type": artifact["type"],
                    "artifact_profile": schema.get("profile"),
                    "path": str(path),
                    "title": entity.get("title"),
                    "statement": entity.get("statement"),
                    "status": entity.get("status"),
                    "scope": entity.get("scope"),
                    "data": entity,
                }
                if entity_id in entities:
                    issues.append(
                        build_issue(
                            "error",
                            "RTM002",
                            f"{path}:entities.{bucket_name}[{index}]",
                            f"实体 ID 重复：`{entity_id}`。",
                            "确保聚合输入中的实体 ID 全局唯一。",
                        )
                    )
                else:
                    entities[entity_id] = entity_entry

        raw_relations = metadata.get("relations", [])
        if isinstance(raw_relations, list):
            for relation in raw_relations:
                if not isinstance(relation, dict):
                    continue
                relations.append(
                    {
                        **relation,
                        "artifact_id": artifact_id,
                        "artifact_type": artifact["type"],
                        "artifact_profile": schema.get("profile"),
                        "path": str(path),
                    }
                )

        raw_waivers = metadata.get("waivers", [])
        if isinstance(raw_waivers, list):
            for waiver in raw_waivers:
                if not isinstance(waiver, dict):
                    continue
                waivers.append({**waiver, "artifact_id": artifact_id, "path": str(path)})

    incoming: dict[str, list[dict[str, Any]]] = {entity_id: [] for entity_id in entities}
    outgoing: dict[str, list[dict[str, Any]]] = {entity_id: [] for entity_id in entities}
    unresolved_relation_targets: list[dict[str, Any]] = []

    for relation in relations:
        rel_id = relation.get("id", "<unknown>")
        rel_from = relation.get("from")
        rel_to = relation.get("to")

        if isinstance(rel_from, str):
            if rel_from in entities:
                outgoing[rel_from].append(relation)
            else:
                issues.append(
                    build_issue(
                        "error",
                        "RTM004",
                        f"{relation['path']}:relations.{rel_id}",
                        f"Relation `{rel_id}` 的 from `{rel_from}` 在全局聚合后仍无法解析。",
                        "确保 relation.from 指向当前输入集合中的已声明实体。",
                    )
                )

        if not isinstance(rel_to, str):
            continue

        if rel_to in entities:
            incoming[rel_to].append(relation)
            continue

        if is_artifact_id(rel_to):
            continue

        if is_entity_id(rel_to):
            unresolved = {
                "relation_id": rel_id,
                "artifact_id": relation["artifact_id"],
                "from": rel_from,
                "to": rel_to,
                "type": relation.get("type"),
                "path": relation["path"],
            }
            unresolved_relation_targets.append(unresolved)
            issues.append(
                build_issue(
                    "error",
                    "RTM003",
                    f"{relation['path']}:relations.{rel_id}.to",
                    f"Relation `{rel_id}` 指向外部对象 `{rel_to}`，但在本次 RTM 聚合输入中未找到。",
                    "将被引用对象对应的 metadata 文档一起传给 trace-build-rtm。",
                )
            )

    active_waivers: dict[str, list[str]] = {}
    for waiver in waivers:
        if not is_active_waiver(waiver):
            continue
        waiver_id = waiver.get("id")
        for target_id in waiver.get("target_ids", []) or []:
            if isinstance(target_id, str):
                active_waivers.setdefault(target_id, []).append(waiver_id)

    orphan_entities: list[dict[str, Any]] = []
    for entity_id, entity in entities.items():
        if len(incoming.get(entity_id, [])) == 0 and len(outgoing.get(entity_id, [])) == 0:
            orphan_entities.append(
                {
                    "id": entity_id,
                    "artifact_id": entity["artifact_id"],
                    "bucket": entity["bucket"],
                    "title": entity.get("title"),
                }
            )
            issues.append(
                build_issue(
                    "warning",
                    "RTM101",
                    f"{entity['path']}:{entity_id}",
                    f"实体 `{entity_id}` 是 orphan，没有任何 incoming/outgoing relation。",
                    "检查该实体是否遗漏了 derived_from/verifies/mitigates/refines 等关系。",
                )
            )

    def entity_row(entity: dict[str, Any]) -> dict[str, Any]:
        entity_id = entity["id"]
        incoming_relations = incoming.get(entity_id, [])
        outgoing_relations = outgoing.get(entity_id, [])
        verified_by = sorted(
            relation["from"]
            for relation in incoming_relations
            if relation.get("type") == "verifies" and isinstance(relation.get("from"), str)
        )
        mitigated_by = sorted(
            relation["from"]
            for relation in incoming_relations
            if relation.get("type") == "mitigates" and isinstance(relation.get("from"), str)
        )
        derived_from = sorted(
            relation["to"]
            for relation in outgoing_relations
            if relation.get("type") == "derived_from" and isinstance(relation.get("to"), str)
        )
        refines = sorted(
            relation["to"]
            for relation in outgoing_relations
            if relation.get("type") == "refines" and isinstance(relation.get("to"), str)
        )
        refined_by = sorted(
            relation["from"]
            for relation in incoming_relations
            if relation.get("type") == "refines" and isinstance(relation.get("from"), str)
        )
        waived_by = sorted(active_waivers.get(entity_id, []))
        bucket = entity["bucket"]

        if bucket == "risks":
            covered = bool(verified_by or mitigated_by or waived_by)
        elif bucket in {"requirements", "must_not_regress", "external_behaviors"}:
            covered = bool(verified_by or refined_by or waived_by)
        elif bucket in {"decisions", "flows"}:
            # DEC-*/FLOW-* are covered if they have outgoing refines/derived_from (tracing to upstream)
            covered = bool(refines or derived_from or waived_by)
        else:
            covered = bool(verified_by or mitigated_by or derived_from or refines or waived_by)

        if waived_by:
            coverage_status = "waived"
        else:
            coverage_status = "covered" if covered else "uncovered"

        return {
            "id": entity_id,
            "artifact_id": entity["artifact_id"],
            "artifact_type": entity["artifact_type"],
            "profile": entity["artifact_profile"],
            "bucket": bucket,
            "title": entity.get("title"),
            "status": entity.get("status"),
            "scope": entity.get("scope"),
            "verified_by": verified_by,
            "mitigated_by": mitigated_by,
            "derived_from": derived_from,
            "refines": refines,
            "refined_by": refined_by,
            "waived_by": waived_by,
            "coverage_status": coverage_status,
            "data": entity["data"],
        }

    matrices = {
        bucket: [entity_row(entity) for entity in entities.values() if entity["bucket"] == bucket]
        for bucket in MATRIX_BUCKETS
    }

    test_case_links: list[dict[str, Any]] = []
    for case in matrices["test_cases"]:
        outgoing_relations = outgoing.get(case["id"], [])
        verified_targets = sorted(
            relation["to"]
            for relation in outgoing_relations
            if relation.get("type") == "verifies" and isinstance(relation.get("to"), str)
        )
        case["verifies"] = verified_targets
        test_case_links.append(
            {
                "id": case["id"],
                "artifact_id": case["artifact_id"],
                "title": case["title"],
                "verifies": verified_targets,
            }
        )

    def count_covered(rows: list[dict[str, Any]]) -> int:
        return sum(1 for row in rows if row["coverage_status"] in {"covered", "waived"})

    summary = {
        "artifacts": len(artifacts),
        "entities": len(entities),
        "relations": len(relations),
        "waivers": len(waivers),
        "requirements_total": len(matrices["requirements"]),
        "requirements_covered": count_covered(matrices["requirements"]),
        "requirements_uncovered": sum(1 for row in matrices["requirements"] if row["coverage_status"] == "uncovered"),
        "risks_total": len(matrices["risks"]),
        "risks_covered": count_covered(matrices["risks"]),
        "risks_uncovered": sum(1 for row in matrices["risks"] if row["coverage_status"] == "uncovered"),
        "must_not_regress_total": len(matrices["must_not_regress"]),
        "must_not_regress_covered": count_covered(matrices["must_not_regress"]),
        "must_not_regress_uncovered": sum(
            1 for row in matrices["must_not_regress"] if row["coverage_status"] == "uncovered"
        ),
        "external_behaviors_total": len(matrices["external_behaviors"]),
        "external_behaviors_covered": count_covered(matrices["external_behaviors"]),
        "external_behaviors_uncovered": sum(
            1 for row in matrices["external_behaviors"] if row["coverage_status"] == "uncovered"
        ),
        "decisions_total": len(matrices.get("decisions", [])),
        "decisions_covered": count_covered(matrices.get("decisions", [])),
        "decisions_uncovered": sum(1 for row in matrices.get("decisions", []) if row["coverage_status"] == "uncovered"),
        "flows_total": len(matrices.get("flows", [])),
        "flows_covered": count_covered(matrices.get("flows", [])),
        "flows_uncovered": sum(1 for row in matrices.get("flows", []) if row["coverage_status"] == "uncovered"),
        "test_cases_total": len(matrices["test_cases"]),
        "unresolved_relation_targets": len(unresolved_relation_targets),
        "orphan_entities": len(orphan_entities),
    }

    aggregate_payload = {
        "artifacts": sorted(artifacts.values(), key=lambda item: item["id"]),
        "entities": {entity_id: entities[entity_id] for entity_id in sorted(entities)},
        "relations": relations,
        "waivers": waivers,
        "matrices": matrices,
        "test_case_links": test_case_links,
        "unresolved_relation_targets": unresolved_relation_targets,
        "orphan_entities": orphan_entities,
        "summary": summary,
    }
    return aggregate_payload, issues


def render_failure_json(
    lint_reports: list[trace_lint.ArtifactReport],
    build_issues: list[BuildIssue],
    strict: bool,
) -> str:
    lint_summary = {
        "artifacts": len(lint_reports),
        "passed": sum(1 for report in lint_reports if report.result(strict) == "pass"),
        "failed": sum(1 for report in lint_reports if report.result(strict) == "fail"),
        "warnings": sum(report.counts()["warnings"] for report in lint_reports),
        "errors": sum(report.counts()["errors"] for report in lint_reports),
    }
    payload = {
        "tool": "trace-build-rtm",
        "version": TOOL_VERSION,
        "status": "fail",
        "strict": strict,
        "lint": {
            "status": "fail" if lint_summary["failed"] > 0 else "pass",
            "reports": [report.to_json(strict) for report in lint_reports],
            "summary": lint_summary,
        },
        "build_issues": [issue.to_json() for issue in build_issues],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def render_success_json(
    lint_reports: list[trace_lint.ArtifactReport],
    aggregate_payload: dict[str, Any],
    build_issues: list[BuildIssue],
    strict: bool,
) -> str:
    lint_summary = {
        "artifacts": len(lint_reports),
        "passed": sum(1 for report in lint_reports if report.result(strict) == "pass"),
        "failed": sum(1 for report in lint_reports if report.result(strict) == "fail"),
        "warnings": sum(report.counts()["warnings"] for report in lint_reports),
        "errors": sum(report.counts()["errors"] for report in lint_reports),
    }
    status = "fail" if any(issue.severity == "error" for issue in build_issues) else "pass"
    payload = {
        "tool": "trace-build-rtm",
        "version": TOOL_VERSION,
        "status": status,
        "strict": strict,
        "lint": {
            "status": "fail" if lint_summary["failed"] > 0 else "pass",
            "reports": [report.to_json(strict) for report in lint_reports],
            "summary": lint_summary,
        },
        "build": {
            "issues": [issue.to_json() for issue in build_issues],
            **aggregate_payload,
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def format_list(values: list[str]) -> str:
    return ", ".join(values) if values else "-"


def render_markdown(
    lint_reports: list[trace_lint.ArtifactReport],
    aggregate_payload: dict[str, Any],
    build_issues: list[BuildIssue],
    strict: bool,
) -> str:
    summary = aggregate_payload["summary"]
    lines = [
        "# RTM 汇总",
        "",
        "## 概览",
        "",
        "| 指标 | 数值 |",
        "|------|------|",
        f"| Artifacts | {summary['artifacts']} |",
        f"| Entities | {summary['entities']} |",
        f"| Relations | {summary['relations']} |",
        f"| Requirements Covered / Total | {summary['requirements_covered']} / {summary['requirements_total']} |",
        f"| Risks Covered / Total | {summary['risks_covered']} / {summary['risks_total']} |",
        f"| Must-not-regress Covered / Total | {summary['must_not_regress_covered']} / {summary['must_not_regress_total']} |",
        f"| External Behaviors Covered / Total | {summary['external_behaviors_covered']} / {summary['external_behaviors_total']} |",
        f"| Decisions Covered / Total | {summary['decisions_covered']} / {summary['decisions_total']} |",
        f"| Flows Covered / Total | {summary['flows_covered']} / {summary['flows_total']} |",
        f"| Test Cases | {summary['test_cases_total']} |",
        f"| Unresolved Relation Targets | {summary['unresolved_relation_targets']} |",
        f"| Orphan Entities | {summary['orphan_entities']} |",
        "",
        "## Inputs",
        "",
        "| Artifact | Type | Profile | Path |",
        "|----------|------|---------|------|",
    ]

    for artifact in aggregate_payload["artifacts"]:
        lines.append(f"| {artifact['id']} | {artifact['type']} | {artifact['profile']} | {artifact['path']} |")

    def render_matrix(title: str, rows: list[dict[str, Any]], extra_column: str) -> None:
        lines.extend(
            [
                "",
                f"## {title}",
                "",
                "| ID | Artifact | 标题 | 覆盖状态 | 覆盖/关联对象 | 来源 |",
                "|----|----------|------|----------|---------------|------|",
            ]
        )
        for row in rows:
            if extra_column == "verified":
                linked = row["verified_by"]
            elif extra_column == "risk":
                linked = sorted(set(row["verified_by"] + row["mitigated_by"]))
            elif extra_column == "refines":
                linked = row.get("refines", []) + row.get("derived_from", [])
            else:
                linked = row.get("verifies", [])
            lines.append(
                f"| {row['id']} | {row['artifact_id']} | {row.get('title') or '-'} | {row['coverage_status']} | "
                f"{format_list(linked)} | {format_list(row.get('derived_from', []))} |"
            )

    render_matrix("Requirements Matrix", aggregate_payload["matrices"]["requirements"], "verified")
    render_matrix("Risks Matrix", aggregate_payload["matrices"]["risks"], "risk")
    render_matrix("Must-not-regress Matrix", aggregate_payload["matrices"]["must_not_regress"], "verified")
    render_matrix("External Behaviors Matrix", aggregate_payload["matrices"]["external_behaviors"], "verified")
    render_matrix("Decisions Matrix", aggregate_payload["matrices"].get("decisions", []), "refines")
    render_matrix("Flows Matrix", aggregate_payload["matrices"].get("flows", []), "refines")

    lines.extend(
        [
            "",
            "## Test Cases Matrix",
            "",
            "| ID | Artifact | 标题 | Verifies |",
            "|----|----------|------|----------|",
        ]
    )
    for case in aggregate_payload["test_case_links"]:
        lines.append(
            f"| {case['id']} | {case['artifact_id']} | {case.get('title') or '-'} | {format_list(case['verifies'])} |"
        )

    missing_sections = [
        ("Uncovered Requirements", [row for row in aggregate_payload["matrices"]["requirements"] if row["coverage_status"] == "uncovered"]),
        ("Uncovered Risks", [row for row in aggregate_payload["matrices"]["risks"] if row["coverage_status"] == "uncovered"]),
        (
            "Uncovered Must-not-regress",
            [row for row in aggregate_payload["matrices"]["must_not_regress"] if row["coverage_status"] == "uncovered"],
        ),
        (
            "Uncovered External Behaviors",
            [row for row in aggregate_payload["matrices"]["external_behaviors"] if row["coverage_status"] == "uncovered"],
        ),
        (
            "Uncovered Decisions",
            [row for row in aggregate_payload["matrices"].get("decisions", []) if row["coverage_status"] == "uncovered"],
        ),
        (
            "Uncovered Flows",
            [row for row in aggregate_payload["matrices"].get("flows", []) if row["coverage_status"] == "uncovered"],
        ),
    ]
    for title, rows in missing_sections:
        lines.extend(["", f"## {title}", ""])
        if not rows:
            lines.append("- None")
            continue
        for row in rows:
            lines.append(f"- `{row['id']}` {row.get('title') or ''}".rstrip())

    lines.extend(["", "## Build Issues", ""])
    if not build_issues:
        lines.append("- None")
    else:
        for issue in build_issues:
            lines.append(f"- [{issue.severity.upper()}] {issue.code} {issue.message}")

    lint_warnings_or_infos = [
        issue
        for report in lint_reports
        for issue in report.issues
        if issue.severity in {"warning", "info"}
    ]
    lines.extend(["", "## Lint Notes", ""])
    if not lint_warnings_or_infos:
        lines.append("- None")
    else:
        for issue in lint_warnings_or_infos:
            lines.append(f"- [{issue.severity.upper()}] {issue.code} {issue.message}")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    paths = [Path(item).resolve() for item in args.paths]
    for path in paths:
        if not path.exists() or not path.is_file():
            print(f"trace-build-rtm: input file does not exist: {path}", file=sys.stderr)
            return 2

    lint_reports = [trace_lint.lint_path(path, None) for path in paths]
    if any(report.result(args.strict) == "fail" for report in lint_reports):
        if args.format == "json":
            print(render_failure_json(lint_reports, [], args.strict))
        else:
            print(trace_lint.render_text(lint_reports, args.strict))
        return 1

    try:
        metadata_entries = [(path, load_metadata(path)) for path in paths]
    except (OSError, ValueError) as exc:
        print(f"trace-build-rtm: failed to read input: {exc}", file=sys.stderr)
        return 2

    aggregate_payload, build_issues = aggregate(metadata_entries)
    has_build_errors = any(issue.severity == "error" for issue in build_issues)

    if args.format == "json":
        print(render_success_json(lint_reports, aggregate_payload, build_issues, args.strict))
    else:
        print(render_markdown(lint_reports, aggregate_payload, build_issues, args.strict))

    return 1 if has_build_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
