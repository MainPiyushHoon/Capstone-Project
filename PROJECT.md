# PROJECT.md --- Employee Data Automation & Reporting System

## 1. Project Overview

Build a Python-based **Employee Data Automation & Reporting System**
that automates the processing of employee data supplied through
CSV/Excel files.

The system must:

1.  Read employee data from CSV/Excel files.
2.  Validate the input data.
3.  Clean and standardize valid records.
4.  Calculate useful HR/business metrics.
5.  Generate cleaned data and summary reports.
6.  Handle errors without stopping the complete processing pipeline.
7.  Maintain processing logs.
8.  Support scheduled/automated execution.
9.  Optionally send notifications when reports are generated or
    important validation errors occur.

The project specification explicitly lists Python, Pandas, openpyxl,
pathlib, logging, datetime, and optional email/API and SQLite usage.

------------------------------------------------------------------------

## 2. Important Scope

This is an **internship capstone project assigned by the organization**.

Do not unnecessarily turn the project into an overly complex enterprise
application.

### Required Core Features

The implementation must cover:

-   CSV/Excel input
-   Required-column validation
-   Employee record validation
-   Data cleaning and standardization
-   HR metric calculation
-   Cleaned output generation
-   Summary report generation
-   Validation-error reporting
-   Exception handling
-   Logging
-   Automated/scheduled execution

### Optional Extensions

These may be implemented if they improve the project without making the
core system unnecessarily complicated:

-   SQLite/PostgreSQL integration
-   FastAPI REST API
-   Excel report formatting with openpyxl
-   Email notifications
-   Docker deployment
-   pytest unit tests
-   Environment-variable configuration
-   Scheduled execution
-   Streamlit dashboard
-   Cloud deployment

Do not implement every extension blindly. Prioritize a stable and
maintainable core system first.

------------------------------------------------------------------------

## 3. Input Data

The system should support employee records containing fields such as:

  Field          Example
  -------------- -------------------
  employee_id    EMP1001
  name           Rahul Sharma
  department     Engineering
  salary         85000
  joining_date   2024-06-15
  email          rahul@example.com
  status         Active

The system should primarily work with CSV and Excel input files.

------------------------------------------------------------------------

## 4. Data Validation Requirements

Validate the following:

### File-Level Validation

-   Input file exists.
-   File format is supported.
-   Required columns exist.

Required columns:

``` text
employee_id
name
department
salary
email
```

### Record-Level Validation

Check for:

-   Missing employee IDs
-   Duplicate employee records
-   Invalid email addresses
-   Invalid/missing dates
-   Invalid salary values
-   Missing required values
-   Invalid employee status where applicable
-   Other obvious malformed employee records

A bad record must **not crash the entire processing operation**.

Invalid records should be captured in a validation-error output with
enough information to identify the problem.

------------------------------------------------------------------------

## 5. Data Cleaning

Clean and standardize valid employee data.

Examples:

-   Strip leading/trailing whitespace.
-   Standardize employee names.
-   Standardize department values.
-   Convert salary values to numeric values.
-   Convert joining dates to proper datetime values.
-   Normalize other inconsistent fields where appropriate.

Example transformation:

``` python
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
df["joining_date"] = pd.to_datetime(df["joining_date"], errors="coerce")
df["department"] = df["department"].str.strip().str.title()
```

Do not silently discard invalid data. Invalid transformations should be
reported through validation/error handling.

------------------------------------------------------------------------

## 6. HR Metrics

Calculate useful metrics, including at minimum:

-   Department-wise employee count
-   Department-wise average salary
-   Active employee count
-   New joiners
-   Other reasonable HR metrics if useful

Example department summary:

``` text
department | employee_count | average_salary
Engineering | 25 | 84500
HR          | 8  | 62000
Finance     | 12 | 71000
```

Keep metric calculations modular so that additional metrics can be added
later.

------------------------------------------------------------------------

## 7. Processing Pipeline

The overall workflow should follow:

``` text
Input CSV/Excel
      ↓
Read Data
      ↓
Validate
      ↓
Clean
      ↓
Transform
      ↓
Calculate Metrics
      ↓
Generate Reports
      ↓
Log Results
      ↓
Send Notification (optional)
```

The implementation should preserve this separation rather than placing
the entire workflow into one large function.

------------------------------------------------------------------------

## 8. Expected Outputs

Generate outputs equivalent to:

``` text
cleaned_employees.xlsx
department_summary.xlsx
processing_log.txt
validation_errors.csv
summary_report.txt
```

