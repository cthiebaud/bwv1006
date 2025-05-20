from xml.etree import ElementTree as ET
from pathlib import Path
import re

# Regex to extract translate(x, y)
translate_re = re.compile(r"translate\(([-\d.]+),\s*([-\d.]+)\)")

ET.register_namespace("", "http://www.w3.org/2000/svg")  # SVG as default namespace
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")

def tighten_viewbox(input_svg_path, output_svg_path):
    input_svg = Path(input_svg_path)
    output_svg = Path(output_svg_path)

    tree = ET.parse(input_svg)
    root = tree.getroot()

    min_x = float("inf")
    min_y = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")

    # Search all <g transform="translate(x, y)"> elements
    for g in root.findall(".//{http://www.w3.org/2000/svg}g"):
        transform = g.get("transform")
        if transform:
            match = translate_re.search(transform)
            if match:
                x = float(match.group(1))
                y = float(match.group(2))
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)

    if min_x < float("inf") and min_y < float("inf"):
        vertical_margin = 5.0
        horizontal_margin = 0.0  # optional, can add too

        min_x -= horizontal_margin
        min_y -= vertical_margin
        width = (max_x - min_x) + 2 * horizontal_margin
        height = (max_y - min_y) + 2 * vertical_margin

        new_viewbox = f"{min_x:.4f} {min_y:.4f} {width:.4f} {height:.4f}"

        root.set("viewBox", new_viewbox)
        print(f"✅ Updated viewBox to: {new_viewbox}")
    else:
        print("⚠️ No valid transform=translate(x, y) found.")

    tree.write(output_svg, encoding="utf-8", xml_declaration=True)
    print(f"💾 Saved: {output_svg}")

# Example usage:
if __name__ == "__main__":
    tighten_viewbox("bwv1006_no_hrefs_in_tabs.svg", "bwv1006_no_hrefs_in_tabs_bounded.svg")
