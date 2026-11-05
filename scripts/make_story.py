import json

characters = {
    "noah": {"skin": "#c68a64", "shirt": "#2b3445", "pants": "#1c1f26", "hair": "short", "hairColor": "#1a120c", "sleeves": True},
    "coach": {"skin": "#8d5a3b", "shirt": "#5a4632", "pants": "#2a2a2e", "hair": "short", "hairColor": "#cfcfcf", "sleeves": True, "height": 0.97},
    "mara": {"skin": "#e2b48f", "shirt": "#c9b79a", "pants": "#3b4a63", "hair": "bun", "hairColor": "#5a2e1a"},
    "jalen": {"skin": "#5e3a26", "shirt": "#d63a2f", "pants": "#111318", "hair": "bald", "height": 1.04},
    "theo": {"skin": "#f0cfb0", "shirt": "#101114", "pants": "#101114", "hair": "short", "hairColor": "#c49a5a", "sleeves": True},
    "dee": {"skin": "#7a4a30", "shirt": "#f2a524", "pants": "#1b2a52", "hair": "afro", "hairColor": "#120c08", "height": 1.06},
    "kenji": {"skin": "#d9a77e", "shirt": "#1d1d22", "pants": "#a32323", "hair": "short", "hairColor": "#0d0d0d"},
}

def S(env, caption, cast=None, camera="wide", **kw):
    d = {"env": env, "durationSec": 4, "caption": caption, "camera": camera}
    if cast:
        d["cast"] = cast
    d.update(kw)
    return d

C = lambda who, action, **kw: dict({"who": who, "action": action}, **kw)

