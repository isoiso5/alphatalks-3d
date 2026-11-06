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


def pad_note(freq, dur, vel=0.05):
    # soft string pad: detuned sines with a slow swell, gentle release
    n = int(dur * SR)
    t = np.arange(n, dtype=np.float64) / SR
    att = np.clip(t / (dur * 0.35), 0, 1)
    rel = np.clip((dur - t) / (dur * 0.3), 0, 1)
    env = np.sin(att * np.pi / 2) * rel
    sig = np.zeros(n)
    for det, a in [(-0.004, 0.5), (0.0, 0.7), (0.005, 0.5), (1.0, 0.18)]:
        f = freq * (2 if det == 1.0 else 1 + det)
        sig += a * np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 5.1 * t))
    return np.nan_to_num(sig * env * vel)


# Melody themes. Each theme: tempo, beats per bar, arpeggio pattern (chord-tone index per half-beat),
# per-mood progressions (chords, bass, arp velocity, melody on/off), an optional string pad,
# and a 4-bar melody phrase: (beat, tone, beats) where tone indexes the chord tones
# [root, third, fifth, root+12, third+12, fifth+12] played two octaves up; a float adds semitones.
THEMES = {
    # the original soft piano (Am F C G)
    "dawn": {
        "bpm": 64, "beats": 4, "pattern": [0, 1, 2, 1, 2, 1, 0, 2], "pad": False,
        "moods": MOODS,
        "phrase": [[], [(2, 2, 4)], [], [(2, 2, 4)]],
    },
    # 3/4 waltz on the water, D minor, rocking arpeggio
    "tide": {
        "bpm": 72, "beats": 3, "pattern": [0, 2, 3, 2, 1, 2], "pad": True,
        "moods": {
            "calm": ([[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]], [38, 34, 41, 36], 0.09, True),   # Dm Bb F C
            "dark": ([[50, 53, 57], [46, 50, 53], [45, 49, 52], [45, 49, 52]], [38, 34, 33, 33], 0.07, False),  # Dm Bb A A
            "hope": ([[46, 50, 53], [53, 57, 60], [48, 52, 55], [50, 53, 57]], [34, 41, 36, 38], 0.10, True),   # Bb F C Dm
            "rise": ([[46, 50, 53], [48, 52, 55], [53, 57, 60], [53, 57, 60]], [34, 36, 41, 41], 0.12, True),   # Bb C F F
        },
        "phrase": [[(0, 2, 2), (2, 1, 1)], [(0, 0, 3)], [(0, 1, 1), (1, 2, 1), (2, 3, 1)], [(0, 2, 3)]],
    },
    # warm and open, E major with the lifted IV (Lydian colour), slow and glowing
    "ember": {
        "bpm": 58, "beats": 4, "pattern": [0, 2, 3, 4, 3, 2, 1, 2], "pad": True,
        "moods": {
            "calm": ([[52, 56, 59], [57, 61, 64], [49, 52, 56], [57, 61, 64]], [40, 45, 37, 45], 0.09, True),   # E A C#m A
            "dark": ([[49, 52, 56], [45, 49, 52], [52, 56, 59], [47, 51, 54]], [37, 33, 40, 35], 0.07, False),  # C#m A E B
            "hope": ([[52, 56, 59], [47, 51, 54], [49, 52, 56], [57, 61, 64]], [40, 35, 37, 45], 0.10, True),   # E B C#m A
            "rise": ([[57, 61, 64], [59, 63, 66], [52, 56, 59], [52, 56, 59]], [45, 47, 40, 40], 0.12, True),   # A B E E
        },
        "phrase": [[(0, 2, 2), (2, 3, 2)], [(0, 1, 4)], [(0, 2, 1), (1, 1, 1), (2, 0, 2)], [(1, 1, 3)]],
    },
    # quiet night piano, G minor, falling melody that answers itself
    "nocturne": {
        "bpm": 60, "beats": 4, "pattern": [0, 2, 4, 2, 3, 2, 4, 2], "pad": False,
        "moods": {
            "calm": ([[55, 58, 62], [51, 55, 58], [46, 50, 53], [53, 57, 60]], [43, 39, 34, 41], 0.085, True),  # Gm Eb Bb F
            "dark": ([[55, 58, 62], [51, 55, 58], [50, 54, 57], [50, 54, 57]], [31, 39, 38, 38], 0.065, True),  # Gm Eb D D
            "hope": ([[46, 50, 53], [53, 57, 60], [51, 55, 58], [53, 57, 60]], [34, 41, 39, 41], 0.10, True),   # Bb F Eb F
            "rise": ([[51, 55, 58], [53, 57, 60], [46, 50, 53], [55, 58, 62]], [39, 41, 34, 43], 0.12, True),   # Eb F Bb Gm
        },
        "phrase": [[(0, 4, 1.5), (1.5, 3, 0.5), (2, 2, 2)], [(0, 1, 2), (2, 2, 2)],
                   [(0, 3, 1), (1, 2, 1), (2, 1, 1), (3, 2, 1)], [(0, 0, 4)]],
    },
    # building anthem, C major, steady pulse and a climbing hook (for comeback stories)
    "anthem": {
        "bpm": 70, "beats": 4, "pattern": [0, 2, 3, 2, 0, 2, 3, 2], "pad": True,
        "moods": {
            "calm": ([[48, 52, 55], [45, 48, 52], [53, 57, 60], [55, 59, 62]], [36, 33, 41, 43], 0.09, True),   # C Am F G
            "dark": ([[45, 48, 52], [53, 57, 60], [52, 55, 59], [52, 56, 59]], [33, 41, 40, 40], 0.07, False),  # Am F Em E
            "hope": ([[53, 57, 60], [48, 52, 55], [55, 59, 62], [45, 48, 52]], [41, 36, 43, 33], 0.11, True),   # F C G Am
            "rise": ([[53, 57, 60], [55, 59, 62], [52, 55, 59], [45, 48, 52]], [41, 43, 40, 45], 0.13, True),   # F G Em Am
        },
        "phrase": [[(0, 0, 1), (1, 1, 1), (2, 2, 2)], [(0, 3, 2), (2, 2, 2)],
                   [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)], [(0, 3, 4)]],
    },
    # bright and hopeful, F major in 6/8, flowing (for journeys and new beginnings)
    "horizon": {
        "bpm": 66, "beats": 6, "pattern": [0, 1, 2, 3, 2, 1], "pad": True,
        "moods": {
            "calm": ([[53, 57, 60], [50, 53, 57], [46, 50, 53], [48, 52, 55]], [41, 38, 34, 36], 0.09, True),   # F Dm Bb C
            "dark": ([[50, 53, 57], [46, 50, 53], [45, 48, 52], [45, 49, 52]], [38, 34, 33, 33], 0.07, False),  # Dm Bb Am A
            "hope": ([[46, 50, 53], [53, 57, 60], [48, 52, 55], [53, 57, 60]], [34, 41, 36, 41], 0.10, True),   # Bb F C F
            "rise": ([[46, 50, 53], [48, 52, 55], [50, 53, 57], [53, 57, 60]], [34, 36, 38, 41], 0.12, True),   # Bb C Dm F
        },
        "phrase": [[(0, 2, 3), (3, 3, 3)], [(0, 1, 6)], [(0, 2, 2), (2, 3, 2), (4, 4, 2)], [(0, 3, 6)]],
    },
    # tense, heartbeat-like, B minor with sparse low notes (for struggle and battles)
    "pulse": {
        "bpm": 76, "beats": 4, "pattern": [0, 0, 2, 0, 3, 0, 2, 0], "pad": True,
        "moods": {
            "calm": ([[47, 50, 54], [43, 47, 50], [50, 54, 57], [45, 49, 52]], [35, 31, 38, 33], 0.08, True),   # Bm G D A
            "dark": ([[47, 50, 54], [43, 47, 50], [42, 46, 49], [42, 46, 49]], [35, 31, 30, 30], 0.07, True),   # Bm G F# F#
            "hope": ([[43, 47, 50], [50, 54, 57], [45, 49, 52], [47, 50, 54]], [31, 38, 33, 35], 0.10, True),   # G D A Bm
            "rise": ([[43, 47, 50], [45, 49, 52], [50, 54, 57], [50, 54, 57]], [31, 33, 38, 38], 0.12, True),   # G A D D
        },
        "phrase": [[(0, 3, 1), (1, 2, 1), (2, 3, 2)], [(0, 4, 3)], [(0, 3, 1), (1, 2, 1), (2, 1, 2)], [(0, 0, 4)]],
    },
}
NEW_THEMES = ["tide", "ember", "nocturne", "anthem", "horizon", "pulse"]


