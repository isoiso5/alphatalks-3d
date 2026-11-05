import json

# "The Harbour" — Alphatalks3000, long video #3
# Angle: a former champion swimmer drowning on dry land. An old fisherman teaches him the
# three pillars through the rhythm of the sea. Climax: a storm rescue only a clear, strong man could make.
characters = {
    "kai": {"skin": "#c68e64", "shirt": "#2b4a6b", "pants": "#1d232c", "hair": "short", "hairColor": "#1a120c", "sleeves": True},
    "tomas": {"skin": "#a8774f", "shirt": "#c9b07a", "pants": "#3b3226", "hair": "beanie", "hairColor": "#7a2d24", "height": 0.94, "sleeves": True},
    "finn": {"skin": "#f0c9a6", "shirt": "#e2b13c", "pants": "#2f4460", "hair": "cap", "hairColor": "#3a6aa8", "height": 0.68},
    "rosa": {"skin": "#8a5a3c", "shirt": "#5fa7a0", "pants": "#26303a", "hair": "bun", "hairColor": "#1d130c"},
    "dex": {"skin": "#e7c2a0", "shirt": "#5a2f2f", "pants": "#222", "hair": "short", "hairColor": "#8a6a3a", "sleeves": True},
}

def S(env, caption, cast=None, camera="wide", **kw):
    d = {"env": env, "durationSec": 4, "caption": caption, "camera": camera}
    if cast:
        d["cast"] = cast
    d.update(kw)
    return d

C = lambda who, action, **kw: dict({"who": who, "action": action}, **kw)
PIER = 0.41  # standing height on the pier

