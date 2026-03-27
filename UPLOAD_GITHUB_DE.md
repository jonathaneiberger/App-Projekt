# Direkt richtig zu GitHub hochladen (ohne Chaos)

Diese Anleitung ist auf **einfach und sicher** getrimmt.

## A) Erstes Hochladen (neues GitHub-Repo)

1. Erstelle ein leeres Repo auf GitHub (ohne README/License/.gitignore).
2. Öffne Terminal im Projektordner.
3. Führe aus:

```bash
./scripts/github_first_push.sh <DEIN_GITHUB_REPO_URL>
```

Beispiel:

```bash
./scripts/github_first_push.sh git@github.com:deinuser/offline-arcade.git
```

Auf Windows (cmd):

```bat
scripts\github_first_push.bat https://github.com/deinuser/offline-arcade.git
```

---

## B) Spätere Updates (ohne Merge-Konflikt-Chaos)

Vor jedem Push:

```bash
./scripts/github_update_push.sh
```

Auf Windows (cmd):

```bat
scripts\github_update_push.bat
```

Die Scripts machen automatisch:
- `git fetch`
- `git pull --rebase`
- `git push`

Dadurch bleibt die Historie sauber und Konflikte werden reduziert.

---

## C) Falls doch Konflikte auftauchen

1. Konflikt-Dateien öffnen.
2. Marker `<<<<<<<`, `=======`, `>>>>>>>` auflösen.
3. Dann:

```bash
git add <dateien>
git rebase --continue
git push
```

---

## D) Wichtiger Hinweis

Eine `.gitignore` ist im Projekt vorhanden, damit Cache-/Build-Dateien (z. B. `__pycache__`) nicht mehr versehentlich hochgeladen werden.
