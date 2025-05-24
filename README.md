# BWV 1006

![bwv1006](bwv1006.svg)

## 🛠️ Building the Project

This project uses [`invoke`](https://www.pyinvoke.org/) as a task runner to build LilyPond scores, post-process SVGs, and generate synchronized animation data from MIDI.

### 📦 Step 1: Install prerequisites

Make sure you have the following installed:

* [Docker](https://www.docker.com/) — required for LilyPond compilation
* Python 3.8 or higher
* [Node.js](https://nodejs.org/) — required for SVG optimization (SVGO)
* The `invoke` package:

```bash
pip install invoke
```

### 📦 Install dependencies

```bash
pip install -r scripts/requirements.txt
```

Alternatively, you can install packages manually:

```bash
pip install librosa matplotlib midi2audio mido numpy pandas soundfile
```

For SVG optimization, SVGO is automatically handled via npx (comes with Node.js):

```bash
# No additional installation needed - npx will download SVGO as needed
# Alternatively, you can install SVGO globally:
npm install -g svgo
```

### ⚙️ Step 2: Build everything

Run this from the project root:

```bash
invoke all
```

This will:

1. Compile `bwv1006.ly` to PDF and SVG using LilyPond in Docker
2. Post-process the SVG (remove tab anchors, tighten viewbox, optimize, and prepare for swell animations)
3. Generate the one-line score used for synchronization
4. Extract and align MIDI and SVG data
5. Produce a `bwv1006_json_notes.json` file for animation timing

You can also run steps individually:

```bash
invoke build-pdf
invoke build-svg
invoke postprocess-svg    # Handles all SVG post-processing steps
invoke build-svg-one-line
invoke json-notes
```

Add `--force` to any task to force a rebuild regardless of file changes.

### 🎨 SVG Post-Processing

The `postprocess-svg` task performs multiple optimization steps:
- Removes href anchors from tabs
- Tightens the SVG viewbox for better display
- Optimizes the SVG using SVGO to reduce file sizes by 10-30%
- Prepares the SVG for swell animations

The optimization preserves:
- Musical notation positioning and structure
- `data-bar` attributes needed for bar highlighting
- Element IDs required for note synchronization
- All animation-related functionality

---

## 🚀 Run the Project Locally

After building, you can serve the output locally using Python:

```bash
python3 -m http.server
```

Then open your browser at:

```
http://localhost:8000
```

to view the animated score.


![Bach's Seal](media/Bach_Seal_blurred_gray_bg_final.svg)