#!/usr/bin/env python3
"""
SVG Path Wrapper Script

This script modifies SVG files by wrapping <path> elements with <g> elements
when they are inside <a> tags that have xlink:href attributes.

Usage:
    python svg_modifier.py input.svg output.svg
    python svg_modifier.py input.svg  # overwrites input file
"""

import xml.etree.ElementTree as ET
import sys
import argparse
from pathlib import Path


def modify_svg_paths(svg_content):
    """
    Modify SVG content by wrapping path elements in group elements
    when they're inside anchor tags with xlink:href attributes.
    
    Args:
        svg_content (str): The SVG content as a string
        
    Returns:
        tuple: (str, str) - Modified SVG content and informational message
    """
    # Parse the SVG content
    try:
        root = ET.fromstring(svg_content)
    except ET.ParseError as e:
        error_msg = f"Error parsing SVG: {e}"
        return svg_content, error_msg
    
    # Clear default namespace to avoid ns0: prefixes
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    
    # Build parent map to find parent elements
    parent_map = {c: p for p in root.iter() for c in p}
    
    # Find all <a> elements with xlink:href attributes (without namespace prefixes)
    anchor_elements = []
    
    # Recursively search for all 'a' elements
    def find_anchor_elements(element):
        if element.tag == 'a' or element.tag.endswith('}a'):
            # Check if it has xlink:href attribute (with or without namespace)
            for attr_name in element.attrib:
                if attr_name == 'href' or attr_name.endswith('}href'):
                    anchor_elements.append(element)
                    break
        
        for child in element:
            find_anchor_elements(child)
    
    find_anchor_elements(root)
    
    modifications_made = 0
    
    for anchor in anchor_elements:
        # Get the href attribute from the anchor
        href_value = None
        for attr_name, attr_value in anchor.attrib.items():
            if attr_name == 'href' or attr_name.endswith('}href'):
                href_value = attr_value
                break
        
        # Find direct child path elements
        path_elements = []
        for child in anchor:
            if child.tag == 'path' or child.tag.endswith('}path'):
                path_elements.append(child)
        
        for path in path_elements:
            # Check if path has a transform attribute
            transform_attr = path.get('transform')
            
            if transform_attr:
                # Create a new group element with proper namespace
                if '{http://www.w3.org/2000/svg}' in path.tag:
                    group = ET.Element('{http://www.w3.org/2000/svg}g')
                else:
                    group = ET.Element('g')
                
                # Set href and transform attributes on group
                if href_value:
                    group.set('href', href_value)
                group.set('transform', transform_attr)
                
                # Remove transform from path and add path to group
                path.attrib.pop('transform', None)
                group.append(path)
                
                # Replace the entire anchor with the group
                parent = parent_map.get(anchor)
                if parent is not None:
                    parent_children = list(parent)
                    anchor_index = parent_children.index(anchor)
                    parent.insert(anchor_index, group)
                    parent.remove(anchor)
                else:
                    # If anchor is root element, replace root
                    root = group
                
                modifications_made += 1
                break  # Only process first path in each anchor
    
    # Generate informational message
    if modifications_made > 0:
        msg = f"Modified {modifications_made} path element(s)"
    else:
        msg = "No modifications needed"
    
    # Convert back to string with proper formatting
    xml_str = ET.tostring(root, encoding='unicode', xml_declaration=False)
    
    # Add XML declaration if it was originally present
    if svg_content.strip().startswith('<?xml'):
        xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str
    
    return xml_str, msg


def process_svg_file(input_path, output_path=None):
    """
    Process an SVG file and apply the path wrapping modifications.
    
    Args:
        input_path (str): Path to input SVG file
        output_path (str, optional): Path to output SVG file. If None, creates <input>_swellable.svg
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"Error: Input file '{input_path}' does not exist")
        return False
    
    if not input_file.suffix.lower() == '.svg':
        print(f"Warning: File '{input_path}' does not have .svg extension")
    
    try:
        # Read the SVG file
        with open(input_file, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        # print(f"Processing: {input_path}")
        
        # Modify the SVG content and get message
        modified_content, message = modify_svg_paths(svg_content)
        
        # Determine output path
        if output_path is None:
            # Create filename with _swellable suffix
            stem = input_file.stem  # filename without extension
            parent = input_file.parent
            output_file = parent / f"{stem}_swellable.svg"
        else:
            output_file = Path(output_path)
        
        # Write the modified content
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        print(f"💾 Saved: {output_file} [ {message} ]")
        return True
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return False


def main():
    """Main function to handle command line arguments and process files."""
    parser = argparse.ArgumentParser(
        description='Modify SVG files to wrap path elements with group elements',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python svg_modifier.py input.svg output.svg    # Save to specific file
  python svg_modifier.py input.svg               # Creates input_swell.svg
  python svg_modifier.py *.svg                   # Creates multiple *_swellable.svg files
        """
    )
    
    parser.add_argument('input_files', nargs='+', help='Input SVG file(s)')
    parser.add_argument('-o', '--output', help='Output file (only for single input file)')
    
    args = parser.parse_args()
    
    # Handle multiple input files
    if len(args.input_files) > 1:
        if args.output:
            print("Error: Cannot specify output file when processing multiple input files")
            return 1
        
        success_count = 0
        for input_file in args.input_files:
            if process_svg_file(input_file):
                success_count += 1
            print()  # Empty line between files
        
        print(f"Successfully processed {success_count}/{len(args.input_files)} files")
        
    else:
        # Handle single input file
        input_file = args.input_files[0]
        if process_svg_file(input_file, args.output):
            return 0
        else:
            return 1


if __name__ == '__main__':
    sys.exit(main())