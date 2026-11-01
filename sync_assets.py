# -*- coding: utf-8 -*-
import json
import urllib.request
import os

with open('assets_manifest.json', 'r', encoding='utf-8') as f:
    manifest = json.load(f)

os.makedirs('spin_scrubber', exist_ok=True)
success_count = 0

for item in manifest:
    name = item['name']
    url = item['url']
    out_path = os.path.join('spin_scrubber', name)
    
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        success_count += 1
        continue
        
    print(f'Fetching {name} from {url}...')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as res:
            data = res.read()
            if len(data) > 1000:
                with open(out_path, 'wb') as out_f:
                    out_f.write(data)
                print(f'  -> OK ({len(data)} bytes)')
                success_count += 1
            else:
                print(f'  -> Warning: file too small ({len(data)} bytes)')
    except Exception as e:
        print(f'  -> Error fetching {name}: {e}')

print(f'Sync finished: {success_count}/{len(manifest)} images ready!')
