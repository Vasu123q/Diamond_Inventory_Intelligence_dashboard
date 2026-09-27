import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
sales=pd.read_excel(project_root / "L1" / "size range added" / "Sales_Summary_mhs.xlsx")

df1=(sales.groupby(
    ['Color', 'Clarity', 'Shape', 'Size ranges', 'Lab'],
        as_index=False,
        dropna=False
        )
.agg(
    Total_sales=('ItemCD','count'),
    Avg_Sold_Age=('Sold Age','mean')

    )

)

df1=df1.rename(columns={'Total_sales':'Total Sales',})

df1.to_excel(project_root / "L1" / "Grouped_Sales.xlsx", index=False)