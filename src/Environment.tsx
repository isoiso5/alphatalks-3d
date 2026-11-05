import React, { useMemo } from 'react';
import * as THREE from 'three';
import { EnvName, Scene, TimeOfDay } from './types';
import { getBallTexture } from './models';

/* ---------- helpers ---------- */

const rand = (seed: number) => {
  let s = seed % 2147483647;
  if (s <= 0) s += 2147483646;
  return () => (s = (s * 16807) % 2147483647) / 2147483647;
};

let glowTex: THREE.CanvasTexture | null = null;
const getGlow = () => {
  if (glowTex) return glowTex;
  const c = document.createElement('canvas');
  c.width = c.height = 128;
  const g = c.getContext('2d')!;
  const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
  gr.addColorStop(0, 'rgba(255,255,255,1)');
  gr.addColorStop(0.25, 'rgba(255,255,255,0.45)');
  gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr;
  g.fillRect(0, 0, 128, 128);
  glowTex = new THREE.CanvasTexture(c);
  return glowTex;
};

export const Glow: React.FC<{ position: [number, number, number]; color: string; size: number; opacity?: number }> = ({
  position,
  color,
  size,
  opacity = 0.8,
}) => (
  <sprite position={position} scale={[size, size, 1]}>
    <spriteMaterial
      map={getGlow()}
      color={color}
      transparent
      opacity={opacity}
      blending={THREE.AdditiveBlending}
      depthWrite={false}
      fog={false}
    />
  </sprite>
);

const M: React.FC<{ c: string; r?: number; m?: number; e?: string; ei?: number }> = ({ c, r = 0.8, m = 0, e, ei = 0 }) => (
  <meshStandardMaterial color={c} roughness={r} metalness={m} emissive={e ?? '#000000'} emissiveIntensity={ei} />
);

const Box: React.FC<{
  p: [number, number, number];
  s: [number, number, number];
  c: string;
  r?: number;
  m?: number;
  e?: string;
  ei?: number;
  rot?: [number, number, number];
  shadow?: boolean;
}> = ({ p, s, c, r, m, e, ei, rot, shadow = true }) => (
  <mesh position={p} rotation={rot} castShadow={shadow} receiveShadow>
    <boxGeometry args={s} />
    <M c={c} r={r} m={m} e={e} ei={ei} />
  </mesh>
);

/* ---------- sky + light presets ---------- */

type Preset = { top: string; horizon: string; fog: string; amb: number; ambC: string; key: string; keyI: number; sun: [number, number, number] };

const PRESETS: Record<TimeOfDay, Preset> = {
  dawn: { top: '#2a2f5c', horizon: '#f2a36b', fog: '#b98073', amb: 0.45, ambC: '#a9a2c8', key: '#ffb47a', keyI: 2.2, sun: [-12, 3, -20] },
  day: { top: '#3d78c2', horizon: '#cfe3f2', fog: '#b9cfe0', amb: 0.7, ambC: '#cfe0ff', key: '#fff4e0', keyI: 2.6, sun: [10, 20, 8] },
  dusk: { top: '#1d1b3d', horizon: '#ff7a4a', fog: '#7a4a52', amb: 0.4, ambC: '#9a86c0', key: '#ff9a5c', keyI: 2.0, sun: [14, 4, -18] },
  night: { top: '#03050d', horizon: '#121a33', fog: '#0a0f1f', amb: 0.25, ambC: '#5a6aa8', key: '#9fb8ff', keyI: 0.7, sun: [-8, 14, 6] },
  storm: { top: '#1c2230', horizon: '#56606e', fog: '#3e4652', amb: 0.55, ambC: '#a6b2c4', key: '#c9d6e8', keyI: 1.3, sun: [-6, 16, 8] },
};

const Sky: React.FC<{ p: Preset }> = ({ p }) => {
  const mat = useMemo(
    () =>
      new THREE.ShaderMaterial({
        side: THREE.BackSide,
        depthWrite: false,
        fog: false,
        uniforms: { top: { value: new THREE.Color(p.top) }, bottom: { value: new THREE.Color(p.horizon) } },
        vertexShader:
          'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0); }',
        fragmentShader:
          'uniform vec3 top; uniform vec3 bottom; varying vec3 vP; void main(){ float h = clamp(vP.y*1.6+0.08,0.0,1.0); gl_FragColor = vec4(mix(bottom, top, pow(h,0.7)),1.0); #include <tonemapping_fragment>\n#include <colorspace_fragment>\n }',
      }),
    [p.top, p.horizon],
  );
  return (
    <mesh material={mat}>
      <sphereGeometry args={[150, 32, 16]} />
    </mesh>
  );
};

const Dust: React.FC<{ t: number; color: string; count?: number; spread?: number; seed?: number }> = ({
  t,
  color,
  count = 260,
  spread = 14,
  seed = 7,
}) => {
  const base = useMemo(() => {
    const r = rand(seed);
    return Array.from({ length: count }, () => [(r() - 0.5) * spread, r() * 6, (r() - 0.5) * spread, r() * 6.28]);
  }, [count, spread, seed]);
  const geo = useMemo(() => new THREE.BufferGeometry(), []);
  const arr = new Float32Array(count * 3);
  base.forEach(([x, y, z, ph], i) => {
    arr[i * 3] = x + Math.sin(t * 0.3 + ph) * 0.4;
    arr[i * 3 + 1] = (y + t * 0.12) % 6;
    arr[i * 3 + 2] = z + Math.cos(t * 0.25 + ph) * 0.4;
  });
  geo.setAttribute('position', new THREE.BufferAttribute(arr, 3));
  return (
    <points geometry={geo}>
      <pointsMaterial color={color} size={0.035} transparent opacity={0.7} blending={THREE.AdditiveBlending} depthWrite={false} />
    </points>
  );
};

