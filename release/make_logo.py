# -*- coding: utf-8 -*-
"""生成电磁离合器Logo（圆形铁芯 + 铜色线圈 + 磁力线），
输出 assets/logo.png (1024x1024) 与 assets/icon.ico (多尺寸，供PyInstaller做exe图标)。
"""
import math
import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
os.makedirs(ASSETS, exist_ok=True)

S = 1024
CX = CY = S // 2

STEEL_DARK = (36, 38, 41, 255)
STEEL_MID = (54, 57, 61, 255)
STEEL_RIM = (74, 78, 83, 255)
COPPER = (196, 124, 51, 255)
COPPER_DARK = (138, 82, 27, 255)
COPPER_LIGHT = (224, 158, 92, 255)
BG = (0, 0, 0, 0)


def circle(draw, r, fill, cx=CX, cy=CY):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


def main():
    img = Image.new("RGBA", (S, S), BG)
    d = ImageDraw.Draw(img)

    # 外圈铁芯壳体
    circle(d, 500, STEEL_RIM)
    circle(d, 478, STEEL_DARK)

    # 铜色线圈环带
    circle(d, 380, COPPER_DARK)
    circle(d, 362, COPPER)
    circle(d, 300, STEEL_DARK)

    # 线圈绕组刻线（径向短线，模拟缠绕匝数）
    n_turns = 40
    for i in range(n_turns):
        ang = 2 * math.pi * i / n_turns
        r1, r2 = 308, 356
        x1, y1 = CX + r1 * math.cos(ang), CY + r1 * math.sin(ang)
        x2, y2 = CX + r2 * math.cos(ang), CY + r2 * math.sin(ang)
        d.line([x1, y1, x2, y2], fill=COPPER_DARK, width=6)

    # 中心衔铁/轴
    circle(d, 210, STEEL_MID)
    circle(d, 190, STEEL_DARK)
    circle(d, 46, COPPER_LIGHT)
    circle(d, 30, COPPER)

    # 气隙分隔线（水平细缝，表示衔铁与铁芯的结合面）
    d.rectangle([CX - 300, CY - 7, CX + 300, CY + 7], fill=(20, 21, 23, 220))

    # 放大画布并居中，为外圈磁力线留出不被裁切的空间
    pad = 120
    canvas = Image.new("RGBA", (S + pad * 2, S + pad * 2), BG)
    canvas.paste(img, (pad, pad), img)
    d2 = ImageDraw.Draw(canvas)
    ccx, ccy = CX + pad, CY + pad

    for base_ang_deg in (0, 90, 180, 270):
        base = math.radians(base_ang_deg)
        for k in range(3):
            r = 512 + k * 34
            span = math.radians(26)
            steps = 14
            pts = []
            for s in range(steps + 1):
                a = base - span / 2 + span * s / steps
                pts.append((ccx + r * math.cos(a), ccy + r * math.sin(a)))
            for j in range(0, len(pts) - 1, 2):
                d2.line([pts[j], pts[j + 1]], fill=(196, 124, 51, 235 - k * 60), width=10)

    img = canvas
    img.save(os.path.join(ASSETS, "logo.png"))

    icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(os.path.join(ASSETS, "icon.ico"), sizes=icon_sizes)
    print("已生成:", os.path.join(ASSETS, "logo.png"))
    print("已生成:", os.path.join(ASSETS, "icon.ico"))


if __name__ == "__main__":
    main()
