# helper.py
import pandas as pd

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names and try to detect name/gender/score columns."""
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    # Try to rename common columns to known names
    # If dataset has no name column, create one
    if "name" not in df.columns:
        possible_name_cols = [c for c in df.columns if "student" in c or "name" in c]
        if possible_name_cols:
            df = df.rename(columns={possible_name_cols[0]: "name"})
        else:
            # create an index-based name column
            df.insert(0, "name", [f"Student_{i+1}" for i in range(len(df))])
    return df

def compute_scores(df: pd.DataFrame, subject_cols=None, max_marks_per_subject=100, name_col="name") -> pd.DataFrame:
    """Compute total, average, percentage and grade for given subject columns."""
    df = df.copy()
    # If subject_cols not provided, try to detect
    if subject_cols is None:
        # Simple heuristic: any column with 'score' or numeric types except name/gender
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        subject_cols = [c for c in numeric_cols if c != 'total' and c != 'average' and c != 'percentage']
        if not subject_cols:
            raise ValueError("No numeric subject columns detected. Provide subject_cols.")
    # Fill missing numeric values with column mean
    df[subject_cols] = df[subject_cols].fillna(df[subject_cols].mean())

    df['total'] = df[subject_cols].sum(axis=1)
    df['average'] = df['total'] / len(subject_cols)
    df['percentage'] = (df['total'] / (max_marks_per_subject * len(subject_cols))) * 100

    df['grade'] = df['percentage'].apply(assign_grade)
    return df

def assign_grade(pct):
    if pct >= 90:
        return "A+"
    elif pct >= 80:
        return "A"
    elif pct >= 70:
        return "B"
    elif pct >= 60:
        return "C"
    else:
        return "F"
