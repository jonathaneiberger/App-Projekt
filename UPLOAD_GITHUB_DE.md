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

---

## E) PR zeigt weiterhin Konflikte? (Auto-Fix)

Wenn GitHub weiterhin Konflikte zeigt (z. B. in `INSTALLATION_DE.md` oder `OfflineArcadeWindows/app.py`), nutze:

```bash
./scripts/fix_github_conflicts_keep_ours.sh main
```

Windows (cmd):

```bat
scripts\fix_github_conflicts_keep_ours.bat main
```

Das Script merged `origin/main` in deinen Branch und übernimmt bei bekannten Konfliktdateien automatisch **deine aktuelle Branch-Version** (`--ours`), committet und pusht.

---

## F) Garantiert konfliktfreier PR-Branch (Rebase + Force Push)

Wenn GitHub weiterhin „This branch has conflicts“ zeigt, nutze exakt diesen Ablauf:

```bash
./scripts/github_make_conflict_free_pr.sh <DEIN_GITHUB_REPO_URL> main work
```

Windows (cmd):

```bat
scripts\github_make_conflict_free_pr.bat <DEIN_GITHUB_REPO_URL> main work
```

Damit wird dein PR-Branch auf `origin/main` rebased und danach mit `--force-with-lease` gepusht.
Das entfernt den GitHub-Conflict-Status in der Regel zuverlässig.
