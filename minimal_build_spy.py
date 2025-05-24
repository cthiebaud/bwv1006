#!/usr/bin/env python3
"""
Minimal build spy to debug dtruss issues.
"""

import subprocess
import re
import sys
from pathlib import Path

def run_dtruss_test(command):
    """Test dtruss with a simple command."""
    print(f"🔍 Testing dtruss with: {command}")
    
    # Let's try with a command that does more obvious I/O
    print("\n🔬 Method 1: Test with echo redirection")
    test_echo_command()
    
    print("\n🔬 Method 2: Test with cp command")  
    test_cp_command()
    
    print("\n🔬 Method 3: Original touch command")
    test_touch_command(command)

def test_echo_command():
    """Test with echo command that should definitely write a file."""
    command = "echo hello world > dtruss_test.txt"
    dtruss_cmd = ['sudo', 'dtruss', '-e', 'sh', '-c', command]
    
    try:
        print(f"🚀 Executing: {' '.join(dtruss_cmd)}")
        result = subprocess.run(dtruss_cmd, capture_output=True, text=True, timeout=10)
        
        print(f"📊 Exit code: {result.returncode}")
        
        # Look for our test file
        file_ops = []
        for line in result.stderr.split('\n'):
            if 'dtruss_test.txt' in line:
                file_ops.append(line.strip())
                
        if file_ops:
            print(f"✅ Found operations on dtruss_test.txt:")
            for op in file_ops:
                print(f"   {op}")
        else:
            print("❌ No operations found on dtruss_test.txt")
            # Show any open() calls
            open_calls = [line.strip() for line in result.stderr.split('\n') if 'open(' in line and '"' in line]
            print(f"🔍 All open() calls: {len(open_calls)}")
            for call in open_calls[:5]:
                print(f"   {call}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def test_cp_command():
    """Test with cp command."""
    # Copy a system file to our directory
    dtruss_cmd = ['sudo', 'dtruss', '-e', 'cp', '/etc/hosts', 'dtruss_hosts_copy.txt']
    
    try:
        print(f"🚀 Executing: {' '.join(dtruss_cmd)}")
        result = subprocess.run(dtruss_cmd, capture_output=True, text=True, timeout=10)
        
        print(f"📊 Exit code: {result.returncode}")
        
        # Look for our files
        for target in ['hosts', 'dtruss_hosts_copy.txt']:
            file_ops = [line.strip() for line in result.stderr.split('\n') if target in line and 'open(' in line]
            if file_ops:
                print(f"✅ Found operations on {target}:")
                for op in file_ops[:3]:
                    print(f"   {op}")
            else:
                print(f"❌ No operations found on {target}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def test_touch_command(command):
    """Test the original touch command with more debugging."""
    cmd_parts = command.split()
    dtruss_cmd = ['sudo', 'dtruss', '-e'] + cmd_parts
    
    try:
        print(f"🚀 Executing: {' '.join(dtruss_cmd)}")
        result = subprocess.run(dtruss_cmd, capture_output=True, text=True, timeout=10)
        
        print(f"📊 Exit code: {result.returncode}")
        
        # Save full output to file for inspection
        with open('dtruss_full_output.txt', 'w') as f:
            f.write(result.stderr)
        print(f"💾 Full dtruss output saved to: dtruss_full_output.txt")
        
        # Look for file operations - UPDATED to include touch-specific syscalls
        target_file = cmd_parts[-1]
        
        print(f"\n🔍 Looking for operations on: {target_file}")
        
        # Look for different types of file operations
        file_operations = {
            'open': [],
            'fstatat64': [],
            'setattrlistat': [],
            'other': []
        }
        
        for line_num, line in enumerate(result.stderr.split('\n')):
            line_clean = line.strip()
            if not line_clean:
                continue
                
            # Look for file operations that might involve our target file
            # The key insight: touch uses fstatat64 and setattrlistat, not open!
            
            if 'open(' in line and '"' in line:
                # Extract filename from open calls
                match = re.search(r'open\("([^"]+)', line)
                if match:
                    filepath = match.group(1).replace('\\0', '')
                    if target_file in filepath:
                        file_operations['open'].append(f"Line {line_num}: {line_clean}")
                        
            elif 'fstatat64(' in line:
                # fstatat64 operates on file descriptors + relative paths
                # Format: fstatat64(fd, path_ptr, stat_buf) = result
                file_operations['fstatat64'].append(f"Line {line_num}: {line_clean}")
                
            elif 'setattrlistat(' in line:
                # setattrlistat sets file attributes (like timestamps)
                # This is likely what touch uses to update timestamps!
                file_operations['setattrlistat'].append(f"Line {line_num}: {line_clean}")
                
            elif any(syscall in line for syscall in ['openat(', 'creat(', 'write(']):
                if target_file in line or '"' in line:
                    file_operations['other'].append(f"Line {line_num}: {line_clean}")
        
        # Report findings
        total_ops = sum(len(ops) for ops in file_operations.values())
        if total_ops > 0:
            print(f"✅ Found {total_ops} potential file operations:")
            
            for op_type, ops in file_operations.items():
                if ops:
                    print(f"  📁 {op_type.upper()} operations: {len(ops)}")
                    for op in ops[:3]:  # Show first 3 of each type
                        print(f"     {op}")
                        
            # The key insight: touch probably uses setattrlistat to modify timestamps
            if file_operations['setattrlistat']:
                print(f"\n💡 INSIGHT: touch command uses setattrlistat() to modify file timestamps")
                print(f"   This means it WRITES to the file (updates timestamps)")
                
        else:
            print(f"❌ No obvious file operations found")
            
            # Show syscall summary
            syscalls = {}
            for line in result.stderr.split('\n'):
                if ':' in line and '(' in line:
                    # Extract syscall name
                    parts = line.split(':')
                    if len(parts) >= 2:
                        syscall_part = parts[-1].strip()
                        if '(' in syscall_part:
                            syscall_name = syscall_part.split('(')[0].strip()
                            syscalls[syscall_name] = syscalls.get(syscall_name, 0) + 1
            
            print(f"📊 Syscall summary (top 10):")
            for syscall, count in sorted(syscalls.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"   {syscall}: {count}")
                
        # Final check: did the file get created/modified?
        import os
        if os.path.exists(target_file):
            stat = os.stat(target_file)
            print(f"\n✅ File '{target_file}' exists (size: {stat.st_size}, modified: {stat.st_mtime})")
            print(f"   → This confirms touch WROTE to the file (created/updated timestamps)")
        else:
            print(f"\n❌ File '{target_file}' does not exist")
                
    except Exception as e:
        print(f"❌ Error: {e}")

def parse_dtruss_simple_single_line(line, expected_file):
    """Parse a single dtruss line."""
    print(f"\n🔍 Parsing line: {line}")
    
    if 'open(' in line:
        # Extract filename
        match = re.search(r'open\("([^"]+)', line)
        if match:
            filepath = match.group(1).replace('\\0', '')
            print(f"📁 File: {filepath}")
            
            # Extract flags
            flags_match = re.search(r'0x([0-9A-Fa-f]+)', line)
            if flags_match:
                flags = int(flags_match.group(1), 16)
                print(f"🏁 Flags: 0x{flags:x}")
                
                # Determine operation type
                if flags & 0x200:  # O_CREAT = 0x200
                    print(f"✏️  → WRITE/CREATE operation")
                elif flags & 0x1:  # O_WRONLY = 0x1
                    print(f"✏️  → WRITE operation")
                elif flags == 0x0:  # O_RDONLY = 0x0
                    print(f"📖 → READ operation")
                else:
                    print(f"❓ → UNKNOWN operation (flags: 0x{flags:x})")
            else:
                print("❓ No flags found")
        else:
            print("❓ No filename found in open() call")

def parse_dtruss_simple(output, command):
    """Simple dtruss parser."""
    print(f"\n🔍 Parsing dtruss output...")
    
    reads = []
    writes = []
    
    for line in output.split('\n'):
        if 'open(' in line and '"' in line:
            # Extract filename
            match = re.search(r'open\("([^"]+)', line)
            if match:
                filepath = match.group(1).replace('\\0', '')
                
                # Skip system files
                if any(skip in filepath for skip in ['/usr/', '/System/', '/Library/', '/dev/', '/tmp/', '/var/']):
                    continue
                
                # Check if it's a user file
                if '/' not in filepath or filepath.startswith('./') or Path(filepath).is_absolute() == False:
                    # Determine read vs write from flags
                    flags_match = re.search(r'0x([0-9A-Fa-f]+)', line)
                    if flags_match:
                        flags = int(flags_match.group(1), 16)
                        if flags & 0x201:  # Write flags
                            writes.append(filepath)
                            print(f"  ✏️  WRITE: {filepath} (flags: 0x{flags:x})")
                        else:
                            reads.append(filepath)
                            print(f"  📖 READ:  {filepath} (flags: 0x{flags:x})")
                    else:
                        print(f"  ❓ UNKNOWN: {filepath} (no flags found)")
    
    print(f"\n📊 Summary: {len(reads)} reads, {len(writes)} writes")
    return reads, writes

if __name__ == '__main__':
    if len(sys.argv) > 1:
        command = ' '.join(sys.argv[1:])
    else:
        command = 'touch test_file.txt'
    
    run_dtruss_test(command)