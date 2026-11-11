#!/usr/bin/env python3
"""damai-ticket-assistant-skill 静态校验脚本。

检查内容：
1. Skill 目录结构与 frontmatter 完整性；
2. 全仓库 Markdown 相对链接可解析；
3. 表述红线：面向用户的文档不得承诺购票成功或诱导绕过平台限制（否定语境除外）；
4. 可选参数 --version：校验 README 版本行与 CHANGELOG 版本小节存在且一致。

用法：
    python -I scripts/validate_skill.py
    python -I scripts/validate_skill.py --version 0.2.0
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SKILL_MD = REPO / "skills" / "damai-ticket-assistant" / "SKILL.md"

# 否定语境词：命中词出现在目标词前 12 个字符内时，视为"警示性表述"而非违规。
NEGATIONS = ("不", "勿", "禁", "没有", "拒绝", "无法", "不能")

# 高置信度红线：违规即校验失败。
HARD_TERMS = ("保证抢到", "保证买到", "保证成功", "保证出票",
              "必定抢到", "一定抢到", "100%抢到", "100%成功", "100%出票")

# 低置信度红线：仅输出警告，供人工复核。
SOFT_TERMS = ("绕过", "私有接口", "抢票程序", "破解读取", "代答验证码")


def has_negation_before(text: str, pos: int, window: int = 24) -> bool:
    prefix = text[max(0, pos - window):pos]
    return any(word in prefix for word in NEGATIONS)


def scan_terms(files: dict[pathlib.Path, str]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for path, text in files.items():
        rel = path.relative_to(REPO).as_posix()
        for term in HARD_TERMS:
            for m in re.finditer(re.escape(term), text):
                if not has_negation_before(text, m.start()):
                    errors.append(f"{rel}：出现承诺性表述「{term}」")
        for term in SOFT_TERMS:
            for m in re.finditer(re.escape(term), text):
                if not has_negation_before(text, m.start()):
                    warnings.append(f"{rel}：「{term}」缺少否定语境，请人工复核")
    return errors, warnings


def check_links(files: dict[pathlib.Path, str]) -> list[str]:
    errors: list[str] = []
    link_re = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
    for path, text in files.items():
        for m in link_re.finditer(text):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#", "../")):
                continue  # 外部链接、页内锚点与 GitHub UI 相对路径（如 ../../releases）不在本地检查范围
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            if not resolved.exists():
                rel = path.relative_to(REPO).as_posix()
                errors.append(f"{rel}：相对链接 {target} 指向不存在的文件")
    return errors


def check_skill_structure() -> list[str]:
    errors: list[str] = []
    if not SKILL_MD.exists():
        return [f"缺少 {SKILL_MD.relative_to(REPO).as_posix()}"]
    text = SKILL_MD.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return ["SKILL.md 缺少 frontmatter（应以 --- 开头）"]
    end = text.find("\n---", 3)
    if end == -1:
        return ["SKILL.md frontmatter 未闭合"]
    fm = text[3:end]
    name_m = re.search(r"^name:\s*(\S+)\s*$", fm, re.M)
    desc_m = re.search(r"^description:\s*(.+)\s*$", fm, re.M)
    if not name_m or name_m.group(1) != SKILL_MD.parent.name:
        errors.append("SKILL.md frontmatter 的 name 缺失，或与文件夹名 damai-ticket-assistant 不一致")
    if not desc_m or not desc_m.group(1).strip():
        errors.append("SKILL.md frontmatter 缺少 description")
    elif len(desc_m.group(1)) > 1024:
        errors.append("SKILL.md description 超过 1024 字符")
    return errors


def check_version(version: str) -> list[str]:
    errors: list[str] = []
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    if f"当前版本：v{version}" not in readme:
        errors.append(f"README.md 缺少版本标识行「当前版本：v{version}」")
    changelog = (REPO / "CHANGELOG.md").read_text(encoding="utf-8")
    if not re.search(rf"^##\s*\[{re.escape(version)}\]", changelog, re.M):
        errors.append(f"CHANGELOG.md 缺少「## [{version}]」小节，请先归档 Unreleased")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Skill 仓库静态校验")
    parser.add_argument("--version", help="校验该版本号在 README 与 CHANGELOG 中的一致性")
    args = parser.parse_args()

    md_files = {p: p.read_text(encoding="utf-8")
                for p in REPO.rglob("*.md") if ".git" not in p.parts}

    errors = check_skill_structure()
    errors += check_links(md_files)
    term_errors, warnings = scan_terms(md_files)
    errors += term_errors
    if args.version:
        errors += check_version(args.version)

    for w in warnings:
        print(f"警告：{w}")
    if errors:
        for e in errors:
            print(f"错误：{e}")
        print(f"校验未通过：{len(errors)} 个错误。")
        return 1
    print("校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
