# CLAUDE.md — streamdeck-radio-frames

Project-specific rules. Global `~/.claude/CLAUDE.md` still applies (git
workflow, storage tiers, autonomy, French chat, etc.).

## What this is

A **content pack**: coloured selection frames + corner notches that mark the
active key in a Stream Deck radio-button group. Built with the generic
[sdicons](https://github.com/Beennnn/stream-deck-icons) toolkit (sibling repo
`../stream-deck-icons`). Sibling of `streamdeck-stage-keys` — same
pack-in-its-own-repo convention (own versioning, own Marketplace home, tool
stays lean).

## Layout

- `gen_frames.py` — the generator. Edit `COLOURS` (slug, Display Name, hex) or
  the geometry constants, then `python3 gen_frames.py` rewrites `src/*.svg` +
  `tags.json`. One SVG per colour per family: `frame-<colour>.svg` (full
  border) and `notch-<colour>.svg` (four corner brackets).
- `src/` — generated SVGs (committed, so the pack is reproducible).
- `manifest.json` / `icon.svg` / `license.txt` — pack identity (CC-BY-4.0).
- `tags.json` — per-icon Display Name + tags (generated). Names carry the
  words Benoît asked for: "Selected Frame" / "Selected Corner Notch".
- `bin/build.sh` — render → meta → contact → validate → package via sdicons.
- `dist/`, `contact-sheet.png`, `maker-media/` — gitignored (reproduce with
  `bin/build.sh`).

## Design intent (don't regress)

- **Transparent centre.** The icon is an OVERLAY behind the key title text; the
  centre must stay clear so white text keeps contrast on every colour. Never
  fill the centre with an opaque colour.
- **Dark halo under every stroke** (`stroke-opacity 0.38` black, wider) so the
  frame is visible on light key backgrounds too, not only black keys.
- **Bold edge = the whole signal.** Idle state = no frame; selected = frame.
  The pack ships only the "selected" images by design.
- Pack id is `com.beennnn.radioframes` (the `<id>.sdIconPack/` wrapper name).

## The radio-button state script (for the README + support)

Trevligaspel MIDI plugin, exclusive group `@radio:1`:

```text
[(@radio:1){state:0}]
[(release){state:1}]
[(press){state:1}{@radio:1}]
```

One key holds state 1 (frame shown) per group; pressing another clears it.
Different group id per independent set.

## Conventions

- Commits + README + docs in **English** (public GitHub repo). Chat FR.
- `validate` must stay green; never weaken it to "ship anyway".
- New colours: add to `COLOURS`, regenerate, rebuild, bump `manifest.json`
  Version. Keep `gen_frames.py` single-responsibility and < 1000 LOC.
