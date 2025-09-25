extends CharacterBody3D

@export var speed := 10.0
@export var accel := 40.0
@export var look_sens := 0.003
@export var jump_force := 12.0
@export var gravity := 32.0
@export var hurt_cooldown := 0.25   # for testing

var health := 100
var dash_cd := 0.0
var tail_cd := 0.0
var roar_cd := 0.0
var _hurt_cd := 0.2

var gene_energy := 0
var tier := 1  # 1=juvenile, 2=adolescent, 3=apex

var _ground_y: float = -INF
var _stick_frames: int = 0
var _lock_y_frames: int = 0
var _lock_y_value: float = 0.0
const _GROUND_SKIN := 0.10	# tiny extra height above floor

@onready var cam: Camera3D = $Camera3D
@onready var bite_ray := $BiteRay
@onready var tail_area := $TailWhipArea
@onready var _colshape: CollisionShape3D = $CollisionShape3D
@onready var hud := get_tree().get_first_node_in_group("hud")


# Build a mask from whatever layers your "enemy" nodes are actually on.
func _enemy_mask() -> int:
	var m := 0
	for n in get_tree().get_nodes_in_group("enemy"):
		if n is CollisionObject3D:
			m |= (n as CollisionObject3D).collision_layer
	return m

# Clamp the player to the floor under their feet (prevents the 1-step drop).
func _clearance_to_origin() -> float:
	var oy := 0.0
	if _colshape:
		oy = _colshape.transform.origin.y	# your 1.0

	var cap: CapsuleShape3D = null
	if _colshape and _colshape.shape is CapsuleShape3D:
		cap = _colshape.shape as CapsuleShape3D

	if cap:
		# distance from floor to *Player origin* so the capsule bottom sits on the floor
		# (radius + height/2) - local_shape_y  (+ tiny epsilon)
		return cap.radius + cap.height * 0.5 - oy + 0.02

	# fallback if shape missing: assume r≈0.5,h≈2.0 → 1.5, minus oy
	return 1.5 - oy

func _sample_floor_y() -> float:
	var from := global_transform.origin + Vector3(0, 3.0, 0)
	var to := from + Vector3(0, -10.0, 0)

	var q := PhysicsRayQueryParameters3D.new()
	q.from = from
	q.to = to
	q.exclude = [self]
	q.collide_with_bodies = true
	q.collide_with_areas = false
	q.collision_mask = 0xFFFFFFFF	# hit any floor layer
	q.hit_from_inside = true

	var hit := get_world_3d().direct_space_state.intersect_ray(q)
	if hit.has("position"):
		if hit.has("collider") and hit["collider"] is CollisionObject3D:
			var c := hit["collider"] as CollisionObject3D
		return (hit["position"] as Vector3).y
	return -INF

func _clamp_to_floor():
	# If we're in a short "stick" period, pin Y exactly.
	if _lock_y_frames > 0:
		var t := global_transform
		t.origin.y = max(t.origin.y, _lock_y_value)
		global_transform = t
		velocity.y = 0.0
		_lock_y_frames -= 1
		return

	# Otherwise: raise-only to the sampled floor.
	_ground_y = _sample_floor_y()
	if _ground_y == -INF:
		return
	var desired := _ground_y + _clearance_to_origin() + _GROUND_SKIN
	if global_transform.origin.y < desired:
		var t := global_transform
		t.origin.y = desired
		global_transform = t
		velocity.y = 0.0

func _desired_floor_y() -> float:
	var gy := _sample_floor_y()
	if gy == -INF:
		return -INF
	return gy + _clearance_to_origin() + _GROUND_SKIN
		
func _lock_to_ground(frames: int = 4) -> void:
	var dy := _desired_floor_y()
	if dy == -INF:
		return
	_lock_y_value = dy
	_lock_y_frames = frames

