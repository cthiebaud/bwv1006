def main():
    parser = argparse.ArgumentParser(description='Generate build scripts from DOT file')
    parser.add_argument('dot_file', help='Input DOT file')
    parser.add_argument('--output', '-o', help='Output file name')
    parser#!/usr/bin/env python3
"""
Generate build scripts (invoke tasks.py or doit dodo.py) from a DOT file.
Usage: python generate_build.py build_pipeline.dot --output dodo.py --format doit
"""

import re
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def parse_dot_file(dot_content):
    """Parse DOT file and extract build pipeline information."""
    
    # Extract node definitions
    tasks = {}
    files = {}
    globs = {}
    
    # Find all node definitions
    node_pattern = r'"([^"]+)"\s*\[([^\]]+)\]'
    for match in re.finditer(node_pattern, dot_content):
        node_id = match.group(1)
        attributes = match.group(2)
        
        # Parse attributes
        attrs = {}
        for attr_match in re.finditer(r'(\w+)=([^,\]]+)', attributes):
            key = attr_match.group(1)
            value = attr_match.group(2).strip('"')
            attrs[key] = value
        
        # Check if it's a glob pattern
        if node_id.startswith('glob:'):
            pattern = node_id[5:]  # Remove 'glob:' prefix
            label = attrs.get('label', node_id)
            
            # Determine glob type by color
            fillcolor = attrs.get('fillcolor', 'lightcyan')
            if fillcolor == 'lightcyan':
                glob_type = 'input'
            elif fillcolor == 'lightgreen':
                glob_type = 'output'
            elif fillcolor == 'orange':
                glob_type = 'temp'
            else:
                glob_type = 'unknown'
                
            globs[node_id] = {
                'pattern': pattern,
                'type': glob_type,
                'label': label
            }
        elif 'shape=box' in attributes:
            # Task node
            label = attrs.get('label', node_id)
            
            # Extract commands from label (lines after first line)
            lines = label.split('\\n')
            task_name = lines[0]
            commands = lines[1:] if len(lines) > 1 else []
            
            tasks[node_id] = {
                'name': task_name,
                'commands': commands,
                'inputs': [],
                'outputs': [],
                'task_deps': [],
                'glob_inputs': [],
                'glob_outputs': []
            }
        else:
            # Regular file node
            label = attrs.get('label', node_id)
            file_name = label.split('\\n')[0]  # First line is filename
            
            # Determine file type by color
            fillcolor = attrs.get('fillcolor', 'lightblue')
            if fillcolor == 'lightblue':
                file_type = 'source'
            elif fillcolor == 'lightyellow':
                file_type = 'intermediate'
            elif fillcolor == 'lightgreen':
                file_type = 'output'
            else:
                file_type = 'unknown'
                
            files[node_id] = {
                'name': file_name,
                'type': file_type
            }
    
    # Extract edges (dependencies)
    edge_pattern = r'"([^"]+)"\s*->\s*"([^"]+)"\s*\[([^\]]+)\]'
    for match in re.finditer(edge_pattern, dot_content):
        source = match.group(1)
        target = match.group(2)
        attributes = match.group(3)
        
        if 'color=blue' in attributes:
            # File/Glob -> Task (input)
            if target in tasks:
                if source.startswith('glob:'):
                    tasks[target]['glob_inputs'].append(source)
                else:
                    tasks[target]['inputs'].append(source)
        elif 'color=green' in attributes:
            # Task -> File/Glob (output)
            if source in tasks:
                if target.startswith('glob:'):
                    tasks[source]['glob_outputs'].append(target)
                else:
                    tasks[source]['outputs'].append(target)
        elif 'color=black' in attributes:
            # Task -> Task (dependency)
            if target in tasks:
                tasks[target]['task_deps'].append(source)
    
    return tasks, files, globs

