# 3D Asset Pipeline (Realismus-Upgrade)

## Ziel
Primitive Platzhalter durch echte 3D-Assets ersetzen:
- Tanks mit Turret-Animation
- Charakter mit Run/Jump-Animation
- Tischtennis-Umgebung + Materialien

## Empfohlene Formate
- `.glb` / `.gltf` für Modelle + Skeleton
- `.png` / `.jpg` für PBR Texturen
- `.wav` / `.ogg` für SFX/Musik

## Ordnerstruktur
- `assets/models/`
- `assets/textures/`
- `assets/audio/`

## Schritte
1. Assets in Godot importieren
2. Placeholder-Meshes in Scripts durch PackedScenes ersetzen
3. AnimationTree für Character/Tank anbinden
4. Particle-FX + AudioStreamPlayer für Treffer/Explosion/Coins ergänzen
