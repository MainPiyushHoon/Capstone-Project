import pandas as pd

def clean_employee_data(valid_df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes string formatting, department casing, numerical values, and dates."""
    if valid_df.empty:
        return valid_df.copy()
        
    df = valid_df.copy()
    
    for col in ["employee_id", "name", "department", "email", "status"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
            
    df["name"] = df["name"].str.title()
    df["department"] = df["department"].str.title()
    df["status"] = df["status"].str.title()
    
    df["salary"] = pd.to_numeric(df["salary"]).round(2)
    df["joining_date"] = pd.to_datetime(df["joining_date"]).dt.strftime("%Y-%m-%d")
    
    return df
