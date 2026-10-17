"""讀取 src/script.js 的串場台詞，供 gen_audio.py 與 build.py 共用。"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "src" / "script.js"
AUDIO = ROOT / "src" / "audio"
MANIFEST = AUDIO / "manifest.json"


def load_lines():
    """回傳 [{id, who, face, text}]，id 為「場景id_兩位數序號」，例如 why_02。需要 Node.js。"""
    js = (
        "global.window={};require(process.argv[1]);const out=[];"
        "for(const [sid,lines] of Object.entries(window.CTI_SCRIPT)){lines.forEach((l,i)=>"
        "out.push({id:sid+'_'+String(i+1).padStart(2,'0'),who:l[0],face:l[1],text:l[2]}))}"
        "console.log(JSON.stringify(out))"
    )
    res = subprocess.run(["node", "-e", js, str(SCRIPT)], check=True, capture_output=True, text=True)
    return json.loads(res.stdout)


def line_key(line):
    return f'{line["who"]}|{line["text"]}'


def load_manifest():
    if not MANIFEST.exists():
        return {}
    return json.loads(MANIFEST.read_text(encoding="utf-8"))
