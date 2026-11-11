## 变更类型

- [ ] 文档修正（README / 模板 / 排错指引）
- [ ] Skill 规则调整（SKILL.md 或 references/）
- [ ] 发布流程或 CI
- [ ] 其他

## 动机与内容

为什么改、改了什么。关联 Issue 请写 `Fixes #编号`。

## 自查清单

- [ ] 不含任何凭据、身份证号、二维码、订单截图等敏感信息
- [ ] 未弱化 SKILL.md 中"必须保持的约束"与"不绕过平台限制"的安全边界
- [ ] 涉及行为变化的，已同步更新 README 与 CHANGELOG 的 Unreleased 段
- [ ] 文档内相对链接均可访问（本地跑过 `python -I scripts/validate_skill.py`）
