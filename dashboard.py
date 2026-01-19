import streamlit as st
import pandas as pd
import subprocess

st.set_page_config(page_title="Exam Planning Dashboard", layout="wide")

# ===============================
# Load data
# ===============================
examens = pd.read_csv("planning_examens_dashboard.csv")
examens["date_exam"] = pd.to_datetime(examens["date_exam"], errors="coerce")

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
        st.subheader("Room usage per day")

        room_usage = (
            scheduled
            .groupby(["date_exam", "salle"])
            .size()
            .reset_index(name="count")
        )

        pivot = room_usage.pivot(
            index="date_exam",
            columns="salle",
            values="count"
        ).fillna(0)

        st.bar_chart(pivot)

        st.subheader("Conflicts by department")

        def detect_conflicts(df):
            return pd.Series({
                "Group conflicts": df.duplicated(
                    subset=["groupe", "date_exam"]
                ).sum(),
                "Professor conflicts": df.duplicated(
                    subset=["prof", "date_exam"]
                ).sum()
            })

        conflicts = scheduled.groupby("departement").apply(detect_conflicts)
        st.dataframe(conflicts)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total exams", len(scheduled))
        col2.metric("Professors involved", scheduled["prof"].nunique())
        col3.metric("Groups involved", scheduled["groupe"].nunique())

        if st.button("Validate timetable"):
            st.success("Timetable validated successfully.")

# ===============================
# Exam Administrator
# ===============================
elif role == "Exam Administrator":
    st.title("Exam Administration")

    st.subheader("All exams")
    st.dataframe(examens)

    if st.button("Generate timetable"):
        subprocess.run(["python", "generate_timetable.py"])
        st.success("Timetable generated. Refresh the page.")

    if st.button("Detect conflicts"):
        scheduled = examens[examens["prof"] != "Not scheduled"]

        st.write(
            "Student conflicts:",
            scheduled.duplicated(subset=["groupe", "date_exam"]).sum()
        )
        st.write(
            "Professor conflicts:",
            scheduled.duplicated(subset=["prof", "date_exam"]).sum()
        )

    if st.button("Export to CSV"):
        examens.to_csv("exam_planning.csv", index=False)
        st.success("File exported.")

# ===============================
# Department Head
# ===============================
elif role == "Department Head":
    st.title("Department View")

    dept = st.selectbox(
        "Select department",
        examens["departement"].dropna().unique()
    )

    dept_data = examens[examens["departement"] == dept]

    formation = st.selectbox(
        "Select formation",
        dept_data["formation"].dropna().unique()
    )

    data = dept_data[dept_data["formation"] == formation]

    st.dataframe(data)

    st.metric("Total exams", len(data))
    st.metric("Groups", data["groupe"].nunique())
    st.metric("Professors", data["prof"].nunique())

# ===============================
# Student / Professor
# ===============================
else:
    st.title("Personal Exam Schedule")

    user_type = st.radio("I am a", ["Student", "Professor"])

    if user_type == "Professor":
        prof = st.selectbox(
            "Choose your name",
            examens[examens["prof"] != "Not scheduled"]["prof"].unique()
        )
        st.dataframe(
            examens[examens["prof"] == prof].sort_values("date_exam")
        )
    else:
        group = st.selectbox(
            "Choose your group",
            examens["groupe"].unique()
        )
        st.dataframe(
            examens[examens["groupe"] == group].sort_values("date_exam")
        )
