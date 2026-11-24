#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端中文本地化补丁（仅替换中文侧字典里仍残留英文的条目）

背景：
    官方前端 `_t = {zh: Ls, en: Ms}` 两套字典本身是完整的（zh 985 条 / en 984 条），
    但有 8 条中文值仍是英文（Usage / Breakdown / Task / Trace ...），
    在中文界面下会露出来。本脚本只改这 8 条。

用法：
    python apply_frontend_localization.py <解包后的 static/assets 目录>

示例：
    asar extract app.asar app_unpacked
    python apply_frontend_localization.py app_unpacked/backend/.../static/assets
    asar pack app_unpacked app.asar

安全说明：
    只做「"键":"旧值" -> "键":"新值"」的整对替换，
    不碰键名、不碰英文侧字典、不碰任何标识符，因此不会破坏路由或状态键。
"""

import sys
import pathlib

MAPPING = [
    # (字典键, 原英文值, 中文值)
    ("layout.appFallbackDescription", "Web workspace", "网页工作台"),
    ("layout.appFallbackTitle", "Daily Stock Analysis", "股票智能分析"),
    ("usage.breakdown", "Breakdown", "明细"),
    ("usage.eyebrow", "Usage", "用量"),
    ("usage.completionTokens", "Completion tokens", "输出 Tokens"),
    ("usage.promptTokens", "Prompt tokens", "输入 Tokens"),
    ("runFlow.summary.task", "Task", "任务"),
    ("runFlow.summary.trace", "Trace", "追踪"),
]


def patch_file(path: pathlib.Path) -> int:
    text = path.read_text(encoding="utf-8")
    total = 0
    for key, old, new in MAPPING:
        src = f'"{key}":"{old}"'
        dst = f'"{key}":"{new}"'
        hits = text.count(src)
        if hits:
            text = text.replace(src, dst)
            total += hits
        print(f"  {key:<34} {hits} 处 -> {new}")
    if total:
        path.write_text(text, encoding="utf-8")
    return total


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2

    assets = pathlib.Path(sys.argv[1])
    if not assets.is_dir():
        print(f"目录不存在: {assets}")
        return 2

    targets = sorted(assets.glob("index-*.js"))
    if not targets:
        print("未找到 index-*.js，请确认路径指向 static/assets")
        return 1

    grand = 0
    for f in targets:
        print(f"[文件] {f.name}")
        grand += patch_file(f)

    if grand == 0:
        print("\n提示：0 处改动。可能是已经打过补丁，或上游已修复这些条目。")
    else:
        print(f"\n完成，共替换 {grand} 处。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())