scenes = [
    # ---------- COLD OPEN ----------
    S("room", "Three in the morning. The phone is still glowing. Noah has watched a hundred people live their dreams tonight, and he has not moved an inch toward his own.",
      [C("noah", "lie", pos=[-2, -2], y=0.42, face=180)], "top", time="night", fade=True),
    S("room", "He is not lazy. He is not broken. He is something quieter and more dangerous. He is unclear.",
      [C("noah", "lie", pos=[-2, -2], y=0.42, face=180)], "close", time="night", punch="Not lazy. Unclear."),
    S("void", "", None, "wide", titleCard={"title": "The Clarity Code", "subtitle": "Alphatalks3000 presents"}, durationSec=7),
    S("room", "Welcome to Alpha Talks 3000. Tonight's story is about clarity, and about the five people who taught one young man how to find it.",
      [C("noah", "wakeup", pos=[-2, -1.6], y=0.42)], "push", time="dawn"),
    S("room", "Because clarity is not something you think your way into. It is something you build, one honest day at a time.",
      [C("noah", "idle", pos=[0, 0])], "orbit", time="dawn"),

    # ---------- THE MEETING ----------
    S("road", "That morning, Noah went for a walk he did not want to take. Twenty minutes in, an old man fell into step beside him.",
      [C("noah", "walk", pos=[0.8, 6], to=[0.8, -6]), C("coach", "walk", pos=[-0.6, 6.3], to=[-0.6, -5.7])], "track", time="dawn"),
    S("road", "The old man had coached champions for forty years. He looked at Noah and said one sentence that changed everything.",
      [C("coach", "idle", pos=[-0.6, 0], face=40), C("noah", "idle2", pos=[0.8, 0.2], face=-50)], "side", time="dawn", focus=0),
    S("road", "You do not need more motivation. You need a clear picture. Let me show you five people who found theirs.",
      [C("coach", "interact", pos=[-0.6, 0], face=40), C("noah", "idle", pos=[0.8, 0.2], face=-50)], "close", time="dawn",
      punch="You need a clear picture."),

    # ---------- CHAPTER 1 — THE PAINTER ----------
    S("studio", "The first was Mara. A painter. For seven years she started a new canvas every week, and she never finished a single one.",
      [C("mara", "idle", pos=[0, 0], face=200)], "wide", chapterLabel="Chapter I", chapterTitle="The Painter", color="#f5b942", paint=[0.05, 0.08]),
    S("studio", "She had talent. Everyone told her so. But talent without direction is just noise with a beautiful voice.",
      [C("mara", "paint", pos=[0.2, -0.1], face=200)], "orbit", paint=[0.08, 0.12]),
    S("studio", "One winter she made a decision so simple it scared her. One painting. No new ideas until it was done.",
      [C("mara", "idle2", pos=[-0.5, 0.6], face=180)], "push", paint=[0.12, 0.14], punch="One painting. Nothing else."),
    S("studio", "She stopped eating late at night, when her mind was foggy and her hands were restless. She painted in the morning, on an empty stomach, sharp and awake.",
      [C("mara", "paint", pos=[0.2, -0.1], face=200)], "side", time="dawn", paint=[0.14, 0.3]),
    S("studio", "Every afternoon she walked for an hour. Not for fitness, but to let the painting speak to her when she was not looking at it.",
      [C("mara", "walk", pos=[-4, 1.5], to=[3, 1.5])], "track", paint=[0.3, 0.35]),
    S("studio", "And she cut out the voices that hurt her. The friend who mocked her work. Her own inner critic at midnight. She simply stopped feeding them.",
      [C("mara", "backoff", pos=[0, 0], to=[0, 2.5], face=0)], "low", paint=[0.35, 0.45]),
    S("studio", "Six weeks later, Mara finished her first painting in seven years. It was not perfect. It was clear. And clear beats perfect every single time.",
      [C("mara", "cheer", pos=[-0.8, 0.8], face=160)], "pull", paint=[0.45, 1.0], punch="Clear beats perfect."),
    S("road", "The coach looked at Noah. Mara did not find clarity by thinking harder. She found it by removing everything that was not the painting.",
      [C("coach", "walkslow", pos=[-0.6, 4], to=[-0.6, -2]), C("noah", "walkslow", pos=[0.8, 4.3], to=[0.8, -1.7])], "track", time="day"),

    # ---------- CHAPTER 2 — THE SPRINTER ----------
    S("stadium", "The second was Jalen. A sprinter who was fast enough to win, and lost every final he ever ran.",
      [C("jalen", "idle", pos=[0, 15], face=90)], "wide", chapterLabel="Chapter II", chapterTitle="The Sprinter", color="#ff5a3c", focus=0),
    S("stadium", "His problem was not his legs. His problem was the hundred thoughts screaming in his head at the starting line.",
      [C("jalen", "crouch", pos=[0, 15], face=90)], "close", focus=0, punch="A hundred thoughts. Zero focus."),
    S("stadium", "So his coach gave him a strange assignment. Before every training day, write down one thing. Only one thing to improve.",
      [C("jalen", "idle2", pos=[0, 15], face=90)], "orbit", focus=0),
    S("stadium", "Monday: the first three steps. Tuesday: the arms. Wednesday: breathing. Never everything. Always one.",
      [C("jalen", "run", pos=[-8, 15], to=[8, 15])], "track", focus=0),
    S("stadium", "He trained at sunrise, before breakfast, when the track was empty and his body felt light. His mind went quiet when his stomach did.",
      [C("jalen", "sprint", pos=[-9, 14.6], to=[9, 14.6])], "side", time="dawn", focus=0),
    S("stadium", "And he made a promise. No more partying the night before a race. No more poison he called fun. He protected his body like it belonged to someone he loved.",
      [C("jalen", "pushups", pos=[0, 15], face=90)], "low", focus=0, punch="Protect it like you love it."),
    S("stadium", "On the day of the championship final, there was only one thought in Jalen's head. The first three steps.",
      [C("jalen", "crouch", pos=[-6, 15], face=90)], "push", focus=0),
    S("stadium", "He crossed the line first. Not because he wanted it more than the others. Because he saw it more clearly than they did.",
      [C("jalen", "sprint", pos=[-8, 15], to=[6, 15]), ], "track", focus=0),
    S("stadium", "",
      [C("jalen", "cheer", pos=[6, 15], face=0)], "crane", focus=0, durationSec=4, punch="One thought wins races."),

    # ---------- CHAPTER 3 — THE PIANIST ----------
    S("stage", "The third was Theo. A pianist who practiced eight hours a day, and was getting worse.",
      [C("theo", "seated", pos=[0, 0.5], face=180)], "wide", chapterLabel="Chapter III", chapterTitle="The Pianist", color="#9fb8ff"),
    S("stage", "He played tired. He played angry. He played late into the night until his fingers remembered his frustration better than the music.",
      [C("theo", "work", pos=[0, 0.75], face=180)], "close", camAngle=150),
    S("stage", "An old teacher listened to him for two minutes, closed the piano, and said: you are practicing confusion. Stop.",
      [C("theo", "idle2", pos=[1.4, 0.8], face=-90), C("coach", "idle", pos=[-1.6, 0.8], face=90)], "side", focus=0, punch="You are practicing confusion."),
    S("stage", "Theo cut his practice from eight hours to three. Three focused hours, in the morning, before he ate a single bite.",
      [C("theo", "work", pos=[0, 0.75], face=180)], "orbit", time="dawn", camAngle=180),
    S("stage", "In the afternoon he trained his body. Push ups, long walks, deep breathing. A strong body gave his music a steady pulse.",
      [C("theo", "pushups", pos=[2.2, 1.6], face=90)], "low"),
    S("stage", "And he stopped tearing himself apart after every mistake. He learned that cruelty toward yourself is still cruelty. It just has no witness.",
      [C("theo", "meditate", pos=[0, 2], face=0)], "push", punch="Cruelty toward yourself is still cruelty."),
    S("stage", "A year later, Theo played a concert hall. The same music he used to fight with. This time, it sounded like freedom.",
      [C("theo", "work", pos=[0, 0.75], face=180)], "crane", camAngle=200),

    # ---------- MIDPOINT ----------
    S("city", "That night Noah walked through the city alone. He saw the pattern now, but he did not want to see it.",
      [C("noah", "walkslow", pos=[0, 2], to=[0, -10])], "track", time="night"),
    S("city", "Because every story said the same thing. Clarity does not come from the outside. It comes from what you stop doing.",
      [C("noah", "idle2", pos=[0, -2], face=0)], "close", time="night", punch="Clarity is what remains."),
    S("room", "He went home and looked at his phone. Four hours of scrolling every single day. Midnight snacks. No movement. And quiet words he said to himself that he would never say to a friend.",
      [C("noah", "seated", pos=[1.5, 0.5], face=200)], "push", time="night"),
    S("room", "For the first time, he did not feel shame. He felt something better. He felt clear.",
      [C("noah", "rise", pos=[1.5, 0.5], face=0)], "pull", time="night"),

    # ---------- CHAPTER 4 — THE PLAYER ----------
    S("court", "The fourth was Dee. A basketball player with a beautiful game and no discipline at all.",
      [C("dee", "idle", pos=[0, 1.5], face=180, ball=True)], "wide", chapterLabel="Chapter IV", chapterTitle="The Player", color="#f2a524", focus=0),
    S("court", "She ate whatever, whenever. She trained when she felt like it. And she missed the shots that mattered most.",
      [C("dee", "shoot", pos=[0.2, 1.8], face=180)], "low", focus=0, shot="miss", shotAt=0.9),
    S("court", "After a season on the bench, she built what she called her non negotiables. Three rules. No exceptions.",
      [C("dee", "idle2", pos=[0, 1.5], face=0)], "close", focus=0, punch="Three rules. No exceptions."),
    S("court", "Rule one. She ate in an eight hour window and fasted the rest. Her energy stopped crashing. Her focus stopped drifting.",
      [C("dee", "run", pos=[-5, 3], to=[5, 3])], "track", focus=0),
    S("court", "Rule two. Five hundred shots every day before anyone else arrived. Not when she felt like it. Every day.",
      [C("dee", "shootloop", pos=[0.3, 1.6], face=180, speed=0.9)], "orbit", focus=0),
    S("court", "Rule three. No trash talk that crossed the line. No harm to her teammates, her opponents, or herself. She played hard and she played clean.",
      [C("dee", "guard", pos=[0, 2], face=180), C("jalen", "idle", pos=[0.9, 0.8], face=0)], "side", focus=0),
    S("court", "In the final seconds of the championship game, the ball found Dee. She did not hope. She did not pray. She had already made this shot ten thousand times.",
      [C("dee", "shoot", pos=[0, 2.4], face=180)], "push", focus=0, shot="make", shotAt=2.6),
    S("court", "",
      [C("dee", "cheer", pos=[0, 2.4], face=0)], "crane", focus=0, durationSec=4, punch="Discipline is clarity in motion."),

    # ---------- CHAPTER 5 — THE FIGHTER ----------
    S("gym", "The fifth was Kenji. A fighter. And his story was the hardest one to tell.",
      [C("kenji", "guard", pos=[0, 0], face=180, gloves="#b8332e")], "wide", chapterLabel="Chapter V", chapterTitle="The Fighter", color="#b8332e"),
    S("gym", "Kenji was strong, but his anger was stronger. He fought in the ring, and then he fought outside it, where there were no rules and no winners.",
      [C("kenji", "punch", pos=[0, 0], face=180, gloves="#b8332e")], "close"),
    S("gym", "One night, he hurt someone who did not deserve it. And in that moment, he lost everything he had trained for.",
      [C("kenji", "collapse", pos=[0, 0], face=180, gloves="#b8332e")], "top", time="night", punch="Strength without control is harm."),
    S("gym", "He spent a long time on the floor of his own life. Then he made a choice. His strength would only ever protect, never destroy.",
      [C("kenji", "getup", pos=[0, 0], face=180, gloves="#b8332e")], "low"),
    S("gym", "He fasted every morning to train his patience. When you can say no to hunger, you can say no to rage.",
      [C("kenji", "meditate", pos=[0, 0], face=180)], "orbit", time="dawn", punch="Say no to hunger. Say no to rage."),
    S("gym", "He trained twice a day, until his body was too calm for anger to live in.",
      [C("kenji", "kick", pos=[-1, 0], face=90, gloves="#b8332e"), C("noah", "block", pos=[1, 0], face=-90, gloves="#2f4d7a")], "side"),
    S("gym", "Today Kenji teaches kids from his old neighbourhood. He does not teach them to fight. He teaches them to stay in control.",
      [C("kenji", "guard", pos=[0, -1], face=0, gloves="#b8332e"), C("noah", "guard", pos=[-1.2, 1.2], face=180, gloves="#2f4d7a"), C("dee", "guard", pos=[1.2, 1.2], face=180, gloves="#f2a524")], "pull"),

    # ---------- THE CODE ----------
    S("void", "The coach brought Noah back to where it all started, and showed him what all five stories had in common.",
      [C("coach", "idle", pos=[-1, 1.5], face=30), C("noah", "idle2", pos=[1, 1.5], face=-30)], "wide", chapterLabel="Chapter VI", chapterTitle="The Clarity Code", color="#f5c451", pillars=0),
    S("void", "Pillar one. Consistent fasting. Every one of them learned that an empty stomach can make a full mind. Discipline over appetite is the first victory of the day.",
      [C("noah", "idle", pos=[0, 2.2], face=180)], "push", pillars=1, punch="Pillar one. The fast."),
    S("void", "Pillar two. Consistent workouts. A body that moves every day gives the mind a rhythm to follow. Motion creates clarity.",
      [C("noah", "pushups", pos=[0, 2.2], face=90)], "orbit", pillars=2, punch="Pillar two. The work."),
    S("void", "Pillar three. Stay away from harm. Harm against others, and harm against yourself. The poison you consume, the words you speak, the habits that quietly destroy you.",
      [C("noah", "meditate", pos=[0, 2.2], face=180)], "low", pillars=3, punch="Pillar three. The shield."),
    S("void", "Fast. Train. Protect. Not once. Not when you feel like it. Consistently. That is the whole code.",
      [C("noah", "idle", pos=[0, 2.2], face=180), C("coach", "idle2", pos=[-2, 3], face=40)], "crane", pillars=3, punch="Fast. Train. Protect."),

    # ---------- NOAH'S TRANSFORMATION ----------
    S("kitchen", "So Noah began. Day one. No breakfast. Just water, silence, and one clear goal written on paper.",
      [C("noah", "seated", pos=[0, 0.55], face=180)], "push", time="dawn", chapterLabel="Chapter VII", chapterTitle="Day One"),
    S("room", "Day seven. The phone stayed in another room at night. He slept. For the first time in months, he really slept.",
      [C("noah", "liedown", pos=[-2, -1.8], y=0.42, face=180)], "top", time="night"),
    S("road", "Day thirty. He was running now. Slow, but every single morning.",
      [C("noah", "run", pos=[0, 8], to=[0, -8])], "track", time="dawn"),
    S("gym", "Day sixty. The words he said to himself changed. He stopped calling himself a failure, and started calling himself a beginner.",
      [C("noah", "pushups", pos=[0, 0], face=90)], "low", punch="Not a failure. A beginner."),
    S("gym", "Day ninety. Kenji put gloves on him and taught him that control is the highest form of strength.",
      [C("noah", "punch", pos=[1, 0], face=-90, gloves="#2f4d7a"), C("kenji", "block", pos=[-1, 0], face=90, gloves="#b8332e")], "side", focus=0),
    S("city", "Day one hundred. Noah walked the same city streets that once felt empty. Now they felt like possibility.",
      [C("noah", "walk", pos=[0, 2], to=[0, -10])], "track", time="dusk"),

    # ---------- CLIMAX ----------
    S("summit", "On day one hundred and eighty, Noah reached the top of a mountain he had once been too tired to even look at.",
      [C("noah", "walktired", pos=[0, 3], to=[0, 0.5])], "crane", time="dawn", chapterLabel="Chapter VIII", chapterTitle="The Summit", color="#ffcf6b"),
    S("summit", "He was not a champion. He was not famous. But he knew exactly who he was, where he was going, and what he would never do again.",
      [C("noah", "idle", pos=[0, 0.5], face=180)], "orbit", time="dawn"),
    S("summit", "That is clarity. Not knowing everything. Knowing what matters, and having the discipline to protect it.",
      [C("noah", "cheer", pos=[0, 0.5], face=0)], "pull", time="dawn", punch="Know what matters. Protect it."),

    # ---------- OUTRO ----------
    S("void", "Mara found it in a painting. Jalen in three steps. Theo in silence. Dee in five hundred shots. Kenji in control. And Noah, in one honest day after another.",
      [C("mara", "idle", pos=[-3, 1], face=20), C("jalen", "idle2", pos=[-1.5, 2], face=10), C("theo", "idle", pos=[0, 2.4]), C("dee", "idle2", pos=[1.5, 2], face=-10), C("kenji", "idle", pos=[3, 1], face=-20)],
      "wide", pillars=3, focus=2),
    S("void", "Your story starts the same way. Tomorrow morning. One fast. One workout. One harmful habit you finally put down.",
      [C("noah", "idle", pos=[0, 2.2], face=180)], "push", pillars=3, punch="Tomorrow. One step."),
    S("void", "This is Alpha Talks 3000. Fast. Train. Protect. And the clarity will come to you.",
      [C("noah", "idle", pos=[0, 2.2], face=180), C("coach", "idle2", pos=[-1.8, 2.8], face=30)], "crane", pillars=3, durationSec=10,
      titleCard={"title": "Fast. Train. Protect.", "subtitle": "Alphatalks3000"}),
]

story = {
    "title": "The Clarity Code — Alphatalks3000",
    "characters": characters,
    "scenes": scenes,
    "thumbnail": {"text": "THE CLARITY CODE", "sub": "5 stories. 3 pillars.", "scene": next(i for i,x in enumerate(scenes) if x.get("punch")=="Know what matters. Protect it."), "at": 3},
}
json.dump(story, open("stories/clarity-code.json", "w"), indent=1)
words = sum(len((s.get("caption") or "").split()) for s in scenes)
print("scenes", len(scenes), "words", words, "est minutes", round(words / 2.25 / 60 + len(scenes) * 1.6 / 60 + 8 * 4 / 60, 1))
