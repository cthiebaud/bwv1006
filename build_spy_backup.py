#!/usr/bin/env python3
"""
Build Spy - Discover build dependencies by monitoring filesystem activity.
Generates DOT files from observed command execution patterns.

Usage: 
    python build_spy.py --watch-dir /path/to/project --command "make all"
    python build_spy.py --config build_spy.yaml
"""

import subprocess
import json
import re
import sys
import argparse
import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import tempfile
import os

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
        path = Path(filepath).resolve()
        for watch_dir in self.watch_dirs:
            try:
                path.relative_to(watch_dir.resolve())
                return True
            except ValueError:
                continue
        return False
    
    def run_with_strace(self, command, name=None):
        """Run command with strace monitoring on Linux."""
        print(f"🔍 Monitoring command with strace: {command}")
        
        # Create temporary file for strace output
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.strace', delete=False) as f:
            strace_file = f.name
        
        try:
            # Run command with strace
            strace_cmd = [
                'strace', 
                '-f',  # Follow forks
                '-e', 'trace=openat,open,creat,write,writev,close',  # File operations
                '-o', strace_file,  # Output to file
                'sh', '-c', command
            ]
            
            print(f"🚀 Executing: {' '.join(strace_cmd)}")
            result = subprocess.run(strace_cmd, capture_output=True, text=True)
            
            print(f"📊 Command exit code: {result.returncode}")
            if result.stdout:
                print(f"📝 stdout: {result.stdout[:200]}...")
            if result.stderr:
                print(f"⚠️  stderr: {result.stderr[:200]}...")
            
            if result.returncode != 0:
                print(f"⚠️  Command failed with return code {result.returncode}")
            
            # Check if strace file was created and has content
            strace_path = Path(strace_file)
            if strace_path.exists():
                content = strace_path.read_text()
                print(f"📄 strace output size: {len(content)} bytes")
                if content:
                    print(f"📄 First few lines of strace:")
                    for line in content.split('\n')[:5]:
                        if line.strip():
                            print(f"    {line}")
                else:
                    print("❌ strace output is empty!")
            else:
                print("❌ strace output file not created!")
            
            # Parse strace output
            self.parse_strace_output(strace_file, command, name)
            
        finally:
            # Clean up strace file
            try:
                os.unlink(strace_file)
            except:
                pass
    
    def run_with_fs_usage(self, command, name=None):
        """Run command with fs_usage monitoring on macOS (no sudo required)."""
        print(f"🔍 Monitoring command with fs_usage: {command}")
        
        # Start fs_usage in background to monitor filesystem activity
        fs_usage_cmd = ['fs_usage', '-w', '-f', 'filesys']
        
        try:
            # Start fs_usage
            print(f"🚀 Starting fs_usage monitoring...")
            fs_process = subprocess.Popen(fs_usage_cmd, stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE, text=True)
            
            # Give fs_usage a moment to start
            import time
            time.sleep(1)
            
            # Run the actual command
            print(f"🚀 Executing monitored command: {command}")
            cmd_result = subprocess.run(['sh', '-c', command], 
                                      capture_output=True, text=True)
            
            print(f"📊 Command exit code: {cmd_result.returncode}")
            
            # Give a moment for fs_usage to capture the activity
            time.sleep(2)
            
            # Stop fs_usage
            fs_process.terminate()
            
            # Get fs_usage output
            fs_output, fs_errors = fs_process.communicate(timeout=5)
            
            print(f"📄 fs_usage output size: {len(fs_output)} bytes")
            if fs_output:
                print(f"📄 First few lines of fs_usage output:")
                for line in fs_output.split('\n')[:10]:
                    if line.strip():
                        print(f"    {line}")
            
            # Parse fs_usage output
            self.parse_fs_usage_output(fs_output, command, name)
            
        except subprocess.TimeoutExpired:
            fs_process.kill()
            print("⚠️  fs_usage timed out")
        except FileNotFoundError:
            print("❌ fs_usage not found! This should be available on macOS by default.")
        except Exception as e:
            print(f"⚠️  fs_usage error: {e}")
    
    def parse_fs_usage_output(self, output, command, name):
        """Parse fs_usage output to extract file operations."""
        task_name = name or f"cmd_{len(self.file_access)}"
        reads = set()
        writes = set()
        
        for line in output.split('\n'):
            if not line.strip():
                continue
                
            # fs_usage format: timestamp syscall[pid] (process_name)
            # Look for file operations
            if any(op in line for op in ['open', 'write', 'read', 'creat']):
                # Try to extract filepath - fs_usage format is complex
                parts = line.split()
                for part in parts:
                    if '/' in part and not part.startswith('0x'):
                        filepath = part.strip()
                        
                        if not self.is_in_watch_dirs(filepath) or self.should_ignore_file(filepath):
                            continue
                        
                        # Simple heuristic based on operation type
                        if 'write' in line.lower() or 'creat' in line.lower():
                            writes.add(filepath)
                        elif 'open' in line.lower() or 'read' in line.lower():
                            reads.add(filepath)
        
        self.file_access[task_name] = {
            'reads': reads,
            'writes': writes,
            'command': command
        }
        
        print(f"📊 Task '{task_name}': {len(reads)} reads, {len(writes)} writes")
    
    def run_with_dtruss(self, command, name=None):
        """Run command with dtruss monitoring on macOS (fallback, requires sudo)."""
        print(f"🔍 Monitoring command with dtruss: {command}")
        print(f"⚠️  Note: dtruss requires sudo and may be blocked by SIP!")
        
        # dtruss requires sudo on macOS
        dtruss_cmd = [
            'sudo', 'dtruss', 
            '-f',  # Follow forks
            '-t', 'open,openat,write',  # System calls to trace
            'sh', '-c', command
        ]
        
        try:
            print(f"🚀 Executing: {' '.join(dtruss_cmd)}")
            result = subprocess.run(dtruss_cmd, capture_output=True, text=True)
            
            print(f"📊 Command exit code: {result.returncode}")
            print(f"📄 dtruss output size: {len(result.stderr)} bytes")
            
            if result.stderr:
                print(f"📄 First few lines of dtruss output:")
                for line in result.stderr.split('\n')[:10]:
                    if line.strip():
                        print(f"    {line}")
            else:
                print("❌ No dtruss output received!")
            
            # Parse dtruss output (from stderr)
            self.parse_dtruss_output(result.stderr, command, name)
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️  dtruss failed: {e}")
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
        
        # Debug: Show some before files
        if before_files:
            print("📋 Sample files before:")
            for i, (filepath, info) in enumerate(list(before_files.items())[:3]):
                print(f"    {Path(filepath).name}: mtime={info['mtime']:.0f}, size={info['size']}")
        
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
        
        # Debug: Show some after files and detect changes
        new_files = set(after_files.keys()) - set(before_files.keys())
        if new_files:
            print(f"🆕 New files detected: {len(new_files)}")
            for filepath in list(new_files)[:5]:
                print(f"    ➕ {Path(filepath).name}")
        else:
            print("❌ No new files detected")
        
        # Check for modifications
        modified_files = []
        for filepath in before_files:
            if filepath in after_files:
                before_info = before_files[filepath]
                after_info = after_files[filepath]
                if (before_info['mtime'] != after_info['mtime'] or 
                    before_info['size'] != after_info['size']):
                    modified_files.append(filepath)
        
        if modified_files:
            print(f"📝 Modified files: {len(modified_files)}")
            for filepath in modified_files[:5]:
                print(f"    📝 {Path(filepath).name}")
        else:
            print("❌ No modified files detected")
        
        # Determine reads and writes
        reads = set()
        writes = set()
        
        # Files that were modified or created = writes
        for filepath, after_info in after_files.items():
            before_info = before_files.get(filepath)
            if not before_info:
                # New file = write
                writes.add(filepath)
                print(f"➕ Created: {Path(filepath).name}")
            elif (before_info['mtime'] != after_info['mtime'] or 
                  before_info['size'] != after_info['size']):
                # Modified file = write
                writes.add(filepath)
                print(f"📝 Modified: {Path(filepath).name}")
        
        # For reads, let's be EXTREMELY conservative
        # Only consider files as reads if there's a STRONG indication they were used
        
        if writes:
            for filepath in before_files:
                if filepath not in writes and filepath in after_files:
                    path = Path(filepath)
                    
                    # Only consider as read if ALL of these are true:
                    # 1. It has a very specific input extension 
                    # 2. It's directly related to the command or output files
                    
                    is_very_likely_input = (
                        # Very specific input extensions only
                        path.suffix.lower() in ['.ly', '.ily'] and 
                        any(write_path for write_path in writes 
                            if Path(write_path).stem in path.stem or path.stem in Path(write_path).stem)
                    ) or (
                        # Python files only if the command mentions python
                        path.suffix.lower() == '.py' and 'python' in command.lower()
                    ) or (
                        # Config files only if they match the command
                        path.suffix.lower() in ['.yaml', '.yml', '.json'] and
                        any(pattern in command.lower() for pattern in [path.stem.lower(), 'config'])
                    )
                    
                    if is_very_likely_input:
                        reads.add(filepath)
        
        print(f"🔍 Applied strict filtering for realistic dependencies")
        
        self.file_access[task_name] = {
            'reads': reads,
            'writes': writes,
            'command': command
        }
        
        print(f"📊 Task '{task_name}': {len(reads)} reads, {len(writes)} writes")
        if reads:
            print(f"📖 Potential reads: {[Path(f).name for f in list(reads)[:5]]}")
        if writes:
            print(f"✏️  Writes: {[Path(f).name for f in writes]}")
        
        return len(reads) + len(writes) > 0
    
    def parse_strace_output(self, strace_file, command, name):
        """Parse strace output to extract file operations."""
        task_name = name or f"cmd_{len(self.file_access)}"
        reads = set()
        writes = set()
        
        try:
            with open(strace_file, 'r') as f:
                for line in f:
                    # Parse strace lines like:
                    # 1234 openat(AT_FDCWD, "/path/to/file", O_RDONLY) = 5
                    # 1234 openat(AT_FDCWD, "/path/to/file", O_WRONLY|O_CREAT, 0644) = 5
                    
                    if 'openat(' in line or 'open(' in line:
                        # Extract filepath from the line
                        match = re.search(r'"([^"]+)"', line)
                        if match:
                            filepath = match.group(1)
                            
                            # Skip if not in watch directories or should be ignored
                            if not self.is_in_watch_dirs(filepath) or self.should_ignore_file(filepath):
                                continue
                            
                            # Determine if read or write based on flags
                            if 'O_WRONLY' in line or 'O_RDWR' in line or 'O_CREAT' in line:
                                writes.add(filepath)
                            elif 'O_RDONLY' in line:
                                reads.add(filepath)
                                
        except Exception as e:
            print(f"⚠️  Error parsing strace output: {e}")
        
        self.file_access[task_name] = {
            'reads': reads,
            'writes': writes, 
            'command': command
        }
        
        print(f"📊 Task '{task_name}': {len(reads)} reads, {len(writes)} writes")
    
    def parse_dtruss_output(self, output, command, name):
        """Parse dtruss output to extract file operations."""
        task_name = name or f"cmd_{len(self.file_access)}"
        reads = set()
        writes = set()
        
        for line in output.split('\n'):
            # Parse dtruss lines - format varies
            if 'open(' in line or 'openat(' in line:
                # Extract filepath 
                match = re.search(r'"([^"]+)"', line)
                if match:
                    filepath = match.group(1)
                    
                    if not self.is_in_watch_dirs(filepath) or self.should_ignore_file(filepath):
                        continue
                    
                    # Simple heuristic: assume read unless creating/writing
                    if 'W' in line or 'CREAT' in line:
                        writes.add(filepath)
                    else:
                        reads.add(filepath)
        
        self.file_access[task_name] = {
            'reads': reads,
            'writes': writes,
            'command': command
        }
        
        print(f"📊 Task '{task_name}': {len(reads)} reads, {len(writes)} writes")
    
    def monitor_command(self, command, name=None):
        """Monitor a command's filesystem activity."""
        # Let's go back to trying dtruss first on macOS
        if sys.platform == 'darwin':
            print("🍎 macOS detected - trying dtruss monitoring")
            self.run_with_dtruss(command, name)
        elif sys.platform.startswith('linux'):
            print("🐧 Linux detected - using strace monitoring")  
            self.run_with_strace(command, name)
        else:
            print(f"⚠️  Platform {sys.platform} - falling back to simple monitoring")
            self.run_with_simple_monitoring(command, name)
        
        return True
    
    def monitor_build_sequence(self, commands):
        """Monitor a sequence of build commands."""
        print(f"🔍 Monitoring {len(commands)} build commands...")
        
        for i, cmd_info in enumerate(commands):
            if isinstance(cmd_info, str):
                command = cmd_info
                name = f"step_{i+1}"
            else:
                command = cmd_info.get('command', '')
                name = cmd_info.get('name', f"step_{i+1}")
            
            if command:
                self.monitor_command(command, name)
    
    def infer_dependencies(self):
        """Infer dependencies between tasks based on file I/O."""
        dependencies = defaultdict(set)
        
        task_names = list(self.file_access.keys())
        
        for i, task1 in enumerate(task_names):
            for j, task2 in enumerate(task_names):
                if i >= j:  # Only check forward dependencies
                    continue
                
                task1_writes = self.file_access[task1]['writes']
                task2_reads = self.file_access[task2]['reads']
                
                # If task1 writes files that task2 reads, task2 depends on task1
                common_files = task1_writes.intersection(task2_reads)
                if common_files:
                    dependencies[task2].add(task1)
                    print(f"📎 Dependency: {task2} depends on {task1} (shared files: {common_files})")
        
        return dependencies
    
    def generate_dot_file(self, output_file='discovered_build.dot'):
        """Generate DOT file from discovered dependencies."""
        dependencies = self.infer_dependencies()
        
        dot_content = f'''// Build pipeline discovered by monitoring filesystem activity
// Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
digraph DiscoveredBuild {{
    rankdir=TD;
    
    // Files (ellipses)
    node [shape=ellipse, style=filled];
    
'''
        
        # Collect all files
        all_files = set()
        for task_info in self.file_access.values():
            all_files.update(task_info['reads'])
            all_files.update(task_info['writes'])
        
        # Add file nodes
        for filepath in sorted(all_files):
            rel_path = Path(filepath).name  # Just filename for readability
            dot_content += f'    "{filepath}" [label="{rel_path}", fillcolor=lightblue];\n'
        
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
        
        # Task -> Task dependencies
        dot_content += '\n    // Task dependencies (black solid)\n'
        for task_name, deps in dependencies.items():
            for dep_task in deps:
                dot_content += f'    "{dep_task}" -> "{task_name}" [color=black];\n'
        
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
    parser = argparse.ArgumentParser(description='Discover build dependencies through filesystem monitoring')
    parser.add_argument('--command', '-c', help='Single command to monitor')
    parser.add_argument('--config', help='YAML config file with commands to monitor')
    parser.add_argument('--watch-dir', '-w', action='append', help='Directory to watch (can be specified multiple times)')
    parser.add_argument('--output', '-o', default='discovered_build.dot', help='Output DOT file')
    parser.add_argument('--name', '-n', help='Name for the monitored command')
    
    args = parser.parse_args()
    
    # Setup watch directories
    watch_dirs = [Path(d) for d in args.watch_dir] if args.watch_dir else [Path.cwd()]
    
    spy = BuildSpy(watch_dirs=watch_dirs)
    
    if args.command:
        # Monitor single command
        spy.monitor_command(args.command, args.name)
    elif args.config:
        # Monitor from config file
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
        
        commands = config.get('commands', [])
        spy.monitor_build_sequence(commands)
    else:
        print("❌ Must specify either --command or --config")
        return 1
    
    # Generate outputs
    spy.generate_dot_file(args.output)
    spy.save_results(args.output.replace('.dot', '_results.json'))
    
    print(f"\n🎯 Next steps:")
    print(f"  📊 View graph: dot -Tpng {args.output} -o build_graph.png && open build_graph.png")
    print(f"  🔧 Generate build script: python generate_build.py {args.output}")

if __name__ == '__main__':
    main()