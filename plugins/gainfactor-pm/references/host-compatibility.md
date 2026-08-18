# Codex 运行规则

本插件当前仅支持 Codex。执行任一 skill 时，按本文件使用当前会话实际提供的能力；不要调用不存在的工具。

## 交互提问

文档中的“宿主交互提问机制”表示：

- 仅在 `request_user_input` 可用时使用；不可用时，直接用简短、明确的普通文本提问。
- 不要为了使用某个工具切换工作模式，也不要在工具不可用时伪造调用。

## Subagent 调度

文档中的“宿主 subagent 调度机制”表示：

- 使用 `spawn_agent` 派发，使用 `wait_agent` 等待；需要继续同一角色时使用 `followup_task`。
- 如果当前宿主没有 subagent 能力：
  - skill 明确要求隔离执行时，说明能力缺口并询问用户是否接受同一任务内的顺序降级。
  - 隔离仅为优化项时，可在同一任务中顺序执行，但必须标注未实现独立上下文。
- 不得声称已经完成独立评审，除非确实使用了独立 subagent。

## Skill 调用格式

工作流内部只依赖稳定 skill ID，例如 `prd-writer`。向用户展示时使用 Codex 调用格式：

- 本插件：`$prd-writer`
- 兄弟插件 `gainfactor-pm-bot`：`$case-writing`

不得根据 artifact 名或自然语言自行发明 skill ID。

## 插件内脚本

不要假设用户工作区包含 `plugins/gainfactor-pm`。调用脚本前，先从当前 `SKILL.md` 或本文件的位置解析 `gainfactor-pm` 插件根目录，再使用绝对路径执行：

```text
<gainfactor-pm-plugin-root>/scripts/trace_lint.py
<gainfactor-pm-plugin-root>/scripts/trace_build_rtm.py
```

文档中的 `<gainfactor-pm-plugin-root>` 是运行时占位符，必须替换为已解析的绝对路径后再执行，不能原样传给 shell。

## 浏览器中的原型评审意见

- Browser 能力可用时，只读取原型公开的 URL fragment、runtime export 或只读
  DOM Markdown；Browser 不可用时，请用户展开或复制 Markdown。
- 禁止为了读取评审意见而访问 `localStorage`、`sessionStorage`、Cookie、
  浏览器配置或用户资料。
