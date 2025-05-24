#!/usr/bin/env python3
"""
SVG optimization script using SVGO
Preserves music notation-specific attributes and structure
"""

import subprocess
import shutil
from pathlib import Path

def optimize_svg(input_file, output_file=None):
    """Optimize SVG file with SVGO, preserving music notation integrity"""
    
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ Input file {input_file} not found")
        return False
    
    # Use input filename with _optimized suffix if no output specified
    if output_file is None:
        output_file = input_path.stem + "_optimized" + input_path.suffix
    
    output_path = Path(output_file)
    
    try:
        # Run SVGO optimization (shortest syntax)
        cmd = ["npx", "svgo", "--config=svgo.config.js", str(input_path), "-o", str(output_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        # print(f"🎯 Optimized {input_file} → {output_file}")

        if result.returncode == 0:
            # Get file sizes for comparison
            original_size = input_path.stat().st_size
            optimized_size = output_path.stat().st_size
            reduction = ((original_size - optimized_size) / original_size) * 100
            
            print(f"💾 Saved: {output_file} [ 📊 Size: {original_size:,} → {optimized_size:,} bytes ({reduction:.1f}% reduction) ]")
            return True
        else:
            print(f"❌ SVGO failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error optimizing {input_file}: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    files_to_optimize = [
        "bwv1006_svg_no_hrefs_in_tabs_bounded.svg"
    ]
    
    # Command line arguments override default files
    if len(sys.argv) > 1:
        files_to_optimize = sys.argv[1:]
    
    success_count = 0
    for file in files_to_optimize:
        if optimize_svg(file):
            success_count += 1
    
    # print(f"\n🎯 Optimized {success_count}/{len(files_to_optimize)} files successfully")