#!/usr/bin/env python3
"""
BWV 1006 Build System Tasks

Clean task definitions that import utilities from tasks_utils.py
This separation prevents accidental loss of utility functions during workflow changes.
"""

from datetime import datetime
from invoke import task
from pathlib import Path

# Import all utilities from separate module
from tasks_utils import (
    smart_task, 
    remove_outputs,
    print_build_status,
    find_glob_sources,
    init_build_system
)

# =============================================================================
# PROJECT-SPECIFIC CONFIGURATION
# =============================================================================

def shared_ly_sources():
    """Get all shared LilyPond dependencies for BWV 1006."""
    return [
        Path("bwv1006_ly_main.ly"), 
        Path("highlight-bars.ily"), 
        Path("defs.ily")
    ] + list(Path(".").rglob("_?/*.ly"))

# Standard file lists for this project
LILYPOND_OUTPUTS = [
    "bwv1006.pdf", 
    "bwv1006.svg",
    "bwv1006_ly_one_line.svg", 
    "bwv1006_ly_one_line.midi"
]

SVG_PROCESSING_CHAIN = [
    "bwv1006_svg_no_hrefs_in_tabs.svg",
    "bwv1006_svg_no_hrefs_in_tabs_swellable.svg",
    "exports/bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg"
]

DATA_EXTRACTION_OUTPUTS = [
    "bwv1006_csv_midi_note_events.csv",
    "bwv1006_csv_svg_note_heads.csv",
    "exports/bwv1006_json_notes.json"
]

ALL_GENERATED_FILES = LILYPOND_OUTPUTS + SVG_PROCESSING_CHAIN + DATA_EXTRACTION_OUTPUTS + [".build_cache.json"]

# Initialize the build system
init_build_system("BWV 1006 Build System")

# =============================================================================
# LILYPOND BUILD TASKS
# =============================================================================

@task
def build_pdf(c, force=False):
    """Generate PDF with LilyPond."""
    smart_task(
        c,
        sources=[Path("bwv1006.ly")] + shared_ly_sources(),
        targets=["bwv1006.pdf"],
        commands=[
            f'docker run -v "{Path.cwd()}:/work" codello/lilypond:dev bwv1006.ly'
        ],
        force=force,
    )

@task(pre=[build_pdf])
def build_svg(c, force=False):
    """Generate main SVG score with LilyPond."""
    smart_task(
        c,
        sources=[Path("bwv1006.ly")] + shared_ly_sources(),
        targets=["bwv1006.svg"],
        commands=[
            f'docker run -v "{Path.cwd()}:/work" codello/lilypond:dev --svg bwv1006.ly'
        ],
        force=force,
    )

@task(pre=[build_svg])
def postprocess_svg(c, force=False):
    """Prepare final SVG - ready for JavaScript interaction."""
    smart_task(
        c,
        sources=[Path("bwv1006.svg"), Path("svgo.config.js")],
        targets=[
            "bwv1006_svg_no_hrefs_in_tabs.svg", 
            "bwv1006_svg_no_hrefs_in_tabs_swellable.svg",
            "exports/bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg"
        ],
        commands=[
            "python3 scripts/svg_remove_hrefs_in_tabs.py",
            "python3 scripts/svg_prepare_for_swell.py bwv1006_svg_no_hrefs_in_tabs.svg",
            "python3 scripts/svg_optimize.py bwv1006_svg_no_hrefs_in_tabs_swellable.svg exports/bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg"
        ],
        force=force,
    )

@task
def build_svg_one_line(c, force=False):
    """Generate one-line SVG score with LilyPond."""
    smart_task(
        c,
        sources=[Path("bwv1006_ly_one_line.ly")] + shared_ly_sources(),
        targets=["bwv1006_ly_one_line.svg", "bwv1006_ly_one_line.midi"],
        commands=[
            f'docker run -v "{Path.cwd()}:/work" codello/lilypond:dev --svg bwv1006_ly_one_line.ly'
        ],
        force=force,
    )

# =============================================================================
# INDEPENDENT DATA EXTRACTION TASKS
# (These tasks have no interdependencies and could be parallelized in the future)
# =============================================================================

@task(pre=[build_svg_one_line])
def extract_midi_timing(c, force=False):
    """Extract MIDI note timing data from generated MIDI file."""
    smart_task(
        c,
        sources=[Path("bwv1006_ly_one_line.midi")],
        targets=["bwv1006_csv_midi_note_events.csv"],
        commands=[
            "python3 scripts/midi_map.py"
        ],
        force=force,
    )

