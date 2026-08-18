#!/usr/bin/env python3
"""Create a disposable PRD review portal from the bundled UI template."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "prd-review-portal"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prd", type=Path, help="PRD Markdown file")
    parser.add_argument("target", type=Path, help="Empty output directory")
    parser.add_argument("--version", default="")
    parser.add_argument("--status", default="待评审")
    parser.add_argument("--owner", default="未指定")
    parser.add_argument("--updated", default="")
    parser.add_argument("--review", type=Path, help="Optional structured review JSON")
    args = parser.parse_args()

    prd = args.prd.resolve()
    target = args.target.resolve()
    if not prd.is_file():
        parser.error(f"PRD file does not exist: {prd}")
    if target.exists() and any(target.iterdir()):
        parser.error(f"Target directory must be empty: {target}")

    shutil.copytree(TEMPLATE_ROOT, target, dirs_exist_ok=True)
    command = [
        "node",
        "scripts/import-prd.mjs",
        str(prd),
        "content/docs/prd.mdx",
        f"--status={args.status}",
        f"--owner={args.owner}",
    ]
    if args.version:
        command.append(f"--version={args.version}")
    if args.updated:
        command.append(f"--updated={args.updated}")
    subprocess.run(command, cwd=target, check=True)
    if args.review:
        review_path = args.review.resolve()
        if not review_path.is_file():
            parser.error(f"Review JSON does not exist: {review_path}")
        review = json.loads(review_path.read_text(encoding="utf-8"))
        if not isinstance(review.get("conclusion"), str) or not isinstance(review.get("issues"), list):
            parser.error("Review JSON must contain a string conclusion and an issues array")
        for issue in review["issues"]:
            required = ("id", "severity", "title", "sectionId")
            if not isinstance(issue, dict) or any(not isinstance(issue.get(key), str) for key in required):
                parser.error(f"Each review issue must contain string fields: {', '.join(required)}")
            if issue["severity"] not in {"P0", "P1", "P2"}:
                parser.error("Review issue severity must be P0, P1, or P2")
        output = f"export const reviewData = {json.dumps(review, ensure_ascii=False, indent=2)} as {{ conclusion: string; issues: Array<{{ id: string; severity: 'P0' | 'P1' | 'P2'; title: string; sectionId: string; sectionTitle?: string; suggestion?: string }}> }};\n"
        (target / "lib/review-data.generated.ts").write_text(output, encoding="utf-8")
        (target / "lib/review-data.ts").write_text(
            "export type ReviewSeverity = 'P0' | 'P1' | 'P2';\n"
            "export type ReviewIssue = { id: string; severity: ReviewSeverity; title: string; sectionId: string; sectionTitle?: string; suggestion?: string };\n"
            "export { reviewData } from './review-data.generated';\n",
            encoding="utf-8",
        )
    print(f"Created PRD review portal: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