/* ---------- painting texture ---------- */

const paintCache = new Map<number, THREE.CanvasTexture>();
const getPainting = (progress: number) => {
  const key = Math.round(THREE.MathUtils.clamp(progress, 0, 1) * 120);
  const hit = paintCache.get(key);
  if (hit) return hit;
  const c = document.createElement('canvas');
  c.width = 512;
  c.height = 384;
  const g = c.getContext('2d')!;
  g.fillStyle = '#f2ece0';
  g.fillRect(0, 0, 512, 384);
  const r = rand(42);
  const palette = ['#1d2a4f', '#2f4d7a', '#e8a33d', '#f2c66d', '#c2563a', '#f7e3b0', '#5a3d6b'];
  for (let i = 0; i < key * 3; i++) {
    const y = r() * 384;
    const x = r() * 512;
    const sky = y < 230;
    const col = sky ? palette[Math.floor(r() * 2)] : palette[2 + Math.floor(r() * 5)];
    g.strokeStyle = col;
    g.globalAlpha = 0.55;
    g.lineWidth = 6 + r() * 18;
    g.lineCap = 'round';
    g.beginPath();
    g.moveTo(x, y);
    g.quadraticCurveTo(x + 40 * r(), y - 20 + 40 * r(), x + 30 + 90 * r(), y - 10 + 20 * r());
    g.stroke();
    if (i === 200) {
      g.globalAlpha = 0.9;
      g.fillStyle = '#ffd36b';
      g.beginPath();
      g.arc(256, 230, 60, Math.PI, 0);
      g.fill();
    }
  }
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  paintCache.set(key, tex);
  return tex;
};

/* ---------- environments ---------- */

const Floor: React.FC<{ c: string; size?: number; r?: number; m?: number }> = ({ c, size = 80, r = 0.9, m = 0 }) => (
  <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
    <planeGeometry args={[size, size]} />
    <M c={c} r={r} m={m} />
  </mesh>
);

const Stadium: React.FC<{ t: number }> = () => (
  <>
    <Floor c="#2b5a32" />
    {/* running track */}
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]} receiveShadow>
      <ringGeometry args={[12, 18, 96]} />
      <M c="#a8442e" r={0.95} />
    </mesh>
    {[13.2, 14.4, 15.6, 16.8].map((r) => (
      <mesh key={r} rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.02, 0]}>
        <ringGeometry args={[r, r + 0.06, 128]} />
        <meshBasicMaterial color="#f4efe6" />
      </mesh>
    ))}
    {/* stands */}
    {Array.from({ length: 10 }).map((_, i) => (
      <Box key={i} p={[0, 0.5 + i * 0.7, -22 - i * 1.2]} s={[70, 1, 1.2]} c={i % 2 ? '#2a2f3d' : '#323849'} shadow={false} />
    ))}
    {/* flood lights */}
    {[-22, 22].map((x) => (
      <group key={x} position={[x, 0, -24]}>
        <Box p={[0, 9, 0]} s={[0.5, 18, 0.5]} c="#555" m={0.6} shadow={false} />
        <Box p={[0, 18.5, 0.3]} s={[4, 1.6, 0.4]} c="#fff" e="#ffffff" ei={3} shadow={false} />
        <Glow position={[0, 18.5, 1]} color="#eef4ff" size={14} />
      </group>
    ))}
    <spotLight position={[0, 20, 6]} angle={0.6} penumbra={0.6} intensity={400} color="#f1f5ff" castShadow />
  </>
);

const Court: React.FC<{ scene: Scene; t: number }> = ({ scene, t }) => {
  const rim: [number, number, number] = [0, 3.05, -5.6];
  const shotT = scene.shotAt ?? 1e9;
  let ball: [number, number, number] | null = null;
  const shooter = scene.cast?.[0]?.pos ?? [0, 2];
  if (scene.shot && t >= shotT) {
    const k = (t - shotT) / 1.1;
    const start: [number, number, number] = [shooter[0], 2.3, shooter[1] - 0.3];
    if (k <= 1) {
      const target = scene.shot === 'make' ? rim : [rim[0] + 0.28, rim[1] + 0.05, rim[2] + 0.1];
      ball = [
        start[0] + (target[0] - start[0]) * k,
        start[1] + (target[1] - start[1]) * k + Math.sin(Math.PI * k) * 2.4,
        start[2] + (target[2] - start[2]) * k,
      ];
    } else {
      const k2 = Math.min(2.5, k - 1);
      if (scene.shot === 'make') ball = [rim[0], Math.max(0.12, rim[1] - k2 * 3.2), rim[2] + k2 * 0.4];
      else ball = [rim[0] + 0.28 + k2 * 1.8, Math.max(0.12, rim[1] + Math.sin(Math.min(Math.PI, k2 * 3)) * 0.8 - k2 * 1.8), rim[2] + k2 * 2.2];
    }
  }
  return (
    <>
      <Floor c="#b5834a" r={0.45} m={0.05} size={60} />
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, -5.6]}>
        <ringGeometry args={[6.6, 6.7, 64, 1, Math.PI, Math.PI]} />
        <meshBasicMaterial color="#f5f0e6" />
      </mesh>
      <Box p={[0, 0.01, -3.6]} s={[3.6, 0.01, 4]} c="#7a2f2a" r={0.5} shadow={false} />
      {/* hoop */}
      <Box p={[0, 1.8, -6.6]} s={[0.25, 3.6, 0.25]} c="#2b2f38" m={0.6} />
      <Box p={[0, 3.6, -6.0]} s={[1.8, 1.05, 0.06]} c="#e9eef5" r={0.2} />
      <mesh position={rim} rotation={[Math.PI / 2, 0, 0]} castShadow>
        <torusGeometry args={[0.23, 0.02, 10, 32]} />
        <M c="#ff5a1f" m={0.4} r={0.3} />
      </mesh>
      <mesh position={[rim[0], rim[1] - 0.22, rim[2]]}>
        <cylinderGeometry args={[0.23, 0.15, 0.42, 16, 1, true]} />
        <meshStandardMaterial color="#f2f2f2" wireframe />
      </mesh>
      {ball && (
        <mesh position={ball} castShadow>
          <sphereGeometry args={[0.12, 24, 16]} />
          <meshStandardMaterial map={getBallTexture()} roughness={0.7} />
        </mesh>
      )}
      {/* gym walls & bleachers */}
      <Box p={[0, 6, -14]} s={[40, 12, 0.5]} c="#1d2230" shadow={false} />
      {Array.from({ length: 5 }).map((_, i) => (
        <Box key={i} p={[0, 0.4 + i * 0.6, 10 + i * 0.9]} s={[24, 0.8, 0.9]} c="#3a3f4f" shadow={false} />
      ))}
      <spotLight position={[0, 12, -1]} angle={0.55} penumbra={0.7} intensity={320} color="#fff1d6" castShadow />
      <Glow position={[0, 11.5, -1]} color="#fff1d6" size={4} />
    </>
  );
};

