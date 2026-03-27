import math
import random
import tkinter as tk
from tkinter import ttk, messagebox
from enum import Enum


class BotDifficulty(Enum):
    EASY = ("Leicht", 0.35)
    MEDIUM = ("Mittel", 0.55)
    HARD = ("Schwer", 0.75)
    VERY_HARD = ("Sehr schwer", 0.90)

    @property
    def label(self) -> str:
        return self.value[0]

    @property
    def skill(self) -> float:
        return self.value[1]


class LockScreen(ttk.Frame):
    def __init__(self, master, on_unlock):
        super().__init__(master, padding=20)
        self.on_unlock = on_unlock
        self.pin_value = "2907"

        ttk.Label(self, text="🔒 Offline Arcade (Windows)", font=("Segoe UI", 18, "bold")).pack(pady=(0, 12))
        ttk.Label(self, text="Nur für berechtigte Nutzer", foreground="#555").pack(pady=(0, 16))

        row = ttk.Frame(self)
        row.pack(pady=6)
        ttk.Label(row, text="PIN:").pack(side=tk.LEFT, padx=(0, 8))
        self.pin_entry = ttk.Entry(row, show="*", width=12)
        self.pin_entry.pack(side=tk.LEFT)

        ttk.Button(self, text="Entsperren", command=self.try_unlock).pack(pady=10)

    def try_unlock(self):
        if self.pin_entry.get().strip() == self.pin_value:
            self.on_unlock()
        else:
            messagebox.showerror("Fehler", "Falsche PIN")
            self.pin_entry.delete(0, tk.END)


