# Employee Data Automation & Reporting System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a robust, modular Python Employee Data Automation & Reporting System that ingests CSV/Excel datasets, validates rules, cleans fields, computes HR metrics, exports Excel/CSV/text reports, logs activity, and handles errors gracefully.

**Architecture:** A clean modular Python package (`app/`) structured by domain responsibilities (`ingestion`, `validation`, `processing`, `analytics`, `reporting`, `utils`), supported by CLI (`app/main.py`), data directories (`data/input`, `data/output`), and comprehensive unit tests (`tests/`).

**Tech Stack:** Python 3.10+, Pandas, openpyxl, pathlib, logging, datetime, pytest.

## Global Constraints

- No unnecessary external frameworks (no Streamlit, FastAPI, Docker, SQLite).
- Strict validation reporting: invalid rows must be recorded in `validation_errors.csv` and logged without stopping processing.
- Clean separation of original data vs cleaned output: source files are preserved read-only.
- All code modules must include type hints and docstrings.

---

### Task 1: Project Setup & Dependency Configuration

**Files:**
- Create: `requirements.txt`
- Create: `app/__init__.py`
- Create: `app/config.py`
- Create: `app/utils/__init__.py`
- Create: `app/utils/logger.py`
- Test: `tests/test_config.py`

**Interfaces:**
- Consumes: None
- Produces: `app.config.Config`, `app.utils.logger.setup_logger(log_file: Path, verbose: bool)`

- [ ] **Step 1: Write failing test for config and logger setup**

```python
# tests/test_config.py
from pathlib import Path
from app.config import Config
from app.utils.logger import setup_logger

def test_config_defaults():
    assert isinstance(Config.INPUT_DIR, Path)
    assert isinstance(Config.OUTPUT_DIR, Path)
    assert "employee_id" in Config.REQUIRED_COLUMNS

def test_logger_setup(tmp_path):
    log_file = tmp_path / "test.log"
    logger = setup_logger(log_file=log_file, verbose=True)
    logger.info("Test message")
    assert log_file.exists()
    assert "Test message" in log_file.read_text()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_config.py -v`  
Expected: FAIL with ModuleNotFoundError.

- [ ] **Step 3: Create dependencies file, package init, config and logger implementation**

```text
# requirements.txt
pandas>=2.0.0
openpyxl>=3.1.0
pytest>=7.0.0
```

```python
# app/config.py
from pathlib import Path

class Config:
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
```

```python
# app/utils/logger.py
import logging
import sys
from pathlib import Path

def setup_logger(log_file: Path | None = None, verbose: bool = False) -> logging.Logger:
    logger = logging.getLogger("EmployeeAutomation")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.handlers.clear()
    
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_config.py -v`  
Expected: PASS.

---

### Task 2: Data Ingestion Module

**Files:**
- Create: `app/ingestion/__init__.py`
- Create: `app/ingestion/reader.py`
- Test: `tests/test_reader.py`

**Interfaces:**
- Consumes: File path (`Path` object)
- Produces: `app.ingestion.reader.read_employee_file(file_path: Path) -> pd.DataFrame`

- [ ] **Step 1: Write test for reading CSV and Excel files**

```python
# tests/test_reader.py
import pandas as pd
import pytest
from pathlib import Path
from app.ingestion.reader import read_employee_file

def test_read_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    df_orig = pd.DataFrame({"employee_id": ["EMP01"], "name": ["Alice"]})
    df_orig.to_csv(csv_file, index=False)
    
    df_loaded = read_employee_file(csv_file)
    assert len(df_loaded) == 1
    assert df_loaded.iloc[0]["employee_id"] == "EMP01"

def test_read_missing_file():
    with pytest.raises(FileNotFoundError):
        read_employee_file(Path("non_existent_file.csv"))

def test_read_unsupported_format(tmp_path):
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("hello")
    with pytest.raises(ValueError, match="Unsupported file format"):
        read_employee_file(txt_file)
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/test_reader.py -v`  
Expected: FAIL.

- [ ] **Step 3: Implement data reader**

```python
# app/ingestion/reader.py
from pathlib import Path
import pandas as pd

def read_employee_file(file_path: Path) -> pd.DataFrame:
    """Reads employee dataset from CSV or Excel file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found at: {path}")
        
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, dtype=str)
    elif suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path, dtype=str)
    else:
        raise ValueError(f"Unsupported file format '{suffix}'. Supported formats: .csv, .xlsx, .xls")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_reader.py -v`  
Expected: PASS.

---

### Task 3: Data Validation Module

**Files:**
- Create: `app/validation/__init__.py`
- Create: `app/validation/validator.py`
- Test: `tests/test_validator.py`

**Interfaces:**
- Consumes: Raw `pd.DataFrame` read from file
- Produces: `validate_employee_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]`

- [ ] **Step 1: Write validation unit tests**

```python
# tests/test_validator.py
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
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/test_validator.py -v`  
Expected: FAIL.

- [ ] **Step 3: Implement validation logic**