def generate_dodo_py(tasks, files, globs):
    """Generate dodo.py file for doit."""
    
    content = f'''"""
Build script generated from DOT file
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

from pathlib import Path
from datetime import datetime

def expand_glob(pattern):
    """Expand a glob pattern and return list of Path objects."""
    if '**' in pattern:
        # Recursive glob
        parts = pattern.split('**/')
        if len(parts) == 2:
            base_path = Path(parts[0]) if parts[0] else Path('.')
            return list(base_path.rglob(parts[1]))
    
    # Regular glob
    return list(Path('.').glob(pattern))

def shared_ly_sources():
    """Get shared LilyPond source files."""
    shared_files = []
    
    # Static files
    for file_path in [Path("bwv1006_ly_main.ly"), Path("highlight-bars.ily"), Path("defs.ily")]:
        if file_path.exists():
            shared_files.append(file_path)
    
    # Dynamic globs
    shared_files.extend(expand_glob("_?/*.ly"))
    shared_files.extend(expand_glob("**/*.ily"))
    
    return shared_files

def remove_outputs(*filenames):
    """Clean action to remove output files."""
    def clean_targets():
        deleted = []
        for name in filenames:
            path = Path(name)
            if path.exists():
                path.unlink()
                deleted.append(path.name)
        if deleted:
            print(f"🗑️  Deleted: {{', '.join(deleted)}}")
    return clean_targets

def remove_glob_outputs(*patterns):
    """Clean action to remove files matching glob patterns."""
    def clean_glob_targets():
        deleted = []
        for pattern in patterns:
            for path in expand_glob(pattern):
                if path.exists():
                    path.unlink()
                    deleted.append(path.name)
        if deleted:
            print(f"🗑️  Deleted glob matches: {{', '.join(deleted)}}")
    return clean_glob_targets

'''
    
    # Generate task functions
    for task_id, task_info in tasks.items():
        if not task_info['commands']:  # Skip tasks without commands
            continue
            
        task_name = task_id.replace('-', '_')  # Python function names
        
        content += f'''
def task_{task_name}():
    """{task_info['name']}."""
    sources = []
    
    # Static input files'''
        
        # Add input files
        for input_file in task_info['inputs']:
            if files.get(input_file, {}).get('name'):
                file_name = files[input_file]['name']
                content += f'''
    sources.append(Path("{file_name}"))'''
        
        # Add glob inputs
        for glob_input in task_info['glob_inputs']:
            if globs.get(glob_input, {}).get('pattern'):
                pattern = globs[glob_input]['pattern']
                content += f'''
    sources.extend(expand_glob("{pattern}"))'''
        
        content += f'''
    
    # Filter existing sources
    sources = [s for s in sources if s.exists()]
    
    targets = []'''
        
        # Add output files
        for output_file in task_info['outputs']:
            if files.get(output_file, {}).get('name'):
                file_name = files[output_file]['name']
                content += f'''
    targets.append("{file_name}")'''
        
        # Note: glob outputs are handled differently since they're dynamic
        glob_output_patterns = []
        for glob_output in task_info['glob_outputs']:
            if globs.get(glob_output, {}).get('pattern'):
                pattern = globs[glob_output]['pattern']
                glob_output_patterns.append(pattern)
        
        content += f'''
    
    return {{
        'actions': ['''
        
        # Add commands
        for cmd in task_info['commands']:
            # Convert generic commands to actual shell commands
            if 'docker run lilypond' in cmd:
                if '--svg' in cmd:
                    content += f'''
            'docker run -v "{{Path.cwd()}}:/work" codello/lilypond:dev --svg {cmd.split()[-1]}','''
                else:
                    content += f'''
            'docker run -v "{{Path.cwd()}}:/work" codello/lilypond:dev {cmd.split()[-1]}','''
            elif cmd.endswith('.py'):
                content += f'''
            'python3 scripts/{cmd}','''
            else:
                content += f'''
            '{cmd}','''
        
        content += f'''
        ],
        'file_dep': [str(s) for s in sources],
        'targets': targets,'''
        
        # Add task dependencies
        if task_info['task_deps']:
            deps = [f"'{dep}'" for dep in task_info['task_deps']]
            content += f'''
        'task_dep': [{', '.join(deps)}],'''
        
        # Add clean actions
        clean_actions = ['remove_outputs(*targets)']
        if glob_output_patterns:
            patterns_str = ', '.join(f'"{p}"' for p in glob_output_patterns)
            clean_actions.append(f'remove_glob_outputs({patterns_str})')
        
        content += f'''
        'clean': [{', '.join(clean_actions)}],
        'verbosity': 2,
    }}'''
    
    # Add utility tasks
    content += '''

def task_list_globs():
    """List all files matching glob patterns."""
    def list_glob_matches():
        print("🔍 Glob pattern matches:")'''
    
    for glob_id, glob_info in globs.items():
        pattern = glob_info['pattern']
        content += f'''
        print(f"  {pattern}:")
        for path in expand_glob("{pattern}"):
            print(f"    {{path}}")'''
    
    content += '''
    
    return {
        'actions': [list_glob_matches],
        'verbosity': 2,
    }'''
    
    # Add default configuration
    content += '''

# Default task configuration
def task_all():
    """Run the complete build pipeline."""
    def completion_message():
        print(f"\\n✅✅✅ All steps completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ✅✅✅")
    
    return {
        'actions': [completion_message],
        'task_dep': ['''
    
    # Add all main tasks as dependencies for 'all'
    final_tasks = [task_id for task_id, task_info in tasks.items() 
                   if task_info['commands'] and (task_info['outputs'] or task_info['glob_outputs'])]
    
    if final_tasks:
        content += f"'{final_tasks[-1]}'"
    else:
        content += ', '.join(f"'{task}'" for task in list(tasks.keys())[:5])
    
    content += '''],
        'verbosity': 2,
    }

DOIT_CONFIG = {
    'default_tasks': ['all'],
    'verbosity': 2,
}
'''
    
    return content

