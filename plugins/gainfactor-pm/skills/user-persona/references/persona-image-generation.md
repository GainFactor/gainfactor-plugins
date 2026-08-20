# Persona 人物图片生成

每个保留 Persona 生成一张人物图片，用于帮助读者快速建立对人物处境、生活环境和行为气质的整体印象。图片是 Persona 档案的组成部分，必须在 Persona 内容稳定后生成，不能先看图片再反向补写人物。

## 生成时机与工具

1. 完成人物背景、典型情境、核心目标、关键行为、核心痛点、决策与信任因素和期望产品功能，并通过画像内容门禁。
2. 从 Persona 中提取确实影响画面的信息，不补写与人物无关的身份特征。
3. 默认使用内置 `image_gen` 生成；每个 Persona 单独调用一次。
4. 检查人物年龄感、职业或生活状态、环境、情绪、动作和整体风格是否与 Persona 一致。不一致时只针对冲突项迭代。
5. 将最终图片移入当前项目，通过人物档案与表达门禁后再写入报告；不得让项目引用的图片只停留在 `$CODEX_HOME/generated_images`。

若当前宿主没有可用的图片生成能力，报告中说明人物图片待生成，不插入不存在的文件路径；其余画像研究可以正常交付。

## 默认视觉方向

- 使用 `photorealistic-natural`，生成自然纪实、编辑摄影感的人物环境肖像。
- 默认采用竖版 4:5 构图，以半身或带环境的中景为主；人物是明确主体，背景能解释现实处境但不过度抢夺注意力。
- 使用自然光、真实皮肤和衣物纹理、日常环境与克制表情，避免广告大片、证件照、影棚写真或过度精修质感。
- 多个 Persona 保持一致的摄影语言、色彩克制程度、画幅和完成度，但人物、环境、动作和情绪必须体现各自差异。
- 图片中不放文字、标签、品牌 Logo、水印、UI、统计图或装饰边框。
- 不使用夸张道具、刻板服装或外貌符号代替职业、地区、年龄和性格；行为差异优先通过情境、动作、注意力和环境表现。
- 不复制真实公众人物或将 Persona 设计成可识别的真实个人。

## Prompt 结构

使用以下结构组织每张图的提示词，只填写 Persona 已经给出的信息：

```text
Use case: photorealistic-natural
Asset type: USER_PERSONA report portrait
Primary request: 为 Persona「姓名」生成自然纪实的人物环境肖像
Scene/backdrop: Persona 的典型生活或工作环境
Subject: 年龄感、职业或生活状态、服装、姿态、正在进行的自然动作
Behavioral cues: 最重要的行为习惯、注意力方向、现实约束和情绪状态
Style/medium: photorealistic candid editorial photography, realistic skin and fabric texture
Composition/framing: vertical 4:5 environmental portrait, medium shot, subject clearly readable
Lighting/mood: 符合典型情境的自然光与克制情绪
Constraints: 与 Persona 信息一致；单一主要人物；自然日常；无文字、无 logo、无水印
Avoid: 影棚证件照、广告摆拍、过度磨皮、夸张表情、刻板职业符号、无依据的奢华环境
```

图片不需要把 Persona 的所有字段都视觉化。优先表现最能帮助阅读的三项：现实处境、典型行为、情绪或关系压力。

## 保存与引用

默认以报告文件所在目录为基准保存：

```text
docs/
├── User-Persona-{产品名}-{YYYYMMDD}.mdx
└── assets/
    └── user-persona/
        └── {product-slug}/
            ├── {persona-slug}.png
            └── {persona-slug-2}.png
```

- `product-slug` 和 `persona-slug` 只使用小写字母、数字和连字符；同一人物重新生成且未明确要求替换时使用 `-v2` 等版本后缀。
- 报告在 `Profile.image` 中使用项目相对路径，例如：

```mdx
<Profile
  name="周敏"
  image={{
    src: "assets/user-persona/example-product/zhou-min.png",
    alt: "周敏，正在为当前任务核验重要信息"
  }}
>
  人物背景正文。
</Profile>
```

- 图片是对应人物 `Profile` 的组成部分，不在组件前后重复插入 Markdown 图片。
- alt 文本包含人物姓名和可观察的使用背景，不能写“用户图片”、抽象画像标签或留空。
- 同一报告内每个人物图片使用唯一 alt；首屏人物卡的 `sourceImageAlt` 与对应 `Profile.image.alt` 完全一致。
- 导入文档门户时，生成器会复制 `Profile.image.src` 指向的本地图片并重写为门户资产路径。图片缺失时应让导入失败，避免发布破图报告。