const Studio: React.FC<{ scene: Scene; t: number }> = ({ scene, t }) => {
  const [a, b] = scene.paint ?? [0.05, 0.05];
  const k = THREE.MathUtils.clamp(t / Math.max(1, scene.durationSec), 0, 1);
  const tex = getPainting(a + (b - a) * k);
  return (
    <>
      <Floor c="#5b4434" r={0.7} size={30} />
      <Box p={[0, 4, -5]} s={[16, 8, 0.3]} c="#d9cbb5" shadow={false} />
      <Box p={[-8, 4, 0]} s={[0.3, 8, 12]} c="#cbbca5" shadow={false} />
      {/* window with light shaft */}
      <Box p={[3.5, 3.6, -4.82]} s={[3, 3.4, 0.05]} c="#fff3d6" e="#ffe2a8" ei={2} shadow={false} />
      <Glow position={[3.5, 3.6, -4.6]} color="#ffd9a0" size={9} opacity={0.6} />
      <directionalLight position={[6, 7, -9]} intensity={2.2} color="#ffd8a8" castShadow />
      {/* easel + canvas */}
      <group position={[0.9, 0, -1.2]} rotation={[0, -0.35, 0]}>
        <Box p={[0, 1.0, 0.05]} s={[0.08, 2, 0.08]} c="#6b4a2f" rot={[-0.08, 0, 0]} />
        <Box p={[-0.6, 0.9, 0.25]} s={[0.07, 1.9, 0.07]} c="#6b4a2f" rot={[0.12, 0, 0.12]} />
        <Box p={[0.6, 0.9, 0.25]} s={[0.07, 1.9, 0.07]} c="#6b4a2f" rot={[0.12, 0, -0.12]} />
        <mesh position={[0, 1.55, 0.18]} rotation={[-0.08, 0, 0]} castShadow>
          <boxGeometry args={[1.5, 1.1, 0.05]} />
          <meshStandardMaterial attach="material-0" color="#ddd" />
          <meshStandardMaterial attach="material-1" color="#ddd" />
          <meshStandardMaterial attach="material-2" color="#ddd" />
          <meshStandardMaterial attach="material-3" color="#ddd" />
          <meshStandardMaterial attach="material-4" map={tex} roughness={0.8} />
          <meshStandardMaterial attach="material-5" color="#ddd" />
        </mesh>
      </group>
      {/* table with paints */}
      <Box p={[-2.2, 0.75, -1.5]} s={[1.6, 0.08, 0.9]} c="#7b5a3c" />
      <Box p={[-2.2, 0.37, -1.5]} s={[1.4, 0.74, 0.7]} c="#5e4430" />
      {['#e8a33d', '#2f4d7a', '#c2563a', '#f7e3b0'].map((c, i) => (
        <mesh key={c} position={[-2.7 + i * 0.3, 0.84, -1.4]} castShadow>
          <cylinderGeometry args={[0.07, 0.07, 0.12, 16]} />
          <M c={c} r={0.4} />
        </mesh>
      ))}
      {/* stacked canvases */}
      {[0, 1, 2].map((i) => (
        <Box key={i} p={[-6.5, 0.7, -2 + i * 0.4]} s={[0.06, 1.4, 1.1]} c={['#a85b3a', '#3b4f73', '#d8b56a'][i]} rot={[0, 0, 0.12]} />
      ))}
    </>
  );
};

