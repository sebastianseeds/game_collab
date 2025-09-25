extends CharacterBody3D

@export var hp: int = 60
@export var move_speed: float = 8.0
@export var touch_damage: int = 8
@export var touch_range: float = 1.2
@export var think_interval: float = 0.2
@export var attack_cooldown: float = 0.7
@onready var body_mesh: MeshInstance3D = $Body

var _atk_cd: float = 0.0
var _think_cd: float = 0.0
var _player: Node3D
var _stick_frames: int = 0
var _dbg_accum := 0.0
@onready var _shape: CollisionShape3D = $CollisionShape3D

func _capsule_radius(n: Node) -> float:
	# read capsule radius for self or player
	var cs: CollisionShape3D = null
	if n == self:
		cs = _shape
	elif n is Node3D:
		cs = (n as Node3D).get_node_or_null("CollisionShape3D") as CollisionShape3D
	if cs and cs.shape is CapsuleShape3D:
		return (cs.shape as CapsuleShape3D).radius
	return 0.6  # fallback
	
func _capsule_center_global(n: Node) -> Vector3:
	# returns the capsule's global center if possible, else node origin
	if n == self:
		if _shape:
			return _shape.global_transform.origin
	elif n is Node3D:
		var cs := (n as Node3D).get_node_or_null("CollisionShape3D")
		if cs and cs is CollisionShape3D:
			return (cs as CollisionShape3D).global_transform.origin
	return (n as Node3D).global_transform.origin

func _min_center_dist_to_player() -> float:
	if _player == null:
		return 1.4
	var pr := _capsule_radius(_player)
	var sr := _capsule_radius(self)
	# small padding so they don't need to interpenetrate to hit
	return pr + sr + 0.15  # e.g., 0.5 + 0.8 + 0.15 = 1.45

func _player_mask() -> int:
	# Use the player's layer if available, otherwise allow all layers.
	if _player is CollisionObject3D:
		return (_player as CollisionObject3D).collision_layer
	return 0x7FFFFFFF  # collide with everything (32 bits)
	
func _player_capsule_center_y() -> float:
	var cs := (_player as Node3D).get_node_or_null("CollisionShape3D") as CollisionShape3D
	if cs:
		return cs.global_transform.origin.y
	return _player.global_transform.origin.y

const DEBUG_MELEE := false

const EPS := 0.06  # small tolerance for float + movement settling

func _try_melee_hit() -> bool:
	# compute with CAPSULE CENTERS
	var my_center := _capsule_center_global(self)
	var pl_center := _capsule_center_global(_player)

	var to: Vector3 = pl_center - my_center
	to.y = 0.0
	var dist: float = to.length()

	var sr: float = _capsule_radius(self)
	var pr: float = _capsule_radius(_player)
	var contact_needed: float = max(touch_range, sr + pr)

	if dist > contact_needed + EPS:
		# debug: print("gate FAIL dist=%.3f need=%.3f" % [dist, contact_needed])
		return false

	# overlap at the PLAYER capsule center
	var center := pl_center
	var shape := SphereShape3D.new()
	shape.radius = pr + 0.55

	var p := PhysicsShapeQueryParameters3D.new()
	p.shape = shape
	p.transform = Transform3D(Basis(), center)
	p.exclude = [self]
	p.collide_with_bodies = true
	p.collide_with_areas = false
	p.collision_mask = 0x7FFFFFFF

	var hits := get_world_3d().direct_space_state.intersect_shape(p, 8)
	for h in hits:
		var c: Object = h.get("collider", null)
		if c == _player and c.has_method("take_damage"):
			_player.take_damage(touch_damage)
			return true

	# ray fallback soldier -> player center
	var rq := PhysicsRayQueryParameters3D.new()
	rq.from = my_center + Vector3(0, 0.8, 0)
	rq.to   = center
	rq.exclude = [self]
	rq.collide_with_bodies = true
	rq.collide_with_areas = false
	rq.collision_mask = 0x7FFFFFFF

	var r := get_world_3d().direct_space_state.intersect_ray(rq)
	if r.has("collider"):
		var col: Object = r["collider"]
		if col == _player and _player.has_method("take_damage"):
			_player.take_damage(touch_damage)
			return true

	# final safety
	if dist <= contact_needed + EPS and _player.has_method("take_damage"):
		_player.take_damage(touch_damage)
		return true

	return false
	
func _clearance_to_origin() -> float:
	if _shape and _shape.shape is CapsuleShape3D:
		var c := _shape.shape as CapsuleShape3D
		return c.radius + c.height * 0.5 + 0.02  # = 1.62
	return 1.5
	
func _snap_to_floor_now() -> void:
	var from := global_transform.origin + Vector3(0, 3.0, 0)
	var to := from + Vector3(0, -10.0, 0)
	var q := PhysicsRayQueryParameters3D.new()
	q.from = from
	q.to = to
	q.exclude = [self]
	q.collide_with_bodies = true
	q.collide_with_areas = false
	q.collision_mask = 0xFFFFFFFF
	q.hit_from_inside = true
	var hit := get_world_3d().direct_space_state.intersect_ray(q)
	if hit.has("position"):
		var gy := (hit["position"] as Vector3).y
		var desired := gy + _clearance_to_origin()
		var t := global_transform
		if t.origin.y < desired:
			t.origin.y = desired
			global_transform = t
			velocity.y = 0.0

