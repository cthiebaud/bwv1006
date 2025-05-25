import hashlib
import json
import inspect
from datetime import datetime
from pathlib import Path
from invoke import task

# File to store hash-based cache of source files
CACHE_FILE = Path(".build_cache.json")

# 🔧 Utility to delete files
def remove_outputs(*filenames, force=True):
    deleted = []
    for name in filenames:
        path = Path(name)
        if path.exists():
            path.unlink()
            deleted.append(path.name)
    if deleted:
        print(f"🗑️  Deleted: {', '.join(deleted)}")
        
# 📁 Get all shared .ly dependencies
def shared_ly_sources():
    return [Path("bwv1006_ly_main.ly"), Path("highlight-bars.ily"), Path("defs.ily")] + list(Path(".").rglob("_?/*.ly"))

# 🔐 Compute SHA256 hash of a file
def hash_file(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# 📦 Load and save build cache
def load_cache():
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}

def save_cache(cache):
    CACHE_FILE.write_text(json.dumps(cache, indent=2))

# 🔁 Check if any input file changed
def sources_changed(task_name, source_paths):
    cache = load_cache()
    current_hashes = {str(p): hash_file(p) for p in source_paths if p.exists()}
    cached_hashes = cache.get(task_name, {})
    changed = current_hashes != cached_hashes
    if changed:
        cache[task_name] = current_hashes
        save_cache(cache)
    return changed

# ✨ Unified smart task runner
def smart_task(c, *, sources, targets, commands, force=False):
    task_name = inspect.stack()[1].function
    print(f"--- {task_name}")
    if force or sources_changed(task_name, sources):
        remove_outputs(*targets)
        print(f"🔧 Rebuilding {task_name}...")
        for cmd in commands:
            c.run(cmd)
        if targets:
            print(f"✅ Generated: {', '.join(str(t) for t in targets)}")
        else:
            print(f"✅ Task {task_name} completed")
    else:
        if targets:
            print("✅ Up to date:")
            for t in targets:
                print(f"   └── {t}")
        else:
            print(f"✅ Up to date: {task_name}")

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
    """Post-process and optimize the SVG files."""
    smart_task(
        c,
        sources=[Path("bwv1006.svg")],
        targets=[
            "bwv1006_svg_no_hrefs_in_tabs.svg", 
            "bwv1006_svg_no_hrefs_in_tabs_bounded.svg",
            "bwv1006_svg_no_hrefs_in_tabs_bounded_optimized.svg",
            "bwv1006_svg_no_hrefs_in_tabs_bounded_optimized_swellable.svg"
        ],
        commands=[
            "python3 scripts/svg_remove_hrefs_in_tabs.py",
            "python3 scripts/svg_tighten_viewbox.py",
            "python3 scripts/svg_optimize.py",
            "python3 scripts/svg_prepare_for_swell.py bwv1006_svg_no_hrefs_in_tabs_bounded_optimized.svg"
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
# PARALLEL DATA EXTRACTION TASKS
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
        targets=["bwv1006_json_notes.json"],
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
    Complete MIDI-to-JSON alignment pipeline (parallel extraction + alignment).
    
    This task runs the full data extraction and alignment workflow:
    1. extract_midi_timing & extract_svg_noteheads (can run in parallel)
    2. align_data (requires both CSV files)
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
    json_notes(c, force=force)  # This now runs the optimized parallel workflow
    print(f"\n✅✅✅ All steps completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ✅✅✅")

# =============================================================================
# DEVELOPMENT AND DEBUGGING TASKS
# =============================================================================

@task
def debug_origin(c):
    """Confirm that tasks.py is loaded."""
    print("✅ This is the optimized tasks.py with parallel processing!")

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
    
    # Check if scripts exist
    print(f"\n🔍 Script Status:")
    scripts = [
        "scripts/midi_map.py",
        "scripts/svg_extract_note_heads.py", 
        "scripts/align_pitch_by_geometry_simplified.py"
    ]
    
    for script in scripts:
        path = Path(script)
        if path.exists():
            print(f"   ✅ {script}")
        else:
            print(f"   ❌ {script}: Missing")

@task
def clean(c):
    """Clean all generated files and build cache."""
    files_to_clean = [
        # LilyPond outputs
        "bwv1006.pdf", "bwv1006.svg",
        "bwv1006_ly_one_line.svg", "bwv1006_ly_one_line.midi",
        
        # SVG processing chain
        "bwv1006_svg_no_hrefs_in_tabs.svg",
        "bwv1006_svg_no_hrefs_in_tabs_bounded.svg", 
        "bwv1006_svg_no_hrefs_in_tabs_bounded_optimized.svg",
        "bwv1006_svg_no_hrefs_in_tabs_bounded_optimized_swellable.svg",
        
        # Data extraction outputs
        "bwv1006_csv_midi_note_events.csv",
        "bwv1006_csv_svg_note_heads.csv",
        "bwv1006_json_notes.json",
        
        # Build cache
        ".build_cache.json"
    ]
    
    remove_outputs(*files_to_clean)
    print("🧹 Cleaned all generated files and build cache")

@task
def status(c):
    """Show status of all build targets."""
    targets = {
        "PDF": "bwv1006.pdf",
        "Main SVG": "bwv1006.svg", 
        "Animated SVG": "bwv1006_svg_no_hrefs_in_tabs_bounded_optimized_swellable.svg",
        "One-line SVG": "bwv1006_ly_one_line.svg",
        "MIDI Data": "bwv1006_ly_one_line.midi",
        "MIDI Events CSV": "bwv1006_csv_midi_note_events.csv",
        "SVG Noteheads CSV": "bwv1006_csv_svg_note_heads.csv", 
        "Synchronized JSON": "bwv1006_json_notes.json"
    }
    
    print("📊 Build Status:")
    for name, filename in targets.items():
        path = Path(filename)
        if path.exists():
            size = path.stat().st_size
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            print(f"   ✅ {name}: {filename} ({size:,} bytes, {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            print(f"   ❌ {name}: {filename} (missing)")