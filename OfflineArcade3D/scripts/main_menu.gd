extends Control

const PIN := "2907"

@onready var pin_input: LineEdit = $VBox/Pin
@onready var error_label: Label = $VBox/Error
@onready var btn_pong: Button = $VBox/BtnPong
@onready var btn_tank: Button = $VBox/BtnTank
@onready var btn_parkour: Button = $VBox/BtnParkour

func _ready() -> void:
	_set_locked(true)
	pin_input.text_changed.connect(_on_pin_changed)
	btn_pong.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/Pong3D.tscn"))
	btn_tank.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/Tank3D.tscn"))
	btn_parkour.pressed.connect(func(): get_tree().change_scene_to_file("res://scenes/Parkour3D.tscn"))

func _on_pin_changed(_new_value: String) -> void:
	if pin_input.text == PIN:
		error_label.text = ""
		_set_locked(false)
	else:
		_set_locked(true)
		error_label.text = "Falsche PIN"

func _set_locked(locked: bool) -> void:
	btn_pong.disabled = locked
	btn_tank.disabled = locked
	btn_parkour.disabled = locked
