import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = "340 cau thi CCNV Dau thau 2025.xlsm"
try:
    df = pd.read_excel(file_path, sheet_name="Bank", nrows=3)
    print("Columns:", df.columns.tolist())
    for i, row in df.iterrows():
        print(f"Row {i}:")
        print(f"  Question: {row.get('Question')}")
        print(f"  Options: {row.get('Options')}")
        print(f"  Correct: {row.get('Correct')}")
        print(f"  Answer: {row.get('Answer')}")
        print("-" * 10)
except Exception as e:
    print(f"Error: {e}")
