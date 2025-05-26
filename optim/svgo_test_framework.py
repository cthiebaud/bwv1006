#!/usr/bin/env python3
"""
SVGO Incremental Test Framework for Musical Notation SVGs

This script builds an optimal SVGO configuration by testing each plugin
individually against your actual functionality tests.

Usage: python3 svgo_test_framework.py input.svg test_command
Example: python3 svgo_test_framework.py input.svg "npm test"
"""

import json
import subprocess
import sys
import tempfile
import os
import shutil
from pathlib import Path
from datetime import datetime

# All SVGO preset-default plugins in alphabetical order
PLUGINS = [
"addAttributesToSVGElement",
"addClassesToSVGElement",
"cleanupAttrs",
"cleanupAttrs",
"cleanupEnableBackground",
"cleanupIds",
"cleanupListOfValues",
"cleanupNumericValues",
"collapseGroups",
"convertColors",
"convertEllipseToCircle",
"convertOneStopGradients",
"convertPathData",
"convertShapeToPath",
"convertStyleToAttrs",
"convertTransform",
"inlineStyles",
"mergePaths",
"mergeStyles",
"minifyStyles",
"moveElemsAttrsToGroup",
"moveGroupAttrsToElems",
"Plugin Architecture",
"PluginscleanupAttrs",
"prefixIds",
"removeAttributesBySelector",
"removeAttrs",
"removeComments",
"removeDeprecatedAttrs",
"removeDesc",
"removeDimensions",
"removeDoctype",
"removeEditorsNSData",
"removeElementsByAttr",
"removeEmptyAttrs",
"removeEmptyContainers",
"removeEmptyText",
"removeHiddenElems",
"removeMetadata",
"removeNonInheritableGroupAttrs",
"removeOffCanvasPaths",
"removeRasterImages",
"removeScriptElement",
"removeStyleElement",
"removeTitle",
"removeUnknownsAndDefaults",
"removeUnusedNS",
"removeUselessDefs",
"removeUselessStrokeAndFill",
"removeViewBox",
"removeXlink",
"removeXMLNS",
"removeXMLProcInst",
"reusePaths",
"sortAttrs",
"sortDefsChildren",
]

