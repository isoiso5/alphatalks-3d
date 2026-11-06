export type EnvName =
  | 'stadium'
  | 'court'
  | 'studio'
  | 'stage'
  | 'gym'
  | 'city'
  | 'road'
  | 'room'
  | 'kitchen'
  | 'summit'
  | 'shore'
  | 'forest'
  | 'cosmos'
  | 'void';

export type TimeOfDay = 'dawn' | 'day' | 'dusk' | 'night' | 'storm';

export type CamMode =
  | 'wide'
  | 'push'
  | 'pull'
  | 'close'
  | 'low'
  | 'crane'
  | 'side'
  | 'orbit'
  | 'track'
  | 'top'
  | 'spin'
  | 'drone'
  | 'dolly'
  | 'dutch'
  | 'hero';

export type FxName =
  | 'sparks'
  | 'embers'
  | 'fireflies'
  | 'petals'
  | 'confetti'
  | 'fireworks'
  | 'stars'
  | 'godrays'
  | 'aura'
  | 'speed'
  | 'shockwave';

// a camera cut inside one scene (montage)
export type Shot = { at: number; camera: CamMode; camAngle?: number; zoom?: number; focus?: number };

export type HairStyle = 'short' | 'bun' | 'afro' | 'beanie' | 'cap' | 'bald';

export type CharacterSpec = {
  skin: string;
  shirt: string;
  pants: string;
  hair?: HairStyle;
  hairColor?: string;
  sleeves?: boolean; // true = arms in shirt colour (hoodie / long sleeves)
  height?: number; // 1 = 1.75m
  eyeColor?: string;
  beard?: boolean;
};

export type CastMember = {
  who: string; // key in StoryProps.characters
  action: string; // see ACTIONS in Actor.tsx
  pos?: [number, number]; // x, z
  to?: [number, number]; // walk/run to this x, z during the scene
  y?: number; // elevation (e.g. lying on a bed)
  face?: number; // degrees, 0 = facing camera (+z)
  speed?: number; // animation speed multiplier
  delay?: number; // seconds before the action starts
  gloves?: string; // boxing glove colour
  ball?: boolean; // basketball in right hand
};

export type Scene = {
  env: EnvName;
  time?: TimeOfDay;
  durationSec: number;
  voSec?: number; // narration length (set by scripts/tts.py)
  voiceoverFile?: string;
  chapterLabel?: string; // e.g. "Chapter II"
  chapterTitle?: string; // gold chapter title
  caption?: string; // narration text
  punch?: string; // big punch line on screen
  titleCard?: { title: string; subtitle?: string };
  cast?: CastMember[];
  camera?: CamMode;
  camAngle?: number; // degrees, rotates the camera around the focus
  focus?: number; // index of cast member the camera follows
  color?: string; // accent colour
  paint?: [number, number]; // painting progress from..to (studio)
  pillars?: number; // 0-3 lit pillars (void)
  shot?: 'make' | 'miss'; // basketball shot (court)
  shotAt?: number; // seconds into the scene
  piano?: boolean; // piano on stage
  fade?: boolean; // fade from black at the start
  hook?: string; // big text at the top of the frame (Shorts hook)
  punchAt?: number; // seconds into the scene when the punch line lands
  zoom?: number; // camera distance multiplier override
  lead?: number; // seconds of silence before narration (overrides default)
  weather?: 'rain' | 'snow'; // falling rain / snow particles
  tone?: 'cold' | 'warm'; // colour grade: cold = the old life, warm = the new life
  mood?: 'calm' | 'dark' | 'hope' | 'rise'; // soundtrack mood from this scene on
  music?: string; // switch melody theme from this scene on
  fx?: FxName[]; // particle / light effects
  shots?: Shot[]; // extra camera cuts inside the scene
  slowmo?: number; // animation speed (0.35 = slow motion)
  flash?: boolean; // white flash cut into this scene
  shake?: number; // camera shake strength (0.5 = strong)
};

export type StoryProps = {
  title: string;
  characters: Record<string, CharacterSpec>;
  scenes: Scene[];
  ttsRate?: string; // e.g. "+4%" (Shorts read a little faster)
  thumbnail?: { text: string; sub?: string; scene: number; at?: number };
};
