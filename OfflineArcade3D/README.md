# Offline Arcade 3D (Komplett-Überarbeitung)

Diese Version ist ein **3D-Neustart** auf Basis von **Godot 4**.

## Enthaltene 3D-Spiele (spielbar)

1. **3D Tischtennis** – beweglicher Schläger, Ballphysik, Bot-Paddle, HUD, Pause
2. **3D Tank Battle** – sichtbare Tanks, Aim/Schuss, HP, HUD, Pause
3. **3D Parkour** – Mario-ähnlicher 3D-Level, Coins, Ziel, HUD, Pause

## Zugriffsschutz

Im Hauptmenü wird eine PIN geprüft (MVP: `2907`) bevor Spiele gestartet werden.

## Steuerung

- Allgemein: `ESC` zurück ins Menü, `P` pausieren, `O` fortsetzen
- Tischtennis: `W/S` (vor/zurück)
- Tank: `A/D` (strafe), `W/S` (Turret drehen), Linksklick schießen
- Parkour: `WASD` bewegen, `Space` springen

## Starten

1. Godot 4 installieren
2. Godot öffnen -> Import -> `OfflineArcade3D/project.godot`
3. Play drücken

## Export (Windows + iOS)

- Vorbereitete Preset-Datei: `OfflineArcade3D/export_presets.cfg`
- Asset/Realismus-Upgrade-Plan: `OfflineArcade3D/ASSET_PIPELINE.md`
