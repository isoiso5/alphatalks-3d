# Prepares a render job:
#  1. Microsoft Azure neural voiceover per scene (edge-tts, free) + exact word timings for captions
#  2. Stretches every scene to fit its narration
#  3. Builds the full soundtrack: voice + soft generated piano + whoosh/boom/impact sound effects
#  4. Writes props.json (final) and out/audio.wav, and prints chunk ranges for parallel rendering
import asyncio, json, math, os, subprocess, sys
import numpy as np
import edge_tts

VOICE = os.environ.get("TTS_VOICE", "en-US-AndrewNeural")
RATE = os.environ.get("TTS_RATE", "-5%")
FPS = 30
SR = 44100
CHUNKS = int(os.environ.get("CHUNKS", "16"))
VO_LEAD = 0.5
TITLE_LEAD = 4.6


def run(cmd):
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def read_audio(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"])
    return np.frombuffer(raw, dtype=np.float32).copy()


async def tts(text, path, rate=None):
    last = None
    for attempt in range(6):
        try:
            return await asyncio.wait_for(tts_once(text, path, rate or RATE), timeout=90)
        except Exception as e:  # network hiccups / NoAudioReceived
            last = e
            print(f"  tts retry {attempt + 1}: {e}", flush=True)
            await asyncio.sleep(3 + attempt * 4)
    raise last


async def tts_once(text, path, rate=RATE):
    words = []
    try:
        com = edge_tts.Communicate(text, VOICE, rate=rate, boundary="WordBoundary")
    except TypeError:
        com = edge_tts.Communicate(text, VOICE, rate=rate)
    with open(path, "wb") as f:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                s = chunk["offset"] / 1e7
                e = s + chunk["duration"] / 1e7
                words.append({"w": chunk["text"], "s": round(s, 3), "e": round(e, 3)})
    return words


def attach_punctuation(text, words):
    """edge-tts drops punctuation from boundaries; map original tokens back for nicer captions."""
    tokens = text.split()
    if len(tokens) == len(words):
        for t, w in zip(tokens, words):
            w["w"] = t
        return words
    out, ti = [], 0
    for w in words:
        clean = w["w"].strip(".,!?;:\"'").lower()
        while ti < len(tokens) and clean and clean not in tokens[ti].lower():
            ti += 1
        if ti < len(tokens):
            w = dict(w, w=tokens[ti])
            ti += 1
        out.append(w)
    return out


# ---------------- music + sfx synthesis ----------------

def note_freq(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def decay(t, rate):
    """exp(-rate*t) computed safely (clipped, finite)."""
    x = np.clip(-rate * np.asarray(t, dtype=np.float64), -60.0, 0.0)
    out = np.power(np.e, x)
    return np.nan_to_num(np.clip(out, 0.0, 1.0))


def piano_note(freq, dur, vel=0.25):
    n = int(dur * SR)
    t = np.arange(n, dtype=np.float64) / SR
    env = decay(t, 2.2) * (1 - decay(t, 300))
    sig = np.zeros(n)
    for h, a in [(1, 1.0), (2, 0.45), (3, 0.2), (4, 0.12), (5, 0.05)]:
        sig += a * np.sin(2 * np.pi * freq * h * t * (1 + 0.0004 * h)) * decay(t, h * 0.6)
    return np.nan_to_num(sig * env * vel)


MOODS = {
    # chords (MIDI), bass, arpeggio velocity, melody on/off
    "calm": ([[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]], [45, 41, 36, 43], 0.10, True),   # Am F C G
    "dark": ([[57, 60, 64], [57, 60, 65], [52, 55, 59], [52, 56, 59]], [33, 41, 40, 40], 0.075, False),  # Am Dm/A Em E
    "hope": ([[48, 52, 55], [55, 59, 62], [57, 60, 64], [53, 57, 60]], [36, 43, 45, 41], 0.11, True),   # C G Am F
    "rise": ([[53, 57, 60], [55, 59, 62], [57, 60, 64], [60, 64, 67]], [41, 43, 45, 48], 0.13, True),   # F G Am C
}


def make_piano(total_sec, mood_at=None):
    # soft cinematic piano at 64 bpm; mood_at(t) picks the chord set for each bar
    beat = 60 / 64
    bar = beat * 4
    out = np.zeros(int((total_sec + 6) * SR))
    rng = np.random.default_rng(3)
    t0 = 0.0
    i = 0
    while t0 < total_sec:
        prog, bass, vel, melody = MOODS.get(mood_at(t0) if mood_at else "calm", MOODS["calm"])
        chord = prog[i % 4]
        b = bass[i % 4]
        st = int(t0 * SR)
        seg = piano_note(note_freq(b), bar * 1.5, 0.22)
        out[st:st + len(seg)] += seg[: len(out) - st]
        # arpeggio
        pattern = [0, 1, 2, 1, 2, 1, 0, 2]
        for k, p in enumerate(pattern):
            ns = t0 + k * beat / 2
            s2 = int(ns * SR)
            if s2 >= len(out):
                break
            note = chord[p] + 12
            seg = piano_note(note_freq(note), beat * 2.5, vel + 0.03 * rng.random())
            out[s2:s2 + len(seg)] += seg[: len(out) - s2]
        # occasional high melody note
        if melody and i % 2 == 1:
            s3 = int((t0 + beat * 2) * SR)
            if s3 < len(out):
                seg = piano_note(note_freq(chord[2] + 24), beat * 4, 0.06)
                out[s3:s3 + len(seg)] += seg[: len(out) - s3]
        t0 += bar
        i += 1
    # simple reverb (feedback delays)
    for d, g in [(0.031, 0.35), (0.047, 0.3), (0.071, 0.25), (0.113, 0.2)]:
        k = int(d * SR)
        rev = np.zeros_like(out)
        rev[k:] = out[:-k] * g
        out += rev
    return out[: int(total_sec * SR)]


def whoosh(dur=0.9):
    n = int(dur * SR)
    t = np.arange(n) / SR
    noise = np.random.default_rng(1).standard_normal(n)
    # sweeping low-pass via moving average of changing width
    out = np.zeros(n)
    acc = 0.0
    for i in range(n):
        a = 0.02 + 0.25 * math.sin(math.pi * i / n)
        acc += a * (noise[i] - acc)
        out[i] = acc
    env = np.sin(np.pi * t / dur) ** 2
    return np.nan_to_num(out * env * 0.5)


def boom(dur=2.5):
    t = np.arange(int(dur * SR)) / SR
    f = 55 * decay(t, 1.5) + 30
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * decay(t, 1.6) * 0.7


def impact(dur=1.2):
    t = np.arange(int(dur * SR)) / SR
    low = np.sin(2 * np.pi * 70 * t) * decay(t, 5)
    noise = np.random.default_rng(2).standard_normal(len(t)) * decay(t, 18) * 0.25
    return (low + noise) * 0.6


def rain_bed(dur):
    n = int(dur * SR)
    noise = np.random.default_rng(5).standard_normal(n)
    k = 6
    sm = np.convolve(noise, np.ones(k) / k, mode="same")
    return np.nan_to_num((noise - sm) * 0.12 + sm * 0.05)


def thunder(dur=3.0):
    t = np.arange(int(dur * SR)) / SR
    noise = np.random.default_rng(9).standard_normal(len(t))
    k = 400
    low = np.convolve(noise, np.ones(k) / k, mode="same") * 18
    env = (1 - decay(t, 40)) * decay(t, 1.2)
    return np.nan_to_num(low * env * 0.8)


def add(buf, sig, at, gain=1.0):
    s = int(at * SR)
    if s >= len(buf) or s < 0:
        return
    e = min(len(buf), s + len(sig))
    buf[s:e] += sig[: e - s] * gain


async def main():
    props = json.load(open("props.json", encoding="utf-8"))
    os.makedirs("vo", exist_ok=True)
    os.makedirs("out", exist_ok=True)
    scenes = props["scenes"]
    vo_tracks = []
    for i, sc in enumerate(scenes):
        text = (sc.get("caption") or "").strip()
        lead = sc.get("lead")
        if lead is None:
            lead = TITLE_LEAD if (sc.get("chapterTitle") or sc.get("titleCard")) else VO_LEAD
        sc["voLead"] = lead
        if not text:
            vo_tracks.append(None)
            continue
        mp3 = f"vo/scene-{i}.mp3"
        words = await tts(text, mp3, props.get("ttsRate"))
        audio = read_audio(mp3)
        d = len(audio) / SR
        sc["voSec"] = round(d, 3)
        if words:
            sc["words"] = attach_punctuation(text, words)
        need = max(float(sc.get("durationSec") or 0), lead + d + float(sc.get("tail", 1.1)))
        sc["durationSec"] = round(math.ceil(need * FPS) / FPS, 6)
        vo_tracks.append(audio)
        print(f"scene {i:02d}: {d:5.1f}s narration -> {sc['durationSec']:.1f}s", flush=True)

    for sc in scenes:
        sc["durationSec"] = round(math.ceil(float(sc["durationSec"]) * FPS - 1e-6) / FPS, 6)
    frames = [max(1, int(round(sc["durationSec"] * FPS))) for sc in scenes]
    total_frames = sum(frames)
    total_sec = total_frames / FPS
    print(f"TOTAL: {total_frames} frames = {total_sec / 60:.1f} minutes", flush=True)

    # soundtrack
    voice = np.zeros(int(total_sec * SR) + SR)
    sfx = np.zeros_like(voice)
    start = 0
    for i, sc in enumerate(scenes):
        st = start / FPS
        if vo_tracks[i] is not None:
            add(voice, vo_tracks[i], st + sc["voLead"])
        if i > 0:
            add(sfx, whoosh(), st - 0.45, 0.35)
        if sc.get("chapterTitle") or sc.get("titleCard"):
            add(sfx, boom(), st + 0.2, 0.55)
        if sc.get("punch"):
            punch_at = sc.get("punchAt", max(1.2, sc["durationSec"] * 0.5))
            add(sfx, impact(), st + punch_at, 0.45)
        if sc.get("weather") == "rain" or sc.get("time") == "storm":
            add(sfx, rain_bed(frames[i] / FPS), st, 0.5)
        if sc.get("time") == "storm":
            seed = i
            for a in (1.4 + (seed % 3) * 0.7, 4.8 + (seed % 5) * 0.5):
                if a < frames[i] / FPS:
                    add(sfx, thunder(), st + a + 0.25, 0.6)
        start += frames[i]
    # mood timeline: a scene's "mood" applies from that scene until the next mood change
    marks, start, cur = [], 0, props.get("mood", "calm")
    for i, sc in enumerate(scenes):
        cur = sc.get("mood", cur)
        marks.append((start / FPS, cur))
        start += frames[i]

    def mood_at(t):
        m = marks[0][1] if marks else "calm"
        for st, md in marks:
            if st <= t:
                m = md
            else:
                break
        return m

    music = make_piano(len(voice) / SR, mood_at)
    music = np.pad(music, (0, max(0, len(voice) - len(music))))[: len(voice)]
    # duck music under voice
    w = SR // 5
    cs = np.concatenate([[0.0], np.cumsum(np.abs(voice))])
    idx = np.arange(len(voice))
    lo = np.clip(idx - w // 2, 0, len(voice))
    hi = np.clip(idx + w // 2, 0, len(voice))
    env = (cs[hi] - cs[lo]) / w
    duck = 1.0 - np.clip(env * 6, 0, 0.55)
    mix = np.nan_to_num(voice * 1.0 + music * 0.22 * duck + sfx)
    # fade out last 3 seconds
    fade = int(3 * SR)
    mix[-fade:] *= np.linspace(1, 0, fade)
    peak = np.max(np.abs(mix)) or 1
    mix = (mix / peak * 0.92).astype(np.float32)
    mix.tofile("out/audio.f32")
    run(["ffmpeg", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "out/audio.f32", "-ac", "2", "out/audio.wav"])
    os.remove("out/audio.f32")

    json.dump(props, open("props.json", "w", encoding="utf-8"))

    n = max(1, min(CHUNKS, math.ceil(total_frames / 600)))
    size = math.ceil(total_frames / n)
    chunks = []
    for c in range(n):
        a = c * size
        b = min(total_frames - 1, (c + 1) * size - 1)
        if a <= b:
            chunks.append({"i": c, "range": f"{a}-{b}"})
    with open(os.environ.get("GITHUB_OUTPUT", "/dev/null"), "a") as f:
        f.write("chunks=" + json.dumps(chunks) + "\n")
        f.write(f"minutes={total_sec / 60:.1f}\n")
    print("chunks:", chunks)


asyncio.run(main())
