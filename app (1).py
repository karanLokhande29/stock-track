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
        # === CASE 1: CSV Upload ===
        if uploaded_file.name.endswith(".csv"):
            df_raw = pd.read_csv(uploaded_file, skiprows=1)
            df_cleaned = df_raw.iloc[:, [0, 1, 5, 9, 13, 15, 16]].copy()
            df_cleaned.columns = [
                "Product Name", "Opening Qty", "Inward Qty", "Outward Qty",
                "Closing Qty", "Closing Rate", "Total Value"
            ]
            for col in ["Opening Qty", "Inward Qty", "Outward Qty", "Closing Qty", "Closing Rate", "Total Value"]:
                df_cleaned[col] = df_cleaned[col].apply(clean_number)

        # === CASE 2: XLSX Upload ===
        else:
            df_excel = pd.read_excel(uploaded_file, sheet_name="Stock Category Summary", engine="openpyxl")
            df_cleaned = df_excel.iloc[15:, [0, 1, 5, 9, 13, 14, 16]].copy()
            df_cleaned.columns = [
                "Product Name", "Opening Qty", "Inward Qty", "Outward Qty",
                "Closing Qty", "Closing Rate", "Total Value"
            ]
            for col in ["Opening Qty", "Inward Qty", "Outward Qty", "Closing Qty", "Closing Rate", "Total Value"]:
                df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors="coerce").fillna(0)

        # Add movement status
        df_cleaned["Movement Status"] = df_cleaned.apply(
            lambda row: "Moved" if (row["Inward Qty"] > 0 or row["Outward Qty"] > 0) else "Not Moved", axis=1
        )

        # === FILTERS ===
        st.sidebar.header("🔎 Filters")
        search = st.sidebar.text_input("Search Product Name")
        status_filter = st.sidebar.multiselect("Movement Status", ["Moved", "Not Moved"], default=["Moved", "Not Moved"])

        filtered = df_cleaned[df_cleaned["Movement Status"].isin(status_filter)]
        if search:
            filtered = filtered[filtered["Product Name"].str.contains(search, case=False)]

        # === METRICS ===
        total_moved = filtered[filtered["Movement Status"] == "Moved"]["Total Value"].sum()
        total_not_moved = filtered[filtered["Movement Status"] == "Not Moved"]["Total Value"].sum()

        st.markdown("### 📊 Summary")
        col1, col2 = st.columns(2)
        col1.metric("💰 Total Value – Moved", f"₹ {total_moved:,.2f}")
        col2.metric("🚫 Total Value – Not Moved", f"₹ {total_not_moved:,.2f}")

        # === COLORED TABLE ===
        def color_row(row):
            return ["background-color: #ffcccc" if row["Movement Status"] == "Not Moved"
                    else "background-color: #ccffcc"] * len(row)

        st.markdown("### 📋 Detailed Inventory")
        st.dataframe(filtered.style.apply(color_row, axis=1), use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

else:
    st.info("📤 Please upload your stock summary `.csv` or `.xlsx` file.")
