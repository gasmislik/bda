import streamlit as st
import pandas as pd
import subprocess

st.set_page_config(page_title="Exam Planning Dashboard", layout="wide")

# ===============================
# Load data
# ===============================
examens = pd.read_csv("planning_examens_dashboard.csv")
examens["date_exam"] = pd.to_datetime(examens["date_exam"], errors="coerce")
examens["prof"] = examens["prof"].fillna("Not scheduled")

# ===============================
# Sidebar
# ===============================
st.sidebar.title("User Role")
role = st.sidebar.selectbox(
    "Choose your role",
    [
        "Vice Dean / Dean",
        "Exam Administrator",
        "Department Head",
        "Student / Professor"
    ]
)

# ===============================
# Vice Dean / Dean
# ===============================
if role == "Vice Dean / Dean":
    st.title("Global Overview of Exam Planning")

    scheduled = examens[examens["prof"] != "Not scheduled"]

    if scheduled.empty:
        st.warning("No exams scheduled.")
    else:
        # ---------- Room usage ----------
        st.subheader("Room usage per day")
        room_usage = scheduled.groupby(["date_exam", "salle"]).size().reset_index(name="count")
        pivot = room_usage.pivot(index="date_exam", columns="salle", values="count").fillna(0)
        st.bar_chart(pivot)

        # ---------- Exams per department ----------
        st.subheader("Exam distribution by department")
        dept_count = scheduled.groupby("departement").size().reset_index(name="Number of exams")
        st.bar_chart(dept_count.set_index("departement"))

        # ---------- Exams per formation ----------
        st.subheader("Exam load per formation")
        formation_stats = scheduled.groupby(["departement", "formation"]).size().reset_index(name="Number of exams")
        st.dataframe(formation_stats, use_container_width=True)

        # ---------- Key indicators ----------
        st.subheader("Key indicators")
        total_exams = len(examens)
        scheduled_exams = len(scheduled)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total exams", total_exams)
        col2.metric("Scheduled exams", scheduled_exams)
        col3.metric("Completion rate", f"{(scheduled_exams / total_exams) * 100:.1f}%")
        col4.metric("Rooms used", scheduled["salle"].nunique())

        if st.button("Validate timetable"):
            st.success("Timetable validated successfully.")

# ===============================
# Exam Administrator
# ===============================
elif role == "Exam Administrator":
    st.title("Exam Administration")

    st.subheader("All exams")
    st.dataframe(examens, use_container_width=True)

    if st.button("Generate timetable"):
        subprocess.run(["python", "generate_timetable.py"])
        st.success("Timetable generated. Refresh the page.")

    if st.button("Export to CSV"):
        examens.to_csv("exam_planning_export.csv", index=False)
        st.success("File exported successfully.")

# ===============================
# Department Head
# ===============================
elif role == "Department Head":
    st.title("Department View")
    dept = st.selectbox("Select department", examens["departement"].dropna().unique())
    dept_data = examens[examens["departement"] == dept]
    formation = st.selectbox("Select formation", dept_data["formation"].dropna().unique())
    data = dept_data[dept_data["formation"] == formation]
    st.dataframe(data, use_container_width=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total exams", len(data))
    col2.metric("Groups", data["groupe"].nunique())
    col3.metric("Professors", data["prof"].nunique())

# ===============================
# Student / Professor
# ===============================
else:
    st.title("Personal Exam Schedule")
    user_type = st.radio("I am a", ["Student", "Professor"])
    if user_type == "Professor":
        prof = st.selectbox("Choose your name", examens[examens["prof"] != "Not scheduled"]["prof"].unique())
        st.dataframe(examens[examens["prof"] == prof].sort_values("date_exam"), use_container_width=True)
    else:
        group = st.selectbox("Choose your group", examens["groupe"].unique())
        st.dataframe(examens[examens["groupe"] == group].sort_values("date_exam"), use_container_width=True)
