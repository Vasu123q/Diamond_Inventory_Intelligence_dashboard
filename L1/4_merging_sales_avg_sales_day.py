import pandas as pd
from datetime import datetime
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]
sales=pd.read_excel(project_root / "L1" / "size range added" / "Sales_Summary_mhs.xlsx")

sales['Certification']=pd.to_datetime(sales['Certification'],errors='coerce')
sales['Purchase Date']=pd.to_datetime(sales['Purchase Date'],errors='coerce')
sales['Sold Age']=abs(sales['Certification']-sales['Purchase Date']).dt.days
df1=(sales.groupby(
    ['Color', 'Clarity', 'Shape', 'Size ranges', 'SOLD FROM', 'Lab'],
        as_index=False,
        dropna=False
        )
.agg(
    Total_sales=('ItemCD','count')

    )

)

print('Total Sales added!')

df1=df1.rename(columns={'Total_sales':'Total Sales',})

df2=(sales.groupby(
    ['Color', 'Clarity', 'Shape', 'Size ranges', 'SOLD FROM', 'Lab'],
        as_index=False,
        dropna=False
)
     .agg(
    Avg_Sold_Age=('Sold Age','mean')
))

print('Sold Age Added!')

df=pd.merge(df1,df2,on=['Color', 'Clarity', 'Shape', 'Size ranges', 'SOLD FROM', 'Lab'],how='left')



df.to_excel(project_root / "L1" / "Proccesed_Sales.xlsx", index=False)


