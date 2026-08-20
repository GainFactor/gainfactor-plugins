#!/usr/bin/env python3
"""Tests for generic portal presentation compilation."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "compile_portal_document.py"
PORTAL_ROOT = SCRIPT.parent.parent / "assets/document-review-portal"


class CompilePortalDocumentTest(unittest.TestCase):
    def test_registered_content_components_exist_in_mdx_context(self) -> None:
        registry = json.loads((PORTAL_ROOT / "portal-capabilities.json").read_text(encoding="utf-8"))
        mdx_context = (PORTAL_ROOT / "components/mdx.tsx").read_text(encoding="utf-8")
        registered_components = {
            item["component"] for item in registry["contentTools"] if item["component"]
        }
        for component in registered_components:
            self.assertRegex(mdx_context, rf"\b{component},")

    def test_antv_infographic_is_version_locked_and_local_only(self) -> None:
        registry = json.loads((PORTAL_ROOT / "portal-capabilities.json").read_text(encoding="utf-8"))
        package = json.loads((PORTAL_ROOT / "package.json").read_text(encoding="utf-8"))
        component = (PORTAL_ROOT / "components/infographic.tsx").read_text(encoding="utf-8")
        capability = next(item for item in registry["contentTools"] if item["id"] == "antv-infographic")
        self.assertEqual(capability["version"], package["dependencies"]["@antv/infographic"])
        self.assertEqual("local-only", capability["network"])
        self.assertNotIn("https://", component)
        self.assertNotIn("unpkg", component)
        self.assertIn("registerResourceLoader", component)
        self.assertIn("font.fontWeight = {}", component)
        self.assertIn("ref:(?:url|remote|search)", component)

    def test_mermaid_measurement_nodes_remain_laid_out_during_render(self) -> None:
        styles = (PORTAL_ROOT / "app/global.css").read_text(encoding="utf-8")
        component = (PORTAL_ROOT / "components/mermaid.tsx").read_text(encoding="utf-8")
        self.assertNotIn("body > div[id^='dmermaid-']", styles)
        self.assertNotIn("body > svg[id^='mermaid-']", styles)
        self.assertIn("cleanupMermaidArtifacts", component)

    def test_lucide_icons_are_registered_without_a_business_allowlist(self) -> None:
        registry = json.loads((PORTAL_ROOT / "portal-capabilities.json").read_text(encoding="utf-8"))
        capability = next(item for item in registry["contentTools"] if item["id"] == "lucide-icon")
        icon_component = (PORTAL_ROOT / "components/lucide-icon.tsx").read_text(encoding="utf-8")
        infographic = (PORTAL_ROOT / "components/infographic.tsx").read_text(encoding="utf-8")
        self.assertEqual("all", capability["coverage"])
        self.assertEqual("local-only", capability["network"])
        self.assertIn("iconNames", icon_component)
        self.assertIn("dynamicIconImports", infographic)

    def test_generic_report_components_are_registered_with_fallbacks(self) -> None:
        registry = json.loads((PORTAL_ROOT / "portal-capabilities.json").read_text(encoding="utf-8"))
        tools = {item["id"]: item for item in registry["contentTools"]}
        for tool_id in ("profile", "info-grid", "structured-steps", "content-panel", "grouped-board"):
            self.assertEqual("registered", tools[tool_id]["status"])
            self.assertTrue(tools[tool_id]["fallback"])
        components = (PORTAL_ROOT / "components/document-blocks.tsx").read_text(encoding="utf-8")
        styles = (PORTAL_ROOT / "app/global.css").read_text(encoding="utf-8")
        for component in ("Profile", "InfoGrid", "StructuredSteps", "ContentPanel", "GroupedBoard"):
            self.assertIn(f"function {component}", components)
        self.assertIn("@media print", styles)
        self.assertIn(".gf-profile", styles)
        self.assertIn(".gf-grouped-board", styles)
        self.assertNotIn("P0", components)
        self.assertNotIn("P1", components)
        self.assertNotIn("P2", components)

    def test_compiles_generic_modules_and_resolves_imported_image(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            document = root / "report.mdx"
            manifest = root / "report.portal.json"
            document.write_text("# 研究报告\n\n![赵宁](/document-assets/report/zhao.png)\n", encoding="utf-8")
            manifest.write_text(json.dumps({
                "schemaVersion": 1,
                "layout": "report",
                "modules": [
                    {"id": "summary", "type": "metrics", "items": [{"label": "核心用户", "value": "低负担启动型"}]},
                    {"id": "people", "type": "cards", "items": [{"title": "赵宁", "sourceImageAlt": "赵宁"}]},
                    {"id": "path", "type": "steps", "items": [{"content": "表达约束"}]},
                ],
            }, ensure_ascii=False), encoding="utf-8")
            completed = subprocess.run([
                "python3", str(SCRIPT), str(document), f"--presentation={manifest}", "--validate",
            ], check=True, capture_output=True, text=True)
            presentation = json.loads(completed.stdout)["presentation"]
            self.assertEqual("report", presentation["layout"])
            self.assertEqual(3, len(presentation["modules"]))
            self.assertEqual("/document-assets/report/zhao.png", presentation["modules"][1]["items"][0]["image"])

    def test_profile_image_alt_is_available_as_a_source_image(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            document = root / "report.mdx"
            manifest = root / "report.portal.json"
            document.write_text(
                '<Profile name="赵宁" image={{ alt: "赵宁人物画像", src: "/document-assets/report/zhao.png" }} />\n',
                encoding="utf-8",
            )
            manifest.write_text(json.dumps({
                "schemaVersion": 1,
                "layout": "report",
                "modules": [{
                    "id": "people",
                    "type": "cards",
                    "items": [{"title": "赵宁", "sourceImageAlt": "赵宁人物画像"}],
                }],
            }, ensure_ascii=False), encoding="utf-8")
            completed = subprocess.run(
                ["python3", str(SCRIPT), str(document), f"--presentation={manifest}", "--validate"],
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)
            self.assertEqual([], payload["errors"])
            self.assertEqual(
                "/document-assets/report/zhao.png",
                payload["presentation"]["modules"][0]["items"][0]["image"],
            )

    def test_card_source_image_alt_resolves_a_profile_image(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            document = root / "report.mdx"
            manifest = root / "report.portal.json"
            document.write_text(
                '<Profile name="赵宁" image={{ src: "/document-assets/report/zhao.png", alt: "赵宁人物画像" }} />\n',
                encoding="utf-8",
            )
            manifest.write_text(json.dumps({
                "schemaVersion": 1,
                "layout": "report",
                "modules": [{
                    "id": "people",
                    "type": "cards",
                    "items": [{"title": "赵宁", "sourceImageAlt": "赵宁人物画像"}],
                }],
            }, ensure_ascii=False), encoding="utf-8")
            completed = subprocess.run(
                ["python3", str(SCRIPT), str(document), f"--presentation={manifest}", "--validate"],
                check=True,
                capture_output=True,
                text=True,
            )
            card = json.loads(completed.stdout)["presentation"]["modules"][0]["items"][0]
            self.assertEqual("/document-assets/report/zhao.png", card["image"])
            self.assertEqual("赵宁人物画像", card["imageAlt"])

    def test_rejects_ambiguous_alt_across_markdown_and_profile_images(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            document = root / "report.mdx"
            manifest = root / "report.portal.json"
            document.write_text(
                '![代表人物](/document-assets/report/first.png)\n\n'
                '<Profile name="示例" image={{ src: "/document-assets/report/second.png", alt: "代表人物" }} />\n',
                encoding="utf-8",
            )
            manifest.write_text(json.dumps({
                "schemaVersion": 1,
                "layout": "report",
                "modules": [{
                    "id": "people",
                    "type": "cards",
                    "items": [{"title": "示例", "sourceImageAlt": "代表人物"}],
                }],
            }, ensure_ascii=False), encoding="utf-8")
            completed = subprocess.run(
                ["python3", str(SCRIPT), str(document), f"--presentation={manifest}", "--validate"],
                capture_output=True,
                text=True,
            )
            self.assertEqual(1, completed.returncode)
            self.assertIn("sourceImageAlt 对应多个不同图片", completed.stdout)

    def test_duplicate_alt_with_the_same_src_is_not_ambiguous(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            document = root / "report.mdx"
            manifest = root / "report.portal.json"
            src = "/document-assets/report/person.png"
            document.write_text(
                f'![代表人物]({src})\n\n<Profile name="示例" image={{{{ src: "{src}", alt: "代表人物" }}}} />\n',
                encoding="utf-8",
            )
            manifest.write_text(json.dumps({
                "schemaVersion": 1,
                "layout": "report",
                "modules": [{
                    "id": "people",
                    "type": "cards",
                    "items": [{"title": "示例", "sourceImageAlt": "代表人物"}],
                }],
            }, ensure_ascii=False), encoding="utf-8")
            completed = subprocess.run(
                ["python3", str(SCRIPT), str(document), f"--presentation={manifest}", "--validate"],
                check=True,
                capture_output=True,
                text=True,
            )
            card = json.loads(completed.stdout)["presentation"]["modules"][0]["items"][0]
            self.assertEqual(src, card["image"])

    def test_validation_rejects_unknown_module(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            document = root / "report.md"
            manifest = root / "report.portal.json"
            document.write_text("# 报告\n", encoding="utf-8")
            manifest.write_text('{"schemaVersion":1,"layout":"report","modules":[{"id":"x","type":"persona"}]}', encoding="utf-8")
            completed = subprocess.run([
                "python3", str(SCRIPT), str(document), f"--presentation={manifest}", "--validate",
            ], capture_output=True, text=True)
            self.assertEqual(1, completed.returncode)
            self.assertIn("type 不受支持", completed.stdout)

    def test_plain_markdown_needs_no_presentation_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            document = Path(temporary_directory) / "doc.md"
            document.write_text("# 普通文档\n", encoding="utf-8")
            completed = subprocess.run(["python3", str(SCRIPT), str(document)], check=True, capture_output=True, text=True)
            self.assertEqual([], json.loads(completed.stdout)["presentation"]["modules"])


if __name__ == "__main__":
    unittest.main()
