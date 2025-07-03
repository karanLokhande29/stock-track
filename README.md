
# 📦 Inventory Dashboard (Streamlit)

This is a smart inventory management dashboard built with **Streamlit**, tailored for pharmaceutical workflows at Precise Chemipharma. It allows real-time tracking of stock movement and status based on manufacturing dates, sales, and product category.

---

## 🚀 Features

- Upload raw Excel/CSV inventory data directly (no manual edits)
- Automatically categorizes:
  - ✅ Finished Goods
  - 🏭 Raw Materials
  - ⚙️ Work In Progress
- Flags inventory by status:
  - 🟥 Stuck > 6 months
  - 🟨 In Stock < 6 months
  - 🟩 Fully Sold
- View by:
  - Section (FG, RM, WIP)
  - Product/Material
  - Status
  - Unit
  - Date range
- Calculate Sales Value Summary (FG only)
- Export filtered results to CSV

---

## 📂 How to Run

1. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```

3. Upload your Excel/CSV file in the interface.

---

## 📝 Notes

- Your dataset must include at minimum:
  - `Section`, `Date`, `Unit`, `Product Name`, `Inward Qty`, `Manufacture Date`
  - Optional: `Sales Qty`, `Unit Price`, `Stage`, `Supervisor Notes`

- The dashboard intelligently calculates:
  - Remaining stock
  - Product age
  - Sales value

---

Built for Precise Chemipharma by Karan Lokhande 🚀
