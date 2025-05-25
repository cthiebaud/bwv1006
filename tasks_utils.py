#!/usr/bin/env python3
"""
Generic Build System Utilities

This module contains generic utility functions for build systems,
with no project-specific references. Can be reused across different projects.
"""

import builtins
import hashlib
import inspect
import json
import os
from datetime import datetime
from pathlib import Path

# ==============================================================================
# ENHANCED PRINT FUNCTION WITH CONDITIONAL TIMESTAMPING
# ==============================================================================
# This monkey-patch globally replaces Python's built-in print() function to:
# 1. Always flush output immediately (fixes log ordering issues)
# 2. Add timestamps only when output is redirected to files (preserves clean console output)

# Store reference to original print function before we replace it
_original_print = builtins.print

def smart_print(*args, **kwargs):
    """
    Enhanced print function that conditionally adds timestamps and always flushes.
    
    Behavior:
    - Interactive use: Clean output without timestamps
    - Redirected to file: Timestamped output for debugging
    - Always flushes immediately to prevent output ordering issues
    """
    # Only add timestamps when redirected to a file
    if not os.isatty(1):  # stdout is not a terminal (redirected to file/pipe)
        # Generate timestamp in HH:MM:SS.mmm format (millisecond precision)
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]  # [:-3] truncates microseconds to milliseconds
        
        # Prepend timestamp to all arguments
        if args:
            args = (f"[{timestamp}]", *args)  # Add timestamp as first argument
        else:
            args = (f"[{timestamp}]",)        # Handle edge case of print() with no args
    
    # Call original print with all arguments, forcing flush=True for consistent output ordering
    return _original_print(*args, **kwargs, flush=True)

# Globally replace the built-in print function
# This affects ALL Python code in this process, including imported modules and scripts
builtins.print = smart_print

# ==============================================================================
# BUILD CACHE SYSTEM
# ==============================================================================

def hash_file(path):
    """Compute SHA256 hash of a file for change detection."""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def load_cache(cache_file=".build_cache.json"):
    """Load build cache from disk."""
    cache_path = Path(cache_file)
    if cache_path.exists():
        return json.loads(cache_path.read_text())
    return {}

def save_cache(cache, cache_file=".build_cache.json"):
    """Save build cache to disk."""
    cache_path = Path(cache_file)
    cache_path.write_text(json.dumps(cache, indent=2))

def sources_changed(task_name, source_paths, cache_file=".build_cache.json"):
    """
    Check if any input file changed since last build.
    
    Args:
        task_name: Name of the task (for cache key)
        source_paths: List of Path objects to check
        cache_file: Path to cache file
        
    Returns:
        bool: True if any source file changed
    """
    cache = load_cache(cache_file)
    current_hashes = {str(p): hash_file(p) for p in source_paths if p.exists()}
    cached_hashes = cache.get(task_name, {})
    changed = current_hashes != cached_hashes
    if changed:
        cache[task_name] = current_hashes
        save_cache(cache, cache_file)
    return changed

# ==============================================================================
# FILE MANAGEMENT UTILITIES
# ==============================================================================

def remove_outputs(*filenames, force=True):
    """
    Remove output files with nice logging.
    
    Args:
        *filenames: Files to remove
        force: If True, ignore missing files
    """
    deleted = []
    for name in filenames:
        path = Path(name)
        if path.exists():
            path.unlink()
            deleted.append(path.name)

    print("🗑️  Deleted:", end="")
    if deleted:
        print()  # Add newline for multi-line format
        for d in deleted:
            print(f"   └── {d}")
    else:
        print(" ∅")  # Continue on same line

def get_file_info(filename, name):
    """
    Get file information for status reporting.
    
    Args:
        filename: Path to file
        name: Display name for file
        
    Returns:
        tuple: (mtime, name, filename, size, exists)
    """
    path = Path(filename)
    if path.exists():
        mtime = path.stat().st_mtime
        size = path.stat().st_size
        return (mtime, name, filename, size, True)
    else:
        return (0, name, filename, 0, False)  # Missing files sort first

# ==============================================================================
# SMART TASK RUNNER
# ==============================================================================

def smart_task(c, *, sources, targets, commands, force=False, cache_file=".build_cache.json"):
    """
    Unified smart task runner with caching and progress reporting.
    
    Args:
        c: Invoke context
        sources: List of source file paths
        targets: List of target file paths/names
        commands: List of shell commands to run
        force: If True, force rebuild regardless of cache
        cache_file: Path to cache file
    """
    task_name = inspect.stack()[1].function
    print(f"")
    print(f"[{task_name}]")
    
    if force or sources_changed(task_name, sources, cache_file):
        remove_outputs(*targets)
        print(f"🔧 Rebuilding {task_name}...")
        
        for cmd in commands:
            # Run subprocess commands with unbuffered output for better logging
            if cmd.startswith('python3 '):
                cmd = cmd.replace('python3 ', 'python3 -u ')
            c.run(cmd)
        
        # Validate that all targets were actually created
        missing_targets = [t for t in targets if not Path(t).exists()]
        if missing_targets:
            print(f"❌ Error: Some targets were not created:")
            for target in missing_targets:
                print(f"   • {target}")
            raise RuntimeError(f"Task {task_name} failed to create all targets")
        
        if targets:
            print("✅ Generated:")
            for t in targets:
                print(f"   └── {t}")
        else:
            print(f"✅ Task {task_name} completed")
    else:
        # Validate targets exist even when up-to-date
        missing_targets = [t for t in targets if not Path(t).exists()]
        if missing_targets:
            print(f"⚠️  Cache inconsistency detected - targets missing:")
            for target in missing_targets:
                print(f"   • {target}")
            print(f"🔧 Forcing rebuild due to missing targets...")
            # Recursively call with force=True to rebuild
            return smart_task(c, sources=sources, targets=targets, commands=commands, force=True, cache_file=cache_file)
        
        if targets:
            print("✅ Up to date:")
            for t in targets:
                print(f"   └── {t}")
        else:
            print(f"✅ Up to date: {task_name}")

# ==============================================================================
# UTILITY FUNCTIONS FOR COMMON PATTERNS
# ==============================================================================

def format_file_size(bytes_size):
    """Format file size in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

def print_build_status(files):
    """
    Print formatted build status for a list of files.
    
    Args:
        files: List of (filename, display_name) tuples
    """
    # Get file info and sort by timestamp
    file_infos = [get_file_info(filename, name) for filename, name in files]
    file_infos.sort(key=lambda x: x[0])  # Sort by mtime
    
    print("📊 Build Status:")
    for mtime, name, filename, size, exists in file_infos:
        if exists:
            mtime_str = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            print(f"   ✅ {name:<18}: {filename:<75} ({size:>10,} bytes, {mtime_str})")
        else:
            print(f"   ❌ {name:<18}: {filename:<75} (missing)")

def find_glob_sources(*patterns):
    """
    Find source files matching glob patterns.
    
    Args:
        *patterns: Glob patterns to search for
        
    Returns:
        list: List of Path objects
    """
    sources = []
    for pattern in patterns:
        sources.extend(Path(".").glob(pattern))
    return sources

# ==============================================================================
# INITIALIZATION (Optional)
# ==============================================================================

def init_build_system(project_name="Build System"):
    """
    Initialize the build system with optional project name.
    
    Args:
        project_name: Name of the project (for display only)
    """
    print(f"🔧 {project_name} Utilities Loaded")
    print(f"   📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   🔍 Smart print: {'✅ Timestamped' if not os.isatty(1) else '✅ Clean Console'}")