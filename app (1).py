import streamlit as st
import pandas as pd

st.set_page_config(page_title="📦 Inventory Movement Tracker", layout="wide")
st.title("📦 Inventory Movement Tracker – Unit 1")

uploaded_file = st.file_uploader("Upload Stock Summary File (.xlsx or .csv)", type=["xlsx", "csv"])

def clean_number(value):
    if isinstance(value, str):
        parts = value.split()
        try:
            return float(parts[0].replace(",", ""))
        except:
            return 0.0
    return value if pd.notnull(value) else 0.0

if uploaded_file:
    try:
        # === CASE 1: CSV ===
        if uploaded_file.name.endswith(".csv"):
            df_raw = pd.read_csv(uploaded_file, skiprows=1)
            df_cleaned = df_raw.iloc[:, [0, 1, 5, 9, 13, 15, 16]].copy()
            df_cleaned.columns = [
                "Product Name", "Opening Qty", "Inward Qty", "Outward Qty",
                "Closing Qty", "Closing Rate", "Total Value"
            ]
            for col in ["Opening Qty", "Inward Qty", "Outward Qty", "Closing Qty", "Closing Rate", "Total Value"]:
                df_cleaned[col] = df_cleaned[col].apply(clean_number)

        # === CASE 2: XLSX ===
        else:
            df_excel = pd.read_excel(uploaded_file, sheet_name="Stock Category Summary", engine="openpyxl")
            df_cleaned = df_excel.iloc[15:, [0, 1, 5, 9, 13, 14, 16]].copy()
            df_cleaned.columns = [
                "Product Name", "Opening Qty", "Inward Qty", "Outward Qty",
                "Closing Qty", "Closing Rate", "Total Value"
            ]
            for col in ["Opening Qty", "Inward Qty", "Outward Qty", "Closing Qty", "Closing Rate", "Total Value"]:
                df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors="coerce").fillna(0)

        # Add Movement Status Column
        df_cleaned["Movement Status"] = df_cleaned.apply(
            lambda row: "Moved" if (row["Inward Qty"] > 0 or row["Outward Qty"] > 0) else "Not Moved", axis=1
        )

        # === SIDEBAR FILTERS ===
        st.sidebar.header("🔎 Filters")
        search = st.sidebar.text_input("Search Product Name")
        movement_filter = st.sidebar.radio("Select Movement Type", ["All", "Moved", "Not Moved"], index=0)

        # Apply filters
        filtered = df_cleaned.copy()
        if movement_filter != "All":
            filtered = filtered[filtered["Movement Status"] == movement_filter]

        if search:
            filtered = filtered[filtered["Product Name"].str.contains(search, case=False)]

        # === SUMMARY ===
        total_moved = df_cleaned[df_cleaned["Movement Status"] == "Moved"]["Total Value"].sum()
        total_not_moved = df_cleaned[df_cleaned["Movement Status"] == "Not Moved"]["Total Value"].sum()

        st.markdown("### 📊 Summary")
        col1, col2 = st.columns(2)
        col1.metric("💰 Total Sales – Moved", f"₹ {total_moved:,.2f}")
        col2.metric("🚫 Total Sales – Not Moved", f"₹ {total_not_moved:,.2f}")

        # === TABLE ===
        st.markdown("### 📋 Inventory Data")
        st.dataframe(filtered, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("📤 Please upload a `.csv` or `.xlsx` stock summary file.")
