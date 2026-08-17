# Employee Data Automation & Reporting System

A modular Python automation system that reads employee data from CSV and Excel spreadsheets, validates records against business rules, standardizes clean data, calculates key business/HR metrics, and generates formatted report outputs.

---

## 🌟 Key Features

- **CSV & Excel Spreadsheet Support**: Ingest `.csv`, `.xlsx`, and `.xls` files cleanly using `pandas` and `openpyxl`.
- **Validation Engine**:
  - File-level verification of mandatory columns (`employee_id`, `name`, `department`, `salary`, `joining_date`, `email`, `status`).
  - Row-level validation checking for missing IDs, duplicate IDs, invalid email syntax, negative/non-numeric salaries, and invalid dates.
- **Data Cleaning & Standardization**:
  - Trims whitespace and collapses redundant internal spaces.
  - Normalizes employee names and department names to Title Case.
  - Coerces dates to `YYYY-MM-DD` ISO format and rounds salaries to 2 decimal places.
- **Business HR Metrics**:
  - Computes department headcount and average salary.
  - Tracks total active/inactive counts, new joiners, and validation error rates.
- **Multi-Format Report Generation**:
  - `cleaned_employees.xlsx`: Validated and standardized dataset.
  - `department_summary.xlsx`: Department headcount and average salary matrix.
  - `validation_errors.csv`: Detailed log of rejected rows with exact line numbers and failure reasons.
  - `summary_report.txt`: Executive text summary of pipeline execution and metrics.
  - `processing_log.txt`: Complete execution audit log with timestamps and severity levels (`INFO`, `WARNING`, `ERROR`).
- **Unit Testing**: Automated unit tests using `pytest` covering configuration, file reading, validation rules, data cleaning, metric formulas, and report outputs.

---

## 📂 Project Structure

```text
Capstone Project/
├── app/
│   ├── __init__.py
│   ├── main.py             # CLI entrypoint
│   ├── config.py           # Configuration settings & paths
│   ├── ingestion/          # CSV & Excel file readers
│   ├── validation/         # Schema & record-level validation rules
│   ├── processing/         # Data cleaning & standardization
│   ├── analytics/          # HR metrics calculation
│   ├── reporting/          # Excel, CSV, and summary report generator
│   └── utils/              # Python logging & exception utilities
├── data/
│   ├── input/              # Sample CSV & Excel input datasets
│   └── output/             # Output destination for generated reports & logs
├── tests/                  # Pytest unit test suite
├── requirements.txt
├── PROJECT.md
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Requirements & Installation
Python 3.10 or higher is required.

Install project dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run the Automation Pipeline

To process the default sample CSV file:
```bash
python -m app.main
```

To process a custom CSV or Excel input file:
```bash
python -m app.main --input data/input/sample_employees.csv --output data/output
```

To process an Excel spreadsheet:
```bash
python -m app.main --input data/input/sample_employees.xlsx --output data/output
```

Options:
- `--input` / `-i`: Path to the input CSV or Excel file.
- `--output` / `-o`: Output directory for generated reports and logs.
- `--verbose` / `-v`: Enable debug level logging output.

### 3. Run Automated Tests

Run the full pytest suite:
```bash
python -m pytest -v
```

---

## 📋 Definition of Done Verification

- [x] CSV & Excel file ingestion
- [x] File schema column validation
- [x] Record-level error detection (missing ID, duplicate ID, invalid email, negative salary, bad date)
- [x] Data cleaning and department normalization
- [x] HR metric calculations (headcount, avg salary, active count, new joiners)
- [x] Output exports (`cleaned_employees.xlsx`, `department_summary.xlsx`, `validation_errors.csv`, `summary_report.txt`, `processing_log.txt`)
- [x] Non-fatal exception resilience and dual console/file logging
- [x] 100% passing test suite
