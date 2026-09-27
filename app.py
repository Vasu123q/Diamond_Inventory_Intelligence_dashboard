import streamlit as st

st.set_page_config(layout="wide")


st.title("💎 Diamond Inventory Intelligence💎")
st.markdown("### Smart analytics for Inventory, demand & sales")

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.markdown("### Inventory Stones")
    st.write("Explore full Inventory Stones and view Insights and Demands of the Stones.")
    if st.button("Go to Inventory Stones"):
        st.switch_page("pages/1_Inventory_Stones.py")

with c2:
    st.markdown("###  Stone Status")
    st.write("Track Stone Status Location Wise")
    if st.button("Go to Stones Status"):
        st.switch_page("pages/2_Stone_Status.py")

