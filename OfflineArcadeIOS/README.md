# Offline Arcade iOS (Konzept + SwiftUI-MVP)

Dieses Projekt ist ein **offline-fähiger Spiele-Hub** für iOS mit mehreren Mini-Games und optionalem lokalem Multiplayer.

## Enthaltene Spiele (MVP)

1. Fußball-Duell (Penalty)
2. Tischtennis (Reflex/Pong-ähnlich)
3. Schiffe versenken (gegen Bot)
4. TicTacToe (gegen Bot)
5. Rennspiel (Lane-Runner)
6. Panzerkampf (Tank vs Tank)
7. Parkour (Mario-ähnliches Side-Runner-Prinzip)
8. Extra: Memory
9. Extra: Zahlencode-Knacker

## Anforderungen aus dem Auftrag

- Offline-Betrieb: Alle Kernmechaniken laufen lokal.
- Bot-Gegner mit Stufen: leicht, mittel, schwer, sehr schwer.
- Multiplayer in manchen Spielen:
  - TicTacToe: lokal 2 Spieler
  - Panzerkampf: lokaler Multiplayer-Stub vorbereitet
  - Tischtennis: lokaler Multiplayer-Stub vorbereitet
- App soll nicht öffentlich für jeden aufrufbar sein:
  - Sperrbildschirm mit Face ID / Touch ID (wenn möglich)
  - PIN-Backup

## Technischer Aufbau

- `App/`: Einstiegspunkt
- `Models/`: Datenmodelle und Schwierigkeitsgrade
- `Security/`: Zugriffsschutz
- `Services/`: Bot-Logik und Multiplayer-Stub
- `Views/`: Hub, Lock-Screen, Spiele-Screens

## Nächste Schritte

1. Xcode-Projekt erstellen und Ordner einhängen.
2. Assets/Audio ergänzen.
3. Kollisionen/Physik mit SpriteKit erweitern (Racing, Parkour, Tank).
4. Echten Multiplayer mit `MultipeerConnectivity` finalisieren.
5. Elternmodus/Admin-PIN für Jugendschutz hinzufügen.

## Installation

Eine vollständige Schritt-für-Schritt-Anleitung für iOS und Windows findest du in:

- `INSTALLATION_DE.md`
