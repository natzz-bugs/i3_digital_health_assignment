from pathlib import Path

#Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "SampleDateExtract.xlsx"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"

#Output directories exist at runtime
PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================================
# TEMPORARY CREDENTIAL MANAGEMENT (For Local Assessment Validation)
# =========================================================================
# The downstream AIChatCleaner module will automatically ingest this variable.
GEMINI_API_KEY = "paste_API_key_here"