const Piano: React.FC<{ p: [number, number, number]; rot?: number }> = ({ p, rot = 0 }) => (
  <group position={p} rotation={[0, rot, 0]}>
    <Box p={[0, 0.62, 0]} s={[1.6, 0.3, 0.7]} c="#0b0b0d" r={0.15} m={0.3} />
    <Box p={[0, 1.1, -0.25]} s={[1.6, 0.75, 0.2]} c="#0b0b0d" r={0.15} m={0.3} />
    <Box p={[0, 0.78, 0.22]} s={[1.45, 0.03, 0.22]} c="#f3f0e8" r={0.3} />
    {Array.from({ length: 20 }).map((_, i) => (
      <Box key={i} p={[-0.68 + i * 0.072, 0.81, 0.16]} s={[0.035, 0.03, 0.12]} c="#111" shadow={false} />
    ))}
    {[-0.7, 0.7].map((x) => (
      <Box key={x} p={[x, 0.24, 0.15]} s={[0.1, 0.48, 0.1]} c="#0b0b0d" />
    ))}
    <Box p={[0, 0.33, 0.85]} s={[0.9, 0.06, 0.35]} c="#1a1a1e" />
  </group>
);

const Stage: React.FC<{ scene: Scene }> = ({ scene }) => (
  <>
    <Floor c="#0d0c10" r={0.4} />
    <Box p={[0, 0.25, 0]} s={[14, 0.5, 8]} c="#2a1d17" r={0.35} />
    <Box p={[0, 5, -4.2]} s={[16, 10, 0.4]} c="#4a0f18" r={0.95} shadow={false} />
    {Array.from({ length: 16 }).map((_, i) => (
      <Box key={i} p={[-7.5 + i, 5, -3.95]} s={[0.4, 10, 0.2]} c="#5c1520" r={0.95} shadow={false} />
    ))}
    {scene.piano !== false && <Piano p={[0, 0.5, -0.6]} />}
    {/* empty seats */}
    {Array.from({ length: 6 }).map((_, row) =>
      Array.from({ length: 14 }).map((_, c) => (
        <Box key={`${row}-${c}`} p={[-6.5 + c, 0.45, 7 + row * 1.2]} s={[0.7, 0.9, 0.6]} c="#2a0d12" shadow={false} />
      )),
    )}
    <spotLight position={[0, 9, 4]} angle={0.32} penumbra={0.5} intensity={500} color="#ffe3b3" castShadow />
    <Glow position={[0, 9, 4]} color="#ffe3b3" size={3} />
  </>
);

const Gym: React.FC<{ t: number }> = ({ t }) => (
  <>
    <Floor c="#1c1d22" r={0.95} size={40} />
    <Box p={[0, 4, -7]} s={[24, 8, 0.4]} c="#3b3a3f" shadow={false} />
    <Box p={[0, 4, -6.75]} s={[24, 0.25, 0.05]} c="#d4a62a" e="#d4a62a" ei={0.4} shadow={false} />
    {/* boxing ring ropes */}
    {[-4, 4].map((x) =>
      [-4, 4].map((z) => <Box key={`${x}${z}`} p={[x, 0.75, z]} s={[0.18, 1.5, 0.18]} c="#c7c7c7" m={0.7} />),
    )}
    {[0.6, 1.0, 1.4].map((y) => (
      <group key={y}>
        <Box p={[0, y, -4]} s={[8, 0.05, 0.05]} c="#b8332e" shadow={false} />
        <Box p={[-4, y, 0]} s={[0.05, 0.05, 8]} c="#b8332e" shadow={false} />
        <Box p={[4, y, 0]} s={[0.05, 0.05, 8]} c="#b8332e" shadow={false} />
      </group>
    ))}
    <Box p={[0, 0.02, 0]} s={[8, 0.04, 8]} c="#24334f" r={0.8} shadow={false} />
    {/* punching bag swinging */}
    <group position={[-6, 3.4, -3]} rotation={[0, 0, Math.sin(t * 1.6) * 0.08]}>
      <Box p={[0, -0.5, 0]} s={[0.04, 1, 0.04]} c="#888" shadow={false} />
      <mesh position={[0, -1.6, 0]} castShadow>
        <cylinderGeometry args={[0.32, 0.32, 1.4, 20]} />
        <M c="#7a1f1c" r={0.5} />
      </mesh>
    </group>
    {/* weight rack */}
    <Box p={[6.5, 0.8, -4]} s={[2.6, 0.08, 0.6]} c="#555" m={0.7} />
    {[0, 1, 2, 3, 4].map((i) => (
      <mesh key={i} position={[5.5 + i * 0.5, 0.95, -4]} rotation={[0, 0, Math.PI / 2]} castShadow>
        <cylinderGeometry args={[0.12, 0.12, 0.35, 16]} />
        <M c="#222" m={0.6} r={0.4} />
      </mesh>
    ))}
    {[-3, 0, 3].map((x) => (
      <group key={x}>
        <Box p={[x, 7.6, 0]} s={[2.2, 0.1, 0.4]} c="#fff" e="#fff8e8" ei={2} shadow={false} />
        <Glow position={[x, 7.4, 0]} color="#fff3d0" size={3.5} opacity={0.5} />
      </group>
    ))}
    <spotLight position={[0, 9, 3]} angle={0.7} penumbra={0.8} intensity={280} color="#fff3d0" castShadow />
  </>
);

