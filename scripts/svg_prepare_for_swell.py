#!/usr/bin/env python3
"""
svg_prepare_for_swell.py

SVG Animation Preparation Pipeline
=================================

This script prepares LilyPond-generated SVG files for CSS/JavaScript animation
by restructuring the DOM hierarchy. It specifically handles the transformation
needed for "swell" animations (scaling effects) on musical noteheads.

Problem Solved:
LilyPond generates SVG with this structure:
  <a href="...">
    <path transform="translate(x,y)" />  ← Transform on path, hard to animate
  </a>

This script transforms it to:
  <g href="..." transform="translate(x,y)">  ← Transform on group, easy to animate
    <path />
  </g>

This restructuring enables smooth CSS animations on noteheads while preserving
all musical cross-reference links needed for score interaction.

Usage:
    python svg_prepare_for_swell.py input.svg [output.svg]
    python svg_prepare_for_swell.py input.svg  # Creates input_swellable.svg
    python svg_prepare_for_swell.py *.svg      # Batch process multiple files
"""

import xml.etree.ElementTree as ET
import sys
import argparse
from pathlib import Path

# =============================================================================
# SVG NAMESPACE CONFIGURATION
# =============================================================================

# Register XML namespaces to prevent ns0: prefixes in output
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

# =============================================================================
# CORE TRANSFORMATION ENGINE
# =============================================================================

def modify_svg_paths(svg_content):
    """
    Transform SVG structure to enable CSS animations on musical noteheads.
    
    This function restructures the SVG DOM by moving transform attributes from
    path elements to parent group elements, making it possible to animate
    noteheads with CSS transforms while preserving musical functionality.
    
    Args:
        svg_content (str): Original SVG content as string
        
    Returns:
        tuple: (modified_svg_string, summary_message)
               - modified_svg_string: Transformed SVG content
               - summary_message: Human-readable transformation summary
    
    Transformation Process:
    1. Parse SVG and build parent-child relationship map
    2. Find all <a> elements with href attributes (musical cross-references)
    3. Locate child <path> elements with transform attributes
    4. Create new <g> wrapper with href and transform
    5. Move path inside new group and remove original transform
    6. Replace original anchor with new group structure
    """
    
    print("   🔍 Parsing SVG structure...")
    
    # =================================================================
    # SVG PARSING AND VALIDATION
    # =================================================================
    
    try:
        svg_root = ET.fromstring(svg_content)
    except ET.ParseError as parse_error:
        error_message = f"SVG parsing failed: {parse_error}"
        print(f"   ❌ {error_message}")
        return svg_content, error_message
    
    print("   🗺️  Building element relationship map...")
    
    # Create parent-child mapping for DOM manipulation
    # This allows us to find and replace elements in the tree
    parent_map = {child: parent for parent in svg_root.iter() for child in parent}
    
    # =================================================================
    # ANCHOR ELEMENT DISCOVERY
    # =================================================================
    
    print("   🔗 Finding musical cross-reference anchors...")
    
    musical_anchors = []
    
    def find_href_anchors(element):
        """Recursively find all <a> elements with href attributes."""
        # Check if this is an anchor element (with or without namespace)
        if element.tag == 'a' or element.tag.endswith('}a'):
            # Look for href attribute (various namespace formats)
            for attribute_name in element.attrib:
                if attribute_name == 'href' or attribute_name.endswith('}href'):
                    musical_anchors.append(element)
                    break
        
        # Recursively check all children
        for child_element in element:
            find_href_anchors(child_element)
    
    find_href_anchors(svg_root)
    print(f"   📊 Found {len(musical_anchors)} musical anchor elements")
    
    # =================================================================
    # TRANSFORMATION PROCESSING
    # =================================================================
    
    transformations_applied = 0
    
    print("   🔄 Applying DOM transformations...")
    
    for anchor_element in musical_anchors:
        # Extract href value for preservation
        href_value = None
        for attr_name, attr_value in anchor_element.attrib.items():
            if attr_name == 'href' or attr_name.endswith('}href'):
                href_value = attr_value
                break
        
        # Find direct child path elements that need transformation
        child_paths = []
        for child in anchor_element:
            if child.tag == 'path' or child.tag.endswith('}path'):
                child_paths.append(child)
        
        # Process each path element
        for path_element in child_paths:
            transform_value = path_element.get('transform')
            
            if transform_value:
                print(f"      🎯 Transforming path with: {transform_value}")
                
                # Create new group element with proper namespace
                if '{http://www.w3.org/2000/svg}' in path_element.tag:
                    new_group = ET.Element('{http://www.w3.org/2000/svg}g')
                else:
                    new_group = ET.Element('g')
                
                # Transfer attributes to new group
                if href_value:
                    new_group.set('href', href_value)  # Preserve musical link
                new_group.set('transform', transform_value)  # Move transform up
                
                # Clean path element and add to group
                path_element.attrib.pop('transform', None)  # Remove original transform
                new_group.append(path_element)  # Path becomes child of group
                
                # Replace anchor with new group in parent
                anchor_parent = parent_map.get(anchor_element)
                if anchor_parent is not None:
                    parent_children = list(anchor_parent)
                    anchor_index = parent_children.index(anchor_element)
                    anchor_parent.insert(anchor_index, new_group)
                    anchor_parent.remove(anchor_element)
                else:
                    # Handle case where anchor is the root element
                    svg_root = new_group
                
                transformations_applied += 1
                break  # Only process first transformable path per anchor
    
    # =================================================================
    # RESULT GENERATION
    # =================================================================
    
    # Generate summary message
    if transformations_applied > 0:
        summary = f"Transformed {transformations_applied} notehead(s) for animation"
        print(f"   ✅ {summary}")
    else:
        summary = "No transformations needed - SVG already animation-ready"
        print(f"   ℹ️  {summary}")
    
    # Convert modified tree back to string
    print("   📝 Serializing modified SVG...")
    xml_string = ET.tostring(svg_root, encoding='unicode', xml_declaration=False)
    
    # Preserve original XML declaration if present
    if svg_content.strip().startswith('<?xml'):
        xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_string
    
    return xml_string, summary

