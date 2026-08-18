from __future__ import annotations

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "trace_build_rtm.py"


PRD_METADATA = """
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: prd-profile-v1
artifact:
  id: PRD-CHECKOUT-001
  type: PRD
  title: 优惠券结算能力
  status: draft
  created_at: 2026-03-08
  updated_at: 2026-03-08
  source_documents:
    - BRD-CHECKOUT-001
entities:
  requirements:
    - id: REQ-CHECKOUT-001
      class: functional
      title: 支持在结算页应用优惠券
      statement: 系统必须允许用户在结算页输入有效优惠券并应用折扣。
      priority: P0
      status: proposed
      scope: in
      acceptance_criteria:
        - 用户输入有效优惠券后，必须展示折后金额。
      source_refs:
        - artifact_id: BRD-CHECKOUT-001
          section: 3.1
  risks: []
  must_not_regress: []
  external_behaviors: []
  decisions: []
  flows: []
  test_cases: []
relations:
  - id: REL-PRD-001
    type: derived_from
    from: REQ-CHECKOUT-001
    to: BRD-CHECKOUT-001
    status: active
waivers: []
"""


TEST_STRATEGY_METADATA = """
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: test-strategy-profile-v1
artifact:
  id: TSTRAT-CHECKOUT-001
  type: TEST_STRATEGY
  title: 优惠券结算测试策略
  status: draft
  created_at: 2026-03-08
  updated_at: 2026-03-08
  source_documents:
    - PRD-CHECKOUT-001
entities:
  requirements: []
  risks:
    - id: RISK-CHECKOUT-001
      title: 折扣金额与最终成交价不一致
      statement: 结算页展示金额与实际入单金额可能不一致。
      status: proposed
      scope: in
      level: high
      source_refs:
        - artifact_id: PRD-CHECKOUT-001
          section: 2.3
  must_not_regress:
    - id: MR-CHECKOUT-001
      title: 原价下单流程不能退化
      statement: 不使用优惠券时的原价下单流程必须保持稳定。
      status: proposed
      scope: in
      priority: P0
      source_refs:
        - artifact_id: PRD-CHECKOUT-001
          section: 3.2
  external_behaviors:
    - id: BEH-CHECKOUT-001
      title: 结算页展示折后金额
      statement: 用户输入有效优惠券后，结算页必须展示折后金额。
      status: proposed
      scope: in
      actor: user
      trigger: 输入有效优惠券
      observable_outcome: 页面金额发生变化
      source_refs:
        - artifact_id: PRD-CHECKOUT-001
          section: 3.1
  decisions: []
  flows: []
  test_cases: []
relations: []
waivers: []
"""


TEST_SPEC_METADATA = """
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: test-spec-profile-v1
artifact:
  id: TSPEC-CHECKOUT-001
  type: TEST_SPEC
  title: 优惠券结算测试包
  status: draft
  created_at: 2026-03-08
  updated_at: 2026-03-08
  source_documents:
    - PRD-CHECKOUT-001
    - TSTRAT-CHECKOUT-001
entities:
  requirements: []
  risks: []
  must_not_regress: []
  external_behaviors: []
  decisions: []
  flows: []
  test_cases:
    - id: CASE-CHECKOUT-001
      title: 优惠券主流程
      statement: 验证用户在结算页成功应用优惠券并下单。
      status: proposed
      scope: in
      layer: e2e
      priority: P0
      source_refs:
        - artifact_id: PRD-CHECKOUT-001
          section: 3.1
relations:
  - id: REL-TSPEC-001
    type: verifies
    from: CASE-CHECKOUT-001
    to: REQ-CHECKOUT-001
    status: active
  - id: REL-TSPEC-002
    type: verifies
    from: CASE-CHECKOUT-001
    to: RISK-CHECKOUT-001
    status: active
  - id: REL-TSPEC-003
    type: verifies
    from: CASE-CHECKOUT-001
    to: MR-CHECKOUT-001
    status: active
  - id: REL-TSPEC-004
    type: verifies
    from: CASE-CHECKOUT-001
    to: BEH-CHECKOUT-001
    status: active
waivers: []
"""


