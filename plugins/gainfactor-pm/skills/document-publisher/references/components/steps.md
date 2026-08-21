# Steps / Step

线性过程统一使用 Fumadocs 原生 `Steps` 与 `Step`，不再维护独立步骤视觉组件。步骤内需要标签和值时组合 `FieldList`。

```mdx
<Steps>
  <Step>
    ### 表达约束

    用户说明日期、预算和同行人。

    <FieldList items={[
      { label: "输入", value: "自然语言" },
      { label: "完成标准", value: "系统正确复述关键约束" }
    ]} />
  </Step>
  <Step>
    ### 核验候选

    用户检查价格、库存与取消条件。
  </Step>
</Steps>
```

出现分支、回退、循环或多主体交互时改用 Mermaid。步骤旁需要截图证据时使用 `EvidenceStep`。
