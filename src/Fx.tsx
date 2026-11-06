import React, { useMemo } from 'react';
import * as THREE from 'three';
import { FxName } from './types';

// Visual effects layer (all deterministic in t, safe for parallel chunk rendering)

const rand = (seed: number) => {
  let s = seed % 2147483647;
  if (s <= 0) s += 2147483646;
  return () => (s = (s * 16807) % 2147483647) / 2147483647;
};

let dotTex: THREE.CanvasTexture | null = null;
const getDot = () => {
  if (dotTex) return dotTex;
  const c = document.createElement('canvas');
  c.width = c.height = 64;
  const g = c.getContext('2d')!;
  const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(255,255,255,1)');
  gr.addColorStop(0.3, 'rgba(255,255,255,0.6)');
  gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr;
  g.fillRect(0, 0, 64, 64);
  dotTex = new THREE.CanvasTexture(c);
  return dotTex;
};

const Points: React.FC<{ pos: Float32Array; col?: Float32Array; color?: string; size: number; opacity?: number }> = ({ pos, col, color, size, opacity = 0.9 }) => {
  const geo = useMemo(() => new THREE.BufferGeometry(), []);
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  if (col) geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
  return (
    <points geometry={geo}>
      <pointsMaterial
        map={getDot()}
        color={col ? '#ffffff' : color}
        vertexColors={!!col}
        size={size}
        sizeAttenuation
        transparent
        opacity={opacity}
        blending={THREE.AdditiveBlending}
        depthWrite={false}
      />
    </points>
  );
};

type P = { t: number; c: [number, number, number]; color?: string };

const Sparks: React.FC<P> = ({ t, c, color = '#ffb347' }) => {
  const n = 260;
  const base = useMemo(() => {
    const r = rand(91);
    return Array.from({ length: n }, () => [(r() - 0.5) * 7, r() * 5, (r() - 0.5) * 7, 0.5 + r() * 1.2, r() * 6.28]);
  }, []);
  const pos = new Float32Array(n * 3);
  base.forEach(([x, y, z, sp, ph], i) => {
    const h = (y + t * sp) % 5;
    pos[i * 3] = c[0] + x + Math.sin(t * 2 + ph) * 0.3 * h * 0.3;
    pos[i * 3 + 1] = h;
    pos[i * 3 + 2] = c[2] + z + Math.cos(t * 1.7 + ph) * 0.3;
  });
  return <Points pos={pos} color={color} size={0.12} />;
};

const Fireflies: React.FC<P> = ({ t, c }) => {
  const n = 120;
  const base = useMemo(() => {
    const r = rand(17);
    return Array.from({ length: n }, () => [(r() - 0.5) * 16, 0.3 + r() * 3, (r() - 0.5) * 14, r() * 6.28, 0.3 + r() * 0.6]);
  }, []);
  const pos = new Float32Array(n * 3);
  base.forEach(([x, y, z, ph, sp], i) => {
    pos[i * 3] = c[0] + x + Math.sin(t * sp + ph) * 0.8;
    pos[i * 3 + 1] = y + Math.sin(t * sp * 1.3 + ph * 2) * 0.4;
    pos[i * 3 + 2] = c[2] + z + Math.cos(t * sp * 0.8 + ph) * 0.8;
  });
  return <Points pos={pos} color="#d8ff7a" size={0.22} opacity={0.75 + Math.sin(t * 3) * 0.15} />;
};

const Petals: React.FC<P> = ({ t, c }) => {
  const n = 220;
  const base = useMemo(() => {
    const r = rand(33);
    return Array.from({ length: n }, () => [(r() - 0.5) * 14, r() * 7, (r() - 0.5) * 12, 0.25 + r() * 0.35, r() * 6.28]);
  }, []);
  const pos = new Float32Array(n * 3);
  base.forEach(([x, y, z, sp, ph], i) => {
    const h = 7 - ((7 - y + t * sp) % 7);
    pos[i * 3] = c[0] + x + Math.sin(t * 0.9 + ph) * 0.9 + t * 0.25;
    pos[i * 3 + 1] = h;
    pos[i * 3 + 2] = c[2] + z + Math.cos(t * 0.7 + ph) * 0.5;
  });
  return <Points pos={pos} color="#ff9ec7" size={0.13} opacity={0.85} />;
};