func _ready():
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	$Camera3D.current = true   # ensure we always have a view
	motion_mode = CharacterBody3D.MOTION_MODE_GROUNDED
	floor_max_angle = deg_to_rad(58.0)
	floor_snap_length = 1.5   # <- keeps you glued to ground on tiny gaps
	collision_layer = 1 << 1			# Layer 2
	collision_mask  = (1 << 0) | (1 << 2)	# Collide with floor(1) + enemies(3)
	
	if hud and hud.has_method("set_health"):
		hud.set_health(health)
	# if you want DNA to show on start:
	if hud and hud.has_method("set_energy"):
		hud.set_energy(gene_energy)

func _unhandled_input(event):
	if event is InputEventMouseMotion:
		rotate_y(-event.relative.x * look_sens)
		cam.rotate_x(-event.relative.y * look_sens)
		cam.rotation_degrees.x = clamp(cam.rotation_degrees.x, -80, 80)

func _physics_process(delta: float) -> void:
	# cooldowns
	dash_cd = max(dash_cd - delta, 0)
	tail_cd = max(tail_cd - delta, 0)
	roar_cd = max(roar_cd - delta, 0)
	_hurt_cd = max(_hurt_cd - delta, 0.0)

	# 1) SAMPLE INPUTS FIRST (so we can lock this same frame)
	var do_claw := Input.is_action_just_pressed("attack_primary")
	var do_bite := Input.is_action_just_pressed("attack_bite")
	var do_tail := Input.is_action_just_pressed("attack_tail")
	var do_roar := Input.is_action_just_pressed("roar")

	# if a melee is queued, start ground lock BEFORE physics
	if do_claw or (do_tail and tail_cd == 0):
		_lock_to_ground(5)
				
	# If we're ground-locked, pre-clamp before physics so we don't dip this frame.
	if _lock_y_frames > 0:
		var dy := _desired_floor_y()
		if dy != -INF:
			var t := global_transform
			t.origin.y = max(t.origin.y, dy)
			global_transform = t
			velocity.y = 0.0

	# 2) MOVEMENT
	var input_dir := Input.get_vector("move_left","move_right","move_forward","move_back")
	var wish := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	var target_vel := wish * speed
	velocity.x = lerp(velocity.x, target_vel.x, accel * delta)
	velocity.z = lerp(velocity.z, target_vel.z, accel * delta)

	# gravity
	if is_on_floor():
		velocity.y = -0.2
	else:
		velocity.y -= gravity * delta

	# dash
	if Input.is_action_just_pressed("dash") and dash_cd == 0:
		velocity += wish * 20.0
		dash_cd = 1.2

	# only snap if we are not currently ground-locked
	if _lock_y_frames == 0:
		apply_floor_snap()

	move_and_slide()
	_clamp_to_floor()

	# 3) ACTIONS AFTER MOVEMENT  ✅ (this replaces your old block)
	if do_claw:
		_claw_combo()
	if do_bite:
		_bite_execution()
	if do_tail and tail_cd == 0:
		_tail_whip()
		tail_cd = 1.0
	if do_roar and roar_cd == 0:
		_roar_shockwave()
		roar_cd = 6.0

func _shake(intensity := 0.06, time := 0.08) -> void:
	var base_h := cam.h_offset
	var base_v := cam.v_offset
	var t := time
	while t > 0.0:
		# jitter left/right only — keep vertical at base to avoid “drop” feel
		cam.h_offset = base_h + randf_range(-intensity, intensity)
		cam.v_offset = base_v
		await get_tree().process_frame
		t -= get_process_delta_time()
	cam.h_offset = base_h
	cam.v_offset = base_v
#func _claw_combo():
	#for body in tail_area.get_overlapping_bodies():
		#if body.has_method("take_damage"):
			#body.take_damage(20)

