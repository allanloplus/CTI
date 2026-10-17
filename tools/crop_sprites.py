"""從角色設定圖裁出姿勢與表情，去除白色背景後輸出 WebP 精靈圖。

用法：python3 tools/crop_sprites.py
來源：src/source/arale-sheet.jpg、src/source/allan-sheet.jpg
輸出：src/sprites/<name>.webp
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "source"
OUT = ROOT / "src" / "sprites"

# 設定圖上的灰色分隔線（列範圍），裁切前先抹成白色
RULES = {
    "arale-sheet.jpg": [(137, 146), (741, 750)],
    "allan-sheet.jpg": [],
}

# (來源檔, 名稱, 裁切框 left, top, right, bottom, 輸出最長邊, 選項)
# 選項 seeds：被手臂圍住、從邊緣填不到的白色區塊（原圖座標）
# 選項 fade：(方向, 像素) 切邊漸隱，用於與隔壁角色重疊的手
CROPS = [
    # 阿拉蕾：全身
    ("arale-sheet.jpg", "arale-wave", (80, 118, 455, 768), 520, {}),
    ("arale-sheet.jpg", "arale-tablet", (1148, 148, 1492, 760), 560, {"fade": ("right", 46)}),
    ("arale-sheet.jpg", "arale-present", (1560, 148, 1992, 760), 560, {"fade": ("left", 70)}),
    ("arale-sheet.jpg", "arale-hi", (68, 802, 420, 1478), 520, {}),
    # 阿拉蕾：表情（框線內側）
    ("arale-sheet.jpg", "arale-laugh", (440, 810, 794, 1112), 320, {}),
    ("arale-sheet.jpg", "arale-think", (826, 810, 1180, 1112), 320, {}),
    ("arale-sheet.jpg", "arale-wow", (1212, 810, 1566, 1112), 320, {}),
    ("arale-sheet.jpg", "arale-confused", (1597, 810, 1951, 1112), 320, {}),
    ("arale-sheet.jpg", "arale-explain", (440, 1146, 794, 1447), 320, {}),
    ("arale-sheet.jpg", "arale-sad", (826, 1146, 1180, 1447), 320, {}),
    ("arale-sheet.jpg", "arale-wink", (1212, 1146, 1566, 1447), 320, {}),
    ("arale-sheet.jpg", "arale-fight", (1597, 1146, 1951, 1447), 320, {"seeds": [(1702, 1388)]}),
    # Allan 顧問：全身
    ("allan-sheet.jpg", "allan-present", (50, 82, 772, 1480), 640, {}),
    # Allan 顧問：表情
    ("allan-sheet.jpg", "allan-smile", (762, 792, 1024, 1120), 320, {}),
    ("allan-sheet.jpg", "allan-laugh", (1070, 792, 1334, 1120), 320, {}),
    ("allan-sheet.jpg", "allan-think", (1380, 792, 1636, 1120), 320, {}),
    ("allan-sheet.jpg", "allan-scratch", (1640, 792, 1972, 1120), 320, {"seeds": [(1717, 942)]}),
    ("allan-sheet.jpg", "allan-wow", (762, 1132, 1024, 1462), 320, {}),
    ("allan-sheet.jpg", "allan-point", (1040, 1132, 1334, 1462), 320, {}),
    ("allan-sheet.jpg", "allan-wink", (1380, 1132, 1644, 1462), 320, {}),
    ("allan-sheet.jpg", "allan-shock", (1700, 1132, 1966, 1462), 320, {}),
]

WHITE_MIN = 232  # RGB 皆高於此值視為接近白色


def erase_rules(sheet: Image.Image, rows) -> Image.Image:
    """把分隔線上的中性灰像素改成白色，角色本身的彩色與黑線不受影響。"""
    if not rows:
        return sheet
    arr = np.asarray(sheet).copy()
    for top, bottom in rows:
        band = arr[top:bottom].astype(np.int16)
        neutral = (band.min(axis=2) > 110) & ((band.max(axis=2) - band.min(axis=2)) < 22)
        arr[top:bottom][neutral] = 255
    return Image.fromarray(arr).copy()


def remove_background(img: Image.Image, seeds=()) -> Image.Image:
    """從邊緣與指定種子點 flood fill 接近白色的區域並設為透明，保留角色內部的白色。"""
    rgb = np.asarray(img.convert("RGB")).astype(np.int16)
    near_white = (rgb.min(axis=2) >= WHITE_MIN) & ((rgb.max(axis=2) - rgb.min(axis=2)) <= 18)
    # 用 putdata 建立獨立影像；fromarray 會共用唯讀記憶體，floodfill 寫不回去
    mask = Image.new("L", img.size, 0)
    mask.putdata((near_white.astype(np.uint8) * 255).ravel().tolist())
    w, h = mask.size
    px = mask.load()
    points = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)]
    points += [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    points += list(seeds)
    for xy in points:
        if 0 <= xy[0] < w and 0 <= xy[1] < h and px[xy] == 255:
            ImageDraw.floodfill(mask, xy, 128, thresh=0)
    bg = np.asarray(mask) == 128
    alpha = Image.new("L", img.size, 0)
    alpha.putdata(np.where(bg, 0, 255).astype(np.uint8).ravel().tolist())
    # 輕微收邊與羽化，去掉白邊
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    out = img.convert("RGBA")
    out.putalpha(alpha)
    return out


def apply_fade(img: Image.Image, side: str, width: int) -> Image.Image:
    """在指定邊做線性漸隱。"""
    a = np.asarray(img.getchannel("A")).astype(np.float32)
    ramp = np.clip(np.arange(img.width, dtype=np.float32) / width, 0, 1)
    if side == "right":
        ramp = ramp[::-1]
    a *= ramp[None, :]
    alpha = Image.new("L", img.size, 0)
    alpha.putdata(a.astype(np.uint8).ravel().tolist())
    img.putalpha(alpha)
    return img


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sheets = {}
    for src, name, box, longest, opts in CROPS:
        if src not in sheets:
            sheets[src] = erase_rules(Image.open(SRC / src).convert("RGB"), RULES.get(src))
        seeds = [(x - box[0], y - box[1]) for x, y in opts.get("seeds", [])]
        piece = remove_background(sheets[src].crop(box), seeds)
        if "fade" in opts:
            piece = apply_fade(piece, *opts["fade"])
        bbox = piece.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        if bbox:
            piece = piece.crop(bbox)
        scale = longest / max(piece.size)
        if scale < 1:
            piece = piece.resize((round(piece.width * scale), round(piece.height * scale)), Image.LANCZOS)
        dest = OUT / f"{name}.webp"
        piece.save(dest, "WEBP", quality=82, method=6)
        print(f"{name:16s} {piece.size[0]:4d}x{piece.size[1]:<4d} {dest.stat().st_size // 1024:4d} KB")


if __name__ == "__main__":
    main()
