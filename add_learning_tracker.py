# Batch Update Script - Add Learning Tracker to All Training Modules
# This script adds the learning tracker to all HTML files in the training directory

import os
import re
from pathlib import Path

def add_learning_tracker(file_path):
    """Add learning tracker script and data-module-name to an HTML file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has learning tracker
    if 'learning_tracker.js' in content:
        print(f"✓ Skipped (already has tracker): {file_path.name}")
        return False
    
    # Extract module name from file path
    relative_path = file_path.relative_to(Path(r'c:\Users\ksank\training'))
    parts = str(relative_path).replace('\\', '_').replace('.html', '')
    module_name = parts.lower().replace(' ', '_')
    
    # Calculate relative path to learning_tracker.js
    depth = len(relative_path.parts) - 1  # -1 because file itself doesn't count
    tracker_path = '../' * depth + 'learning_tracker.js'
    
    # Add script tag after <title>
    title_pattern = r'(<title>.*?</title>)'
    script_tag = f'\\1\n    <!-- Learning Tracker -->\n    <script src="{tracker_path}"></script>'
    content = re.sub(title_pattern, script_tag, content, count=1)
    
    # Add data-module-name to <body> tag
    body_pattern = r'<body>'
    body_replacement = f'<body data-module-name="{module_name}">'
    content = re.sub(body_pattern, body_replacement, content, count=1)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated: {file_path.name}")
    return True

def main():
    training_dir = Path(r'c:\Users\ksank\training')
    
    # Find all HTML files (excluding TRAINING_HUB.html)
    html_files = []
    for root, dirs, files in os.walk(training_dir):
        for file in files:
            if file.endswith('.html') and file != 'TRAINING_HUB.html':
                html_files.append(Path(root) / file)
    
    print(f"Found {len(html_files)} HTML files to process\n")
    
    updated = 0
    skipped = 0
    
    for file_path in html_files:
        if add_learning_tracker(file_path):
            updated += 1
        else:
            skipped += 1
    
    print(f"\n{'='*50}")
    print(f"✓ Updated: {updated} files")
    print(f"○ Skipped: {skipped} files (already had tracker)")
    print(f"Total: {len(html_files)} files")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
