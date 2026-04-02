#!/usr/bin/env python3
"""Build script: aggregates individual JSON content files into a single data.json"""

import json
import os
import glob

def build():
    root = os.path.dirname(os.path.abspath(__file__))
    content_dir = os.path.join(root, 'content')
    out_dir = os.path.join(root, 'public')
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, 'admin'), exist_ok=True)

    data = {}

    # Cocktails
    cocktail_files = sorted(glob.glob(os.path.join(content_dir, 'cocktails', '*.json')))
    cocktails = []
    for f in cocktail_files:
        with open(f, 'r') as fh:
            cocktails.append(json.load(fh))
    data['cocktails'] = cocktails

    # Write aggregated data
    with open(os.path.join(out_dir, 'data.json'), 'w') as f:
        json.dump(data, f)

    print(f"Built data.json: {len(cocktails)} cocktails")

    # Copy static files to public/
    import shutil
    shutil.copy2(os.path.join(root, 'index.html'), os.path.join(out_dir, 'index.html'))
    shutil.copy2(os.path.join(root, 'admin', 'index.html'), os.path.join(out_dir, 'admin', 'index.html'))
    shutil.copy2(os.path.join(root, 'admin', 'config.yml'), os.path.join(out_dir, 'admin', 'config.yml'))

    print("Copied static files to public/")

if __name__ == '__main__':
    build()
