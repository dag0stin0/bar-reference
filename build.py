#!/usr/bin/env python3
"""Build script: aggregates individual JSON content files into a single data.json"""

import json
import os
import glob

def build():
    content_dir = os.path.join(os.path.dirname(__file__), 'content')
    out_dir = os.path.join(os.path.dirname(__file__), '_site')
    os.makedirs(out_dir, exist_ok=True)

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

    # Copy static files to _site
    import shutil
    static_files = ['index.html', 'admin']
    for item in static_files:
        src = os.path.join(os.path.dirname(__file__), item)
        dst = os.path.join(out_dir, item)
        if os.path.isdir(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
        elif os.path.isfile(src):
            shutil.copy2(src, dst)

    print("Copied static files to _site/")

if __name__ == '__main__':
    build()
