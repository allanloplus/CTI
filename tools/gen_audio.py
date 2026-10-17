#!/usr/bin/env python3
"""依 src/script.js 的串場台詞，用 edge-tts 產生每句語音與 src/audio/manifest.json。

角色聲音（沿用教學動畫的慣例）：
    Allan 顧問 → zh-TW-YunJheNeural（台灣男聲，語速 +6%）
    阿拉蕾     → zh-TW-HsiaoYuNeural（台灣女聲，調高音調 +30Hz、語速 +12%）

用法：
    pip install edge-tts          另需 ffprobe（ffmpeg）與 Node.js
    python3 tools/gen_audio.py          只重新產生台詞有變動的句子
    python3 tools/gen_audio.py --all    全部重新產生
連線：edge-tts 會連到 speech.platform.bing.com（WebSocket，443 埠）。
"""
import asyncio
import json
import os
import re
import subprocess
import sys

from cti_script import AUDIO, MANIFEST, line_key, load_lines, load_manifest

VOICES = {
    "allan": dict(voice="zh-TW-YunJheNeural", rate="+6%", pitch="+0Hz"),
    "arale": dict(voice="zh-TW-HsiaoYuNeural", rate="+12%", pitch="+30Hz"),
}
CN = dict(zip("0123456789", "零一二三四五六七八九"))
digits = lambda s: "".join(CN[c] for c in s)

# 讓 TTS 用台灣顧問習慣的唸法（只影響語音，不影響畫面文字）
SAY = [
    (r"ISO/IEC", "ISO"),
    (r"27001:2022", "二七零零一 二零二二年版"),
    (r"27001", "二七零零一"),
    (r"27701", "二七七零一"),
    (r"A\.(\d)\.(\d+)", lambda m: f"A {CN[m[1]]}點{digits(m[2])}"),
    (r"(\d)\.(\d+)", lambda m: f"{CN[m[1]]}點{digits(m[2])}"),
    (r"(20\d\d) ?年", lambda m: digits(m[1]) + "年"),
    (r"\bP([1-4])\b", lambda m: "P " + CN[m[1]]),
    (r"CVSS", "C V S S"),
    (r"VPN", "V P N"),
    (r"SOC", "S O C"),
    (r"KPI", "K P I"),
    (r"ISAC", "I SAC"),
]


def tts_text(text):
    for pat, rep in SAY:
        text = re.sub(pat, rep, text)
    return text


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    return round(float(out), 3)


async def synth(line, path):
    import edge_tts
    v = VOICES[line["who"]]
    kw = {"proxy": os.environ["HTTPS_PROXY"]} if os.environ.get("HTTPS_PROXY") else {}
    for attempt in range(4):
        try:
            await edge_tts.Communicate(tts_text(line["text"]), v["voice"], rate=v["rate"], pitch=v["pitch"], **kw).save(str(path))
            return
        except Exception as e:  # 網路不穩時重試
            if attempt == 3:
                raise
            print(f"  retry {line['id']}: {e}")
            await asyncio.sleep(2 ** (attempt + 1))


async def main():
    ca = os.environ.get("SSL_CERT_FILE")  # 企業 proxy 自訂 CA
    if ca:
        import certifi
        certifi.where = lambda: ca

    regen_all = "--all" in sys.argv
    AUDIO.mkdir(parents=True, exist_ok=True)
    lines = load_lines()
    old = load_manifest()
    new = {}
    for ln in lines:
        path = AUDIO / f'{ln["id"]}.mp3'
        prev = old.get(ln["id"])
        if not regen_all and prev and prev.get("key") == line_key(ln) and path.exists():
            new[ln["id"]] = prev
            continue
        print(f'TTS {ln["id"]} [{ln["who"]}] {ln["text"][:28]}')
        await synth(ln, path)
        new[ln["id"]] = {"key": line_key(ln), "dur": duration(path)}

    for f in AUDIO.glob("*.mp3"):  # 移除已不存在的台詞音檔
        if f.stem not in new:
            f.unlink()

    MANIFEST.write_text(json.dumps(new, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    total = sum(v["dur"] for v in new.values())
    print(f"done: {len(new)} clips, {total / 60:.1f} min of speech")


if __name__ == "__main__":
    asyncio.run(main())
