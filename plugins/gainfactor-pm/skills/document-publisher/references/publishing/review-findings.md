# 挂载结构化评审结果

专业 Reviewer 负责生成结论；本 Skill 只校验和挂载调用方提供的 `.review.json`，没有结果时使用通用空状态，不制造问题。

挂载前按 `../../../references/document-portal-contract.md` 校验：

- 数据结构符合门户契约；
- 每个 `sectionId` 对应正文中真实存在的稳定标题 ID；
- 引用的文档 slug 与目标文档一致；
- 更新不会删除其他文档的评审数据。

通过 [`publish`](publish.md) 的公共导入命令追加 `--review=<review.json>` 写入。若只更新评审，也必须重新执行该发布流程的构建与门禁。评审挂载失败属于 `imported` 之前的失败，不能跳过后继续宣称发布完成。
