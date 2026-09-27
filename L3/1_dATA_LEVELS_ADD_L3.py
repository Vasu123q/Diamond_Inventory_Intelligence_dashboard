import pandas as pd
import numpy as np
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

inv=pd.read_excel(project_root /"Input" / "Inventory_Summary.xlsx")
sales=pd.read_excel(project_root / "Input" / "Sales_Summary.xlsx")

df = [inv, sales]

color_map = {
    'D':'D-F','E':'D-F',
    'F':'D-F','G':'G-J',
    'H':'G-J','I':'G-J',
    'J':'G-J','K':'K-N',
    'L':'K-N','M':'K-N',
    'N':'K-N','OP':'N-YZ',
    'QR':'N-YZ','ST':'N-YZ',
    'UV':'N-YZ','WX':'N-YZ','YZ':'N-YZ'
}

clarity_map = {
    'FL':'FL-VVS1','IF':'FL-VVS1',
    'VVS1':'FL-VVS1','VVS2':'VVS2-VS2',
    'VS1':'VVS2-VS2','VS2':'VVS2-VS2',
    'SI1':'SI1-I3','SI2':'SI1-I3','SI3':'SI1-I3',
    'I1':'SI1-I3','I2':'SI1-I3','I3':'SI1-I3'
}


for i in df:

    i['Color-ranges'] = i['Color'].map(color_map)
    i['Clarity-ranges'] = i['Clarity'].map(clarity_map)

    pos = i.columns.get_loc('Color')
    col_data = i.pop('Color-ranges')
    i.insert(pos+1, 'Color-ranges', col_data)

    pos = i.columns.get_loc('Clarity')
    col_data = i.pop('Clarity-ranges')
    i.insert(pos+1, 'Clarity-ranges', col_data)

   
inv.to_excel(project_root /'L3'/'Input'/'Inventory_Summary_dl.xlsx', index=False)
sales.to_excel(project_root /'L3'/'Input'/'Sales_Summary_dl.xlsx', index=False)
print('Inventory and Sales data with new Data Levels') 