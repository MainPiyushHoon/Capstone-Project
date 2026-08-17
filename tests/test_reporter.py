from pathlib import Path
import pandas as pd
from app.reporting.reporter import generate_all_reports

def test_report_generation(tmp_path):
    cleaned_df = pd.DataFrame([{"employee_id": "EMP1", "name": "Alice", "department": "HR", "salary": 50000}])
    dept_summary = pd.DataFrame([{"department": "HR", "employee_count": 1, "average_salary": 50000.0}])
    errors_df = pd.DataFrame([{"row_index": 2, "error_reason": "Missing email"}])
    metrics = {
        "total_processed": 2, "valid_count": 1, "error_count": 1,
        "active_count": 1, "inactive_count": 0, "avg_salary": 50000.0,
        "new_joiners_count": 1
    }
    
    outputs = generate_all_reports(cleaned_df, dept_summary, errors_df, metrics, tmp_path)
    assert outputs["cleaned_excel"].exists()
    assert outputs["dept_summary_excel"].exists()
    assert outputs["errors_csv"].exists()
    assert outputs["summary_txt"].exists()
