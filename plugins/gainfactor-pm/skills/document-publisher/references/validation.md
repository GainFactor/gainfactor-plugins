# 文档验证

根据当前任务执行需要的层级，不预读组件手册。

## 格式与引用

```bash
python3 <plugin-root>/scripts/compile_portal_document.py \
  <document.md-or-mdx> --presentation=<document.portal.json> --validate
```

未使用 presentation 时省略该参数。纯标准 Markdown 文档可以使用 `.md`；只要使用任何注册组件，最终源文件就必须使用 `.mdx`。校验会阻止无效 manifest、重复来源、无目标引用、孤立来源和已经删除的旧组件；错误会包含组件名、位置与替换建议。

本 Shortcut 到这里结束，不运行门户类型检查、构建或视觉门禁。需要形成可发布门户时进入 [`publishing/publish`](publishing/publish.md)。
