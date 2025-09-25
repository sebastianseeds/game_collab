extends StaticBody3D

func _ready() -> void:
	# Floor on Layer 1, sees Player(2) and Soldier(3)
	collision_layer = 1
	collision_mask = 0
	set_collision_mask_value(2, true)
	set_collision_mask_value(3, true)
