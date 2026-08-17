import pandas as pd
import pytest
from app.validation.validator import validate_employee_data, validate_file_columns

def test_missing_required_columns():
    df = pd.DataFrame({"employee_id": ["EMP1"], "name": ["John"]})
    with pytest.raises(ValueError, match="Missing required column"):
        validate_file_columns(df)

def test_record_validation():
    data = {
        "employee_id": ["EMP1001", "EMP1001", "", "EMP1002", "EMP1003"],
        "name": ["Alice", "Alice Dup", "Bob", "Charlie", "David"],
        "department": ["Engineering", "Sales", "HR", "Finance", "IT"],
        "salary": ["85000", "70000", "50000", "-100", "invalid_salary"],
        "joining_date": ["2024-06-15", "2024-06-15", "2024-01-01", "2024-05-01", "2024-05-01"],
        "email": ["alice@example.com", "alice@example.com", "bob_email", "charlie@example.com", "david@example.com"],
        "status": ["Active", "Active", "Active", "Active", "Active"]
    }
    df = pd.DataFrame(data)
    valid_df, errors_df = validate_employee_data(df)
    
    assert len(valid_df) == 1
    assert valid_df.iloc[0]["employee_id"] == "EMP1001"
    assert len(errors_df) == 4
    
    # Check error reasons captured
    reasons = " ".join(errors_df["error_reason"].tolist())
    assert "Duplicate employee_id" in reasons
    assert "Missing employee_id" in reasons
    assert "Non-positive salary" in reasons
    assert "Invalid salary" in reasons
