# -*- coding: utf-8 -*-
"""
电磁离合器仿真台 —— 桌面版启动入口

不再使用pywebview内嵌窗口（在部分Windows 10机器上因缺少WebView2运行时/.NET环境
而无法打开），改为：把界面文件复制到本机一个固定目录，再用系统默认浏览器打开它。
这样只依赖浏览器本身，兼容性更好，也不需要用户额外安装任何运行时。
"""
import os
import shutil
import sys
import webbrowser
from pathlib import Path

APP_TITLE = "电磁离合器仿真台"


def resource_path(relative_path):
    """兼容开发环境与PyInstaller打包后的资源路径。"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def persistent_copy_path():
    """浏览器需要一个在exe进程退出后依然存在的文件路径
    （PyInstaller onefile的_MEIPASS临时目录会在进程退出后被清理）。
    统一放到 %LOCALAPPDATA%\\ClutchSim\\app.html。
    """
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    target_dir = os.path.join(base, "ClutchSim")
    os.makedirs(target_dir, exist_ok=True)
    return os.path.join(target_dir, "app.html")


def find_chrome():
    """优先使用 Chrome 打开；依次检查常见安装路径与注册表 App Paths。"""
    candidates = [
        os.path.join(os.environ.get("PROGRAMFILES", r"C:\Program Files"), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"), "Google", "Chrome", "Application", "chrome.exe"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "Application", "chrome.exe"),
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    try:
        import winreg
        for root in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
            try:
                with winreg.OpenKey(root, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe") as k:
                    val, _ = winreg.QueryValueEx(k, None)
                    if val and os.path.exists(val):
                        return val
            except OSError:
                continue
    except ImportError:
        pass
    return None


def main():
    src = resource_path("app.html")
    dst = persistent_copy_path()
    shutil.copyfile(src, dst)

    url = Path(dst).as_uri()
    chrome = find_chrome()
    if chrome:
        try:
            import subprocess
            subprocess.Popen([chrome, url], close_fds=True)
            return
        except OSError:
            pass
    # 未安装 Chrome 时退回系统默认浏览器
    opened = webbrowser.open(url)
    if not opened:
        print(f"未能自动打开浏览器，请手动用浏览器打开: {dst}")


if __name__ == "__main__":
    main()
