import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Sequence,
  staticFile,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { ThreeCanvas } from '@remotion/three';
import * as THREE from 'three';

export type SceneType = 'sunrise' | 'workout' | 'shield' | 'orbit' | 'path' | 'lighthouse';

export type Scene = {
  type: SceneType;
  durationSec: number;
  chapterTitle?: string; // gold chapter title (optional)
  caption: string; // narration text shown as captions
  voiceoverUrl?: string; // mp3/wav URL for this scene
  voiceoverFile?: string; // file in /public (set by the GitHub Action TTS step)
  color?: string; // main accent color
};

export type StoryProps = {
  title: string;
  scenes: Scene[];
  musicUrl?: string;
  musicVolume?: number;
};

export const defaultStory: StoryProps = {
  title: 'Alpha Talks 3000',
  musicVolume: 0.15,
  scenes: [
    {
      type: 'sunrise',
      durationSec: 5,
      chapterTitle: 'Chapter 1 — The Fast',
      caption: 'Every morning he chose discipline before breakfast.',
      color: '#f5b942',
    },
    {
      type: 'workout',
      durationSec: 5,
      chapterTitle: 'Chapter 2 — The Grind',
      caption: 'One rep at a time, the body learns what the mind decides.',
      color: '#4fa3ff',
    },
    {
      type: 'shield',
      durationSec: 5,
      chapterTitle: 'Chapter 3 — The Shield',
      caption: 'Protect yourself. Protect others. That is real strength.',
      color: '#7cffb2',
    },
  ],
};

/* ---------------- 3D scenes ---------------- */

const Lights: React.FC<{ color: string }> = ({ color }) => (
  <>
    <ambientLight intensity={0.35} />
    <directionalLight position={[5, 8, 5]} intensity={1.4} castShadow />
    <pointLight position={[-4, 2, 3]} intensity={30} color={color} />
  </>
);

const Ground: React.FC = () => (
  <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.5, 0]} receiveShadow>
    <circleGeometry args={[12, 64]} />
    <meshStandardMaterial color="#14161c" roughness={0.9} />
  </mesh>
);

