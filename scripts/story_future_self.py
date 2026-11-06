import json

# "The Man From Year Ten" — Alphatalks3000, long video #5
# Angle: a broken man meets his future self in a dream among the stars. Each pillar is a "world" his
# future self shows him. Engine upgrade: montage cuts, new cameras (spin, drone, dolly, dutch, hero),
# slow motion, flashes, shake, particles (sparks, embers, fireflies, petals, confetti, fireworks, stars,
# god rays, aura, speed lines, shockwaves) and two new worlds (forest, cosmos).
# Music: three melodies — nocturne (the broken life), horizon (the journey), anthem (the comeback).
characters = {
    "dev": {"skin": "#b07a55", "shirt": "#3d4452", "pants": "#1e222b", "hair": "short", "hairColor": "#17110c",
            "sleeves": True, "eyeColor": "#2b1a0f"},
    "future": {"skin": "#b07a55", "shirt": "#e9e2d0", "pants": "#2a2620", "hair": "short", "hairColor": "#6e6e6e",
               "beard": True, "eyeColor": "#2b1a0f", "height": 1.02},
    "amara": {"skin": "#7a4e33", "shirt": "#2f7d6d", "pants": "#252a33", "hair": "bun", "hairColor": "#120b07", "eyeColor": "#24150b"},
    "kid": {"skin": "#b07a55", "shirt": "#f2b134", "pants": "#2a3550", "hair": "afro", "hairColor": "#17110c", "height": 0.68},
    "boss": {"skin": "#e3bfa0", "shirt": "#2b2f3a", "pants": "#1a1c22", "hair": "short", "hairColor": "#4a3a2a", "sleeves": True},
    "rico": {"skin": "#c49572", "shirt": "#8a2c2c", "pants": "#1d1d1d", "hair": "cap", "hairColor": "#111", "beard": True},
}

def S(env, caption, cast=None, camera="wide", **kw):
    d = {"env": env, "durationSec": 4, "caption": caption, "camera": camera}
    if cast:
        d["cast"] = cast
    d.update(kw)
    return d

C = lambda who, action, **kw: dict({"who": who, "action": action}, **kw)
sh = lambda at, camera, **kw: dict({"at": at, "camera": camera}, **kw)

