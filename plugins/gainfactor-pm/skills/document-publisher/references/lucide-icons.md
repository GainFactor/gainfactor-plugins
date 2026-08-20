# Lucide 图标渠道与写法

门户本地集成 `lucide-react`，正文 MDX 和 AntV Infographic 可使用锁定版本中存在的全部 Lucide 图标，不设业务白名单，也不请求线上图标资源。

## 查找与核验渠道

1. 在 [Lucide Icons](https://lucide.dev/icons/) 按英文概念搜索并打开图标详情页。
2. 详情页 URL 最后一段就是写入名称。例如 `/icons/triangle-alert` 对应 `triangle-alert`。
3. 需要离线核验完整名称时，在门户目录执行：

   ```bash
   node --input-type=module -e "import { iconNames } from 'lucide-react/dynamic'; console.log(iconNames.join('\\n'))"
   ```

以门户锁定的本地包为最终依据；Lucide 官网新增但本地版本尚未包含的图标，需要先升级门户依赖再使用。

## 正文 MDX

源文件必须为 `.mdx`。使用统一的 `Icon`，不要自行 import `lucide-react`：

```mdx
<Icon name="target" label="目标" />
<Icon name="route" label="体验路径" size={20} />
<Icon name="triangle-alert" label="风险" color="var(--color-fd-warning)" strokeWidth={1.8} />
```

可写属性：

| 属性 | 用途 | 默认值 |
|-|-|-|
| `name` | Lucide 图标名，使用官网 URL 中的 kebab-case 名称 | 必填 |
| `label` | 图标的可访问名称；图标单独出现或表达状态时填写 | 无 |
| `size` | 图标尺寸 | `18` |
| `strokeWidth` | 线宽 | `2` |
| `color` | CSS 颜色；默认继承当前文本颜色 | `currentColor` |
| `className` | 需要与现有门户样式组合时使用 | 无 |

图标与可见文字组合时可以省略 `label`，此时图标对读屏工具隐藏；图标单独出现时必须填写 `label`。名称不存在时门户显示明确的缺失标记，便于在发布前发现拼写错误。

## AntV Infographic

Infographic DSL 的 `icon` 字段使用相同名称：

```text
data
  sequences
    - label 明确目标
      icon target
    - label 识别风险
      icon triangle-alert
    - label 推进交付
      icon rocket
```

门户从本地 Lucide 包动态载入相应 SVG。名称不存在时使用本地图标占位，不会回退到远程搜索。

## 使用原则

- 图标用于补充标题、状态、步骤、导航提示或关键概念，不替代文字、证据和结论。
- 优先选择读者熟悉的通用隐喻；同一文档中的同一语义保持一致。
- 不使用图标制造无信息增益的装饰行，也不在连续段落前机械添加图标。
- 不引用 Lucide CDN、外部 SVG URL、`unpkg` 或线上搜索接口。
- 品牌标志、产品 Logo 和人物图片不属于 Lucide 图标用途，使用正式品牌或图片资产。
