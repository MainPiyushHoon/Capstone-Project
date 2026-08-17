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
    """Executes end-to-end employee data processing pipeline."""
    input_file = Path(input_file)
    output_dir = Path(output_dir)
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
            
        logger.info("==========================================")
        logger.info("Pipeline completed successfully!")
        logger.info("==========================================")
        
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