class ArcadeHub(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self.difficulty_var = tk.StringVar(value=BotDifficulty.MEDIUM.label)

        top = ttk.Frame(self)
        top.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(top, text="Bot-Schwierigkeit:").pack(side=tk.LEFT, padx=(0, 8))
        options = [d.label for d in BotDifficulty]
        ttk.Combobox(top, textvariable=self.difficulty_var, values=options, width=14, state="readonly").pack(side=tk.LEFT)

        info = ttk.Label(
            top,
            text="Steuerung: Spiel-Tab öffnen und Fenster anklicken, dann Tastatur nutzen.",
            foreground="#666",
        )
        info.pack(side=tk.LEFT, padx=15)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        games = [
            ("Fußball", SoccerGame),
            ("Tischtennis", TableTennisGame),
            ("Schiffe", BattleshipGame),
            ("TicTacToe", TicTacToeGame),
            ("Rennspiel", RacingGame),
            ("Tank", TankGame),
            ("Parkour", PlatformerGame),
            ("Memory", MemoryGame),
            ("Code", CodeBreakerGame),
        ]

        for title, cls in games:
            frame = cls(self.notebook, self.current_difficulty)
            self.notebook.add(frame, text=title)

    def current_difficulty(self) -> BotDifficulty:
        label = self.difficulty_var.get()
        for d in BotDifficulty:
            if d.label == label:
                return d
        return BotDifficulty.MEDIUM


class SoccerGame(ttk.Frame):
    def __init__(self, master, get_diff):
        super().__init__(master, padding=12)
        self.get_diff = get_diff
        self.score = 0
        self.rounds = 0

        self.info = tk.StringVar(value="Wähle Schussrichtung")
        self.stats = tk.StringVar(value="Tore: 0/0")

        ttk.Label(self, text="Fußball-Duell", font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(self, textvariable=self.stats).pack(pady=(4, 2))
        ttk.Label(self, textvariable=self.info).pack(pady=(0, 10))

        btns = ttk.Frame(self)
        btns.pack()
        for i, label in enumerate(["Links", "Mitte", "Rechts"]):
            ttk.Button(btns, text=label, command=lambda lane=i: self.shoot(lane)).pack(side=tk.LEFT, padx=6)

    def shoot(self, lane):
        self.rounds += 1
        diff = self.get_diff()
        goalie = lane if random.random() < diff.skill else random.randint(0, 2)
        if goalie == lane:
            self.info.set("Gehalten!")
        else:
            self.score += 1
            self.info.set("TOOOOR!")
        self.stats.set(f"Tore: {self.score}/{self.rounds}")


class TableTennisGame(ttk.Frame):
    def __init__(self, master, get_diff):
        super().__init__(master, padding=8)
        self.get_diff = get_diff
        self.width, self.height = 760, 360
        self.running = True
        self.keys = set()

        ttk.Label(self, text="Tischtennis (echt spielbar)", font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(self, text="Steuerung: ↑/↓ für deinen Schläger", foreground="#666").pack(pady=(0, 6))

        self.score_text = tk.StringVar(value="Du 0 : 0 Bot")
        ttk.Label(self, textvariable=self.score_text).pack()

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="#0f1828", highlightthickness=0)
        self.canvas.pack(pady=6)

        self.player_score = 0
        self.bot_score = 0

        self.player_y = self.height / 2
        self.bot_y = self.height / 2
        self.paddle_h = 70
        self.ball_x = self.width / 2
        self.ball_y = self.height / 2
        self.ball_vx = 6
        self.ball_vy = 3

        self.bind_all("<KeyPress>", self.on_key_down)
        self.bind_all("<KeyRelease>", self.on_key_up)
        self.update_loop()

    def on_key_down(self, e):
        self.keys.add(e.keysym)

    def on_key_up(self, e):
        self.keys.discard(e.keysym)

    def reset_ball(self, direction=1):
        self.ball_x = self.width / 2
        self.ball_y = self.height / 2
        self.ball_vx = direction * random.choice([5, 6, 7])
        self.ball_vy = random.choice([-4, -3, 3, 4])

    def update_loop(self):
        if "Up" in self.keys:
            self.player_y -= 8
        if "Down" in self.keys:
            self.player_y += 8
        self.player_y = max(self.paddle_h / 2, min(self.height - self.paddle_h / 2, self.player_y))

        diff = self.get_diff()
        bot_speed = 2 + int(diff.skill * 10)
        if self.ball_y < self.bot_y - 4:
            self.bot_y -= bot_speed
        elif self.ball_y > self.bot_y + 4:
            self.bot_y += bot_speed
        self.bot_y = max(self.paddle_h / 2, min(self.height - self.paddle_h / 2, self.bot_y))

        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        if self.ball_y <= 8 or self.ball_y >= self.height - 8:
            self.ball_vy *= -1

        left_x, right_x = 30, self.width - 30

        if self.ball_x <= left_x + 8 and abs(self.ball_y - self.player_y) <= self.paddle_h / 2:
            self.ball_vx = abs(self.ball_vx)
            spin = (self.ball_y - self.player_y) / 12
            self.ball_vy += spin

        if self.ball_x >= right_x - 8 and abs(self.ball_y - self.bot_y) <= self.paddle_h / 2:
            self.ball_vx = -abs(self.ball_vx)
            spin = (self.ball_y - self.bot_y) / 12
            self.ball_vy += spin

        if self.ball_x < 0:
            self.bot_score += 1
            self.reset_ball(direction=1)
        elif self.ball_x > self.width:
            self.player_score += 1
            self.reset_ball(direction=-1)

        self.score_text.set(f"Du {self.player_score} : {self.bot_score} Bot")
        self.draw()
        self.after(16, self.update_loop)

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_line(self.width / 2, 0, self.width / 2, self.height, fill="#334", dash=(6, 8))
        self.canvas.create_rectangle(20, self.player_y - self.paddle_h / 2, 40, self.player_y + self.paddle_h / 2, fill="#4ade80", width=0)
        self.canvas.create_rectangle(self.width - 40, self.bot_y - self.paddle_h / 2, self.width - 20, self.bot_y + self.paddle_h / 2, fill="#f97316", width=0)
        self.canvas.create_oval(self.ball_x - 8, self.ball_y - 8, self.ball_x + 8, self.ball_y + 8, fill="#f8fafc", width=0)


class BattleshipGame(ttk.Frame):
    def __init__(self, master, get_diff):
        super().__init__(master, padding=10)
        self.ships = set(random.sample(range(36), 5))
        self.shots = set()
        self.hit_count = 0
        self.status = tk.StringVar(value="Treffer: 0/5")

        ttk.Label(self, text="Schiffe versenken", font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(self, textvariable=self.status).pack(pady=(4, 8))

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack()
        self.buttons = []
        for r in range(6):
            row = []
            for c in range(6):
                idx = r * 6 + c
                b = tk.Button(self.grid_frame, text="~", width=3, command=lambda i=idx: self.fire(i))
                b.grid(row=r, column=c, padx=1, pady=1)
                row.append(b)
            self.buttons.append(row)

    def fire(self, idx):
        if idx in self.shots:
            return
        self.shots.add(idx)
        r, c = divmod(idx, 6)
        if idx in self.ships:
            self.hit_count += 1
            self.buttons[r][c].config(text="X", bg="#e85")
        else:
            self.buttons[r][c].config(text="•", bg="#aaa")
        self.status.set(f"Treffer: {self.hit_count}/5")


class TicTacToeGame(ttk.Frame):
    WIN_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]

    def __init__(self, master, get_diff):
        super().__init__(master, padding=10)
        self.get_diff = get_diff
        self.board = [""] * 9
        self.status = tk.StringVar(value="Du bist X")

        ttk.Label(self, text="TicTacToe", font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(self, textvariable=self.status).pack(pady=(4, 8))

        g = ttk.Frame(self)
        g.pack()
        self.cells = []
        for i in range(9):
            btn = tk.Button(g, text=" ", width=5, height=2, command=lambda idx=i: self.play(idx))
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.cells.append(btn)

    def play(self, idx):
        if self.board[idx] or self.winner():
            return
        self.board[idx] = "X"
        self.refresh()
        if self.winner() or all(self.board):
            self.finish_status()
            return

        free = [i for i, v in enumerate(self.board) if not v]
        diff = self.get_diff()
        bot_idx = random.choice(free) if random.random() < diff.skill else free[0]
        self.board[bot_idx] = "O"
        self.refresh()
        self.finish_status()

    def winner(self):
        for a, b, c in self.WIN_LINES:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def finish_status(self):
        w = self.winner()
        if w:
            self.status.set(f"Gewinner: {w}")
        elif all(self.board):
            self.status.set("Unentschieden")

    def refresh(self):
        for i, btn in enumerate(self.cells):
            btn.config(text=self.board[i] if self.board[i] else " ")


class RacingGame(ttk.Frame):
    def __init__(self, master, get_diff):
        super().__init__(master, padding=12)
        ttk.Label(self, text="Rennspiel (MVP)", font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(self, text="Dieses Game bleibt aktuell ein MVP-Mode.").pack(pady=8)


class TankGame(ttk.Frame):
    def __init__(self, master, get_diff):
        super().__init__(master, padding=8)
        self.get_diff = get_diff
        self.width, self.height = 760, 360
        self.ground_y = 300

        self.player_x = 120
        self.enemy_x = 640
        self.player_hp = 100
        self.enemy_hp = 100

        self.angle = 45
        self.power = 18
        self.projectile = None
        self.enemy_cooldown = 0
        self.keys = set()

        ttk.Label(self, text="Tank Battle (echt steuerbar)", font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(self, text="A/D bewegen | ←/→ Winkel | ↑/↓ Power | Space schießen", foreground="#666").pack(pady=(0, 6))

        self.status = tk.StringVar(value="Bereit")
        self.hp_text = tk.StringVar(value="Du 100 HP | Gegner 100 HP")
        ttk.Label(self, textvariable=self.hp_text).pack()
        ttk.Label(self, textvariable=self.status).pack()

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="#87CEEB", highlightthickness=0)
        self.canvas.pack(pady=6)

        self.bind_all("<KeyPress>", self.on_key_down)
        self.bind_all("<KeyRelease>", self.on_key_up)
        self.loop()

    def on_key_down(self, e):
        self.keys.add(e.keysym)

    def on_key_up(self, e):
        self.keys.discard(e.keysym)

    def fire(self, start_x, start_y, angle_deg, speed, owner):
        rad = math.radians(angle_deg)
        self.projectile = {
            "x": start_x,
            "y": start_y,
            "vx": math.cos(rad) * speed,
            "vy": -math.sin(rad) * speed,
            "owner": owner,
        }

    def handle_controls(self):
        if "a" in {k.lower() for k in self.keys}:
            self.player_x = max(50, self.player_x - 4)
        if "d" in {k.lower() for k in self.keys}:
            self.player_x = min(self.width - 200, self.player_x + 4)
        if "Left" in self.keys:
            self.angle = max(10, self.angle - 1)
        if "Right" in self.keys:
            self.angle = min(80, self.angle + 1)
        if "Up" in self.keys:
            self.power = min(30, self.power + 0.2)
        if "Down" in self.keys:
            self.power = max(8, self.power - 0.2)
        if "space" in {k.lower() for k in self.keys} and self.projectile is None and self.player_hp > 0 and self.enemy_hp > 0:
            self.fire(self.player_x + 30, self.ground_y - 18, self.angle, self.power, "player")
            self.status.set("Du hast geschossen")

    def update_projectile(self):
        if not self.projectile:
            return
        p = self.projectile
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.35

        if p["owner"] == "player" and abs(p["x"] - self.enemy_x) < 25 and abs(p["y"] - (self.ground_y - 15)) < 20:
            dmg = random.randint(14, 28)
            self.enemy_hp = max(0, self.enemy_hp - dmg)
            self.status.set(f"Treffer! Gegner -{dmg} HP")
            self.projectile = None
        elif p["owner"] == "enemy" and abs(p["x"] - self.player_x) < 25 and abs(p["y"] - (self.ground_y - 15)) < 20:
            dmg = random.randint(10, 24)
            self.player_hp = max(0, self.player_hp - dmg)
            self.status.set(f"Du wurdest getroffen (-{dmg})")
            self.projectile = None
        elif p["y"] > self.ground_y or p["x"] < 0 or p["x"] > self.width:
            self.projectile = None

    def enemy_ai(self):
        if self.projectile or self.enemy_hp <= 0 or self.player_hp <= 0:
            return
        self.enemy_cooldown += 1
        if self.enemy_cooldown < int(90 - self.get_diff().skill * 55):
            return
        self.enemy_cooldown = 0

        dx = max(50, self.enemy_x - self.player_x)
        base_angle = 45
        skill = self.get_diff().skill
        angle_noise = int((1 - skill) * random.randint(-20, 20))
        speed = math.sqrt(dx * 0.35)
        speed = max(10, min(28, speed))
        speed += random.uniform(-(1 - skill) * 6, (1 - skill) * 6)
        self.fire(self.enemy_x - 30, self.ground_y - 18, 180 - (base_angle + angle_noise), speed, "enemy")

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, self.ground_y, self.width, self.height, fill="#2e7d32", width=0)

        self.canvas.create_rectangle(self.player_x - 20, self.ground_y - 15, self.player_x + 20, self.ground_y, fill="#374151", width=0)
        self.canvas.create_rectangle(self.player_x - 14, self.ground_y - 28, self.player_x + 14, self.ground_y - 15, fill="#16a34a", width=0)
        p_rad = math.radians(self.angle)
        self.canvas.create_line(
            self.player_x,
            self.ground_y - 23,
            self.player_x + math.cos(p_rad) * 26,
            self.ground_y - 23 - math.sin(p_rad) * 26,
            fill="#111",
            width=4,
        )

        self.canvas.create_rectangle(self.enemy_x - 20, self.ground_y - 15, self.enemy_x + 20, self.ground_y, fill="#374151", width=0)
        self.canvas.create_rectangle(self.enemy_x - 14, self.ground_y - 28, self.enemy_x + 14, self.ground_y - 15, fill="#ef4444", width=0)
        self.canvas.create_line(self.enemy_x, self.ground_y - 23, self.enemy_x - 24, self.ground_y - 30, fill="#111", width=4)

        if self.projectile:
            p = self.projectile
            self.canvas.create_oval(p["x"] - 4, p["y"] - 4, p["x"] + 4, p["y"] + 4, fill="#111", width=0)

        self.canvas.create_text(130, 20, text=f"Winkel: {int(self.angle)}°  Power: {int(self.power)}", font=("Segoe UI", 10, "bold"))

    def loop(self):
        if self.player_hp > 0 and self.enemy_hp > 0:
            self.handle_controls()
            self.enemy_ai()
            self.update_projectile()
        elif self.enemy_hp <= 0:
            self.status.set("Sieg! Gegner zerstört")
        elif self.player_hp <= 0:
            self.status.set("Niederlage! Dein Tank ist zerstört")

        self.hp_text.set(f"Du {self.player_hp} HP | Gegner {self.enemy_hp} HP")
        self.draw()
        self.after(16, self.loop)


class PlatformerGame(ttk.Frame):
    def __init__(self, master, get_diff):
        super().__init__(master, padding=8)
        self.width, self.height = 760, 360
        self.world_w = 2200
        self.gravity = 0.8
        self.keys = set()

        ttk.Label(self, text="Parkour / Mario-Style (Level)", font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(self, text="A/D laufen, Space springen – Ziel ist die Flagge rechts", foreground="#666").pack(pady=(0, 6))

        self.state = tk.StringVar(value="Coins: 0")
        ttk.Label(self, textvariable=self.state).pack()

        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="#7dd3fc", highlightthickness=0)
        self.canvas.pack()

        self.player = {"x": 40.0, "y": 240.0, "vx": 0.0, "vy": 0.0, "w": 24, "h": 30, "on_ground": False}
        self.camera_x = 0
        self.coins = 0
        self.game_over = False
        self.win = False

        self.platforms = [
            (0, 300, 500, 60), (560, 300, 260, 60), (900, 300, 320, 60), (1300, 300, 320, 60), (1720, 300, 480, 60),
            (280, 230, 100, 16), (700, 220, 120, 16), (1140, 200, 120, 16), (1540, 240, 100, 16),
        ]
        self.hazards = [(520, 300, 30, 30), (1240, 300, 30, 30), (1680, 300, 30, 30)]
        self.coin_positions = [[330, 200, True], [730, 190, True], [1170, 170, True], [1580, 210, True], [1890, 270, True]]
        self.goal_x = 2120

        self.bind_all("<KeyPress>", self.on_key_down)
        self.bind_all("<KeyRelease>", self.on_key_up)
        self.loop()

    def on_key_down(self, e):
        self.keys.add(e.keysym)

    def on_key_up(self, e):
        self.keys.discard(e.keysym)

    def intersects(self, a, b):
        ax, ay, aw, ah = a
        bx, by, bw, bh = b
        return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

    def update_player(self):
        if self.game_over:
            return

        left = "a" in {k.lower() for k in self.keys}
        right = "d" in {k.lower() for k in self.keys}
        jump = "space" in {k.lower() for k in self.keys}

        if left and not right:
            self.player["vx"] = -4
        elif right and not left:
            self.player["vx"] = 4
        else:
            self.player["vx"] *= 0.75

        if jump and self.player["on_ground"]:
            self.player["vy"] = -13
            self.player["on_ground"] = False

        self.player["vy"] += self.gravity

        self.player["x"] += self.player["vx"]
        self.player["x"] = max(0, min(self.world_w - self.player["w"], self.player["x"]))

        self.player["y"] += self.player["vy"]
        self.player["on_ground"] = False

        p_rect = [self.player["x"], self.player["y"], self.player["w"], self.player["h"]]
        for x, y, w, h in self.platforms:
            plat = [x, y, w, h]
            if self.intersects(p_rect, plat) and self.player["vy"] >= 0 and self.player["y"] + self.player["h"] - self.player["vy"] <= y + 6:
                self.player["y"] = y - self.player["h"]
                self.player["vy"] = 0
                self.player["on_ground"] = True
                p_rect = [self.player["x"], self.player["y"], self.player["w"], self.player["h"]]

        for hz in self.hazards:
            if self.intersects(p_rect, hz):
                self.game_over = True
                self.state.set("Game Over – mit R neu starten")

        for c in self.coin_positions:
            if c[2] and self.intersects(p_rect, [c[0] - 8, c[1] - 8, 16, 16]):
                c[2] = False
                self.coins += 1

        if self.player["x"] >= self.goal_x:
            self.win = True
            self.game_over = True
            self.state.set(f"Level geschafft! Coins: {self.coins} – mit R neu starten")

        if "r" in {k.lower() for k in self.keys} and self.game_over:
            self.reset()

        self.camera_x = int(max(0, min(self.world_w - self.width, self.player["x"] - 240)))
        if not self.game_over:
            self.state.set(f"Coins: {self.coins}")

    def reset(self):
        self.player = {"x": 40.0, "y": 240.0, "vx": 0.0, "vy": 0.0, "w": 24, "h": 30, "on_ground": False}
        self.coins = 0
        self.game_over = False
        self.win = False
        self.coin_positions = [[330, 200, True], [730, 190, True], [1170, 170, True], [1580, 210, True], [1890, 270, True]]

    def draw(self):
        self.canvas.delete("all")
        offset = self.camera_x

        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#7dd3fc", width=0)

        for x, y, w, h in self.platforms:
            self.canvas.create_rectangle(x - offset, y, x + w - offset, y + h, fill="#654321", width=0)

        for x, y, w, h in self.hazards:
            self.canvas.create_polygon(x - offset, y + h, x + w / 2 - offset, y, x + w - offset, y + h, fill="#ef4444", outline="")

        for x, y, alive in self.coin_positions:
            if alive:
                self.canvas.create_oval(x - 8 - offset, y - 8, x + 8 - offset, y + 8, fill="#facc15", width=0)

        self.canvas.create_rectangle(self.goal_x - offset, 220, self.goal_x + 8 - offset, 300, fill="#111", width=0)
        self.canvas.create_rectangle(self.goal_x + 8 - offset, 220, self.goal_x + 36 - offset, 240, fill="#22c55e", width=0)

        px, py = self.player["x"] - offset, self.player["y"]
        self.canvas.create_rectangle(px, py, px + self.player["w"], py + self.player["h"], fill="#2563eb", width=0)

        if self.game_over:
            msg = "LEVEL GESCHAFFT" if self.win else "GAME OVER"
            self.canvas.create_text(self.width / 2, 90, text=msg, font=("Segoe UI", 24, "bold"), fill="#fff")

    def loop(self):
        self.update_player()
        self.draw()
        self.after(16, self.loop)


class MemoryGame(ttk.Frame):
    def __init__(self, master, get_diff):
        super().__init__(master, padding=12)
        self.symbols = ["🐶", "🐱", "🦊", "🐼", "🐸", "🐵"] * 2
        random.shuffle(self.symbols)
        self.revealed = []
        self.matched = set()

        ttk.Label(self, text="Memory", font=("Segoe UI", 14, "bold")).pack()
        self.grid = ttk.Frame(self)
        self.grid.pack(pady=8)
        self.buttons = []
        for i in range(12):
            b = tk.Button(self.grid, text="?", width=4, command=lambda idx=i: self.flip(idx))
            b.grid(row=i // 4, column=i % 4, padx=3, pady=3)
            self.buttons.append(b)

    def flip(self, idx):
        if idx in self.matched or idx in self.revealed:
            return
        self.revealed.append(idx)
        self.buttons[idx].config(text=self.symbols[idx])
        if len(self.revealed) == 2:
            a, b = self.revealed
            if self.symbols[a] == self.symbols[b]:
                self.matched.update(self.revealed)
                self.revealed.clear()
            else:
                self.after(500, self.hide_unmatched)

    def hide_unmatched(self):
        for idx in self.revealed:
            self.buttons[idx].config(text="?")
        self.revealed.clear()


class CodeBreakerGame(ttk.Frame):
    def __init__(self, master, get_diff):
        super().__init__(master, padding=12)
        self.secret = random.randint(100, 999)

        ttk.Label(self, text="Code-Knacker", font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(self, text="Rate den 3-stelligen Code").pack(pady=(6, 4))

        row = ttk.Frame(self)
        row.pack()
        self.input = ttk.Entry(row, width=10)
        self.input.pack(side=tk.LEFT, padx=6)
        ttk.Button(row, text="Prüfen", command=self.guess).pack(side=tk.LEFT)

        self.log = tk.Text(self, width=34, height=10)
        self.log.pack(pady=8)

    def guess(self):
        value = self.input.get().strip()
        self.input.delete(0, tk.END)
        if not value.isdigit() or len(value) != 3:
            self.log.insert(tk.END, "Ungültige Eingabe\n")
            return
        val = int(value)
        if val == self.secret:
            self.log.insert(tk.END, f"✅ Treffer! ({self.secret})\n")
            self.secret = random.randint(100, 999)
        elif val < self.secret:
            self.log.insert(tk.END, f"⬆️ Höher als {val}\n")
        else:
            self.log.insert(tk.END, f"⬇️ Niedriger als {val}\n")


def run():
    root = tk.Tk()
    root.title("Offline Arcade - Windows")
    root.geometry("980x760")

    def show_hub():
        lock.pack_forget()
        hub = ArcadeHub(root)
        hub.pack(fill=tk.BOTH, expand=True)

    lock = LockScreen(root, show_hub)
    lock.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    run()