const PALETTE = ['#ffd45e', '#ff5a5a', '#5ab4ff', '#7dff9a', '#ff8af0', '#ffffff'].map((h) => new THREE.Color(h));

const Confetti: React.FC<P> = ({ t, c }) => {
  const n = 400;
  const base = useMemo(() => {
    const r = rand(55);
    return Array.from({ length: n }, () => [(r() - 0.5) * 10, r() * 8, (r() - 0.5) * 8, 0.6 + r() * 0.8, r() * 6.28, Math.floor(r() * PALETTE.length)]);
  }, []);
  const pos = new Float32Array(n * 3);
  const col = new Float32Array(n * 3);
  base.forEach(([x, y, z, sp, ph, ci], i) => {
    const h = 8 - ((8 - y + t * sp) % 8);
    pos[i * 3] = c[0] + x + Math.sin(t * 3 + ph) * 0.25;
    pos[i * 3 + 1] = h;
    pos[i * 3 + 2] = c[2] + z + Math.cos(t * 2.5 + ph) * 0.25;
    const p = PALETTE[ci];
    const tw = 0.6 + 0.4 * Math.abs(Math.sin(t * 6 + ph));
    col[i * 3] = p.r * tw;
    col[i * 3 + 1] = p.g * tw;
    col[i * 3 + 2] = p.b * tw;
  });
  return <Points pos={pos} col={col} size={0.12} />;
};

const Fireworks: React.FC<P> = ({ t, c }) => {
  const per = 140;
  const bursts = 4;
  const dirs = useMemo(() => {
    const r = rand(71);
    return Array.from({ length: per }, () => {
      const u = r() * 2 - 1;
      const a = r() * 6.28;
      const s = Math.sqrt(1 - u * u);
      return [s * Math.cos(a), u, s * Math.sin(a), 0.7 + r() * 0.3];
    });
  }, []);
  const pos = new Float32Array(per * bursts * 3);
  const col = new Float32Array(per * bursts * 3);
  for (let b = 0; b < bursts; b++) {
    const cycle = 2.6;
    const off = b * 0.65;
    const k = Math.floor((t + off) / cycle);
    const lt = ((t + off) % cycle) / cycle;
    const r = rand(1000 + k * 7 + b);
    const cx = c[0] + (r() - 0.5) * 18;
    const cy = 9 + r() * 6;
    const cz = c[2] - 14 - r() * 10;
    const pc = PALETTE[Math.floor(r() * 5)];
    const radius = 4.5 * (1 - Math.pow(1 - lt, 3));
    const fade = lt < 0.08 ? lt / 0.08 : Math.max(0, 1 - (lt - 0.08) / 0.92);
    dirs.forEach(([dx, dy, dz, sp], i) => {
      const j = (b * per + i) * 3;
      pos[j] = cx + dx * radius * sp;
      pos[j + 1] = cy + dy * radius * sp - lt * lt * 3;
      pos[j + 2] = cz + dz * radius * sp;
      col[j] = pc.r * fade;
      col[j + 1] = pc.g * fade;
      col[j + 2] = pc.b * fade;
    });
  }
  return <Points pos={pos} col={col} size={0.45} />;
};

export const Stars: React.FC<{ t: number; count?: number }> = ({ t, count = 1600 }) => {
  const pos = useMemo(() => {
    const r = rand(5);
    const a = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const u = r() * 2 - 1;
      const th = r() * 6.28;
      const s = Math.sqrt(1 - u * u);
      const R = 60 + r() * 60;
      a[i * 3] = s * Math.cos(th) * R;
      a[i * 3 + 1] = Math.abs(u) * R * 0.9 - 5;
      a[i * 3 + 2] = s * Math.sin(th) * R;
    }
    return a;
  }, [count]);
  return (
    <group rotation={[0, t * 0.01, 0]}>
      <Points pos={pos} color="#dfe8ff" size={0.7} opacity={0.9} />
    </group>
  );
};

