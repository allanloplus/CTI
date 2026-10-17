"""把範本、台詞、角色圖（src/sprites）與語音組成單一 HTML 檔，可直接用瀏覽器開啟或離線使用。

用法：
  python3 tools/build.py                       動畫簡報 → index.html
  python3 tools/build.py --target game         闖關遊戲 → game/index.html
  python3 tools/build.py --fragment OUT        另外輸出不含 <html>/<head>/<body> 外殼的版本（供 Artifact 發布）
需要 Node.js（讀取 src/script.js）。
"""
import argparse
import base64
import json
import re
from pathlib import Path

from cti_script import line_key, load_lines, load_manifest, target

ROOT = Path(__file__).resolve().parent.parent
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


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def inline_sprites(text: str) -> str:
    cache = {}

    def repl(m):
        name = m.group(1)
        if name not in cache:
            cache[name] = data_uri(SPRITES / f"{name}.webp", "image/webp")
        return cache[name]

    out = re.sub(r"\{\{sprite:([a-z0-9-]+)\}\}", repl, text)
    print(f"內嵌精靈圖 {len(cache)} 張")
    return out


def audio_js(t) -> str:
    """只內嵌台詞與語音一致的句子；其餘在播放時改用瀏覽器語音。"""
    manifest = load_manifest(t)
    clips, missing = {}, []
    for ln in load_lines(t):
        m = manifest.get(ln["id"])
        mp3 = t["audio"] / f'{ln["id"]}.mp3'
        if m and m.get("key") == line_key(ln) and mp3.exists():
            clips[ln["id"]] = {"dur": m["dur"], "src": data_uri(mp3, "audio/mpeg")}
        else:
            missing.append(ln["id"])
    total = sum(c["dur"] for c in clips.values())
    print(f"內嵌語音 {len(clips)} 句，共 {total / 60:.1f} 分鐘")
    if missing:
        print(f"注意：{len(missing)} 句沒有對應語音，請執行 python3 tools/gen_audio.py：{', '.join(missing)}")
    return "window.CTI_AUDIO = " + json.dumps(clips, ensure_ascii=False, separators=(",", ":")) + ";"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default="show", help="show（動畫簡報）或 game（闖關遊戲）")
    ap.add_argument("--fragment", type=Path, help="另存不含外殼的版本")
    args = ap.parse_args()
    t = target(args.target)

    tpl = t["template"].read_text(encoding="utf-8")
    if HEAD_MARK not in tpl:
        raise SystemExit(f"範本缺少 {HEAD_MARK} 分隔標記")
    full = inline_sprites(tpl)
    left = re.findall(r"\{\{(?!SCRIPT_JS|AUDIO_JS)[^}]*\}\}", full)
    if left:
        raise SystemExit(f"未替換的佔位符：{left[:5]}")
    full = full.replace("/*{{SCRIPT_JS}}*/", t["script"].read_text(encoding="utf-8").strip())
    full = full.replace("/*{{AUDIO_JS}}*/", audio_js(t))
    head, body = full.split(HEAD_MARK, 1)

    out = t["out"]
    out.write_text(SHELL.format(head=head.strip(), body=body.strip()), encoding="utf-8")
    print(f"{out.relative_to(ROOT)}  {out.stat().st_size / 1024:.0f} KB")

    if args.fragment:
        args.fragment.parent.mkdir(parents=True, exist_ok=True)
        args.fragment.write_text(head.strip() + "\n" + body.strip() + "\n", encoding="utf-8")
        print(f"{args.fragment}  {args.fragment.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
