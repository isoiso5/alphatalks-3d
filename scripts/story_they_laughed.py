import json

# "They Laughed" — Alphatalks3000 Short (9:16, ~50s)
# Underdog hook, three rules, one-year payoff, loop back to the gym.
characters = {
    "theo": {"skin": "#c68e6a", "shirt": "#2b2f3a", "pants": "#15171d", "hair": "short", "hairColor": "#1b120c", "sleeves": True, "height": 1.02},
    "jay": {"skin": "#6e452c", "shirt": "#b23a3a", "pants": "#22252e", "hair": "cap", "hairColor": "#111111"},
    "max": {"skin": "#e2b48f", "shirt": "#3f6fb0", "pants": "#22252e", "hair": "short", "hairColor": "#6b4a2b"},
}

def S(env, caption, cast, camera, **kw):
    d = {"env": env, "durationSec": 3, "caption": caption, "camera": camera, "cast": cast, "lead": 0.15, "tail": 0.35}
    d.update(kw)
    return d

T = lambda action, **kw: dict({"who": "theo", "action": action}, **kw)
J = lambda action, **kw: dict({"who": "jay", "action": action}, **kw)
M = lambda action, **kw: dict({"who": "max", "action": action}, **kw)

scenes = [
    S("gym", "They laughed when Theo walked into the gym. Out of breath in five minutes. Gone in ten.",
      [T("walktired", pos=[0, 3], to=[0, 0.5]), J("cheer", pos=[-2.2, -1.2], face=40), M("idle2", pos=[2.2, -1.2], face=-40)],
      "push", lead=0.05, fade=False, zoom=0.8, tone="cold", mood="dark",
      hook="They laughed at him"),
    S("room", "That night, he made three rules. And he promised himself he would not break them.",
      [T("sitfloor", pos=[0, 0.5], face=180)], "low", time="night", tone="cold", zoom=0.8),
    S("kitchen", "One. Eat in an eight hour window. Fast the rest.",
      [T("cook", pos=[0, 0.4], face=180)], "push", time="dawn", punch="FAST.", punchAt=1.3, mood="hope"),
    S("gym", "Two. Show up every single day. Especially the days nobody is watching.",
      [T("punch", pos=[0, 0.5], face=90, gloves="#c9a227")], "side", zoom=0.75, punch="TRAIN.", punchAt=1.5),
    S("city", "Three. Cut the harm. The late night junk. The friends who mocked him. The voice that said quit.",
      [T("walk", pos=[0, 6], to=[0, 1])], "track", time="night", punch="PROTECT.", punchAt=3.4),
    S("road", "Month two, he was running past the gym before it even opened.",
      [T("run", pos=[-5, 1], to=[5, 1])], "track", time="dawn", tone="warm", mood="rise"),
    S("gym", "Month six, the heavy bag started to fear him.",
      [T("kick", pos=[0, 0.5], face=90, gloves="#c9a227")], "low", zoom=0.75, tone="warm"),
    S("gym", "One year later, the same guys who laughed came up to him and asked for his routine.",
      [T("idle", pos=[0, 0.3], face=180), J("walkslow", pos=[-3, 2.5], to=[-1.3, 1.2]), M("walkslow", pos=[3, 2.5], to=[1.3, 1.2])],
      "crane", tone="warm", punch="Same gym. Different man.", punchAt=4.2, tail=1.2),
    S("void", "This is the routine. Start it tonight. Follow Alpha Talks 3000 for the full system.",
      [T("guard", pos=[0, 2.2], face=180, gloves="#c9a227")], "push", pillars=3, durationSec=5, lead=0.3, tail=0.8,
      titleCard={"title": "Fast. Train. Protect.", "subtitle": "Alphatalks3000"}),
]

story = {
    "title": "They Laughed — Alphatalks3000",
    "ttsRate": "+4%",
    "characters": characters,
    "scenes": scenes,
    "thumbnail": {"text": "THEY LAUGHED", "sub": "One year later...", "scene": 7, "at": 2.0},
}
json.dump(story, open("stories/they-laughed.json", "w"), indent=1)
words = sum(len((s.get("caption") or "").split()) for s in scenes)
print("scenes", len(scenes), "words", words, "est seconds", round(words / 2.7 + len(scenes) * 0.6))
