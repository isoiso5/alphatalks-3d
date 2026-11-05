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
  | 'void';

export type TimeOfDay = 'dawn' | 'day' | 'dusk' | 'night';

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
  | 'top';

export type HairStyle = 'short' | 'bun' | 'afro' | 'beanie' | 'cap' | 'bald';

export type CharacterSpec = {
  skin: string;
  shirt: string;
  pants: string;
  hair?: HairStyle;
  hairColor?: string;
  sleeves?: boolean; // true = arms in shirt colour (hoodie / long sleeves)
  height?: number; // 1 = 1.75m
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
};

export type StoryProps = {
  title: string;
  characters: Record<string, CharacterSpec>;
  scenes: Scene[];
  ttsRate?: string; // e.g. "+4%" (Shorts read a little faster)
  thumbnail?: { text: string; sub?: string; scene: number; at?: number };
};
