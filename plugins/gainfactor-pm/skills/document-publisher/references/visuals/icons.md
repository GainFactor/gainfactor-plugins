# Lucide 图标

门户本地集成完整 `lucide-react` 图标集合。正文使用统一的 `Icon` 或组件 `icon` 属性，不自行 import，也不引用 CDN。

```mdx
<Icon name="target" label="目标" />
<Icon name="triangle-alert" label="风险" size={20} strokeWidth={1.8} />
```

`Icon` 支持 `name`、`label`、`size`、`strokeWidth`、`color`、`className`。图标与可见文字并列时可以省略 label，此时对读屏隐藏；单独出现或表达状态时必须填写。

在 Lucide 官网按英文概念搜索，URL 最后一段即 kebab-case 名称。离线核验以门户锁定包为准：

```bash
node --input-type=module -e "import { iconNames } from 'lucide-react/dynamic'; console.log(iconNames.join('\\n'))"
```

同一文档中的同一语义保持同一图标。品牌 Logo、人物图片和产品截图使用正式资源，不用 Lucide 替代。
