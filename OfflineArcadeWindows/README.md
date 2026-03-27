# Offline Arcade für Windows Notebook

Diese Version ergänzt das iOS-Konzept um eine **Windows-Desktop-App** (Tkinter), die offline läuft.

## Features

- Zugriffsschutz per PIN beim Start (`2907` als MVP-Default).
- Bot-Schwierigkeiten: Leicht, Mittel, Schwer, Sehr schwer.
- Mehrere Spiele in einem Hub (Tab-Navigation).
- **Echt spielbare Modi mit Steuerung und Visualisierung**:
  - Tischtennis: bewegbarer Schläger (↑/↓), sichtbarer Ball, Bot-Gegner.
  - Tank Battle: sichtbare Tanks, Bewegung, Winkel/Power und Projektil-Schuss.
  - Parkour/Mario-Style: Level mit Plattformen, Sprüngen, Coins, Gefahren und Ziel-Flagge.
- Weitere Mini-Games als Arcade-MVP: Fußball, Schiffe versenken, TicTacToe, Memory, Code-Knacker.

## Start

```bash
python3 OfflineArcadeWindows/app.py
```

## Wichtige Steuerung

- Tischtennis: `↑` / `↓`
- Tank: `A` / `D` bewegen, `←` / `→` Winkel, `↑` / `↓` Power, `Space` schießen
- Parkour: `A` / `D` laufen, `Space` springen, `R` Neustart nach Game Over

## Installation (detailliert)

Eine ausführliche Anleitung (inkl. iOS + Windows + EXE-Build) findest du in:

- `INSTALLATION_DE.md`
