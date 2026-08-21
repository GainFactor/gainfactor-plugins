# PersonaBrief

`PersonaBrief` 是用户画像章节开头的人物导读，帮助读者在进入背景、行为和决策分析前，快速识别人物、当前处境和必要事实。它不是通用主体卡片，不用于公司、产品或案例，也不包裹后续画像正文。

```ts
type PersonaBriefProps = {
  name: string
  identity?: string
  situation?: string
  priority?: string
  image?: { src: string; alt: string }
  traits?: string[]
  facts?: Array<{ label: string; value: ReactNode; span?: 1 | 2 | "full" }>
}
```

```mdx
<SectionHeading level={3} id="persona-zhao-ning" icon="user-round" title="1 赵宁" />
<PersonaBrief
  name="赵宁"
  identity="视觉设计师"
  priority="核心用户"
  situation="假期临近，但没有时间制作完整攻略。"
  image={{ src: "./assets/zhao.png", alt: "赵宁正在核验短途旅行候选" }}
  traits={["体验优先", "少量候选", "可取消"]}
  facts={[
    { label: "年龄", value: "29 岁" },
    { label: "地区", value: "成都" },
    { label: "同行人", value: "伴侣" },
    { label: "预算", value: "6000 元" }
  ]}
/>
```

人物章节的稳定锚点和目录标题由紧邻在前的 `SectionHeading` 承担。`facts` 只写短事实；长内容进入后续正文或分节。图片的 `src` 与非空 `alt` 都必填，相对资源由导入器搬运。
