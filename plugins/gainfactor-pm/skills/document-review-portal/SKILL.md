---
name: document-review-portal
description: Create or extend a local GainFactor reading and review portal for Markdown or MDX documents such as product definitions, BRD, PRD, HLD, LLD, test strategy, and runbooks. Use when the user asks to display, browse, preview, or review one or more documents in the shared portal UI.
---

# 文档阅读与评审门户

把用户指定的 Markdown/MDX 文档加入统一的本地文档门户。门户负责文档导航、章节目录、搜索、Mermaid 阅读和评审问题定位，不负责生成或改写文档内容。

## 工作方式

1. 确认用户要加入的文档路径、文档类型和目标门户目录。未指定目标时创建独立临时目录，不写入用户项目。
2. 从当前 `SKILL.md` 向上解析 `gainfactor-pm` 插件根目录。
3. 为每份文档选择稳定且不冲突的 URL slug。追加到已有门户时保留原有文档，不重新初始化。生成器会按文档类型自动归入“产品需求 / 技术设计 / 质量与交付 / 其他文档”一级分组，文档作为二级条目展示。
4. 执行公共生成器：

   ```bash
   python3 <gainfactor-pm-plugin-root>/scripts/create_document_portal.py \
     <document.md> <portal-directory> \
     --slug=<stable-slug> \
     --type=<Product-Definition|BRD|PRD|HLD|LLD|Test-Strategy|Runbook|其他> \
     --collection=<文档集合名称> \
     --version=<版本> --status=<状态> --owner=<负责人> --updated=<YYYY-MM-DD>
   ```

5. 有结构化评审结果时，按 `../../references/document-portal-contract.md` 生成 JSON，并追加 `--review=<review.json>`。没有评审结果时使用通用空状态，不制造问题。
6. 只有用户要求预览或打开页面时，才在门户目录安装锁定依赖并启动本地服务，然后提供 URL。

## 约束

- 页面正文只能来自用户本轮指定的文档。
- 公共模板中不得加入业务 Mock、示例评审结论或项目专属正文。
- 同一目标目录可以持续追加不同类型文档；相同 slug 表示明确更新该文档。
- 自动分组不合适时可用 `--group=<product-requirements|technical-design|quality-delivery|other>` 覆盖。
- 不覆盖非 GainFactor 文档门户的非空目录。
- 评审问题的 `sectionId` 必须对应该文档中真实存在的标题 ID。
