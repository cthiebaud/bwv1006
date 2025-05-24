#!/usr/bin/env python3
"""
svg_remove_hrefs_in_tabs.py

Musical Score Link Cleanup Utility
==================================

This script removes hyperlinks from non-musical elements in LilyPond-generated
SVG files, specifically targeting tablature numbers and text annotations while
preserving essential notehead links needed for interactive score features.

Problem Addressed:
LilyPond embeds cross-reference links (href attributes) in ALL clickable elements,
including tablature numbers, fingering annotations, and text markings. For score
animation applications, we typically only want links on actual noteheads, as
other links can interfere with user interaction and animation logic.

Selective Link Removal:
- REMOVES links from: <text> elements (numbers, annotations, lyrics)
- REMOVES links from: <rect> elements (boxes, tablature backgrounds)  
- PRESERVES links on: <path> elements (actual noteheads and musical symbols)

This creates cleaner SVG files optimized for musical score interaction.
"""

from xml.etree import ElementTree as ET
from pathlib import Path

# =============================================================================
# XML NAMESPACE CONFIGURATION
# =============================================================================

# Standard SVG and XLink namespaces used in LilyPond-generated files
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"

# Register namespaces to ensure clean output without ns0: prefixes
ET.register_namespace("", SVG_NAMESPACE)      # SVG as default namespace
ET.register_namespace("xlink", XLINK_NAMESPACE)  # XLink for href attributes

# Namespace map for XPath queries
NAMESPACE_MAP = {
    "svg": SVG_NAMESPACE, 
    "xlink": XLINK_NAMESPACE
}

# =============================================================================
# LINK CLEANUP ENGINE
# =============================================================================

def remove_href_from_tab_links(input_path: Path, output_path: Path):
    """
    Remove hyperlinks from text and rectangular elements in SVG musical scores.
    
    This function processes LilyPond-generated SVG files to selectively remove
    href attributes from elements that typically contain tablature numbers,
    fingering annotations, or other textual content, while preserving links
    on actual musical noteheads.
    
    Args:
        input_path (Path): Path to input SVG file with embedded links
        output_path (Path): Path where cleaned SVG will be written
        
    Process:
    1. Parse SVG file and locate all anchor (<a>) elements
    2. Check each anchor for text or rectangle child elements
    3. Remove href attributes from anchors containing text/rect elements
    4. Preserve href attributes on anchors containing only musical paths
    5. Write cleaned SVG maintaining all other attributes and structure
    
    Target Elements for Link Removal:
    - <text>: Tablature numbers, fingerings, lyrics, tempo markings
    - <rect>: Background boxes, tablature grids, measure boundaries
    
    Preserved Elements:
    - <path>: Noteheads, stems, beams, slurs (core musical notation)
    - <g>: Grouping elements (structure preservation)
    """
    
    print(f"🎼 Processing musical score: {input_path.name}")
    
    # =================================================================
    # SVG LOADING AND PARSING
    # =================================================================
    
    try:
        print("   📖 Loading SVG file...")
        svg_tree = ET.parse(input_path)
        svg_root = svg_tree.getroot()
        
    except ET.ParseError as parse_error:
        print(f"   ❌ SVG parsing failed: {parse_error}")
        return
    except FileNotFoundError:
        print(f"   ❌ Input file not found: {input_path}")
        return
    
    # =================================================================
    # LINK ANALYSIS AND REMOVAL
    # =================================================================
    
    print("   🔍 Analyzing anchor elements for link removal...")
    
    removed_link_count = 0
    total_anchor_count = 0
    text_anchor_count = 0
    rect_anchor_count = 0
    
    # Find all anchor elements using XPath with proper namespaces
    for anchor_element in svg_root.findall(".//svg:a", NAMESPACE_MAP):
        total_anchor_count += 1
        
        # Check for text content (tablature numbers, annotations, etc.)
        contains_text = anchor_element.find(".//svg:text", NAMESPACE_MAP) is not None
        
        # Check for rectangular elements (backgrounds, grids, etc.)
        contains_rect = anchor_element.find(".//svg:rect", NAMESPACE_MAP) is not None
        
        # Track statistics for reporting
        if contains_text:
            text_anchor_count += 1
        if contains_rect:
            rect_anchor_count += 1
        
        # Remove href if anchor contains text or rect elements
        if contains_text or contains_rect:
            # Handle both namespaced and non-namespaced href attributes
            href_removed = False
            
            # Try namespaced href first (most common in LilyPond output)
            namespaced_href = f"{{{XLINK_NAMESPACE}}}href"