const SunriseScene: React.FC<{ f: number; color: string }> = ({ f, color }) => {
  const y = interpolate(f, [0, 120], [-2.5, 1.8], { extrapolateRight: 'clamp' });
  return (
    <>
      <mesh position={[0, y, -6]}>
        <sphereGeometry args={[1.6, 64, 64]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={1.2} />
      </mesh>
      {Array.from({ length: 14 }).map((_, i) => (
        <mesh key={i} position={[(i - 7) * 1.4, -1.2 + Math.sin(i * 1.7) * 0.4, -3 - (i % 3)]}>
          <coneGeometry args={[0.9, 2 + (i % 4) * 0.5, 4]} />
          <meshStandardMaterial color="#222634" flatShading />
        </mesh>
      ))}
    </>
  );
};

const WorkoutScene: React.FC<{ f: number; color: string }> = ({ f, color }) => {
  const lift = Math.abs(Math.sin(f / 12)) * 1.4;
  return (
    <group rotation={[0, f / 90, 0]}>
      {/* Stylized figure: body + head (no hands, by style rule) */}
      <mesh position={[0, -0.3, 0]} castShadow>
        <capsuleGeometry args={[0.45, 1.1, 8, 16]} />
        <meshStandardMaterial color="#d9dde6" roughness={0.4} />
      </mesh>
      <mesh position={[0, 0.85, 0]} castShadow>
        <sphereGeometry args={[0.35, 32, 32]} />
        <meshStandardMaterial color="#d9dde6" roughness={0.4} />
      </mesh>
      {/* Barbell */}
      <group position={[0, 0.3 + lift, 0]}>
        <mesh rotation={[0, 0, Math.PI / 2]}>
          <cylinderGeometry args={[0.05, 0.05, 3, 16]} />
          <meshStandardMaterial color="#999" metalness={0.9} roughness={0.2} />
        </mesh>
        {[-1.4, 1.4].map((x) => (
          <mesh key={x} position={[x, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
            <cylinderGeometry args={[0.45, 0.45, 0.2, 32]} />
            <meshStandardMaterial color={color} metalness={0.5} roughness={0.3} />
          </mesh>
        ))}
      </group>
    </group>
  );
};

const ShieldScene: React.FC<{ f: number; color: string }> = ({ f, color }) => {
  const s = interpolate(f, [0, 40], [0.2, 1], { extrapolateRight: 'clamp' });
  return (
    <group scale={s} rotation={[0, Math.sin(f / 40) * 0.6, 0]}>
      <mesh>
        <icosahedronGeometry args={[1.5, 1]} />
        <meshStandardMaterial color={color} wireframe />
      </mesh>
      <mesh>
        <icosahedronGeometry args={[1.1, 0]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.4} flatShading />
      </mesh>
      {Array.from({ length: 24 }).map((_, i) => {
        const a = (i / 24) * Math.PI * 2 + f / 60;
        return (
          <mesh key={i} position={[Math.cos(a) * 3, Math.sin(a * 2) * 0.5, Math.sin(a) * 3]}>
            <sphereGeometry args={[0.08, 12, 12]} />
            <meshStandardMaterial color="#fff" emissive="#fff" emissiveIntensity={1} />
          </mesh>
        );
      })}
    </group>
  );
};

const OrbitScene: React.FC<{ f: number; color: string }> = ({ f, color }) => (
  <group rotation={[0.3, f / 50, 0]}>
    <mesh>
      <torusKnotGeometry args={[1, 0.3, 160, 24]} />
      <meshStandardMaterial color={color} metalness={0.7} roughness={0.2} />
    </mesh>
  </group>
);

const PathScene: React.FC<{ f: number; color: string }> = ({ f, color }) => (
  <group position={[0, 0, (f / 30) % 2]}>
    {Array.from({ length: 20 }).map((_, i) => (
      <mesh key={i} position={[0, -1.4, -i * 2]}>
        <boxGeometry args={[1.2, 0.1, 1.6]} />
        <meshStandardMaterial color={i % 2 ? color : '#333'} />
      </mesh>
    ))}
  </group>
);

const LighthouseScene: React.FC<{ f: number; color: string }> = ({ f, color }) => {
  const a = f / 25;
  return (
    <group rotation={[0, Math.sin(f / 200) * 0.4, 0]}>
      <mesh position={[0, 0.4, -1]} castShadow>
        <cylinderGeometry args={[0.35, 0.6, 3.6, 24]} />
        <meshStandardMaterial color="#e9e4da" roughness={0.6} />
      </mesh>
      <mesh position={[0, 2.4, -1]}>
        <sphereGeometry args={[0.35, 24, 24]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={2} />
      </mesh>
      <mesh position={[Math.cos(a) * 2.5, 2.4, -1 + Math.sin(a) * 2.5]} rotation={[0, -a, Math.PI / 2]}>
        <coneGeometry args={[0.6, 5, 24, 1, true]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.6} transparent opacity={0.25} />
      </mesh>
      {Array.from({ length: 10 }).map((_, i) => (
        <mesh key={i} position={[(i - 5) * 1.5, -1.35 + Math.sin(f / 15 + i) * 0.08, 1 + (i % 2)]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[1.6, 0.6]} />
          <meshStandardMaterial color="#1e3a5f" metalness={0.6} roughness={0.2} />
        </mesh>
      ))}
    </group>
  );
};

const Scene3D: React.FC<{ scene: Scene }> = ({ scene }) => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const color = scene.color ?? '#f5b942';
  const camZ = interpolate(f, [0, scene.durationSec * 30], [8, 6.5]);
  const map: Record<SceneType, React.ReactNode> = {
    sunrise: <SunriseScene f={f} color={color} />,
    workout: <WorkoutScene f={f} color={color} />,
    shield: <ShieldScene f={f} color={color} />,
    orbit: <OrbitScene f={f} color={color} />,
    path: <PathScene f={f} color={color} />,
    lighthouse: <LighthouseScene f={f} color={color} />,
  };
  return (
    <ThreeCanvas
      width={width}
      height={height}
      camera={{ fov: 45, position: [0, 0.8, camZ] }}
      gl={{ antialias: true, toneMapping: THREE.ACESFilmicToneMapping }}
      style={{ background: 'radial-gradient(#1d2333, #07080c)' }}
    >
      <Lights color={color} />
      <Ground />
      {map[scene.type] ?? map.orbit}
    </ThreeCanvas>
  );
};

/* ---------------- Captions & titles ---------------- */

const Captions: React.FC<{ text: string; durationSec: number }> = ({ text, durationSec }) => {
  const f = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const words = text.split(/\s+/).filter(Boolean);
  const chunkSize = 4;
  const chunks: string[] = [];
  for (let i = 0; i < words.length; i += chunkSize) chunks.push(words.slice(i, i + chunkSize).join(' '));
  const per = (durationSec * fps) / Math.max(1, chunks.length);
  const idx = Math.min(chunks.length - 1, Math.floor(f / per));
  const local = f - idx * per;
  const pop = spring({ frame: local, fps, config: { damping: 12 } });
  const vertical = height > width;
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center', paddingBottom: vertical ? 420 : 110 }}>
      <div
        style={{
          transform: `scale(${0.85 + pop * 0.15})`,
          fontFamily: 'Arial Black, Arial, sans-serif',
          fontSize: vertical ? 78 : 64,
          color: 'white',
          textAlign: 'center',
          maxWidth: '85%',
          textShadow: '0 4px 18px rgba(0,0,0,0.9), 0 0 2px #000',
          WebkitTextStroke: '2px black',
        }}
      >
        {chunks[idx]}
      </div>
    </AbsoluteFill>
  );
};

const ChapterTitle: React.FC<{ text: string }> = ({ text }) => {
  const f = useCurrentFrame();
  const opacity = interpolate(f, [0, 15, 60, 80], [0, 1, 1, 0], { extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-start', alignItems: 'center', paddingTop: 90 }}>
      <div
        style={{
          opacity,
          fontFamily: 'Georgia, serif',
          fontSize: 60,
          letterSpacing: 4,
          color: '#e8c15a',
          textShadow: '0 0 24px rgba(232,193,90,0.6)',
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

/* ---------------- Main composition ---------------- */

export const Story3D: React.FC<StoryProps> = ({ scenes, musicUrl, musicVolume = 0.15 }) => {
  const { fps } = useVideoConfig();
  let from = 0;
  return (
    <AbsoluteFill style={{ backgroundColor: '#07080c' }}>
      {musicUrl ? <Audio src={musicUrl} volume={musicVolume} loop /> : null}
      {scenes.map((sc, i) => {
        const dur = Math.round(sc.durationSec * fps);
        const start = from;
        from += dur;
        return (
          <Sequence key={i} from={start} durationInFrames={dur}>
            <Scene3D scene={sc} />
            {sc.chapterTitle ? <ChapterTitle text={sc.chapterTitle} /> : null}
            <Captions text={sc.caption} durationSec={sc.durationSec} />
            {sc.voiceoverFile ? (
              <Audio src={staticFile(sc.voiceoverFile)} />
            ) : sc.voiceoverUrl ? (
              <Audio src={sc.voiceoverUrl} />
            ) : null}
          </Sequence>
        );
      })}
      {/* Cinematic vignette */}
      <AbsoluteFill style={{ background: 'radial-gradient(transparent 55%, rgba(0,0,0,0.65))' }} />
    </AbsoluteFill>
  );
};
