import re
import csv
import xml.etree.ElementTree as ET

SVG_FILE = "bwv1006.svg"
LY_FILE = "bwv1006.ly"
OUTPUT_CSV = "bwv1006_svg_note_heads.csv"

# --- Load SVG and LilyPond source ---
with open(SVG_FILE, encoding="utf-8") as f:
    svg = ET.parse(f)

with open(LY_FILE, encoding="utf-8") as f:
    ly_lines = f.readlines()

NS = {'svg': 'http://www.w3.org/2000/svg', 'xlink': 'http://www.w3.org/1999/xlink'}
root = svg.getroot()

note_regex = re.compile(r"""
            ^                 # start of string
            ([a-g])        # pitch letter
            (isis|eses|is|es)?# optional accidentals
            \s*               # optional octave marks
            [,']*             # optional octave marks
        """, re.VERBOSE)


import re

def extract_text_from_href(href):
    try:
        if href.startswith("textedit:///work/"):
            href = href[len("textedit:///work/"):]
        else:
            return "(invalid href format)"

        parts = href.split(":")
        file_path = parts[0]
        line = int(parts[1]) - 1
        col_start = int(parts[2]) 

        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()

        # Extract from col_start to end
        text_line = lines[line][col_start:]
        text = text_line.strip().strip("[]<>()")
        # print(file_path, line, col_start, text)

        match = note_regex.match(text)

        if match:
            return match.group(0).replace(" ", "")
        else:
            return None

    except Exception as e:
        return f"(error: {e})"

# Collect note-like <a> tags with their x-position
notehead_data = []

for a in root.findall(".//svg:a", NS):
    href = a.get(f"{{{NS['xlink']}}}href")
    snippet = extract_text_from_href(href)

    
    if not snippet is None:
        g = a.find("svg:g", NS)
        if g is None:
            print(snippet)
        if g is not None:
            transform = g.attrib.get("transform", "")
            match = re.search(r"translate\(([-\d.]+)[ ,]+([-\d.]+)", transform)
            if not match:
                print(snippet)
            if match:
                x = float(match.group(1))
                y = float(match.group(2))
                notehead_data.append({
                    "x": x,
                    "y": y,
                    "href": href,
                    "snippet": snippet
                })

# Sort by x position
notehead_data.sort(key=lambda n: (n["x"], -n["y"]))  # descending y = top-to-bottom

# Write to CSV
with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["index", "x", "y", "snippet", "href"])
    writer.writeheader()
    for i, note in enumerate(notehead_data, 1):
        writer.writerow({
            "index": i,
            "x": round(note["x"], 3),
            "y": round(note["y"], 3),
            "snippet": note["snippet"],
            "href": note["href"]
        })

print(f"✅ {len(notehead_data)} note heads written to {OUTPUT_CSV}")
