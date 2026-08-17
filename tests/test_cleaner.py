import pandas as pd
from app.processing.cleaner import clean_employee_data

def test_cleaning_transformation():
    df = pd.DataFrame({
        "employee_id": ["EMP1001"],
        "name": [" rahul  sharma "],
        "department": [" engineering "],
        "salary": ["85000.50"],
        "joining_date": ["2024-06-15 00:00:00"],
        "email": ["rahul@example.com"],
        "status": [" active "]
    })
    cleaned = clean_employee_data(df)
    assert cleaned.iloc[0]["name"] == "Rahul Sharma"
    assert cleaned.iloc[0]["department"] == "Engineering"
    assert cleaned.iloc[0]["salary"] == 85000.50
    assert cleaned.iloc[0]["joining_date"] == "2024-06-15"
    assert cleaned.iloc[0]["status"] == "Active"