```python
# app/validation/validator.py
import re
from typing import Tuple
import pandas as pd
from app.config import Config

def validate_file_columns(df: pd.DataFrame) -> None:
    missing = [col for col in Config.REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(missing)}")

def validate_employee_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    validate_file_columns(df)
    
    valid_rows = []
    error_rows = []
    seen_emp_ids = set()
    
    email_pattern = re.compile(Config.EMAIL_REGEX)
    
    for idx, row in df.iterrows():
        reasons = []
        emp_id = str(row.get("employee_id", "")).strip()
        email = str(row.get("email", "")).strip()
        salary_str = str(row.get("salary", "")).strip()
        joining_date_str = str(row.get("joining_date", "")).strip()
        
        if not emp_id or emp_id.lower() == "nan":
            reasons.append("Missing employee_id")
        elif emp_id in seen_emp_ids:
            reasons.append(f"Duplicate employee_id '{emp_id}'")
        
        if not email or not email_pattern.match(email):
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
            err_record["row_index"] = idx + 2
            err_record["error_reason"] = "; ".join(reasons)
            error_rows.append(err_record)
        else:
            seen_emp_ids.add(emp_id)
            valid_rows.append(row.to_dict())
            
    valid_df = pd.DataFrame(valid_rows) if valid_rows else pd.DataFrame(columns=df.columns)
    errors_df = pd.DataFrame(error_rows) if error_rows else pd.DataFrame(columns=list(df.columns) + ["row_index", "error_reason"])
    
    return valid_df, errors_df
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_validator.py -v`  
Expected: PASS.

---

### Task 4: Data Cleaning & HR Metrics Modules

**Files:**
- Create: `app/processing/__init__.py`
- Create: `app/processing/cleaner.py`
- Create: `app/analytics/__init__.py`
- Create: `app/analytics/metrics.py`
- Test: `tests/test_cleaner.py`
- Test: `tests/test_metrics.py`

**Interfaces:**
- Consumes: `valid_df`
- Produces: `clean_employee_data(df: pd.DataFrame) -> pd.DataFrame`, `calculate_hr_metrics(df: pd.DataFrame, errors_df: pd.DataFrame) -> Dict[str, Any]`

- [ ] **Step 1: Write cleaner and metrics tests**

```python
# tests/test_cleaner.py
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
```

```python
# tests/test_metrics.py
import pandas as pd
from app.analytics.metrics import calculate_hr_metrics

def test_hr_metrics_calculation():
    df = pd.DataFrame({
        "employee_id": ["EMP1", "EMP2"],
        "department": ["Engineering", "HR"],
        "salary": [100000, 60000],
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
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/test_cleaner.py tests/test_metrics.py -v`  
Expected: FAIL.

- [ ] **Step 3: Implement cleaner and metrics modules**

```python
# app/processing/cleaner.py
import pandas as pd

def clean_employee_data(valid_df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes string formatting, numerical fields, and dates."""
    if valid_df.empty:
        return valid_df.copy()
        
    df = valid_df.copy()
    
    for col in ["employee_id", "name", "department", "email", "status"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    df["name"] = df["name"].str.title()
    df["department"] = df["department"].str.title()
    df["status"] = df["status"].str.title()
    
    df["salary"] = pd.to_numeric(df["salary"]).round(2)
    df["joining_date"] = pd.to_datetime(df["joining_date"]).dt.strftime("%Y-%m-%d")
    
    return df
```

```python
# app/analytics/metrics.py
from typing import Dict, Any
import pandas as pd
from datetime import datetime

def calculate_hr_metrics(cleaned_df: pd.DataFrame, errors_df: pd.DataFrame) -> Dict[str, Any]:
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_cleaner.py tests/test_metrics.py -v`  
Expected: PASS.

---

### Task 5: Reporting & Main CLI Application

**Files:**
- Create: `app/reporting/__init__.py`
- Create: `app/reporting/reporter.py`
- Create: `app/main.py`
- Create: `data/input/sample_employees.csv`
- Test: `tests/test_reporter.py`
- Test: `tests/test_integration.py`

**Interfaces:**
- Consumes: Cleaned DataFrame, Department Summary, Errors DataFrame, Metrics Dict, Output Path
- Produces: `generate_all_reports()`, `main()` entrypoint.

- [ ] **Step 1: Write test for reporting & CLI execution**

```python
# tests/test_reporter.py
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
```

- [ ] **Step 2: Run test to verify failure**

Run: `pytest tests/test_reporter.py -v`  
Expected: FAIL.

- [ ] **Step 3: Implement reporter, CLI main script, and sample dataset**

```python
# app/reporting/reporter.py
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
```

