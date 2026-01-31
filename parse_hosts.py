import csv
import json
import sys

files = [
    {'name': 'Morning', 'path': r'c:\Users\kilot\projects\oca hosts\host_morning.csv'},
    {'name': 'Afternoon', 'path': r'c:\Users\kilot\projects\oca hosts\host_afternoon.csv'}
]

all_script_data = {}

for file_info in files:
    script_data = []
    current_speaker = None
    
    with open(file_info['path'], 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: continue
            
            while len(row) < 3:
                row.append('')
                
            speaker = row[0].strip()
            text_cn = row[1].strip()
            # row[2] could be missing or index out of range if we didn't pad, but we padded
            text_en = row[2].strip() 
            
            if not speaker and not text_cn and not text_en:
                continue
                
            if speaker.lower() == 'ending':
                 script_data.append({
                    'type': 'header',
                    'text': 'Ending'
                })
                 current_speaker = None
                 continue

            if 'minutes' in text_cn or 'minutes' in speaker:
                 continue

            if speaker == '节目' or text_cn.startswith('#') or (not speaker and text_cn.startswith('#')):
                script_data.append({
                    'type': 'header',
                    'text': text_cn + ' ' + text_en
                })
                continue
            
            if speaker:
                current_speaker = speaker
            
            effective_speaker = speaker if speaker else current_speaker
            
            # Special case for "开场" or "下午开场" in headers/titles
            if effective_speaker and ('开场' in effective_speaker or '开场' in text_cn) and not text_en:
                 # Check if it looks like a header line
                 if len(text_cn) < 10: 
                     script_data.append({
                        'type': 'header',
                        'text': effective_speaker if '开场' in effective_speaker else text_cn
                    })
                     current_speaker = None
                     continue
            
            if effective_speaker:
                script_data.append({
                    'type': 'dialogue',
                    'speaker': effective_speaker,
                    'text_cn': text_cn,
                    'text_en': text_en
                })
    
    all_script_data[file_info['name']] = script_data

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(all_script_data, f, ensure_ascii=False, indent=2)
