import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Application Audit Checklist",
    layout="wide"
)

# -------------------------------------------------
# STYLES (Better UI)
# -------------------------------------------------
st.markdown("""
<style>
.block-container {padding-top: 1.5rem;}
.section-card {
    padding: 14px;
    border-radius: 10px;
    background: #f6f8fa;
    margin-bottom: 15px;
}
.ok {color: green; font-weight:600}
.notok {color: red; font-weight:600}
.na {color: orange; font-weight:600}
.pending {color: gray; font-weight:600}
</style>
""", unsafe_allow_html=True)

st.title("Application Validation & Compliance Checklist")

# -------------------------------------------------
# CHECKLIST MASTER
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
# HEADER DETAILS
# -------------------------------------------------
st.subheader("Audit Details")

c1, c2, c3 = st.columns(3)

programmer = c1.text_input("Programmer Name *")
programme = c2.text_input("Programme *")
category = c3.text_input("Category *")

auditor = st.text_input("Auditor Name (Digital Sign)")
approver = st.text_input("Approver Name (Digital Sign)")

if not all([programmer, programme, category]):
    st.warning("Fill mandatory fields to continue")
    st.stop()

# -------------------------------------------------
# CHECKLIST FORM
# -------------------------------------------------
results = []

status_colors = {
    "OK": "ok",
    "Not OK": "notok",
    "NA": "na",
    "Pending": "pending"
}

st.subheader("Checklist")

for section, items in CHECKLIST.items():

    st.markdown(f"<div class='section-card'><h4>{section}</h4>", unsafe_allow_html=True)

    for item, desc in items:
        c1, c2, c3, c4 = st.columns([2.5, 3, 1.2, 2])

        with c1:
            st.write(item)

        with c2:
            st.caption(desc)

        with c3:
            status = st.selectbox(
                "",
                ["OK", "Not OK", "NA", "Pending"],
                key=item
            )

        with c4:
            remark = st.text_input("Remark", key="r_"+item)

        results.append([section, item, desc, status, remark])

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# DATAFRAME
# -------------------------------------------------
df = pd.DataFrame(
    results,
    columns=["Section", "Checklist Item", "Validation Points", "Status", "Remarks"]
)

# -------------------------------------------------
# COMPLIANCE %
# -------------------------------------------------
total = len(df)
ok_count = len(df[df["Status"] == "OK"])
compliance = round((ok_count/total)*100, 1)

st.metric("Compliance Score", f"{compliance}%")

# -------------------------------------------------
# EXCEL EXPORT
# -------------------------------------------------
def to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False)
    return output.getvalue()

excel_data = to_excel(df)

st.download_button(
    "⬇ Download Excel",
    excel_data,
    file_name="checklist_report.xlsx"
)

# -------------------------------------------------
# PDF EXPORT (CERT STYLE)
# -------------------------------------------------
def generate_pdf(dataframe):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Application Compliance Report", styles["Heading1"]))
    elements.append(Spacer(1, 10))

    meta = f"""
    Programmer: {programmer}<br/>
    Programme: {programme}<br/>
    Category: {category}<br/>
    Auditor: {auditor}<br/>
    Approver: {approver}<br/>
    Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}
    """
    elements.append(Paragraph(meta, styles["Normal"]))
    elements.append(Spacer(1, 15))

    table_data = [dataframe.columns.tolist()] + dataframe.values.tolist()

    table = Table(table_data, repeatRows=1)

    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
        ('GRID',(0,0),(-1,-1),0.5,colors.black),
        ('FONTSIZE',(0,0),(-1,-1),8),
    ]))

    elements.append(table)
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    return pdf

pdf_data = generate_pdf(df)

st.download_button(
    "⬇ Download PDF (CERT-In Format)",
    pdf_data,
    file_name="checklist_report.pdf"
)

# -------------------------------------------------
# TABLE PREVIEW
# -------------------------------------------------
st.subheader("Report Preview")
st.dataframe(df, use_container_width=True)

st.success("Ready for audit submission")