const City: React.FC<{ t: number }> = ({ t }) => {
  const moon = <directionalLight position={[-6, 12, 10]} intensity={1.2} color="#9fb8ff" />;
  const blds = useMemo(() => {
    const r = rand(11);
    return Array.from({ length: 34 }, (_, i) => {
      const side = i % 2 ? 1 : -1;
      return { x: side * (8 + r() * 6), z: -40 + (i >> 1) * 5, h: 6 + r() * 22, w: 3 + r() * 2.5, lit: r() };
    });
  }, []);
  return (
    <>
      {moon}
      <Floor c="#2a2c34" r={0.35} m={0.3} />
      <Box p={[0, 0.01, -10]} s={[7, 0.02, 80]} c="#22242b" r={0.4} m={0.2} shadow={false} />
      {Array.from({ length: 16 }).map((_, i) => (
        <Box key={i} p={[0, 0.03, -40 + i * 5]} s={[0.15, 0.01, 2]} c="#e8d9a0" shadow={false} />
      ))}
      {blds.map((b, i) => (
        <group key={i}>
          <Box p={[b.x, b.h / 2, b.z]} s={[b.w, b.h, 4]} c="#1e2230" r={0.6} shadow={false} />
          {Array.from({ length: Math.floor(b.h / 2.2) }).map((_, j) => (
            <Box
              key={j}
              p={[b.x - Math.sign(b.x) * (b.w / 2 + 0.01), 1.6 + j * 2.2, b.z]}
              s={[0.02, 0.7, 3]}
              c="#000"
              e={b.lit > 0.5 ? '#ffcf87' : '#6f8cff'}
              ei={(j + i) % 3 === 0 ? 0.1 : 1.2}
              shadow={false}
            />
          ))}
        </group>
      ))}
      {[-30, -18, -6, 6].map((z) => (
        <group key={z} position={[4, 0, z]}>
          <Box p={[0, 2.5, 0]} s={[0.12, 5, 0.12]} c="#333" shadow={false} />
          <Glow position={[-0.4, 5, 0]} color="#ffc98a" size={3} />
          <pointLight position={[-0.4, 4.8, 0]} intensity={60 + Math.sin(t * 2) * 2} color="#ffc98a" distance={16} />
        </group>
      ))}
    </>
  );
};

const Road: React.FC = () => {
  const trees = useMemo(() => {
    const r = rand(5);
    return Array.from({ length: 50 }, () => ({ x: (r() > 0.5 ? 1 : -1) * (4 + r() * 12), z: -60 + r() * 70, h: 2 + r() * 3 }));
  }, []);
  return (
    <>
      <Floor c="#3e5a34" size={200} />
      <Box p={[0, 0.01, -20]} s={[3.5, 0.02, 120]} c="#4a4744" r={0.9} shadow={false} />
      {trees.map((tr, i) => (
        <group key={i} position={[tr.x, 0, tr.z]}>
          <Box p={[0, 0.4, 0]} s={[0.2, 0.8, 0.2]} c="#4a3426" />
          <mesh position={[0, 0.8 + tr.h / 2, 0]} castShadow>
            <coneGeometry args={[tr.h * 0.32, tr.h, 7]} />
            <meshStandardMaterial color="#29482b" flatShading />
          </mesh>
        </group>
      ))}
      {[-40, -10, 30].map((x, i) => (
        <mesh key={x} position={[x, -6, -80 - i * 10]}>
          <sphereGeometry args={[30, 24, 16]} />
          <meshStandardMaterial color="#3b5070" flatShading />
        </mesh>
      ))}
    </>
  );
};

const Room: React.FC<{ t: number; time: TimeOfDay }> = ({ t, time }) => (
  <>
    <Floor c="#4a3a30" r={0.7} size={30} />
    <Box p={[0, 3, -4]} s={[12, 6, 0.3]} c="#2d3345" shadow={false} />
    <Box p={[-5, 3, 0]} s={[0.3, 6, 10]} c="#283042" shadow={false} />
    {/* window */}
    <Box
      p={[2.5, 3, -3.84]}
      s={[2.4, 2.2, 0.05]}
      c="#000"
      e={time === 'night' ? '#1f3a7a' : '#ffd9a6'}
      ei={time === 'night' ? 0.6 : 2}
      shadow={false}
    />
    <Box p={[2.5, 3, -3.8]} s={[0.06, 2.2, 0.06]} c="#ddd" shadow={false} />
    {/* bed */}
    <Box p={[-2, 0.15, -2]} s={[2.2, 0.3, 3.4]} c="#3a2b22" />
    <Box p={[-2, 0.36, -2]} s={[2.1, 0.14, 3.3]} c="#d8dbe3" r={0.95} />
    <Box p={[-2, 0.48, -3.3]} s={[1.6, 0.16, 0.5]} c="#f4f4f6" r={0.95} />
    <Box p={[-2, 0.45, -1.4]} s={[2.15, 0.06, 2.0]} c="#3d5a8a" r={0.95} />
    <Box p={[-2, 0.8, -3.8]} s={[2.3, 1.2, 0.15]} c="#3a2b22" />
    {/* nightstand + glowing phone */}
    <Box p={[-0.4, 0.35, -3.2]} s={[0.6, 0.7, 0.5]} c="#3a2b22" />
    <Box p={[-0.4, 0.72, -3.2]} s={[0.12, 0.01, 0.22]} c="#000" e="#8fb8ff" ei={time === 'night' ? 3 : 0.6} shadow={false} />
    {time === 'night' && <pointLight position={[-0.4, 0.95, -3.1]} intensity={4 + Math.sin(t * 7) * 0.8} color="#8fb8ff" distance={4} />}
    {/* lamp */}
    <Box p={[3.8, 0.9, -3]} s={[0.08, 1.8, 0.08]} c="#888" />
    <mesh position={[3.8, 1.9, -3]}>
      <coneGeometry args={[0.35, 0.4, 20, 1, true]} />
      <M c="#f2e3c4" e="#ffd28a" ei={0.8} />
    </mesh>
    <pointLight position={[3.8, 1.7, -3]} intensity={8} color="#ffcf8a" distance={8} />
  </>
);

