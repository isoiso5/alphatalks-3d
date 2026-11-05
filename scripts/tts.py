# Generates one voiceover mp3 per scene with Microsoft Azure neural voices (edge-tts, free)
# and stretches each scene so it is at least as long as its narration.
import asyncio, json, os, subprocess, sys
import edge_tts

VOICE = os.environ.get("TTS_VOICE", "en-US-AndrewNeural")

def duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", path,
    ])
    return float(out.strip())

async def main():
    props = json.load(open("props.json", encoding="utf-8"))
    os.makedirs("public/vo", exist_ok=True)
    for i, sc in enumerate(props["scenes"]):
        text = (sc.get("caption") or "").strip()
        if not text or sc.get("voiceoverUrl"):
            continue
        rel = f"vo/scene-{i}.mp3"
        await edge_tts.Communicate(text, VOICE, rate="-5%").save(f"public/{rel}")
        d = duration(f"public/{rel}")
        sc["voiceoverFile"] = rel
        sc["durationSec"] = round(max(float(sc.get("durationSec") or 0), d + 0.8), 2)
        print(f"scene {i}: {d:.1f}s narration -> {sc['durationSec']}s")
    json.dump(props, open("props.json", "w", encoding="utf-8"))
    print("total seconds:", round(sum(s["durationSec"] for s in props["scenes"]), 1))

asyncio.run(main())
