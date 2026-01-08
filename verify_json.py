import json
import sys

# Encoding check
sys.stdout.reconfigure(encoding='utf-8')

try:
    with open("340_cau_hoi.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print(f"Total entries: {len(data)}")
    
    for i, item in enumerate(data[:3]):
        print(f"\nItem {i+1}:")
        print(f"ID: {item['id']}")
        print(f"Question: {item['question'][:100]}...") # truncate
        print(f"Options: {item['options']}")
        print(f"Answer: '{item['answer']}'")
        
    # Check for empty fields
    empty_ans = [x['id'] for x in data if not x['answer']]
    empty_opts = [x['id'] for x in data if not x['options']]
    
    if empty_ans:
        print(f"\nWARNING: IDs with empty answer: {empty_ans[:5]}...")
    if empty_opts:
        print(f"WARNING: IDs with empty options: {empty_opts[:5]}...")
        
except Exception as e:
    print(f"Error: {e}")
