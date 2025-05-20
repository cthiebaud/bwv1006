#!/bin/bash

LOGFILE="debug.txt"
> "$LOGFILE"  # clear existing log

echo ">>> $(date '+%Y-%m-%d %H:%M:%S') Cleaning up old files" | tee -a "$LOGFILE"
rm -vf \
  bwv1006_csv_midi_note_events.csv \
  bwv1006_csv_svg_note_heads.csv   \
  bwv1006_json_notes.json          \
  bwv1006_ly_one_line.svg          \
  bwv1006_ly_one_line.midi         \
  bwv1006.pdf                      \
  bwv1006.svg | tee -a "$LOGFILE"

logrun() {
  echo "\\n>>> $(date '+%Y-%m-%d %H:%M:%S') $*" | tee -a "$LOGFILE"
  "$@" 2>&1 | tee -a "$LOGFILE"
}

# LilyPond PDF
logrun docker run -v "$(pwd):/work" codello/lilypond:dev bwv1006.ly

# LilyPond SVG (main)
logrun docker run -v "$(pwd):/work" codello/lilypond:dev --svg bwv1006.ly

# remove hrefs in tabs 
logrun python3 scripts/svg_remove_hrefs_in_tabs.py

# LilyPond SVG (one-line)
logrun docker run -v "$(pwd):/work" codello/lilypond:dev --svg bwv1006_ly_one_line.ly

# Python processing scripts
logrun python3 scripts/midi_map.py
logrun python3 scripts/svg_extract_note_heads.py
logrun python3 scripts/align_pitch_by_geometry_simplified.py
