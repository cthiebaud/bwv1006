#!/usr/bin/env python3
"""
align_pitch_by_geometry_simplified.py

Matches SVG noteheads with MIDI note events, accounting for ties,
and builds a simplified `bwv1006_json_notes.json` for SVG animation.
"""

import pandas as pd
import json

# --- Load Data ---
midi_df = pd.read_csv("bwv1006_csv_midi_note_events.csv")
svg_df = pd.read_csv("bwv1006_csv_svg_note_heads.csv")
ties_df = pd.read_csv("bwv1006_csv_ties.csv")

# --- Step 1: Normalize href paths (remove editor artifacts) ---
svg_df["href"] = (
    svg_df["href"]
    .str.replace("textedit://", "", regex=False)
    .str.replace("/work/", "", regex=False)
)

# --- Step 2: Filter out secondaries ---
secondary_hrefs = set(ties_df["secondary"])
## print(f"SVG before secondary removal: {len(svg_df)}")
svg_df = svg_df[~svg_df["href"].isin(secondary_hrefs)].copy()
## print(f"SVG after secondary removal: {len(svg_df)}")

# --- Step 3: Sort datasets ---
midi_df = midi_df.sort_values(by=["on", "channel", "pitch"], ascending=[True, False, True]).reset_index(drop=True)
svg_df = svg_df.sort_values(by=["x", "y"], ascending=[True, False]).reset_index(drop=True)

# --- Step 5: Pitch class mapping with extended accidentals ---
def parse_lilypond_note(note_str):
    """
    Convert LilyPond note notation to MIDI pitch value.
    
    LilyPond uses letter notation with modifiers for accidentals and octaves:
    - Base notes: c, d, e, f, g, a, b
    - Accidentals: is (sharp), es/s (flat), isis (double sharp), eses (double flat)
    - Octaves: ' (up one octave), , (down one octave)
    
    Args:
        note_str (str): LilyPond notation string (e.g., "cis'", "bes,,")
        
    Returns:
        int: Corresponding MIDI pitch value, or -1 if parsing failed
    """
    # Define base MIDI values for notes in the middle octave (C3 to B3)
    base_notes = {
        'c': 36, 'cis': 37, 'des': 37, 'd': 38, 'dis': 39, 'ees': 39, 'es': 39,
        'e': 40, 'f': 41, 'fis': 42, 'ges': 42, 'g': 43, 'gis': 44, 'aes': 44,
        'as': 44, 'a': 45, 'ais': 46, 'bes': 46, 'b': 47,
        
        # Less common accidentals
        'eis': 41, 'bis': 48, 'ces': 35, 'fes': 40,
        
        # Double accidentals
        'cisis': 38, 'disis': 40, 'eisis': 42, 'fisis': 43, 'gisis': 45,
        'aisis': 47, 'bisis': 49,
        'ceses': 34, 'deses': 36, 'eses': 38, 'feses': 39, 'geses': 41, 
        'aeses': 43, 'beses': 45
    }
    
    # Generate octave variations (commas for lower octaves)
    for i in range(1, 4):  # Add up to 3 octaves down
        for note in list(base_notes):
            key = f"{note}{',' * i}"  # Add commas for lower octaves
            value = base_notes[note] - i * 12  # Each octave is 12 semitones
            if value >= 0:  # Ensure we don't go below MIDI range
                base_notes[key] = value
    
    # Generate octave variations (apostrophes for higher octaves)
    for i in range(1, 8):  # Add up to 7 octaves up
        for note in list(base_notes):
            key = f"{note}" + ("'" * i)  # Add apostrophes for higher octaves
            value = base_notes[note] + i * 12  # Each octave is 12 semitones
            if value <= 127:  # Ensure we don't exceed MIDI range
                base_notes[key] = value
    
    # Return the MIDI pitch, or -1 if not found
    return base_notes.get(note_str.strip(), -1)

# --- Step 5: Tie expansion helper ---
def collect_full_tie_group(primary_href, ties_df):
    """
    Given a primary href, follow all chained secondaries recursively.
    """
    group = [primary_href]
    visited = set(group)
    queue = [primary_href]

    while queue:
        current = queue.pop(0)
        secondaries = ties_df.loc[ties_df["primary"] == current, "secondary"].tolist()
        for sec in secondaries:
            if sec not in visited:
                group.append(sec)
                visited.add(sec)
                queue.append(sec)

    return group

# --- Step 6: Match MIDI with SVG noteheads ---
notes = []
for i, (midi_row, svg_row) in enumerate(zip(midi_df.itertuples(), svg_df.itertuples())):
    lp_pitch = parse_lilypond_note(svg_row.snippet)
    midi_pc = midi_row.pitch % 12
    lp_pc_val = lp_pitch % 12 if lp_pitch != -1 else -1

    if lp_pc_val != midi_pc:
        print(f"Mismatch at {i}: MIDI pitch={midi_row.pitch} ({midi_pc}) vs LP='{svg_row.snippet}' → {lp_pc_val} {svg_row.href}")
        exit()

    tie_group = collect_full_tie_group(svg_row.href, ties_df)

    notes.append({
        "hrefs": tie_group,
        "on": midi_row.on,
        "off": midi_row.off,
        "pitch": midi_row.pitch,
        "channel": midi_row.channel
    })

# --- Step 7: Write output file ---
ouput_file = "bwv1006_json_notes.json"
with open(ouput_file, "w") as f:
    json.dump(notes, f, indent=2)

details = f"[ wrote {len(notes)} aligned notes ]"
print(f"💾 Saved: {ouput_file} {details}")
