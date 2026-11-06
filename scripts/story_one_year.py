import json

# "One Year" — Alphatalks3000, long video #4
# Viral angle: a doctor gives a father one year. His daughter's wedding is in one year.
# Open loop in the first 10 seconds (will he walk her down the aisle?), paid off in the final act.
# Engine upgrade for this video: characters now have faces (eyes, brows, nose, mouth, ears, beards).
characters = {
    "marcus": {"skin": "#9c6b48", "shirt": "#4a5568", "pants": "#1f2430", "hair": "short", "hairColor": "#1b1410",
               "sleeves": True, "beard": True, "eyeColor": "#2e1d10", "height": 1.03},
    "zara": {"skin": "#a87452", "shirt": "#e8d6c0", "pants": "#3a3f4b", "hair": "bun", "hairColor": "#140d08", "eyeColor": "#3b2414"},
    "doc": {"skin": "#e6c3a2", "shirt": "#f2f4f6", "pants": "#3b4a5c", "hair": "short", "hairColor": "#8d8d8d", "sleeves": True, "eyeColor": "#3d5a73"},
    "ruth": {"skin": "#6e472f", "shirt": "#c0392b", "pants": "#222831", "hair": "afro", "hairColor": "#d9d9d9", "height": 0.92, "eyeColor": "#24160c"},
    "leo": {"skin": "#d9a882", "shirt": "#2e7d5b", "pants": "#1d2228", "hair": "cap", "hairColor": "#1a1a1a", "eyeColor": "#4a3320"},
    "vince": {"skin": "#c79a78", "shirt": "#6b2d2d", "pants": "#222", "hair": "short", "hairColor": "#3a2a1a", "sleeves": True, "beard": True},
}

def S(env, caption, cast=None, camera="wide", **kw):
    d = {"env": env, "durationSec": 4, "caption": caption, "camera": camera}
    if cast:
        d["cast"] = cast
    d.update(kw)
    return d

C = lambda who, action, **kw: dict({"who": who, "action": action}, **kw)

