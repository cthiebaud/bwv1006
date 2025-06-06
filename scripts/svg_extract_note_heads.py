#!/usr/bin/env python3
"""
svg_extract_note_heads.py

SVG Musical Notehead Extraction Pipeline  
========================================

This script extracts notehead positions and pitch information from SVG files
generated by LilyPond music notation software. It creates a dataset mapping
visual notehead locations to their corresponding musical pitches for use in
animated score following applications.

Process Overview:
1. Parse LilyPond-generated SVG to find clickable notehead elements
2. Extract pitch information from LilyPond source code via href links  
3. Determine visual coordinates for each notehead
4. Create sorted dataset ordered by visual appearance (left-to-right, top-to-bottom)

Input Files:
- SVG file with embedded LilyPond cross-references
- Original LilyPond (.ly) source file for pitch extraction

Output:
- CSV file with notehead coordinates, pitches, and reference links
"""

import re
import csv
import xml.etree.ElementTree as ET

# =============================================================================
# LILYPOND PITCH PATTERN MATCHING
# =============================================================================

# Regular expression to identify LilyPond note syntax in source code
# Matches: letter name + optional accidentals + optional octave marks
note_regex = re.compile(r"""
            ^                 # start of string
            ([a-g])        # pitch letter
            (isis|eses|is|es)?# optional accidentals
            \s*               # optional octave marks
            [,']*             # optional octave marks
        """, re.VERBOSE)

# =============================================================================
# LILYPOND SOURCE CODE PARSING FUNCTION
# =============================================================================

def extract_text_from_href(href):
    """
    Extract LilyPond pitch notation from cross-reference URLs.
    
    LilyPond embeds "textedit" URLs in SVG that point back to specific
    locations in the source .ly file. These URLs encode file path, line
    number, and column position, allowing us to extract the exact pitch
    notation that generated each visual notehead.
    
    Args:
        href (str): TextEdit URL from SVG (e.g., "textedit:///work/file.ly:25:10")
        
    Returns:
        str or None: LilyPond pitch notation (e.g., "cis'") or None if not found
        
    URL Format: textedit:///work/filepath:line:column
    - filepath: Path to .ly source file
    - line: 1-based line number  
    - column: 1-based character position
    """
    try:
        # Clean up URL format - remove textedit protocol prefix
        if href.startswith("textedit:///work/"):
            href = href[len("textedit:///work/"):]
        else:
            return "(invalid href format)"

        # Parse URL components: "file.ly:line:column"
        parts = href.split(":")
        file_path = parts[0]
        line = int(parts[1]) - 1      # Convert to 0-based indexing
        col_start = int(parts[2])     # 1-based column position

        # Read the specific LilyPond source file referenced in the href
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()

        # Extract text from the specified position to end of line
        text_line = lines[line][col_start:]
        text = text_line.strip().strip("[]<>()")
        
        # Attempt to match LilyPond note pattern
        match = note_regex.match(text)

        if match:
            # Return the matched note notation without extra whitespace
            return match.group(0).replace(" ", "")
        else:
            # Return None if no valid note pattern found
            return None

    except Exception as e:
        return f"(error: {e})"

