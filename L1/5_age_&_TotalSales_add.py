import pandas as pd
from datetime import datetime
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
    
data=pd.read_excel(project_root / "L1" / "size range added" / "Inventory_Summary_mhs.xlsx")
sales=pd.read_excel(project_root / "L1" / "Grouped_Sales.xlsx")

data['Certification']=pd.to_datetime(data['Certification'],errors='coerce')
data['Purchase Date']=pd.to_datetime(data['Purchase Date'],errors='coerce')
current=datetime.now()

data['Certification Age']=(current-data['Certification']).dt.days
data['Inventory Age']=(current-data['Purchase Date']).dt.days
print('Cerification and Inventory Age added!')
cols=['Color', 'Clarity', 'Shape', 'Size ranges', 'Lab']


for col in cols:
    data[col] = data[col].astype(str).str.strip().str.upper()
    sales[col] = sales[col].astype(str).str.strip().str.upper()

df=pd.merge(data,sales,on=['Color', 'Clarity', 'Shape', 'Size ranges', 'Lab'],how='left')


df.to_excel(project_root / "L1" / "Data.xlsx", index=False)

