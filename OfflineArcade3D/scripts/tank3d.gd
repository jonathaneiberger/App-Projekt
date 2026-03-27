extends Node3D

var player_tank: Node3D
var enemy_tank: Node3D
var turret: Node3D
var camera: Camera3D
var shell: MeshInstance3D
var shell_velocity := Vector3.ZERO
var shell_active := false
var player_hp := 100
var enemy_hp := 100

func _ready() -> void:
	_setup_world()

func _setup_world() -> void:
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-55, -20, 0)
	add_child(sun)

	camera = Camera3D.new()
	camera.position = Vector3(0, 24, 32)
	camera.rotation_degrees = Vector3(-35, 0, 0)
	camera.current = true
	add_child(camera)

	var ground := MeshInstance3D.new()
	var g := PlaneMesh.new()
	g.size = Vector2(60, 60)
	ground.mesh = g
	add_child(ground)

	player_tank = _create_tank(Color(0.25, 0.8, 0.3), Vector3(-12, 0.8, 0))
	enemy_tank = _create_tank(Color(0.9, 0.2, 0.2), Vector3(12, 0.8, 0))
	turret = player_tank.get_node("Turret")

	shell = MeshInstance3D.new()
	var s := SphereMesh.new()
	s.radius = 0.3
	shell.mesh = s
	shell.visible = false
	add_child(shell)

func _create_tank(color: Color, pos: Vector3) -> Node3D:
	var root := Node3D.new()
	root.position = pos

	var body := MeshInstance3D.new()
	var body_mesh := BoxMesh.new()
	body_mesh.size = Vector3(2.8, 1.0, 2.0)
	body.mesh = body_mesh
	var mat := StandardMaterial3D.new()
	mat.albedo_color = color
	body.material_override = mat
	root.add_child(body)

	var turret_node := Node3D.new()
	turret_node.name = "Turret"
	turret_node.position = Vector3(0, 0.6, 0)
	root.add_child(turret_node)

	var gun := MeshInstance3D.new()
	var gun_mesh := BoxMesh.new()
	gun_mesh.size = Vector3(2.2, 0.2, 0.2)
	gun.mesh = gun_mesh
	gun.position = Vector3(1.0, 0.0, 0.0)
	turret_node.add_child(gun)

	add_child(root)
	return root

func _physics_process(delta: float) -> void:
	if Input.is_action_pressed("move_left"):
		player_tank.position.z -= 8 * delta
	if Input.is_action_pressed("move_right"):
		player_tank.position.z += 8 * delta
	player_tank.position.z = clamp(player_tank.position.z, -12.0, 12.0)

	if Input.is_action_pressed("move_forward"):
		turret.rotation_degrees.y -= 40 * delta
	if Input.is_action_pressed("move_back"):
		turret.rotation_degrees.y += 40 * delta

	if Input.is_action_just_pressed("shoot") and not shell_active:
		_fire_player_shell()

	_enemy_ai(delta)
	_update_shell(delta)

	if Input.is_key_pressed(KEY_ESCAPE):
		get_tree().change_scene_to_file("res://scenes/MainMenu.tscn")

func _fire_player_shell() -> void:
	shell_active = true
	shell.visible = true
	shell.position = player_tank.position + Vector3(1.8, 0.8, 0)
	var yaw := deg_to_rad(turret.rotation_degrees.y)
	shell_velocity = Vector3(cos(yaw), 0.06, sin(yaw)) * 18

func _enemy_ai(_delta: float) -> void:
	# basic strafe and periodic fire
	enemy_tank.position.z = lerp(enemy_tank.position.z, player_tank.position.z, 0.02)

func _update_shell(delta: float) -> void:
	if not shell_active:
		return
	shell.position += shell_velocity * delta
	shell_velocity.y -= 9.8 * delta

	if shell.position.y < 0.2:
		shell_active = false
		shell.visible = false

	if shell.position.distance_to(enemy_tank.position) < 1.5:
		enemy_hp -= 20
		shell_active = false
		shell.visible = false
		if enemy_hp <= 0:
			get_tree().change_scene_to_file("res://scenes/MainMenu.tscn")
