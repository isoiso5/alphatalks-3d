import React, { useLayoutEffect, useMemo } from 'react';
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing } from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import { useThree } from '@react-three/fiber';
import * as THREE from 'three';
import { loadFont as loadCinzel } from '@remotion/google-fonts/Cinzel';
import { loadFont as loadMontserrat } from '@remotion/google-fonts/Montserrat';
import { Actor, actorPosition } from './Actor';
import { Environment } from './Environment';
import { FxLayer } from './Fx';
import { Library, useLibrary } from './models';
import { CamMode, Scene, StoryProps } from './types';

const { fontFamily: SERIF } = loadCinzel('normal', { weights: ['600', '700'], subsets: ['latin'] });
const { fontFamily: SANS } = loadMontserrat('normal', { weights: ['600', '800'], subsets: ['latin'] });

export const FPS = 30;
export const VO_LEAD = 0.5; // seconds of silence before narration starts in each scene
const GOLD = 'linear-gradient(180deg, #fff3c4 0%, #f5c451 45%, #b8862b 100%)';

export const sceneFrames = (s: Scene) => Math.max(1, Math.round(s.durationSec * FPS));
export const totalFrames = (p: StoryProps) => p.scenes.reduce((a, s) => a + sceneFrames(s), 0);

const ease = (k: number) => Easing.inOut(Easing.cubic)(THREE.MathUtils.clamp(k, 0, 1));

/* ---------------- camera ---------------- */

