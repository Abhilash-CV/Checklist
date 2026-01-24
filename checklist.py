import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Programme Checklist & Report",
    layout="wide"
)

st.title("Programme Checklist & Report")

# -----------------------------
# Master Data
# -----------------------------
PROGRAMMES = [
    "KEAM",
    "BPHARM",
    "BPHARM LE",
    "ENGINEERING",
    "MEDICAL",
    "ARCHITECTURE"
]

CATEGORIES = [
    "Development",
    "Testing",
    "Deployment",
    "Audit",
    "Maintenance"
]

CHECKLIST_ITEMS = [
    "Requirements verified",
    "Code review completed",
    "Database validation done",
    "Security checks completed",
    "Performance tested",
    "Documentation updated",
    "Approval obtained"
]

# -----------------------------
# Input Section
# -----------------------------
st.subheader("Mandatory Details")

col1, col2, col3 = st.columns(3)

with col1:
    programmer_name = st.text_input("Programmer Name *")

with col2:
    programme = st.selectbox("Programme *", [""] + PROGRAMMES)

with col3:
    category = st.selectbox("Category *", [""] + CATEGORIES)

# -----------------------------
# Validation
# -----------------------------
mandatory_ok = all([
    programmer_name.strip() != "",
    programme != "",
    category != ""
])

if not mandatory_ok:
    st.warning("Please fill all mandatory fields (*) to proceed.")

st.divider()

# -----------------------------
# Report Type Selection
# -----------------------------
report_type = st.radio(
    "Select View",
    ["Checklist View", "Report View"],
    horizontal=True,
    disabled=not mandatory_ok
)

# -----------------------------
# Checklist View
# -----------------------------
if report_type == "Checklist View" and mandatory_ok:
    st.subheader("Checklist")

    checklist_status = {}
    for item in CHECKLIST_ITEMS:
        checklist_status[item] = st.checkbox(item)

    if st.button("Generate Report"):
        completed = sum(checklist_status.values())
        total = len(CHECKLIST_ITEMS)

        st.success("Checklist report generated successfully.")

        report_data = {
            "Programmer Name": programmer_name,
            "Programme": programme,
            "Category": category,
            "Checklist Completed": f"{completed} / {total}",
            "Generated On": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

        st.subheader("Checklist Summary")
        st.json(report_data)

# -----------------------------
# Report View (Tabular)
# -----------------------------
if report_type == "Report View" and mandatory_ok:
    st.subheader("Report View")

    report_rows = []
    for item in CHECKLIST_ITEMS:
        report_rows.append({
            "Programme": programme,
            "Category": category,
            "Checklist Item": item,
            "Status": "Pending"
        })

    df = pd.DataFrame(report_rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        f"Report generated for **{programme}** under **{category}** "
        f"by **{programmer_name}**"
    )

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("© Programme Checklist System | Internal Use Only")
