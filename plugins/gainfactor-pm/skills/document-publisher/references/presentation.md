# Portal Presentation v1

`.portal.json` 是可选首屏摘要，不替代正文。没有明显首屏收益时不生成。

```json
{"schemaVersion":1,"layout":"report","modules":[]}
```

`layout`：`document | report | reference`。模块只允许：

- `metrics`：2–4 个关键数字或短判断；items 支持 `label`、`value`、可选 `note`、`change`、`definition`、`source`。
- `cards`：同构对象概览；支持 `title`、`eyebrow`、`description`、`quote`、`fields`、`image`。
- `steps`：正文已有的线性阶段；`items: [{title?, content}]`。
- `callout`：一个关键结论或边界；支持 `tone: info | success | warning`。

卡片可用 `sourceImageAlt` 映射正文 Markdown 图片或 `PersonaBrief.image.alt`。相同 alt 指向不同资源时校验失败；显式 `cards.image` 不依赖此映射。首屏不得引入正文中不存在的事实。

完成后运行 [`validation`](validation.md)。
