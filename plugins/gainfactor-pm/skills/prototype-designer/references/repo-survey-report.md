# 仓库探查报告模板

Phase 0.5 完成后，必须按此模板输出报告。

---

## 仓库探查报告

### 前端工作区门禁

| 信号 | 命中 | 证据 |
|------|------|------|
| UI 框架依赖 | ✅/❌ | [package.json 中的框架及版本] |
| 页面/路由目录 | ✅/❌ | [命中的路径] |
| 组件目录 | ✅/❌ | [命中的路径] |

**门禁结论**：[通过 / 用户确认后通过 / 未通过——已引导用户]

### 技术栈

| 项目 | 值 | 来源 |
|------|-----|------|
| 框架 | [框架 + 版本] | [package.json 路径] |
| 路由方案 | [文件路由 / 配置路由 / 约定] | [配置文件/目录路径] |
| 样式方案 | [Tailwind / CSS Modules / Styled Components / ...] | [配置文件路径] |
| 状态管理 | [Redux / Zustand / Pinia / Context / ...] | [来源路径] |
| TypeScript | [是/否 + strict 级别] | [tsconfig.json 路径] |
| 包管理器 | [npm / pnpm / yarn / bun] | [lock 文件路径] |

### 组件目录索引

| 组件名 | 类别 | 路径 |
|--------|------|------|
| Button | 基础 | src/components/ui/Button.tsx |
| Table | 数据展示 | src/components/Table/index.tsx |
| Form | 表单 | src/components/Form/Form.tsx |
| Empty | 状态 | src/components/Empty.tsx |
| Loading / Skeleton | 状态 | src/components/Loading.tsx |
| ... | ... | ... |

> 此阶段只列目录索引，不含 Props 详情。Props 在 Phase 1.4 按需读取。

### 设计规范

- **布局模式**：[sidebar + main / top-nav + content / ...]
- **通用状态组件**：[空态: 路径, 加载态: 路径, 错误态: 路径]
- **Storybook**：[存在/不存在; 路径]

### 运行命令识别

| 项目 | 命令 | 来源 |
|------|------|------|
| 包管理器 | [pnpm / npm / yarn / bun] | [lock 文件] |
| 开发启动 | [pnpm dev / npm run dev / ...] | [package.json scripts] |
| Lint 检查 | [pnpm lint / npm run lint / ...] | [package.json scripts] |
| 类型检查 | [pnpm typecheck / pnpm exec tsc --noEmit / npx tsc --noEmit / 需确认] | [package.json scripts；或 tsconfig + 包管理器 exec（pnpm exec / yarn exec / bunx / npx）；或待 宿主交互提问机制] |
| 工作区定位 | [monorepo 时: 包名或 --filter 参数] | [workspace 配置] |

### 原型沙箱规划

- **沙箱路径**：[用户确认的路径，如 src/prototype/ 或 app/prototype/]
- **路由隔离方式**：[文件路由天然隔离 / 独立入口文件 / 用户协商方案]
- **路由前缀**：[/prototype/]
