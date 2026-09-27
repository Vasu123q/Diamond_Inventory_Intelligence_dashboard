from anyio import Path
import pandas as pd
import numpy as np
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
data = pd.read_excel(project_root / "L1" / "Sales_Prediction.xlsx")

required_cols = ['Total Sales', 'Inventory Age', 'Avg_Sold_Age',
                 'Inventory Score', 'Certification Score', 'Sales Score']

def window_score(age, avg, start, end):
    """
    Returns how well current stone fits this window
    """
    mid = (start + end) / 2
    return np.exp(-((age - mid) ** 2) / (2 * (avg ** 2)))

age = data['Inventory Age']
avg = data['Avg_Sold_Age']
sales = data['Sales Score']

data['Prob(0-30)'] = (
    0.45 * sales +
    0.40 * window_score(age, avg, 0, 30) +
    0.15 * np.exp(-abs(avg - 30)/30)
)

data['Prob(30-90)'] = (
    0.45 * sales +
    0.40 * window_score(age, avg, 30, 90) +
    0.15 * np.exp(-abs(avg - 60)/60)
)

data['Prob(90-150)'] = (
    0.45 * sales +
    0.40 * window_score(age, avg, 90, 150) +
    0.15 * np.exp(-abs(avg - 120)/120)
)

data['Prob(150-365)'] = (
    0.45 * sales +
    0.40 * window_score(age, avg, 150, 365) +
    0.15 * np.exp(-abs(avg - 250)/250)
)

data['Prob(365+)'] = (
    0.45 * sales +
    0.40 * (age / (avg + 1)).clip(0, 2) +
    0.15 * (avg / avg.max())
)

cols = ['Prob(0-30)','Prob(30-90)','Prob(90-150)','Prob(150-365)','Prob(365+)']

total = data[cols].sum(axis=1).replace(0, 1)

for col in cols:
    data[col] = (data[col] / total).clip(0,1).round(3)


print('Probability buckets added')

data['Aging Risk Score'] = (
    ((1 - data['Inventory Score']) * 0.35) +
    ((1 - data['Certification Score']) * 0.15) +
    ((1 - data['Sales Score']) * 0.50)
) * 100

data['Aging Risk Score'] = data['Aging Risk Score'].round(0).clip(0, 100)

print('Aging Risk score added')


conditions = [
    data['Aging Risk Score'] >= 75,
    (data['Aging Risk Score'] >= 45) & (data['Aging Risk Score'] < 75),
    data['Aging Risk Score'] < 45
]

choices = ["High", "Medium", "Low"]

data['Risk Classification'] = np.select(conditions, choices, default='')

data.to_excel(project_root / "L1" / "Sales_Prediction_with_Probabilities_&_SCORES.xlsx", index=False)
