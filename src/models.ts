import { useEffect, useState } from 'react';
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { clone as cloneSkinned } from 'three/examples/jsm/utils/SkeletonUtils.js';
import { cancelRender, continueRender, delayRender, staticFile } from 'remotion';
import { CharacterSpec } from './types';

// KayKit Character Animations (CC0, Kay Lousberg) – downloaded by the GitHub Action into public/models
const ANIM_FILES = [
  'Rig_Medium_General',
  'Rig_Medium_MovementBasic',
  'Rig_Medium_MovementAdvanced',
  'Rig_Medium_Simulation',
  'Rig_Medium_CombatMelee',
  'Rig_Medium_Tools',
];

export type Library = {
  base: THREE.Object3D;
  clips: Map<string, THREE.AnimationClip>;
  height: number;
  minY: number;
};

let promise: Promise<Library> | null = null;

export const loadLibrary = (): Promise<Library> => {
  if (!promise) {
    const loader = new GLTFLoader();
    const load = (f: string) => loader.loadAsync(staticFile(`models/${f}.glb`));
    promise = Promise.all([load('Mannequin_Medium'), ...ANIM_FILES.map(load)]).then(([man, ...anims]) => {
      const clips = new Map<string, THREE.AnimationClip>();
      anims.forEach((g) => g.animations.forEach((c) => clips.set(c.name, c)));
      man.scene.updateMatrixWorld(true);
      const box = new THREE.Box3().setFromObject(man.scene);
      let height = box.max.y - box.min.y;
      let minY = box.min.y;
      if (!(height > 0.2 && height < 50)) {
        height = 1.8;
        minY = 0;
      }
      return { base: man.scene, clips, height, minY };
    });
  }
  return promise;
};

export const useLibrary = (): Library | null => {
  const [lib, setLib] = useState<Library | null>(null);
  const [handle] = useState(() => delayRender('Loading 3D characters', { timeoutInMilliseconds: 180000 }));
  useEffect(() => {
    loadLibrary()
      .then((l) => {
        setLib(l);
        continueRender(handle);
      })
      .catch((e) => cancelRender(e));
  }, [handle]);
  return lib;
};

const std = (color: string, roughness = 0.75) =>
  new THREE.MeshStandardMaterial({ color: new THREE.Color(color), roughness, metalness: 0.02 });

const findBone = (root: THREE.Object3D, names: string[]) => {
  for (const n of names) {
    const o = root.getObjectByName(n);
    if (o) return o;
  }
  return undefined;
};

let ballTexture: THREE.CanvasTexture | null = null;
export const getBallTexture = () => {
  if (ballTexture) return ballTexture;
  const c = document.createElement('canvas');
  c.width = 256;
  c.height = 128;
  const g = c.getContext('2d')!;
  g.fillStyle = '#d4651f';
  g.fillRect(0, 0, 256, 128);
  g.strokeStyle = '#1a0f08';
  g.lineWidth = 4;
  g.beginPath();
  g.moveTo(0, 64);
  g.lineTo(256, 64);
  g.moveTo(64, 0);
  g.lineTo(64, 128);
  g.moveTo(192, 0);
  g.lineTo(192, 128);
  g.stroke();
  ballTexture = new THREE.CanvasTexture(c);
  ballTexture.colorSpace = THREE.SRGBColorSpace;
  return ballTexture;
};

export type BuiltCharacter = { root: THREE.Object3D; scale: number; lift: number };

