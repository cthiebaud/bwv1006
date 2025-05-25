#!/usr/bin/env python3
"""
SVG Structure Validator for Musical Notation

This script validates that an optimized SVG maintains the required structure
for note head highlighting and bar highlighting functionality.

Usage: python3 svg_validator.py <svg_file>
"""

import sys
from pathlib import Path
from xml.etree import ElementTree as ET

def find_note_heads(svg_root):
    """Find all elements with href-like attributes that have path children (note heads)"""
    note_heads = []
    
    # Find all elements with any href-like attributes (ignoring namespaces)
    for elem in svg_root.iter():
        href_value = None
        
        # Check all attributes for anything ending with 'href'
        for attr_name, attr_value in elem.attrib.items():
            if attr_name.endswith('href'):
                href_value = attr_value
                break
        
        if href_value and 'textedit://' in href_value:
            # Check if this element has path children
            paths = []
            # Look for path children (ignore namespaces)
            for child in elem:
                if child.tag.endswith('path'):
                    paths.append(child)
            
            # Also check nested children
            for descendant in elem.iter():
                if descendant.tag.endswith('path') and descendant != elem:
                    paths.append(descendant)
            
            if paths:
                note_heads.append({
                    'href': href_value,
                    'path_count': len(paths)
                })
    
    return note_heads

def find_bar_highlights(svg_root):
    """Find all elements with data-bar attributes (bar highlights)"""
    bar_highlights = []
    
    # Find all elements with data-bar attributes (any namespace)
    for elem in svg_root.iter():
        for attr_name, attr_value in elem.attrib.items():
            if attr_name.endswith('data-bar') or attr_name == 'data-bar':
                bar_highlights.append({
                    'data_bar': attr_value
                })
                break  # Only count each element once
    
    return bar_highlights

def validate_svg(svg_file):
    """Validate a single SVG file"""
    try:
        tree = ET.parse(svg_file)
        svg_root = tree.getroot()
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False
    
    # Find structural elements
    note_heads = find_note_heads(svg_root)
    bar_highlights = find_bar_highlights(svg_root)
    
    print(f"📊 SVG Structure Analysis: {svg_file}")
    print(f"   Note heads (elements with [href] + path children): {len(note_heads)}")
    print(f"   Bar highlights (elements with [data-bar]): {len(bar_highlights)}")
    
    # Validation
    valid = True
    
    if len(note_heads) == 0:
        print("❌ ERROR: No note heads found")
        valid = False
    
    if len(bar_highlights) == 0:
        print("❌ ERROR: No bar highlights found")
        valid = False
    
    if valid:
        print("✅ SVG structure is valid for musical notation functionality")
    else:
        print("❌ SVG structure is invalid - functionality will be broken")
    
    return valid

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 svg_validator.py <svg_file>")
        print("Example: python3 svg_validator.py optimized.svg")
        sys.exit(1)
    
    svg_file = Path(sys.argv[1])
    
    if not svg_file.exists():
        print(f"❌ File not found: {svg_file}")
        sys.exit(1)
    
    # Validate the SVG
    is_valid = validate_svg(svg_file)
    
    # Exit with appropriate code
    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()