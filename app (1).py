import streamlit as st
import pandas as pd

st.set_page_config(page_title="📦 Inventory Stock Tracker", layout="wide")
st.title("📦 Inventory Stock Tracking System – Grand Total View")

uploaded_file = st.file_uploader("📤 Upload Cleaned Inventory CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Sidebar filters
        st.sidebar.header("🔎 Filter Options")
        search_term = st.sidebar.text_input("🔍 Search Product Name")
        move_filter = st.sidebar.multiselect(
            "📦 Filter by Movement Status",
            options=["Moved", "Not Moved"],
            default=["Moved", "Not Moved"]
        )

        filtered_df = df[df["Movement Status"].isin(move_filter)]

        if search_term:
            filtered_df = filtered_df[filtered_df["Product Name"].str.contains(search_term, case=False)]

        # === Grand Totals ===
        st.markdown("### 📊 Grand Totals")
        total_opening = df["Opening Value"].sum()
        total_inward = df["Inward Value"].sum()
        total_outward = df["Outward Value"].sum()
        total_closing = df["Closing Value"].sum()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏁 Opening Value (All)", f"₹ {total_opening:,.2f}")
            st.metric("📥 Inward Value (All)", f"₹ {total_inward:,.2f}")
        with col2:
            st.metric("📤 Outward Value (All)", f"₹ {total_outward:,.2f}")
            st.metric("📦 Closing Value (All)", f"₹ {total_closing:,.2f}")

        # === Filtered Table ===
        st.markdown("### 📋 Inventory Details (Filtered)")
        st.dataframe(filtered_df, use_container_width=True)

        # Download filtered CSV
        csv_download = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Filtered CSV", data=csv_download, file_name="filtered_inventory.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("📤 Please upload the `cleaned_inventory_complete.csv` file to get started.")
