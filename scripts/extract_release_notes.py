#!/usr/bin/env python3
"""从 CHANGELOG.md 提取指定版本的小节，作为 GitHub Release 说明。

用法：
    python -I scripts/extract_release_notes.py v0.2.0
"""

from __future__ import annotations

import pathlib
import re
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("用法：extract_release_notes.py vX.Y.Z", file=sys.stderr)
        return 2
    version = sys.argv[1].lstrip("v")

    changelog_path = pathlib.Path(__file__).resolve().parent.parent / "CHANGELOG.md"
    lines = changelog_path.read_text(encoding="utf-8").splitlines()

    start = None
    for i, line in enumerate(lines):
        if re.match(rf"^##\s*\[{re.escape(version)}\]", line.strip()):
            start = i
            break
    if start is None:
        print(f"CHANGELOG.md 中没有版本 [{version}] 的小节，请先归档 Unreleased。", file=sys.stderr)
        return 1

    out = [re.sub(r"\[Unreleased\]|\[[^\]]+\]", version, lines[start], count=1)]
    for line in lines[start + 1:]:
        if re.match(r"^##\s*\[", line.strip()):
            break
        out.append(line)

    body = "\n".join(out).strip()
    # 去掉尾部的引用式链接定义（如 [0.1.0]: https://...）
    body = re.sub(r"^\[[^\]]+\]:\s*\S+\s*$", "", body, flags=re.M).strip()
    print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
