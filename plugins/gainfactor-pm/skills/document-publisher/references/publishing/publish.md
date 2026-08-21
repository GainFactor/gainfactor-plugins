# 发布或更新最终文档

发布只接受已经完成的 `.md` 或 `.mdx`，以及同目录同名的可选 `.portal.json` 和调用方提供的可选 `.review.json`。不得在发布阶段改写正文语义或推导首屏内容。

需要 Python 3 执行校验与导入，需要 Node.js、`pnpm` 和 Playwright Chromium 完成构建与视觉门禁。缺少依赖时停止在实际达到的状态；不要改用另一包管理器隐式改变锁文件。

## 1. 确定门户与文档身份

从本 Skill 向上解析插件根目录。标准正式产物按 [`artifact-management`](../artifact-management.md) 使用工作区 `.gainfactor/portal`；显式指定门户或隔离评审目录时沿用该 target。不得写入非空的非 GainFactor 目录。

选择稳定 slug。目标 manifest 中相同 `sourceSlug` 或 route 已存在即为更新，否则为首次导入；两种情况使用同一流程，并保留其他文档、导航、资产和评审数据。

## 2. 校验并导入

先按 [`../validation`](../validation.md) 校验最终源文件。然后执行：

```bash
python3 <plugin-root>/scripts/create_document_portal.py \
  <document.md-or-mdx> \
  --subject-slug=<product-or-project-slug> --subject-title=<visible-title> \
  --artifact=<artifact-key> \
  --version=<version> --status=<status> \
  --owner=<owner> --updated=<YYYY-MM-DD>
```

旧文档、非标准 artifact 或隔离评审可显式传 `<portal-directory>`、`--slug`、`--type`、`--collection`、`--group` 和 `--group-title`。显式值优先于自动值。传入 presentation 时使用 `--presentation=<file>`，要求富首屏时同时使用 `--rich`；挂载已校验评审时使用 `--review=<file>`。只检查解析结果时追加 `--dry-run`。导入成功达到 `imported`。

## 3. 分阶段构建与验证

日常内容或局部样式修改，在门户目录执行类型检查、Lint 和 Quick：

```bash
pnpm run types:check
pnpm run lint
PORTAL_GATE_QUICK=1 pnpm run visual:gate
```

Quick 只覆盖 1280×800 桌面视口、明亮与暗黑主题，以及首页、组件陈列页和发布门禁页。它仍执行空白图形、图片失败、横向溢出、无效引用和组件裁切等核心规则，只缩小页面与视口范围，不能作为正式发布完成条件。

公共组件、Token、响应式或图形能力阶段完成时执行 Full：

```bash
pnpm run types:check
pnpm run lint
pnpm run build
pnpm run visual:gate
```

正式发布还必须运行 Skill 契约测试，并以 `publish:check` 重新构建后执行 Full：

```bash
python3 -m unittest discover -s <plugin-root>/scripts/tests -p 'test_document_publisher_skill.py'
pnpm run types:check
pnpm run lint
pnpm run publish:check
```

Full 自动发现全部正式文档，并固定覆盖 1920×1080 超宽屏、1280×800 普通桌面、768×1024 平板、390×844 移动端、320×720 紧凑移动端，以及明亮和暗黑主题。它必须阻止：空白或零尺寸图形、图片失败、横向溢出、无效内部引用、容器裁切和主题切换后未重绘。AntV 至少验证 `chart-bar-plain-text` 与 `relation-dagre-flow-tb-badge-card` 存在非空 SVG/Canvas 和实际图元。

构建后直接检查目标 slug 的静态产物或路由数据、导航、预期标题和本地资源，不以修改时间代替产物验证。服务正在运行时，再检查目标 URL 成功、不是 404，并包含预期标题和导航。

## 4. 报告状态

- `source-written`：最终源文件已写入。
- `imported`：正文、manifest、导航、presentation、review 和资产已更新。
- `built`：类型检查及本轮静态构建成功，目标产物存在。
- `verified`：目标页面、导航、引用、图形、图片和资源均通过门禁。
- `published`：完整流程结束；至少达到 `verified` 才能使用这一表述。

任何一步失败都停止提升状态。服务未运行时可报告“已构建并验证，预览服务未启动”，不能声称 URL 当前可访问。失败后才读取 [`troubleshooting`](troubleshooting.md)。