const Kitchen: React.FC<{ t: number }> = ({ t }) => (
  <>
    <Floor c="#6b6258" r={0.5} size={30} />
    <Box p={[0, 3, -4]} s={[12, 6, 0.3]} c="#e4ddd0" shadow={false} />
    <Box p={[0, 0.45, -3.4]} s={[7, 0.9, 1]} c="#2e3540" />
    <Box p={[0, 0.93, -3.4]} s={[7.1, 0.06, 1.05]} c="#d9d4ca" r={0.3} />
    <Box p={[0, 2.6, -3.7]} s={[7, 1, 0.6]} c="#2e3540" />
    {/* chair */}
    <Box p={[0, 0.36, 0.55]} s={[0.55, 0.06, 0.55]} c="#6b4a30" />
    {[-0.24, 0.24].map((x) => [0.32, 0.78].map((z) => <Box key={`c${x}${z}`} p={[x, 0.18, z]} s={[0.05, 0.36, 0.05]} c="#5a3d27" />))}
    {/* table + water glass */}
    <Box p={[0, 0.75, -0.4]} s={[2, 0.08, 1.1]} c="#8a6544" r={0.6} />
    {[-0.9, 0.9].map((x) => [-0.9, 0.1].map((z) => <Box key={`${x}${z}`} p={[x, 0.37, z]} s={[0.08, 0.74, 0.08]} c="#6b4a30" />))}
    <mesh position={[0.4, 0.88, -0.4]}>
      <cylinderGeometry args={[0.06, 0.05, 0.18, 20]} />
      <meshStandardMaterial color="#cfe8ff" transparent opacity={0.45} roughness={0.05} />
    </mesh>
    {/* wall clock */}
    <group position={[-2.5, 3.6, -3.82]}>
      <mesh rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[0.45, 0.45, 0.05, 32]} />
        <M c="#f5f2ea" />
      </mesh>
      <Box p={[0, 0.12, 0.04]} s={[0.03, 0.26, 0.01]} c="#222" rot={[0, 0, -t * 0.05]} shadow={false} />
      <Box p={[0, 0.18, 0.05]} s={[0.02, 0.36, 0.01]} c="#b8332e" rot={[0, 0, -t * 0.6]} shadow={false} />
    </group>
    <Box p={[3, 3.2, -3.84]} s={[2, 1.6, 0.05]} c="#000" e="#ffd9a6" ei={2} shadow={false} />
    <directionalLight position={[4, 6, -8]} intensity={1.6} color="#ffd8a8" castShadow />
  </>
);

const Summit: React.FC = () => {
  const peaks = useMemo(() => {
    const r = rand(3);
    return Array.from({ length: 14 }, (_, i) => ({ x: (i - 7) * 9 + r() * 4, z: -30 - r() * 30, h: 10 + r() * 18 }));
  }, []);
  return (
    <>
      <mesh position={[0, -4, 0]} receiveShadow>
        <cylinderGeometry args={[6, 14, 8, 9]} />
        <meshStandardMaterial color="#4a4a52" flatShading />
      </mesh>
      {[[-2, 0.3, 1], [2.5, 0.2, -1], [1, 0.25, 2.2]].map((p, i) => (
        <mesh key={i} position={p as [number, number, number]} castShadow>
          <dodecahedronGeometry args={[0.5 + i * 0.15, 0]} />
          <meshStandardMaterial color="#5b5b63" flatShading />
        </mesh>
      ))}
      {peaks.map((p, i) => (
        <mesh key={i} position={[p.x, -6 + p.h / 2, p.z]}>
          <coneGeometry args={[p.h * 0.6, p.h, 6]} />
          <meshStandardMaterial color={i % 2 ? '#3d4660' : '#4a5470'} flatShading />
        </mesh>
      ))}
      {Array.from({ length: 12 }).map((_, i) => (
        <mesh key={`c${i}`} position={[(i - 6) * 7, -3.5, -12 - (i % 3) * 6]}>
          <sphereGeometry args={[3 + (i % 3), 16, 12]} />
          <meshStandardMaterial color="#f3d9c8" transparent opacity={0.5} />
        </mesh>
      ))}
    </>
  );
};

const Void: React.FC<{ scene: Scene; t: number }> = ({ scene, t }) => {
  const lit = scene.pillars ?? 0;
  const labels = ['#f5b942', '#f5b942', '#f5b942'];
  return (
    <>
      <Floor c="#07080c" r={0.15} m={0.8} />
      {[-3.2, 0, 3.2].map((x, i) => {
        const on = i < lit;
        const pulse = on ? 1.4 + Math.sin(t * 2 + i) * 0.3 : 0;
        return (
          <group key={x} position={[x, 0, -2.5]}>
            <mesh position={[0, 2.6, 0]} castShadow>
              <cylinderGeometry args={[0.45, 0.55, 5.2, 24]} />
              <M c={on ? '#3a2c10' : '#1a1b22'} m={0.6} r={0.3} e={labels[i]} ei={on ? pulse * 0.35 : 0} />
            </mesh>
            <Box p={[0, 0.15, 0]} s={[1.6, 0.3, 1.6]} c="#202128" m={0.5} r={0.3} />
            <Box p={[0, 5.3, 0]} s={[1.4, 0.25, 1.4]} c="#202128" m={0.5} r={0.3} />
            {on && <Glow position={[0, 5.8, 0]} color="#ffcf6b" size={4} />}
            {on && <pointLight position={[0, 3, 1.2]} intensity={25} color="#ffcf6b" distance={9} />}
          </group>
        );
      })}
      <spotLight position={[0, 12, 6]} angle={0.5} penumbra={0.9} intensity={150} color="#c9d4ff" castShadow />
    </>
  );
};


