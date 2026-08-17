from typing import Dict, Any
import pandas as pd
from datetime import datetime

def calculate_hr_metrics(cleaned_df: pd.DataFrame, errors_df: pd.DataFrame) -> Dict[str, Any]:
    """Calculates summary HR statistics including headcount, average salary, status counts, and new joiners."""
    valid_count = len(cleaned_df)
    error_count = len(errors_df)
    total_processed = valid_count + error_count
    
    if cleaned_df.empty:
        return {
            "total_processed": total_processed,
            "valid_count": 0,
            "error_count": error_count,
            "active_count": 0,
            "inactive_count": 0,
            "avg_salary": 0.0,
            "dept_summary": pd.DataFrame(columns=["department", "employee_count", "average_salary"]),
            "new_joiners_count": 0
        }
        
    dept_summary = cleaned_df.groupby("department").agg(
        employee_count=("employee_id", "count"),
        average_salary=("salary", "mean")
    ).reset_index()
    dept_summary["average_salary"] = dept_summary["average_salary"].round(2)
    
    active_count = len(cleaned_df[cleaned_df["status"].str.lower() == "active"])
    inactive_count = valid_count - active_count
    avg_salary = round(float(cleaned_df["salary"].mean()), 2)
    
    current_year = str(datetime.now().year)
    new_joiners_count = len(cleaned_df[cleaned_df["joining_date"].str.startswith(current_year)])
    
    return {
        "total_processed": total_processed,
        "valid_count": valid_count,
        "error_count": error_count,
        "active_count": active_count,
        "inactive_count": inactive_count,
        "avg_salary": avg_salary,
        "dept_summary": dept_summary,
        "new_joiners_count": new_joiners_count
    }