@task(pre=[build_svg_one_line])
def extract_svg_noteheads(c, force=False):
    """Extract notehead positions and pitch data from generated SVG file."""
    smart_task(
        c,
        sources=[Path("bwv1006_ly_one_line.svg")],
        targets=["bwv1006_csv_svg_note_heads.csv"],
        commands=[
            "python3 scripts/svg_extract_note_heads.py"
        ],
        force=force,
    )

@task(pre=[extract_midi_timing, extract_svg_noteheads])
def align_data(c, force=False):
    """Align MIDI timing data with SVG notehead positions."""
    # Check that prerequisite files exist before proceeding
    midi_csv = Path("bwv1006_csv_midi_note_events.csv")
    svg_csv = Path("bwv1006_csv_svg_note_heads.csv")
    
    if not midi_csv.exists():
        print(f"❌ Missing required file: {midi_csv}")
        print("   Try running: invoke extract_midi_timing")
        return
    
    if not svg_csv.exists():
        print(f"❌ Missing required file: {svg_csv}")
        print("   Try running: invoke extract_svg_noteheads")
        return
    
    smart_task(
        c,
        sources=[midi_csv, svg_csv],
        targets=["exports/bwv1006_json_notes.json"],
        commands=[
            "python3 scripts/align_pitch_by_geometry_simplified.py"
        ],
        force=force,
    )

# =============================================================================
# AGGREGATE TASKS
# =============================================================================

@task
def json_notes(c, force=False):
    """
    Complete MIDI-to-JSON alignment pipeline (independent extraction + alignment).
    
    This task runs the full data extraction and alignment workflow:
    1. extract_midi_timing & extract_svg_noteheads (independent tasks, run sequentially)
    2. align_data (requires both CSV files from step 1)
    
    Note: Steps 1a and 1b are independent and could be parallelized in future versions.
    """
    extract_midi_timing(c, force=force)
    extract_svg_noteheads(c, force=force) 
    align_data(c, force=force)

@task
def all(c, force=False):
    """Run the full build and post-processing pipeline."""
    build_pdf(c, force=force)
    build_svg(c, force=force)
    postprocess_svg(c, force=force)
    build_svg_one_line(c, force=force)
    json_notes(c, force=force)
    print(f"\n✅✅✅ All steps completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ✅✅✅")

# =============================================================================
# DEVELOPMENT AND DEBUGGING TASKS
# =============================================================================

@task
def debug_origin(c):
    """Confirm that tasks.py is loaded."""
    print("✅ This is the clean, modular tasks.py with utilities imported from tasks_utils.py!")

@task
def debug_csv_files(c):
    """Debug helper to check CSV file status."""
    csv_files = [
        "bwv1006_csv_midi_note_events.csv",
        "bwv1006_csv_svg_note_heads.csv"
    ]
    
    print("🔍 CSV File Status:")
    for filename in csv_files:
        path = Path(filename)
        if path.exists():
            size = path.stat().st_size
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            print(f"   ✅ {filename}: {size:,} bytes, modified {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Show first few lines
            try:
                with open(path, 'r') as f:
                    lines = f.readlines()[:3]
                print(f"      Preview: {len(lines)} lines shown")
                for i, line in enumerate(lines):
                    print(f"      {i+1}: {line.strip()}")
            except Exception as e:
                print(f"      ⚠️ Could not read file: {e}")
        else:
            print(f"   ❌ {filename}: Missing")

@task
def clean(c):
    """Clean all generated files and build cache."""
    remove_outputs(*ALL_GENERATED_FILES)
    print("🧹 Cleaned all generated files and build cache")

@task
def status(c):
    """Show status of all build targets."""
    files = [
        ("bwv1006.pdf", "PDF"),
        ("bwv1006.svg", "Main SVG"),
        ("bwv1006_svg_no_hrefs_in_tabs.svg", "Cleaned SVG"),
        ("bwv1006_svg_no_hrefs_in_tabs_swellable.svg", "Swellable SVG"),
        ("exports/bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg", "Optimized SVG"),
        ("bwv1006_ly_one_line.svg", "One-line SVG"),
        ("bwv1006_ly_one_line.midi", "MIDI Data"),
        ("bwv1006_csv_midi_note_events.csv", "MIDI Events CSV"),
        ("bwv1006_csv_svg_note_heads.csv", "SVG Noteheads CSV"),
        ("exports/bwv1006_json_notes.json", "Synchronized JSON")
    ]
    
    print_build_status(files)