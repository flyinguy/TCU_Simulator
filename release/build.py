# -*- coding: utf-8 -*-
"""
电磁离合器仿真台 —— 打包与版本管理脚本

用法：
    python build.py "本次更新说明文字"

每次运行会：
    1) 读取 version.txt 中的当前版本号（如 1.0）
    2) 用该版本号渲染 app_template.html -> app.html（替换 {{VERSION}}）
    3) 调用 PyInstaller 打包成单文件exe：dist_exe/电磁离合器仿真台_V{当前版本}.exe
    4) 把本次更新说明插入到 ../update.log 标题下方（最新版本在最上面；版本号=本次构建使用的版本）
    5) 将 version.txt 中的版本号自动+0.1，供下一次构建使用（1.0 -> 1.1 -> 1.2 ...）

即：第一次运行时 version.txt=1.0，产出 V1.0 的exe与changelog条目，
   运行结束后 version.txt 自动变为1.1；下次运行 build.py 就会产出 V1.1。
"""
import datetime
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(HERE, "version.txt")
CHANGELOG_FILE = os.path.join(HERE, "..", "update.log")
TEMPLATE_FILE = os.path.join(HERE, "app_template.html")
RENDERED_HTML = os.path.join(HERE, "app.html")
APP_ENTRY = os.path.join(HERE, "app.py")
DIST_DIR = os.path.join(HERE, "dist_exe")
WORK_DIR = os.path.join(HERE, "build_tmp")
ICON_FILE = os.path.join(HERE, "assets", "icon.ico")
APP_NAME_BASE = "电磁离合器仿真台"


def read_version():
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


def write_version(v):
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(v + "\n")


def bump_version(v):
    """1.0 -> 1.1 -> 1.2 ... 简单的次版本号+1，不做10进位处理。"""
    major, minor = v.split(".")
    return f"{major}.{int(minor)+1}"


def render_html(version_tag):
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("{{VERSION}}", version_tag)
    with open(RENDERED_HTML, "w", encoding="utf-8") as f:
        f.write(content)


def run_pyinstaller(exe_name):
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(WORK_DIR, exist_ok=True)
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--windowed", "--noconfirm",
        "--name", exe_name,
        "--add-data", f"{RENDERED_HTML}{os.pathsep}.",
    ]
    if os.path.exists(ICON_FILE):
        cmd += ["--icon", ICON_FILE]
    cmd += [
        "--distpath", DIST_DIR,
        "--workpath", WORK_DIR,
        "--specpath", WORK_DIR,
        APP_ENTRY,
    ]
    print("执行:", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=HERE)


def prepend_changelog(version_tag, description, exe_name):
    """新条目插入到标题行之后，保持"最新版本在最上面"的顺序；文件统一使用CRLF换行。"""
    today = datetime.date.today().isoformat()
    entry = f"## {version_tag} - {today}\n\n{description.strip()}\n\n" \
            f"- 产出文件: `dist_exe/{exe_name}.exe`\n"
    header = "# 电磁离合器仿真台 - 版本更新日志\n"
    body = ""
    if os.path.exists(CHANGELOG_FILE):
        with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
            old = f.read()
        if old.startswith("# "):
            first, _, body = old.partition("\n")
            header = first + "\n"
        else:
            body = old
    content = header + "\n" + entry + ("\n" + body.lstrip("\n") if body.strip() else "")
    with open(CHANGELOG_FILE, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(content)


def main():
    if len(sys.argv) < 2:
        print("用法: python build.py \"本次更新说明\"")
        sys.exit(1)
    description = sys.argv[1]

    current_version = read_version()
    version_tag = f"V{current_version}"
    exe_name = f"{APP_NAME_BASE}_{version_tag}"

    print(f"[1/4] 当前构建版本: {version_tag}")
    render_html(version_tag)
    print("[2/4] app.html 已渲染完成")

    run_pyinstaller(exe_name)
    print(f"[3/4] 打包完成: dist_exe/{exe_name}.exe")

    prepend_changelog(version_tag, description, exe_name)
    next_version = bump_version(current_version)
    write_version(next_version)
    print(f"[4/4] 更新日志已写入 update.log；version.txt 已更新为下一版本号 {next_version}")


if __name__ == "__main__":
    main()
