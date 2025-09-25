extends CharacterBody3D

@export var hp: int = 60
@export var move_speed: float = 6.0
@export var touch_damage: int = 8
@export var touch_range: float = 1.6
@export var think_interval: float = 0.2

var _think_cd: float = 0.0
var _player: Node3D

func _ready() -> void:
	# Find the player (put your Player node in the "player" group in the editor)
	_player = get_tree().get_first_node_in_group("player")

func _physics_process(delta: float) -> void:
	if _player == null:
		return

	# very light "AI": every think_interval, steer toward the player
	_think_cd = max(_think_cd - delta, 0.0)
	if _think_cd == 0.0:
		_think_cd = think_interval
		var to_target: Vector3 = _player.global_transform.origin - global_transform.origin
		var flat: Vector3 = Vector3(to_target.x, 0.0, to_target.z)
		var dir: Vector3 = flat.normalized()
		velocity.x = dir.x * move_speed
		velocity.z = dir.z * move_speed
		look_at(Vector3(_player.global_transform.origin.x, global_transform.origin.y, _player.global_transform.origin.z), Vector3.UP)

	# simple gravity (optional if your level is fully flat)
	if not is_on_floor():
		velocity.y -= 32.0 * delta
	else:
		velocity.y = 0.0

	move_and_slide()

	# poke the player for damage if very close (prototype)
	if global_transform.origin.distance_to(_player.global_transform.origin) <= touch_range:
		if _player.has_method("take_damage"):
			_player.take_damage(touch_damage)

# ----- Combat API -----

func take_damage(dmg: int) -> void:
	hp -= dmg
	if hp <= 0:
		_drop_genetic_energy(false)
		queue_free()

func execute() -> void:
	# instant kill with bigger drop (used by player's bite execution)
	_drop_genetic_energy(true)
	queue_free()

func stagger(duration_sec: float) -> void:
	# placeholder: briefly slow movement
	var old_speed := move_speed
	move_speed = max(0.0, move_speed * 0.25)
	await get_tree().create_timer(duration_sec).timeout
	move_speed = old_speed

func apply_impulse(v: Vector3) -> void:
	# crude knockback for prototype
	velocity += v

# ----- Drops -----

func _drop_genetic_energy(big: bool) -> void:
	var scene: PackedScene = load("res://scenes/GeneticEnergy.tscn")
	if scene == null:
		return
	var node: Node3D = scene.instantiate()
	# bigger amount on executions
	var amt: int = 20 if big else 8
	if node.has_variable("amount"):
		node.set("amount", amt)
	# place at soldier position
	node.global_transform.origin = global_transform.origin
	get_tree().current_scene.add_child(node)
