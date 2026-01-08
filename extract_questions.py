import pandas as pd
import json
import re

def extract_questions(file_path, output_path):
    try:
        # Read from 'Bank' sheet
        df = pd.read_excel(file_path, sheet_name="Bank")
        questions = []
        
        for index, row in df.iterrows():
            try:
                # Extract basic fields - using English column names found in 'Bank' sheet
                stt = row['STT']
                if pd.isna(stt):
                    continue
                
                question_text = str(row['Question']).strip() if not pd.isna(row['Question']) else ""
                
                # 'Correct' column seems to hold the answer key (e.g. 'A', 'B', 'D')
                # Sometimes might contain text, so we'll just clean it.
                answer_raw = str(row['Correct']).strip() if not pd.isna(row['Correct']) else ""
                # Attempt to extract just the letter if it looks like "A. content" or "A content"
                match_ans = re.match(r'^([A-D])[\.\s]', answer_raw)
                if match_ans:
                   answer = match_ans.group(1)
                else:
                   # If just "A" or "B"
                   if answer_raw in ['A', 'B', 'C', 'D']:
                       answer = answer_raw
                   else:
                       answer = answer_raw # Fallback keeps original text

                # Parse Options from 'Options'
                options_text = str(row['Options']).strip() if not pd.isna(row['Options']) else ""
                options = {}
                
                # Split by A., B., C., D.
                # Adding a lookahead or lookbehind might be cleaner, or just splitting using capturing group
                parts = re.split(r'([A-D]\.)', options_text)
                
                current_key = None
                for part in parts:
                    part = part.strip()
                    if not part:
                        continue
                        
                    if re.match(r'^[A-D]\.$', part):
                        current_key = part[0] # Get 'A' from 'A.'
                    elif current_key:
                        options[current_key] = part
                        current_key = None 
                
                # Fallback: if regex failed to find structured options (empty dict), 
                # maybe they are newline separated without prefixes?
                # For now, just store what we have.
                
                q_obj = {
                    "id": int(stt),
                    "question": question_text,
                    "options": options,
                    "answer": answer
                }
                questions.append(q_obj)
                
            except Exception as row_e:
                print(f"Error processing row {index}: {row_e}")
                continue

        print(f"Extracted {len(questions)} questions.")
        
        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=4)
        print(f"Saved to {output_path}")
        
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    excel_file = "340 cau thi CCNV Dau thau 2025.xlsm"
    json_file = "340_cau_hoi.json"
    extract_questions(excel_file, json_file)
