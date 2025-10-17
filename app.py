# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from helper import (
    clean_dataframe,
    compute_scores,
    assign_grade
)

st.set_page_config(page_title="Student Grade Analyzer", layout="wide")
st.title("📊 Student Grade Analyzer — Streamlit Dashboard")

st.markdown(
    """
    Upload a CSV file with student scores (or use the sample dataset).
    The CSV should have a column for student name and numeric columns for each subject.
    """
)

# Sidebar options
st.sidebar.header("Options")
use_sample = st.sidebar.checkbox("Use sample dataset", value=True)
uploaded_file = None
if not use_sample:
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

# Load data
if use_sample:
    df = pd.read_csv("sample_data/StudentsPerformance.csv")
else:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.info("Upload a CSV or check 'Use sample dataset' to load an example.")
        st.stop()

# Clean and prepare data
df = clean_dataframe(df)
df = compute_scores(df, subject_cols=["math_score", "reading_score", "writing_score"], max_marks_per_subject=100, name_col="name")

# Show data
st.subheader("Analyzed Data")
st.dataframe(df)

# Summary metrics
st.subheader("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Students", int(df.shape[0]))
col2.metric("Average % (all)", f"{df['percentage'].mean():.2f}%")
col3.metric("Top Score", int(df['total'].max()))

# Sidebar filters
st.sidebar.subheader("Filters")
grade_filter = st.sidebar.multiselect("Filter by Grade", options=sorted(df['grade'].unique()), default=sorted(df['grade'].unique()))

# Gender filter: behave correctly whether 'gender' column exists or not
if "gender" in df.columns:
    gender_options = sorted(df['gender'].dropna().astype(str).unique().tolist())
    gender_filter = st.sidebar.multiselect("Filter by Gender (if present)", options=gender_options, default=gender_options)
else:
    gender_options = ["All"]
    gender_filter = st.sidebar.multiselect("Filter by Gender (if present)", options=gender_options, default=gender_options)

# Apply filters
filtered = df[df['grade'].isin(grade_filter)]
if "gender" in df.columns:
    # If the user didn't leave the gender selection empty, filter by selected genders
    if gender_filter:
        filtered = filtered[filtered['gender'].astype(str).isin(gender_filter)]
# If no 'gender' column exists, we skip gender filtering

# Visualizations (use filtered dataframe)
st.subheader("Visualizations")

# Grade distribution
st.markdown("**Grade Distribution**")
fig1, ax1 = plt.subplots()
filtered['grade'].value_counts().sort_index().plot(kind="bar", ax=ax1)
ax1.set_xlabel("Grade")
ax1.set_ylabel("Number of Students")
ax1.grid(axis='y', linestyle='--', alpha=0.6)
st.pyplot(fig1)

# Scatter: math vs writing
st.markdown("**Math vs Writing Score**")
fig2, ax2 = plt.subplots()
ax2.scatter(filtered['math_score'], filtered['writing_score'], alpha=0.5)
ax2.set_xlabel("Math Score")
ax2.set_ylabel("Writing Score")
ax2.grid(True)
st.pyplot(fig2)


# Download analyzed CSV
st.subheader("Download Results")
csv = filtered.to_csv(index=False)
st.download_button("Download analyzed CSV", data=csv, file_name="analyzed_students.csv", mime="text/csv")

st.success("Analysis complete! You can upload your own CSV or use the sample dataset.")
