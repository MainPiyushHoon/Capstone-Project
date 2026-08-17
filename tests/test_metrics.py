import pandas as pd
from app.analytics.metrics import calculate_hr_metrics

def test_hr_metrics_calculation():
    df = pd.DataFrame({
        "employee_id": ["EMP1", "EMP2"],
        "department": ["Engineering", "HR"],
        "salary": [100000.0, 60000.0],
        "status": ["Active", "Active"],
        "joining_date": ["2024-01-01", "2023-01-01"]
    })
    errors_df = pd.DataFrame([{"error_reason": "bad ID"}])
    
    metrics = calculate_hr_metrics(df, errors_df)
    assert metrics["total_processed"] == 3
    assert metrics["valid_count"] == 2
    assert metrics["error_count"] == 1
    assert metrics["active_count"] == 2
    assert metrics["avg_salary"] == 80000.0
