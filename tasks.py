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
    return [Path("bwv1006_ly_main.ly"), Path("defs.ily")] + list(Path(".").rglob("_?/*.ly"))

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

# 🧱 Tasks

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
def process_svg(c, force=False):
    """Post-process the SVG to clean and adjust."""
    smart_task(
        c,
        sources=[Path("bwv1006.svg")],
        targets=["bwv1006_svg_no_hrefs_in_tabs.svg", "bwv1006_svg_no_hrefs_in_tabs_bounded.svg"],
        commands=[
            "python3 scripts/svg_remove_hrefs_in_tabs.py",
            "python3 scripts/svg_tighten_viewbox.py",
        ],
        force=force,
    )

@task(pre=[process_svg])
def optimize_svg(c, force=False):
    """Optimize SVG files with SVGO."""
    smart_task(
        c,
        sources=[Path("bwv1006_svg_no_hrefs_in_tabs_bounded.svg")],
        targets=["bwv1006_svg_no_hrefs_in_tabs_bounded_optimized.svg"],
        commands=[
            "python3 scripts/svg_optimize.py"
        ],
        force=force,
    )

@task(pre=[optimize_svg])
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

@task(pre=[build_svg_one_line])
def json_notes(c, force=False):
    """Run MIDI to JSON alignment steps."""
    smart_task(
        c,
        sources=[Path("bwv1006_ly_one_line.svg"), Path("bwv1006_ly_one_line.midi")],
        targets=[
            "bwv1006_csv_midi_note_events.csv",
            "bwv1006_csv_svg_note_heads.csv",
            "bwv1006_json_notes.json",
        ],
        commands=[
            "python3 scripts/midi_map.py",
            "python3 scripts/svg_extract_note_heads.py",
            "python3 scripts/align_pitch_by_geometry_simplified.py",
        ],
        force=force,
    )

@task
def all(c, force=False):
    """Run the full build and post-processing pipeline."""
    build_pdf(c, force=force)
    build_svg(c, force=force)
    process_svg(c, force=force)
    build_svg_one_line(c, force=force)
    json_notes(c, force=force)
    print(f"\n✅✅✅ All steps completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ✅✅✅")

@task
def debug_origin(c):
    """Confirm that tasks_on_steroids.py is loaded."""
    print("✅ This is tasks_on_steroids.py in action.")
