import pandas as pd
import logging
from pathlib import Path

class DataProfiler:
    def __init__(self, df: pd.DataFrame, output_dir: Path):
        self.df = df
        self.output_dir = output_dir

    def run_audit(self) -> dict:
        """Executes a programmatic audit on the dataset."""
        logging.info("Executing Data Quality Audit...")
        
        audit_results = {
            "total_records": len(self.df),
            "columns": len(self.df.columns),
            "completeness": {},
            "cardinality": {},
            "anomalies": {}
        }

        for col in self.df.columns:
            # Completeness: Calculate percentage of non-null values
            missing_count = self.df[col].isna().sum()
            audit_results["completeness"][col] = round((1 - missing_count / len(self.df)) * 100, 2)
            
            # Cardinality: How many unique categorical values exist?
            audit_results["cardinality"][col] = self.df[col].nunique()

        # Specifically hunt for formatting anomalies in the raw text
        if 'recruitment_status' in self.df.columns:
            # Hunt for unescaped newlines in the middle of words
            messy_status_count = self.df['recruitment_status'].str.contains(r'\n', na=False, regex=True).sum()
            audit_results["anomalies"]["newline_in_status"] = messy_status_count

        if 'nct_id' in self.df.columns:
            # Duplicate clinical trial IDs will break downstream relational joins
            duplicate_ids = self.df['nct_id'].duplicated().sum()
            audit_results["anomalies"]["duplicate_nct_ids"] = duplicate_ids

        return audit_results

    def generate_markdown_report(self, audit_results: dict):
        """Generates a presentation-ready markdown report."""
        report_path = self.output_dir / "data_quality_report.md"
        logging.info(f"Exporting markdown report to {report_path.name}")
        
        with open(report_path, "w", encoding='utf-8') as f:
            f.write("# 📊 Data Quality Audit Report\n\n")
            f.write(f"**Total Records:** {audit_results['total_records']} | **Total Columns:** {audit_results['columns']}\n\n")
            
            f.write("## 1. Field Completeness & Cardinality\n")
            f.write("| Feature | Completeness (%) | Unique Values (Cardinality) |\n")
            f.write("| :--- | :--- | :--- |\n")
            
            for col in self.df.columns:
                comp = audit_results["completeness"][col]
                card = audit_results["cardinality"][col]
                
                # Flag fields with less than 80% completeness
                comp_str = f"**{comp}%** ⚠️" if comp < 80 else f"{comp}%"
                f.write(f"| `{col}` | {comp_str} | {card} |\n")
                
            f.write("\n## 2. Structural Anomalies Detected\n")
            f.write(f"- **Duplicate `nct_id` records:** {audit_results['anomalies'].get('duplicate_nct_ids', 0)}\n")
            f.write(f"- **Newline/Truncation errors in `recruitment_status`:** {audit_results['anomalies'].get('newline_in_status', 0)}\n")
            f.write("\n> *Note: These anomalies mandate a strict string-normalization and deduplication layer before analytical metrics can be reliably computed.*\n")