from pathlib import Path
import pandas as pd
import pytest
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
    txt_file.write_text("hello", encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported file format"):
        read_employee_file(txt_file)
