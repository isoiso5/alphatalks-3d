import json

# "The Clarity State" — Alphatalks3000
# Angle: a chef who lost his sense of taste (and his taste for life) gets his senses back
# in 40 days. Five awakenings: Taste, Breath, Awareness, Creativity, Results.
characters = {
    "ezra": {"skin": "#b07a55", "shirt": "#f1efe9", "pants": "#22252c", "hair": "short", "hairColor": "#1b130d", "sleeves": True},
    "ama": {"skin": "#6e4128", "shirt": "#7b3f5e", "pants": "#3a2a33", "hair": "bun", "hairColor": "#d8d8d8", "height": 0.9, "sleeves": True},
    "lena": {"skin": "#efcaa8", "shirt": "#2fa37a", "pants": "#1e2630", "hair": "bun", "hairColor": "#b5652b"},
    "sol": {"skin": "#4a2c1c", "shirt": "#16c2d5", "pants": "#0f1a2a", "hair": "bald", "height": 1.07, "sleeves": True},
    "ivy": {"skin": "#d9a27a", "shirt": "#e8d6b0", "pants": "#4a2f5c", "hair": "afro", "hairColor": "#2a1a10"},
    "milo": {"skin": "#f0cfb0", "shirt": "#e9e6df", "pants": "#2c2f36", "hair": "cap", "hairColor": "#6b4a2a"},
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
    S("kitchen", "Midnight. An empty restaurant. Ezra lifts a spoon of his own soup, the soup that once made people cry, and he tastes nothing at all.",
      [C("ezra", "cook", pos=[0, 0.4], face=180)], "push", time="night", fade=True),
    S("kitchen", "Not salt. Not warmth. Nothing. Somewhere along the way, food had turned grey. And so had everything else.",
      [C("ezra", "idle2", pos=[0, 0.9], face=0)], "close", time="night", punch="Everything turned grey."),
    S("void", "", None, "wide", titleCard={"title": "The Clarity State", "subtitle": "Alphatalks3000 presents"}, durationSec=7),
    S("kitchen", "Welcome to Alpha Talks 3000. Tonight's story is about a feeling most people have forgotten exists. The clarity state.",
      [C("ezra", "seated", pos=[0, 0.55], face=180)], "orbit", time="night"),
    S("kitchen", "The state where food tastes ten times better. Where every breath feels deep. Where your mind is clean, ideas arrive on their own, and your results finally match your talent.",
      [C("ezra", "seated", pos=[0, 0.55], face=180)], "pull", time="night"),
    S("void", "And the strangest part? You do not have to add anything to reach it. You only have to stop the things that are covering it.",
      [C("ezra", "idle", pos=[0, 2.2], face=180)], "push", punch="Clarity is already in you."),

    # ---------- CHAPTER 1 — THE GREY YEARS ----------
    S("kitchen", "Ezra had been the best young chef in the city. Then success came, and with it, a life without edges.",
      [C("ezra", "cook", pos=[0, 0.4], face=180)], "wide", chapterLabel="Chapter I", chapterTitle="The Grey Years", color="#9aa3ad"),
    S("kitchen", "He ate all day without ever being hungry. Tasting, snacking, sugar to stay awake, more sugar to keep going.",
      [C("ezra", "work", pos=[0.4, 0.5], face=180)], "side", time="day"),
    S("room", "Every night ended with a bottle of wine, a phone in his hand, and four hours of broken sleep.",
      [C("ezra", "seated", pos=[1.5, 0.5], face=200)], "top", time="night"),
    S("gym", "His body had not moved in years. The gym membership was still in his wallet, like a promise he had stopped believing.",
      [C("ezra", "walktired", pos=[-4, 1], to=[2, 1])], "track", time="dusk"),
    S("kitchen", "And when the pressure built up, he let it out on the people around him. He shouted at his cooks. He shouted at himself. Every single day.",
      [C("ezra", "punch", pos=[-0.6, 0.6], face=90), C("milo", "backoff", pos=[1.2, 0.6], to=[2.6, 1.4], face=-90)], "side", focus=0,
      punch="Harm always spreads."),
    S("kitchen", "Customers noticed before he did. The food was still good. But it had lost its soul. One by one, the tables went empty.",
      [C("ezra", "idle2", pos=[0, 0.9], face=0)], "low", time="night"),

    # ---------- THE VISIT ----------
    S("kitchen", "Then one rainy morning, his grandmother Ama walked into the kitchen. The woman who had taught him how to cook when he was six years old.",
      [C("ama", "walkslow", pos=[2.6, 2.5], to=[0.9, 1]), C("ezra", "idle", pos=[-0.8, 0.6], face=60)], "wide", time="dawn"),
    S("kitchen", "She tasted his soup, put the spoon down, and said: this soup is not bad. It is foggy. Just like you.",
      [C("ama", "interact", pos=[0.9, 0.9], face=-70), C("ezra", "idle2", pos=[-0.8, 0.6], face=70)], "close", time="dawn", focus=0,
      punch="It is foggy. Just like you."),
    S("kitchen", "She gave him forty days and three rules. Eat nothing until noon. Move your body every single day. And stop every harm. The wine. The shouting. The cruel voice in your head.",
      [C("ama", "idle", pos=[0.9, 0.9], face=-70), C("ezra", "idle", pos=[-0.8, 0.6], face=70)], "orbit", time="dawn", focus=1),
    S("kitchen", "Not to lose weight, she said. To get your senses back. A chef without senses is just a man with knives.",
      [C("ama", "interact", pos=[0.9, 0.9], face=-70), C("ezra", "idle2", pos=[-0.8, 0.6], face=70)], "push", time="dawn", focus=0),

    # ---------- CHAPTER 2 — TASTE ----------
    S("kitchen", "Day one was a war. By ten in the morning his hands were shaking and his mind was screaming for sugar.",
      [C("ezra", "seated", pos=[0, 0.55], face=180)], "push", time="dawn", chapterLabel="Chapter II", chapterTitle="Taste", color="#f2994a"),
    S("kitchen", "Day three was worse. But Ama told him something he never forgot. That is not hunger talking. That is habit leaving your body.",
      [C("ama", "idle", pos=[0.9, 0.9], face=-70), C("ezra", "seated", pos=[-0.4, 0.55], face=120)], "side", time="dawn", focus=1,
      punch="That is habit leaving."),
    S("kitchen", "On day nine, at exactly twelve o'clock, he broke his fast with the simplest thing in the kitchen. A slice of bread, olive oil, and a pinch of salt.",
      [C("ezra", "use", pos=[0, 0.4], face=180)], "close", time="day"),
    S("kitchen", "And he stopped. The bread was warm and sweet. The oil was green and peppery. The salt sparkled on his tongue. He tasted every single thing, as if for the first time.",
      [C("ezra", "idle2", pos=[0, 0.9], face=0)], "orbit", time="day"),
    S("kitchen", "That is the first wonder of the clarity state. When you stop eating all day, hunger comes back. And hunger turns the simplest food into a feast.",
      [C("ezra", "cheer", pos=[0, 0.9], face=0)], "pull", time="day", punch="Hunger is the best chef."),
    S("kitchen", "Ezra laughed alone in his kitchen. For the first time in years, food had colour again.",
      [C("ezra", "cook", pos=[0, 0.4], face=180)], "crane", time="day"),

    # ---------- CHAPTER 3 — BREATH ----------
    S("road", "Every morning before sunrise, Ezra walked. Then he jogged. And on the hill road outside the city, he kept passing the same runner.",
      [C("ezra", "run", pos=[0.8, 8], to=[0.8, -8]), C("lena", "run", pos=[-0.8, 5], to=[-0.8, -9])], "track", time="dawn",
      chapterLabel="Chapter III", chapterTitle="Breath", color="#56c2a6"),
    S("road", "Her name was Lena. Ten years ago she smoked a pack a day and could not climb a staircase without stopping.",
      [C("lena", "idle", pos=[-0.6, 0], face=40), C("ezra", "idle2", pos=[0.8, 0.2], face=-50)], "side", time="dawn", focus=0),
    S("road", "She looked at Ezra gasping for air and said: you are breathing like someone who is running away. Breathe like someone who is arriving.",
      [C("lena", "interact", pos=[-0.6, 0], face=40), C("ezra", "idle", pos=[0.8, 0.2], face=-50)], "close", time="dawn", focus=0,
      punch="Breathe like you are arriving."),
    S("road", "In through the nose. Slow. Deep into the belly. Out even slower. Step after step, his chest opened like a window after a long winter.",
      [C("ezra", "run", pos=[0.8, 8], to=[0.8, -8], speed=0.85)], "side", time="dawn"),
    S("summit", "On day twenty, they ran to the top of the hill together. The air was cold and clean, and every breath felt ten times deeper than it ever had.",
      [C("lena", "walk", pos=[-0.8, 3], to=[-0.8, 0.6]), C("ezra", "walk", pos=[0.8, 3.4], to=[0.8, 0.8])], "crane", time="dawn"),
    S("summit", "That is the second wonder. A body that moves every day, free from poison, breathes the way it was designed to breathe. And a calm breath means a calm mind.",
      [C("ezra", "idle", pos=[0, 0.5], face=180)], "orbit", time="dawn", punch="A calm breath. A calm mind."),
    S("summit", "Lena smiled. She had quit smoking not by fighting the cigarette, but by falling in love with the feeling of breathing.",
      [C("lena", "cheer", pos=[-0.8, 0.6], face=0), C("ezra", "idle2", pos=[0.8, 0.8], face=-20)], "pull", time="dawn", focus=0),

    # ---------- CHAPTER 4 — AWARENESS ----------
    S("stadium", "On a rest day, Lena took him to watch her brother Sol train. Sol was a goalkeeper, and everyone said he could see the future.",
      [C("sol", "crouch", pos=[0, 15], face=90)], "wide", focus=0, chapterLabel="Chapter IV", chapterTitle="Awareness", color="#16c2d5"),
    S("stadium", "Strikers took shot after shot. Sol was already moving before the ball was kicked. Left. Right. Dive. Save.",
      [C("sol", "dodge", pos=[0, 15], face=90)], "low", focus=0),
    S("stadium", "Ezra asked him how. Sol shrugged. When my mind is clean, the game slows down. I see the hips, the eyes, the breath of the striker. I just notice more.",
      [C("sol", "idle", pos=[-0.6, 15], face=40), C("ezra", "idle2", pos=[0.8, 15.2], face=-50)], "side", focus=0, punch="A clean mind sees more."),
    S("stadium", "Sol fasted in the morning, trained twice a day, and once a year he did the hardest thing of all. He cut out every person who pulled him back into chaos.",
      [C("sol", "jump", pos=[0, 15], face=90)], "orbit", focus=0),
    S("city", "That evening, Ezra walked home through the city. And he noticed things he had walked past for years.",
      [C("ezra", "walkslow", pos=[0, 2], to=[0, -10])], "track", time="dusk"),
    S("city", "The smell of rain on warm stone. The laughter from an open window. The colour of the sky between the buildings. The world had been there all along. He had simply been too foggy to see it.",
      [C("ezra", "idle", pos=[0, -2], face=0)], "orbit", time="dusk", punch="The world was always there."),
    S("kitchen", "The next morning, he noticed something else. The tired eyes of Milo, his youngest cook. The fear in his shoulders every time Ezra walked in.",
      [C("milo", "work", pos=[0.8, 0.5], face=180), C("ezra", "idle2", pos=[-1, 1.2], face=60)], "side", time="dawn", focus=1),
    S("kitchen", "Ezra put down his knife and said two words he had not said in years. I'm sorry. And for the first time, his kitchen went quiet in a good way.",
      [C("ezra", "interact", pos=[-0.4, 0.8], face=90), C("milo", "idle2", pos=[0.8, 0.8], face=-90)], "close", time="dawn", focus=0,
      punch="Stop the harm. Start the peace."),
    S("void", "That is the third wonder. When you stop harming yourself and others, your awareness becomes clean. You stop reacting. You start seeing.",
      [C("ezra", "meditate", pos=[0, 2.2], face=180)], "push", pillars=0),

    # ---------- CHAPTER 5 — CREATIVITY ----------
    S("stage", "On day thirty, Ezra was invited to a small concert. At the piano sat Ivy, a songwriter who had not written a single song in three years.",
      [C("ivy", "seated", pos=[0, 0.5], face=180)], "wide", chapterLabel="Chapter V", chapterTitle="Creativity", color="#c792ea"),
    S("stage", "She told the audience the truth. For three years I tried to force it. Coffee, late nights, people who drained me. The harder I pushed, the emptier it got.",
      [C("ivy", "idle2", pos=[1.4, 1.2], face=0)], "close"),
    S("stage", "Then I stopped forcing. I fasted in the mornings. I walked for an hour every afternoon. I stopped answering the people who made me feel small.",
      [C("ivy", "walkslow", pos=[-3, 1.8], to=[2.5, 1.8])], "track"),
    S("stage", "And the songs came back. Not at the piano. On walks. In the shower. In the quiet of an empty stomach. Ideas need space, and I had finally given them some.",
      [C("ivy", "work", pos=[0, 0.75], face=180)], "orbit", camAngle=180, punch="Ideas need space."),
    S("stage", "She played her new song, and Ezra felt something move inside his chest that he had not felt since he was a boy in his grandmother's kitchen.",
      [C("ivy", "work", pos=[0, 0.75], face=180)], "crane", camAngle=200),
    S("kitchen", "The next morning, before noon, with nothing in his stomach and nothing in his head but silence, the ideas started arriving.",
      [C("ezra", "seated", pos=[0, 0.55], face=180)], "push", time="dawn"),
    S("kitchen", "A soup made from roasted onions and smoke. A bread with burnt honey and sea salt. A dessert that tasted like the first day of summer.",
      [C("ezra", "cook", pos=[0, 0.4], face=180)], "orbit", time="day"),
    S("kitchen", "That is the fourth wonder. Creativity is not something you chase. It is what flows when you stop blocking it.",
      [C("ezra", "cheer", pos=[0, 0.9], face=0)], "pull", time="day", punch="Stop blocking it."),

    # ---------- CHAPTER 6 — RESULTS ----------
    S("kitchen", "On day forty, Ezra reopened his restaurant with a new menu. He called it Clarity.",
      [C("ezra", "cook", pos=[-0.6, 0.4], face=180), C("milo", "work", pos=[0.9, 0.5], face=180)], "wide", time="dusk",
      chapterLabel="Chapter VI", chapterTitle="Results", color="#f5c451"),
    S("kitchen", "His cooks were not afraid anymore. They laughed. They tried things. Milo created his first dish, and Ezra put it on the menu.",
      [C("milo", "cheer", pos=[0.9, 0.9], face=0), C("ezra", "idle", pos=[-0.6, 0.9], face=40)], "side", time="dusk", focus=0),
    S("city", "Word spread through the city. The tables filled up again. Then there was a waiting list. Then a waiting list for the waiting list.",
      [C("lena", "walk", pos=[-1, 4], to=[-1, -4]), C("sol", "walk", pos=[0.4, 5], to=[0.4, -3]), C("ivy", "walk", pos=[1.6, 4.5], to=[1.6, -3.5])], "track", time="dusk"),
    S("kitchen", "But the real result was not the money or the reviews. It was Ezra himself. He slept deeply. He woke up early without an alarm. He was calm under pressure.",
      [C("ezra", "cook", pos=[0, 0.4], face=180)], "orbit", time="dawn"),
    S("gym", "He trained every day, not to punish his body, but because movement had become the best part of his morning.",
      [C("ezra", "pushups", pos=[0, 0], face=90)], "low", time="dawn"),
    S("void", "That is the fifth wonder. Results are not the reward for working harder in the fog. They are what naturally happens when you work from a clear state.",
      [C("ezra", "idle", pos=[0, 2.2], face=180)], "push", pillars=0, punch="Clarity creates results."),

    # ---------- CHAPTER 7 — THE CLARITY STATE ----------
    S("void", "So what is the clarity state, really? It is not a secret. It is not a pill. It is what remains when you remove the fog.",
      [C("ezra", "idle2", pos=[0, 2.2], face=180)], "wide", pillars=0, chapterLabel="Chapter VII", chapterTitle="The Clarity State", color="#ffd166"),
    S("void", "Pillar one. Consistent fasting. Give your body hours without food, and it gives you back hunger, energy, and a taste for life.",
      [C("ezra", "seated", pos=[0, 2.2], face=180)], "push", pillars=1, punch="Pillar one. The fast."),
    S("void", "Pillar two. Consistent workouts. Move every single day, and your breath deepens, your sleep heals, and your mind finds its rhythm.",
      [C("ezra", "pushups", pos=[0, 2.2], face=90)], "orbit", pillars=2, punch="Pillar two. The work."),
    S("void", "Pillar three. Stay away from harm. Against others, and against yourself. The poison you drink, the words you shout, the voice that tells you that you are not enough.",
      [C("ezra", "meditate", pos=[0, 2.2], face=180)], "low", pillars=3, punch="Pillar three. The shield."),
    S("void", "Taste. Breath. Awareness. Creativity. Results. Five wonders. Three pillars. One state. And it is available to anyone willing to stay consistent.",
      [C("ezra", "idle", pos=[0, 2.2], face=180), C("lena", "idle2", pos=[-2.2, 2.8], face=30), C("ivy", "idle", pos=[2.2, 2.8], face=-30)], "crane", pillars=3,
      punch="Five wonders. Three pillars."),

    # ---------- CLIMAX ----------
    S("kitchen", "On the last night of the first week, after the final guest had left, Ama came back into the kitchen.",
      [C("ama", "walkslow", pos=[2.6, 2.5], to=[0.9, 1]), C("ezra", "idle", pos=[-0.8, 0.6], face=60)], "wide", time="night",
      chapterLabel="Chapter VIII", chapterTitle="The Taste of You", color="#ffcf6b"),
    S("kitchen", "Ezra made her the same soup. The one she had called foggy forty days before. His hands were steady. His mind was quiet.",
      [C("ezra", "cook", pos=[-0.2, 0.4], face=180)], "push", time="night"),
    S("kitchen", "She tasted it slowly. Closed her eyes. And then she smiled. Now, she said, it tastes like you again.",
      [C("ama", "use", pos=[0.9, 0.9], face=-70), C("ezra", "idle2", pos=[-0.8, 0.6], face=70)], "close", time="night", focus=0,
      punch="Now it tastes like you."),
    S("kitchen", "Ezra did not say anything. He just tasted it too. Salt. Smoke. Warmth. Memory. Everything.",
      [C("ezra", "idle", pos=[-0.8, 0.6], face=70), C("ama", "idle", pos=[0.9, 0.9], face=-70)], "orbit", time="night", focus=0),

    # ---------- OUTRO ----------
    S("void", "Lena found it in her breath. Sol in a clean mind. Ivy in the space for ideas. And Ezra found it in the soup that had lost its soul.",
      [C("lena", "idle", pos=[-2.4, 1.4], face=20), C("sol", "idle2", pos=[-0.8, 2.2], face=10), C("ivy", "idle", pos=[0.8, 2.2], face=-10), C("ezra", "idle2", pos=[2.4, 1.4], face=-20)],
      "wide", pillars=3, focus=3),
    S("void", "Your clarity state is waiting under the fog. Start tomorrow morning. One fast. One workout. One harm you finally let go of.",
      [C("ezra", "idle", pos=[0, 2.2], face=180)], "push", pillars=3, punch="Remove the fog."),
    S("void", "Then taste your food. Take a breath. Look around you. And notice how alive you really are.",
      [C("ezra", "meditate", pos=[0, 2.2], face=180)], "orbit", pillars=3),
    S("void", "This is Alpha Talks 3000. Fast. Train. Protect. And life will taste like life again.",
      [C("ezra", "idle", pos=[0, 2.2], face=180), C("ama", "idle2", pos=[-1.8, 2.8], face=30)], "crane", pillars=3, durationSec=10,
      titleCard={"title": "Fast. Train. Protect.", "subtitle": "Alphatalks3000"}),
]

story = {
    "title": "The Clarity State — Alphatalks3000",
    "characters": characters,
    "scenes": scenes,
    "thumbnail": {"text": "THE CLARITY STATE", "sub": "Life tastes 10x better", "scene": next(i for i, x in enumerate(scenes) if x.get("punch") == "Hunger is the best chef."), "at": 3},
}
json.dump(story, open("stories/clarity-state.json", "w"), indent=1)
words = sum(len((s.get("caption") or "").split()) for s in scenes)
print("scenes", len(scenes), "words", words, "est minutes", round(words / 2.25 / 60 + len(scenes) * 1.6 / 60 + 8 * 4 / 60, 1))
