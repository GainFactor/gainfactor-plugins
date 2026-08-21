#!/usr/bin/env python3
"""Progressive-disclosure and contract checks for document-publisher."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).parent.parent.parent
SKILL_ROOT = PLUGIN_ROOT / "skills/document-publisher"
PORTAL_ROOT = PLUGIN_ROOT / "assets/document-review-portal"
LINK = re.compile(r"\[[^]]+\]\(([^)]+\.md)\)")
CUSTOM_COMPONENTS = {
    "SectionHeading": ({"title"}, {"level", "icon", "id"}),
    "PersonaBrief": ({"name"}, {"identity", "situation", "priority", "image", "traits", "facts"}),
    "FieldList": ({"items"}, {"columns", "variant"}),
    "Panel": ({"title"}, {"id", "icon", "eyebrow", "description", "children"}),
    "Board": ({"groups"}, {"label", "columns"}),
    "Citation": ({"source"}, {"children"}),
    "Source": ({"id", "children"}, set()),
    "SourceIndex": ({"children"}, {"label"}),
    "Screenshot": ({"src"}, {"title", "caption", "evidenceId", "device", "step", "maxHeight"}),
    "ScreenshotGallery": ({"children"}, {"columns", "layout"}),
    "EvidenceStep": ({"step", "title"}, {"id", "children", "evidence"}),
}
CUSTOM_ENUMS = {
    "SectionHeading": {"level": {2, 3, 4}},
    "FieldList": {
        "columns": {1, 2, 3, 4, "auto"},
        "variant": {"plain", "grid"},
        "items[].span": {1, 2, "full"},
    },
    "Board": {
        "columns": {1, 2, 3, "auto"},
        "groups[].tone": {"neutral", "info", "warning", "critical"},
    },
    "Screenshot": {"device": {"desktop", "tablet", "mobile"}},
    "ScreenshotGallery": {"columns": {1, 2, 3}, "layout": {"grid", "rail"}},
}
COMPONENT_REFERENCES = {
    "SectionHeading": "section-heading.md",
    "PersonaBrief": "persona-brief.md",
    "FieldList": "field-list.md",
    "Panel": "panel.md",
    "Board": "board.md",
    "Citation": "citations.md",
    "Source": "citations.md",
    "SourceIndex": "citations.md",
    "Screenshot": "screenshots.md",
    "ScreenshotGallery": "screenshots.md",
    "EvidenceStep": "screenshots.md",
}


class DocumentPublisherSkillTest(unittest.TestCase):
    def test_entry_is_a_shortcut_router(self) -> None:
        entry = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(entry.splitlines()), 60)
        routes = LINK.findall(entry)
        self.assertTrue(routes)
        self.assertTrue(all((SKILL_ROOT / route).is_file() for route in routes))

    def test_all_local_markdown_links_resolve(self) -> None:
        files = [SKILL_ROOT / "SKILL.md", *sorted((SKILL_ROOT / "references").rglob("*.md"))]
        for source in files:
            for target in LINK.findall(source.read_text(encoding="utf-8")):
                with self.subTest(source=source.name, target=target):
                    self.assertTrue((source.parent / target).resolve().is_file())

    def test_removed_monolithic_references_do_not_return(self) -> None:
        removed = {
            "authoring-contract.md", "capabilities.md", "expression-design.md",
            "generic-report-components.md", "lucide-icons.md", "publish-workflow.md", "tool-catalog.md",
        }
        self.assertFalse(removed & {path.name for path in (SKILL_ROOT / "references").glob("*.md")})

    def test_publishing_lifecycle_is_owned_by_document_publisher(self) -> None:
        publishing = SKILL_ROOT / "references/publishing"
        self.assertEqual(
            {"publish.md", "review-findings.md", "preview.md", "troubleshooting.md"},
            {path.name for path in publishing.glob("*.md")},
        )
        retired_skill = "document-" + "review"
        self.assertFalse((PLUGIN_ROOT / "skills" / retired_skill).exists())

    def test_source_validation_does_not_build_the_portal(self) -> None:
        validation = (SKILL_ROOT / "references/validation.md").read_text(encoding="utf-8")
        self.assertNotIn("run build", validation)
        self.assertNotIn("publish:check", validation)

    def test_publish_uses_the_portal_package_manager_and_visual_gate(self) -> None:
        publish = (SKILL_ROOT / "references/publishing/publish.md").read_text(encoding="utf-8")
        self.assertIn("pnpm run types:check", publish)
        self.assertIn("pnpm run publish:check", publish)
        self.assertNotIn("npm run ", publish.replace("pnpm run ", ""))

    def test_visual_gate_covers_exactly_five_viewports_two_themes_and_quick_mode(self) -> None:
        gate = (PORTAL_ROOT / "scripts/visual-release-gate.mjs").read_text(encoding="utf-8")
        viewports = set(re.findall(r"name:\s*['\"]([^'\"]+)['\"]", gate))
        self.assertEqual({"wide", "desktop", "tablet", "mobile", "compact"}, viewports)
        self.assertRegex(gate, r"\[['\"]light['\"],\s*['\"]dark['\"]\]")
        self.assertIn("PORTAL_GATE_QUICK", gate)
        self.assertIn("[allViewports[1]]", gate)

    def test_publishing_docs_define_staged_quick_and_full_gates(self) -> None:
        publish = (SKILL_ROOT / "references/publishing/publish.md").read_text(encoding="utf-8")
        preview = (SKILL_ROOT / "references/publishing/preview.md").read_text(encoding="utf-8")
        for expected in ("320", "390", "768", "1280", "1920", "PORTAL_GATE_QUICK=1", "pnpm run visual:gate"):
            with self.subTest(expected=expected):
                self.assertIn(expected, publish)
        self.assertIn("PORTAL_GATE_QUICK=1", preview)
        self.assertIn("pnpm run visual:gate", preview)

    def test_custom_components_publish_machine_readable_props(self) -> None:
        registry = json.loads((PORTAL_ROOT / "portal-capabilities.json").read_text(encoding="utf-8"))
        tools = {item["component"]: item for item in registry["contentTools"] if item.get("component")}
        for component, (required, optional) in CUSTOM_COMPONENTS.items():
            with self.subTest(component=component):
                self.assertIn("props", tools[component])
                self.assertEqual(required, set(tools[component]["props"].get("required", [])))
                self.assertEqual(optional, set(tools[component]["props"].get("optional", [])))

    def test_custom_component_enums_match_the_machine_contract(self) -> None:
        registry = json.loads((PORTAL_ROOT / "portal-capabilities.json").read_text(encoding="utf-8"))
        tools = {item["component"]: item for item in registry["contentTools"] if item.get("component")}
        for component, expected_enums in CUSTOM_ENUMS.items():
            actual_enums = tools[component]["props"].get("enums", {})
            with self.subTest(component=component):
                self.assertEqual(set(expected_enums), set(actual_enums))
                for prop, values in expected_enums.items():
                    self.assertEqual(values, set(actual_enums[prop]))

    def test_component_references_cover_every_public_prop(self) -> None:
        for component, (required, optional) in CUSTOM_COMPONENTS.items():
            reference = SKILL_ROOT / "references/components" / COMPONENT_REFERENCES[component]
            text = reference.read_text(encoding="utf-8")
            with self.subTest(component=component):
                self.assertIn(component, text)
                for prop in required | optional:
                    self.assertRegex(text, rf"\b{re.escape(prop)}\b")

    def test_component_reference_exists_for_each_custom_authoring_tool(self) -> None:
        registry = json.loads((PORTAL_ROOT / "portal-capabilities.json").read_text(encoding="utf-8"))
        documented = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((SKILL_ROOT / "references/components").glob("*.md"))
        )
        for item in registry["contentTools"]:
            if item.get("origin") != "gainfactor":
                continue
            self.assertIn(item["component"], documented)

    def test_public_docs_and_examples_do_not_use_removed_components(self) -> None:
        registry = json.loads((PORTAL_ROOT / "portal-capabilities.json").read_text(encoding="utf-8"))
        removed = set(registry["removedComponents"])
        files = [
            PLUGIN_ROOT / "README.md",
            SKILL_ROOT / "SKILL.md",
            *sorted((SKILL_ROOT / "references").rglob("*.md")),
        ]
        for source in files:
            text = source.read_text(encoding="utf-8")
            for component in removed:
                with self.subTest(source=source.name, component=component):
                    self.assertNotRegex(text, rf"<{re.escape(component)}\b")
        readme = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("`Profile`", readme)

    def test_upstream_skills_only_reference_current_shortcuts(self) -> None:
        retired = {"publish-create", "publish-update", "preview-and-gate"}
        upstream_files = [
            PLUGIN_ROOT / "skills/define-product/SKILL.md",
            PLUGIN_ROOT / "skills/user-persona/SKILL.md",
            PLUGIN_ROOT / "skills/product-metrics/SKILL.md",
            PLUGIN_ROOT / "skills/competitive-analysis/SKILL.md",
        ]
        for source in upstream_files:
            text = source.read_text(encoding="utf-8")
            for shortcut in retired:
                with self.subTest(source=source.name, shortcut=shortcut):
                    self.assertNotIn(shortcut, text)

    def test_portal_skills_use_stable_product_artifact_paths(self) -> None:
        expected = {
            "define-product": "docs/gainfactor/{product-slug}/product-definition.mdx",
            "user-persona": "docs/gainfactor/{product-slug}/user-persona.mdx",
            "competitive-analysis": "docs/gainfactor/{product-slug}/competitive-analysis.mdx",
            "product-metrics": "docs/gainfactor/{product-slug}/product-metrics.mdx",
        }
        for skill, path in expected.items():
            files = [
                PLUGIN_ROOT / f"skills/{skill}/SKILL.md",
                *sorted((PLUGIN_ROOT / f"skills/{skill}/references").glob("*.md")),
            ]
            documented = "\n".join(file.read_text(encoding="utf-8") for file in files)
            with self.subTest(skill=skill):
                self.assertIn(path, documented)
                self.assertNotIn("{产品名}-{YYYYMMDD}", documented)

    def test_artifact_management_is_a_routed_reference(self) -> None:
        entry = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        management = SKILL_ROOT / "references/artifact-management.md"
        self.assertTrue(management.is_file())
        self.assertIn("references/artifact-management.md", entry)
        text = management.read_text(encoding="utf-8")
        for expected in (
            "docs/gainfactor/{product-slug}/",
            ".gainfactor/portal",
            "assets/{artifact-key}/",
            ".work/",
            "product-definition",
            "user-persona",
            "competitive-analysis",
            "product-metrics",
        ):
            self.assertIn(expected, text)

    def test_retired_document_review_skill_has_no_routes(self) -> None:
        retired = "document-" + "review"
        self.assertFalse((PLUGIN_ROOT / "skills" / retired).exists())
        public_files = [
            PLUGIN_ROOT / "README.md",
            PLUGIN_ROOT / "skills/guide/SKILL.md",
            PLUGIN_ROOT / "skills/guide/references/workflow-map.yaml",
            SKILL_ROOT / "SKILL.md",
            *sorted((SKILL_ROOT / "references").rglob("*.md")),
        ]
        for source in public_files:
            with self.subTest(source=source.name):
                text = source.read_text(encoding="utf-8")
                self.assertNotIn(f"${retired}", text)
                self.assertNotIn(f"skills/{retired}", text)


if __name__ == "__main__":
    unittest.main()
