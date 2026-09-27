import pandas as pd
import numpy as np
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]


df=pd.read_excel(project_root / "L2" / "mapping and hidden space removal added" / "Inventory_Summary_mh.xlsx")
df2=pd.read_excel(project_root / "L2" / "mapping and hidden space removal added" / "Sales_Summary_mh.xlsx")
ranges_df=pd.read_excel(project_root / "Input" / "size_range.xlsx")


df['Size'] = pd.to_numeric(df['Size'], errors='coerce')
df2['Size'] = pd.to_numeric(df2['Size'], errors='coerce')

ranges = ranges_df.iloc[:, 0].dropna().astype(str)

bins = []
labels = []

for r in ranges:
    r = r.strip().replace("–", "-").replace("—", "-")

    if "-" in r:
        low, high = map(float, r.split("-"))
        bins.append(low)
        labels.append(r)

    elif "+" in r:
        low = float(r.replace("+", ""))
        bins.append(low)
        labels.append(r)

bins = sorted(bins)

bins.append(np.inf)

df['Size ranges'] = pd.cut(
    df['Size'],
    bins=bins,
    labels=labels,
    right=False   
)

df2['Size ranges'] = pd.cut(
    df2['Size'],
    bins=bins,
    labels=labels,
    right=False
)

pos_sr=df.columns.get_loc('Size')
col_sr=df.pop('Size ranges')
df.insert(pos_sr+1,'Size ranges',col_sr)

pos_sr2=df2.columns.get_loc('Size')
col_sr2=df2.pop('Size ranges')
df2.insert(pos_sr2+1,'Size ranges',col_sr2)


df.to_excel(project_root / "L2" / "size range added" / "Inventory_Summary_mhs.xlsx", index=False)
df2.to_excel(project_root / "L2" / "size range added" / "Sales_Summary_mhs.xlsx", index=False)            

print("DONE — Size ranges assigned")