# =============================================================================
# FILE PROCESSING INTERFACE
# =============================================================================

def process_svg_file(input_path, output_path=None):
    """
    Process a single SVG file and apply animation preparation transformations.
    
    Args:
        input_path (str): Path to input SVG file
        output_path (str, optional): Path for output. If None, creates input_swellable.svg
        
    Returns:
        bool: True if processing succeeded, False otherwise
    """
    
    input_file = Path(input_path)
    
    # =================================================================
    # INPUT VALIDATION
    # =================================================================
    
    if not input_file.exists():
        print(f"❌ Error: Input file '{input_path}' does not exist")
        return False
    
    if not input_file.suffix.lower() == '.svg':
        print(f"⚠️  Warning: File '{input_path}' does not have .svg extension")
    
    print(f"🎼 Processing: {input_path}")
    
    try:
        # =============================================================
        # FILE LOADING AND PROCESSING
        # =============================================================
        
        print("   📖 Reading SVG file...")
        with open(input_file, 'r', encoding='utf-8') as file_handle:
            original_svg_content = file_handle.read()
        
        # Apply transformations
        modified_svg_content, transformation_summary = modify_svg_paths(original_svg_content)
        
        # =============================================================
        # OUTPUT PATH DETERMINATION
        # =============================================================
        
        if output_path is None:
            # Generate descriptive output filename
            output_file = input_file.parent / f"{input_file.stem}_swellable.svg"
        else:
            output_file = Path(output_path)
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # =============================================================
        # FILE WRITING
        # =============================================================
        
        print(f"   💾 Writing transformed SVG...")
        with open(output_file, 'w', encoding='utf-8') as output_handle:
            output_handle.write(modified_svg_content)
        
        print(f"✅ Success: {output_file}")
        print(f"   📊 {transformation_summary}")
        return True
        
    except Exception as processing_error:
        print(f"❌ Error processing '{input_path}': {processing_error}")
        return False

# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def main():
    """Main function handling command line arguments and batch processing."""
    
    parser = argparse.ArgumentParser(
        description='Prepare SVG files for CSS animation by restructuring DOM hierarchy',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python svg_prepare_for_swell.py score.svg output.svg    # Specific output file
  python svg_prepare_for_swell.py score.svg               # Creates score_swellable.svg
  python svg_prepare_for_swell.py *.svg                   # Batch process multiple files
        """
    )
    
    parser.add_argument('input_files', nargs='+', help='Input SVG file(s) to process')
    parser.add_argument('-o', '--output', help='Output file (single input only)')
    
    args = parser.parse_args()
    
    print("🚀 SVG Animation Preparation Pipeline")
    print("=" * 45)
    
    # =================================================================
    # BATCH VS SINGLE FILE PROCESSING
    # =================================================================
    
    if len(args.input_files) > 1:
        # Batch processing mode
        if args.output:
            print("❌ Error: Cannot specify output file for batch processing")
            return 1
        
        print(f"📋 Batch processing {len(args.input_files)} files:")
        for i, filename in enumerate(args.input_files, 1):
            print(f"   {i}. {filename}")
        print()
        
        successful_count = 0
        for input_file in args.input_files:
            if process_svg_file(input_file):
                successful_count += 1
            print()  # Separator between files
        
        # Batch summary
        print("=" * 45)
        print(f"🎯 Batch Processing Complete")
        print(f"   ✅ Successfully processed: {successful_count}/{len(args.input_files)} files")
        
        if successful_count == len(args.input_files):
            print("   🎉 All files processed successfully!")
        else:
            failed_count = len(args.input_files) - successful_count
            print(f"   ⚠️  {failed_count} files failed processing")
        
    else:
        # Single file processing mode
        input_file = args.input_files[0]
        success = process_svg_file(input_file, args.output)
        
        if success:
            print("\n🎉 Processing complete - SVG ready for animation!")
            return 0
        else:
            print("\n💥 Processing failed")
            return 1

# =============================================================================
# SCRIPT ENTRY POINT
# =============================================================================

if __name__ == '__main__':
    sys.exit(main())