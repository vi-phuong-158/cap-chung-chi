import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = "340 cau thi CCNV Dau thau 2025.xlsm"
try:
    xl = pd.ExcelFile(file_path)
    print("ALL SHEETS:", xl.sheet_names)
    
    for sheet in xl.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        print(f"Sheet '{sheet}': {len(df)} rows.")

except Exception as e:
    print(f"Error reading excel: {e}")