def main():
    """Main function with project context support."""

    SVG_FILE = "bwv1006_ly_one_line.svg"     # LilyPond-generated SVG with noteheads
    LY_FILE = "bwv1006.ly"                   # Original LilyPond source code
    OUTPUT_CSV = "bwv1006_csv_svg_note_heads.csv"  # Output dataset

    print(f"🎼 Processing musical score:")
    print(f"   📄 SVG source: {SVG_FILE}")
    print(f"   🎵 LilyPond source: {LY_FILE}")
    
    # =============================================================================
    # XML NAMESPACE SETUP AND FILE LOADING
    # =============================================================================

    print("🔍 Loading and parsing SVG file...")

    # Load SVG file
    with open(SVG_FILE, encoding="utf-8") as f:
        svg = ET.parse(f)

    # Load LilyPond source (used by extract_text_from_href function)
    with open(LY_FILE, encoding="utf-8") as f:
        ly_lines = f.readlines()

    # SVG namespaces for XPath queries
    NS = {'svg': 'http://www.w3.org/2000/svg', 'xlink': 'http://www.w3.org/1999/xlink'}
    root = svg.getroot()
    # =============================================================================
    # NOTEHEAD DISCOVERY AND COORDINATE EXTRACTION
    # =============================================================================

    print("📍 Extracting notehead positions and pitch data...")

    # Storage for discovered noteheads
    notehead_data = []

    # Find all clickable <a> elements (these contain the noteheads)
    for a in root.findall(".//svg:a", NS):
        # Get the cross-reference URL
        href = a.get(f"{{{NS['xlink']}}}href")
        
        # Extract pitch information from the href
        snippet = extract_text_from_href(href)

        # Skip if we couldn't extract valid pitch information
        if not snippet is None:
            # Find the graphical group element containing visual positioning
            g = a.find("svg:g", NS)
            
            if g is not None:
                # Extract coordinate transformation from the group's transform attribute
                transform = g.attrib.get("transform", "")
                
                # Parse translation coordinates: "translate(x, y)" or "translate(x,y)"
                match = re.search(r"translate\(([-\d.]+)[ ,]+([-\d.]+)", transform)
                
                if not match:
                    print(f"no matching transform near <a> of [{href}] for snippet [{snippet}]")
                
                if match:
                    # Extract and convert coordinates
                    x = float(match.group(1))
                    y = float(match.group(2))
                    
                    # Store the notehead information
                    notehead_data.append({
                        "x": x,
                        "y": y,
                        "href": href,
                        "snippet": snippet
                    })

    print(f"   📊 Processed {len(root.findall('.//svg:a', NS))} anchor elements")
    print(f"   ✅ Found {len(notehead_data)} valid noteheads with pitch data") 

    # =============================================================================
    # SPATIAL SORTING FOR VISUAL ALIGNMENT
    # =============================================================================

    print("📐 Sorting noteheads by visual position...")

    # Sort noteheads by visual reading order:
    # 1. Primary sort: x-coordinate (left to right across the staff)  
    # 2. Secondary sort: y-coordinate (top to bottom for simultaneous notes)
    #    Note: Negative y-coordinate because SVG y=0 is at top, music reads top-to-bottom
    notehead_data.sort(key=lambda n: (n["x"], -n["y"]))  # descending y = top-to-bottom

    print(f"   🎯 Sorted {len(notehead_data)} noteheads in reading order")

    # =============================================================================
    # CSV EXPORT
    # =============================================================================

    print(f"💾 Writing results to {OUTPUT_CSV}...")

    # Define CSV structure with all relevant data for downstream processing
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["index", "x", "y", "snippet", "href"])
        
        # Write header row
        writer.writeheader()
        
        # Write data rows with sequential indexing
        for i, note in enumerate(notehead_data, 1):
            writer.writerow({
                "index": i,                             # Sequential position number
                "x": round(note["x"], 3),              # X-coordinate (3 decimal precision)
                "y": round(note["y"], 3),              # Y-coordinate (3 decimal precision)  
                "snippet": note["snippet"],            # LilyPond pitch notation
                "href": note["href"]                   # Original cross-reference URL
            })

    # =============================================================================
    # COMPLETION SUMMARY
    # =============================================================================

    extraction_summary = f"[ extracted {len(notehead_data)} noteheads with coordinates and pitch data ]"
    print(f"✅ Export complete: {OUTPUT_CSV} {extraction_summary}")

    # Additional statistics for verification
    if notehead_data:
        x_range = max(n["x"] for n in notehead_data) - min(n["x"] for n in notehead_data)
        y_range = max(n["y"] for n in notehead_data) - min(n["y"] for n in notehead_data)
        unique_pitches = len(set(n["snippet"] for n in notehead_data))
        
        print(f"\n📊 Extraction Statistics:")
        print(f"   📏 X-coordinate range: {x_range:.1f} units")
        print(f"   📐 Y-coordinate range: {y_range:.1f} units") 
        print(f"   🎵 Unique pitch notations: {unique_pitches}")
        print(f"   🔗 Average notes per pitch: {len(notehead_data)/unique_pitches:.1f}")

    print(f"\n� Ready for alignment with MIDI data in next pipeline stage")

if __name__ == "__main__":
    main()
