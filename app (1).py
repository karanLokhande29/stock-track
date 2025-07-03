
# Streamlit Dashboard for Inventory Management

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Inventory Dashboard", layout="wide")
st.title("📦 Smart Inventory Status Dashboard")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Inventory Excel File", type=["csv", "xlsx"])

if uploaded_file:
    # Read the file
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
    else:
        # Standardize column names
        df.columns = df.columns.str.strip()

        # Parse dates
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Manufacture Date'] = pd.to_datetime(df['Manufacture Date'], errors='coerce')

        # Replace NaNs for optional columns
        if 'Sales Qty' not in df.columns:
            df['Sales Qty'] = 0
        if 'Unit Price' not in df.columns:
            df['Unit Price'] = 0
        if 'Value' not in df.columns:
            df['Value'] = df['Inward Qty'] * df['Unit Price']
        if 'Supervisor Notes' not in df.columns:
            df['Supervisor Notes'] = ""

        # Sidebar filters
        st.sidebar.header("📅 Date Range Filter")
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        start_date = st.sidebar.date_input("Start Date", min_date)
        end_date = st.sidebar.date_input("End Date", max_date)

        # Filter by date range
        df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

        # Section Tabs
        sections = ['Finished Goods', 'Raw Materials', 'Work In Progress']
        tab_fg, tab_rm, tab_wip = st.tabs(sections)

        def process_and_display(tab, section_name):
            with tab:
                st.subheader(f"🔍 {section_name} Overview")
                sec_df = df[df['Section'] == section_name].copy()

                # Derived columns
                today = pd.to_datetime(end_date)
                sec_df['Remaining Qty'] = sec_df['Inward Qty'] - sec_df['Sales Qty'].fillna(0)
                sec_df['Stock Age (Days)'] = (today - sec_df['Manufacture Date']).dt.days

                # Assign status
                def get_status(row):
                    if row['Remaining Qty'] <= 0:
                        return '🟩 Cleared'
                    elif row['Stock Age (Days)'] > 180:
                        return '🟥 Stuck > 6 Months'
                    else:
                        return '🟨 In Stock < 6 Months'

                sec_df['Status'] = sec_df.apply(get_status, axis=1)

                # Filters
                with st.expander("🔧 Filters"):
                    unit_filter = st.multiselect("Select Unit", sec_df['Unit'].unique(), default=sec_df['Unit'].unique())
                    product_filter = st.multiselect("Select Product", sec_df['Product Name'].unique(), default=sec_df['Product Name'].unique())
                    status_filter = st.multiselect("Select Status", sec_df['Status'].unique(), default=sec_df['Status'].unique())

                sec_df = sec_df[
                    sec_df['Unit'].isin(unit_filter) &
                    sec_df['Product Name'].isin(product_filter) &
                    sec_df['Status'].isin(status_filter)
                ]

                # Display Data
                st.dataframe(sec_df, use_container_width=True)

                # Sales Summary (FG only)
                if section_name == 'Finished Goods':
                    st.markdown("### 💰 Sales Value Summary")
                    sales_summary = sec_df.copy()
                    sales_summary['Sales Value'] = sales_summary['Sales Qty'] * sales_summary['Unit Price']
                    st.dataframe(
                        sales_summary.groupby('Status')[['Sales Qty', 'Sales Value']].sum().style.format("{:.2f}"),
                        use_container_width=True
                    )

                # Export Option
                csv = sec_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Filtered Data", data=csv, file_name=f"{section_name}_filtered.csv", mime='text/csv')

        # Display each tab
        process_and_display(tab_fg, 'Finished Goods')
        process_and_display(tab_rm, 'Raw Materials')
        process_and_display(tab_wip, 'Work In Progress')