func _claw_combo():
	var range: float = 3.6                    # swipe reach (tune 2.8–3.5)
	var half_angle: float = deg_to_rad(85.0)  # cone width (tune 60–90)
	var origin: Vector3 = global_transform.origin

	# Player forward flattened to XZ
	var fwd: Vector3 = -global_transform.basis.z
	fwd.y = 0.0
	fwd = fwd.normalized()

	var hits: int = 0
	for node in get_tree().get_nodes_in_group("enemy"):
		if not (node is Node3D):
			continue
		var s := node as Node3D

		# Vector to target flattened to XZ
		var to: Vector3 = s.global_transform.origin - origin
		to.y = 0.0
		var dist: float = to.length()
		if dist > range or dist < 0.1:
			continue

		var dir: Vector3 = to / max(dist, 0.001)
		if fwd.dot(dir) > cos(half_angle):
			if s.has_method("take_damage"):
				s.take_damage(20)
				hits += 1
				
		_shake(0.06, 0.08)

# stick to ground briefly to kill any solver dip
	_stick_frames = 2
	_clamp_to_floor()

func _bite_execution():
	var dir = -cam.global_transform.basis.z
	dir.y = 0.0
	dir = dir.normalized()

	var center = cam.global_transform.origin + dir * 1.2	# center of the bite volume
	var shape := SphereShape3D.new()
	shape.radius = 0.6

	var p := PhysicsShapeQueryParameters3D.new()
	p.shape = shape
	p.transform = Transform3D(Basis(), center)
	p.exclude = [self]
	p.collide_with_bodies = true
	p.collide_with_areas = false
	p.collision_mask = _enemy_mask()
	
	var mask := _enemy_mask()
	if mask == 0:
		mask = 1 << 2	# sane default: Layer 3
	p.collision_mask = mask

	var hits := get_world_3d().direct_space_state.intersect_shape(p, 8)
	if hits.size() == 0:
		return

	for h in hits:
		if h.has("collider"):
			var c: Object = h["collider"]
			if c.has_method("execute"):
				c.execute()
				health = min(health + 30, 100)
			elif c.has_method("take_damage"):
				c.take_damage(40)
			break
			
#func _tail_whip():
	#for body in tail_area.get_overlapping_bodies():
		#if body.has_method("take_damage"):
			#body.take_damage(25)
		#if body.has_method("apply_impulse"):
			#var dir: Vector3 = (body.global_transform.origin - global_transform.origin).normalized()
			#body.apply_impulse(dir * 15.0)

func _tail_whip():
	var bodies = tail_area.get_overlapping_bodies()
	for body in bodies:
		if body == self or body.is_in_group("player"):
			continue
		if body.has_method("take_damage"):
			body.take_damage(25)
		if body.has_method("apply_impulse"):
			var offset: Vector3 = body.global_transform.origin - global_transform.origin
			offset.y = 0.0
			var dir: Vector3 = offset.normalized()
			body.apply_impulse(dir * 15.0)
	_shake()
	# stick to ground briefly to kill any solver dip
	_stick_frames = 2
	_clamp_to_floor()
	
func _roar_shockwave():
	for body in tail_area.get_overlapping_bodies():
		if body.has_method("stagger"):
			body.stagger(1.0)

func apply_impulse(v: Vector3) -> void:
	v.y = 0.0
	velocity += v

func take_damage(dmg:int):
	if _hurt_cd > 0.0:
		return
	health -= dmg
	print("Player hit: -%d -> hp=%d" % [dmg, health])
	if hud and hud.has_method("set_health"):
		hud.set_health(health)
	_hurt_cd = hurt_cooldown
	if health <= 0:
		queue_free()

	if _hurt_cd > 0.0:
		return
	health -= dmg
	if hud and hud.has_method("set_health"):
		hud.set_health(health)
	_hurt_cd = hurt_cooldown

func gain_genetic_energy(a:int):
	gene_energy += a
	if hud and hud.has_method("set_energy"):
		hud.set_energy(gene_energy)
	_check_evolution()

func _check_evolution():
	var thresholds = [0, 50, 150]
	if tier < 3 and gene_energy >= thresholds[tier]:
		tier += 1
		_apply_evolution(tier)

func _apply_evolution(t:int):
	match t:
		2:
			speed += 2.0
		3:
			speed += 2.0
			health = min(health + 40, 140)
