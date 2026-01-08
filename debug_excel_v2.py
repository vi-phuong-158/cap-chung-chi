import pandas as pd
import sys
import io

# Redirect output to file to avoid console truncation issues during quick preview
with open("sheets_info.txt", "w", encoding="utf-8") as f:
    try:
        file_path = "340 cau thi CCNV Dau thau 2025.xlsm"
        xl = pd.ExcelFile(file_path)
        f.write(f"ALL SHEETS: {xl.sheet_names}\n\n")
        
        for sheet in xl.sheet_names:
            try:
                df = pd.read_excel(file_path, sheet_name=sheet)
                f.write(f"Sheet '{sheet}': {len(df)} rows\n")
                f.write(f"Columns: {df.columns.tolist()}\n")
                f.write("-" * 20 + "\n")
            except Exception as e_sheet:
                f.write(f"Error reading sheet {sheet}: {e_sheet}\n")
                
    except Exception as e:
        f.write(f"Error reading excel: {e}\n")
