#!/usr/bin/env python3
"""Regression test for the bundled PRD review portal scaffold."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
import json
from pathlib import Path


SCRIPT = Path(__file__).with_name("create_review_portal.py")


class CreateReviewPortalTest(unittest.TestCase):
    def test_imports_only_the_requested_prd_and_metadata(self) -> None:
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
                    "--version=V2.1",
                    "--status=评审中",
                    "--owner=产品团队",
                    "--updated=2026-08-18",
                    f"--review={review}",
                ],
                check=True,
            )

            generated = (target / "content/docs/prd.mdx").read_text(encoding="utf-8")
            metadata = (target / "lib/document-meta.ts").read_text(encoding="utf-8")
            review_data = (target / "lib/review-data.generated.ts").read_text(encoding="utf-8")
            self.assertIn('title: "示例 PRD：结算流程"', generated)
            self.assertIn("这是本轮测试文档。", generated)
            self.assertIn('"version": "V2.1"', metadata)
            self.assertIn('"status": "评审中"', metadata)
            self.assertIn('"conclusion": "有条件通过"', review_data)
            self.assertIn('"sectionId": "一版本说明"', review_data)
            self.assertIn('"sectionTitle": "一、版本说明"', review_data)
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

            subprocess.run(["python3", str(SCRIPT), str(source), str(target)], check=True)

            generated = (target / "content/docs/prd.mdx").read_text(encoding="utf-8")
            self.assertIn('title: "仅 Frontmatter 的 PRD"', generated)
            self.assertIn("正文。", generated)


if __name__ == "__main__":
    unittest.main()
