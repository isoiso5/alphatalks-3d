#!/usr/bin/env bash
# Downloads KayKit Character Animations (CC0, Kay Lousberg, www.kaylousberg.com)
set -euo pipefail
BASE="${MODELS_BASE:-https://raw.githubusercontent.com/NoLimitNexus/game-models/d188ebf93ceb3c4b95ba9bc6b1856cd1fd34915d}"
mkdir -p public/models
curl -fsSL -o public/models/Mannequin_Medium.glb "$BASE/tools/reference/Mannequin_Medium.glb"
for f in General MovementBasic MovementAdvanced Simulation CombatMelee Tools; do
  curl -fsSL -o "public/models/Rig_Medium_$f.glb" "$BASE/library/animations/Rig_Medium_$f.glb"
done
ls -la public/models
