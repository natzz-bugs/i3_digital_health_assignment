import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExcelIngestor:
    def __init__(self, filepath: Path | str):
        self.filepath = Path(filepath)

    def load_data(self) -> pd.DataFrame:
        """Loads raw .xlsx file ensuring raw text preservation."""
        logging.info(f"Ingesting raw data from {self.filepath.name}")
        
        if not self.filepath.exists():
            raise FileNotFoundError(f"Critical failure: Dataset not found at {self.filepath}")
            
        try:
            # Enforce string typing universally to prevent silent data corruption
            df = pd.read_excel(self.filepath, engine='openpyxl', dtype=str)
            
            # Standardize column headers (lowercase, snake_case, strip whitespace)
            df.columns = (
                df.columns.str.strip()
                .str.lower()
                .str.replace(' ', '_')
                .str.replace('-', '_')
            )
            logging.info(f"Successfully ingested {len(df)} rows and {len(df.columns)} columns.")
            return df
            
        except Exception as e:
            logging.error(f"Failed to ingest data: {e}")
            raise