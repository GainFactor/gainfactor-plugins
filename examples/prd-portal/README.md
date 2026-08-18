# GainFactor PRD Portal

基于 Fumadocs 的 PRD 阅读原型。它验证 Markdown/MDX 内容可以获得统一目录、全文搜索、响应式阅读和静态部署能力。

## 本地运行

```bash
pnpm install
pnpm dev
```

访问 `http://localhost:3000/docs`。

## 导入现有 PRD

旧 PRD 包含 MDX 不支持的 HTML 注释追踪区。通过导入脚本从一级标题开始提取正文：

```bash
pnpm import:prd /absolute/path/to/prd.md content/docs/my-prd.mdx
```

导入后执行：

```bash
pnpm lint
pnpm types:check
pnpm build
```

`pnpm build` 会在 `out/` 生成可静态部署的站点。

## 当前边界

- 已验证 PRD 阅读、目录、搜索、Markdown 复制和移动端布局。
- 尚未实现段落评论、评审状态流转、版本 Diff 和 PDF 导出。
- 当前示例内容来自 GainFactor 教务系统 V1.0 PRD，仅用于框架验证。
