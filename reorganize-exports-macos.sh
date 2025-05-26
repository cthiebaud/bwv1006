#!/bin/bash

# reorganize-exports-macos.sh
# Script to move files to exports/ directory and update all references
# macOS compatible version

echo "🔄 Starting reorganization to exports/ directory..."

# Step 1: Create exports directory and move files
echo "📁 Creating exports/ directory and moving files..."
mkdir -p exports
mv bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg exports/
mv bwv1006_json_notes.json exports/
mv bwv1006.config.yaml exports/

echo "✅ Files moved to exports/"

# Step 2: Update all file references (macOS sed syntax)
echo "🔧 Updating file references..."

# Update tasks.py
echo "  📝 Updating tasks.py..."
sed -i '' 's|"bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg"|"exports/bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg"|g' tasks.py
sed -i '' 's|"bwv1006_json_notes.json"|"exports/bwv1006_json_notes.json"|g' tasks.py

# Update README.md
echo "  📝 Updating README.md..."
sed -i '' 's|bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg|exports/bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg|g' README.md
sed -i '' 's|bwv1006_json_notes.json|exports/bwv1006_json_notes.json|g' README.md

# Update scripts/svg_href_cleaner.py
echo "  📝 Updating scripts/svg_href_cleaner.py..."
sed -i '' 's|bwv1006_json_notes.json|exports/bwv1006_json_notes.json|g' scripts/svg_href_cleaner.py

# Update scripts/align_pitch_by_geometry_simplified.py
echo "  📝 Updating scripts/align_pitch_by_geometry_simplified.py..."
sed -i '' 's|bwv1006_json_notes.json|exports/bwv1006_json_notes.json|g' scripts/align_pitch_by_geometry_simplified.py

# Update tasks.mmd
echo "  📝 Updating tasks.mmd..."
sed -i '' 's|bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg|exports/bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg|g' tasks.mmd
sed -i '' 's|bwv1006_json_notes.json|exports/bwv1006_json_notes.json|g' tasks.mmd

# Update svgo documentation if it exists (optional, might be temp files)
if [ -f "svgo_incremental_20250526_031103/USAGE.md" ]; then
    echo "  📝 Updating svgo_incremental_20250526_031103/USAGE.md..."
    sed -i '' 's|bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg|exports/bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg|g' svgo_incremental_20250526_031103/USAGE.md
fi

echo "✅ All file references updated!"

# Step 3: Verification
echo "🔍 Verifying changes..."
echo ""
echo "✅ Files with updated references:"
grep -r "exports/bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg" . --exclude-dir=.git --exclude="*.sh" 2>/dev/null || echo "  (None found for SVG - might be normal)"
grep -r "exports/bwv1006_json_notes.json" . --exclude-dir=.git --exclude="*.sh" 2>/dev/null || echo "  (None found for JSON - might be normal)"

echo ""
echo "❌ Checking for any remaining old references (excluding temp/build files):"
OLD_SVG=$(grep -r "bwv1006_svg_no_hrefs_in_tabs_swellable_optimized.svg" . --exclude-dir=.git --exclude-dir=svgo_incremental_* --exclude="*.sh" --exclude="scarse.log" 2>/dev/null | grep -v "exports/")
OLD_JSON=$(grep -r "bwv1006_json_notes.json" . --exclude-dir=.git --exclude-dir=svgo_incremental_* --exclude="*.sh" --exclude="scarse.log" 2>/dev/null | grep -v "exports/")

if [ -z "$OLD_SVG" ] && [ -z "$OLD_JSON" ]; then
    echo "🎉 Perfect! No old references found in main files."
else
    echo "⚠️  Found some old references in main files:"
    [ ! -z "$OLD_SVG" ] && echo "$OLD_SVG"
    [ ! -z "$OLD_JSON" ] && echo "$OLD_JSON"
    echo ""
    echo "ℹ️  Note: References in svgo_incremental_* directories are likely temp files and can be ignored."
fi

echo ""
echo "📂 Contents of exports/ directory:"
ls -la exports/

echo ""
echo "🎉 Reorganization complete! Files moved and references updated."
echo "📝 Next steps:"
echo "   1. Test your application to make sure everything works"
echo "   2. Run: git add . && git commit -m 'Reorganize exports'"
echo "   3. Then update your web repo submodule"