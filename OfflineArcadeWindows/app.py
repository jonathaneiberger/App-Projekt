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
        ttk.Label(
            self,
            text="Hinweis: Auf Windows kann man später Windows Hello (Biometrie) ergänzen.",
            foreground="#666",
        ).pack(pady=(6, 0))

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

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        games = [
            ("Fußball", SoccerGame),
            ("Tischtennis", TableTennisGame),
            ("Schiffe", BattleshipGame),
            ("TicTacToe", TicTacToeGame),
            ("Rennspiel", RacingGame),
            ("Tank", TankGame),
            ("Parkour", ParkourGame),
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

        ttk.Button(self, text="Reset", command=self.reset).pack(pady=10)

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

    def reset(self):
        self.score = 0
        self.rounds = 0
        self.info.set("Wähle Schussrichtung")
        self.stats.set("Tore: 0/0")


class TableTennisGame(ttk.Frame):
    def __init__(self, master, get_diff):
        super().__init__(master, padding=12)
        self.get_diff = get_diff
        self.player = 0
        self.bot = 0

        self.score = tk.StringVar(value="Du 0 : 0 Bot")
        self.mp_var = tk.BooleanVar(value=False)
        self.mp_text = tk.StringVar(value="Kein Multiplayer aktiv")

        ttk.Label(self, text="Tischtennis (Reflex)", font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(self, textvariable=self.score).pack(pady=(6, 8))
        ttk.Button(self, text="🏓 Return", command=self.rally).pack()
        ttk.Checkbutton(self, text="Lokaler Multiplayer", variable=self.mp_var, command=self.toggle_mp).pack(pady=10)
        ttk.Label(self, textvariable=self.mp_text, foreground="#666").pack()

    def rally(self):
        diff = self.get_diff()
        if random.random() > diff.skill:
            self.player += 1
        else:
            self.bot += 1
        self.score.set(f"Du {self.player} : {self.bot} Bot")

    def toggle_mp(self):
        if self.mp_var.get():
            self.mp_text.set("Lokaler Multiplayer vorbereitet (Stub)")
        else:
            self.mp_text.set("Kein Multiplayer aktiv")


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

        ttk.Button(self, text="Neue Runde", command=self.reset).pack(pady=8)

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
        if self.hit_count == 5:
            messagebox.showinfo("Gewonnen", "Alle Schiffe zerstört!")

    def reset(self):
        self.ships = set(random.sample(range(36), 5))
        self.shots.clear()
        self.hit_count = 0
        self.status.set("Treffer: 0/5")
        for row in self.buttons:
            for b in row:
                b.config(text="~", bg="SystemButtonFace")


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

        ttk.Button(self, text="Neu", command=self.reset).pack(pady=8)

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
        if random.random() < diff.skill:
            bot_idx = random.choice(free)
        else:
            bot_idx = free[0]
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
        else:
            self.status.set("Du bist X")

    def refresh(self):
        for i, btn in enumerate(self.cells):
            btn.config(text=self.board[i] if self.board[i] else " ")

    def reset(self):
        self.board = [""] * 9
        self.status.set("Du bist X")
        self.refresh()


class RacingGame(ttk.Frame):
    def __init__(self, master, get_diff):
        super().__init__(master, padding=12)
        self.lane = 1
        self.obstacle = random.randint(0, 2)
        self.distance = 0
        self.crashed = False

        ttk.Label(self, text="Rennspiel", font=("Segoe UI", 14, "bold")).pack()
        self.state = tk.StringVar(value="Distanz 0m")
        ttk.Label(self, textvariable=self.state).pack(pady=(4, 8))

        self.visual = tk.StringVar(value=self.render())
        ttk.Label(self, textvariable=self.visual, font=("Consolas", 12)).pack()

        ctrl = ttk.Frame(self)
        ctrl.pack(pady=8)
        ttk.Button(ctrl, text="←", command=lambda: self.move(-1)).pack(side=tk.LEFT, padx=6)
        ttk.Button(ctrl, text="Gas", command=self.tick).pack(side=tk.LEFT, padx=6)
        ttk.Button(ctrl, text="→", command=lambda: self.move(1)).pack(side=tk.LEFT, padx=6)

    def render(self):
        lanes = []
        for i in range(3):
            car = "🚗" if i == self.lane else "·"
            obs = "🧱" if i == self.obstacle else " "
            lanes.append(f"[{car}{obs}]")
        return " ".join(lanes)

    def move(self, d):
        if self.crashed:
            return
        self.lane = min(2, max(0, self.lane + d))
        self.visual.set(self.render())

    def tick(self):
        if self.crashed:
            return
        self.distance += 25
        if self.lane == self.obstacle:
            self.crashed = True
            self.state.set(f"💥 Crash bei {self.distance}m")
        else:
            self.state.set(f"Distanz {self.distance}m")
        self.obstacle = random.randint(0, 2)
        self.visual.set(self.render())


class TankGame(ttk.Frame):
    def __init__(self, master, get_diff):
        super().__init__(master, padding=12)
        self.get_diff = get_diff
        self.player_hp = 100
        self.bot_hp = 100
        self.status = tk.StringVar(value="Bereit")
        self.hp_view = tk.StringVar(value="Du 100 HP | Bot 100 HP")
        self.mp = tk.BooleanVar(value=False)

        ttk.Label(self, text="Tank Battle", font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(self, textvariable=self.hp_view).pack(pady=(4, 2))
        ttk.Label(self, textvariable=self.status).pack(pady=(0, 8))

        row = ttk.Frame(self)
        row.pack()
        ttk.Button(row, text="Schuss", command=lambda: self.attack(1.0)).pack(side=tk.LEFT, padx=6)
        ttk.Button(row, text="Rakete", command=lambda: self.attack(1.6)).pack(side=tk.LEFT, padx=6)

        ttk.Checkbutton(self, text="Lokaler Multiplayer (Stub)", variable=self.mp).pack(pady=8)

    def attack(self, mul):
        if self.player_hp <= 0 or self.bot_hp <= 0:
            return
        dmg = int(random.randint(10, 20) * mul)
        self.bot_hp = max(0, self.bot_hp - dmg)
        if self.bot_hp == 0:
            self.status.set("Du hast gewonnen!")
            self.hp_view.set(f"Du {self.player_hp} HP | Bot {self.bot_hp} HP")
            return

        bot_dmg = int(random.randint(8, 22) * self.get_diff().skill)
        self.player_hp = max(0, self.player_hp - bot_dmg)
        if self.player_hp == 0:
            self.status.set("Du wurdest zerstört")
        else:
            self.status.set(f"Du triffst {dmg}, Bot {bot_dmg}")
        self.hp_view.set(f"Du {self.player_hp} HP | Bot {self.bot_hp} HP")


class ParkourGame(ttk.Frame):
    def __init__(self, master, get_diff):
        super().__init__(master, padding=12)
        self.energy = 100
        self.coins = 0
        self.items = []
        self.state = tk.StringVar(value=self.text())

        ttk.Label(self, text="Parkour Dash", font=("Segoe UI", 14, "bold")).pack()
        ttk.Label(self, textvariable=self.state).pack(pady=(6, 10))

        row = ttk.Frame(self)
        row.pack()
        ttk.Button(row, text="Springen", command=lambda: self.act(0.7)).pack(side=tk.LEFT, padx=6)
        ttk.Button(row, text="Sliden", command=lambda: self.act(0.6)).pack(side=tk.LEFT, padx=6)
        ttk.Button(row, text="Item nutzen", command=self.use_item).pack(side=tk.LEFT, padx=6)

    def text(self):
        return f"Energie {self.energy} | Coins {self.coins} | Items {', '.join(self.items) if self.items else '-'}"

    def act(self, success):
        if random.random() < success:
            self.coins += random.randint(1, 4)
            if random.randint(0, 100) > 80:
                self.items.append(random.choice(["Medkit", "Coin-Magnet"]))
        else:
            self.energy = max(0, self.energy - random.randint(10, 24))
        self.state.set(self.text())

    def use_item(self):
        if not self.items:
            return
        item = self.items.pop(0)
        if item == "Medkit":
            self.energy = min(100, self.energy + 20)
        elif item == "Coin-Magnet":
            self.coins += 10
        self.state.set(self.text())


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
                if len(self.matched) == 12:
                    messagebox.showinfo("Memory", "Alle Paare gefunden!")
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
    root.geometry("900x700")

    def show_hub():
        lock.pack_forget()
        hub = ArcadeHub(root)
        hub.pack(fill=tk.BOTH, expand=True)

    lock = LockScreen(root, show_hub)
    lock.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    run()
