---
name: document-review
description: Mount completed GainFactor Markdown or MDX artifacts into a local shared reading and review portal, manage stable document identity and navigation, attach structured review findings, and run or inspect the portal. Use when documents are ready to browse, preview, or review. Content authoring, visual design, and portal-format decisions belong to document-publisher.
---

# 文档阅读与评审

把已经完成并符合门户契约的 Markdown/MDX 文档挂载到统一的本地门户，管理文档身份、导航、评审数据与预览环境。本 Skill 不生成、改写或美化正文。

## 与 document-publisher 的边界

- `$document-publisher` 定义表达决策、已注册工具、Markdown/MDX 写入契约、Portal Presentation 和发布前校验。
- `$document-review` 选择或发现门户实例，把合格产物导入或更新到该实例，挂载评审结果，并检查阅读环境。
- 本 Skill 不从标题或正文推导组件、信息图、首屏模块或 presentation manifest；缺失这些产物时也不代写。
- 若源文档还没有完成表达设计，返回上游内容 Skill 使用 `$document-publisher` 完成，而不是在导入阶段补救。

## 输入

至少需要最终 `.md` 或 `.mdx` 路径。复用上游已经给出的值，不重复确认：

- 稳定 slug、artifact type、collection 和目标门户目录；
- 与正文同名的可选 `.portal.json`；
- 可选结构化评审 `.review.json`；
- 版本、状态、负责人和更新时间等文档元数据。

正文同目录存在同名 `.portal.json` 时默认作为配套产物处理，不要求用户再次确认。它必须由上游明确写出；不得从正文自动生成。

## 工作方式

1. 确认最终源文件，并检查同名 `.portal.json`。源文件或 manifest 仍在编辑、含占位内容或明显不是最终格式时停止导入并指出具体问题。
2. 从当前 `SKILL.md` 向上解析 `gainfactor-pm` 插件根目录。
3. 按 `$document-publisher` 的发布前协议校验源文件；存在 presentation 时执行：

   ```bash
   python3 <gainfactor-pm-plugin-root>/scripts/compile_portal_document.py \
     <document.md-or-mdx> --presentation=<document.portal.json> --validate
   ```

4. 优先使用任务中已知的 GainFactor 门户；否则寻找当前工作区已有的 GainFactor 门户。只有没有可复用实例时才创建新的门户目录，且不得写入非 GainFactor 的非空目录。
5. 为文档选择稳定且不冲突的 slug。相同 slug 表示更新；追加时保留门户内既有文档、评审数据和导航。
6. 执行公共导入器：

   ```bash
   python3 <gainfactor-pm-plugin-root>/scripts/create_document_portal.py \
     <document.md-or-mdx> <portal-directory> \
     --slug=<stable-slug> \
     --type=<artifact-type> \
     --collection=<文档集合名称> \
     --version=<版本> --status=<状态> --owner=<负责人> --updated=<YYYY-MM-DD>
   ```

   同名 presentation 已存在时由导入流程载入；不得在此步骤重新解释正文。自动归类不合适时使用导入器支持的 `--group` 覆盖。
7. 有结构化评审结果时，按 `../../references/document-portal-contract.md` 校验后附加 `--review=<review.json>`。没有评审结果时使用通用空状态，不制造问题。
8. 运行与变更范围相称的验证。至少检查导入成功和文档清单；涉及组件或模板变更时再执行门户类型检查或构建。
9. 每次导入都会在门户根目录安装或更新 `打开文档门户.command` 与 `关闭文档门户.command`。用户可以脱离 AI 双击使用；首次打开或内容变化时启动器自动安装锁定依赖并构建，之后复用静态构建与已运行服务。
10. 用户在当前会话要求打开、预览或评审时，执行同一启动器并提供 URL。检查首屏、导航、目录、正文、图片、图表、移动端和评审问题定位。

## 约束

- 页面正文只能来自本轮指定的最终文档；presentation 只能来自配套 manifest。
- 公共模板中不得加入业务 Mock、示例评审结论或项目专属正文。
- 同一目标目录可持续追加不同类型文档；不得为了单篇更新重新初始化整个门户。
- `review.json` 的 `sectionId` 必须对应正文真实存在的标题 ID。
- 不复制 `$document-publisher` 的工具目录或表达规则；通过其契约保持单一来源。
- 导入失败时报告校验或兼容性问题，不通过手工修改已生成页面绕过源产物问题。
- 启动器只监听 `127.0.0.1`，运行状态与日志保存在可删除的 `.portal-runtime/`；不得默认暴露到局域网。
