import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

st.set_page_config(layout="wide")
st.title(" Inventory Stones")

# 🔄 Refresh button (manual)
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# ================= LOAD (cached) =================
@st.cache_data(ttl=60)  # cache expires after 60s (no auto rerun)
def load_data():
    xls = pd.ExcelFile(project_root/"Final_Predicted.xlsx")
    
    return {
        "L1": pd.read_excel(xls, "Level_1"),
        "L2": pd.read_excel(xls, "Level_2"),
        "L3": pd.read_excel(xls, "Level_3"),
    }


file_path = project_root / "Final_Predicted.xlsx"
last_modified = os.path.getmtime(file_path)

if "last_modified_p1" not in st.session_state:
    st.session_state.last_modified_p1 = last_modified

elif st.session_state.last_modified_p1 != last_modified:
    st.warning("⚠️ Data was Modified! Click refresh button.", icon="⚠️")
    st.session_state.last_modified_p1 = last_modified

data = load_data()
level1 = data["L1"]
level2 = data["L2"]
level3 = data["L3"]

# ================= HELPERS =================
@st.cache_data
def safe_unique(df, col):
    return sorted(df[col].dropna().astype(str).unique())

def k(tab, name):
    return f"{tab}_{name}"

def clean_pie(df, col):
    data = df[col].value_counts()
    fig = px.pie(values=data.values, names=data.index, hole=0.5)
    fig.update_layout(height=350)
    return fig

