# System Design: Employee Data Automation & Reporting System

Date: 2026-08-17  
Status: Approved  

## 1. Executive Summary
The Employee Data Automation & Reporting System is a modular Python solution designed to process HR employee data from CSV and Excel files. The application validates records against business rules, standardizes clean data, calculates key business/HR metrics, exports structured reports (Excel, CSV, plain text), and records execution activity in processing logs.

Per constraints, this implementation focuses exclusively on core pipeline reliability, clean architecture, exception resilience, logging, and unit testing without over-engineering or unnecessary external services.

---

## 2. System Architecture & Components

```
Capstone Project/
├── app/
│   ├── __init__.py
│   ├── main.py             # CLI entrypoint (argparse)
│   ├── config.py           # Application settings, paths, & validation constants
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── reader.py       # File reading (.csv, .xlsx, .xls)
│   ├── validation/
│   │   ├── __init__.py
│   │   └── validator.py    # Schema & row-level validation logic
│   ├── processing/
│   │   ├── __init__.py
│   │   └── cleaner.py      # String trimming, date parsing, salary normalization
│   ├── analytics/
│   │   ├── __init__.py
│   │   └── metrics.py      # HR summary statistics calculation
│   ├── reporting/
│   │   ├── __init__.py
│   │   └── reporter.py     # Output generation (xlsx, csv, summary report txt)
│   └── utils/
│       ├── __init__.py
│       └── logger.py       # Python standard logging configuration
├── data/
│   ├── input/              # Input directory for CSV/Excel employee datasets
│   └── output/             # Output destination for reports & logs
├── tests/
│   ├── __init__.py
│   ├── test_ingestion.py
│   ├── test_validation.py
│   ├── test_cleaner.py
│   ├── test_metrics.py
│   └── test_reporter.py
├── requirements.txt
├── README.md
└── PROJECT.md
```

---

## 3. Detailed Component Specifications

### 3.1 Configuration (`app/config.py`)
- Defines default input/output directories (`data/input`, `data/output`).
- Required columns: `employee_id`, `name`, `department`, `salary`, `joining_date`, `email`, `status`.
- Email regex pattern validation rule.
- Default log file path: `data/output/processing_log.txt`.

### 3.2 Ingestion (`app/ingestion/reader.py`)
- Function: `read_employee_file(file_path: Path) -> pd.DataFrame`
- Uses `pandas.read_csv()` for CSV files and `pandas.read_excel()` with `openpyxl` engine for Excel spreadsheets.
- Handles `FileNotFoundError` and unsupported format extensions.

### 3.3 Validation (`app/validation/validator.py`)
- Function: `validate_employee_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]`
- Returns a tuple of `(valid_df, errors_df)`.
- **File-Level Validation**:
  - Validates presence of all required columns (`employee_id`, `name`, `department`, `salary`, `email`).
- **Record-Level Validation Rules**:
  1. `employee_id`: Must be non-empty and unique across the dataset (identifies duplicates).
  2. `email`: Must be non-empty and conform to standard email regex syntax (`^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$`).
  3. `salary`: Must be parsable as a non-negative float (> 0).
  4. `joining_date`: Must be a valid date string/timestamp not in the far future.
  5. `status`: Standardized values (e.g. Active, Inactive, On Leave).
- Non-valid rows are appended to `errors_df` along with specific failure reasons (`error_reason`).

### 3.4 Data Cleaning & Transformation (`app/processing/cleaner.py`)
- Function: `clean_employee_data(valid_df: pd.DataFrame) -> pd.DataFrame`
- Strips leading/trailing whitespace from string fields (`name`, `department`, `status`, `email`).
- Normalizes `department` values to Title Case (e.g., `"engineering "` -> `"Engineering"`).
- Normalizes `name` values to Title Case.
- Converts `salary` to rounded float representation (2 decimal places).
- Converts `joining_date` to `YYYY-MM-DD` ISO format.

### 3.5 Business Analytics (`app/analytics/metrics.py`)
- Function: `calculate_hr_metrics(df: pd.DataFrame, errors_df: pd.DataFrame) -> Dict[str, Any]`
- Computes:
  - Total records processed, valid record count, error record count.
  - Department headcount breakdown.
  - Department average salary breakdown.
  - Total active vs. inactive employees.
  - New joiners count (joining date within the current calendar year or past 365 days).
  - Overall average company salary.

### 3.6 Reporting (`app/reporting/reporter.py`)
- Function: `generate_all_reports(cleaned_df: pd.DataFrame, dept_summary_df: pd.DataFrame, errors_df: pd.DataFrame, metrics: Dict[str, Any], output_dir: Path)`
- Generates:
  1. `cleaned_employees.xlsx`: Cleaned & validated employee records.
  2. `department_summary.xlsx`: Department headcount and average salary statistics.
  3. `validation_errors.csv`: Failed records with row index and error explanations.
  4. `summary_report.txt`: Human-readable executive summary of HR metrics & processing run statistics.

### 3.7 Logging & CLI (`app/utils/logger.py` & `app/main.py`)
- Sets up Python's `logging` module to output to both console and `processing_log.txt`.
- Logs counts of processed, valid, and rejected records.
- Command-line arguments:
  - `--input` / `-i`: Input CSV or Excel file path.
  - `--output` / `-o`: Output directory for reports and logs.
  - `--verbose` / `-v`: Enable DEBUG logging level.

---

## 4. Verification & Testing Strategy
- Unit test suite in `tests/` using standard `pytest` or `unittest`:
  - Test valid vs invalid email syntax.
  - Test salary coercion and invalid value flagging.
  - Test duplicate `employee_id` detection.
  - Test department normalization (`" hr "` -> `"Hr"` / `"HR"`).
  - Test metric calculation math correctness.
  - Test full pipeline run using sample CSV/Excel input files.

---

## 5. Definition of Done
1. All core modular files implemented with clean Python typing and docstrings.
2. Sample data (`data/input/sample_employees.csv` & `data/input/sample_employees.xlsx`) provided.
3. Automated execution completes without errors and produces all 5 required output artifacts.
4. Comprehensive test suite passes cleanly.
5. Clear `README.md` documentation explaining setup, execution, and project structure.