const CameraRig: React.FC<{ scene: Scene; t: number; aspect: number }> = ({ scene, t, aspect }) => {
  const { camera } = useThree();
  useLayoutEffect(() => {
    const sceneDur = Math.max(1, scene.durationSec);
    const at = (scene.slowmo ?? 1) * t;
    // montage: pick the active shot
    let shot: { at: number; camera: CamMode; camAngle?: number; zoom?: number; focus?: number } = {
      at: 0, camera: scene.camera ?? 'wide', camAngle: scene.camAngle, zoom: scene.zoom, focus: scene.focus,
    };
    let shotEnd = sceneDur;
    const shots = [...(scene.shots ?? [])].sort((a, b) => a.at - b.at);
    for (let i = 0; i < shots.length; i++) {
      if (t >= shots[i].at) {
        shot = shots[i];
        shotEnd = i + 1 < shots.length ? shots[i + 1].at : sceneDur;
      } else if (i === 0) {
        shotEnd = shots[0].at;
      }
    }
    const dur = Math.max(0.5, shotEnd - shot.at);
    const k = ease((t - shot.at) / dur);
    const cast = scene.cast ?? [];
    const fm = cast[shot.focus ?? 0];
    const [fx, fy, fz] = fm ? actorPosition(fm, at, sceneDur * (scene.slowmo ?? 1)) : [0, 0, 0];
    const F = new THREE.Vector3(fx, fy + 1.05, fz);
    const mode: CamMode = shot.camera;
    const portrait = aspect < 1;
    const zoom = shot.zoom ?? (portrait ? (cast.length > 1 ? 1.4 : 0.95) : 1);
    let off = new THREE.Vector3(0, 2, 8);
    let look = F.clone();
    switch (mode) {
      case 'wide':
        off.set(-1 + 2 * k, 2.4, 10);
        break;
      case 'push':
        off.set(0.6, 1.7 - 0.2 * k, 8.5 - 4.5 * k);
        break;
      case 'pull':
        off.set(0.4, 1.4 + 2.4 * k, 3.6 + 6 * k);
        break;
      case 'close':
        off.set(0.7 - 0.3 * k, 0.55, 2.8 - 0.4 * k);
        look = F.clone().add(new THREE.Vector3(0, 0.45, 0));
        break;
      case 'low':
        off.set(1.6 - 0.8 * k, -0.6, 4.6 - 0.6 * k);
        look = F.clone().add(new THREE.Vector3(0, 0.5, 0));
        break;
      case 'crane':
        off.set(0, -0.2 + 5.5 * k, 5 + 3 * k);
        break;
      case 'side':
        off.set(6.5, 0.6, 0.5 - k);
        break;
      case 'orbit': {
        const a = -0.6 + 1.2 * k;
        off.set(Math.sin(a) * 6, 1.3, Math.cos(a) * 6);
        break;
      }
      case 'track':
        off.set(-2.8, 0.8, 4.8);
        break;
      case 'top':
        off.set(0, 9 - 2 * k, 3.5);
        break;
      case 'spin': {
        const a = k * Math.PI * 2;
        off.set(Math.sin(a) * 4.5, 1.1 + 0.6 * Math.sin(k * Math.PI), Math.cos(a) * 4.5);
        break;
      }
      case 'drone':
        off.set(-6 + 12 * k, 7 - 2 * k, 9 - 3 * k);
        break;
      case 'dolly': {
        const e = 1 - Math.pow(1 - THREE.MathUtils.clamp((t - shot.at) / Math.min(1.4, dur), 0, 1), 3);
        off.set(0.4, 0.5, 9 - 6.6 * e);
        look = F.clone().add(new THREE.Vector3(0, 0.35, 0));
        break;
      }
      case 'dutch':
        off.set(2.2 - k, 0.9, 4.2);
        break;
      case 'hero':
        off.set(-1.2 + 2.4 * k, -0.85, 3.4);
        look = F.clone().add(new THREE.Vector3(0, 0.7, 0));
        break;
    }
    off.multiplyScalar(zoom);
    if (shot.camAngle) off.applyAxisAngle(new THREE.Vector3(0, 1, 0), (shot.camAngle * Math.PI) / 180);
    // subtle handheld breathing
    const bx = Math.sin(t * 0.7) * 0.04;
    const by = Math.sin(t * 0.9 + 1) * 0.03;
    const sh = scene.shake ?? 0;
    const sx = sh ? (Math.sin(t * 37.1) + Math.sin(t * 23.3)) * 0.04 * sh : 0;
    const sy = sh ? (Math.sin(t * 31.7) + Math.sin(t * 19.9)) * 0.04 * sh : 0;
    camera.position.set(F.x + off.x + bx + sx, Math.max(0.25, F.y + off.y + by + sy), F.z + off.z);
    camera.up.set(0, 1, 0);
    camera.lookAt(look);
    if (mode === 'dutch') camera.rotateZ(0.22);
    const pc = camera as THREE.PerspectiveCamera;
    pc.fov = mode === 'close' || mode === 'dolly' ? 30 : mode === 'hero' ? 46 : mode === 'drone' ? 44 : 38;
    pc.near = 0.05;
    pc.far = 400;
    pc.updateProjectionMatrix();
  });
  return null;
};

/* ---------------- 3D scene ---------------- */

const EXPOSURE: Record<string, number> = {
  studio: 0.85,
  kitchen: 1.0,
  court: 1.25,
  room: 1.6,
  road: 1.45,
  stadium: 1.35,
  stage: 1.5,
  city: 2.3,
  gym: 1.85,
  summit: 1.35,
  shore: 1.75,
  void: 1.7,
  forest: 1.9,
  cosmos: 2.3,
};

export const SceneView: React.FC<{ scene: Scene; t: number; lib: Library; characters: StoryProps['characters']; width: number; height: number; sceneKey: string }> = ({
  scene,
  t,
  lib,
  characters,
  width,
  height,
  sceneKey,
}) => (
  <ThreeCanvas
    width={width}
    height={height}
    shadows
    gl={{ antialias: true, toneMapping: THREE.ACESFilmicToneMapping, toneMappingExposure: EXPOSURE[scene.env] ?? 1.4, preserveDrawingBuffer: true }}
    camera={{ fov: 38, position: [0, 2, 8] }}
  >
    <CameraRig scene={scene} t={t} aspect={width / height} />
    <group key={sceneKey}>
      <Environment scene={scene} t={t} />
      <FxLayer
        fx={scene.fx}
        t={t * (scene.slowmo ?? 1)}
        center={scene.cast && scene.cast[0] ? actorPosition(scene.cast[0], t * (scene.slowmo ?? 1), scene.durationSec * (scene.slowmo ?? 1)) : [0, 0, 0]}
        color={scene.color}
      />
      {(scene.cast ?? []).map((m, i) => {
        const spec = characters[m.who];
        if (!spec) return null;
        const sm = scene.slowmo ?? 1;
        return <Actor key={`${sceneKey}-${i}`} lib={lib} spec={spec} member={m} t={t * sm} sceneDur={scene.durationSec * sm} />;
      })}
    </group>
  </ThreeCanvas>
);

