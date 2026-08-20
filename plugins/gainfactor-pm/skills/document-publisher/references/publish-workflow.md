# 文档创建、导入与更新工作流

1. 确认源文件、稳定 slug、artifact type 和目标门户；上游已给出时不重复询问。
2. 检查源文件已经是业务 Skill 直接完成的最终 `.mdx`；发布阶段不得重新选择组件、从普通 Markdown 转换，或从正文推导首屏。
3. 若有 presentation manifest，先做只读格式校验：

   ```bash
   python3 <plugin-root>/scripts/compile_portal_document.py \
     <document.mdx> --presentation=<document.portal.json> --validate
   ```

4. 需要加入统一阅读与评审门户时，交给 `$document-review` 选择目标门户、管理稳定 slug、载入既有 presentation 和评审数据。底层 `create_document_portal.py` 只机械导入既有产物、搬运相对图片并更新清单与导航。
5. 更新同一文档时复用 slug；不要覆盖整个门户或丢弃其他文档。
6. 运行 Python 测试和目标门户的 `npm run types:check`。组件或构建配置有改动时再运行 lint/build。
7. 用户要求打开或预览时启动服务，检查首屏、目录、正文、图表、图片与移动端。

动作模型是 `create/import | update | validate | preview`。所有动作操作调用者已经写好的文档，不承担内容转换。后续加入局部 block 编辑时，应使用稳定 module id/section id 做最小更新，并在每次更新后重新读取验证，不通过全文覆盖模拟局部更新。
