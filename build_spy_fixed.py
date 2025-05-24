#!/usr/bin/env python3
"""
Build Spy - Discover build dependencies by monitoring filesystem activity.
FIXED VERSION with working dtruss implementation.

Usage: 
    python build_spy_fixed.py --command "cp /etc/hosts test.txt"
    python build_spy_fixed.py --command 'docker run -v "$(pwd):/work" codello/lilypond:dev bwv1006.ly'
"""

import subprocess
import json
import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime

class BuildSpy:
    def __init__(self, watch_dirs=None, ignore_patterns=None):
        self.watch_dirs = watch_dirs or [Path.cwd()]
        self.ignore_patterns = ignore_patterns or [
            r'\.git/',
            r'__pycache__/',
            r'\.pyc$',
            r'\.tmp$',
            r'/tmp/',
            r'\.log$',
            r'\.pid$'
        ]
        self.file_access = defaultdict(lambda: {'reads': set(), 'writes': set(), 'command': None})
        
    def should_ignore_file(self, filepath):
        """Check if file should be ignored based on patterns."""
        for pattern in self.ignore_patterns:
            if re.search(pattern, str(filepath)):
                return True
        return False
    
    def is_in_watch_dirs(self, filepath):
        """Check if file is within our watched directories."""
        # For absolute paths, we'll be more lenient and allow system files
        # that are commonly read (like /etc/hosts)
        if filepath.startswith('/'):
            # Allow common system files that are inputs
            if any(allowed in filepath for allowed in ['/etc/', '/usr/share/', '/opt/']):
                return True
            # Allow files in our watch directories
            path = Path(filepath).resolve()
            for watch_dir in self.watch_dirs:
                try:
                    path.relative_to(watch_dir.resolve())
                    return True
                except ValueError:
                    continue
            return False
        else:
            # For relative paths, they're usually in the current directory
            return True
    
    def run_with_dtruss(self, command, name=None):
        """Run command with dtruss monitoring on macOS (WORKING VERSION)."""
        print(f"🔍 Monitoring command with dtruss: {command}")
        
        # Use the -e flag that we know works from our testing
        # Run the command directly (not through sh -c) when possible
        cmd_parts = command.split()
        
        # For simple commands, run directly
        if len(cmd_parts) > 0 and not any(shell_char in command for shell_char in ['>', '<', '|', '&', ';', '$', '(', ')']):
            dtruss_cmd = ['sudo', 'dtruss', '-e'] + cmd_parts
            print(f"🔧 Using direct execution")
        else:
            # For complex commands with shell features, use sh -c
            dtruss_cmd = ['sudo', 'dtruss', '-e', 'sh', '-c', command]
            print(f"🔧 Using shell execution")
        
        try:
            print(f"🚀 Executing: {' '.join(dtruss_cmd)}")
            result = subprocess.run(dtruss_cmd, capture_output=True, text=True, timeout=60)
            
            print(f"📊 Command exit code: {result.returncode}")
            print(f"📄 dtruss stderr size: {len(result.stderr)} bytes")
            
            if result.stderr:
                print(f"📄 First 10 lines of dtruss output:")
                for i, line in enumerate(result.stderr.split('\n')[:10]):
                    if line.strip():
                        print(f"    {i:2d}: {line}")
            
            # Parse dtruss output 
            self.parse_dtruss_output(result.stderr, command, name)
            
        except subprocess.TimeoutExpired:
            print("⏰ dtruss timed out")
        except Exception as e:
            print(f"⚠️  dtruss error: {e}")
    
    def parse_dtruss_output(self, output, command, name):
        """Parse dtruss output to extract file operations - WORKING VERSION."""
        task_name = name or f"cmd_{len(self.file_access)}"
        reads = set()
        writes = set()
        
        print(f"🔍 Parsing dtruss output ({len(output)} chars)...")
        
        for line_num, line in enumerate(output.split('\n')):
            if not line.strip():
                continue
            
            # Skip dtrace system messages and headers
            if any(skip in line for skip in ['dtrace:', 'SYSCALL(args)', 'PID/THRD', 'ELAPSD']):
                continue
                
            # Look for file operations in dtruss output
            # Format: ELAPSED SYSCALL(args) = return
            
            if 'open(' in line and '"' in line:
                # Extract the filename from open() calls
                match = re.search(r'open\("([^"]+)', line)
                if match:
                    filepath = match.group(1).replace('\\0', '')  # Remove null terminator
                    
                    print(f"    🔍 Found open(): {filepath}")
                    
                    # Skip system/library files (but allow /etc/ files)
                    if any(skip in filepath for skip in ['/System/', '/Library/', '/dev/', '/tmp/', '/var/', '/private/']):
                        print(f"    ⏭️  Skipping system file: {filepath}")
                        continue
                    
                    # Check if file is in watch directories
                    if not self.is_in_watch_dirs(filepath):
                        print(f"    ⏭️  Skipping file outside watch dirs: {filepath}")
                        continue
                        
                    # Check ignore patterns
                    if self.should_ignore_file(filepath):
                        print(f"    ⏭️  Skipping ignored file: {filepath}")
                        continue
                    
                    print(f"    ✅ Processing file: {filepath}")
                    
                    # Determine if read or write based on flags
                    # 0x0 = O_RDONLY (read)
                    # 0x601 = O_WRONLY|O_CREAT|O_TRUNC (write)
                    # 0x201 = O_WRONLY|O_CREAT (write)
                    flags_match = re.search(r'0x([0-9A-Fa-f]+)', line)
                    if flags_match:
                        flags = int(flags_match.group(1), 16)
                        # Check for write flags (O_WRONLY=1, O_CREAT=512, O_TRUNC=1024)
                        if flags & 0x601:  # Any write flags
                            writes.add(filepath)
                            print(f"  ✏️  Write: {Path(filepath).name} (flags: 0x{flags:x})")
                        elif flags == 0x0:  # Explicit read-only
                            reads.add(filepath)
                            print(f"  📖 Read: {Path(filepath).name} (flags: 0x{flags:x})")
                        else:
                            # Default to read for other flags
                            reads.add(filepath)
                            print(f"  📖 Read: {Path(filepath).name} (flags: 0x{flags:x})")
                    else:
                        # Default to read if we can't determine flags
                        reads.add(filepath)
                        print(f"  📖 Read: {Path(filepath).name} (unknown flags)")
                        
            elif 'setattrlistat(' in line:
                # setattrlistat modifies file attributes - this is a write operation
                print(f"  ✏️  File attribute modification detected (setattrlistat)")
                
        self.file_access[task_name] = {
            'reads': reads,
            'writes': writes,
            'command': command
        }
        
        print(f"📊 Task '{task_name}': {len(reads)} reads, {len(writes)} writes")
    
    def monitor_command(self, command, name=None):
        """Monitor a command's filesystem activity."""
        if sys.platform == 'darwin':
            print("🍎 macOS detected")
            
            # For Docker commands, use directory monitoring since dtruss can't see inside containers
            if 'docker' in command.lower():
                print("🐳 Docker command detected - using directory monitoring")
                return self.run_with_simple_monitoring(command, name)
            else:
                print("🔧 Using dtruss monitoring")
                self.run_with_dtruss(command, name)
        else:
            print(f"⚠️  Platform {sys.platform} not supported in this fixed version")
            return False
        return True
    
    def run_with_simple_monitoring(self, command, name=None):
        """Simple monitoring by comparing directory contents before/after."""
        print(f"🔍 Simple monitoring (directory diff): {command}")
        
        task_name = name or f"cmd_{len(self.file_access)}"
        
        # Get initial state of watched directories
        before_files = {}
        for watch_dir in self.watch_dirs:
            if watch_dir.exists():
                for file_path in watch_dir.rglob('*'):
                    if file_path.is_file() and not self.should_ignore_file(file_path):
                        try:
                            stat = file_path.stat()
                            before_files[str(file_path)] = {
                                'mtime': stat.st_mtime,
                                'size': stat.st_size,
                                'exists': True
                            }
                        except:
                            pass
        
        print(f"📊 Found {len(before_files)} files before execution")
        
        # Run the command
        print(f"🚀 Executing: {command}")
        result = subprocess.run(['sh', '-c', command], capture_output=True, text=True)
        print(f"📊 Command exit code: {result.returncode}")
        
        if result.stdout:
            print(f"📝 stdout: {result.stdout[:200]}...")
        if result.stderr:
            print(f"⚠️  stderr: {result.stderr[:200]}...")
        
        # Small delay to ensure filesystem changes are visible
        import time
        time.sleep(0.5)
        
        # Get state after command
        after_files = {}
        for watch_dir in self.watch_dirs:
            if watch_dir.exists():
                for file_path in watch_dir.rglob('*'):
                    if file_path.is_file() and not self.should_ignore_file(file_path):
                        try:
                            stat = file_path.stat()
                            after_files[str(file_path)] = {
                                'mtime': stat.st_mtime,
                                'size': stat.st_size,
                                'exists': True
                            }
                        except:
                            pass
        
        print(f"📊 Found {len(after_files)} files after execution")
        
        # Determine reads and writes
        reads = set()
        writes = set()
        
        # Files that were modified or created = writes
        for filepath, after_info in after_files.items():
            before_info = before_files.get(filepath)
            if not before_info:
                # New file = write
                writes.add(filepath)
                print(f"  ✏️  Created: {Path(filepath).name}")
            elif (before_info['mtime'] != after_info['mtime'] or 
                  before_info['size'] != after_info['size']):
                # Modified file = write
                writes.add(filepath)
                print(f"  ✏️  Modified: {Path(filepath).name}")
        
        # For reads, infer from command and existing files
        # This is more intelligent than our previous approach
        if writes:
            # Look for files mentioned in the command
            for filepath in before_files:
                if filepath not in writes and filepath in after_files:
                    filename = Path(filepath).name
                    
                    # Check if file is mentioned in the command
                    if filename in command:
                        reads.add(filepath)
                        print(f"  📖 Command mentions: {filename}")
                        continue
                    
                    # Check for common input file patterns for the outputs we created
                    path = Path(filepath)
                    
                    # LilyPond-specific logic: if we generated a PDF/SVG, look for related .ly/.ily files
                    if any(Path(write_file).suffix.lower() in ['.pdf', '.svg'] for write_file in writes):
                        if path.suffix.lower() in ['.ly', '.ily']:
                            # Check if this file is in the same directory tree or subdirectories
                            write_stems = {Path(w).stem.split('_')[0] for w in writes}  # e.g. 'bwv1006' from 'bwv1006.pdf'
                            
                            if any(stem in path.name for stem in write_stems):
                                reads.add(filepath)
                                print(f"  📖 Related LilyPond file: {filename}")
                                continue
                            
                            # Also include files in _digit/ subdirectories (LilyPond includes)
                            if path.parent.name.startswith('_') and path.parent.name[1:].isdigit():
                                reads.add(filepath)
                                print(f"  📖 LilyPond include file: {filename}")
                                continue
                    
                    # General logic: files with similar names to outputs are likely inputs
                    elif any(Path(write_file).stem in filename or filename in Path(write_file).stem 
                           for write_file in writes):
                        if path.suffix.lower() in ['.ly', '.ily', '.py', '.yaml', '.yml', '.json']:
                            reads.add(filepath)
                            print(f"  📖 Related input: {filename}")
                            continue
                    
                    # Also check for common build input patterns
                    elif path.suffix.lower() in ['.ly', '.ily'] and any(
                        # Files that contain the base name of any output
                        any(base_name in path.name for base_name in [Path(w).stem.split('_')[0] for w in writes])
                        for w in writes
                    ):
                        reads.add(filepath)
                        print(f"  📖 Build input file: {filename}")
        
        # Additional pass: look for files that are commonly included by detected inputs
        if reads:
            main_input_files = [r for r in reads if r.endswith('.ly')]
            for main_file in main_input_files:
                try:
                    # Read the main .ly file and look for \include statements
                    content = Path(main_file).read_text(encoding='utf-8', errors='ignore')
                    
                    # Find \include "filename" patterns
                    include_patterns = re.findall(r'\\include\s+"([^"]+)"', content)
                    
                    for include_file in include_patterns:
                        # Convert relative paths to absolute
                        if not include_file.startswith('/'):
                            include_path = str(Path(main_file).parent / include_file)
                        else:
                            include_path = include_file
                        
                        # Check if this included file exists in our file list
                        if include_path in before_files and include_path not in reads:
                            reads.add(include_path)
                            print(f"  📖 Included file: {Path(include_file).name}")
                            
                except Exception as e:
                    print(f"    ⚠️  Could not parse {Path(main_file).name}: {e}")
                    continue
        
        self.file_access[task_name] = {
            'reads': reads,
            'writes': writes,
            'command': command
        }
        
        print(f"📊 Task '{task_name}': {len(reads)} reads, {len(writes)} writes")
        return len(reads) + len(writes) > 0
    
    def generate_dot_file(self, output_file='discovered_build.dot'):
        """Generate DOT file from discovered dependencies."""
        dot_content = f'''// Build pipeline discovered by monitoring filesystem activity
// Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
digraph DiscoveredBuild {{
    rankdir=TD;
    
    // Files (ellipses)
    node [shape=ellipse, style=filled, fillcolor=lightblue];
    
'''
        
        # Collect all files
        all_files = set()
        for task_info in self.file_access.values():
            all_files.update(task_info['reads'])
            all_files.update(task_info['writes'])
        
        # Add file nodes
        for filepath in sorted(all_files):
            filename = Path(filepath).name  # Just filename for readability
            dot_content += f'    "{filepath}" [label="{filename}"];\n'
        
        # Tasks (rectangles)
        dot_content += '\n    // Tasks (rectangles)\n'
        dot_content += '    node [shape=box, style=filled, fillcolor=lightgray];\n\n'
        
        for task_name, task_info in self.file_access.items():
            # Escape command for DOT
            command = task_info['command'].replace('"', '\\"')
            dot_content += f'    "{task_name}" [label="{task_name}", cmd1="{command}"];\n'
        
        # File -> Task dependencies (inputs)
        dot_content += '\n    // File inputs (blue dashed)\n'
        for task_name, task_info in self.file_access.items():
            for read_file in task_info['reads']:
                dot_content += f'    "{read_file}" -> "{task_name}" [color=blue, style=dashed];\n'
        
        # Task -> File dependencies (outputs)  
        dot_content += '\n    // File outputs (green dashed)\n'
        for task_name, task_info in self.file_access.items():
            for write_file in task_info['writes']:
                dot_content += f'    "{task_name}" -> "{write_file}" [color=green, style=dashed];\n'
        
        dot_content += '}\n'
        
        # Write DOT file
        Path(output_file).write_text(dot_content)
        print(f"✅ Generated DOT file: {output_file}")
        
        return output_file
    
    def save_results(self, output_file='build_spy_results.json'):
        """Save results to JSON for further analysis."""
        # Convert sets to lists for JSON serialization
        results = {}
        for task_name, task_info in self.file_access.items():
            results[task_name] = {
                'command': task_info['command'],
                'reads': list(task_info['reads']),
                'writes': list(task_info['writes'])
            }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Saved results to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Discover build dependencies (FIXED VERSION)')
    parser.add_argument('--command', '-c', required=True, help='Command to monitor')
    parser.add_argument('--name', '-n', help='Name for the monitored command')
    parser.add_argument('--output', '-o', default='discovered_build.dot', help='Output DOT file')
    
    args = parser.parse_args()
    
    spy = BuildSpy()
    
    # Monitor single command
    spy.monitor_command(args.command, args.name)
    
    # Generate outputs
    spy.generate_dot_file(args.output)
    spy.save_results(args.output.replace('.dot', '_results.json'))
    
    print(f"\n🎯 Next steps:")
    print(f"  📊 View graph: dot -Tpng {args.output} -o build_graph.png && open build_graph.png")

if __name__ == '__main__':
    main()