/* ---------------- overlays ---------------- */

let grainUrl = '';
const getGrain = () => {
  if (grainUrl) return grainUrl;
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const g = c.getContext('2d')!;
  const img = g.createImageData(256, 256);
  let s = 1234567;
  for (let i = 0; i < img.data.length; i += 4) {
    s = (s * 16807) % 2147483647;
    const v = s % 255;
    img.data[i] = img.data[i + 1] = img.data[i + 2] = v;
    img.data[i + 3] = 22;
  }
  g.putImageData(img, 0, 0);
  grainUrl = c.toDataURL();
  return grainUrl;
};

const TONES: Record<string, string> = {
  neutral: 'linear-gradient(180deg, rgba(0,60,80,0.18), rgba(255,150,60,0.12))',
  cold: 'linear-gradient(180deg, rgba(20,70,120,0.42), rgba(40,90,130,0.30))',
  warm: 'linear-gradient(180deg, rgba(255,170,70,0.30), rgba(255,120,40,0.22))',
};

const Grade: React.FC<{ frame: number; portrait: boolean; bars: boolean; tone?: string }> = ({ frame, portrait, bars, tone }) => (
  <>
    <AbsoluteFill style={{ background: TONES[tone ?? 'neutral'] ?? TONES.neutral, mixBlendMode: 'soft-light' }} />
    <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)' }} />
    <AbsoluteFill
      style={{
        backgroundImage: `url(${getGrain()})`,
        backgroundPosition: `${(frame * 37) % 256}px ${(frame * 53) % 256}px`,
        opacity: 0.55,
        mixBlendMode: 'overlay',
      }}
    />
    {bars && !portrait && (
      <>
        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 92, background: '#000' }} />
        <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: 92, background: '#000' }} />
      </>
    )}
  </>
);

const goldText: React.CSSProperties = {
  backgroundImage: GOLD,
  WebkitBackgroundClip: 'text',
  backgroundClip: 'text',
  color: 'transparent',
  filter: 'drop-shadow(0 4px 18px rgba(0,0,0,0.85))',
};

