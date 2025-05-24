"""
Build script generated from DOT file
Generated on: 2025-05-24 09:29:21
"""

from pathlib import Path
from datetime import datetime

def expand_glob(pattern):
    """Expand a glob pattern and return list of Path objects."""
    if '**' in pattern:
        # Recursive glob
        parts = pattern.split('**/')
        if len(parts) == 2:
            base_path = Path(parts[0]) if parts[0] else Path('.')
            return list(base_path.rglob(parts[1]))
    
    # Regular glob
    return list(Path('.').glob(pattern))

def shared_ly_sources():
    """Get shared LilyPond source files."""
    shared_files = []
    
    # Static files
    for file_path in [Path("bwv1006_ly_main.ly"), Path("highlight-bars.ily"), Path("defs.ily")]:
        if file_path.exists():
            shared_files.append(file_path)
    
    # Dynamic globs
    shared_files.extend(expand_glob("_?/*.ly"))
    shared_files.extend(expand_glob("**/*.ily"))
    
    return shared_files

def remove_outputs(*filenames):
    """Clean action to remove output files."""
    def clean_targets():
        deleted = []
        for name in filenames:
            path = Path(name)
            if path.exists():
                path.unlink()
                deleted.append(path.name)
        if deleted:
            print(f"🗑️  Deleted: {', '.join(deleted)}")
    return clean_targets

def remove_glob_outputs(*patterns):
    """Clean action to remove files matching glob patterns."""
    def clean_glob_targets():
        deleted = []
        for pattern in patterns:
            for path in expand_glob(pattern):
                if path.exists():
                    path.unlink()
                    deleted.append(path.name)
        if deleted:
            print(f"🗑️  Deleted glob matches: {', '.join(deleted)}")
    return clean_glob_targets



def task_list_globs():
    """List all files matching glob patterns."""
    def list_glob_matches():
        print("🔍 Glob pattern matches:")
        print(f"  _?/*.ly:")
        for path in expand_glob("_?/*.ly"):
            print(f"    {path}")
        print(f"  **/*.ily:")
        for path in expand_glob("**/*.ily"):
            print(f"    {path}")
        print(f"  scripts/*.py:")
        for path in expand_glob("scripts/*.py"):
            print(f"    {path}")
        print(f"  output/*.json:")
        for path in expand_glob("output/*.json"):
            print(f"    {path}")
        print(f"  temp/*.tmp:")
        for path in expand_glob("temp/*.tmp"):
            print(f"    {path}")
    
    return {
        'actions': [list_glob_matches],
        'verbosity': 2,
    }

# Default task configuration
def task_all():
    """Run the complete build pipeline."""
    def completion_message():
        print(f"\n✅✅✅ All steps completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ✅✅✅")
    
    return {
        'actions': [completion_message],
        'task_dep': [],
        'verbosity': 2,
    }

DOIT_CONFIG = {
    'default_tasks': ['all'],
    'verbosity': 2,
}