const GodRays: React.FC<P> = ({ t, c, color = '#ffe2a8' }) => (
  <group position={[c[0] - 2, 0, c[2] - 3]}>
    {[-3, -1.2, 0.6, 2.4, 4.2].map((x, i) => (
      <mesh key={i} position={[x, 6, -1 - i * 0.6]} rotation={[0, 0, 0.35]}>
        <coneGeometry args={[1.1 + (i % 2) * 0.5, 16, 24, 1, true]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.07 + 0.03 * Math.sin(t * 0.8 + i)}
          blending={THREE.AdditiveBlending}
          depthWrite={false}
          side={THREE.DoubleSide}
          fog={false}
        />
      </mesh>
    ))}
  </group>
);

const Aura: React.FC<P> = ({ t, c, color = '#f5c451' }) => (
  <group position={[c[0], 0.05, c[2]]}>
    {[0, 1, 2].map((i) => (
      <mesh key={i} rotation={[-Math.PI / 2 + Math.sin(t + i) * 0.15, 0, t * (0.8 + i * 0.5)]} position={[0, 0.2 + i * 0.75 + Math.sin(t * 1.5 + i) * 0.1, 0]}>
        <torusGeometry args={[0.85 + i * 0.12, 0.025, 8, 64]} />
        <meshBasicMaterial color={color} transparent opacity={0.85 - i * 0.2} blending={THREE.AdditiveBlending} depthWrite={false} />
      </mesh>
    ))}
    <sprite position={[0, 1.1, -0.3]} scale={[4.5, 5, 1]}>
      <spriteMaterial map={getDot()} color={color} transparent opacity={0.45 + 0.1 * Math.sin(t * 2)} blending={THREE.AdditiveBlending} depthWrite={false} />
    </sprite>
    <pointLight position={[0, 1.2, 1]} intensity={14} color={color} distance={6} />
  </group>
);

const Speed: React.FC<P> = ({ t, c }) => {
  const n = 160;
  const base = useMemo(() => {
    const r = rand(23);
    return Array.from({ length: n }, () => {
      const a = r() * 6.28;
      const R = 1.6 + r() * 4;
      return [Math.cos(a) * R, 1 + Math.sin(a) * R * 0.7, r() * 30, 14 + r() * 10];
    });
  }, []);
  const geo = useMemo(() => new THREE.BufferGeometry(), []);
  const arr = new Float32Array(n * 6);
  base.forEach(([x, y, z0, sp], i) => {
    const z = c[2] - 25 + ((z0 + t * sp) % 30);
    arr.set([c[0] + x, Math.max(0.1, y), z, c[0] + x, Math.max(0.1, y), z + 1.6], i * 6);
  });
  geo.setAttribute('position', new THREE.BufferAttribute(arr, 3));
  return (
    <lineSegments geometry={geo}>
      <lineBasicMaterial color="#ffffff" transparent opacity={0.45} blending={THREE.AdditiveBlending} depthWrite={false} />
    </lineSegments>
  );
};

const Shockwave: React.FC<P> = ({ t, c, color = '#ffd45e' }) => {
  const k = (t % 1.6) / 1.6;
  return (
    <mesh position={[c[0], 0.06, c[2]]} rotation={[-Math.PI / 2, 0, 0]}>
      <ringGeometry args={[k * 6, k * 6 + 0.25, 64]} />
      <meshBasicMaterial color={color} transparent opacity={(1 - k) * 0.8} blending={THREE.AdditiveBlending} depthWrite={false} />
    </mesh>
  );
};

export const FxLayer: React.FC<{ fx?: FxName[]; t: number; center: [number, number, number]; color?: string }> = ({ fx, t, center, color }) => {
  if (!fx || !fx.length) return null;
  return (
    <>
      {fx.includes('sparks') && <Sparks t={t} c={center} />}
      {fx.includes('embers') && <Sparks t={t} c={center} color="#ff6a2a" />}
      {fx.includes('fireflies') && <Fireflies t={t} c={center} />}
      {fx.includes('petals') && <Petals t={t} c={center} />}
      {fx.includes('confetti') && <Confetti t={t} c={center} />}
      {fx.includes('fireworks') && <Fireworks t={t} c={center} />}
      {fx.includes('stars') && <Stars t={t} />}
      {fx.includes('godrays') && <GodRays t={t} c={center} />}
      {fx.includes('aura') && <Aura t={t} c={center} color={color} />}
      {fx.includes('speed') && <Speed t={t} c={center} />}
      {fx.includes('shockwave') && <Shockwave t={t} c={center} color={color} />}
    </>
  );
};
