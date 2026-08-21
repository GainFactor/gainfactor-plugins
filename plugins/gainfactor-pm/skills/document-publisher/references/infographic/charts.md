# Charts

图表使用 `values`，每个数据点包含 `label` 与数值 `value`：

- 单组横向比较：`chart-bar-plain-text`
- 单组纵向比较：`chart-column-simple`
- 单条有序趋势：`chart-line-plain-text`
- 占比：`chart-pie-*`
- 词频主题：`chart-wordcloud`

```infographic
infographic chart-bar-plain-text
data
  title 完成率
  values
    - label 方案 A
      value 68
    - label 方案 B
      value 91
```

`value` 尽量保持纯数值，单位放在 label 或 desc。图表不代替正文中的精确数据表、口径和来源。
