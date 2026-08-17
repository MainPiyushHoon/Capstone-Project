import re
from typing import Tuple
import pandas as pd
from app.config import Config

def validate_file_columns(df: pd.DataFrame) -> None:
    """Verifies that all mandatory columns are present in the DataFrame."""
    missing = [col for col in Config.REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(missing)}")

def validate_employee_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Validates records individually against business rules.
    
    Returns:
        Tuple[valid_df, errors_df]
    """
    validate_file_columns(df)
    
    valid_rows = []
    error_rows = []
    seen_emp_ids = set()
    
    email_pattern = re.compile(Config.EMAIL_REGEX)
    
    for idx, row in df.iterrows():
        reasons = []
        emp_id = str(row.get("employee_id", "") or "").strip()
        email = str(row.get("email", "") or "").strip()
        salary_str = str(row.get("salary", "") or "").strip()
        joining_date_str = str(row.get("joining_date", "") or "").strip()
        
        if not emp_id or emp_id.lower() == "nan":
            reasons.append("Missing employee_id")
        elif emp_id in seen_emp_ids:
            reasons.append(f"Duplicate employee_id '{emp_id}'")
        
        if not email or email.lower() == "nan" or not email_pattern.match(email):
            reasons.append(f"Invalid email address '{email}'")
            
        try:
            salary_val = float(salary_str)
            if salary_val <= 0:
                reasons.append(f"Non-positive salary '{salary_str}'")
        except (ValueError, TypeError):
            reasons.append(f"Invalid salary numeric value '{salary_str}'")
            
        try:
            pd.to_datetime(joining_date_str, errors="raise")
        except Exception:
            reasons.append(f"Invalid joining date '{joining_date_str}'")
            
        if reasons:
            err_record = row.to_dict()
            err_record["row_index"] = idx + 2  # 1-indexed header + row index
            err_record["error_reason"] = "; ".join(reasons)
            error_rows.append(err_record)
        else:
            seen_emp_ids.add(emp_id)
            valid_rows.append(row.to_dict())
            
    valid_df = pd.DataFrame(valid_rows) if valid_rows else pd.DataFrame(columns=df.columns)
    errors_df = pd.DataFrame(error_rows) if error_rows else pd.DataFrame(columns=list(df.columns) + ["row_index", "error_reason"])
    
    return valid_df, errors_df