### cleaned_employees.xlsx

Contains validated and standardized employee data.

### department_summary.xlsx

Contains department-wise headcount and average salary.

### processing_log.txt

Contains processing history, validation failures, skipped rows,
warnings, and execution errors.

### validation_errors.csv

Contains records or error information for data that failed validation.

### summary_report.txt

Contains high-level HR metrics and processing statistics.

The exact filenames may be changed if a better project structure is
used, but the same outputs/functionality must remain available.

------------------------------------------------------------------------

## 9. Error Handling

Use Python exception handling and validation rules.

Requirements:

-   One malformed employee record must not terminate the entire batch.
-   File-level failures should produce a clear error.
-   Validation errors should be distinguishable from unexpected system
    errors.
-   Errors must be logged.
-   The final processing result should indicate how many records
    succeeded, failed, or were skipped.

Avoid broad silent exception handling such as:

``` python
try:
    ...
except:
    pass
```

Errors must never disappear silently.

------------------------------------------------------------------------

## 10. Logging

Use Python's `logging` module.

Log at appropriate levels:

-   `INFO` --- normal processing
-   `WARNING` --- validation issues/skipped records
-   `ERROR` --- processing failures
-   `DEBUG` --- useful diagnostic information during development

Logs should contain useful context, such as:

-   Processing start/end
-   Input file
-   Number of records read
-   Number of valid records
-   Number of invalid records
-   Generated reports
-   Validation failures
-   Unexpected errors

------------------------------------------------------------------------

## 11. Project Architecture

Prefer a modular structure similar to:

``` text
employee-data-automation/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── reader.py
│   │
│   ├── validation/
│   │   ├── __init__.py
│   │   └── validator.py
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   └── cleaner.py
│   │
│   ├── analytics/
│   │   ├── __init__.py
│   │   └── metrics.py
│   │
│   ├── reporting/
│   │   ├── __init__.py
│   │   └── reporter.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── logger.py
│
├── data/
│   ├── input/
│   └── output/
│
├── tests/
│
├── requirements.txt
├── README.md
├── PROJECT.md
└── .gitignore
```

This is a suggested architecture, not a strict requirement. Simplify it
if the final implementation would otherwise become unnecessarily
fragmented.

------------------------------------------------------------------------

## 12. Technology Requirements

### Required

-   Python
-   Pandas
-   pathlib
-   logging
-   datetime

### Recommended

-   openpyxl

### Optional

-   NumPy
-   SQLite/PostgreSQL
-   FastAPI
-   smtplib or email API
-   pytest
-   Streamlit
-   Docker

Do not add dependencies unless they serve a clear purpose.

------------------------------------------------------------------------

## 13. Configuration

If configuration is needed, avoid hardcoding paths and
environment-specific values throughout the code.

Prefer configuration such as:

``` text
INPUT_DIRECTORY
OUTPUT_DIRECTORY
LOG_DIRECTORY
DATABASE_URL
EMAIL settings
```

Environment variables may be used for secrets and deployment-specific
configuration.

Never commit passwords, API keys, or email credentials to source
control.

------------------------------------------------------------------------

## 14. Optional Database Layer

If a database is implemented, SQLite is sufficient for the initial
version.

Possible data model:

``` text
employees
---------
employee_id
name
department
salary
joining_date
email
status
created_at
updated_at
```

The database should complement the CSV/Excel workflow rather than
unnecessarily replacing the required input/output functionality.

------------------------------------------------------------------------

## 15. Optional FastAPI Layer

If FastAPI is added, expose useful endpoints such as:

``` text
GET  /health
POST /process
GET  /employees
GET  /metrics
GET  /reports
```

Do not add an API merely for the sake of having one. It should provide
meaningful access to the automation system.

------------------------------------------------------------------------

## 16. Optional Streamlit Dashboard

If a dashboard is added, show useful HR information such as:

-   Total employees
-   Active employees
-   Department headcount
-   Average salary
-   New joiners
-   Validation error count

Prefer clear charts and tables over unnecessary visual decoration.

------------------------------------------------------------------------

## 17. Optional Notifications

Notifications may be sent when:

-   A report has successfully been generated.
-   Important validation errors are detected.
-   The processing pipeline fails.

Do not expose credentials in source code.

For local development, a mock/log-based notification mode is acceptable.

------------------------------------------------------------------------

## 18. Scheduled Execution