/* ---------- weather ---------- */

const Rain: React.FC<{ t: number }> = ({ t }) => {
  const count = 900;
  const base = useMemo(() => {
    const r = rand(77);
    return Array.from({ length: count }, () => [(r() - 0.5) * 24, r() * 10, (r() - 0.5) * 24 + 2, 0.8 + r() * 0.4]);
  }, []);
  const geo = useMemo(() => new THREE.BufferGeometry(), []);
  const arr = new Float32Array(count * 6);
  base.forEach(([x, y0, z, sp], i) => {
    const y = (((y0 - t * 11 * sp) % 10) + 10) % 10;
    arr[i * 6] = x;
    arr[i * 6 + 1] = y;
    arr[i * 6 + 2] = z;
    arr[i * 6 + 3] = x + 0.06;
    arr[i * 6 + 4] = y + 0.42;
    arr[i * 6 + 5] = z;
  });
  geo.setAttribute('position', new THREE.BufferAttribute(arr, 3));
  return (
    <lineSegments geometry={geo}>
      <lineBasicMaterial color="#cfdcf0" transparent opacity={0.45} depthWrite={false} />
    </lineSegments>
  );
};

const Snow: React.FC<{ t: number }> = ({ t }) => {
  const count = 700;
  const base = useMemo(() => {
    const r = rand(91);
    return Array.from({ length: count }, () => [(r() - 0.5) * 22, r() * 9, (r() - 0.5) * 22 + 2, r() * 6.28, 0.5 + r() * 0.5]);
  }, []);
  const geo = useMemo(() => new THREE.BufferGeometry(), []);
  const arr = new Float32Array(count * 3);
  base.forEach(([x, y0, z, ph, sp], i) => {
    arr[i * 3] = x + Math.sin(t * 0.8 + ph) * 0.35;
    arr[i * 3 + 1] = (((y0 - t * 0.7 * sp) % 9) + 9) % 9;
    arr[i * 3 + 2] = z + Math.cos(t * 0.6 + ph) * 0.3;
  });
  geo.setAttribute('position', new THREE.BufferAttribute(arr, 3));
  return (
    <points geometry={geo}>
      <pointsMaterial color="#ffffff" size={0.07} transparent opacity={0.9} depthWrite={false} />
    </points>
  );
};

/* ---------- shore (harbour town by the sea) ---------- */

const Water: React.FC<{ t: number; time: TimeOfDay }> = ({ t, time }) => {
  const geo = useMemo(() => new THREE.PlaneGeometry(220, 120, 90, 50), []);
  const pos = geo.attributes.position as THREE.BufferAttribute;
  const storm = time === 'storm' ? 2.2 : 1;
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i);
    const y = pos.getY(i);
    pos.setZ(i, (Math.sin(x * 0.18 + t * 1.1) * 0.18 + Math.sin(y * 0.33 - t * 1.6) * 0.12) * storm);
  }
  pos.needsUpdate = true;
  geo.computeVertexNormals();
  const col = time === 'night' ? '#0d1a33' : time === 'storm' ? '#2c3a46' : time === 'dusk' ? '#3a3050' : '#1f4d6e';
  return (
    <mesh geometry={geo} rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.35, -66]} receiveShadow>
      <meshStandardMaterial color={col} roughness={0.15} metalness={0.55} flatShading />
    </mesh>
  );
};

const Shore: React.FC<{ t: number; time: TimeOfDay }> = ({ t, time }) => {
  const posts = useMemo(() => Array.from({ length: 9 }, (_, i) => -6 - i * 2.2), []);
  const houses = useMemo(() => {
    const r = rand(23);
    const cols = ['#c9b8a0', '#9fb2c2', '#d8c7a8', '#b98a6e', '#e0d6c4', '#8fa6a0'];
    return Array.from({ length: 12 }, (_, i) => ({ x: (i < 6 ? -42 + i * 4.6 : 17 + (i - 6) * 4.6) + r() * 1.2, h: 2.2 + r() * 2.4, c: cols[i % cols.length], z: 2 + r() * 5 }));
  }, []);
  const night = time === 'night' || time === 'storm';
  return (
    <>
      {/* sand */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, 0, 4]} receiveShadow>
        <planeGeometry args={[220, 14]} />
        <meshStandardMaterial color={time === 'night' ? '#5d564c' : '#c8b48e'} roughness={1} />
      </mesh>
      <mesh rotation={[-0.06, 0, 0]} position={[0, -0.18, -4.5]} receiveShadow>
        <boxGeometry args={[220, 0.2, 4]} />
        <meshStandardMaterial color="#9c8a6c" roughness={1} />
      </mesh>
      <Water t={t} time={time} />
      {/* wooden pier */}
      <Box p={[5, 0.35, -14]} s={[2.2, 0.12, 20]} c="#6b5038" />
      {posts.map((z) => (
        <React.Fragment key={z}>
          <Box p={[4, -0.2, z]} s={[0.18, 1.3, 0.18]} c="#4a3626" />
          <Box p={[6, -0.2, z]} s={[0.18, 1.3, 0.18]} c="#4a3626" />
        </React.Fragment>
      ))}
      {/* small fishing boat rocking */}
      <group position={[-6, -0.1 + Math.sin(t * 1.3) * 0.08, -10]} rotation={[Math.sin(t * 1.1) * 0.05, 0.4, Math.sin(t * 0.9) * 0.06]}>
        <Box p={[0, 0.3, 0]} s={[1.6, 0.6, 4]} c="#e8e2d4" />
        <Box p={[0, 0.62, 0]} s={[1.65, 0.08, 4.05]} c="#2f5d8a" />
        <Box p={[0, 1.0, -0.6]} s={[1, 0.8, 1.2]} c="#d24a3a" />
        <Box p={[0, 2.0, 0.6]} s={[0.08, 2.4, 0.08]} c="#555" />
      </group>
      {/* harbour houses behind */}
      {houses.map((h, i) => (
        <group key={i} position={[h.x, 0, h.z]}>
          <Box p={[0, h.h / 2, 0]} s={[3, h.h, 2.6]} c={h.c} />
          <mesh position={[0, h.h + 0.6, 0]} rotation={[0, Math.PI / 4, 0]} castShadow>
            <coneGeometry args={[2.3, 1.2, 4]} />
            <meshStandardMaterial color="#7a3b2e" flatShading />
          </mesh>
          <Box p={[0.6, h.h * 0.55, -1.31]} s={[0.6, 0.6, 0.03]} c="#000" e={night ? '#ffcf8a' : '#9ab'} ei={night ? 2.2 : 0.3} shadow={false} />
        </group>
      ))}
      {/* street lamps */}
      {[-11, 11].map((x) => (
        <group key={x} position={[x, 0, 5]}>
          <Box p={[0, 1.6, 0]} s={[0.1, 3.2, 0.1]} c="#2b2b2b" />
          <Box p={[0, 3.25, 0]} s={[0.35, 0.25, 0.35]} c="#222" e="#ffd28a" ei={night ? 3 : 0.2} shadow={false} />
          {night && <pointLight position={[0, 3, 0]} intensity={10} color="#ffcf8a" distance={9} />}
        </group>
      ))}
    </>
  );
};

