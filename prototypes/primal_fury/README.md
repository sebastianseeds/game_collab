# PRIMAL FURY
╭────────────────────────────────────────────────────────────────────────────╮
│ A fast, Doom-style first-person action prototype where **you** are the dino │
│ Built with **Godot 4.4.1** (Forward+)                                       │
╰────────────────────────────────────────────────────────────────────────────╯

> ▸ Play as a juvenile apex that evolves by harvesting **Genetic Energy**  
> ▸ Melee-forward combat: **Claw**, **Bite (Execution)**, **Tail Whip**, **Roar**  
> ▸ Capsule-center combat math for **reliable head-on hits**

---

## ✨ High Concept

- 🐊 **Evolve**: 3 tiers → Juvenile → Adolescent → Apex (speed/health bumps).
- 🪓 **Attacks**:
  - **Claw**: short-range cone swipe aimed by camera.
  - **Bite**: close execution; big damage & bonus drops.
  - **Tail Whip**: radial AOE + knockback.
  - **Roar**: brief stagger for space control.
- 🪖 **Soldiers**: grounded melee AI, drop **Genetic Energy** (more on execution).
- 🦕 **Stegosaurus variant** *(design WIP)*: heavy armor, lower HP, tail-spine
  projectiles on whip.

---

## 🧪 Current Prototype

- **Player**: dash/jump/snap-to-floor, camera shake, evolution thresholds, hurt CD.
- **Enemies**: contact computed from **capsule centers** (not scene roots).
- **Pickups**: `GeneticEnergy.tscn` dropped on death/execution.
- **HUD (basic)**: HP / Energy labels (easy to swap later).
- **Physics polish**: sensible layers/masks; snap/clamp to prevent step-drops.

---

## 🎮 Controls (default)

```
W A S D   Move
Mouse     Look
Space     Jump
Shift     Dash
LMB       Claw
RMB       Bite / Execution
Q         Tail Whip
E         Roar
Esc       Release mouse
```

---

## 🗂 Project Layout

```
scenes/
  Arena.tscn             (Main)
  Player.tscn            (CharacterBody3D + Camera, BiteRay, TailWhipArea)
  Soldier.tscn           (CharacterBody3D + CollisionShape3D)
  GeneticEnergy.tscn     (pickup)

scripts/
  player.gd              (movement/attacks/evolution/HUD hooks)
  soldier.gd             (grounded AI + melee, capsule-center math)
  genetic_energy.gd      (pickup logic)
  hud.gd                 (labels; optional)
```

---

## ▶️ Run It

1. Install **Godot 4.4.1 stable**.
2. Open the project folder in Godot.
3. Set **Main Scene**: `Project → Project Settings → Application → Run → Main Scene → scenes/Arena.tscn`.
4. **Play**.

> Tip: If collisions look odd, toggle **Debug → Visible Collision Shapes**.

---

## 🧱 Layers / Masks (quick reference)

```
| Node                  | Layer | Mask      |
|---------------------- |:-----:|:---------:|
| Floor (StaticBody3D)  |   1   | 1 + 6*    |
| Player (Character)    |   2   | 1 + 3     |
| TailWhip (Area3D)     |   2   | 3         |
| Soldier (Character)   |   3   | 1 + 2     |

* “6” is the default Godot extra mask; leaving it is fine.
```

---

## 🔧 Tuning Cheatsheet

**Player (player.gd)**
```
speed:           10–12
accel:           ~40
look_sens:       ~0.003
gravity:         ~32
jump_force:      ~12
hurt_cooldown:   0.6–0.8
floor_snap_len:  1.2–1.6   (prevents step-drop on attacks)
```

**Soldier (soldier.gd)**
```
hp:              60
move_speed:      6.0–7.5
touch_damage:    8
attack_cooldown: 0.7–1.0
touch_range:     1.2–1.4
capsule radius:  0.8  (example)
```

**Hit Detection Highlights**
- **Bite** → small overlap sphere in front of camera; executions heal & drop more.
- **Claw** → cone check in front (adjust angle/range for feel).
- **Soldier melee** → computed using **capsule centers** with small tolerance so
  **head-on hits** land reliably and don’t “hover” at the edge.

---

## 🧭 Known Quirks & Fixes

- **Sunken/floating characters**  
  ▸ Check each `CollisionShape3D` Y-offset (capsule center ≈ mid-torso).  
  ▸ Verify capsule **radius/height** feel right for model scale.  
  ▸ Keep `floor_snap_length` ≥ 1.2 on characters.

- **Melee feels shy at contact**  
  ▸ Confirm `touch_range` isn’t too small vs. `soldier_radius + player_radius`.  
  ▸ Ensure both actors’ capsules are centered under their models.

---

## 🛣️ Short Roadmap

- [ ] **Stegosaurus** kit: armor bias, tail-spine projectiles.
- [ ] **Ranged soldiers**: darts/shocks, simple boss.
- [ ] **Navmesh** pathing & obstacle avoidance.
- [ ] **Feedback pass**: SFX, hit flashes, decals, post-FX.
- [ ] **Progression**: tier UI, simple upgrades (wider claw vs. faster dash).
- [ ] **Encounters**: waves/spawners, lab/yard arena variants.

---

## 🤝 Contributing

PRs welcome! Keep diffs focused (e.g., “navmesh pass”, “HUD polish”, “Stego tail
prototype”). Use clear commit messages and prefer small, testable chunks.

---

## ⚖️ License

- **Code**: MIT  
- **Placeholder assets**: prototype-only, replace for any distribution.

---

## 🧵 One-liner Pitch

> _Primal Fury_ flips the boomer-shooter fantasy: **you’re the dinosaur**. Claw through
> squads, **execute** with a crushing bite, and **evolve** mid-arena by harvesting
> Genetic Energy. Become the apex.