const ChapterTitle: React.FC<{ label?: string; title: string; t: number; portrait: boolean }> = ({ label, title, t, portrait }) => {
  const o = interpolate(t, [0.2, 1.0, 3.6, 4.4], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const ls = interpolate(t, [0.2, 4.4], [18, 6], { extrapolateRight: 'clamp' });
  const line = interpolate(t, [0.4, 1.6], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', opacity: o, background: `rgba(0,0,0,${0.35 * o})` }}>
      {label && (
        <div style={{ fontFamily: SANS, fontWeight: 600, color: '#e8d6a6', fontSize: portrait ? 34 : 30, letterSpacing: ls, marginBottom: 18, textTransform: 'uppercase' }}>
          {label}
        </div>
      )}
      <div style={{ ...goldText, fontFamily: SERIF, fontWeight: 700, fontSize: portrait ? 92 : 110, textAlign: 'center', padding: '0 60px', lineHeight: 1.1 }}>{title}</div>
      <div style={{ width: 420 * line, height: 2, marginTop: 26, background: 'linear-gradient(90deg, transparent, #f5c451, transparent)' }} />
    </AbsoluteFill>
  );
};

const TitleCard: React.FC<{ title: string; subtitle?: string; t: number; dur: number; portrait: boolean }> = ({ title, subtitle, t, dur, portrait }) => {
  const o = interpolate(t, [0.3, 1.6, dur - 1.2, dur - 0.2], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const sc = interpolate(t, [0, dur], [1.08, 1.0]);
  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', opacity: o, background: `rgba(0,0,0,${0.45 * o})` }}>
      <div style={{ ...goldText, transform: `scale(${sc})`, fontFamily: SERIF, fontWeight: 700, fontSize: portrait ? 110 : 150, textAlign: 'center', lineHeight: 1.05, padding: '0 60px' }}>
        {title}
      </div>
      {subtitle && (
        <div style={{ fontFamily: SANS, fontWeight: 600, color: '#f1e6c8', fontSize: portrait ? 34 : 34, letterSpacing: 8, marginTop: 28, textTransform: 'uppercase', textAlign: 'center' }}>
          {subtitle}
        </div>
      )}
    </AbsoluteFill>
  );
};

const Punch: React.FC<{ text: string; t: number; dur: number; fps: number; portrait: boolean; at?: number }> = ({ text, t, dur, fps, portrait, at }) => {
  const start = at ?? Math.max(1.2, dur * 0.5);
  if (t < start) return null;
  const s = spring({ frame: Math.round((t - start) * fps), fps, config: { damping: 14, mass: 0.8 } });
  const o = interpolate(t, [start, start + 0.3, dur - 0.5, dur - 0.1], [0, 1, 1, 0], { extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', opacity: o }}>
      <div
        style={{
          ...goldText,
          transform: `scale(${0.7 + 0.3 * s})`,
          fontFamily: SERIF,
          fontWeight: 700,
          fontSize: portrait ? 104 : 96,
          textAlign: 'center',
          padding: portrait ? '0 70px' : '0 120px',
          lineHeight: 1.1,
          marginTop: portrait ? -520 : -160,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

type Word = { w: string; s: number; e: number };

const buildWords = (scene: Scene): Word[] => {
  const ext = (scene as Scene & { words?: Word[] }).words;
  if (ext && ext.length) return ext;
  const text = (scene.caption ?? '').trim();
  if (!text) return [];
  const words = text.split(/\s+/);
  const span = scene.voSec ?? Math.max(1, scene.durationSec - 1.2);
  const weights = words.map((w) => 0.6 + w.length * 0.12 + (/[.,!?;:—]$/.test(w) ? 0.6 : 0));
  const total = weights.reduce((a, b) => a + b, 0);
  let acc = 0;
  return words.map((w, i) => {
    const s = (acc / total) * span;
    acc += weights[i];
    return { w, s, e: (acc / total) * span };
  });
};

const Captions: React.FC<{ scene: Scene; t: number; portrait: boolean }> = ({ scene, t, portrait }) => {
  const words = useMemo(() => buildWords(scene), [scene]);
  if (!words.length) return null;
  const vt = t - ((scene as Scene & { voLead?: number }).voLead ?? (scene.chapterTitle || scene.titleCard ? 4.6 : VO_LEAD));
  // group into chunks of up to 6 words, break on punctuation
  const chunks: Word[][] = [];
  let cur: Word[] = [];
  words.forEach((w) => {
    cur.push(w);
    if (cur.length >= (portrait ? 3 : 6) || /[.,!?;:—]$/.test(w.w)) {
      chunks.push(cur);
      cur = [];
    }
  });
  if (cur.length) chunks.push(cur);
  const chunk = chunks.find((c) => vt >= c[0].s - 0.05 && vt < c[c.length - 1].e + 0.35) ?? null;
  if (!chunk) return null;
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center', paddingBottom: portrait ? 640 : 128 }}>
      <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '0 18px', maxWidth: portrait ? 880 : 1500, padding: portrait ? '0 60px' : '0 40px' }}>
        {chunk.map((w, i) => {
          const active = vt >= w.s && vt < w.e + 0.05;
          const done = vt >= w.e;
          return (
            <span
              key={i}
              style={{
                fontFamily: SANS,
                fontWeight: 800,
                fontSize: portrait ? 80 : 54,
                textTransform: portrait ? 'uppercase' : 'none',
                WebkitTextStroke: portrait ? '2px #000' : undefined,
                color: active ? '#ffd45e' : done ? '#ffffff' : 'rgba(255,255,255,0.78)',
                transform: active ? (portrait ? 'scale(1.15) rotate(-2deg)' : 'scale(1.08)') : 'scale(1)',
                textShadow: '0 3px 12px rgba(0,0,0,0.95), 0 0 2px #000',
                display: 'inline-block',
              }}
            >
              {w.w}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const Watermark: React.FC<{ portrait: boolean }> = ({ portrait }) => (
  <div
    style={{
      position: 'absolute',
      top: portrait ? 120 : 112,
      right: portrait ? 60 : 64,
      fontFamily: SERIF,
      fontWeight: 700,
      fontSize: 24,
      letterSpacing: 4,
      color: 'rgba(245,196,81,0.75)',
      textShadow: '0 2px 8px rgba(0,0,0,0.9)',
    }}
  >
    ALPHATALKS3000
  </div>
);

const Hook: React.FC<{ text: string; t: number; fps: number }> = ({ text, t, fps }) => {
  const s = spring({ frame: Math.round(t * fps), fps, config: { damping: 12, mass: 0.6 } });
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-start', alignItems: 'center', paddingTop: 230 }}>
      <div style={{ transform: `scale(${0.6 + 0.4 * s})`, background: 'rgba(0,0,0,0.55)', border: '3px solid #f5c451', borderRadius: 18, padding: '18px 34px', maxWidth: 900 }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, color: '#fff', fontSize: 62, lineHeight: 1.1, textAlign: 'center', textTransform: 'uppercase' }}>{text}</div>
      </div>
    </AbsoluteFill>
  );
};

const Progress: React.FC<{ k: number }> = ({ k }) => (
  <div style={{ position: 'absolute', top: 0, left: 0, height: 10, width: `${k * 100}%`, background: 'linear-gradient(90deg, #b8862b, #fff3c4)', boxShadow: '0 0 14px #f5c451' }} />
);

const Lightning: React.FC<{ t: number; seed: number }> = ({ t, seed }) => {
  // two deterministic flashes per scene
  const at = [1.4 + (seed % 3) * 0.7, 4.8 + (seed % 5) * 0.5];
  let o = 0;
  at.forEach((a) => {
    const d = t - a;
    if (d >= 0 && d < 0.5) o = Math.max(o, d < 0.06 ? 0.55 : d < 0.12 ? 0.1 : d < 0.18 ? 0.4 : 0.4 * (1 - (d - 0.18) / 0.32));
  });
  return o > 0 ? <AbsoluteFill style={{ background: '#dfe8ff', opacity: o, mixBlendMode: 'screen' }} /> : null;
};

const CutFlash: React.FC<{ scene: Scene; t: number }> = ({ scene, t }) => {
  // white flash at the start of a flash scene, quick light flicker on montage cuts, and a hit on the punch line
  let o = 0;
  if (scene.flash) o = Math.max(o, interpolate(t, [0, 0.05, 0.45], [1, 0.9, 0], { extrapolateRight: 'clamp' }));
  (scene.shots ?? []).forEach((s) => {
    const d = t - s.at;
    if (d >= 0 && d < 0.18) o = Math.max(o, 0.35 * (1 - d / 0.18));
  });
  if (scene.punch && scene.flash) {
    const d = t - (scene.punchAt ?? Math.max(1.2, scene.durationSec * 0.5));
    if (d >= 0 && d < 0.3) o = Math.max(o, 0.5 * (1 - d / 0.3));
  }
  return o > 0 ? <AbsoluteFill style={{ background: '#fff8e6', opacity: o }} /> : null;
};

/* ---------------- main composition ---------------- */

export const locateScene = (props: StoryProps, frame: number) => {
  let start = 0;
  for (let i = 0; i < props.scenes.length; i++) {
    const n = sceneFrames(props.scenes[i]);
    if (frame < start + n || i === props.scenes.length - 1) return { index: i, start, frames: n };
    start += n;
  }
  return { index: 0, start: 0, frames: 1 };
};

export const Story3D: React.FC<StoryProps> = (props) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const lib = useLibrary();
  const portrait = height > width;
  const { index, start, frames } = locateScene(props, frame);
  const scene = props.scenes[index];
  const local = frame - start;
  const t = local / fps;
  const dur = frames / fps;

  // fade through black between scenes
  const fadeIn = scene.fade || index === 0 ? 24 : 8;
  const black = Math.max(
    interpolate(local, [0, fadeIn], [1, 0], { extrapolateRight: 'clamp' }),
    interpolate(local, [frames - 8, frames], [0, 1], { extrapolateLeft: 'clamp' }) * (index === props.scenes.length - 1 ? 1 : 0.85),
  );

  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      <AbsoluteFill style={{ filter: scene.tone === 'cold' ? 'contrast(1.1) saturate(0.7)' : scene.tone === 'warm' ? 'contrast(1.08) saturate(1.25)' : 'contrast(1.08) saturate(1.12)' }}>
        {lib && (
          <SceneView scene={scene} t={t} lib={lib} characters={props.characters} width={width} height={height} sceneKey={`s${index}`} />
        )}
      </AbsoluteFill>
      <Grade frame={frame} portrait={portrait} bars tone={scene.tone} />
      {scene.time === 'storm' && <Lightning t={t} seed={index} />}
      <CutFlash scene={scene} t={t} />
      {scene.titleCard && <TitleCard title={scene.titleCard.title} subtitle={scene.titleCard.subtitle} t={t} dur={dur} portrait={portrait} />}
      {scene.chapterTitle && <ChapterTitle label={scene.chapterLabel} title={scene.chapterTitle} t={t} portrait={portrait} />}
      {scene.punch && <Punch text={scene.punch} t={t} dur={dur} fps={fps} portrait={portrait} at={scene.punchAt} />}
      {scene.hook && portrait && <Hook text={scene.hook} t={t} fps={fps} />}
      <Captions scene={scene} t={t} portrait={portrait} />
      <Watermark portrait={portrait} />
      {portrait && <Progress k={frame / Math.max(1, totalFrames(props))} />}
      <AbsoluteFill style={{ backgroundColor: '#000', opacity: black }} />
    </AbsoluteFill>
  );
};

/* ---------------- thumbnail ---------------- */

export const Thumbnail: React.FC<StoryProps> = (props) => {
  const { width, height } = useVideoConfig();
  const lib = useLibrary();
  const th = props.thumbnail ?? { text: props.title, scene: 0, at: 2 };
  const scene = props.scenes[Math.min(th.scene, props.scenes.length - 1)];
  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      <AbsoluteFill style={{ filter: 'contrast(1.15) saturate(1.25) brightness(1.05)' }}>
        {lib && <SceneView scene={scene} t={th.at ?? 2} lib={lib} characters={props.characters} width={width} height={height} sceneKey="thumb" />}
      </AbsoluteFill>
      <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.35) 55%, rgba(0,0,0,0) 100%)' }} />
      <AbsoluteFill style={{ justifyContent: 'center', paddingLeft: 70, width: '62%' }}>
        <div style={{ ...goldText, fontFamily: SERIF, fontWeight: 700, fontSize: 118, lineHeight: 1.0 }}>{th.text}</div>
        {th.sub && (
          <div style={{ fontFamily: SANS, fontWeight: 800, color: '#fff', fontSize: 44, marginTop: 22, textShadow: '0 3px 10px #000', textTransform: 'uppercase', letterSpacing: 2 }}>
            {th.sub}
          </div>
        )}
      </AbsoluteFill>
      <div style={{ position: 'absolute', bottom: 34, left: 70, fontFamily: SERIF, fontWeight: 700, fontSize: 30, letterSpacing: 5, color: '#f5c451' }}>
        ALPHATALKS3000
      </div>
    </AbsoluteFill>
  );
};
