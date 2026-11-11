# 更新日志

本文件记录 damai-ticket-assistant-skill 的每一次对外发布，格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循语义化版本（SemVer）。

- 主版本（X.0.0）：购票授权语义、状态模型或安装方式发生不兼容变更，用户必须重新阅读 README。
- 次版本（X.Y.0）：新增能力、新增模板、较大的文档改进，向后兼容。
- 修订版本（X.Y.Z）：措辞修正、链接修复、排错指引补充，不影响使用方式。

## [Unreleased]

（暂无）

## [0.2.0] - 2026-11-11

### 新增

- 发布体系：GitHub Actions 校验与发布流水线（push v* 标签自动打包 Skill 并创建 Release）、Issue/PR 模板、发布 SOP（docs/RELEASE.md）、静态校验脚本（frontmatter、相对链接、表述红线、版本一致性）。
- README：目录、快速开始、流程概览图（mermaid）、安装验证的预期输出对照、版本诊断与 404 排错 FAQ。
- MIT LICENSE；agents/openai.yaml 增加 version 字段，与 README、CHANGELOG 三处联动标识版本。

### 修正

- 删除"私有仓库"过时表述（仓库为公开仓库），安装前提与 404 排错改为网络原因说明。
- 安装指引改为优先使用 Releases 直装包（解压顶层即 damai-ticket-assistant/），避免"复制哪一层文件夹"的常见失误。
- README 使用示例收敛为单一精简示例，六个完整模板统一到 examples/request-template.md，消除双轨维护分叉。
- 仓库内容表补充 agents/openai.yaml、docs、scripts、.github 等条目。

## [0.1.0] - 2026-10-13

### 新增

- 首个可用版本：`skills/damai-ticket-assistant/SKILL.md`，包含八步购票流程、强制约束与通俗汇报规则。
- `skills/damai-ticket-assistant/references/transaction-recovery.md`：交易状态机与异常恢复规则。
- `examples/request-template.md`：六个可复制的中文购票请求模板（安装验证、仅准备、仅下单、下单并支付、异常核查、停止操作）。
- `skills/damai-ticket-assistant/agents/openai.yaml`：宿主界面元数据与隐式调用开关。
- README：安装前准备、两种安装方式、无下单验证、使用示例、人工接管场景、常见问题、更新与卸载说明。

[0.2.0]: https://github.com/jw070322-svg/damai-ticket-assistant-skill/releases/tag/v0.2.0
[0.1.0]: https://github.com/jw070322-svg/damai-ticket-assistant-skill/releases/tag/v0.1.0
