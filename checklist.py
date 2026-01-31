import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Application Compliance Checklist",
    layout="wide"
)

# -------------------------------------------------
# STYLES (Govt Clean UI)
# -------------------------------------------------
st.markdown("""
<style>
.block-container {padding-top: 1rem;}

.section-card{
    background:#f5f7fa;
    padding:14px;
    border-radius:10px;
    margin-bottom:14px;
    border:1px solid #e0e0e0;
}

.ok {color:green;font-weight:600}
.notok {color:red;font-weight:600}
.na {color:orange;font-weight:600}
.pending {color:gray;font-weight:600}
</style>
""", unsafe_allow_html=True)

st.title("Application Validation & Compliance Checklist")

# -------------------------------------------------
# HEADER DETAILS (Mandatory)
# -------------------------------------------------
st.subheader("Audit Details")

c1, c2, c3 = st.columns(3)

programmer = c1.text_input("Programmer Name *")
programme = c2.text_input("Programme *")
category = c3.text_input("Category *")

auditor = st.text_input("Auditor Name (Digital Sign)")
approver = st.text_input("Approver Name (Digital Sign)")

if not all([programmer, programme, category]):
    st.warning("Please fill all mandatory fields to continue")
    st.stop()

# -------------------------------------------------
# MASTER CHECKLIST
# -------------------------------------------------
CHECKLIST = {
    "Application Setup": [
        ("Prospectus Upload", "Prospectus uploading"),
        ("Academic Year Configuration", "Correct academic year configured"),
        ("Age Limit Configuration", "Age limits set as per prospectus"),
        ("Certificate Format Configuration", "Certificate formats as per prospectus"),
    ],
    "Applicant Support": [
        ("Help Documentation Availability", "How to Apply, Fee Payment, Image Upload, Prerequisites"),
        ("Contact Information", "Helpdesk / Contact number"),
    ],
    "Access & Recovery": [
        ("Forgot Application Number", "Retrieval functionality working"),
        ("Forgot Password", "Password reset working correctly"),
        ("OTP Verification", "OTP generation and validation"),
    ],
    "Application Creation": [
        ("New Application Creation", "Application creation in local/live environment"),
        ("Field Validation", "Mandatory and optional fields validation"),
        ("Button & Navigation Check", "All menus and buttons functioning"),
        ("Save Draft / Resume", "Draft save and resume works"),
    ],
    "Application Submission": [
        ("Final Submission", "Submission successful without errors"),
    ],
    "Fee Management": [
        ("Application Fee – General", "Fee configuration for General category"),
        ("Application Fee – SC/ST", "Fee configuration for SC/ST category"),
        ("Payment Gateway Integration", "Payment gateway functionality"),
        ("Payment Handling", "Success / failure handling"),
    ],
    "Photo & Documents": [
        ("Live Photo Capture", "Live photo capture working"),
        ("Image Upload Validation", "Size, format, clarity validated"),
        ("Document Upload", "Certificates uploaded correctly"),
    ]
}

# -------------------------------------------------
# STATUS OPTIONS
# -------------------------------------------------
STATUS_OPTIONS = ["OK", "Not OK", "NA", "Pending"]

# -------------------------------------------------
# CHECKLIST UI
# -------------------------------------------------
st.subheader("Checklist Verification")

rows = []

for section, items in CHECKLIST.items():

    st.markdown(f"<div class='section-card'><h4>{section}</h4>", unsafe_allow_html=True)

    for item, desc in items:

        col1, col2, col3, col4 = st.columns([2.5, 3, 1.2, 2])

        with col1:
            st.write(item)

        with col2:
            st.caption(desc)

        with col3:
            status = st.selectbox("", STATUS_OPTIONS, key=item)

        with col4:
            remark = st.text_input("Remark", key="r_" + item)

        rows.append([section, item, desc, status, remark])

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# DATAFRAME
# -------------------------------------------------
df = pd.DataFrame(
    rows,
    columns=["Section", "Checklist Item", "Validation Points", "Status", "Remarks"]
)

# -------------------------------------------------
# COMPLIANCE SCORE
# -------------------------------------------------
total = len(df)
ok_count = len(df[df["Status"] == "OK"])
compliance = round((ok_count/total)*100, 1)

st.metric("Compliance Score", f"{compliance}%")

# -------------------------------------------------
# COLOR PREVIEW TABLE
# -------------------------------------------------
def color_status(val):
    if val == "OK":
        return "background-color:#d4edda"
    if val == "Not OK":
        return "background-color:#f8d7da"
    if val == "NA":
        return "background-color:#fff3cd"
    return ""

styled = df.style.applymap(color_status, subset=["Status"])
st.dataframe(styled, use_container_width=True)

# -------------------------------------------------
# EXCEL EXPORT
# -------------------------------------------------
def to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False)
    return output.getvalue()

st.download_button(
    "⬇ Download Excel",
    to_excel(df),
    file_name="checklist_report.xlsx"
)

# -------------------------------------------------
# HTML (PDF) EXPORT — CLOUD SAFE
# -------------------------------------------------
def generate_html_report(dataframe):

    table_html = dataframe.to_html(index=False)

    html = f"""
    <html>
    <head>
    <style>
    body{{font-family:Arial}}
    table{{border-collapse:collapse;width:100%}}
    th,td{{border:1px solid #000;padding:6px;font-size:12px}}
    th{{background:#eee}}
    </style>
    </head>

    <body>
    <h2>Application Compliance Report</h2>

    <p>
    <b>Programmer:</b> {programmer}<br>
    <b>Programme:</b> {programme}<br>
    <b>Category:</b> {category}<br>
    <b>Auditor:</b> {auditor}<br>
    <b>Approver:</b> {approver}<br>
    <b>Date:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}
    </p>

    {table_html}

    <br><br>
    Auditor Signature: ______________________ <br><br>
    Approver Signature: _____________________
    </body>
    </html>
    """

    return html.encode()

st.download_button(
    "⬇ Download PDF Report",
    generate_html_report(df),
    file_name="checklist_report.html",
    mime="text/html"
)

st.info("Open the downloaded file → Press Ctrl+P → Save as PDF")

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.divider()
st.success("Checklist ready for audit submission")
