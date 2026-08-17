from pathlib import Path
import pandas as pd

def read_employee_file(file_path: Path | str) -> pd.DataFrame:
    """Reads employee dataset from CSV or Excel file safely into a pandas DataFrame."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found at: {path}")
        
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, dtype=str)
    elif suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path, dtype=str, engine="openpyxl")
    else:
        raise ValueError(f"Unsupported file format '{suffix}'. Supported formats: .csv, .xlsx, .xls")
