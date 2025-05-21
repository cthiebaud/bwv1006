from xml.etree import ElementTree as ET
from pathlib import Path

# XML namespaces
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"

# Register SVG as the default (no prefix)
ET.register_namespace("", SVG_NS)
ET.register_namespace("xlink", XLINK_NS)

# Use the same NSMAP for XPath searches
NSMAP = {"svg": SVG_NS, "xlink": XLINK_NS}

def remove_href_from_tab_links(in_path: Path, out_path: Path):
    """
    Load an SVG file, remove hrefs from <a> elements that contain <text> or <rect>,
    and save to a new file.

    Args:
        in_path (Path): Input SVG file path
        out_path (Path): Output SVG file path
    """
    tree = ET.parse(in_path)
    root = tree.getroot()
    removed_count = 0

    for a in root.findall(".//svg:a", NSMAP):
        has_text = a.find(".//svg:text", NSMAP) is not None
        has_rect = a.find(".//svg:rect", NSMAP) is not None
        if has_text or has_rect:
            if f"{{{XLINK_NS}}}href" in a.attrib:
                del a.attrib[f"{{{XLINK_NS}}}href"]
                removed_count += 1
            elif "href" in a.attrib:
                del a.attrib["href"]
                removed_count += 1

    tree.write(out_path, encoding="utf-8", xml_declaration=True)
    print(f"💾 Saved: {out_path} [ removed href from {removed_count} <a> elements ]")

# Example usage:
if __name__ == "__main__":
    input_svg = Path("bwv1006.svg")
    output_svg = Path("bwv1006_svg_no_hrefs_in_tabs.svg")
    remove_href_from_tab_links(input_svg, output_svg)