def pick_theme(props):
    name = props.get("music")
    if name in THEMES:
        return name
    # no theme set: pick a new one from the title so each video sounds different
    key = sum(ord(c) for c in props.get("title", ""))
    return NEW_THEMES[key % len(NEW_THEMES)]


def make_piano(total_sec, mood_at=None, theme="dawn"):
    th = THEMES.get(theme, THEMES["dawn"])
    beat = 60 / th["bpm"]
    bar = beat * th["beats"]
    pattern = th["pattern"]
    step = bar / len(pattern)
    out = np.zeros(int((total_sec + 8) * SR))
    rng = np.random.default_rng(3)

    def put(seg, at):
        s = int(at * SR)
        if 0 <= s < len(out):
            out[s:s + len(seg)] += seg[: len(out) - s]

    t0, i = 0.0, 0
    while t0 < total_sec:
        prog, bass, vel, melody = th["moods"].get(mood_at(t0) if mood_at else "calm", th["moods"]["calm"])
        chord = prog[i % 4]
        tones = chord + [n + 12 for n in chord]
        put(piano_note(note_freq(bass[i % 4]), bar * 1.5, 0.22), t0)
        if th["pad"]:
            for n in chord:
                put(pad_note(note_freq(n), bar * 1.25, 0.0008), t0)
        for k, p in enumerate(pattern):
            put(piano_note(note_freq(tones[p] + 12), step * 5, vel + 0.03 * rng.random()), t0 + k * step)
        if melody:
            # play the phrase from the second time through each 8-bar section, so the theme breathes
            if theme == "dawn" or (i // 4) % 2 == 1:
                for b, tone, dur in th["phrase"][i % 4]:
                    ti = int(tone)
                    n = tones[min(ti, 5)] + 24 + round((tone - ti) * 10)
                    put(piano_note(note_freq(n), beat * dur + beat, 0.075 if theme != "dawn" else 0.06), t0 + b * beat)
        t0 += bar
        i += 1
    for d, g in [(0.031, 0.35), (0.047, 0.3), (0.071, 0.25), (0.113, 0.2), (0.173, 0.12)]:
        k = int(d * SR)
        rev = np.zeros_like(out)
        rev[k:] = out[:-k] * g
        out += rev
    return out[: int(total_sec * SR)]


def build_score(props, scenes, frames, total_sec, mood_at):
    """2-3 melodies per video. A scene's "music" field switches theme from that scene on.
    Without scene fields, props["music"] (a name or a list) is spread over chapter starts;
    with nothing set, 3 themes are picked from the title and placed at chapter starts near 0, 1/3, 2/3."""
    starts, t = [], 0.0
    for i in range(len(scenes)):
        starts.append(t)
        t += frames[i] / FPS
    marks = [(starts[i], sc["music"]) for i, sc in enumerate(scenes) if sc.get("music") in THEMES]
    if not marks:
        m = props.get("music")
        if isinstance(m, str) and m in THEMES:
            themes = [m]
        elif isinstance(m, list) and [x for x in m if x in THEMES]:
            themes = [x for x in m if x in THEMES][:3]
        else:
            key = sum(ord(c) for c in props.get("title", ""))
            k = key % len(NEW_THEMES)
            n = 3 if total_sec > 240 else 2
            themes = [NEW_THEMES[(k + j * 2) % len(NEW_THEMES)] for j in range(n)]
        chap = [starts[i] for i, sc in enumerate(scenes) if sc.get("chapterTitle")] or starts
        marks = [(0.0, themes[0])]
        for j in range(1, len(themes)):
            target = total_sec * j / len(themes)
            at = min(chap, key=lambda x: abs(x - target))
            if at > marks[-1][0] + 20:
                marks.append((at, themes[j]))
    if marks[0][0] > 0:
        marks[0] = (0.0, marks[0][1])
    props["music"] = [m for _, m in marks]
    print("music score:", [(round(a), m) for a, m in marks])
    out = np.zeros(int(total_sec * SR))
    xf = 3.0
    for j, (a, theme) in enumerate(marks):
        b = marks[j + 1][0] if j + 1 < len(marks) else total_sec
        s0 = max(0.0, a - xf / 2)
        s1 = min(total_sec, b + xf / 2)
        seg = make_piano(s1 - s0, lambda tt, s0=s0: mood_at(s0 + tt), theme)
        n = len(seg)
        env = np.ones(n)
        f = int(xf * SR)
        if j > 0:
            env[:f] = np.linspace(0, 1, min(f, n))[: min(f, n)]
        if j + 1 < len(marks):
            env[-f:] *= np.linspace(1, 0, f)[-min(f, n):]
        st = int(s0 * SR)
        out[st:st + n] += (seg * env)[: len(out) - st]
    return out


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

    music = build_score(props, scenes, frames, len(voice) / SR, mood_at)
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
