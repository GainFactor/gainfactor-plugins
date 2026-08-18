import shutil
import subprocess
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
ASSET_ROOT = PLUGIN_ROOT / "assets" / "prototype-review-mode"
JS_PATH = ASSET_ROOT / "review-mode.js"
CSS_PATH = ASSET_ROOT / "review-mode.css"


class PrototypeReviewAssetsTest(unittest.TestCase):
    def test_assets_exist(self):
        self.assertTrue(JS_PATH.is_file())
        self.assertTrue(CSS_PATH.is_file())

    def test_javascript_contract_and_brand_neutrality(self):
        source = JS_PATH.read_text(encoding="utf-8")
        for marker in (
            "gainfactor-pm-prototype-review/v1",
            "#prototype-review-v1=",
            "__GAINFACTOR_PM_PROTOTYPE_REVIEW__",
            "gainfactor-pm-review-output",
            "prototypeId",
        ):
            self.assertIn(marker, source)

        for project_marker in ("GainFactor", "GF-R"):
            self.assertNotIn(project_marker, source)

    def test_assets_do_not_add_network_transports(self):
        source = JS_PATH.read_text(encoding="utf-8")
        for transport in (
            "fetch(",
            "XMLHttpRequest",
            "sendBeacon",
            "WebSocket",
        ):
            self.assertNotIn(transport, source)

    def test_css_is_namespaced(self):
        source = CSS_PATH.read_text(encoding="utf-8")
        self.assertIn(".tpr-root", source)
        self.assertIn("body.tpr-active", source)
        self.assertNotIn(".review-", source)

    def test_javascript_syntax(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node.js is not installed")
        result = subprocess.run(
            [node, "--check", str(JS_PATH)],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
