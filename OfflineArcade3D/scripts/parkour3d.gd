extends Node3D

var player: CharacterBody3D
var camera: Camera3D
var speed := 8.0
var jump_velocity := 8.5
var gravity := ProjectSettings.get_setting("physics/3d/default_gravity")
var hud_label: Label
var pause_label: Label
var coins := 0
var coin_nodes: Array[Node3D] = []

func _ready() -> void:
	_build_level()
	_setup_hud()

func _build_level() -> void:
	var light := DirectionalLight3D.new()
	light.rotation_degrees = Vector3(-40, -30, 0)
	add_child(light)

	camera = Camera3D.new()
	camera.position = Vector3(-8, 10, 18)
	camera.rotation_degrees = Vector3(-20, -25, 0)
	camera.current = true
	add_child(camera)

	_add_platform(Vector3(0, -0.5, 0), Vector3(40, 1, 8), Color(0.3, 0.3, 0.35))
	_add_platform(Vector3(8, 1, 0), Vector3(3, 1, 3), Color(0.5, 0.4, 0.3))
	_add_platform(Vector3(14, 3, 0), Vector3(3, 1, 3), Color(0.5, 0.4, 0.3))
	_add_platform(Vector3(20, 5, 0), Vector3(3, 1, 3), Color(0.5, 0.4, 0.3))
	_add_platform(Vector3(28, 7, 0), Vector3(4, 1, 4), Color(0.2, 0.7, 0.2))

	for pos in [Vector3(6,1.8,0), Vector3(12,3.8,0), Vector3(18,5.8,0), Vector3(26,7.8,0)]:
		_add_coin(pos)

	player = CharacterBody3D.new()
	player.position = Vector3(-15, 1, 0)
	var mesh := MeshInstance3D.new()
	var capsule := CapsuleMesh.new()
	capsule.radius = 0.4
	capsule.height = 1.2
	mesh.mesh = capsule
	player.add_child(mesh)
	var body := CollisionShape3D.new()
	var shape := CapsuleShape3D.new()
	shape.radius = 0.4
	shape.height = 1.2
	body.shape = shape
	player.add_child(body)
	add_child(player)

func _setup_hud() -> void:
	var canvas := CanvasLayer.new()
	add_child(canvas)
	hud_label = Label.new()
	hud_label.position = Vector2(20, 18)
	hud_label.add_theme_font_size_override("font_size", 24)
	canvas.add_child(hud_label)
	pause_label = Label.new()
	pause_label.text = "PAUSIERT (P/O)"
	pause_label.position = Vector2(520, 20)
	pause_label.visible = false
	pause_label.add_theme_font_size_override("font_size", 28)
	canvas.add_child(pause_label)

func _add_platform(pos: Vector3, size: Vector3, color: Color) -> void:
	var platform := StaticBody3D.new()
	platform.position = pos
	var mesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = size
	mesh.mesh = box
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	mesh.material_override = mat
	platform.add_child(mesh)
	var col := CollisionShape3D.new()
	var col_shape := BoxShape3D.new()
	col_shape.size = size
	col.shape = col_shape
	platform.add_child(col)
	add_child(platform)

func _add_coin(pos: Vector3) -> void:
	var coin := MeshInstance3D.new()
	var cyl := CylinderMesh.new()
	cyl.top_radius = 0.35
	cyl.bottom_radius = 0.35
	cyl.height = 0.12
	coin.mesh = cyl
	coin.position = pos
	coin.rotation_degrees = Vector3(90, 0, 0)
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(1, 0.84, 0.2)
	coin.material_override = mat
	coin_nodes.append(coin)
	add_child(coin)

func _physics_process(delta: float) -> void:
	if Input.is_key_pressed(KEY_P):
		get_tree().paused = true
		pause_label.visible = true
	if Input.is_key_pressed(KEY_O):
		get_tree().paused = false
		pause_label.visible = false
	if get_tree().paused:
		return

	if not player.is_on_floor():
		player.velocity.y -= gravity * delta

	var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction := Vector3(input_dir.y, 0, input_dir.x)
	if direction.length() > 0:
		direction = direction.normalized()
		player.velocity.x = direction.x * speed
		player.velocity.z = direction.z * speed
	else:
		player.velocity.x = move_toward(player.velocity.x, 0, speed)
		player.velocity.z = move_toward(player.velocity.z, 0, speed)

	if Input.is_action_just_pressed("jump") and player.is_on_floor():
		player.velocity.y = jump_velocity

	player.move_and_slide()
	camera.position = camera.position.lerp(player.position + Vector3(-8, 8, 14), 0.06)
	camera.look_at(player.position + Vector3(0, 1, 0), Vector3.UP)

	for coin in coin_nodes:
		if is_instance_valid(coin):
			coin.rotate_y(delta * 3.0)
			if coin.position.distance_to(player.position) < 1.0:
				coins += 1
				coin.queue_free()

	hud_label.text = "PARKOUR 3D | Coins: %d | ESC Menü" % coins

	if player.position.x > 30:
		_spawn_finish_particles(player.position)
		get_tree().paused = false
		get_tree().change_scene_to_file("res://scenes/MainMenu.tscn")

	if Input.is_key_pressed(KEY_ESCAPE):
		get_tree().paused = false
		get_tree().change_scene_to_file("res://scenes/MainMenu.tscn")

func _spawn_finish_particles(at_pos: Vector3) -> void:
	var p := GPUParticles3D.new()
	var mat := ParticleProcessMaterial.new()
	mat.direction = Vector3(0, 1, 0)
	mat.initial_velocity_min = 3
	mat.initial_velocity_max = 7
	p.process_material = mat
	p.amount = 80
	p.lifetime = 1.0
	p.one_shot = true
	p.position = at_pos
	add_child(p)
	p.emitting = true
