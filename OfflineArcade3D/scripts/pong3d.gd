extends Node3D

var player: Node3D
var bot: Node3D
var ball: Node3D
var camera: Camera3D
var hud_label: Label
var pause_label: Label
var score := Vector2i(0, 0)
var ball_velocity := Vector3(9, 0, 6)

func _ready() -> void:
	_setup_world()
	_setup_hud()

func _setup_world() -> void:
	var light := DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-45, -20, 0)
	add_child(light)

	camera = Camera3D.new()
	camera.position = Vector3(0, 16, 22)
	camera.rotation_degrees = Vector3(-30, 0, 0)
	camera.current = true
	add_child(camera)

	var floor := MeshInstance3D.new()
	floor.mesh = BoxMesh.new()
	floor.scale = Vector3(2.4, 0.2, 1.2)
	floor.position = Vector3(0, -1, 0)
	add_child(floor)

	player = _create_paddle(Color(0.2, 0.85, 0.3), -10)
	bot = _create_paddle(Color(0.9, 0.35, 0.2), 10)

	ball = MeshInstance3D.new()
	var sphere := SphereMesh.new()
	sphere.radius = 0.5
	ball.mesh = sphere
	ball.position = Vector3.ZERO
	add_child(ball)

func _setup_hud() -> void:
	var canvas := CanvasLayer.new()
	add_child(canvas)

	hud_label = Label.new()
	hud_label.position = Vector2(20, 20)
	hud_label.add_theme_font_size_override("font_size", 26)
	canvas.add_child(hud_label)

	pause_label = Label.new()
	pause_label.text = "PAUSIERT (P)"
	pause_label.visible = false
	pause_label.position = Vector2(520, 24)
	pause_label.add_theme_font_size_override("font_size", 28)
	canvas.add_child(pause_label)

func _create_paddle(color: Color, x_pos: float) -> Node3D:
	var paddle := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = Vector3(0.8, 1.5, 3.2)
	paddle.mesh = mesh
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	paddle.material_override = mat
	paddle.position = Vector3(x_pos, 0, 0)
	add_child(paddle)
	return paddle

func _physics_process(delta: float) -> void:
	if Input.is_key_pressed(KEY_P):
		get_tree().paused = true
		pause_label.visible = true
	if Input.is_key_pressed(KEY_O):
		get_tree().paused = false
		pause_label.visible = false

	if get_tree().paused:
		return

	if Input.is_action_pressed("move_forward"):
		player.position.z -= 8.0 * delta
	if Input.is_action_pressed("move_back"):
		player.position.z += 8.0 * delta
	player.position.z = clamp(player.position.z, -5.0, 5.0)

	bot.position.z = lerp(bot.position.z, ball.position.z, delta * 3.0)
	bot.position.z = clamp(bot.position.z, -5.0, 5.0)

	ball.position += ball_velocity * delta
	if abs(ball.position.z) > 5.5:
		ball_velocity.z *= -1

	if ball.position.distance_to(player.position) < 1.8 and ball_velocity.x < 0:
		ball_velocity.x = abs(ball_velocity.x) * 1.02
	if ball.position.distance_to(bot.position) < 1.8 and ball_velocity.x > 0:
		ball_velocity.x = -abs(ball_velocity.x) * 1.02

	if ball.position.x < -13:
		score.y += 1
		_reset_round(1)
	if ball.position.x > 13:
		score.x += 1
		_reset_round(-1)

	hud_label.text = "PONG 3D | DU %d : %d BOT | ESC Menü | P Pause / O Resume" % [score.x, score.y]

	if Input.is_key_pressed(KEY_ESCAPE):
		get_tree().paused = false
		get_tree().change_scene_to_file("res://scenes/MainMenu.tscn")

func _reset_round(dir: int) -> void:
	ball.position = Vector3.ZERO
	ball_velocity = Vector3(9 * dir, 0, randf_range(-7.0, 7.0))
