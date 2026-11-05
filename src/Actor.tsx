import React, { useMemo } from 'react';
import * as THREE from 'three';
import { buildCharacter, Library } from './models';
import { CastMember, CharacterSpec } from './types';

type Step = { clip: string; loop?: boolean; dur?: number };

// action name -> sequence of KayKit clips (last step loops unless loop:false)
export const ACTIONS: Record<string, Step[]> = {
  idle: [{ clip: 'Idle_A' }],
  idle2: [{ clip: 'Idle_B' }],
  walk: [{ clip: 'Walking_A' }],
  walkslow: [{ clip: 'Walking_C' }],
  walktired: [{ clip: 'Walking_B' }],
  run: [{ clip: 'Running_A' }],
  sprint: [{ clip: 'Running_B' }],
  jump: [{ clip: 'Jump_Full_Long' }],
  cheer: [{ clip: 'Cheering' }],
  wave: [{ clip: 'Waving' }],
  pushups: [{ clip: 'Push_Ups' }],
  situps: [{ clip: 'Sit_Ups' }],
  sit: [{ clip: 'Sit_Chair_Down', loop: false }, { clip: 'Sit_Chair_Idle' }],
  seated: [{ clip: 'Sit_Chair_Idle' }],
  sitfloor: [{ clip: 'Sit_Floor_Down', loop: false }, { clip: 'Sit_Floor_Idle' }],
  meditate: [{ clip: 'Sit_Floor_Idle' }],
  rise: [{ clip: 'Sit_Floor_StandUp', loop: false }, { clip: 'Idle_A' }],
  lie: [{ clip: 'Lie_Idle' }],
  wakeup: [{ clip: 'Lie_Idle', loop: false, dur: 1.5 }, { clip: 'Lie_StandUp', loop: false }, { clip: 'Idle_A' }],
  liedown: [{ clip: 'Lie_Down', loop: false }, { clip: 'Lie_Idle' }],
  guard: [{ clip: 'Melee_Unarmed_Idle' }],
  punch: [{ clip: 'Melee_Unarmed_Attack_Punch_A' }],
  kick: [{ clip: 'Melee_Unarmed_Attack_Kick' }],
  block: [{ clip: 'Melee_Blocking' }],
  hit: [{ clip: 'Hit_A', loop: false }, { clip: 'Idle_B' }],
  crouch: [{ clip: 'Crouching' }],
  sneak: [{ clip: 'Sneaking' }],
  backoff: [{ clip: 'Walking_Backwards' }],
  dodge: [{ clip: 'Dodge_Backward', loop: false }, { clip: 'Idle_A' }],
  paint: [{ clip: 'Working_A' }],
  work: [{ clip: 'Working_B' }],
  cook: [{ clip: 'Working_C' }],
  hammer: [{ clip: 'Hammering' }],
  interact: [{ clip: 'Interact' }],
  pickup: [{ clip: 'PickUp', loop: false }, { clip: 'Holding_A' }],
  hold: [{ clip: 'Holding_A' }],
  shoot: [{ clip: 'Throw', loop: false }, { clip: 'Idle_A' }],
  shootloop: [{ clip: 'Throw' }],
  use: [{ clip: 'Use_Item' }],
  collapse: [{ clip: 'Death_B', loop: false }, { clip: 'Death_B_Pose' }],
  down: [{ clip: 'Death_B_Pose' }],
  getup: [{ clip: 'Lie_StandUp', loop: false }, { clip: 'Idle_A' }],
};

const FADE = 0.3;

type Props = {
  lib: Library;
  spec: CharacterSpec;
  member: CastMember;
  t: number; // seconds since scene start
  sceneDur: number;
};

const getClip = (lib: Library, name: string) => lib.clips.get(name) ?? lib.clips.get('Idle_A')!;

export const actorPosition = (m: CastMember, t: number, sceneDur: number): [number, number, number] => {
  const p = m.pos ?? [0, 0];
  if (!m.to) return [p[0], m.y ?? 0, p[1]];
  const d = m.delay ?? 0;
  const k = THREE.MathUtils.clamp((t - d) / Math.max(0.5, sceneDur - d), 0, 1);
  return [p[0] + (m.to[0] - p[0]) * k, m.y ?? 0, p[1] + (m.to[1] - p[1]) * k];
};

export const Actor: React.FC<Props> = ({ lib, spec, member, t, sceneDur }) => {
  const built = useMemo(
    () => buildCharacter(lib, spec, { gloves: member.gloves, ball: member.ball }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [lib, JSON.stringify(spec), member.gloves, member.ball],
  );
  const mixer = useMemo(() => new THREE.AnimationMixer(built.root), [built]);
  const actions = useMemo(() => new Map<string, THREE.AnimationAction>(), [mixer]);

  const getAction = (name: string) => {
    let a = actions.get(name);
    if (!a) {
      a = mixer.clipAction(getClip(lib, name));
      a.play();
      actions.set(name, a);
    }
    return a;
  };

  // Deterministic pose for this exact time (safe for parallel rendering)
  const steps = ACTIONS[member.action] ?? ACTIONS.idle;
  const speed = member.speed ?? 1;
  const local = Math.max(0, t - (member.delay ?? 0)) * speed;
  const delayed = member.delay && t < member.delay;

  let start = 0;
  let idx = 0;
  const lens = steps.map((s) => (s.loop === false ? s.dur ?? getClip(lib, s.clip).duration : Infinity));
  if (!delayed) {
    while (idx < steps.length - 1 && local >= start + lens[idx]) {
      start += lens[idx];
      idx++;
    }
  }
  const cur = delayed ? { clip: 'Idle_A' } : steps[idx];
  const curClip = getClip(lib, cur.clip);
  const into = delayed ? t : local - start;
  const curTime = cur.loop === false && idx < steps.length - 1
    ? Math.min(into, curClip.duration - 0.001)
    : steps.length > 1 && idx === steps.length - 1 && steps[idx].loop === false
      ? Math.min(into, curClip.duration - 0.001)
      : into % curClip.duration;

  actions.forEach((a) => a.setEffectiveWeight(0));
  const main = getAction(cur.clip);
  main.time = curTime;
  if (!delayed && idx > 0 && into < FADE) {
    const prev = steps[idx - 1];
    const pc = getClip(lib, prev.clip);
    const pa = getAction(prev.clip);
    pa.time = Math.min(pc.duration - 0.001, lens[idx - 1]);
    const w = into / FADE;
    pa.setEffectiveWeight(1 - w);
    main.setEffectiveWeight(w);
  } else {
    main.setEffectiveWeight(1);
  }
  mixer.update(0);

  const [x, y, z] = actorPosition(member, t, sceneDur);
  let face = ((member.face ?? 0) * Math.PI) / 180;
  if (member.to && member.face === undefined) {
    const p = member.pos ?? [0, 0];
    face = Math.atan2(member.to[0] - p[0], member.to[1] - p[1]);
  }

  return (
    <group position={[x, y, z]} rotation={[0, face, 0]} scale={built.scale}>
      <primitive object={built.root} position={[0, built.lift, 0]} />
    </group>
  );
};