def generate_tasks_py(tasks, files):
    """Generate tasks.py file for invoke."""
    
    content = f'''"""
Build script generated from DOT file  
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from invoke import task

# Shared utilities (simplified version)
def shared_ly_sources():
    return [Path("bwv1006_ly_main.ly"), Path("highlight-bars.ily"), Path("defs.ily")] + list(Path(".").rglob("_?/*.ly"))

'''
    
    # Generate task functions
    for task_id, task_info in tasks.items():
        if not task_info['commands']:  # Skip tasks without commands
            continue
            
        task_name = task_id.replace('-', '_')
        
        # Determine pre-tasks
        pre_tasks = task_info['task_deps']
        pre_str = f", pre=[{', '.join(pre_tasks)}]" if pre_tasks else ""
        
        content += f'''
@task{pre_str}
def {task_name}(c, force=False):
    """{task_info['name']}."""
    sources = ['''
        
        # Add input files  
        for input_file in task_info['inputs']:
            if files.get(input_file, {}).get('name'):
                file_name = files[input_file]['name']
                content += f'Path("{file_name}"), '
        
        content += ''']
    
    # Add shared sources for LilyPond tasks
    if any("lilypond" in cmd.lower() for cmd in {task_info['commands']}):
        sources.extend(shared_ly_sources())
    
    targets = ['''
        
        # Add targets
        for output_file in task_info['outputs']:
            if files.get(output_file, {}).get('name'):
                file_name = files[output_file]['name']
                content += f'"{file_name}", '
        
        content += f''']
    
    commands = ['''
        
        # Add commands
        for cmd in task_info['commands']:
            if 'docker run lilypond' in cmd:
                if '--svg' in cmd:
                    content += f'''
        'docker run -v "{{Path.cwd()}}:/work" codello/lilypond:dev --svg {cmd.split()[-1]}','''
                else:
                    content += f'''
        'docker run -v "{{Path.cwd()}}:/work" codello/lilypond:dev {cmd.split()[-1]}','''
            elif cmd.endswith('.py'):
                content += f'''
        'python3 scripts/{cmd}','''
            else:
                content += f'''
        '{cmd}','''
        
        content += f'''
    ]
    
    # Simple execution (replace with your smart_task if available)
    for cmd in commands:
        print(f"🔧 {{cmd}}")
        c.run(cmd)
    
    if targets:
        print(f"✅ Generated: {{', '.join(str(t) for t in targets)}}")'''
    
    # Add 'all' task
    content += '''

@task
def all(c):
    """Run the complete build pipeline."""
    # Add your main tasks here
    print(f"\\n✅✅✅ All steps completed successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ✅✅✅")
'''
    
    return content

def main():
    parser = argparse.ArgumentParser(description='Generate build scripts from DOT file')
    parser.add_argument('dot_file', help='Input DOT file')
    parser.add_argument('--output', '-o', help='Output file name')
    parser.add_argument('--format', '-f', choices=['doit', 'invoke'], default='doit',
                        help='Output format (doit or invoke)')
    
    args = parser.parse_args()
    
    # Read DOT file
    dot_content = Path(args.dot_file).read_text()
    
    # Parse DOT file
    tasks, files, globs = parse_dot_file(dot_content)
    
    print(f"📋 Found {len(tasks)} tasks, {len(files)} files, and {len(globs)} glob patterns")
    
    # Show glob patterns found
    if globs:
        print("🔍 Glob patterns detected:")
        for glob_id, glob_info in globs.items():
            print(f"  {glob_info['pattern']} ({glob_info['type']})")
    
    # Generate build script
    if args.format == 'doit':
        content = generate_dodo_py(tasks, files, globs)
        default_output = 'dodo.py'
    else:
        content = generate_tasks_py(tasks, files, globs)
        default_output = 'tasks.py'
    
    # Write output
    output_file = args.output or default_output
    Path(output_file).write_text(content)
    
    print(f"✅ Generated {output_file}")
    print(f"🔧 Run with: {'doit' if args.format == 'doit' else 'invoke --list'}")
    
    if globs:
        print(f"🌟 Try: {'doit list_globs' if args.format == 'doit' else 'invoke list-globs'} to see matched files")

if __name__ == '__main__':
    main()