func _snap_to_floor_for(frames: int) -> void:
	_stick_frames = frames
	_snap_to_floor_now()

func _place_on_floor_once() -> void:
	await get_tree().process_frame  # ensure parent/world transforms are settled
	var from := global_transform.origin + Vector3(0, 3.0, 0)
	var to := from + Vector3(0, -10.0, 0)
	var q := PhysicsRayQueryParameters3D.new()
	q.from = from; q.to = to
	q.exclude = [self]
	q.collide_with_bodies = true
	q.collide_with_areas = false
	q.collision_mask = 0xFFFFFFFF
	q.hit_from_inside = true
	var hit := get_world_3d().direct_space_state.intersect_ray(q)
	if hit.has("position"):
		var ground_y := (hit["position"] as Vector3).y
		var t := global_transform
		t.origin.y = ground_y + _clearance_to_origin() + 0.10
		global_transform = t

func _ready() -> void:
	# CharacterBody3D posture
	motion_mode = CharacterBody3D.MOTION_MODE_GROUNDED
	floor_max_angle = deg_to_rad(58.0)
	floor_snap_length = 1.2
	safe_margin = 0.04

	# Layers/Masks: enemy on Layer 3; collide with floor(1) + player(2)
	collision_layer = 1 << 2                 # 4
	collision_mask  = (1 << 0) | (1 << 1)    # 3

	# Let transforms settle, then glue to floor for a short window
	await get_tree().process_frame
	_snap_to_floor_for(12)                   # ~0.2s at 60 FPS

	add_to_group("enemy")
	_player = get_tree().get_first_node_in_group("player")
	
	print("[SOLDIER READY] path=", get_script().resource_path, " id=", get_instance_id())
	if _player == null:
		print("[SOLDIER READY] _player is NULL!")

	if _shape and _shape.shape is CapsuleShape3D:
		print("[SOLDIER READY] capsule center=", _shape.global_transform.origin)
		var cs_p := (_player as Node3D).get_node_or_null("CollisionShape3D") as CollisionShape3D
		if cs_p:
			print("[PLAYER  READY] capsule center=", cs_p.global_transform.origin)

func _physics_process(delta: float) -> void:
	# glue to floor for a few frames after spawn
	if _stick_frames > 0:
		_snap_to_floor_now()
		_stick_frames -= 1

	if _player == null:
		return

	# cooldowns
	_think_cd = max(_think_cd - delta, 0.0)
	_atk_cd = max(_atk_cd - delta, 0.0)

	# --- compute flat vector between CAPSULE CENTERS, and unified contact ---
	var my_center: Vector3 = _capsule_center_global(self)
	var pl_center: Vector3 = _capsule_center_global(_player)

	var to: Vector3 = pl_center - my_center
	to.y = 0.0
	var dist: float = to.length()

	var sr: float = _capsule_radius(self)
	var pr: float = _capsule_radius(_player)
	var need: float = max(touch_range, sr + pr)  # same notion of "contact" as melee

	# --- steering update EVERY frame (continuous, so we actually close) ---
	if dist > 0.001:
		var dir: Vector3 = to / dist
		var target := dir * move_speed
		velocity.x = lerp(velocity.x, target.x, 8.0 * delta)
		velocity.z = lerp(velocity.z, target.z, 8.0 * delta)
		# face the player but stay upright
		look_at(Vector3(pl_center.x, global_transform.origin.y, pl_center.z), Vector3.UP)

	# ease near contact to reduce jitter (but don't stop completely)
	if dist < need + 0.35:
		velocity.x *= 0.7
		velocity.z *= 0.7

	# --- NUDGE: if hovering just outside contact, push forward a bit ---
	if dist > need - 0.05 and dist < need + 0.70:
		var dir2: Vector3 = (to / max(dist, 0.001))
		var push := move_speed * 0.45
		velocity.x += dir2.x * push
		velocity.z += dir2.z * push

	# melee with cooldown
	if _atk_cd <= 0.0:
		var landed := _try_melee_hit()
		if landed:
			_atk_cd = attack_cooldown

	# gravity / ground
	if is_on_floor():
		velocity.y = -0.2
	else:
		velocity.y -= 32.0 * delta

	# snap, then slide
	apply_floor_snap()
	move_and_slide()

# ----- Combat API -----

func take_damage(dmg: int) -> void:
	hp -= dmg
	_flash()
	if hp <= 0:
		_drop_genetic_energy(false)
		queue_free()

func _flash() -> void:
	if body_mesh:
		var old = body_mesh.modulate
		body_mesh.modulate = Color(1, 0.4, 0.4)
		await get_tree().create_timer(0.08).timeout
		body_mesh.modulate = old

func execute() -> void:
	_drop_genetic_energy(true)
	queue_free()

func stagger(duration_sec: float) -> void:
	var old_speed := move_speed
	move_speed = max(0.0, move_speed * 0.25)
	await get_tree().create_timer(duration_sec).timeout
	move_speed = old_speed

func apply_impulse(v: Vector3) -> void:
	v.y = 0.0
	velocity += v

# ----- Drops -----

func _drop_genetic_energy(big: bool) -> void:
	var scene: PackedScene = load("res://scenes/GeneticEnergy.tscn")
	if scene == null:
		return
	var node: Node3D = scene.instantiate()
	var amt: int = 20 if big else 8
	if node.has_variable("amount"):
		node.set("amount", amt)
	node.global_transform.origin = global_transform.origin
	get_tree().current_scene.add_child(node)