/* ---------- main environment ---------- */

const DEFAULT_TIME: Record<EnvName, TimeOfDay> = {
  stadium: 'night',
  court: 'night',
  studio: 'day',
  stage: 'night',
  gym: 'night',
  city: 'night',
  road: 'dawn',
  room: 'night',
  kitchen: 'dawn',
  summit: 'dawn',
  shore: 'dawn',
  void: 'night',
};

export const sceneTime = (scene: Scene): TimeOfDay => scene.time ?? DEFAULT_TIME[scene.env];

export const Environment: React.FC<{ scene: Scene; t: number }> = ({ scene, t }) => {
  const time = sceneTime(scene);
  const p = PRESETS[time];
  const indoor = ['studio', 'stage', 'gym', 'room', 'kitchen', 'court', 'void'].includes(scene.env);
  const fogNear = indoor ? 12 : 18;
  const fogFar = indoor ? 45 : 110;
  const sunVisible = !indoor && (time === 'dawn' || time === 'dusk');
  return (
    <>
      <color attach="background" args={[p.fog]} />
      <fog attach="fog" args={[scene.env === 'void' ? '#05060a' : p.fog, fogNear, fogFar]} />
      {scene.env !== 'void' && <Sky p={p} />}
      <ambientLight intensity={p.amb * 2.2} color={p.ambC} />
      <hemisphereLight args={[p.horizon, '#2a2018', 1.4]} />
      {/* soft front fill so faces never fall into black */}
      <directionalLight position={[2, 5, 12]} intensity={time === 'night' ? 0.9 : 1.3} color="#fff1e0" />
      <directionalLight
        position={p.sun}
        intensity={p.keyI}
        color={p.key}
        castShadow
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
        shadow-camera-left={-14}
        shadow-camera-right={14}
        shadow-camera-top={14}
        shadow-camera-bottom={-14}
        shadow-camera-far={80}
        shadow-bias={-0.0004}
      />
      {/* rim light for cinematic edges */}
      <directionalLight position={[-6, 5, -8]} intensity={1.1} color={scene.color ?? '#9fc4ff'} />
      {sunVisible && (
        <>
          <mesh position={[p.sun[0] * 3, p.sun[1] * 3 + Math.min(4, t * 0.25), p.sun[2] * 3]}>
            <sphereGeometry args={[5, 32, 16]} />
            <meshBasicMaterial color="#ffd38a" fog={false} />
          </mesh>
          <Glow position={[p.sun[0] * 2.9, p.sun[1] * 3 + Math.min(4, t * 0.25), p.sun[2] * 2.9]} color="#ffb36b" size={60} opacity={0.7} />
        </>
      )}
      {scene.env === 'stadium' && <Stadium t={t} />}
      {scene.env === 'court' && <Court scene={scene} t={t} />}
      {scene.env === 'studio' && <Studio scene={scene} t={t} />}
      {scene.env === 'stage' && <Stage scene={scene} />}
      {scene.env === 'gym' && <Gym t={t} />}
      {scene.env === 'city' && <City t={t} />}
      {scene.env === 'road' && <Road />}
      {scene.env === 'room' && <Room t={t} time={time} />}
      {scene.env === 'kitchen' && <Kitchen t={t} />}
      {scene.env === 'summit' && <Summit />}
      {scene.env === 'shore' && <Shore t={t} time={time} />}
      {scene.weather === 'rain' && <Rain t={t} />}
      {scene.weather === 'snow' && <Snow t={t} />}
      {scene.env === 'void' && <Void scene={scene} t={t} />}
      <Dust t={t} color={time === 'night' ? '#9fb8ff' : '#ffe2b0'} seed={scene.env.length * 13} />
    </>
  );
};
