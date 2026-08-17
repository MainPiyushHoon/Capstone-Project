from pathlib import Path

class Config:
    """Application configuration and default settings."""
    BASE_DIR = Path(__file__).resolve().parent.parent
    INPUT_DIR = BASE_DIR / "data" / "input"
    OUTPUT_DIR = BASE_DIR / "data" / "output"
    
    REQUIRED_COLUMNS = [
        "employee_id",
        "name",
        "department",
        "salary",
        "joining_date",
        "email",
        "status"
    ]
    
    CLEANED_EMPLOYEES_FILENAME = "cleaned_employees.xlsx"
    DEPT_SUMMARY_FILENAME = "department_summary.xlsx"
    VALIDATION_ERRORS_FILENAME = "validation_errors.csv"
    SUMMARY_REPORT_FILENAME = "summary_report.txt"
    PROCESSING_LOG_FILENAME = "processing_log.txt"
    
    EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
