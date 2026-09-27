import pandas as pd
import numpy as np
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

df=pd.read_excel(project_root / "L1" / "Data.xlsx")
gpdata=pd.read_excel(project_root / "L1" / "Proccesed_Sales.xlsx")

cols=['Shape','Clarity','Color','Lab','Size ranges']
for c in cols:
    df[c]=df[c].astype(str).str.strip().str.upper()
    gpdata[c]=gpdata[c].astype(str).str.strip().str.upper()

key=['Shape','Color','Clarity','Size ranges','Lab']

pivot_sales = (
    gpdata.pivot_table(
        index=key,
        columns='SOLD FROM',
        values='Total Sales',
        aggfunc='sum'
    ).reset_index()
)

df = df.merge(pivot_sales, on=key, how='left')

df.rename(columns={
    'HK':'Sales in HK',
    'USA':'Sales in USA'
}, inplace=True)



print("Predicting...")
df[['Sales in HK','Sales in USA']] = df[['Sales in HK','Sales in USA']].fillna(0)
df['Total Sales']=df['Sales in HK']+df['Sales in USA']

# usecols=['Total Sales','Shape','Color','Size ranges','Clarity','Lab']

# df=df.merge(gpdata[usecols+['Avg_Sold_Days']],on=usecols,how='left')


df['Prediction'] = np.select(
    [
        df['Total Sales'] == 0,
        (df['Sales in HK'] == df['Sales in USA']) & (df['Total Sales']>0),
        df['Sales in USA'] >= df['Total Sales'] / 2,
        df['Sales in HK'] >= df['Total Sales'] / 2
    ],
    [
        "No Sales data",
        "Sell to HK",
        "Sell to USA",
        "Sell to HK"
    ],
    default=""
)

pos_sale_hk=df.columns.get_loc('Sales in HK')
col_total_sales=df.pop('Total Sales')
df.insert(pos_sale_hk,'Total Sales',col_total_sales)

print("Sales Added")


print("Predicted Stones Sale")

print("Adding Score...")


# ----///'Inventory Age'///

df["Inv_score"] = 1-df["Inventory Age"].rank(method='average',pct=True)

bonus = np.select(
    [
        df['Inventory Age'] < 365,
        (df['Inventory Age'] >= 365) & (df['Inventory Age'] < 730),
        df['Inventory Age'] >= 730
    ],
    [0.05, 0.02, 0.0],
    default=0
)

df['Inv_score'] = (df['Inv_score'] * (1 + bonus)).clip(0,1).round(2)

conditions_inv=[
    df['Inv_score']>=0.78,
    (df['Inv_score']<=0.77) & (df['Inv_score']>=0.5),
    (df['Inv_score']<=0.49) & (df['Inv_score']>=0)
]

choices_inv=[
    "Fast Moving",
    "Slow Moving",
    "Dead Stock"
]   



#--//Certification Age

df["Cert_score"] = 1-df["Certification Age"].rank(method='average',pct=True).round(2)

conditions_cert=[
     df['Cert_score']>=0.80,
    (df['Cert_score']>=0.6) & (df['Cert_score']<0.8),
    (df['Cert_score']>=0.4) & (df['Cert_score']<0.6),
    (df['Cert_score']>=0.2) & (df['Cert_score']<0.4),
    df['Cert_score']<0.2

]

choices_cert=[
    "Fresh certificate",
    "Acceptable",
    "Slightly old",
    "May need recertification",
    "Very old certificate"
]



#---///'Total Sales'

df["Sales_score"] = (
    np.log1p(df["Total Sales"]) / np.log1p(df["Total Sales"].max())
).round(2)

sales_conditions=[
    df['Sales_score']>=0.80,
    (df['Sales_score']>=0.6) & (df['Sales_score']<0.8),
    (df['Sales_score']>=0.4) & (df['Sales_score']<0.6),
    (df['Sales_score']>=0.2) & (df['Sales_score']<0.4),
    df['Sales_score']<0.2
]
sales_choices=[
    "Very high demand",
    "Good demand",
    "Moderate demand",
    "Very low demand",
    "No demand"
]

print('Scores and Label added')

df['Inventory_label']=np.select(conditions_inv, choices_inv,default='')
df['Certification_label']=np.select(conditions_cert, choices_cert,default='') 
df['Sales_label']=np.select(sales_conditions, sales_choices,default='')

print('Calculating Sales Probability...')


sales_log = np.log1p(df['Total Sales'])

p95 = sales_log.quantile(0.95)

df['sales_norm'] = (sales_log / p95)

df['age_factor'] = 0.0
mask = df['Inventory Age'].notna()
df.loc[mask, 'age_factor'] = 1 / (1 + df.loc[mask, 'Inventory Age'] / 500 )
df['sales_days_norm']=(1-((df['Avg_Sold_Age']-df['Avg_Sold_Age'].min())/(df['Avg_Sold_Age'].max()-df['Avg_Sold_Age'].min())))


df['Sales_Probability'] = (
    0.50 * df['sales_norm'] +
    0.40 * df['age_factor'] +
    0.10* df['sales_days_norm']
).clip(0,1).round(3)


# df.loc[df['age_factor'] == 0, 'Sales_Probability'] = df['sales_norm']
df['Sales_Probability'] = df['Sales_Probability'].clip(0,1).round(3)

prob_conditions=[
    df['Sales_Probability']>=0.75,  
    (df['Sales_Probability']>=0.50) & (df['Sales_Probability']<0.75),
    (df['Sales_Probability']<0.50)
]

prob_choices=[
    "A",
    "B",
    "C"
]
df['Sales_Probability_label']=np.select(prob_conditions, prob_choices,default='')

print('Probability added')


pos_inv=df.columns.get_loc('Inventory Age')
col_inv_label=df.pop('Inv_score')
col_inv_label2=df.pop('Inventory_label')
df.insert(pos_inv+1,'Inventory Score',col_inv_label)
df.insert(pos_inv+2,'Inventory Label',col_inv_label2)

pos_cert=df.columns.get_loc('Certification Age')
col_cert_label=df.pop('Cert_score')
col_cert_label2=df.pop('Certification_label')
df.insert(pos_cert+1,'Certification Score',col_cert_label)
df.insert(pos_cert+2,'Certification Label',col_cert_label2)

pos_sale=df.columns.get_loc('Prediction')
col_sale_label=df.pop('Sales_score')
col_sale_label2=df.pop('Sales_label')
df.insert(pos_sale+1,'Sales Score',col_sale_label)
df.insert(pos_sale+2,'Sales Label',col_sale_label2)

pos_sr=df.columns.get_loc('Size')
col_sr=df.pop('Size ranges')
df.insert(pos_sr+1,'Size ranges',col_sr)
df=df.drop(columns=['sales_norm','age_factor','sales_days_norm'])

df.to_excel(project_root / "L1" / "Sales_Prediction.xlsx", index=False )
print('Done')
