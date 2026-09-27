import streamlit as st
import pandas as pd
import os
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

st.set_page_config(layout="wide")
st.title(" Stone Status")
# 🔄 Refresh button (manual)
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# ================= LOAD (cached) =================
@st.cache_data(ttl=60)  
def load_data():
    xls = pd.ExcelFile(project_root/"Final_Predicted.xlsx")
    return pd.read_excel(xls, "Level_1")

file_path = project_root / "Final_Predicted.xlsx"
last_modified = os.path.getmtime(file_path)

if "last_modified_p2" not in st.session_state:
    st.session_state.last_modified_p2 = last_modified

elif st.session_state.last_modified_p2 != last_modified:
    st.warning("⚠️ Data was Modified! Click refresh button.", icon="⚠️")
    st.session_state.last_modified_p2 = last_modified

df = load_data()    
df = df.copy()

# ================= CLEAN =================
df['Stone Location'] = df['Stone Location'].replace({
    'UAE':'DUBAI',
    'INDIA':'IND'
})

df['Stone Location'] = df['Stone Location'].astype(str).str.upper().str.strip()
df['Status'] = df['Status'].astype(str).str.strip()
df['ItemCD'] = df['ItemCD'].astype(str).str.strip()
df['Lab'] = df['Lab'].astype(str).str.strip()

# ================= FILTER =================
st.markdown("## Filters")

status_options = [
    "Memo Out",
    "AVL Stock",
    "Unpublish AVL(Not On Rap)",
    "On Hand",
    "On Hold",
    "For Web",
    "Transit",
    "Reserved",
    "Consume",
    "Under Certification"
]

with st.form("filters"):

    c1, c2 = st.columns(2)

    loc = c1.multiselect(
        "Location",
        sorted(df["Stone Location"].dropna().unique())
    )

    category = c2.multiselect(
        "Metric / Category",
        status_options
    )

    apply = st.form_submit_button("Apply Filters")

# ================= STOP BEFORE APPLY =================
if not apply:
    st.info("Apply filters to view data")
    st.stop()



# ================= LOCATION FILTER =================
if loc:
    filtered = df[df["Stone Location"].isin(loc)]
    if filtered.empty:
        st.warning("⚠️ No stones found for selected locations")
        st.stop()
    locations = [l.upper() for l in loc]
else:
    filtered = df.copy()
    locations = sorted(filtered["Stone Location"].unique())

# ================= RULES =================
available_status = ["Consignment In","Memo In","Available to Use","In Stock"]
memo_out_status = ["Consignment Out","Memo Out"]

# ================= BUILD SUMMARY =================
summary_list = []

for loc_name in locations:

    g = filtered[filtered["Stone Location"] == loc_name]

    row = {
        "Location": loc_name,
        "Total Stones": len(g),

        "Memo Out": g[g['Status'].isin(memo_out_status)].shape[0],

        "AVL Stock": g[g['Status'].isin(available_status)].shape[0],

        "Unpublish AVL(Not On Rap)": g[
            (g['Status'].isin(available_status)) & (g['Publish']==False)
        ].shape[0],

        "On Hand": g[
            (g['Status'].isin(available_status)) &
            (g['Publish']==False) &
            (~g['ItemCD'].str.startswith(('FE','MO','KV'))) &
            (~g['Lab'].isin(['NC','',None]))
        ].shape[0],

        "On Hold": g[g['Status']=="On Hold"].shape[0],

        "For Web": g[
            (g['Status'].isin(available_status)) & (g['Publish']==True)
        ].shape[0],

        "Transit": g[g['Status']=="Transit"].shape[0],

        "Reserved": g[g['Status']=="Reserved"].shape[0],

        "Consume": g[g['Status']=="Consume"].shape[0],

        "Under Certification": g[g['Status']=="Under Certification"].shape[0],
    }

    summary_list.append(row)

summary = pd.DataFrame(summary_list)

# ================= TOTAL ROW =================
total_row = summary.select_dtypes(include='number').sum()
total_row["Location"] = "Total"

summary = pd.concat(
    [summary, pd.DataFrame([total_row])],
    ignore_index=True
)


# ================= COLUMN FILTER =================
if category:
    selected_cols = ["Location"] + category
else:
    selected_cols = summary.columns.tolist()

# ================= DISPLAY =================
st.markdown("## 📦 Inventory Summary Table")

st.caption(
    f"Filters → Location: {loc if loc else 'All'} | Category: {category if category else 'All'}"
)

st.dataframe(summary[selected_cols], use_container_width=True)

# ================= DRILL DOWN =================
if category:

    # map category → actual status logic
    category_to_filter = {
    "Memo Out": lambda g: g[g['Status'].isin(memo_out_status)],

    "AVL Stock": lambda g: g[g['Status'].isin(available_status)],

    "Unpublish AVL(Not On Rap)": lambda g: g[
        (g['Status'].isin(available_status)) & (g['Publish']==False)
    ],

    "On Hand": lambda g: g[
        (g['Status'].isin(available_status)) &
        (g['Publish']==False) &
        (~g['ItemCD'].str.startswith(('FE','MO','KV'))) &
        (~g['Lab'].isin(['NC','',None]))
    ],

    "On Hold": lambda g: g[g['Status']=="On Hold"],
    "For Web": lambda g: g[(g['Status'].isin(available_status)) & (g['Publish']==True)],
    "Transit": lambda g: g[g['Status']=="Transit"],
    "Reserved": lambda g: g[g['Status']=="Reserved"],
    "Consume": lambda g: g[g['Status']=="Consume"],
    "Under Certification": lambda g: g[g['Status']=="Under Certification"],
}
    drill_df = pd.DataFrame()

    for c in category:
        func = category_to_filter.get(c)
        if func:
            drill_df = pd.concat([drill_df, func(filtered)])

    drill_df = drill_df.drop_duplicates()

    if drill_df.empty:
        st.warning("No stones found")
    else:
        st.success(f"Showing {len(drill_df)} stones")

        st.dataframe(
            drill_df[[
                "ItemCD",
                "Shape",
                "Color",
                "Clarity",
                "Size",
                "Stone Location",
                "Status",
                "Lab",

            ]],
            use_container_width=True
        )   