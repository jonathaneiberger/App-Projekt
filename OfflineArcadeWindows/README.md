# Offline Arcade für Windows Notebook

Diese Version ergänzt das iOS-Konzept um eine **Windows-Desktop-App** (Tkinter), die offline läuft.

## Features

- Zugriffsschutz per PIN beim Start (`2907` als MVP-Default).
- Bot-Schwierigkeiten: Leicht, Mittel, Schwer, Sehr schwer.
- Mehrere Spiele in einem Hub (Tab-Navigation):
  - Fußball-Duell
  - Tischtennis
  - Schiffe versenken
  - TicTacToe
  - Rennspiel
  - Tank Battle
  - Parkour Dash
  - Memory
  - Code-Knacker
- Lokaler Multiplayer-Stub in Spielen, wo sinnvoll (Tischtennis, Tank).

## Start

```bash
python3 OfflineArcadeWindows/app.py
```

## Hinweise

- Vollständig offline: keine Pflicht-Internetverbindung.
- Für produktive Nutzung sollte die PIN sicher gespeichert werden (z. B. Windows Credential Locker).
- Biometrie (Windows Hello) kann später ergänzt werden.

## Installation (detailliert)

Eine ausführliche Anleitung (inkl. iOS + Windows + EXE-Build) findest du in:

- `INSTALLATION_DE.md`
