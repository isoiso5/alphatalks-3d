import json

# "Day 30" — Alphatalks3000 Short (9:16, ~55s)
# One character, one month, three rules. Hook in the first second, loop-able ending.
characters = {
    "nia": {"skin": "#8a5a3c", "shirt": "#e9b949", "pants": "#1d2230", "hair": "afro", "hairColor": "#1a110b", "sleeves": True},
}

def S(env, caption, cast, camera, **kw):
    d = {"env": env, "durationSec": 3, "caption": caption, "camera": camera, "cast": cast, "lead": 0.15, "tail": 0.35}
    d.update(kw)
    return d

C = lambda action, **kw: dict({"who": "nia", "action": action}, **kw)

scenes = [
    S("room", "Day one. Two in the morning. Nia can't sleep, can't focus, and can't remember the last time she felt proud of herself.",
      [C("lie", pos=[-2, -2], y=0.45, face=180)], "top", time="night", lead=0.05, fade=False, zoom=0.75,
      hook="She changed 3 things for 30 days"),
    S("kitchen", "So she made three rules. One. No food until noon.",
      [C("seated", pos=[0, 0.55], face=180)], "push", time="dawn", punch="FAST.", punchAt=1.6),
    S("gym", "Two. Move your body every single day. Even when you don't feel like it.",
      [C("pushups", pos=[-0.8, 0.5], face=90)], "wide", zoom=0.6, camAngle=60, punch="TRAIN.", punchAt=1.8),
    S("city", "Three. Stop the harm. The midnight scrolling. The people who drag you down. The voice that calls you weak.",
      [C("walkslow", pos=[0, 6], to=[0, 1])], "track", time="night", punch="PROTECT.", punchAt=3.2),
    S("road", "Week one hurt. Week two got quiet. By week three, she was running before the sun came up.",
      [C("run", pos=[-5, 1], to=[5, 1])], "track", time="dawn"),
    S("void", "Food tasted like food again. Her head felt clean. Her mornings finally belonged to her.",
      [C("meditate", pos=[0, 2.2], face=180)], "orbit", pillars=3),
    S("summit", "Day thirty. Same girl. Different life.",
      [C("cheer", pos=[0, 0], face=180)], "crane", time="dawn", punch="Same girl. Different life.", punchAt=0.9, tail=1.4),
    S("void", "Your day one is tomorrow. Follow Alpha Talks 3000 for the system.",
      [C("idle", pos=[0, 2.2], face=180)], "push", pillars=3, durationSec=5, lead=0.3, tail=0.8,
      titleCard={"title": "Fast. Train. Protect.", "subtitle": "Alphatalks3000"}),
]

story = {
    "title": "Day 30 — Alphatalks3000",
    "ttsRate": "+3%",
    "characters": characters,
    "scenes": scenes,
    "thumbnail": {"text": "DAY 30", "sub": "Same girl. Different life.", "scene": 6, "at": 1.5},
}
json.dump(story, open("stories/day-thirty.json", "w"), indent=1)
words = sum(len((s.get("caption") or "").split()) for s in scenes)
print("scenes", len(scenes), "words", words, "est seconds", round(words / 2.6 + len(scenes) * 0.6))
