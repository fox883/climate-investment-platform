import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import numpy as np

# Page Config
st.set_page_config(page_title="Project Plan and Resource Management", layout="wide")
st.title("📋 Project Plan and Resource Management")

# -------------------------------
# Specialist Directory
# -------------------------------
specialists_data = {
    "Name": [
        "Amina Yusuf", "Julie Omondi", "Alice Wong", "Imran Sayed",
        "Priya Devani", "Philippe Renaud", "Oscar Tan", "Helena Hills"
    ],
    "Role": [
        "Gender Specialist", "Safeguards Specialist", "Writer", "Legal Liaison",
        "Project Lead", "TTL Support", "Finance Advisor", "IC Reviewer"
    ],
    "Division": ["OCIO"] * 8,
    "Weeks Available": [
        "W2–5, W10–11", "W3–11", "W2–10", "W10–12",
        "W1–W12", "W4–W12", "W1–W6", "W5–W12"
    ],
    "Max Weekly Hours": [20, 18, 25, 15, 30, 20, 10, 15]
}
df_specialists = pd.DataFrame(specialists_data)

st.subheader("👥 Specialist Directory")
st.dataframe(df_specialists, use_container_width=True)

# -------------------------------
# Project Tasks
# -------------------------------
project_tasks_data = {
    "Task ID": [101, 102, 103, 104, 105],
    "Task Name": [
        "Draft Theory of Change",
        "Gender Diagnostic",
        "Legal Review for Pre-Appraisal",
        "Finalize CN for Submission",
        "Board Pack Assembly"
    ],
    "Stage": [
        "Concept Note",
        "Concept Note",
        "Pre-Appraisal",
        "Pre-Appraisal",
        "Board Meeting"
    ],
    "Week": ["W2", "W3", "W10", "W6", "W12"],
    "Assigned To": ["Unassigned"] * 5,
    "Est. Hours": [16, 10, 12, 20, 18]
}
df_project_tasks = pd.DataFrame(project_tasks_data)

# -------------------------------
# Task Filter + Assignment
# -------------------------------
st.subheader("📌 Filter Tasks by Stage")
selected_stage = st.selectbox("Select Stage", df_project_tasks["Stage"].unique())

filtered_tasks = df_project_tasks[df_project_tasks["Stage"] == selected_stage].copy()
assigned_hours = {}

for idx in filtered_tasks.index:
    task_name = filtered_tasks.loc[idx, "Task Name"]
    task_id = filtered_tasks.loc[idx, "Task ID"]
    est_hours = filtered_tasks.loc[idx, "Est. Hours"]

    assigned = st.selectbox(
        f"Assign specialist to task: {task_name}",
        options=["Unassigned"] + df_specialists["Name"].tolist(),
        key=f"assign_{task_id}"
    )
    filtered_tasks.at[idx, "Assigned To"] = assigned

    if assigned != "Unassigned":
        assigned_hours[assigned] = assigned_hours.get(assigned, 0) + est_hours

# Update specialist view to show remaining hours
df_specialists["Remaining Hours"] = df_specialists.apply(
    lambda row: row["Max Weekly Hours"] - assigned_hours.get(row["Name"], 0),
    axis=1
)

st.subheader("🧑‍🔧 Updated Specialist Availability")
st.dataframe(df_specialists, use_container_width=True)

# Show updated task table too
st.subheader("🧾 Assigned Tasks")
st.dataframe(filtered_tasks, use_container_width=True)

# -------------------------------
# Risk Evaluation
# -------------------------------
stage_total_hours = filtered_tasks["Est. Hours"].sum()
available_hours = df_specialists["Max Weekly Hours"].sum()

if stage_total_hours < 0.6 * available_hours:
    risk_flag = "✅ On Track"
elif stage_total_hours < available_hours:
    risk_flag = "🟡 Tight Capacity"
else:
    risk_flag = "⛔ Overloaded"

st.markdown(f"""
### 🧠 Stage Capacity Risk Alert
- **Stage:** `{selected_stage}`
- **Required Hours:** {stage_total_hours}
- **Available Capacity (Est.):** {available_hours}
- **Risk Status:** {risk_flag}
""")

# -------------------------------
# Resource Summary
# -------------------------------
st.subheader("🔢 Resource Summary")

weekly_hours = df_project_tasks.groupby("Week")["Est. Hours"].sum().reset_index(name="Total Task Hours")
stage_hours = df_project_tasks.groupby("Stage")["Est. Hours"].sum().reset_index(name="Total Hours This Stage")

st.markdown("**📅 Total Weekly Hours**")
st.dataframe(weekly_hours, use_container_width=True)

st.markdown("**📂 Total Stage Hours**")
st.dataframe(stage_hours, use_container_width=True)

# -------------------------------
# Gantt Chart - 9-month timeline from Jan 1, 2025
# -------------------------------

# Project stages (use pure datetime)
start_date = datetime.datetime(2025, 1, 1)
concept_note_start = start_date
concept_note_end = concept_note_start + datetime.timedelta(weeks=7)

pre_appraisal_start = concept_note_end + datetime.timedelta(weeks=1)
pre_appraisal_end = pre_appraisal_start + datetime.timedelta(weeks=4)

board_meeting_start = pre_appraisal_end + datetime.timedelta(weeks=1)
board_meeting_end = board_meeting_start + datetime.timedelta(weeks=3)

# Use pure datetime for all
today = datetime.datetime.today()

# Gantt DataFrame
gantt_data = pd.DataFrame({
    "Stage": ["Concept Note", "Pre-Appraisal", "Board Meeting"],
    "Start": [concept_note_start, pre_appraisal_start, board_meeting_start],
    "Finish": [concept_note_end, pre_appraisal_end, board_meeting_end],
    "Status": ["✅ Complete", "🟡 In Progress", "⏳ Upcoming"]
})

# Create Plot
fig = px.timeline(
    gantt_data,
    x_start="Start",
    x_end="Finish",
    y="Stage",
    color="Status",
    title="📊 Project Stage Timeline"
)

# ✅ Remove annotation to avoid internal bug
fig.add_vline(
    x=today,
    line_width=2,
    line_dash="dash",
    line_color="red"
)

fig.update_yaxes(categoryorder="total ascending")
st.plotly_chart(fig, use_container_width=True)
# -------------------------------
# Project Financial and Resource Health Matrix
# -------------------------------
st.subheader("📊 Project Financial & Health Matrix")

resource_matrix = pd.DataFrame({
    "Metric": [
        "Total Estimated Task Hours",
        "Total Specialist Capacity",
        "Available Budget ($)",
        "Estimated Cost ($)",
        "Financial Feasibility",
        "Current Risk Status",
        "Overall Project Health"
    ],
    "Value": [
        76,
        153,
        "$250,000",
        "$180,000",
        "✅ Sufficient",
        risk_flag,
        "🟢 Healthy"
    ]
})
st.dataframe(resource_matrix, use_container_width=True)

# -------------------------------
# Final Advisory
# -------------------------------
st.subheader("✅ System Judgement")

st.markdown("""
- ✅ Concept Note stage complete.
- 🟡 Pre-Appraisal is progressing; monitor capacity for Week 10–12.
- ⛔️ Board preparation needs extra resources by April.
- 💰 Budget is adequate.
- 🧠 Recommendation: Add safeguards/legal staff for April and validate delivery before Gate.
""")
