import pandas as pd
import sys

# Set encoding to utf-8 for output
sys.stdout.reconfigure(encoding='utf-8')

file_path = "340 cau thi CCNV Dau thau 2025.xlsm"
try:
    df = pd.read_excel(file_path, nrows=5)
    print("--- COLUMNS ---")
    for col in df.columns:
        print(f"'{col}'")
    
    print("\n--- FIRST ROW ---")
    row = df.iloc[0]
    for col in df.columns:
        val = row[col]
        print(f"{col}: {val}")

    print("\n--- NON-EMPTY ROW SAMPLE ---")
    clean_df = df.dropna(how='all')
    if not clean_df.empty:
        row = clean_df.iloc[0]
        for col in df.columns:
            print(f"{col}: {row[col]}")

except Exception as e:
    print(f"Error reading excel: {e}")
