#!/usr/bin/env python3
"""
svg_optimize.py - Minimal SVGO wrapper with consistent logging
"""

import subprocess
import sys
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 svg_optimize.py <input.svg> <output.svg>")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])
    
    print(f"🎯 Optimizing SVG: {input_file.name}")
    print(f"   📤 Input: {input_file}")
    print(f"   📥 Output: {output_file}")
    
    # Get original size
    original_size = input_file.stat().st_size
    print(f"   📏 Original size: {original_size:,} bytes")
    
    # Run SVGO
    print(f"   🔧 Running SVGO optimization...")
    result = subprocess.run([
        'npx', 'svgo', str(input_file), '--output', str(output_file)
    ], capture_output=True, text=True)
    
    if result.returncode == 0 and output_file.exists():
        optimized_size = output_file.stat().st_size
        reduction = ((original_size - optimized_size) / original_size) * 100
        
        print(f"✅ Optimization complete: {output_file.name}")
        print(f"   📊 Size: {original_size:,} → {optimized_size:,} bytes ({reduction:.1f}% reduction)")
    else:
        print(f"❌ SVGO optimization failed: {result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()