scenes = [
    # ---------- COLD OPEN ----------
    S("cosmos", "Imagine you fall asleep one night, and you wake up somewhere you have never been. No ground. No sky. Just stars.",
      [C("dev", "lie", pos=[0, 0], y=0.05)], "drone", fade=True, fx=["stars"], mood="dark", music="nocturne",
      shots=[sh(4.5, "spin", zoom=0.9)]),
    S("cosmos", "And standing in front of you is a man with your face. Older. Stronger. Calm in a way you have never been.",
      [C("dev", "wakeup", pos=[-0.9, 0.3], face=60), C("future", "idle", pos=[1.0, 0.3], face=-60)], "dolly", focus=1,
      fx=["aura", "stars"], color="#f5c451", shots=[sh(3.6, "close", focus=0), sh(6.5, "hero", focus=1)],
      punch="It's you. Ten years from now.", punchAt=7.0, flash=True),
    S("cosmos", "He says one sentence. I came back because you're about to waste the next ten years. And I'm the only one who knows how to stop it.",
      [C("future", "idle2", pos=[0.4, 0.3], face=-20)], "push", fx=["aura", "stars"], color="#f5c451",
      shots=[sh(4.0, "dutch", focus=0)]),
    S("void", "", None, "wide", titleCard={"title": "The Man From Year Ten", "subtitle": "Alphatalks3000 presents"},
      durationSec=7, fx=["stars", "sparks"], flash=True),
    S("city", "Welcome to Alpha Talks 3000. Tonight's story is about Dev. And about the version of you that is waiting on the other side of your choices. Stay with it. The ending is for you.",
      [C("dev", "walktired", pos=[0, 6], to=[0, 1])], "track", time="night", weather="rain", tone="cold",
      shots=[sh(5.5, "drone"), sh(10, "low")]),

    # ---------- CHAPTER I — THE LOOP ----------
    S("room", "Dev was thirty two. He worked nights at a warehouse, slept through the mornings, and spent the afternoons on his phone.",
      [C("dev", "lie", pos=[0, 0.3], y=0.5)], "top", time="night", tone="cold", chapterLabel="Chapter I",
      chapterTitle="The Loop", color="#8aa0c8", shots=[sh(4.5, "dutch")]),
    S("kitchen", "He ate when he was bored. Energy drinks at three in the morning. Fast food at noon. Something sweet before bed. Every single day.",
      [C("dev", "cook", pos=[0, 0.4], face=180)], "wide", time="night", tone="cold",
      shots=[sh(2.6, "close", camAngle=30), sh(5.2, "top"), sh(7.8, "side")]),
    S("city", "On weekends there was Rico. Rico always had a plan. A party. A bottle. Something that made Saturday disappear and Sunday hurt.",
      [C("rico", "wave", pos=[-1, 0.8], face=40), C("dev", "idle2", pos=[1, 0.8], face=-40)], "orbit", time="night",
      tone="cold", fx=["embers"], color="#ff6a2a", shots=[sh(4.6, "dutch", focus=1)]),
    S("gym", "He had a gym membership. He paid for it every month for three years. He went four times. The card was still in his wallet, like a promise he kept breaking.",
      [C("dev", "idle2", pos=[0, 0.5], face=180)], "push", time="night", tone="cold", shots=[sh(5.0, "dutch")]),
    S("room", "The worst part wasn't the weight he gained, or the money he wasted. It was the voice. Every morning it said the same thing. Tomorrow. You'll start tomorrow.",
      [C("dev", "seated", pos=[0, 0.4], face=180)], "close", time="dawn", tone="cold", punch="Tomorrow.", punchAt=9.6),
    S("room", "And then there was Amara. His girlfriend. Six years together. She used to laugh at everything he said. Now she mostly waited for him to look up.",
      [C("amara", "seated", pos=[-1, 0.4], face=40), C("dev", "seated", pos=[1, 0.4], face=-140)], "wide", time="dusk",
      tone="cold", shots=[sh(4.8, "close", focus=0), sh(8.2, "close", focus=1, camAngle=-30)]),
    S("room", "One night she said it quietly. Dev, I don't need you to be perfect. I need you to be here. And he said, I'm right here. Without looking up.",
      [C("amara", "idle2", pos=[-0.9, 0.5], face=60), C("dev", "seated", pos=[0.9, 0.4], face=-140)], "push", time="night",
      tone="cold", punch="Without looking up.", punchAt=9.0),
    S("room", "That was the night he fell asleep and woke up among the stars.",
      [C("dev", "liedown", pos=[0, 0.3], y=0.5)], "crane", time="night", tone="cold", fx=["stars"]),

    # ---------- CHAPTER II — THE DEAL ----------
    S("cosmos", "Who are you, Dev asked. You already know, said the older man. I'm what happens if you change three things. Just three.",
      [C("dev", "idle2", pos=[-0.9, 0.3], face=60), C("future", "idle", pos=[0.9, 0.3], face=-60)], "orbit",
      fx=["aura", "stars"], color="#f5c451", chapterLabel="Chapter II", chapterTitle="The Deal", music="horizon", mood="hope",
      shots=[sh(5.8, "close", focus=1)]),
    S("cosmos", "And what happens if I don't? The older man didn't answer. He just turned around. And the stars behind him went dark.",
      [C("future", "idle", pos=[0, 0.3], face=180)], "push", fx=["stars"], tone="cold", mood="dark", shake=0.3,
      punch="The stars went dark.", punchAt=6.0),
    S("cosmos", "Okay, said Dev. Show me. And the platform under his feet began to fall.",
      [C("dev", "idle", pos=[-0.6, 0.3], face=30), C("future", "idle2", pos=[0.6, 0.3], face=-30)], "spin",
      fx=["stars", "speed"], shake=0.6, flash=True, mood="rise", punch="Show me.", punchAt=1.6),

    # ---------- CHAPTER III — WORLD ONE: THE FAST ----------
    S("forest", "He landed in a forest at night. Silent. Glowing. The air was so clean it felt like drinking cold water.",
      [C("dev", "getup", pos=[0, 0.5], face=180)], "drone", time="night", fx=["fireflies"], chapterLabel="World I",
      chapterTitle="The Fast", color="#9dffcf", flash=True, mood="calm", shots=[sh(5.0, "hero")]),
    S("forest", "This is the first world, said his future self. Every animal here eats, and then it stops. It rests. It lets the body clean itself. Only humans eat all day long.",
      [C("future", "walkslow", pos=[-2, 1.5], to=[1, 0.5]), C("dev", "walkslow", pos=[-3, 2.4], to=[0, 1.4])], "track",
      time="night", fx=["fireflies"], shots=[sh(6.0, "side"), sh(10.5, "close")]),
    S("forest", "Your hunger isn't hunger, Dev. It's habit. Give your body a window to eat, and a long night to heal. Sixteen hours. That's where the energy comes from.",
      [C("future", "idle", pos=[0, 0.5], face=180)], "push", time="night", fx=["fireflies", "godrays"],
      punch="FAST.", punchAt=11.5, flash=True),
    S("forest", "The first week will feel like a fight. By the third week, your mind will feel like this forest. Quiet. Awake. Clear.",
      [C("dev", "meditate", pos=[0, 0.5], face=180)], "spin", time="night", fx=["fireflies", "aura"], color="#9dffcf",
      tone="warm", punch="Quiet. Awake. Clear."),

    # ---------- CHAPTER IV — WORLD TWO: THE TRAIN ----------
    S("forest", "Dev asked, what if I'm too weak for it? His future self laughed. You fasted for nine hours last night while you slept. You're not too weak. You're just not used to choosing it.",
      [C("dev", "idle2", pos=[-0.8, 0.5], face=50), C("future", "idle", pos=[0.8, 0.5], face=-50)], "orbit", time="night",
      fx=["fireflies"], shots=[sh(5.2, "close", focus=1)], punch="Choose it."),
    S("stadium", "Then the forest was gone. He was standing in an empty stadium under white lights. And somebody was already running.",
      [C("future", "sprint", pos=[-6, 1], to=[6, 1])], "side", time="night", fx=["speed"], chapterLabel="World II",
      chapterTitle="The Train", color="#ffd45e", flash=True, music="anthem", mood="rise",
      shots=[sh(4.0, "low"), sh(7.0, "hero")]),
    S("stadium", "It was him. Ten years older and faster than he had ever been. Your body is not getting old, his future self said. It is getting ignored.",
      [C("future", "idle", pos=[0.6, 0.4], face=-30), C("dev", "walktired", pos=[-3, 1.4], to=[-0.6, 0.5])], "orbit",
      time="night", punch="Not old. Ignored.", punchAt=9.4, shots=[sh(5.5, "close", focus=0)]),
    S("gym", "Push ups in the morning. A walk at lunch. Weights three times a week. Nobody becomes strong in one day. You become strong in one day, repeated.",
      [C("dev", "pushups", pos=[0, 0.5], face=90)], "low", time="night", fx=["sparks"], color="#ffb347",
      shots=[sh(3.2, "side"), sh(6.2, "top"), sh(9.0, "close")]),
    S("gym", "Dev hit the bag. Once. Twice. And for the first time in years, he felt his own power coming back up through his arms.",
      [C("dev", "punch", pos=[0, 0.5], face=90, gloves="#c0392b", speed=1.0)], "dolly", time="night",
      fx=["sparks", "shockwave"], color="#ffd45e", slowmo=0.45, shake=0.35,
      shots=[sh(3.8, "hero"), sh(7.2, "spin")], punch="One day, repeated.", punchAt=8.6, flash=True),
    S("stadium", "He started running. Slow at first. Then faster. And his future self ran next to him, matching every step.",
      [C("dev", "run", pos=[-7, 1.4], to=[7, 1.4]), C("future", "run", pos=[-7.6, 0.4], to=[6.4, 0.4])], "track",
      time="night", fx=["speed"], shots=[sh(4.2, "side"), sh(7.6, "hero")], punch="TRAIN.", punchAt=8.4, flash=True),

    # ---------- CHAPTER V — WORLD THREE: THE PROTECT ----------
    S("stadium", "When they stopped, Dev was bent over, breathing hard. His future self put a hand on his shoulder. That feeling you hate right now? That is the feeling of you coming back.",
      [C("dev", "crouch", pos=[0, 0.5], face=180), C("future", "idle", pos=[1, 0.4], face=-60)], "low", time="night",
      tone="warm", fx=["godrays"], shots=[sh(5.8, "close", focus=1)], punch="That's you coming back."),
    S("city", "The third world looked like home. His street, at night. And outside the bar on the corner, Rico was waiting.",
      [C("rico", "wave", pos=[1.4, 0.5], face=-40), C("dev", "walkslow", pos=[-3, 3], to=[-0.8, 1])], "track",
      time="night", tone="cold", chapterLabel="World III", chapterTitle="The Protect", color="#ff7a7a", mood="dark",
      flash=True, shots=[sh(5.0, "dutch", focus=0)]),
    S("city", "This is the hardest world, his future self said. Here, the harm doesn't look like harm. It looks like a friend. It looks like a fun night. It looks like just one more.",
      [C("future", "idle", pos=[-1.2, 1.6], face=40), C("rico", "idle2", pos=[1.4, 0.5], face=-40)], "orbit",
      time="night", tone="cold", fx=["embers"], shots=[sh(6.5, "close", focus=1, camAngle=20)]),
    S("city", "Protect your body from the poison. Protect your mind from the people who keep you small. And never become the harm in somebody else's life.",
      [C("dev", "idle", pos=[0, 0.8], face=180)], "push", time="night", fx=["aura"], color="#ff7a7a",
      punch="PROTECT.", punchAt=10.0, flash=True),
    S("city", "Dev looked at Rico. Then he looked at the bar. And for the first time, he said no. Not angry. Just done.",
      [C("dev", "backoff", pos=[0, 0.8], face=180), C("rico", "idle2", pos=[1.4, 0.2], face=-40)], "dolly",
      time="night", slowmo=0.55, shots=[sh(4.0, "close", focus=1), sh(6.8, "hero")], punch="Not angry. Just done.", punchAt=6.8),
    S("room", "Then the last thing. His future self showed him Amara. Sitting alone. Waiting for a man who was always somewhere else.",
      [C("amara", "seated", pos=[0, 0.4], face=180)], "push", time="night", tone="cold", weather="rain"),
    S("room", "Protecting yourself also means protecting the people who love you. From your absence. From your phone. From the version of you that never shows up.",
      [C("amara", "seated", pos=[0, 0.4], face=180)], "close", time="night", tone="cold", punch="Protect them from your absence."),

    # ---------- CHAPTER VI — THE RETURN ----------
    S("room", "Dev sat down next to her, even though she couldn't see him. I'm sorry, he whispered. I'm going to come home. For real this time.",
      [C("amara", "seated", pos=[-0.6, 0.4], face=180), C("dev", "seated", pos=[0.6, 0.4], face=180)], "push", time="night",
      tone="cold", weather="rain", slowmo=0.7, punch="I'm coming home."),
    S("cosmos", "Back among the stars, his future self looked tired. I can't stay, he said. I only exist if you choose me. Every morning. Again and again.",
      [C("future", "idle", pos=[0.8, 0.3], face=-40), C("dev", "idle2", pos=[-0.8, 0.3], face=40)], "orbit",
      fx=["stars", "aura"], color="#f5c451", chapterLabel="Chapter VI", chapterTitle="The Return", mood="calm",
      shots=[sh(5.6, "close", focus=0)]),
    S("cosmos", "And then he began to fade. Light, from the feet up. Until only his voice was left. Fast. Train. Protect. I'll be waiting.",
      [C("dev", "idle", pos=[0, 0.3], face=180)], "spin", fx=["stars", "sparks", "godrays"], slowmo=0.6,
      punch="I'll be waiting.", punchAt=8.4, flash=True),
    S("room", "Dev woke up at five in the morning. His phone was on the floor. For the first time in years, he didn't pick it up.",
      [C("dev", "wakeup", pos=[0, 0.3], y=0.5)], "crane", time="dawn", tone="warm", flash=True, music="horizon", mood="hope",
      punch="He didn't pick it up.", punchAt=7.6),

    # ---------- CHAPTER VII — THE YEAR ----------
    S("road", "Day one, he walked for twenty minutes before the sun came up. It was boring. It was cold. He did it anyway.",
      [C("dev", "walk", pos=[-4, 1], to=[4, 1])], "track", time="dawn", chapterLabel="Chapter VII",
      chapterTitle="The Year", color="#ffd45e", shots=[sh(4.6, "drone")]),
    S("kitchen", "He ate at noon. He ate again at seven. And then he closed the kitchen. The cravings screamed for nine days. On day ten, they whispered.",
      [C("dev", "cook", pos=[0, 0.4], face=180)], "push", time="day", tone="warm",
      shots=[sh(4.4, "top"), sh(8.0, "close")], punch="Day ten, they whispered."),
    S("gym", "Week three, five push ups became fifteen. Month two, he could run a mile without stopping. Month four, he stopped counting.",
      [C("dev", "pushups", pos=[-1.2, 0.5], face=90), C("dev", "run", pos=[2.2, 1.2], to=[2.2, -1])], "wide", time="day",
      fx=["sparks"], shots=[sh(3.0, "side", focus=0), sh(5.8, "track", focus=1), sh(8.6, "hero", focus=1)]),
    S("city", "Rico called every Friday. Every Friday Dev said, not this week. After a while, Rico stopped calling. It hurt. And it was the right thing.",
      [C("dev", "walk", pos=[-3, 1], to=[3, 1])], "side", time="dusk", tone="warm", punch="It hurt. It was right."),
    S("room", "And every night, the phone went in a drawer. He cooked with Amara. He asked about her day and actually listened to the answer.",
      [C("amara", "idle2", pos=[-0.8, 0.5], face=50), C("dev", "idle", pos=[0.8, 0.5], face=-50)], "orbit", time="dusk",
      tone="warm", fx=["fireflies"]),
    S("room", "One night she laughed at something he said. The old laugh. The one he hadn't heard in years. And he realised that was the real reward.",
      [C("amara", "cheer", pos=[-0.7, 0.5], face=40), C("dev", "idle2", pos=[0.7, 0.5], face=-40)], "close", tone="warm",
      fx=["petals"], punch="The old laugh.", punchAt=5.0),

    # ---------- CHAPTER VIII — YEAR TEN ----------
    S("stage", "At the end of the year, Amara dragged him to a small concert in the park. He danced. Badly. Happily. Without checking his phone once.",
      [C("dev", "cheer", pos=[0.6, 0.5], face=-30), C("amara", "cheer", pos=[-0.6, 0.5], face=30)], "spin", tone="warm",
      fx=["confetti"], mood="rise", shots=[sh(5.0, "hero", focus=1)], punch="Badly. Happily."),
    S("road", "He was not a new man. He was the same man, finally pointed in the right direction. And every morning, he chose the future again.",
      [C("dev", "run", pos=[-4, 1], to=[4, 1])], "drone", time="dawn", tone="warm", fx=["godrays"]),
    S("summit", "Ten years later, a man with grey in his beard climbed a mountain at sunrise. Strong. Clear. Calm in a way he had never been.",
      [C("future", "walk", pos=[-3, 2], to=[0, 0])], "drone", time="dawn", tone="warm", chapterLabel="Chapter VIII",
      chapterTitle="Year Ten", color="#ffd45e", music="anthem", mood="rise", fx=["godrays"], flash=True,
      shots=[sh(5.4, "hero")]),
    S("summit", "Behind him, a little boy was climbing too. His son. Slower. Stubborn. Refusing to be carried.",
      [C("future", "idle", pos=[0.6, 0], face=-150), C("kid", "walk", pos=[-2.6, 2.2], to=[-0.6, 0.6])], "crane",
      time="dawn", tone="warm", shots=[sh(4.2, "close", focus=1)]),
    S("summit", "At the top, the boy asked him, Dad, how did you get so strong? And he smiled, because he remembered a night among the stars.",
      [C("future", "idle2", pos=[0.6, 0], face=-60), C("kid", "idle", pos=[-0.6, 0.3], face=60)], "close", time="dawn",
      tone="warm", fx=["godrays"], shots=[sh(4.6, "close", focus=1), sh(7.2, "spin")]),
    S("summit", "I made a deal with the man I wanted to become. And I kept it. Every single morning.",
      [C("future", "cheer", pos=[0.4, 0], face=180), C("kid", "cheer", pos=[-0.8, 0.3], face=160)], "hero", time="dawn",
      tone="warm", fx=["fireworks", "confetti"], slowmo=0.6, punch="I kept it. Every morning.", punchAt=3.6, flash=True,
      shots=[sh(3.6, "drone")]),

    # ---------- OUTRO ----------
    S("cosmos", "Here is the truth. The future version of you is already out there. Stronger. Clearer. Waiting. But he only exists if you choose him.",
      [C("future", "idle", pos=[0, 0.3], face=180)], "spin", fx=["stars", "aura"], color="#f5c451", mood="calm",
      punch="He only exists if you choose him."),
    S("void", "Fast, so your body can heal. Train, so your strength comes back. Protect, so the harm never gets back in.",
      [C("dev", "idle", pos=[0, 2.2], face=180)], "crane", pillars=3, fx=["sparks"], punch="Fast. Train. Protect."),
    S("void", "This is Alpha Talks 3000. If this story hit you, send it to the person who needs to meet their future self. And start tomorrow morning.",
      [C("dev", "idle", pos=[-0.8, 2.2], face=20), C("future", "idle2", pos=[0.8, 2.2], face=-20)], "push", pillars=3,
      durationSec=10, fx=["stars", "sparks"], titleCard={"title": "Fast. Train. Protect.", "subtitle": "Alphatalks3000"}),
]

story = {
    "title": "The Man From Year Ten — Alphatalks3000",
    "mood": "dark",
    "characters": characters,
    "scenes": scenes,
    "thumbnail": {"text": "HE MET HIMSELF 10 YEARS LATER", "sub": "And got one warning", "scene": 1, "at": 7.5},
}
json.dump(story, open("stories/future-self.json", "w"), indent=1)
words = sum(len((s.get("caption") or "").split()) for s in scenes)
print("scenes", len(scenes), "words", words, "est minutes", round(words / 2.25 / 60 + len(scenes) * 1.6 / 60 + 9 * 4 / 60, 1))
