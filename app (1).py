import streamlit as st
import pandas as pd

st.set_page_config(page_title="📦 Inventory Stock Tracking System", layout="wide")
st.title("📦 Inventory Stock Tracking System – Complete View")

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

        # Metrics
        st.markdown("### 📊 Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("📥 Total Inward Value", f"₹ {filtered_df['Inward Value'].sum():,.2f}")
        col2.metric("📤 Total Outward Value", f"₹ {filtered_df['Outward Value'].sum():,.2f}")
        col3.metric("📦 Closing Value", f"₹ {filtered_df['Closing Value'].sum():,.2f}")

        # Table
        st.markdown("### 📋 Inventory Details")
        st.dataframe(filtered_df, use_container_width=True)

        # Download filtered CSV
        csv_download = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Filtered CSV", data=csv_download, file_name="filtered_inventory.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

else:
    st.info("Please upload the `cleaned_inventory_complete.csv` file to get started.")
