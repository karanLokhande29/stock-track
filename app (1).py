import streamlit as st
import pandas as pd

st.set_page_config(page_title="📦 Inventory Movement Tracker", layout="wide")
st.title("📦 Inventory Movement Tracker – Unit 1")

uploaded_file = st.file_uploader("Upload Stock Summary Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Stock Category Summary")

        # Extract relevant columns (based on known structure)
        data = df.iloc[15:, [0, 1, 5, 9, 13, 14, 16]].copy()
        data.columns = [
            "Product Name", "Opening Qty", "Inward Qty", "Outward Qty",
            "Closing Qty", "Closing Rate", "Total Value"
        ]
        data = data.dropna(subset=["Product Name"]).reset_index(drop=True)

        # Convert to numeric
        for col in ["Opening Qty", "Inward Qty", "Outward Qty", "Closing Qty", "Closing Rate", "Total Value"]:
            data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

        # Add movement status
        data["Movement Status"] = data.apply(
            lambda row: "Moved" if (row["Inward Qty"] > 0 or row["Outward Qty"] > 0) else "Not Moved", axis=1
        )

        # Filters
        st.sidebar.header("🔎 Filters")
        search = st.sidebar.text_input("Search Product Name")
        status_filter = st.sidebar.multiselect("Movement Status", ["Moved", "Not Moved"], default=["Moved", "Not Moved"])

        filtered_data = data[
            data["Movement Status"].isin(status_filter)
        ]

        if search:
            filtered_data = filtered_data[filtered_data["Product Name"].str.contains(search, case=False)]

        # Metrics
        total_moved = filtered_data[filtered_data["Movement Status"] == "Moved"]["Total Value"].sum()
        total_not_moved = filtered_data[filtered_data["Movement Status"] == "Not Moved"]["Total Value"].sum()

        st.markdown("### 📊 Summary")
        col1, col2 = st.columns(2)
        col1.metric("💰 Total Value – Moved", f"₹ {total_moved:,.2f}")
        col2.metric("🚫 Total Value – Not Moved", f"₹ {total_not_moved:,.2f}")

        # Apply row styling
        def color_row(row):
            color = "background-color: #ffcccc" if row["Movement Status"] == "Not Moved" else "background-color: #ccffcc"
            return [color] * len(row)

        styled_df = filtered_data.style.apply(color_row, axis=1)

        st.markdown("### 📋 Detailed Inventory")
        st.dataframe(styled_df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("📤 Please upload a valid stock summary Excel file.")
