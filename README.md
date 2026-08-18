# GainFactor Plugins Marketplace

GainFactor 的 Codex / ChatGPT 插件市场。当前包含 `gainfactor-pm`：一套从业务需求到测试与运维准备的产品研发工作流。

## 安装

在 Codex 或 ChatGPT 的插件市场页面中：

1. 选择“添加插件市场”。
2. 在“来源”中填写本 GitHub 仓库或 Git URL。
3. “Git 引用”可留空以使用默认分支，或填写指定版本标签。
4. Marketplace 清单位于仓库的 `.agents/plugins/marketplace.json`；添加整个仓库时“稀疏路径”留空。
5. 添加市场后，安装 `gainfactor-pm`。

## 仓库结构

```text
.
├── .agents/
│   └── plugins/
│       └── marketplace.json
└── plugins/
    └── gainfactor-pm/
        ├── .codex-plugin/plugin.json
        ├── skills/
        ├── scripts/
        ├── references/
        └── README.md
```

插件的功能、Skill 与开发说明见 [`plugins/gainfactor-pm/README.md`](plugins/gainfactor-pm/README.md)。

## 本地校验

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/gainfactor-pm
python3 plugins/gainfactor-pm/scripts/validate_codex_compat.py
python3 -m unittest discover -s plugins/gainfactor-pm/scripts/tests -v
```
