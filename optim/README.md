# SVG Optimization Testing Framework

A comprehensive testing system to find optimal SVGO settings for musical notation SVGs while preserving JavaScript functionality. This framework uses incremental testing to build the perfect SVGO configuration that maximizes file size reduction without breaking interactive features.

## 🚀 Quick Start

### Prerequisites
```bash
# Install SVGO
npm install -g svgo

# Ensure Python 3 is available
python3 --version
```

### Step 1: Run Incremental Optimization Testing
```bash
# Test with automatic SVG structure validation (recommended)
python3 svgo_test_framework.py your_score.svg

# Test with custom functionality test command
python3 svgo_test_framework.py your_score.svg "python3 test_my_svg.py"

# Test with custom size threshold (default 1.0%)
python3 svgo_test_framework.py your_score.svg "" 0.5
```

### Step 2: Visual Compatibility Testing (Optional)
1. Open `index.html` in your browser
2. Drag and drop the generated test SVGs from the results directory
3. The page will automatically run comprehensive tests:
   - 🎵 **Note clicking functionality** - Verifies href links work
   - 📊 **Bar highlighting** - Tests data-bar attributes
   - 💫 **Swell animations** - Validates notehead animation compatibility
   - 📐 **Responsive scaling** - Checks viewBox and scaling behavior

### Step 3: Apply Optimal Configuration
```bash
# Use the generated optimal config
cp svgo_incremental_YYYYMMDD_HHMMSS/svgo.config.js ./svgo.config.js

# Apply optimization to your SVG
npx svgo --config svgo.config.js input.svg -o optimized.svg
```

## 🧪 How It Works

### Incremental Plugin Testing (`svgo_test_framework.py`)

The framework tests each SVGO plugin individually and incrementally:

1. **Baseline Test**: Ensures original SVG passes functionality tests
2. **Incremental Testing**: Adds one plugin at a time to the working set
3. **Functionality Validation**: Runs tests after each plugin addition
4. **Size Impact Analysis**: Measures each plugin's contribution to size reduction
5. **Optimal Configuration**: Builds final config with only safe, effective plugins

**Test Phases:**
- ✅ **Pass**: Plugin maintains functionality and provides meaningful size reduction
- 🗑️ **Useless**: Plugin works but provides minimal size reduction (< threshold)
- ❌ **Failed**: Plugin breaks functionality when combined with current working set

### SVG Structure Validator (`svg_validator.py`)

Validates that optimized SVGs maintain required structure:
- **Note heads**: Elements with `href` attributes containing path children
- **Bar highlights**: Elements with `data-bar` attributes for measure highlighting
- **XML parsing**: Ensures SVG remains well-formed

### Browser Compatibility Tester (`index.html`)

Interactive web-based testing tool that provides:
- **Real-time visual feedback** during tests
- **Multiple file comparison** via drag-and-drop
- **Animated test demonstrations** (highlighting, scaling, animations)
- **Downloadable test reports** in JSON format
- **Automatic test execution** when files are loaded

## 📊 Understanding Results

### Test Output Structure
```
svgo_incremental_YYYYMMDD_HHMMSS/
├── input_optimized.svg              # Final optimized SVG
├── svgo.config.js                   # Optimal SVGO configuration
├── test_report.json                 # Detailed analysis and metrics
├── USAGE.md                         # Implementation guide
└── test_01_removeDoctype.svg        # Individual plugin test files
└── test_02_removeComments.svg       # (one for each tested plugin)
└── ...
```

## 📄 License

This framework is designed to work with your musical notation SVGs while preserving all interactive functionality. Test thoroughly before deploying to production!