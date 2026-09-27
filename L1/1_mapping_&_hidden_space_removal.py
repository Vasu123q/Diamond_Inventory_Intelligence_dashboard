import pandas as pd
import mapping_function as mp
import hidden_space_removal as hs
import os
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]



input_file_inv = project_root / "Input" / "Inventory_Summary.xlsx"
input_file_sales = project_root / "Input" / "Sales_Summary.xlsx"
output_file_inv = project_root/'L1'/'mapping and hidden space removal added'/'Inventory_Summary_mh.xlsx'
output_file_sales = project_root/'L1'/'mapping and hidden space removal added'/'Sales_Summary_mh.xlsx'

inv=pd.read_excel(input_file_inv)
sales=pd.read_excel(input_file_sales)

print('\n Level 1 prediction Started \n')

data = [inv,sales]

cols = ["Shape", "Size", "Color", "Clarity", "Lab"]


SHAPES  = {k.upper().strip(): v for k, v in mp.shapes.items()}
COLOR   = {k.upper().strip(): v for k, v in mp.color.items()}
CLARITY = {k.upper().strip(): v for k, v in mp.clarity.items()}
LAB     = {k.upper().strip(): v for k, v in mp.lab.items()}
COLS_MAP = {k.strip(): v for k, v in mp.cols.items()}


print("Processing...")
for f in data:

    # REMOVE HIDDEN SPACES 
    f = hs.apply_hidden_space_removal(f, cols)
    
print('Hidden Spaces Removed')

for f in data:
    # APPLY MAPPING 
    f['Shape']   = f['Shape'].map(SHAPES).fillna(f['Shape'])
    f['Color']   = f['Color'].map(COLOR).fillna(f['Color'])
    f['Clarity'] = f['Clarity'].map(CLARITY).fillna(f['Clarity'])
    f['Lab']     = f['Lab'].map(LAB).fillna(f['Lab'])
    f.columns = f.columns.str.strip()
    f.rename(columns=COLS_MAP, inplace=True)

print("Mapping Applied Successfully")

for d in data:
    d['Size'] = pd.to_numeric(d['Size'], errors='coerce').round(2)

inv.to_excel(output_file_inv, index=False)
sales.to_excel(output_file_sales, index=False)