class IncrementalSVGOTester:
    def __init__(self, input_file, test_command=None, size_threshold=1.0):
        self.input_file = Path(input_file)
        self.test_command = test_command
        self.size_threshold = size_threshold  # Minimum size reduction percentage
        self.working_dir = Path.cwd()
        self.test_dir = Path(f"svgo_incremental_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # Results
        self.working_plugins = []
        self.failed_plugins = []
        self.useless_plugins = []  # New: plugins that don't provide meaningful size reduction
        self.test_results = []
        
        # Create test directory
        self.test_dir.mkdir(exist_ok=True)
        print(f"🧪 Incremental test results will be saved to: {self.test_dir}")
        print(f"📏 Size reduction threshold: {self.size_threshold}%")
        
    def get_file_size(self, svg_path):
        """Get file size"""
        return svg_path.stat().st_size if svg_path.exists() else 0
    
    def run_svgo_with_plugins(self, plugins, output_file):
        """Run SVGO with specific plugins"""
        if not plugins:
            # No plugins = copy original file
            shutil.copy2(self.input_file, output_file)
            return True
        
        # Create SVGO config
        config = {
            "plugins": plugins,
            "multipass": True
        }
        
        # Write config as ES module
        config_content = f"""export default {json.dumps(config, indent=2)};"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mjs', delete=False) as f:
            f.write(config_content)
            config_file = f.name
        
        try:
            # Run SVGO
            result = subprocess.run([
                'npx', 'svgo',
                '--config', config_file,
                '--input', str(self.input_file),
                '--output', str(output_file)
            ], capture_output=True, text=True, timeout=30)
            
            success = result.returncode == 0 and output_file.exists()
            
            if not success:
                print(f"      ❌ SVGO failed: {result.stderr}")
            
            return success
            
        except subprocess.TimeoutExpired:
            print(f"      ❌ SVGO timeout")
            return False
        except Exception as e:
            print(f"      ❌ SVGO error: {e}")
            return False
        finally:
            # Clean up temp config file
            try:
                os.unlink(config_file)
            except:
                pass
    
    def run_functionality_test(self, svg_file):
        """Run the functionality test on the optimized SVG"""
        if self.test_command:
            # Run custom test command if provided
            # Get absolute paths for comparison
            svg_file = Path(svg_file).resolve()
            target_svg = (self.working_dir / self.input_file.name).resolve()
            
            # If testing the original file in its original location, just run the test
            if svg_file == target_svg:
                print("      ℹ️  Testing original file in place")
                try:
                    result = subprocess.run(
                        self.test_command,
                        shell=True,
                        cwd=self.working_dir,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    
                    success = result.returncode == 0
                    
                    if not success:
                        print(f"      ❌ Test failed: {result.stderr}")
                    
                    return success
                    
                except subprocess.TimeoutExpired:
                    print(f"      ❌ Test timeout")
                    return False
                except Exception as e:
                    print(f"      ❌ Test error: {e}")
                    return False
            
            # For different files, we need to swap them temporarily
            backup_file = None
            
            try:
                # Backup original if it exists and is different
                if target_svg.exists():
                    backup_file = target_svg.with_suffix('.backup')
                    shutil.copy2(target_svg, backup_file)
                
                # Copy test SVG to expected location
                shutil.copy2(svg_file, target_svg)
                
                # Run test command
                result = subprocess.run(
                    self.test_command,
                    shell=True,
                    cwd=self.working_dir,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                success = result.returncode == 0
                
                if not success:
                    print(f"      ❌ Test failed: {result.stderr}")
                
                return success
                
            except subprocess.TimeoutExpired:
                print(f"      ❌ Test timeout")
                return False
            except Exception as e:
                print(f"      ❌ Test error: {e}")
                return False
            finally:
                # Restore original file
                if backup_file and backup_file.exists():
                    shutil.move(backup_file, target_svg)
                elif target_svg.exists() and svg_file != target_svg:
                    target_svg.unlink()
        else:
            # No custom test command - use SVG structure validator
            print("      🔍 Running SVG structure validation...")
            try:
                # Run the svg_validator.py script
                validator_script = Path(__file__).parent / "svg_validator.py"
                result = subprocess.run([
                    'python3', str(validator_script), str(svg_file)
                ], capture_output=True, text=True, timeout=30)
                
                success = result.returncode == 0
                
                if success:
                    print("      ✅ SVG structure validation: PASSED")
                else:
                    print("      ❌ SVG structure validation: FAILED")
                    # Print the validator output for debugging
                    if result.stdout:
                        for line in result.stdout.strip().split('\n'):
                            if line.strip():
                                print(f"         {line}")
                
                return success
                
            except subprocess.TimeoutExpired:
                print(f"      ❌ Validator timeout")
                return False
            except Exception as e:
                print(f"      ❌ Validator error: {e}")
                return False
    
    def test_baseline(self):
        """Test that the original file passes functionality tests"""
        print("📊 Testing baseline (original file)...")
        
        original_size = self.get_file_size(self.input_file)
        print(f"   📏 Original size: {original_size:,} bytes")
        
        passes_test = self.run_functionality_test(self.input_file)
        
        if passes_test:
            print(f"   ✅ Baseline functionality test: PASSED")
            return True
        else:
            print(f"   ❌ Baseline functionality test: FAILED")
            print(f"   🚨 Cannot continue - original file must pass tests!")
            return False
    
    def test_plugin_incrementally(self, plugin):
        """Test adding one plugin to the current working set"""
        test_plugins = self.working_plugins + [plugin]
        
        print(f"   🔧 Testing with {len(test_plugins)} plugins: {self.working_plugins} + {plugin}")
        
        # Generate optimized SVG
        test_file = self.test_dir / f"test_{len(test_plugins):02d}_{plugin}.svg"
        
        # Get baseline size (before adding this plugin)
        if self.working_plugins:
            # Find the last working plugin file
            last_working_plugin = self.working_plugins[-1]
            # Find the file for that plugin
            baseline_file = None
            for existing_file in self.test_dir.glob("*.svg"):
                if existing_file.stem.endswith(last_working_plugin):
                    baseline_file = existing_file
                    break
            baseline_size = self.get_file_size(baseline_file) if baseline_file else self.get_file_size(self.input_file)
        else:
            baseline_size = self.get_file_size(self.input_file)
        
        # Run SVGO
        svgo_success = self.run_svgo_with_plugins(test_plugins, test_file)
        if not svgo_success:
            print(f"      ❌ SVGO failed with {len(test_plugins)} plugins")
            return False
        
        # Get new file size
        new_size = self.get_file_size(test_file)
        original_size = self.get_file_size(self.input_file)
        
        # Calculate reductions (negative = good reduction, positive = bad increase)
        total_reduction = ((original_size - new_size) / original_size) * 100
        plugin_contribution = ((baseline_size - new_size) / baseline_size) * 100 if baseline_size > 0 else 0
        
        print(f"      📏 Size: {new_size:,} bytes ({total_reduction:+.1f}% total)")
        print(f"      📊 This plugin's contribution: {plugin_contribution:.2f}%")
        
        # Test functionality first
        test_success = self.run_functionality_test(test_file)
        
        if not test_success:
            print(f"      ❌ Functionality test: FAILED")
            print(f"      💥 Plugin '{plugin}' breaks functionality when combined with: {self.working_plugins}")
            return False
        
        print(f"      ✅ Functionality test: PASSED")
        
        # Check if plugin provides meaningful size reduction
        if plugin_contribution < self.size_threshold:
            print(f"      ⚠️  Plugin contribution ({plugin_contribution:.2f}%) below threshold ({self.size_threshold}%)")
            return "useless"
        
        return True
    
    def build_optimal_config(self):
        """Build optimal config by testing each plugin incrementally"""
        print(f"🚀 Building optimal SVGO config for {self.input_file}")
        print(f"   Command: {self.test_command or 'No test command (manual verification needed)'}")
        
        # Test baseline first
        if not self.test_baseline():
            return False
        
        print(f"\n🔄 Testing {len(PLUGINS)} plugins incrementally...")
        
        for i, plugin in enumerate(PLUGINS, 1):
            useless_count = len(self.useless_plugins)
            useless_info = f"{useless_count} plugins marked useless" if useless_count > 0 else ""
            
            print(f"\n[{i:2}/{len(PLUGINS)}] Testing plugin: {plugin}")
            if useless_info:
                print(f"             {useless_info}")
            
            success = self.test_plugin_incrementally(plugin)
            
            if success is True:
                self.working_plugins.append(plugin)
                print(f"      ✅ ADDED to config ({len(self.working_plugins)} working total)")
            elif success == "useless":
                self.useless_plugins.append(plugin)
                print(f"      🗑️  MARKED as useless ({len(self.useless_plugins)} useless total)")
            else:  # success is False
                self.failed_plugins.append(plugin)
                print(f"      ❌ REJECTED ({len(self.failed_plugins)} failed total)")
            
            # Record result
            self.test_results.append({
                "plugin": plugin,
                "success": success,
                "total_plugins": len(self.working_plugins)
            })
        
        print(f"\n📋 Final Results:")
        print(f"   ✅ Working plugins: {len(self.working_plugins)}")
        print(f"   🗑️  Useless plugins: {len(self.useless_plugins)}")
        print(f"   ❌ Failed plugins: {len(self.failed_plugins)}")
        
        return True
    
    def generate_final_config(self):
        """Generate the final optimal SVGO configuration"""
        if not self.working_plugins:
            print("⚠️  No working plugins found - generating empty config")
        
        # Generate final optimized SVG
        final_svg = self.test_dir / f"{self.input_file.stem}_optimized.svg"
        svgo_success = self.run_svgo_with_plugins(self.working_plugins, final_svg)
        
        if svgo_success:
            original_size = self.get_file_size(self.input_file)
            final_size = self.get_file_size(final_svg)
            reduction = ((original_size - final_size) / original_size) * 100
            
            print(f"\n🎯 Final Optimization Results:")
            print(f"   📏 Original: {original_size:,} bytes")
            print(f"   📏 Optimized: {final_size:,} bytes")
            print(f"   📉 Reduction: {reduction:.1f}%")
        
        # Generate SVGO config file
        config_file = self.test_dir / "svgo.config.js"
        
        config_content = f"""// Optimal SVGO configuration for musical notation SVG
// Generated by Incremental SVGO Test Framework
// Original size: {self.get_file_size(self.input_file):,} bytes
// Optimized size: {self.get_file_size(final_svg):,} bytes  
// Size reduction: {((self.get_file_size(self.input_file) - self.get_file_size(final_svg)) / self.get_file_size(self.input_file)) * 100:.1f}%
// Working plugins: {len(self.working_plugins)}/{len(PLUGINS)}

module.exports = {{
  plugins: {json.dumps(self.working_plugins, indent=4)},
  multipass: true
}};
"""
        
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        # Generate report
        report_file = self.test_dir / "test_report.json"
        report = {
            "timestamp": datetime.now().isoformat(),
            "input_file": str(self.input_file),
            "test_command": self.test_command,
            "size_threshold": self.size_threshold,
            "original_size": self.get_file_size(self.input_file),
            "final_size": self.get_file_size(final_svg) if svgo_success else 0,
            "working_plugins": self.working_plugins,
            "failed_plugins": self.failed_plugins,
            "useless_plugins": self.useless_plugins,
            "detailed_results": self.test_results
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Generate usage instructions
        usage_file = self.test_dir / "USAGE.md"
        usage_content = f"""# Optimal SVGO Configuration

## Results Summary
- **Working plugins**: {len(self.working_plugins)}/{len(PLUGINS)}
- **Size reduction**: {((self.get_file_size(self.input_file) - self.get_file_size(final_svg)) / self.get_file_size(self.input_file)) * 100:.1f}%
- **Failed plugins**: {', '.join(self.failed_plugins) if self.failed_plugins else 'None'}
- **Useless plugins**: {', '.join(self.useless_plugins) if self.useless_plugins else 'None'}

## Usage

### Replace your current config:
```bash
# Backup your current config
cp svgo.config.js svgo.config.js.backup

# Use the optimal config
cp {self.test_dir}/svgo.config.js ./svgo.config.js
```

### Test the optimized SVG:
```bash
# Copy the optimized SVG
cp {final_svg} ./optimized_output.svg

# Run your tests
{self.test_command or 'Run your functionality tests manually'}
```

## Plugin Analysis

### Working Plugins (provide good size reduction + maintain functionality)
{chr(10).join(f'- `{plugin}`' for plugin in self.working_plugins) if self.working_plugins else '- None'}

### Failed Plugins (break functionality)
{chr(10).join(f'- `{plugin}`' for plugin in self.failed_plugins) if self.failed_plugins else '- None (all plugins worked!)'}

### Useless Plugins (< {self.size_threshold}% size reduction)
{chr(10).join(f'- `{plugin}`' for plugin in self.useless_plugins) if self.useless_plugins else '- None (all plugins were effective!)'}
"""
        
        with open(usage_file, 'w') as f:
            f.write(usage_content)
        
        print(f"\n📁 Generated files:")
        print(f"   ✅ Optimal config: {config_file}")
        print(f"   ✅ Optimized SVG: {final_svg}")
        print(f"   ✅ Detailed report: {report_file}")
        print(f"   ✅ Usage guide: {usage_file}")
        
        return config_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 svgo_test_framework.py <input.svg> [test_command] [size_threshold]")
        print("Examples:")
        print("  python3 svgo_test_framework.py input.svg 'npm test'")
        print("  python3 svgo_test_framework.py input.svg 'make test' 1.5")
        print("  python3 svgo_test_framework.py input.svg  # Manual testing, 1% threshold")
        print("  python3 svgo_test_framework.py input.svg '' 0.15  # Manual testing, 0.15% threshold")
        sys.exit(1)
    
    input_file = sys.argv[1]
    test_command = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else None
    size_threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 0.15
    
    if not Path(input_file).exists():
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)
    
    # Check if SVGO is available
    try:
        subprocess.run(['npx', 'svgo', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ SVGO not available. Install with: npm install -g svgo")
        sys.exit(1)
    
    # Run incremental testing
    tester = IncrementalSVGOTester(input_file, test_command, size_threshold)
    
    if tester.build_optimal_config():
        config_file = tester.generate_final_config()
        print(f"\n🎉 Success! Optimal SVGO config generated.")
        print(f"💡 To use: cp {config_file} ./svgo.config.js")
    else:
        print(f"\n❌ Failed to build optimal config")
        sys.exit(1)

if __name__ == "__main__":
    main()