scenes = [
    # ---------- COLD OPEN (hook + open loop) ----------
    S("room", "The doctor didn't look up from the paper. He just said it. Marcus, if nothing changes, you have about one year.",
      [C("marcus", "seated", pos=[0.6, 0.4], face=-30), C("doc", "idle2", pos=[-1.1, 0.2], face=60)], "push",
      time="night", tone="cold", mood="dark", fade=True, punch="One year.", punchAt=5.2),
    S("room", "One year. That was exactly how long it was until his daughter's wedding. And she had already asked him to walk her down the aisle.",
      [C("marcus", "seated", pos=[0, 0.4], face=180)], "close", time="night", tone="cold"),
    S("road", "That night he sat in his car for two hours. He didn't cry. He didn't call anyone. He just asked himself one question.",
      [C("marcus", "idle2", pos=[0, 1], face=180)], "low", time="night", tone="cold", weather="rain"),
    S("void", "Am I going to be there?", [C("marcus", "idle", pos=[0, 2.2], face=180)], "push",
      punch="Am I going to be there?", punchAt=0.6, durationSec=5, tone="cold"),
    S("void", "", None, "wide", titleCard={"title": "One Year", "subtitle": "Alphatalks3000 presents"}, durationSec=7, mood="calm"),
    S("city", "Welcome to Alpha Talks 3000. This is the story of a father, a deadline, and three simple rules that gave a man his life back. Stay until the end. You'll want to see that wedding.",
      [C("marcus", "walkslow", pos=[0, 5], to=[0, 1])], "track", time="dusk"),

    # ---------- CHAPTER I — THE MAN HE BECAME ----------
    S("kitchen", "Marcus wasn't a bad man. He was a tired man. Forty six years old. Two jobs. Twenty years of eating whatever was fast and whatever was there.",
      [C("marcus", "cook", pos=[0, 0.4], face=180)], "wide", time="night", chapterLabel="Chapter I",
      chapterTitle="The Man He Became", color="#a3917a", tone="cold"),
    S("room", "Breakfast was coffee and sugar. Lunch was whatever the vending machine had. Dinner was at eleven at night, standing in front of the fridge.",
      [C("marcus", "walktired", pos=[-2, 0.5], to=[1.5, 0.5])], "side", time="night", tone="cold"),
    S("city", "He told himself it was for the family. That he had no time. But the truth was harder. He had stopped believing he was worth the time.",
      [C("marcus", "walktired", pos=[0, 5], to=[0, 0.5])], "track", time="night", tone="cold",
      punch="He stopped believing he was worth it."),
    S("room", "Zara noticed first. She noticed him out of breath on the stairs. She noticed he stopped playing with his nephews in the yard.",
      [C("zara", "idle2", pos=[-1.2, 0.6], face=50), C("marcus", "walktired", pos=[1.2, 0.2], face=-40)], "wide", time="dusk", tone="cold"),
    S("room", "Dad, she said, I need you there. Not just at the wedding. After. For the grandkids. For all of it.",
      [C("zara", "idle", pos=[-0.9, 0.5], face=60), C("marcus", "idle2", pos=[0.9, 0.5], face=-60)], "close", time="dusk",
      punch="I need you there.", punchAt=1.4),
    S("room", "He smiled and said he would be fine. And then he went to the kitchen and ate the whole box of cookies in the dark.",
      [C("marcus", "seated", pos=[0, 0.4], face=180)], "top", time="night", tone="cold"),
    S("room", "Two weeks later, he was sitting in front of that doctor.",
      [C("marcus", "seated", pos=[0.6, 0.4], face=-30), C("doc", "idle", pos=[-1.1, 0.2], face=60)], "wide", time="night", tone="cold"),

    # ---------- CHAPTER II — THE RULES ----------
    S("city", "On the walk home, he passed a small church with a sign out front. Every morning, six a.m., walking group. All ages. All welcome.",
      [C("marcus", "walkslow", pos=[-4, 1.2], to=[2, 1.2])], "side", time="dawn", chapterLabel="Chapter II",
      chapterTitle="Three Rules", color="#d4af37", mood="hope"),
    S("road", "The next morning he showed up. One person was there. A seventy two year old woman named Ruth, in bright red, already stretching.",
      [C("ruth", "idle2", pos=[-1, 0.6], face=40), C("marcus", "walkslow", pos=[3, 1.5], to=[1, 0.8])], "wide", time="dawn"),
    S("road", "You look like someone who got bad news, she said. He laughed for the first time in weeks. Then he told her everything.",
      [C("ruth", "idle", pos=[-0.9, 0.6], face=60), C("marcus", "idle2", pos=[0.9, 0.6], face=-60)], "close", time="dawn"),
    S("road", "Ruth had heard the same words from a doctor twenty years earlier. She was still here. And she lived by three rules.",
      [C("ruth", "walk", pos=[-3, 1], to=[3, 1]), C("marcus", "walk", pos=[-4, 1.8], to=[2, 1.8])], "track", time="dawn",
      punch="Three rules.", punchAt=3.5),
    S("kitchen", "Rule one. Give your body a break from food every single day. Eat in a window. Let it rest. Let it heal.",
      [C("ruth", "cook", pos=[0, 0.4], face=180)], "push", time="day", punch="FAST.", punchAt=1.2),
    S("road", "Rule two. Move every single day. Not hard. Not perfect. Every day. Your heart is a muscle. Treat it like one.",
      [C("ruth", "walk", pos=[-3, 1], to=[3, 1])], "track", time="day", punch="TRAIN.", punchAt=1.2),
    S("void", "Rule three. Stop the harm. To your body. To your mind. And never let anyone else bring harm to you, or you to them.",
      [C("ruth", "idle", pos=[0, 2.2], face=180)], "orbit", pillars=3, punch="PROTECT.", punchAt=1.2),
    S("road", "That's it, he asked. That's it, she said. It's simple. It's just not easy. The hard part is doing it on the days you don't want to.",
      [C("ruth", "idle2", pos=[-0.9, 0.6], face=60), C("marcus", "idle", pos=[0.9, 0.6], face=-60)], "close", time="dawn",
      punch="Simple. Not easy."),

    # ---------- CHAPTER III — THE FIRST FAST ----------
    S("kitchen", "Day one, he skipped breakfast. By ten in the morning, his hands were shaking and every thought was about food.",
      [C("marcus", "seated", pos=[0, 0.5], face=180)], "push", time="dawn", chapterLabel="Chapter III",
      chapterTitle="Low Tide", color="#8fb3c9"),
    S("kitchen", "Ruth had warned him. The hunger comes in waves. It rises. It peaks. And if you breathe through it, it passes.",
      [C("marcus", "meditate", pos=[0, 1], face=180)], "orbit", time="day"),
    S("kitchen", "At noon he ate real food. Eggs. Vegetables. Fish. No sugar. No vending machine. And for the first time in years, he wasn't tired after lunch.",
      [C("marcus", "cook", pos=[0, 0.4], face=180)], "wide", time="day", tone="warm"),
    S("room", "By the second week, the waves got smaller. The cravings at night got quieter. He was sleeping through the night again.",
      [C("marcus", "lie", pos=[-2, -2], y=0.45, face=180)], "top", time="night"),
    S("room", "Week three, Zara came over and stopped in the doorway. Dad, your face looks different. Your eyes look awake.",
      [C("zara", "idle2", pos=[-1, 0.6], face=50), C("marcus", "idle", pos=[1, 0.4], face=-50)], "close", time="day", tone="warm",
      punch="Your eyes look awake."),

    # ---------- CHAPTER IV — THE WALK ----------
    S("road", "The first morning walk, he made it eight minutes before he had to sit down on the curb. Ruth sat down next to him.",
      [C("marcus", "sitfloor", pos=[0.6, 0.8], face=180), C("ruth", "idle", pos=[-0.8, 0.8], face=40)], "low", time="dawn",
      chapterLabel="Chapter IV", chapterTitle="The Walk", color="#c9a26b"),
    S("road", "Tomorrow, nine minutes, she said. That's the whole secret. Tomorrow, nine minutes.",
      [C("ruth", "idle2", pos=[-0.8, 0.8], face=50), C("marcus", "sitfloor", pos=[0.6, 0.8], face=-40)], "close", time="dawn",
      punch="Tomorrow, nine minutes.", punchAt=0.8),
    S("road", "Nine minutes became fifteen. Fifteen became thirty. By month two, he was walking an hour before work and actually looking forward to it.",
      [C("marcus", "walk", pos=[-5, 1], to=[5, 1]), C("ruth", "walk", pos=[-6, 1.8], to=[4, 1.8])], "track", time="dawn"),
    S("gym", "Month three, Ruth sent him to her grandson Leo, who coached at a small gym. Leo looked at him and said, we start with the floor.",
      [C("leo", "idle", pos=[-1, 0.4], face=50), C("marcus", "idle2", pos=[1, 0.4], face=-50)], "wide"),
    S("gym", "Marcus couldn't do one push up. Not one. He did them on his knees. He did them against the wall. He did them every day.",
      [C("marcus", "pushups", pos=[-0.8, 0.5], face=90)], "wide", zoom=0.75, camAngle=50, punch="Not one."),
    S("gym", "Week after week, Leo added a little more. Squats. Carrying weight. Stretching that hurt. Marcus showed up even on the days his body begged him not to.",
      [C("marcus", "situps", pos=[0, 0.5], face=90), C("leo", "idle2", pos=[1.6, -0.4], face=-60)], "side"),
    S("gym", "And one Tuesday, without thinking about it, he did ten real push ups in a row. Leo started clapping. Marcus started crying.",
      [C("marcus", "pushups", pos=[-0.8, 0.5], face=90), C("leo", "cheer", pos=[1.6, -0.4], face=-60)], "low", tone="warm",
      punch="Ten in a row.", mood="rise"),

    # ---------- CHAPTER V — THE HARM ----------
    S("city", "But the hardest rule wasn't the food or the walking. It was the third one. Because some of the harm in his life had a name.",
      [C("marcus", "walkslow", pos=[0, 5], to=[0, 1])], "track", time="night", chapterLabel="Chapter V",
      chapterTitle="The Wall", color="#b05a4a", tone="cold", mood="dark"),
    S("city", "His old friend Vince. Every Friday, the same bar. The same drinks. The same jokes about how diets are for people with nothing better to do.",
      [C("vince", "idle2", pos=[-1, 0.6], face=50), C("marcus", "idle", pos=[1, 0.6], face=-50)], "wide", time="night", tone="cold"),
    S("city", "Come on, Vince said. One night won't kill you. And Marcus heard the doctor's voice in his head. Actually, it might.",
      [C("vince", "wave", pos=[-0.9, 0.6], face=60), C("marcus", "idle2", pos=[0.9, 0.6], face=-60)], "close", time="night", tone="cold",
      punch="Actually, it might."),
    S("city", "He said no. Vince laughed. Then he got angry. Then he stopped calling. And Marcus let him go.",
      [C("marcus", "walk", pos=[0, 1], to=[0, 6]), C("vince", "idle2", pos=[-1.2, 0.4], face=20)], "track", time="night"),
    S("room", "It wasn't just Vince. It was the late night phone scrolling. The news that made him angry for no reason. The voice in his head that said too old, too late, too far gone.",
      [C("marcus", "seated", pos=[0, 0.4], face=180)], "push", time="night"),
    S("void", "He built a wall around his life. Not to keep people out. To keep the harm out. And inside that wall, something started to grow.",
      [C("marcus", "idle", pos=[0, 2.2], face=180)], "crane", pillars=3, mood="hope", punch="Keep the harm out."),
    S("room", "He called Zara more. He apologized to his brother for an old fight. He started protecting his peace like it was a medicine. Because it was.",
      [C("marcus", "idle2", pos=[0, 0.5], face=180)], "wide", time="day", tone="warm"),

    # ---------- CHAPTER VI — THE CHECKUP ----------
    S("room", "Six months after that first appointment, he sat in front of the same doctor. The same paper. The same chair.",
      [C("marcus", "seated", pos=[0.6, 0.4], face=-30), C("doc", "idle2", pos=[-1.1, 0.2], face=60)], "wide", time="day",
      chapterLabel="Chapter VI", chapterTitle="The Paper", color="#8fb39a"),
    S("room", "This time, the doctor looked up. He looked at the numbers. Then at Marcus. Then back at the numbers.",
      [C("doc", "idle", pos=[-1.1, 0.2], face=60), C("marcus", "seated", pos=[0.6, 0.4], face=-30)], "close", time="day"),
    S("room", "Thirty one kilos gone. Blood pressure normal. Blood sugar normal. Heart stronger than it had been in ten years.",
      [C("doc", "idle2", pos=[-1.1, 0.2], face=60), C("marcus", "seated", pos=[0.6, 0.4], face=-30)], "push", time="day",
      punch="Heart stronger than in ten years.", punchAt=4.5, mood="rise"),
    S("room", "What did you do, the doctor asked. Marcus smiled. Three rules, he said. Every single day.",
      [C("marcus", "idle", pos=[0.6, 0.4], face=-30), C("doc", "idle2", pos=[-1.1, 0.2], face=60)], "close", time="day", tone="warm",
      punch="Three rules. Every day."),
    S("road", "He walked out of that office and called Ruth first. She didn't say congratulations. She said, good. Now keep going.",
      [C("marcus", "walk", pos=[-4, 1], to=[3, 1])], "track", time="day", tone="warm"),

    # ---------- CHAPTER VII — THE CLIMB ----------
    S("summit", "In month ten, Leo asked him a question. There's a mountain trail two hours from here. Want to climb it with us?",
      [C("leo", "idle2", pos=[-1, 0.4], face=50), C("marcus", "idle", pos=[1, 0.4], face=-50)], "wide", time="dawn",
      chapterLabel="Chapter VII", chapterTitle="The Climb", color="#d4af37"),
    S("summit", "A year ago, Marcus couldn't climb the stairs to his own bedroom. Now he was climbing a mountain at sunrise.",
      [C("marcus", "walk", pos=[-3, 2], to=[0, 0]), C("leo", "walk", pos=[-4, 2.6], to=[-1.2, 0.6])], "crane", time="dawn"),
    S("summit", "At the top, he stood in the cold air and felt something he hadn't felt in twenty years. Not pride. Peace.",
      [C("marcus", "cheer", pos=[0, 0], face=180)], "crane", time="dawn", tone="warm", punch="Not pride. Peace.", punchAt=4.6),
    S("summit", "He took out his phone and sent Zara a picture. Three words. I'll be there.",
      [C("marcus", "idle", pos=[0, 0], face=180)], "close", time="dawn", tone="warm", punch="I'll be there.", punchAt=3.4),

    # ---------- CHAPTER VIII — THE WEDDING ----------
    S("stage", "One year after the doctor said one year, the music started.",
      [C("zara", "idle", pos=[-0.6, 0.6], face=180), C("marcus", "idle2", pos=[0.6, 0.6], face=180)], "push",
      chapterLabel="Chapter VIII", chapterTitle="The Aisle", color="#f0d68a", piano=True, mood="calm", tone="warm"),
    S("stage", "Marcus took his daughter's arm. His legs were steady. His breath was easy. His eyes were clear.",
      [C("zara", "walkslow", pos=[-0.6, 3], to=[-0.6, 0.5]), C("marcus", "walkslow", pos=[0.6, 3], to=[0.6, 0.5])], "track", tone="warm"),
    S("stage", "Halfway down the aisle, Zara whispered, Dad, you made it. And he whispered back, I made it because of you.",
      [C("zara", "idle", pos=[-0.5, 0.6], face=30), C("marcus", "idle2", pos=[0.5, 0.6], face=-30)], "close", tone="warm",
      punch="You made it."),
    S("stage", "In the second row sat a seventy three year old woman in bright red. Ruth didn't cry. She just nodded. Good. Now keep going.",
      [C("ruth", "seated", pos=[0, 0.5], face=180)], "push", tone="warm"),
    S("stage", "And later that night, the man who couldn't climb the stairs danced with his daughter until the band stopped playing.",
      [C("marcus", "cheer", pos=[0.7, 0.4], face=-40), C("zara", "cheer", pos=[-0.7, 0.4], face=40),
       C("leo", "wave", pos=[-2.4, 1.6], face=30), C("ruth", "idle2", pos=[2.4, 1.6], face=-30)], "orbit", tone="warm", mood="rise",
      punch="He danced until the band stopped."),

    # ---------- OUTRO ----------
    S("void", "Marcus didn't have a secret. He didn't have money, or time, or a perfect plan. He had three rules, and a reason.",
      [C("marcus", "idle", pos=[0, 2.2], face=180)], "wide", pillars=3),
    S("void", "Fast, so your body can heal. Train, so your heart stays strong. Protect, so the harm never gets back in.",
      [C("marcus", "idle2", pos=[0, 2.2], face=180), C("ruth", "idle", pos=[-2, 2.8], face=30), C("zara", "idle", pos=[2, 2.8], face=-30)],
      "crane", pillars=3, punch="Fast. Train. Protect."),
    S("void", "Find your reason. Someone you want to be there for. Then start tomorrow. Nine minutes. That's all.",
      [C("marcus", "idle", pos=[0, 2.2], face=180)], "push", pillars=3, punch="Find your reason."),
    S("void", "This is Alpha Talks 3000. If this story moved you, send it to someone who needs a reason today. And never stop showing up.",
      [C("marcus", "idle", pos=[0, 2.2], face=180), C("zara", "idle2", pos=[1.6, 2.7], face=-30)], "crane", pillars=3, durationSec=10,
      titleCard={"title": "Fast. Train. Protect.", "subtitle": "Alphatalks3000"}),
]

story = {
    "title": "One Year — Alphatalks3000",
    "mood": "calm",
    "characters": characters,
    "scenes": scenes,
    "thumbnail": {"text": "THE DOCTOR SAID 1 YEAR", "sub": "Her wedding was in 1 year",
                  "scene": 0, "at": 5.6},
}
json.dump(story, open("stories/one-year.json", "w"), indent=1)
words = sum(len((s.get("caption") or "").split()) for s in scenes)
print("scenes", len(scenes), "words", words, "est minutes", round(words / 2.25 / 60 + len(scenes) * 1.6 / 60 + 8 * 4 / 60, 1))