The application should be capable of being executed automatically.

Possible scheduling mechanisms:

-   Windows Task Scheduler
-   cron
-   cloud scheduler

The core application should remain executable manually as well:

``` bash
python -m app.main
```

------------------------------------------------------------------------

## 19. Testing

If pytest is included, test at least:

-   Valid input
-   Missing columns
-   Missing employee IDs
-   Duplicate records
-   Invalid email
-   Invalid salary
-   Invalid joining date
-   Department normalization
-   Metric calculations
-   Report generation
-   Error handling

Tests should focus on deterministic business logic.

------------------------------------------------------------------------

## 20. Code Quality Requirements

The coding agent must prioritize:

-   Readable Python
-   Small, focused functions
-   Clear naming
-   Type hints where useful
-   Useful docstrings for public functions
-   No unnecessary duplication
-   No hardcoded secrets
-   No silent exception handling
-   Separation of concerns
-   Maintainable modules

Avoid overengineering.

------------------------------------------------------------------------

## 21. CLI / User Experience

A simple command-line interface is preferred for the core system.

Example:

``` bash
python -m app.main --input data/input/employees.csv
```

Possible options:

``` text
--input
--output
--format
--verbose
```

The exact CLI design can be adapted to the implementation.

------------------------------------------------------------------------

## 22. Definition of Done

The project is considered complete when:

-   [ ] CSV input works.
-   [ ] Excel input works.
-   [ ] Required columns are validated.
-   [ ] Invalid employee records are detected.
-   [ ] Duplicate records are detected.
-   [ ] Email values are validated.
-   [ ] Salary values are validated and normalized.
-   [ ] Joining dates are validated and normalized.
-   [ ] Employee data is cleaned.
-   [ ] Department values are standardized.
-   [ ] HR metrics are calculated.
-   [ ] Cleaned employee data is exported.
-   [ ] Department summary is generated.
-   [ ] Validation errors are exported.
-   [ ] A summary report is generated.
-   [ ] Processing is logged.
-   [ ] Exceptions are handled without silently losing errors.
-   [ ] The pipeline can be executed repeatedly.
-   [ ] The project has clear documentation.
-   [ ] A sample input dataset is included.
-   [ ] The project can be set up by another developer using the README.

Optional features should only be marked complete if actually
implemented.

------------------------------------------------------------------------

## 23. Development Priorities

Implement in this order:

### Phase 1 --- Core Pipeline

1.  Project structure
2.  Input reader
3.  Validation
4.  Cleaning
5.  Metrics
6.  Report generation
7.  Logging
8.  Error handling

### Phase 2 --- Reliability

1.  Tests
2.  Configuration
3.  Better validation/error reporting
4.  CLI
5.  Documentation

### Phase 3 --- Extensions

Only after the core system is stable:

1.  SQLite
2.  FastAPI
3.  Streamlit
4.  Notifications
5.  Docker
6.  Cloud deployment

Do not start Phase 3 until Phase 1 works reliably.

------------------------------------------------------------------------

## 24. Coding Agent Instructions

When implementing this project:

1.  Read and follow this `PROJECT.md`.
2.  Treat the **Required Core Features** as mandatory.
3.  Treat **Optional Extensions** as optional unless explicitly
    requested.
4.  Do not introduce unnecessary frameworks or dependencies.
5.  Prefer a simple, modular architecture.
6.  Preserve the original employee data where possible; write cleaned
    data to output files rather than destructively modifying the source.
7.  Make validation failures visible and traceable.
8.  Make the processing pipeline repeatable and deterministic.
9.  Add tests for important business logic.
10. Update `README.md` whenever setup, usage, or architecture changes.
11. Do not add Docker, FastAPI, databases, dashboards, or cloud
    deployment merely for complexity points.
12. If a requirement is ambiguous, prefer the simplest implementation
    consistent with this specification.
13. Never silently ignore errors.
14. Never commit credentials or secrets.
15. Before considering the project complete, verify the entire pipeline
    using a realistic sample dataset.

------------------------------------------------------------------------

## 25. Primary Goal

Build a **reliable, maintainable Python automation system for employee
data processing and HR reporting**, not merely a collection of scripts.

The final project should demonstrate practical skills in:

-   Python
-   File handling
-   Pandas data processing
-   Data validation
-   Data cleaning
-   Business metric calculation
-   Exception handling
-   Logging
-   Automation
-   Report generation

Advanced technologies should enhance the system rather than distract
from its primary purpose.