PRD_WARNING_METADATA = """
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: prd-profile-v1
artifact:
  id: PRD-CHECKOUT-001
  type: PRD
  title: 优惠券结算能力
  status: draft
  created_at: 2026-03-08
  updated_at: 2026-03-08
  source_documents:
    - BRD-CHECKOUT-001
entities:
  requirements:
    - id: REQ-CHECKOUT-001
      class: functional
      title: 支持在结算页应用优惠券
      statement: 系统必须允许用户在结算页输入有效优惠券并应用折扣。
      priority: P0
      status: proposed
      scope: in
      acceptance_criteria:
        - 用户输入有效优惠券后，必须展示折后金额。
  risks: []
  must_not_regress: []
  external_behaviors: []
  decisions: []
  flows: []
  test_cases: []
relations: []
waivers: []
"""


class TraceBuildRtmCliTests(unittest.TestCase):
    maxDiff = None

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(SCRIPT_PATH), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def write_file(self, directory: Path, name: str, content: str) -> Path:
        path = directory / name
        path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
        return path

    def test_build_rtm_json_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prd = self.write_file(root, "prd.yaml", PRD_METADATA)
            strategy = self.write_file(root, "test-strategy.yaml", TEST_STRATEGY_METADATA)
            spec = self.write_file(root, "test-spec.yaml", TEST_SPEC_METADATA)

            result = self.run_cli("--format", "json", str(prd), str(strategy), str(spec))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["tool"], "trace-build-rtm")
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["build"]["summary"]["requirements_total"], 1)
        self.assertEqual(payload["build"]["summary"]["requirements_covered"], 1)
        self.assertEqual(payload["build"]["summary"]["risks_covered"], 1)
        self.assertEqual(payload["build"]["summary"]["must_not_regress_covered"], 1)
        self.assertEqual(payload["build"]["summary"]["external_behaviors_covered"], 1)
        self.assertEqual(payload["build"]["summary"]["unresolved_relation_targets"], 0)
        self.assertEqual(payload["build"]["test_case_links"][0]["verifies"][0], "BEH-CHECKOUT-001")

    def test_unresolved_external_target_fails_build(self) -> None:
        broken_spec = TEST_SPEC_METADATA.replace("REQ-CHECKOUT-001", "REQ-MISSING-001", 1)
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prd = self.write_file(root, "prd.yaml", PRD_METADATA)
            strategy = self.write_file(root, "test-strategy.yaml", TEST_STRATEGY_METADATA)
            spec = self.write_file(root, "test-spec.yaml", broken_spec)

            result = self.run_cli("--format", "json", str(prd), str(strategy), str(spec))

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertEqual(payload["build"]["summary"]["unresolved_relation_targets"], 1)
        self.assertEqual(payload["build"]["issues"][0]["code"], "RTM003")

    def test_duplicate_entity_id_fails_build(self) -> None:
        duplicate_strategy = TEST_STRATEGY_METADATA.replace("RISK-CHECKOUT-001", "REQ-CHECKOUT-001")
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prd = self.write_file(root, "prd.yaml", PRD_METADATA)
            strategy = self.write_file(root, "test-strategy.yaml", duplicate_strategy)
            spec = self.write_file(root, "test-spec.yaml", TEST_SPEC_METADATA)

            result = self.run_cli("--format", "json", str(prd), str(strategy), str(spec))

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertEqual(payload["build"]["issues"][0]["code"], "RTM002")

    def test_strict_mode_fails_on_lint_warning(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prd = self.write_file(root, "prd.yaml", PRD_WARNING_METADATA)

            result = self.run_cli("--strict", "--format", "json", str(prd))

        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "fail")
        self.assertEqual(payload["lint"]["summary"]["failed"], 1)
        self.assertEqual(payload["lint"]["reports"][0]["summary"]["warnings"], 1)


    # ── HLD/LLD RTM integration tests ──

    def test_hld_refines_covers_requirements_and_decisions(self) -> None:
        """PRD + HLD: refines relations should make DEC/FLOW covered and REQ refined_by."""
        hld_metadata = """
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: hld-profile-v1
artifact:
  id: HLD-CHECKOUT-001
  type: HLD
  title: 优惠券结算技术设计
  status: draft
  created_at: 2026-03-08
  updated_at: 2026-03-08
  source_documents:
    - PRD-CHECKOUT-001
entities:
  requirements: []
  risks: []
  must_not_regress: []
  external_behaviors: []
  decisions:
    - id: DEC-CHECKOUT-001
      title: gRPC 选型
      statement: 使用营销服务 gRPC 接口
      status: proposed
      scope: in
      decision: gRPC
      rationale: 低延迟
  flows:
    - id: FLOW-CHECKOUT-001
      title: 优惠券主流程
      statement: 校验 → 计算 → 签名
      status: proposed
      scope: in
      kind: system_flow
  test_cases: []
relations:
  - id: REL-HLD-001
    type: refines
    from: DEC-CHECKOUT-001
    to: REQ-CHECKOUT-001
    status: active
  - id: REL-HLD-002
    type: refines
    from: FLOW-CHECKOUT-001
    to: REQ-CHECKOUT-001
    status: active
waivers: []
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prd = self.write_file(root, "prd.yaml", PRD_METADATA)
            hld = self.write_file(root, "hld.yaml", hld_metadata)

            result = self.run_cli("--format", "json", str(prd), str(hld))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        summary = payload["build"]["summary"]

        # DEC and FLOW should be covered (they have outgoing refines)
        self.assertEqual(summary["decisions_total"], 1)
        self.assertEqual(summary["decisions_covered"], 1)
        self.assertEqual(summary["flows_total"], 1)
        self.assertEqual(summary["flows_covered"], 1)

        # REQ should be covered (it has incoming refines from DEC/FLOW)
        self.assertEqual(summary["requirements_total"], 1)
        self.assertEqual(summary["requirements_covered"], 1)

    def test_hld_rtm_markdown_contains_decisions_flows_sections(self) -> None:
        """PRD + HLD markdown output should contain Decisions Matrix and Flows Matrix."""
        hld_metadata = """
