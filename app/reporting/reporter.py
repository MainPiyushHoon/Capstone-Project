from pathlib import Path
from typing import Dict, Any
import pandas as pd
from app.config import Config

def generate_all_reports(
    cleaned_df: pd.DataFrame,
    dept_summary_df: pd.DataFrame,
    errors_df: pd.DataFrame,
    metrics: Dict[str, Any],
    output_dir: Path
) -> Dict[str, Path]:
    """Generates all 4 primary output files:
    1. cleaned_employees.xlsx
    2. department_summary.xlsx
    3. validation_errors.csv
    4. summary_report.txt
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cleaned_excel = output_dir / Config.CLEANED_EMPLOYEES_FILENAME
    cleaned_df.to_excel(cleaned_excel, index=False, engine="openpyxl")
    
    dept_summary_excel = output_dir / Config.DEPT_SUMMARY_FILENAME
    dept_summary_df.to_excel(dept_summary_excel, index=False, engine="openpyxl")
    
    errors_csv = output_dir / Config.VALIDATION_ERRORS_FILENAME
    errors_df.to_csv(errors_csv, index=False)
    
    summary_txt = output_dir / Config.SUMMARY_REPORT_FILENAME
    with open(summary_txt, "w", encoding="utf-8") as f:
        f.write("==================================================\n")
        f.write("       EMPLOYEE DATA PROCESSING SUMMARY REPORT    \n")
        f.write("==================================================\n\n")
        f.write(f"Total Employee Records Processed: {metrics['total_processed']}\n")
        f.write(f"Successfully Validated & Cleaned: {metrics['valid_count']}\n")
        f.write(f"Failed Validation (Error Rows) : {metrics['error_count']}\n\n")
        f.write("--------------------------------------------------\n")
        f.write("                 KEY HR METRICS                   \n")
        f.write("--------------------------------------------------\n")
        f.write(f"Active Employees Count          : {metrics['active_count']}\n")
        f.write(f"Inactive / On-Leave Count       : {metrics['inactive_count']}\n")
        f.write(f"Overall Average Salary          : ${metrics['avg_salary']:,.2f}\n")
        f.write(f"New Joiners (Current Year)      : {metrics['new_joiners_count']}\n\n")
        f.write("--------------------------------------------------\n")
        f.write("            DEPARTMENT BREAKDOWN                  \n")
        f.write("--------------------------------------------------\n")
        f.write(dept_summary_df.to_string(index=False))
        f.write("\n==================================================\n")
        
    return {
        "cleaned_excel": cleaned_excel,
        "dept_summary_excel": dept_summary_excel,
        "errors_csv": errors_csv,
        "summary_txt": summary_txt
    }
