extends CanvasLayer

@onready var health_label: Label = $HealthLabel
@onready var energy_label: Label = $EnergyLabel

func set_health(h: int) -> void:
	if health_label:
		health_label.text = "HP: %d" % h

func set_energy(e: int) -> void:
	if energy_label:
		energy_label.text = "DNA: %d" % e
