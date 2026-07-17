#!/bin/sh
# Rebuild the Radio Button Selection Frames pack from src/ using sdicons.
#
# Regenerate SVGs first if you edited colours/geometry:
#   python3 gen_frames.py
#
# sdicons is the generic Stream Deck icon-pack toolkit:
#   https://github.com/Beennnn/streamdeck-toolkit
# Resolution order for the toolkit entrypoint:
#   1. $SDICONS env var   2. `sdicons` on PATH   3. ../streamdeck-toolkit/bin/sdicons
set -e
ROOT="$(git rev-parse --show-toplevel)"

if [ -n "$SDICONS" ]; then
  SD="$SDICONS"
elif command -v sdicons >/dev/null 2>&1; then
  SD="sdicons"
elif [ -x "$ROOT/../streamdeck-toolkit/bin/sdicons" ]; then
  SD="$ROOT/../streamdeck-toolkit/bin/sdicons"
else
  echo "sdicons not found. Clone the toolkit next to this repo:" >&2
  echo "  git clone https://github.com/Beennnn/streamdeck-toolkit ../streamdeck-toolkit" >&2
  echo "or set SDICONS=/path/to/bin/sdicons" >&2
  exit 1
fi

# The repo root IS the pack folder (manifest.json + icons/ + icons.json here).
"$SD" build "$ROOT/src" "$ROOT" --out-dir "$ROOT/dist" --id com.beennnn.radioframes
echo "Built dist/com.beennnn.radioframes.streamDeckIconPack — submit-ready"
echo "(double-click to install, or upload to maker.elgato.com)."
