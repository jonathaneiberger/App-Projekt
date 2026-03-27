# Installationsanleitung (iOS + Windows)

## 1) iOS installieren (Xcode)

> Voraussetzung: macOS + Xcode (aktuelle Version), Apple-ID für Signierung.

### Schritt-für-Schritt

1. **Projekt holen**
   ```bash
   git clone <DEIN_REPO_URL>
   cd App-Projekt
   ```
2. **Xcode-Projekt anlegen**
   - Xcode öffnen → *Create a new Xcode Project* → *App (iOS)*.
   - Name z. B. `OfflineArcadeIOSApp`.
3. **Dateien einbinden**
   - Ordner `OfflineArcadeIOS/` in den Xcode-Projektnavigator ziehen.
   - Option *Copy items if needed* aktivieren.
   - Sicherstellen, dass alle Dateien im iOS-Target angehakt sind.
4. **Signing konfigurieren**
   - Projekt auswählen → *Signing & Capabilities*.
   - Team auswählen (deine Apple-ID / Developer-Team).
   - Bundle Identifier eindeutig setzen, z. B. `de.deinname.offlinearcade`.
5. **Berechtigungen/Capabilities**
   - Für Biometrie den Zugriff über `LocalAuthentication` nutzen (ist im Code schon vorbereitet).
   - Optional: Info.plist-Texte für Auth-Hinweise ergänzen.
6. **Auf iPhone installieren**
   - iPhone per Kabel verbinden.
   - In Xcode dein Gerät als Run Destination wählen.
   - **Run (▶)** klicken.
   - Auf dem iPhone ggf. „Entwickler vertrauen“ bestätigen.
7. **App starten**
   - Beim Start erscheint der Lock-Screen.
   - MVP-PIN ist aktuell: `2907`.

### Troubleshooting iOS

- **`no such module SwiftUI`**: Passiert auf Linux/Windows-CLI; für iOS immer in Xcode auf macOS bauen.
- **Signing-Fehler**: Team/Bundel-ID prüfen, ggf. automatisch verwalten lassen.
- **App startet nicht auf Gerät**: Entwickler-Modus auf dem iPhone aktivieren und Zertifikat vertrauen.

---

## 2) Windows installieren (Notebook/Desktop)

> Voraussetzung: Windows 10/11 + Python 3.10+.

### Schritt-für-Schritt

1. **Projekt holen**
   ```powershell
   git clone <DEIN_REPO_URL>
   cd App-Projekt
   ```
2. **Python prüfen**
   ```powershell
   python --version
   ```
3. **App starten**
   ```powershell
   python OfflineArcadeWindows\app.py
   ```
4. **Login in der App**
   - Lock-Screen öffnet sich.
   - MVP-PIN eingeben: `2907`.
5. **Spiele spielen**
   - Im Tab-Hub Spiel auswählen.
   - Schwierigkeit oben im Hub einstellen.

### Optional: EXE bauen

1. PyInstaller installieren:
   ```powershell
   pip install pyinstaller
   ```
2. EXE erstellen:
   ```powershell
   pyinstaller --noconfirm --onefile --windowed OfflineArcadeWindows\app.py
   ```
3. Ergebnis liegt danach unter `dist\app.exe`.

### Troubleshooting Windows

- **`python` nicht gefunden**: Python neu installieren und „Add Python to PATH“ aktivieren.
- **Tkinter fehlt**: Standardmäßig bei normaler Python-Installation enthalten; ggf. Python reparieren.
- **SmartScreen-Warnung bei EXE**: Bei nicht signierten lokalen Builds normal.

---

## Sicherheitshinweis (wichtig)

Die PIN `2907` ist nur ein MVP-Default. Für echten Einsatz:
- PIN nicht im Klartext im Code lassen,
- sichere Speicherung nutzen (iOS Keychain / Windows Credential Locker),
- ggf. Admin-Modus für PIN-Änderung ergänzen.

---

## GitHub Upload (einfach)

Für den korrekten direkten Upload nutze:

- `UPLOAD_GITHUB_DE.md`
- `scripts/github_first_push.sh` / `scripts/github_first_push.bat`
- `scripts/github_update_push.sh` / `scripts/github_update_push.bat`

---

## 3D-Komplettversion (Godot)

Wenn du die komplett überarbeitete 3D-Version möchtest, nutze `OfflineArcade3D/README.md`.
- Export-Presets: `OfflineArcade3D/export_presets.cfg`
- Realismus-Asset-Plan: `OfflineArcade3D/ASSET_PIPELINE.md`
