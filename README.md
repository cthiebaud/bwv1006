# BWV 1006

![bwv1006](bwv1006_svg_no_hrefs_in_tabs_bounded_optimized_swellable.svg)

## 🎼 Project Overview

This project creates an interactive animated musical score from Bach's BWV 1006, synchronizing visual notation with audio playback. The build system processes LilyPond notation files through multiple stages to produce web-ready animated SVG scores with precise timing data.

## 🏗️ Build Workflow

The build process follows a sophisticated pipeline that transforms LilyPond source files into interactive web content:

*View the [complete workflow diagram](tasks.mmd) for a detailed visualization of the build process.*

### 📊 Pipeline Stages

1. **Source Processing** - LilyPond compilation to PDF, SVG, and MIDI
2. **SVG Optimization** - Multi-stage post-processing for web display  
3. **Data Extraction** - Independent extraction of timing and position data
4. **Synchronization** - Alignment of MIDI events with SVG noteheads
5. **Web Integration** - Final output ready for interactive website

## 🛠️ Building the Project

This project uses [`invoke`](https://www.pyinvoke.org/) as a task runner with intelligent caching and parallel processing capabilities.

### 📦 Prerequisites

Make sure you have the following installed:

* [Docker](https://www.docker.com/) — required for LilyPond compilation
* Python 3.8 or higher  
* [Node.js](https://nodejs.org/) — required for SVG optimization (SVGO)
* The `invoke` package:

```bash
pip install invoke
```

### 📦 Install Dependencies

```bash
pip install -r scripts/requirements.txt
```

Alternatively, install packages manually:

```bash
pip install librosa matplotlib midi2audio mido numpy pandas soundfile
```

For SVG optimization, SVGO is automatically handled via npx:

```bash
# No additional installation needed - npx will download SVGO as needed
# Alternatively, install SVGO globally:
npm install -g svgo
```

### ⚙️ Build Commands

**Complete Build:**
```bash
invoke all
```

**Individual Build Stages:**
```bash
# LilyPond compilation
invoke build-pdf          # Generate PDF score
invoke build-svg           # Generate main SVG score  
invoke build-svg-one-line  # Generate analysis SVG + MIDI

# SVG post-processing pipeline
invoke postprocess-svg     # 4-step SVG optimization

# Data extraction and alignment (runs in parallel)
invoke extract-midi-timing     # Extract MIDI note events
invoke extract-svg-noteheads   # Extract SVG notehead positions  
invoke align-data              # Synchronize MIDI with SVG data

# Convenience commands
invoke json-notes          # Complete data extraction pipeline
invoke clean               # Remove all generated files
invoke status              # Show build status and file sizes
```

**Development & Debugging:**
```bash
invoke debug-csv-files     # Check CSV file status and contents
invoke --list              # Show all available tasks
invoke <task> --force      # Force rebuild regardless of file changes
```

### 🚀 Smart Build Features

- **Intelligent Caching** - Only rebuilds changed files using SHA256 hashing
- **Independent Processing** - MIDI and SVG extraction have no interdependencies  
- **Granular Rebuilds** - Change one script without rebuilding everything
- **Comprehensive Logging** - Detailed progress reporting with emojis
- **Error Isolation** - Easy debugging with individual task execution

### 🎨 SVG Post-Processing Pipeline

The `postprocess-svg` task performs a 4-stage optimization:

1. **Link Cleanup** (`svg_remove_hrefs_in_tabs.py`) - Remove non-musical hyperlinks
2. **ViewBox Optimization** (`svg_tighten_viewbox.py`) - Minimize whitespace  
3. **File Optimization** (`svg_optimize.py`) - SVGO compression (10-30% size reduction)
4. **Animation Preparation** (`svg_prepare_for_swell.py`) - DOM restructuring for CSS animations

**Preserved Elements:**
- Musical notation positioning and structure
- Cross-reference links needed for note synchronization  
- `data-bar` attributes for measure highlighting
- All animation-related functionality

### 📈 Build Monitoring

Check build status anytime:
```bash
invoke status
```

Example output:
```
📊 Build Status:
   ✅ PDF: bwv1006.pdf (1,338,131 bytes, 2025-05-25 02:11:51)
   ✅ Animated SVG: bwv1006_svg_...swellable.svg (2,768,193 bytes, 2025-05-25 02:12:43)
   ✅ Synchronized JSON: bwv1006_json_notes.json (326,642 bytes, 2025-05-25 02:13:28)
```

---

## 🚀 Run the Project Locally

After building, serve the project locally:

```bash
python3 -m http.server
```

Then open your browser at: http://localhost:8000

## 🔧 Development Notes

- **File Dependencies** - The build system automatically tracks shared LilyPond includes
- **Docker Integration** - LilyPond runs in Docker for consistent cross-platform builds  
- **Performance** - Intelligent caching and optimized task ordering reduce build time
- **Debugging** - Use individual tasks to isolate issues in the pipeline

For detailed technical documentation, see the comprehensive comments in each script under `scripts/`.

---

![Bach's Seal](media/Bach_Seal_blurred_gray_bg_final.svg)