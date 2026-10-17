"""讀取串場台詞與語音清單，供 gen_audio.py 與 build.py 共用。

兩個專案：
  show  動畫簡報   src/template.html + src/script.js       → index.html
  game  闖關遊戲   game/src/template.html + game/src/voice.js → game/index.html
  dash  戰情儀表板 dashboard/src/template.html + dashboard/src/voice.js → dashboard/index.html
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = {
    "show": {
        "template": ROOT / "src" / "template.html",
        "script": ROOT / "src" / "script.js",
        "audio": ROOT / "src" / "audio",
        "out": ROOT / "index.html",
    },
    "game": {
        "template": ROOT / "game" / "src" / "template.html",
        "script": ROOT / "game" / "src" / "voice.js",
        "audio": ROOT / "game" / "src" / "audio",
        "out": ROOT / "game" / "index.html",
    },
    "dash": {
        "template": ROOT / "dashboard" / "src" / "template.html",
        "script": ROOT / "dashboard" / "src" / "voice.js",
        "audio": ROOT / "dashboard" / "src" / "audio",
        "out": ROOT / "dashboard" / "index.html",
    },
}


def target(name="show"):
    if name not in TARGETS:
        raise SystemExit(f"未知的專案：{name}（可用：{', '.join(TARGETS)}）")
    t = dict(TARGETS[name])
    t["manifest"] = t["audio"] / "manifest.json"
    return t


def load_lines(t):
    """回傳 [{id, who, face, text}]，id 為「群組id_兩位數序號」，例如 why_02。需要 Node.js。"""
    js = (
        "global.window={};require(process.argv[1]);const out=[];"
        "for(const [sid,lines] of Object.entries(window.CTI_SCRIPT)){lines.forEach((l,i)=>"
        "out.push({id:sid+'_'+String(i+1).padStart(2,'0'),who:l[0],face:l[1],text:l[2]}))}"
        "console.log(JSON.stringify(out))"
    )
    res = subprocess.run(["node", "-e", js, str(t["script"])], check=True, capture_output=True, text=True)
    return json.loads(res.stdout)


def line_key(line):
    return f'{line["who"]}|{line["text"]}'


def load_manifest(t):
    if not t["manifest"].exists():
        return {}
    return json.loads(t["manifest"].read_text(encoding="utf-8"))