# ================= MAIN =================
def render_tab(df, tab):

    st.header(tab)

    # ================= FILTER =================
    st.markdown("## Filters")
    color_col = "Color-ranges" if "Color-ranges" in df.columns else "Color"
    clarity_col = "Clarity-ranges" if "Clarity-ranges" in df.columns else "Clarity"

    with st.form(k(tab,"filter")):

        c1,c2,c3,c4,c5 = st.columns(5)

        shape = c1.multiselect("Shape", safe_unique(df,"Shape"), key=k(tab,"shape"))
        color = c2.multiselect(f"{color_col}", safe_unique(df, color_col), key=k(tab,"color"))
        clarity = c3.multiselect(f"{clarity_col}", safe_unique(df, clarity_col), key=k(tab,"clarity"))
        cut = c4.multiselect("Cut", safe_unique(df,"Cut"), key=k(tab,"cut"))
        lab = c5.multiselect("Lab", safe_unique(df,"Lab"), key=k(tab,"lab"))

        c6,c7,c8,c9,c10 = st.columns(5)

        polish = c6.multiselect("Polish", safe_unique(df,"Polish"), key=k(tab,"polish"))
        sym = c7.multiselect("Symmetry", safe_unique(df,"sym"), key=k(tab,"sym"))
        fl = c8.multiselect("Fluorescence", safe_unique(df,"Fluorescence"), key=k(tab,"fl"))
        loc = c9.multiselect("Location", safe_unique(df,"Stone Location"), key=k(tab,"loc"))
        stock = c10.multiselect("Stock Type", safe_unique(df,"Stock_Classification"), key=k(tab,"stock"))

        st.markdown("### Range Filters")

        r1,r2,r3,r4 = st.columns(4)
        carat_from = r1.number_input("Carat From", value=0.0, key=k(tab,"cf"))
        carat_to = r2.number_input("Carat To", value=float(df["Size"].max()), key=k(tab,"ct"))
        depth_from = r3.number_input(" Depth From", value=0.0, key=k(tab,"df"))
        depth_to = r4.number_input("Depth To", value=float(df["Depth%"].max()), key=k(tab,"dt"))

        r5,r6,r7,r8 = st.columns(4)

        table_from = r5.number_input("Table From", value=0.0, key=k(tab,"tf"))
        table_to = r6.number_input("Table To", value=float(df["Table %"].max()), key=k(tab,"tt"))
        ratio_from = r7.number_input("Ratio From", value=0.0, key=k(tab,"rf"))
        ratio_to = r8.number_input("Ratio To", value=float(df["Ratio"].max()), key=k(tab,"rt"))

        apply = st.form_submit_button("Apply Filters")

    filtered = df.copy()

    if apply:
        if shape: filtered = filtered[filtered["Shape"].isin(shape)]
        if color: filtered = filtered[filtered[color_col].isin(color)]
        if clarity: filtered = filtered[filtered[clarity_col].isin(clarity)]
        if cut: filtered = filtered[filtered["Cut"].isin(cut)]
        if lab: filtered = filtered[filtered["Lab"].isin(lab)]
        if polish: filtered = filtered[filtered["Polish"].isin(polish)]
        if sym: filtered = filtered[filtered["sym"].isin(sym)]
        if fl: filtered = filtered[filtered["Fluorescence"].isin(fl)]
        if loc: filtered = filtered[filtered["Stone Location"].isin(loc)]
        if stock: filtered = filtered[filtered["Stock_Classification"].isin(stock)]

        filtered = filtered[
            (filtered["Size"]>=carat_from) &
            (filtered["Size"]<=carat_to) &
            (filtered["Depth%"]>=depth_from) &
            (filtered["Depth%"]<=depth_to) &
            (filtered["Table %"]>=table_from) &
            (filtered["Table %"]<=table_to) &
            (filtered["Ratio"]>=ratio_from) &
            (filtered["Ratio"]<=ratio_to)
        ]
        if filtered.empty:
            st.warning("⚠️ No stones found for selected filters")
  

    # ================= DISTRIBUTION =================
    st.markdown("## Distribution")

    if not filtered.empty:

        d1,d2,d3 = st.columns(3)

        d1.plotly_chart(clean_pie(filtered,"Shape"), use_container_width=True, key=k(tab,"pie1"))
        d2.plotly_chart(clean_pie(filtered, color_col), use_container_width=True, key=k(tab,"pie2"))
        d3.plotly_chart(clean_pie(filtered, clarity_col), use_container_width=True, key=k(tab,"pie3"))

    else:
        st.warning("⚠️ No data available for distribution charts")

    # ================= SIZE RANGE =================
    st.markdown("## Size Range Distribution")

    if not filtered.empty:

        size_data = (
            filtered["Size ranges"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        size_data.columns = ["Carat Range", "Count"]

        fig_size = px.bar(
            size_data,
            x="Carat Range",
            y="Count"
        )

        st.plotly_chart(
            fig_size,
            use_container_width=True,
            key=k(tab,"size")
        )

    else:
        st.warning("No data available for selected filters")

    # ================= SALES OVERVIEW =================
    st.markdown("## Sales Overview")

    total_sales = df["Total Sales"].sum()

    if total_sales > 0:
        usa_sales = (df["Sales in USA"].sum() / total_sales) * 100
        hk_sales  = (df["Sales in HK"].sum() / total_sales) * 100
    else:
        usa_sales, hk_sales = 0, 0
    

    c1,c2,c3 = st.columns(3)
    c2.metric("USA Sales", f"{usa_sales:,.0f}%")
    c3.metric("HK Sales", f"{hk_sales:,.0f}%")

    fig_sales = px.pie(names=["USA","HK"], values=[usa_sales,hk_sales], hole=0.5)
    st.plotly_chart(fig_sales, use_container_width=True, key=k(tab,"sales"))

    # ================= ML SELLING =================
    st.markdown("## Selling Recommendation")

    flow_df = df.groupby(["Stone Location","ML_Sales_Pred"]).size().reset_index(name="count")

    fig_ml = px.bar(
        flow_df,
        x="Stone Location",
        y="count",
        color="ML_Sales_Pred",
        barmode="group"
    )

    st.plotly_chart(fig_ml, use_container_width=True, key=k(tab,"ml"))

    # ================= 4Cs DEMAND =================
    st.markdown("## Stones Demand")

    if k(tab,"4cs_data") not in st.session_state:
        st.session_state[k(tab,"4cs_data")] = None


    with st.form(key=k(tab,"4cs_form")):

        c1,c2,c3,c4 = st.columns(4)

        s_shape = c1.selectbox("Shape", ["Select"] + safe_unique(df,"Shape"))
        s_color = c2.selectbox(f"{color_col}", ["Select"] + safe_unique(df, color_col))
        s_clarity = c3.selectbox(f"{clarity_col}", ["Select"] + safe_unique(df, clarity_col))
        s_size = c4.selectbox("Carat Range", ["Select"] + safe_unique(df,"Size ranges"))

        apply4 = st.form_submit_button("Apply")

    # st.markdown("</div>", unsafe_allow_html=True)

    if apply4 and "Select" not in [s_shape, s_color, s_clarity, s_size]:

        temp = df[
            (df["Shape"].astype(str)==s_shape) &
            (df[color_col].astype(str)==s_color) &
            (df[clarity_col].astype(str)==s_clarity) &
            (df["Size ranges"].astype(str)==s_size)
        ].copy()

        st.session_state[k(tab,"4cs_data")] = temp

    temp = st.session_state[k(tab,"4cs_data")]

    if temp is not None and not temp.empty:

        # Map demand
        demand_map = {
            "No demand": 1,
            "Very low demand": 2,
            "Moderate demand": 3,
            "Good demand": 4,
            "Very high demand": 5
        }
        temp = temp.copy()
        temp["Demand_Level"] = temp["Label_pred"].map(demand_map)

        # Use REAL sizes
        temp = temp.sort_values("Size")


        temp_grouped = temp.groupby("Size")["Demand_Level"].mean().reset_index()

        # Smooth slightly
        temp_grouped["Smooth"] = temp_grouped["Demand_Level"].rolling(window=min(5, len(temp_grouped)), min_periods=1).mean()

        # Plot
        fig = px.line(
            temp_grouped,
            x="Size",
            y="Smooth"
        )

        fig.update_traces(
            line_shape='spline',
            line=dict(width=3)
        )

        fig.update_layout(
            xaxis_title="Size (Carat)",
            yaxis_title="Sales Demand",
            yaxis=dict(
                tickvals=[1,2,3,4,5],
                ticktext=[
                    "No demand",
                    "Very low demand",
                    "Moderate demand",
                    "Good demand",
                    "Very high demand"
                ]
            ),
            height=500
        )

        

        st.plotly_chart(fig, use_container_width=True)

    elif temp is not None and temp.empty:
            st.warning("⚠️ No stone with these attributes exists in inventory")

    # ================= SALES PROB =================
    st.markdown("## Sales Probability")

    if k(tab,"prob_data") not in st.session_state:
        st.session_state[k(tab,"prob_data")] = None

    with st.form(k(tab,"prob")):

        c1,c2,c3,c4,c5 = st.columns(5)

        p1 = c1.selectbox("Shape", ["Select"]+safe_unique(df,"Shape"), key=k(tab,"p1"))
        p2 = c2.selectbox(f"{color_col}", ["Select"]+safe_unique(df, color_col), key=k(tab,"p2"))
        p3 = c3.selectbox(f"{clarity_col}", ["Select"]+safe_unique(df, clarity_col), key=k(tab,"p3"))
        p4 = c4.selectbox("Carat", ["Select"]+safe_unique(df,"Size ranges"), key=k(tab,"p4"))
        p5 = c5.selectbox("Fluorescence", ["Select"]+safe_unique(df,"Fluorescence"), key=k(tab,"p5"))

        go_prob = st.form_submit_button("Apply")

    if go_prob and "Select" not in [p1,p2,p3,p4,p5]:

        temp = df[
                (df["Shape"].astype(str)==p1) &
                (df[color_col].astype(str)==p2) &
                (df[clarity_col].astype(str)==p3) &
                (df["Size ranges"].astype(str)==p4) &
                (df["Fluorescence"].astype(str)==p5)
        ]

        st.session_state[k(tab,"prob_data")] = temp

    temp = st.session_state[k(tab,"prob_data")]

    if temp is not None and not temp.empty:

            st.dataframe(temp[[
            "Shape","Color","Clarity","Size",
            "ML_Sales_Prob",
            "Probability_Sell_(0-30)_Days",
            "Probability_Sell_(30-90)_Days",
            "Probability_Sell_(90-150)_Days",
            "Probability_Sell_(150-365)_Days",
            "Probability_Sell_(365+)_Days",
            "Expected_Days_to_sell"
        ]].rename(columns={
            'ML_Sales_Prob':'Sales Probability',
            'Probability_Sell_(0-30)_Days':'Probability to Sell in 0-30 days',
            'Probability_Sell_(30-90)_Days':'Probability to Sell in 30-90 days',
            'Probability_Sell_(90-150)_Days':'Probability to Sell in 90-150 days',
            'Probability_Sell_(150-365)_Days':'Probability to Sell in 150-365 days',
            'Probability_Sell_(365+)_Days':'Probability to Sell in 365+ days',
            'Expected_Days_to_sell':'Expected Days to sell',
        }), use_container_width=True)

    elif temp is not None and temp.empty:
            st.warning("⚠️ No stone with these attributes exists in inventory")

    # ================= AGING =================
    st.markdown("## Aging Risk")
    if k(tab,"aging_data") not in st.session_state:
        st.session_state[k(tab,"aging_data")] = None
    with st.form(k(tab,"aging")):

        c1,c2,c3,c4 = st.columns(4)

        a1 = c1.selectbox("Shape", ["Select"]+safe_unique(df,"Shape"), key=k(tab,"a1"))
        a2 = c2.selectbox(f"{color_col}", ["Select"]+safe_unique(df, color_col), key=k(tab,"a2"))
        a3 = c3.selectbox(f"{clarity_col}", ["Select"]+safe_unique(df, clarity_col), key=k(tab,"a3"))
        a4 = c4.selectbox("Carat", ["Select"]+safe_unique(df,"Size ranges"), key=k(tab,"a4"))

        go_age = st.form_submit_button("Apply")

        if go_age and "Select" not in [a1,a2,a3,a4]:

            temp = df[
                (df["Shape"].astype(str)==a1) &
                (df[color_col].astype(str)==a2) &
                (df[clarity_col].astype(str)==a3) &
                (df["Size ranges"].astype(str)==a4)
            ]

            st.session_state[k(tab,"aging_data")] = temp

    temp = st.session_state[k(tab,"aging_data")]

    if temp is not None and not temp.empty:

        st.dataframe(temp[[
            "Shape","Color","Clarity","Size",
            "ML_Aging_Risk_Score",
            "Risk Classification",
        ]].rename(columns={
            'ML_Aging_Risk_Score':'Aging Risk Score',
        }), use_container_width=True)

    elif temp is not None and temp.empty:
        st.warning("⚠️ No stone with these attributes exists in inventory")

    # ================= DATA =================
    st.markdown("## Data")

    if not filtered.empty:
        st.dataframe(filtered, use_container_width=True)
    else:
        st.warning("⚠️ No inventory stones available")
    


# ================= RUN =================
t1,t2,t3 = st.tabs(["Level 1","Level 2","Level 3"])

with t1:
    render_tab(level1,"L1")

with t2:
    render_tab(level2,"L2")

with t3:
    render_tab(level3,"L3")