export const buildCharacter = (
  lib: Library,
  spec: CharacterSpec,
  extras: { gloves?: string; ball?: boolean } = {},
): BuiltCharacter => {
  const root = cloneSkinned(lib.base) as THREE.Object3D;
  const skin = std(spec.skin, 0.55);
  const shirt = std(spec.shirt, 0.8);
  const pants = std(spec.pants, 0.85);
  let headMesh: THREE.Mesh | undefined;

  root.traverse((o) => {
    const m = o as THREE.Mesh;
    if (!m.isMesh) return;
    m.castShadow = true;
    m.receiveShadow = true;
    m.frustumCulled = false;
    const n = `${m.name} ${m.parent?.name ?? ''}`.toLowerCase();
    if (n.includes('head')) {
      m.material = skin;
      headMesh = headMesh ?? m;
    } else if (n.includes('leg')) m.material = pants;
    else if (n.includes('arm')) m.material = spec.sleeves ? shirt : skin;
    else m.material = shirt;
  });

  root.updateMatrixWorld(true);

  // Head box (world space, bind pose) for hair and prop sizes
  const headBox = new THREE.Box3();
  if (headMesh) {
    try {
      const sk = headMesh as THREE.SkinnedMesh;
      if (sk.isSkinnedMesh) {
        sk.skeleton.update();
        sk.computeBoundingBox();
        headBox.copy(sk.boundingBox!).applyMatrix4(sk.matrixWorld);
      } else {
        headMesh.geometry.computeBoundingBox();
        headBox.copy(headMesh.geometry.boundingBox!).applyMatrix4(headMesh.matrixWorld);
      }
    } catch {
      headBox.setFromObject(headMesh);
    }
  }
  const hs = new THREE.Vector3();
  const hc = new THREE.Vector3();
  headBox.getSize(hs);
  headBox.getCenter(hc);
  const headOk = hs.x > 0 && hs.y > 0;
  const headBone = findBone(root, ['head', 'Head']);

  // Hair
  const style = spec.hair ?? 'short';
  if (headOk && style !== 'bald') {
    const hairMat = std(spec.hairColor ?? '#15110e', 0.9);
    const hair = new THREE.Group();
    const r = Math.max(hs.x, hs.z) * 0.56;
    const cap = new THREE.Mesh(new THREE.SphereGeometry(r, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.5), hairMat);
    cap.position.set(hc.x, hc.y + hs.y * 0.06, hc.z);
    cap.scale.set(1, style === 'beanie' ? 1.25 : 0.85, 1);
    cap.castShadow = true;
    if (style === 'afro') {
      const afro = new THREE.Mesh(new THREE.IcosahedronGeometry(r * 1.32, 3), hairMat);
      afro.position.set(hc.x, hc.y + hs.y * 0.22, hc.z);
      afro.castShadow = true;
      hair.add(afro);
    } else {
      hair.add(cap);
    }
    if (style === 'bun') {
      const bun = new THREE.Mesh(new THREE.SphereGeometry(r * 0.42, 20, 14), hairMat);
      bun.position.set(hc.x, hc.y + hs.y * 0.5, hc.z);
      hair.add(bun);
    }
    if (style === 'beanie') {
      const rim = new THREE.Mesh(new THREE.TorusGeometry(r * 0.98, r * 0.12, 10, 32), hairMat);
      rim.rotation.x = Math.PI / 2;
      rim.position.set(hc.x, hc.y + hs.y * 0.08, hc.z);
      hair.add(rim);
    }
    if (style === 'cap') {
      const brim = new THREE.Mesh(new THREE.CylinderGeometry(r * 1.35, r * 1.35, r * 0.06, 32), hairMat);
      brim.position.set(hc.x, hc.y + hs.y * 0.08, hc.z);
      hair.add(brim);
    }
    root.add(hair);
    if (headBone) headBone.attach(hair);
  }

  const attachToHand = (names: string[], mesh: THREE.Mesh) => {
    const bone = findBone(root, names);
    if (!bone) return;
    const p = new THREE.Vector3();
    bone.getWorldPosition(p);
    mesh.position.copy(p);
    mesh.castShadow = true;
    root.add(mesh);
    bone.attach(mesh);
  };

  const unit = headOk ? hs.x : lib.height * 0.12;
  if (extras.gloves) {
    const gm = std(extras.gloves, 0.35);
    attachToHand(['handl', 'hand.l', 'hand_l', 'wristl'], new THREE.Mesh(new THREE.SphereGeometry(unit * 0.36, 20, 16), gm));
    attachToHand(['handr', 'hand.r', 'hand_r', 'wristr'], new THREE.Mesh(new THREE.SphereGeometry(unit * 0.36, 20, 16), gm));
  }
  if (extras.ball) {
    const bm = new THREE.MeshStandardMaterial({ map: getBallTexture(), roughness: 0.7 });
    attachToHand(['handr', 'hand.r', 'hand_r'], new THREE.Mesh(new THREE.SphereGeometry(unit * 0.55, 24, 16), bm));
  }

  const scale = (1.75 * (spec.height ?? 1)) / lib.height;
  return { root, scale, lift: -lib.minY };
};
