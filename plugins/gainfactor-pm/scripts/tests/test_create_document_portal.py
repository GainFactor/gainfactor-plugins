#!/usr/bin/env python3
"""Regression tests for the shared document review portal scaffold."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
import json
from pathlib import Path


SCRIPT = Path(__file__).parent.parent / "create_document_portal.py"


class CreateDocumentPortalTest(unittest.TestCase):
    def test_imports_document_metadata_and_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "input.md"
            target = root / "portal"
            source.write_text(
                "# 示例 PRD：结算流程\n\n这是本轮测试文档。\n\n## 一、版本说明\n\n正文。\n",
                encoding="utf-8",
            )
            review = root / "review.json"
            review.write_text(
                json.dumps({
                    "conclusion": "有条件通过",
                    "issues": [{
                        "id": "PRD-001",
                        "severity": "P1",
                        "title": "补充验收标准",
                        "sectionId": "一版本说明",
                        "sectionTitle": "一、版本说明",
                        "suggestion": "增加可量化结果。",
                    }],
                }, ensure_ascii=False),
                encoding="utf-8",
            )

            subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    str(source),
                    str(target),
                    "--slug=settlement-prd",
                    "--type=PRD",
                    "--version=V2.1",
                    "--status=评审中",
                    "--owner=产品团队",
                    "--updated=2026-08-18",
                    f"--review={review}",
                ],
                check=True,
            )

            generated = (target / "content/docs/product-requirements/settlement-prd.mdx").read_text(encoding="utf-8")
            portal_data = (target / "lib/portal-data.generated.ts").read_text(encoding="utf-8")
            self.assertIn('title: "示例 PRD：结算流程"', generated)
            self.assertIn("这是本轮测试文档。", generated)
            self.assertIn('"version": "V2.1"', portal_data)
            self.assertIn('"status": "评审中"', portal_data)
            self.assertIn('"conclusion": "有条件通过"', portal_data)
            self.assertIn('"sectionId": "一版本说明"', portal_data)
            self.assertIn('"sectionTitle": "一、版本说明"', portal_data)
            self.assertNotIn("教务系统", (target / "app/(home)/page.tsx").read_text(encoding="utf-8"))

    def test_accepts_frontmatter_title_without_h1(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "input.mdx"
            target = root / "portal"
            source.write_text(
                '---\ntitle: "仅 Frontmatter 的 PRD"\ndescription: "原摘要"\n---\n\n正文。\n',
                encoding="utf-8",
            )

            subprocess.run(["python3", str(SCRIPT), str(source), str(target), "--slug=frontmatter-doc"], check=True)

            generated = (target / "content/docs/other/frontmatter-doc.mdx").read_text(encoding="utf-8")
            self.assertIn('title: "仅 Frontmatter 的 PRD"', generated)
            self.assertIn("正文。", generated)

    def test_adds_multiple_documents_to_one_portal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            target = root / "portal"
            for slug, document_type in (("requirements", "PRD"), ("architecture", "HLD")):
                source = root / f"{slug}.md"
                source.write_text(f"# {document_type} 示例\n\n正文。\n", encoding="utf-8")
                subprocess.run([
                    "python3", str(SCRIPT), str(source), str(target),
                    f"--slug={slug}", f"--type={document_type}",
                ], check=True)

            subprocess.run([
                "python3", str(SCRIPT), str(root / "requirements.md"), str(target),
                "--slug=requirements", "--type=PRD", "--status=已更新",
            ], check=True)

            manifest = json.loads((target / ".gainfactor-documents.json").read_text(encoding="utf-8"))
            self.assertEqual(
                {"product-requirements/requirements", "technical-design/architecture"},
                set(manifest["documents"]),
            )
            self.assertEqual("已更新", manifest["documents"]["product-requirements/requirements"]["status"])
            self.assertTrue((target / "content/docs/product-requirements/requirements.mdx").is_file())
            self.assertTrue((target / "content/docs/technical-design/architecture.mdx").is_file())
            self.assertEqual(
                {"pages": ["index", "product-requirements", "technical-design"]},
                json.loads((target / "content/docs/meta.json").read_text(encoding="utf-8")),
            )
            self.assertEqual(
                {"title": "产品需求", "pages": ["requirements"]},
                json.loads(
                    (target / "content/docs/product-requirements/meta.json").read_text(encoding="utf-8")
                ),
            )

    def test_groups_product_definition_with_product_requirements(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "product-definition.md"
            target = root / "portal"
            source.write_text("# 产品定义：示例产品\n\n正文。\n", encoding="utf-8")

            subprocess.run([
                "python3", str(SCRIPT), str(source), str(target),
                "--slug=product-definition", "--type=PRODUCT_DEFINITION",
            ], check=True)

            manifest = json.loads((target / ".gainfactor-documents.json").read_text(encoding="utf-8"))
            self.assertIn("product-requirements/product-definition", manifest["documents"])
            self.assertTrue(
                (target / "content/docs/product-requirements/product-definition.mdx").is_file()
            )


if __name__ == "__main__":
    unittest.main()
