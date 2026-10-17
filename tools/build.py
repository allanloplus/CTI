"""把 src/template.html 與 src/sprites/*.webp 組成單一 HTML 檔。

用法：
  python3 tools/build.py                 產生 index.html（完整文件，可直接用瀏覽器開啟或離線播放）
  python3 tools/build.py --fragment OUT  另外輸出不含 <html>/<head>/<body> 外殼的版本（供 Artifact 發布）
"""
import argparse
import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "src" / "template.html"
SPRITES = ROOT / "src" / "sprites"
HEAD_MARK = "<!-- /head -->"

SHELL = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
{head}
</head>
<body>
{body}
</body>
</html>
"""


def inline_sprites(text: str) -> str:
    cache = {}

    def repl(m):
        name = m.group(1)
        if name not in cache:
            data = (SPRITES / f"{name}.webp").read_bytes()
            cache[name] = "data:image/webp;base64," + base64.b64encode(data).decode("ascii")
        return cache[name]

    out = re.sub(r"\{\{sprite:([a-z0-9-]+)\}\}", repl, text)
    left = re.findall(r"\{\{[^}]*\}\}", out)
    if left:
        raise SystemExit(f"未替換的佔位符：{left[:5]}")
    print(f"內嵌精靈圖 {len(cache)} 張：{', '.join(sorted(cache))}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fragment", type=Path, help="另存不含外殼的版本")
    args = ap.parse_args()

    tpl = TEMPLATE.read_text(encoding="utf-8")
    if HEAD_MARK not in tpl:
        raise SystemExit(f"範本缺少 {HEAD_MARK} 分隔標記")
    full = inline_sprites(tpl)
    head, body = full.split(HEAD_MARK, 1)

    out = ROOT / "index.html"
    out.write_text(SHELL.format(head=head.strip(), body=body.strip()), encoding="utf-8")
    print(f"index.html  {out.stat().st_size / 1024:.0f} KB")

    if args.fragment:
        args.fragment.parent.mkdir(parents=True, exist_ok=True)
        args.fragment.write_text(head.strip() + "\n" + body.strip() + "\n", encoding="utf-8")
        print(f"{args.fragment}  {args.fragment.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
