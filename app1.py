import streamlit as st
from database1 import create_table, insert_defect, get_all_defects
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import os
import io

st.set_page_config(page_title="Vehicle-Parts Defect Enlister", page_icon="🚒", layout="wide")
# -----------------------------
# 📦 Initial Setup
# -----------------------------
st.set_page_config(page_title="Defect Enlister", layout="wide")
st.title("🛠️ Smart Defect Enlister & Tracker")
create_table()
# -----------------------------
# 📊 Project Summary
# -----------------------------
rows = get_all_defects()
df = pd.DataFrame(rows, columns=[
    "ID", "Reported Date", "Module", "Description", "Severity",
    "Status", "Assigned To", "Resolution Date", "Image"
])

st.markdown("### 📊 Project Summary")
col1, col2, col3 = st.columns(3)

total = len(df)
open_count = df[df["Status"] == "Open"].shape[0]
high_sev = df[df["Severity"] == "High"].shape[0]

col1.metric("📌 Total Defects", total)
col2.metric("🟠 Open Defects", open_count)
col3.metric("🚨 High Severity", high_sev)

# -----------------------------
# 📝 Log a New Defect
# -----------------------------
st.header("📥 Log a New Defect")
with st.form("defect_form"):
    st.markdown("### 📝 Enter Defect Details")

    col1, col2 = st.columns(2)

    with col1:
        module = st.selectbox("Module Name", [
    "Engine", "Transmission", "Braking System", "Electrical System",
    "Fuel System", "Suspension", "Cabin Controls", "Exhaust/Emission",
    "Cooling System", "Steering System", "Others")]
# Show input box if "Others" is selected
if module == "Others":
    custom_module = st.text_input("Please specify the system")
    final_module = custom_module
else:
    final_module = module

        severity = st.selectbox("Severity", ["Low", "Medium", "High"])
        status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
        vehicle_model = st.selectbox("Vehicle Model", ["Prima 2825", "Prima 3530", "Prima 5530", "Others"])
        if vehicle_model == "Others":
    custom_model = st.text_input("Please specify the vehicle model")
    final_model = custom_model
else:
    final_model = vehicle_model

    with col2:
        assigned_to = st.text_input("Assigned To")
        defect_category = st.selectbox("Defect Category", ["Mechanical", "Electrical", "Software", "Others"])
        reported_by = st.text_input("Reported By")
        date_reported = st.date_input("Reported On", date.today())
        resolution_date = st.date_input("Resolution Date", date.today())

    description = st.text_area("Defect Description")
    image = st.file_uploader("Upload Defect Image (optional)", type=["jpg", "jpeg", "png"])
    confirm = st.checkbox("✅ I confirm the details are correct")
    submit = st.form_submit_button("🚀 Submit Defect")
  if submit:
        if not final_module or not description:
            st.warning("❗ Please fill in the required fields.")
        elif resolution_date < date_reported:
            st.warning("❗ Resolution date cannot be before Reported date.")
        elif not confirm:
            st.warning("❗ Please confirm before submitting.")
        else:
            image_path = ""
            if image:
                os.makedirs("uploads", exist_ok=True)
                image_path = os.path.join("uploads", image.name)
                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())

            # 🔄 Use final_module and final_model
            insert_defect(
                str(date_reported), final_module, description, severity, status,
                assigned_to, str(resolution_date), image_path,
                final_model, defect_category, reported_by
            )
            st.success("✅ Defect logged successfully!")

# -----------------------------
# 🔍 Filter Defects
# -----------------------------
with st.expander("🔍 Filter Defects"):
    st.subheader("🎛️ Filter Options")

    available_modules = df["Module"].unique()
    available_severities = df["Severity"].unique()

    selected_modules = st.multiselect("Select Module(s):", available_modules, default=list(available_modules))
    selected_severities = st.multiselect("Select Severity Level(s):", available_severities, default=list(available_severities))

    filtered_df = df[
        (df["Module"].isin(selected_modules)) &
        (df["Severity"].isin(selected_severities))
    ]

rows = get_all_defects()
df = pd.DataFrame(rows, columns=[
    "ID", "Reported Date", "Module", "Description", "Severity",
    "Status", "Assigned To", "Resolution Date", "Image"
])

if not df.empty:
    available_modules = df["Module"].unique()
    available_severities = df["Severity"].unique()

    selected_modules = st.multiselect("Select Module(s):", available_modules, default=list(available_modules))
    selected_severities = st.multiselect("Select Severity Level(s):", available_severities, default=list(available_severities))

    filtered_df = df[
        (df["Module"].isin(selected_modules)) &
        (df["Severity"].isin(selected_severities))
    ]
else:
    filtered_df = df.copy()

# -----------------------------
# 📋 Display Table
# -----------------------------
st.header("📋 Filtered Defect Log")
st.dataframe(filtered_df)

# -----------------------------
# 📊 Severity Chart
# -----------------------------
st.header("Defects by Severity (Filtered)")
if not filtered_df.empty:
    severity_counts = filtered_df["Severity"].value_counts()
    color_map = {"High": "red", "Medium": "orange", "Low": "green"}
    colors = [color_map.get(sev, "gray") for sev in severity_counts.index]

    fig, ax = plt.subplots()
    severity_counts.plot(kind='bar', color=colors, ax=ax)
    ax.set_ylabel("Number of Defects")
    ax.set_title("Severity-wise Defect Count (Filtered)")
    st.pyplot(fig)
else:
    st.info("No defects match the selected filters.")

# -----------------------------
# 📤 Export Options
# -----------------------------
st.subheader("⬇️ Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(" ⬇️Download as CSV", csv, "defects_filtered.csv", "text/csv")

excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
    filtered_df.to_excel(writer, index=False, sheet_name="Defects")        
st.download_button(
    "📊 Download as Excel", excel_buffer.getvalue(),
    "defects_filtered.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# -----------------------------
# 🖼️ Image Previews
# -----------------------------
with st.expander("🖼️ Uploaded Defect Images"):
    for index, row in filtered_df.iterrows():
        if row["Image"]:
            try:
                st.image(row["Image"], caption=f"{row['Module']} – {row['Description'][:30]}...", use_column_width=True)
            except Exception as e:
                st.error(f"Image could not be loaded for {row['Module']} - {e}")

