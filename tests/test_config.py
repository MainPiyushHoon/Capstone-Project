from pathlib import Path
import pytest
from app.config import Config
from app.utils.logger import setup_logger

def test_config_defaults():
    assert isinstance(Config.INPUT_DIR, Path)
    assert isinstance(Config.OUTPUT_DIR, Path)
    assert "employee_id" in Config.REQUIRED_COLUMNS
    assert "email" in Config.REQUIRED_COLUMNS

def test_logger_setup(tmp_path):
    log_file = tmp_path / "test.log"
    logger = setup_logger(log_file=log_file, verbose=True)
    logger.info("Test logger message")
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "Test logger message" in content