```python
# app/main.py
import argparse
import sys
from pathlib import Path

from app.config import Config
from app.ingestion.reader import read_employee_file
from app.validation.validator import validate_employee_data
from app.processing.cleaner import clean_employee_data
from app.analytics.metrics import calculate_hr_metrics
from app.reporting.reporter import generate_all_reports
from app.utils.logger import setup_logger

def run_pipeline(input_file: Path, output_dir: Path, verbose: bool = False) -> None:
    log_file = output_dir / Config.PROCESSING_LOG_FILENAME
    logger = setup_logger(log_file=log_file, verbose=verbose)
    
    logger.info("==========================================")
    logger.info("Starting Employee Data Automation Pipeline")
    logger.info(f"Input File : {input_file}")
    logger.info(f"Output Dir : {output_dir}")
    logger.info("==========================================")
    
    try:
        logger.info("Step 1: Reading input dataset...")
        raw_df = read_employee_file(input_file)
        logger.info(f"Successfully loaded {len(raw_df)} total raw records.")
        
        logger.info("Step 2: Validating employee records...")
        valid_df, errors_df = validate_employee_data(raw_df)
        logger.info(f"Validation finished. Valid: {len(valid_df)}, Invalid: {len(errors_df)}")
        
        logger.info("Step 3: Cleaning and standardizing valid data...")
        cleaned_df = clean_employee_data(valid_df)
        
        logger.info("Step 4: Calculating business HR metrics...")
        metrics = calculate_hr_metrics(cleaned_df, errors_df)
        
        logger.info("Step 5: Exporting reports and output files...")
        report_paths = generate_all_reports(
            cleaned_df=cleaned_df,
            dept_summary_df=metrics["dept_summary"],
            errors_df=errors_df,
            metrics=metrics,
            output_dir=output_dir
        )
        
        for name, path in report_paths.items():
            logger.info(f"Generated report '{name}': {path}")
            
        logger.info("Pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline processing failed: {e}", exc_info=verbose)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Employee Data Automation & Reporting System")
    parser.add_argument("--input", "-i", type=str, default=str(Config.INPUT_DIR / "sample_employees.csv"), help="Path to input CSV or Excel file")
    parser.add_argument("--output", "-o", type=str, default=str(Config.OUTPUT_DIR), help="Output directory for reports and logs")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose debug logging")
    
    args = parser.parse_args()
    run_pipeline(Path(args.input), Path(args.output), args.verbose)

if __name__ == "__main__":
    main()
```

Sample input dataset `data/input/sample_employees.csv`:
```csv
employee_id,name,department,salary,joining_date,email,status
EMP1001,Rahul Sharma,Engineering ,85000,2024-06-15,rahul@example.com,Active
EMP1002,Priya Patel, HR ,62000,2023-03-10,priya@example.com,Active
EMP1003, Amit Verma ,Finance,71000,2024-01-20,amit@example.com,Active
EMP1004,Neha Gupta,engineering,90000,2022-11-05,neha@example.com,Active
EMP1005,,Marketing,55000,2024-04-12,bad_email,Active
EMP1001,Duplicate User,Sales,40000,2024-02-01,dup@example.com,Active
EMP1006,Suresh Kumar,Sales,-5000,2024-05-18,suresh@example.com,Inactive
```

- [ ] **Step 4: Run pytest and run CLI main pipeline**

Run: `pytest -v`  
Expected: PASS all tests.

---

### Task 6: Documentation and Final Verification

**Files:**
- Create: `README.md`
- Verify: Full pipeline execution and report output generation

**Interfaces:**
- End-to-end user verification and installation guide.

- [ ] **Step 1: Write README.md**

```markdown
# Employee Data Automation & Reporting System

A Python automation system that processes employee data from CSV/Excel files, validates rules, cleans and standardizes fields, computes business HR metrics, and generates formatted reports.

## Features
- **CSV & Excel Support**: Ingest `.csv`, `.xlsx`, `.xls` spreadsheets effortlessly.
- **Validation Engine**: File-level column checks and row-level checks for missing IDs, duplicate records, malformed emails, negative salaries, and invalid dates.
- **Data Cleaning**: Trims whitespace, standardizes names and department casing, formats dates to ISO standard, and rounds salary fields.
- **Business Metrics**: Department headcount, department average salary, total active/inactive counts, new joiners, and error statistics.
- **Multi-Format Exports**: Outputs clean dataset Excel, department summary Excel, validation errors CSV, and summary report TXT.
- **Logging**: Dual console and file logging with detailed audit trails.

## Project Structure
```text
Capstone Project/
├── app/
│   ├── ingestion/       # CSV/Excel reader
│   ├── validation/      # Data validator
│   ├── processing/      # Cleaning & formatting
│   ├── analytics/       # HR metrics
│   ├── reporting/       # Output report generator
│   └── utils/          # Logging helper
├── data/
│   ├── input/           # Input files directory
│   └── output/          # Report & log outputs directory
├── tests/               # Pytest suite
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Automation Pipeline
```bash
python -m app.main --input data/input/sample_employees.csv --output data/output
```

### 3. Run Test Suite
```bash
pytest -v
```
```

- [ ] **Step 2: Execute full pipeline end-to-end and confirm all output files exist**

Run: `python -m app.main --input data/input/sample_employees.csv --output data/output`  
Expected: Pipeline finishes with log messages and outputs:
- `data/output/cleaned_employees.xlsx`
- `data/output/department_summary.xlsx`
- `data/output/validation_errors.csv`
- `data/output/summary_report.txt`
- `data/output/processing_log.txt`
