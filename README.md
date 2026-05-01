# Fireflies Transcript Downloader

Download meeting transcripts from [Fireflies.ai](https://fireflies.ai) as formatted `.docx` files — with no timestamps, grouped by speaker, and automatically named by date.

Comes in two flavours: a **GUI app** for ongoing use, and a **batch script** for one-off bulk downloads.

![Fireflies Downloader icon](fireflies_icon_1024.png)

---

## Features

- Downloads transcripts as clean `.docx` files (speaker names only — no timestamps)
- Names files automatically: `YYYY-MM-DD Meeting Title.docx`
- **GUI app** with date range picker, progress bar, and live log
- Remembers the last downloaded transcript so you always pick up where you left off
- Auto-sets the "From" date to the day after your last download
- Validates date ranges before downloading
- macOS `.app` wrapper for double-click launching from Launchpad or Dock
- Auto-installs Python dependencies on first run

---

## Requirements

- macOS (tested on Ventura/Sonoma/Sequoia)
- Python 3.9+ (Homebrew or system)
- A [Fireflies.ai](https://fireflies.ai) account with API access

---

## Getting Your API Key

1. Log in to [app.fireflies.ai](https://app.fireflies.ai)
2. Go to **Settings → Developer settings**
3. Copy your API key

---

## Installation

Clone or download this repo:

```bash
git clone https://github.com/Joshthejuggler/fireflies-transcript-downloader.git
cd fireflies-transcript-downloader
```

Dependencies are installed automatically on first run (`requests`, `python-docx`, `customtkinter`).

---

## Usage

### GUI App (recommended)

```bash
python3 fireflies_downloader.py
```

On first launch:
1. Paste your API key into the **API Key** field
2. Set your **Save folder**
3. Choose a **date range** (or check "Auto-set From" to continue from your last download)
4. Click **Download Transcripts**

State is saved automatically to `fireflies_state.json` in the same directory — your API key, output folder, and last downloaded date are remembered between sessions.

### Batch Script (bulk one-off download)

Edit the `API_KEY` and `TO_DATE` variables at the top of `download_fireflies.py`, then run:

```bash
python3 download_fireflies.py
```

This downloads all transcripts up to the specified date and saves them to the same directory as the script.

---

## Add to macOS Applications

To create a double-clickable app in `/Applications`:

```bash
printf 'set pyScript to "%s"\ndo shell script "/opt/homebrew/bin/python3 " & quoted form of pyScript & " > /tmp/fireflies.log 2>&1 &"' \
  "$(pwd)/fireflies_downloader.py" | osacompile -o "/Applications/Fireflies Downloader.app"
```

### Apply the custom icon

```bash
ICON_SRC="$(pwd)/fireflies_icon_1024.png"
ICONSET="/tmp/Fireflies.iconset"
APP="/Applications/Fireflies Downloader.app"
mkdir -p "$ICONSET"
for size in 16 32 64 128 256 512; do
  sips -z $size $size "$ICON_SRC" --out "$ICONSET/icon_${size}x${size}.png" > /dev/null 2>&1
  sips -z $((size*2)) $((size*2)) "$ICON_SRC" --out "$ICONSET/icon_${size}x${size}@2x.png" > /dev/null 2>&1
done
iconutil -c icns "$ICONSET" -o /tmp/Fireflies.icns
cp /tmp/Fireflies.icns "$APP/Contents/Resources/applet.icns"
touch "$APP"
```

You may need to relaunch Finder for the icon to appear in Launchpad.

---

## File Structure

```
fireflies-transcript-downloader/
├── fireflies_downloader.py       # GUI app (customtkinter)
├── download_fireflies.py         # Batch download script
├── Open Fireflies Downloader.command  # Double-click launcher (after chmod +x)
├── make_icon.py                  # Generates the app icon (Pillow)
├── fireflies_icon_1024.png       # App icon source image
└── fireflies_state.json          # Auto-generated — saves your last run state
```

---

## Output Format

Each `.docx` file contains:
- **Meeting title** as heading
- **Date and duration** as subtitle
- **Transcript body** grouped by speaker turn — no timestamps

Example filename: `2026-03-30 GPC Data Discussions.docx`

---

## Notes

- The Fireflies API returns a maximum of 50 transcripts per request. For date ranges with more than 50 meetings, use multiple smaller ranges.
- `fireflies_state.json` contains your API key in plain text. Keep the folder private or remove the key before sharing.
- The `.command` launcher file requires `chmod +x` once before it can be double-clicked.

---

## License

MIT