schema:
  name: gainfactor-pm-traceability
  version: "1.0.0"
  profile: hld-profile-v1
artifact:
  id: HLD-CHECKOUT-001
  type: HLD
  title: test
  status: draft
  created_at: 2026-03-08
  updated_at: 2026-03-08
  source_documents:
    - PRD-CHECKOUT-001
entities:
  requirements: []
  risks: []
  must_not_regress: []
  external_behaviors: []
  decisions:
    - id: DEC-CHECKOUT-001
      title: test decision
      statement: test
      status: proposed
      scope: in
      decision: test
      rationale: test
  flows: []
  test_cases: []
relations:
  - id: REL-HLD-001
    type: refines
    from: DEC-CHECKOUT-001
    to: REQ-CHECKOUT-001
    status: active
waivers: []
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            prd = self.write_file(root, "prd.yaml", PRD_METADATA)
            hld = self.write_file(root, "hld.yaml", hld_metadata)

            result = self.run_cli("--format", "markdown", str(prd), str(hld))

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("## Decisions Matrix", result.stdout)
        self.assertIn("## Flows Matrix", result.stdout)
        self.assertIn("## Uncovered Decisions", result.stdout)
        self.assertIn("## Uncovered Flows", result.stdout)
        self.assertIn("DEC-CHECKOUT-001", result.stdout)


if __name__ == "__main__":
    unittest.main()