scenes = [
    # ---------- COLD OPEN ----------
    S("shore", "The storm came in faster than anyone expected. Waves taller than houses. And somewhere out there, a little boy was holding on to an overturned boat.",
      [C("kai", "idle2", pos=[0, 1.5], face=180)], "push", time="storm", weather="rain", tone="cold", mood="dark", fade=True),
    S("shore", "Every man on that beach froze. Every man except one. The one the whole town had given up on.",
      [C("kai", "run", pos=[0, 2.5], to=[0, -2.5])], "track", time="storm", weather="rain", tone="cold", punch="Everyone froze. Except one."),
    S("shore", "But to understand why he ran into that storm, we have to go back. Back to the year he stopped swimming.",
      [C("kai", "idle", pos=[0, 1.2], face=180)], "crane", time="storm", weather="rain", tone="cold"),
    S("void", "", None, "wide", titleCard={"title": "The Harbour", "subtitle": "Alphatalks3000 presents"}, durationSec=7, mood="calm"),
    S("shore", "Welcome to Alpha Talks 3000. Tonight is a story about the sea, about rhythm, and about a man who learned that discipline is not a punishment. It is a tide.",
      [C("kai", "idle", pos=[0, 1.2], face=200)], "orbit", time="dusk"),

    # ---------- CHAPTER 1 — THE DRY YEARS ----------
    S("shore", "Kai grew up in this harbour town. By sixteen, he could outswim every fisherman's son on the coast. By twenty, he was a national champion.",
      [C("kai", "sprint", pos=[-4, 2], to=[4, 2])], "track", time="day", chapterLabel="Chapter I", chapterTitle="The Dry Years", color="#8fa6b8"),
    S("stadium", "Then came the one race that mattered. He lost by a hundredth of a second. And something inside him simply turned off.",
      [C("kai", "idle2", pos=[0, 0], face=0)], "low", tone="cold", punch="One hundredth of a second."),
    S("room", "He came home and never went back to the water. Days became nights. Nights became bottles.",
      [C("kai", "lie", pos=[-2, -2], y=0.45, face=90)], "top", time="night", tone="cold"),
    S("city", "His old friend Dex was always there with another drink, another excuse, another reason to stay exactly the same.",
      [C("dex", "wave", pos=[1.2, 0.5], face=-60), C("kai", "walktired", pos=[-1.0, 0.8], face=60)], "side", tone="cold", focus=1),
    S("kitchen", "He ate whenever he was bored. Chips at noon. Takeaway at midnight. His body, once built like a dolphin, grew slow and heavy.",
      [C("kai", "seated", pos=[0, 0.55], face=180)], "push", time="night", tone="cold"),
    S("room", "And when his sister Rosa tried to help, he pushed her away. Words he could never take back.",
      [C("kai", "punch", pos=[-0.6, 0.4], face=90), C("rosa", "backoff", pos=[1.0, 0.4], to=[2.4, 1.2], face=-90)], "side", time="night", tone="cold", focus=0,
      punch="Harm always spreads."),
    S("shore", "A champion swimmer, slowly drowning on dry land. And the worst part? He told himself he was fine.",
      [C("kai", "walktired", pos=[-3, 2], to=[2, 2])], "wide", time="dusk", tone="cold", punch="Drowning on dry land."),

    # ---------- CHAPTER 2 — THE OLD FISHERMAN ----------
    S("shore", "Every morning at five, an old fisherman named Tomas walked past Kai's window, down to the pier, rain or shine. For forty years. Never once late.",
      [C("tomas", "walkslow", pos=[2, 3], to=[5, -3])], "wide", time="dawn", chapterLabel="Chapter II", chapterTitle="The Fisherman", color="#c9b07a", mood="hope"),
    S("shore", "One morning, Kai was still awake from the night before, sitting on the sand with a bottle in his hand. Tomas stopped.",
      [C("kai", "sitfloor", pos=[-0.8, 1.2], face=30), C("tomas", "idle", pos=[1.0, 1.0], face=-60)], "side", time="dawn", focus=0),
    S("shore", "You know what the sea taught me, he said. It does not care how you feel. It only rewards rhythm.",
      [C("tomas", "interact", pos=[1.0, 1.0], face=-60), C("kai", "meditate", pos=[-0.8, 1.2], face=30)], "close", time="dawn", focus=0,
      punch="The sea rewards rhythm."),
    S("shore", "The tide goes out. The tide comes in. Every single day. It never skips a day because it is tired. And that is why it can move mountains of sand.",
      [C("tomas", "idle2", pos=[1.0, 1.0], face=-60), C("kai", "meditate", pos=[-0.8, 1.2], face=30)], "orbit", time="dawn", focus=0),
    S("shore", "Kai laughed at him. Tomas did not laugh back. He just said: be at the pier tomorrow at five. Without the bottle.",
      [C("tomas", "walkslow", pos=[1.0, 1.0], to=[5, -3]), C("kai", "meditate", pos=[-0.8, 1.2], face=30)], "pull", time="dawn", focus=1),
    S("room", "That night, Kai stared at the ceiling for hours. And for the first time in two years, he set an alarm.",
      [C("kai", "lie", pos=[-2, -2], y=0.45, face=90)], "push", time="night"),

    # ---------- CHAPTER 3 — LOW TIDE (FASTING) ----------
    S("shore", "Five o'clock. Tomas handed him nothing. No coffee. No breakfast. We eat when the work is done, he said. Not before.",
      [C("tomas", "idle", pos=[5, -5], y=PIER, face=-30), C("kai", "idle2", pos=[4.2, -3.5], y=PIER, face=150)], "wide", time="dawn",
      chapterLabel="Chapter III", chapterTitle="Low Tide", color="#7fb7d6"),
    S("shore", "The first mornings were brutal. Kai's stomach screamed. His head pounded. His hands shook as he pulled the nets.",
      [C("kai", "work", pos=[4.5, -6], y=PIER, face=90)], "close", time="dawn"),
    S("shore", "Tomas smiled. That is low tide, he said. When the water pulls back, you see everything that was hiding underneath. Your hunger is not your enemy. It is the cleaning.",
      [C("tomas", "interact", pos=[5.4, -7], y=PIER, face=-90), C("kai", "work", pos=[4.6, -6], y=PIER, face=90)], "side", time="dawn", focus=0,
      punch="Hunger is the cleaning."),
    S("kitchen", "At noon they ate together. Grilled fish, bread, lemon, salt. Kai ate slowly. It was the best meal he could remember.",
      [C("kai", "seated", pos=[0, 0.55], face=180)], "orbit", time="day", tone="warm"),
    S("shore", "By the second week, something changed. The hunger in the morning became quiet. And in its place came a strange, sharp energy.",
      [C("kai", "work", pos=[4.5, -6], y=PIER, face=90)], "push", time="dawn"),
    S("void", "That is the first pillar. Consistent fasting. Not starving. Rhythm. Hours where your body stops digesting and starts repairing. Low tide, every single day.",
      [C("kai", "idle", pos=[0, 2.2], face=180)], "push", pillars=1, punch="Pillar one. The fast."),

    # ---------- CHAPTER 4 — THE ROW (TRAINING) ----------
    S("shore", "Then Tomas took away the boat's motor. From now on, he said, we row.",
      [C("tomas", "hammer", pos=[-4.4, -3.6], face=-120), C("kai", "idle2", pos=[-2.8, -2.8], face=-120)], "wide", time="dawn",
      chapterLabel="Chapter IV", chapterTitle="The Row", color="#f2994a", mood="rise"),
    S("shore", "Every morning, two kilometres out. Two kilometres back. Kai's arms burned. His lungs, ruined by years of smoke and wine, begged him to stop.",
      [C("kai", "work", pos=[-6, -10], y=0.66, face=90)], "low", time="dawn"),
    S("road", "After rowing, they walked the coast road. Then Kai started jogging it. Then running it.",
      [C("kai", "run", pos=[0, 6], to=[0, -10])], "track", time="dawn"),
    S("gym", "In the evenings, instead of the bar, Kai found an old gym above the harbour. Push ups. Pull ups. Squats. Nothing fancy. Just every day.",
      [C("kai", "pushups", pos=[0, 0], face=90)], "orbit", time="dusk"),
    S("gym", "Dex came looking for him one night. Come on, one drink. Kai looked at his old friend, and for the first time, he said no.",
      [C("dex", "idle2", pos=[1.6, 0.6], face=-70), C("kai", "idle", pos=[-0.6, 0.4], face=70)], "side", time="dusk", focus=1,
      punch="For the first time, no."),
    S("road", "Week five. Kai ran the whole coast road without stopping. At the top of the cliff, he looked down at the sea he used to own.",
      [C("kai", "cheer", pos=[0, 0], face=0)], "crane", time="dawn", tone="warm"),
    S("void", "Pillar two. Consistent workouts. Not one heroic day. Every day. The rowing, the running, the push ups. The tide that never skips.",
      [C("kai", "pushups", pos=[0, 2.2], face=90)], "orbit", pillars=2, punch="Pillar two. The work."),

    # ---------- CHAPTER 5 — THE HARBOUR WALL (PROTECT) ----------
    S("shore", "One evening, Tomas showed Kai the old harbour wall. Two hundred years old, still standing, while every storm smashed against it.",
      [C("tomas", "idle", pos=[0.9, 1.2], face=-40), C("kai", "idle", pos=[-0.7, 1.4], face=40)], "wide", time="dusk",
      chapterLabel="Chapter V", chapterTitle="The Harbour Wall", color="#c94f4f", mood="calm"),
    S("shore", "A harbour, he said, is not a place without storms. It is a place where the storms cannot get in. You need a wall too, Kai.",
      [C("tomas", "interact", pos=[0.9, 1.2], face=-40), C("kai", "idle2", pos=[-0.7, 1.4], face=40)], "close", time="dusk", focus=0,
      punch="Build your harbour wall."),
    S("room", "So Kai built one. The bottles went into the bin. The late night phone went into a drawer. The old crowd stopped getting his time.",
      [C("kai", "pickup", pos=[1.5, -1.5], face=180)], "push", time="night"),
    S("void", "But the hardest stone was the voice in his own head. The one that said, you lost, you are nothing, you will always be the man who lost by a hundredth.",
      [C("kai", "crouch", pos=[0, 2.2], face=180)], "low", tone="cold", mood="dark"),
    S("void", "Tomas taught him to answer it. Not with anger. With facts. I rowed today. I ran today. I kept my word today. That voice was a liar.",
      [C("kai", "rise", pos=[0, 2.2], face=180)], "push", mood="hope", punch="That voice was a liar."),
    S("city", "And then Kai did the bravest thing of all. He knocked on his sister's door.",
      [C("kai", "walkslow", pos=[-3, 2], to=[0, 0.5])], "track", time="dusk"),
    S("city", "He did not make excuses. He just said, I am sorry, Rosa. I was drowning, and I pulled you down with me. She held him for a long, long time.",
      [C("rosa", "idle2", pos=[0.6, 0.4], face=-80), C("kai", "idle", pos=[-0.6, 0.4], face=80)], "orbit", time="dusk", tone="warm", focus=1,
      punch="I am sorry."),
    S("void", "Pillar three. Stay away from harm. The harm you drink, the harm you say, the harm you think about yourself. Protect your harbour. Protect the people in it.",
      [C("kai", "meditate", pos=[0, 2.2], face=180)], "low", pillars=3, punch="Pillar three. The shield."),

    # ---------- CHAPTER 6 — BACK IN THE WATER ----------
    S("shore", "Day sixty. Before sunrise, Kai walked to the end of the pier. He had not been in the water for two years.",
      [C("kai", "walk", pos=[5, -5], to=[5, -20], y=PIER)], "track", time="dawn", chapterLabel="Chapter VI", chapterTitle="The Return", color="#5fb0d6", mood="rise"),
    S("shore", "Tomas did not say a word. He just nodded. And Kai dived in.",
      [C("kai", "jump", pos=[5, -20], y=PIER, face=180), C("tomas", "idle", pos=[5.4, -15], y=PIER, face=180)], "low", time="dawn"),
    S("shore", "The cold hit him like a thousand needles. And then, something incredible. His body remembered. Stroke, breath, stroke, breath. Rhythm.",
      [C("tomas", "cheer", pos=[5.4, -15], y=PIER, face=180)], "crane", time="dawn", tone="warm", punch="His body remembered."),
    S("shore", "He swam to the buoy and back. Not fast. Not like a champion. But clean. Clear. Alive.",
      [C("kai", "walk", pos=[4.6, -9], to=[4.6, -6], y=PIER), C("tomas", "idle", pos=[5.4, -6.5], y=PIER, face=-30)], "orbit", time="dawn", tone="warm"),
    S("shore", "Every morning after that, the town saw him out there. Fasted, strong, steady. The fishermen started calling him the tide.",
      [C("kai", "run", pos=[-5, 2.5], to=[5, 2.5])], "track", time="day", tone="warm"),

    # ---------- CHAPTER 7 — THE STORM ----------
    S("shore", "And that brings us back to that night. The storm. The overturned boat. The little boy holding on. His name was Finn. Tomas's grandson.",
      [C("tomas", "idle2", pos=[0.9, 1.5], face=180), C("kai", "idle", pos=[-0.7, 1.5], face=180)], "push", time="storm", weather="rain",
      chapterLabel="Chapter VII", chapterTitle="The Storm", color="#9fb8ff", mood="dark"),
    S("shore", "The lifeboat was an hour away. The waves were too high for any boat in the harbour. Tomas fell to his knees on the sand.",
      [C("tomas", "crouch", pos=[0.9, 1.5], face=180), C("kai", "idle2", pos=[-0.7, 1.5], face=180)], "close", time="storm", weather="rain", focus=0),
    S("shore", "Two years earlier, Kai would have been in a bar, too drunk to stand. Too slow. Too foggy. Too far gone.",
      [C("kai", "idle", pos=[0, 1.5], face=180)], "push", time="storm", weather="rain", tone="cold", punch="Two years earlier..."),
    S("shore", "But tonight, he was clear. Sixty mornings of rowing. Sixty mornings of hunger. Sixty days without poison. He kicked off his shoes and ran into the sea.",
      [C("kai", "sprint", pos=[0, 2.5], to=[0, -3.5])], "track", time="storm", weather="rain", mood="rise"),
    S("shore", "The first wave threw him back. The second one buried him. But he found the rhythm. Stroke, breath, stroke, breath.",
      [C("tomas", "idle2", pos=[0, 2], face=180)], "crane", time="storm", weather="rain", punch="Stroke. Breath. Rhythm."),
    S("shore", "Three hundred metres out, he reached the boat. Finn was ice cold and terrified. Kai held him and said: Breathe with me. We swim on the rhythm.",
      [C("kai", "hold", pos=[-6.2, -10], y=0.66, face=0), C("finn", "idle2", pos=[-5.7, -10.6], y=0.66, face=-40)], "close", time="storm", weather="rain", focus=0),
    S("shore", "It took them twenty minutes to reach the shore. The longest twenty minutes of Kai's life.",
      [C("kai", "walktired", pos=[-1, -3], to=[0, 1.5]), C("finn", "walktired", pos=[-0.4, -3], to=[0.6, 1.6])], "low", time="storm", weather="rain"),
    S("shore", "When their feet touched the sand, Tomas ran into the water and lifted his grandson into his arms. Finn was alive.",
      [C("tomas", "hold", pos=[0.6, 1.6], face=0), C("finn", "idle", pos=[0.6, 2.1], face=180), C("kai", "collapse", pos=[-1, 1.5], face=180)],
      "orbit", time="storm", weather="rain", tone="warm", mood="hope", punch="Finn was alive.", focus=0),

    # ---------- CHAPTER 8 — THE CALM ----------
    S("shore", "The next morning, the sea was flat as glass. The whole town came down to the harbour. Kai was sitting at the end of the pier, just watching the sunrise.",
      [C("kai", "meditate", pos=[5, -18], y=PIER, face=180)], "wide", time="dawn", tone="warm",
      chapterLabel="Chapter VIII", chapterTitle="The Calm", color="#ffcf6b"),
    S("shore", "Tomas sat down next to him. You know, he said, the sea did not save that boy. Your rhythm did. Sixty days of keeping your word.",
      [C("tomas", "sitfloor", pos=[5.6, -17.6], y=PIER, face=180), C("kai", "meditate", pos=[4.6, -18], y=PIER, face=180)], "close", time="dawn", tone="warm",
      punch="Your rhythm saved him."),
    S("shore", "Kai never became a champion again. He became something better. The man the town could count on, every single morning.",
      [C("kai", "walk", pos=[-4, 2.5], to=[3, 2.5]), C("finn", "run", pos=[-5, 3], to=[2.4, 3])], "track", time="day", tone="warm"),

    # ---------- OUTRO ----------
    S("void", "So here is the lesson of the harbour. Discipline is not a punishment. It is a tide. Out and in. Every single day.",
      [C("kai", "idle", pos=[0, 2.2], face=180)], "wide", pillars=3, mood="rise"),
    S("void", "Fast, so you see what is hiding under the water. Train, so your body is ready when the storm comes. Protect, so the storm can never get inside.",
      [C("kai", "idle2", pos=[0, 2.2], face=180), C("tomas", "idle", pos=[-2, 2.8], face=30), C("rosa", "idle", pos=[2, 2.8], face=-30)], "crane", pillars=3,
      punch="Fast. Train. Protect."),
    S("void", "Because one day, someone you love will need you to be strong and clear. And on that day, you want to be ready.",
      [C("kai", "idle", pos=[0, 2.2], face=180), C("finn", "idle2", pos=[1.1, 2.6], face=-20)], "push", pillars=3, punch="Be ready."),
    S("void", "This is Alpha Talks 3000. Find your rhythm. Build your harbour. And never stop showing up.",
      [C("kai", "idle", pos=[0, 2.2], face=180), C("tomas", "idle2", pos=[-1.8, 2.8], face=30)], "crane", pillars=3, durationSec=10,
      titleCard={"title": "Fast. Train. Protect.", "subtitle": "Alphatalks3000"}),
]

story = {
    "title": "The Harbour — Alphatalks3000",
    "mood": "calm",
    "characters": characters,
    "scenes": scenes,
    "thumbnail": {"text": "HE RAN INTO THE STORM", "sub": "60 days changed everything",
                  "scene": next(i for i, x in enumerate(scenes) if x.get("punch") == "Everyone froze. Except one."), "at": 2.2},
}
json.dump(story, open("stories/harbour.json", "w"), indent=1)
words = sum(len((s.get("caption") or "").split()) for s in scenes)
print("scenes", len(scenes), "words", words, "est minutes", round(words / 2.25 / 60 + len(scenes) * 1.6 / 60 + 8 * 4 / 60, 1))
