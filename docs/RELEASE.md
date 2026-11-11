# 发布流程 SOP

本文面向仓库维护者，说明如何把一次改动变成用户可感知、可安装、可追溯的 Release。

## 前置条件

1. `main` 分支 CI（Lint 工作流）为绿色。
2. `CHANGELOG.md` 顶部 `Unreleased` 段已写好本次全部变更，并按语义归类为：新增 / 变更 / 修复 / 移除。
3. `README.md` 顶部"当前版本"行已同步为待发布的版本号。
4. 敏感信息自查：无凭据、身份证号、二维码、订单截图入库。

## 版本号规则（SemVer）

| 版本位 | 何时递增 | 示例 |
| --- | --- | --- |
| 主版本 X.0.0 | 授权语义、状态模型、安装方式发生不兼容变更；用户必须重读 README | 票-人对应规则重写 |
| 次版本 X.Y.0 | 新增模板、新增参考文档、较大文档改进；向后兼容 | 新增无障碍购票指引 |
| 修订版本 X.Y.Z | 措辞修正、链接修复、排错补充 | 修正 FAQ 中的过时说法 |

## 标准发布步骤

1. 本地校验：python -I scripts/validate_skill.py --version 0.Y.Z
2. 提交发布准备：CHANGELOG 归档 + README 版本行 + 本 SOP 涉及文件的改动，一个 commit，信息如：chore(release): v0.2.0
3. 打附注标签并推送：git tag -a v0.Y.Z -m "v0.Y.Z"；git push origin main v0.Y.Z
4. 等 Actions 的 Release 工作流跑完（校验 → 打包 → 发布）。
5. 到 Releases 页检查：说明取自 CHANGELOG、压缩包可下载、已标记 Latest。
6. 下载压缩包抽查：解压后顶层应直接是 damai-ticket-assistant/ 文件夹。
7. 关闭本版对应的 Issue，必要时在相关讨论中贴出 Release 链接。

## 首次发布（v0.2.0）

v0.1.0 仅作为 CHANGELOG 中的历史记录（对应 2026-10-13 的初始提交），**不在旧提交上补打标签**——旧提交不包含发布工作流和脚本，自动发布会失败。首次发布直接从合并发布体系后的 main 开始：

1. 把发布体系（.github/、scripts/、docs/、CHANGELOG.md、README.md、LICENSE、.markdownlint-cli2.jsonc）合入 main。
2. 确认 README 版本行为 v0.2.0、CHANGELOG 已有 [0.2.0] 小节。
3. git tag -a v0.2.0 -m "v0.2.0" 并推送标签，Release 与直装包自动生成。
4. 之后的所有改动走"标准发布步骤"。

## 失败处理

- validate 失败：按 Actions 日志修正（多为链接失效、版本行不同步、CHANGELOG 未归档），修正后删除本地与远端旧标签，重新打标签推送。
- 打包或发布步骤失败：修正后同样重新打标签；不要手工在网页上创建同名 Release。

## 热修与撤回

- 热修：从出问题的 vX.Y.Z 标签拉 hotfix 分支，修复后递增修订版本走标准流程。
- 撤回：Release 页删除 Release 与对应 tag，在 CHANGELOG 中把该版本小节标记为"已撤回"及原因，再发布修复版本。
