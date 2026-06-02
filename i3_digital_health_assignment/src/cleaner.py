import pandas as pd
import ast
import logging
import json
import pydantic
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY

class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    @staticmethod
    def safe_parse_list(val: str) -> list:
        """Safely evaluates stringified lists into actual Python lists."""
        if pd.isna(val) or str(val).strip() == "":
            return []
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            # Fallback for malformed strings that aren't proper lists
            return [str(val).strip()]

    @staticmethod
    def normalize_phase(phase_str: str) -> int:
        """Maps varying phase designations to a numerical hierarchy."""
        if pd.isna(phase_str): 
            return -1
        normalized = str(phase_str).upper().replace(" ", "").replace("_", "")
        if "EARLYPHASE1" in normalized or "PHASE1" in normalized: return 1
        if "PHASE1/PHASE2" in normalized or "PHASE1/2" in normalized: return 12 #Update this to 1.5
        if "PHASE2" in normalized: return 2
        if "PHASE3" in normalized: return 3
        if "PHASE4" in normalized: return 4
        return -1

    def execute_cleaning(self) -> pd.DataFrame:
        logging.info("Deserializing nested arrays and normalizing dates...")
        
        # 1. Deserialize the complex string columns
        list_columns = ['indications', 'interventions_drugs', 'target_names']
        for col in list_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].apply(self.safe_parse_list)

        # 2. Normalize Categoricals
        if 'phase' in self.df.columns:
            self.df['derived_phase_int'] = self.df['phase'].apply(self.normalize_phase)

        # 3. Clean Temporal Data (Forces bad dates to NaT instead of crashing)
        self.df['start_date'] = pd.to_datetime(self.df['start_date'], errors='coerce')
        self.df['completion_date'] = pd.to_datetime(self.df['completion_date'], errors='coerce')
        
        return self.df
    
#Define the strict output structure required from the AI
class StandardizedBioEntities(pydantic.BaseModel):
    standardized_target_classes: list[str]
    primary_technology_modality: str  # E.g., Monoclonal Antibody, Small Molecule, Cell Therapy
    mechanism_of_action_summary: str


#Define the AI Cleaning Agent
class AIChatCleaner:
    def __init__(self):

        # Read the credential directly from the centralized config file
        self.api_key = GEMINI_API_KEY
        
        if not self.api_key or self.api_key == "YOUR_ACTUAL_GEMINI_API_KEY_HERE":
            logging.warning("AI Key placeholder detected. Live pilot fallback triggered.")
            
        # Initialize the connection client
        self.client = genai.Client(api_key=self.api_key)

        # # Initializes the client; looks for GEMINI_API_KEY environment variable natively
        # self.client = genai.Client()

    def standardize_trial_entities(self, brief_title: str, messy_targets: str) -> dict:
        """Uses Gemini to resolve high-cardinality synonyms and typos into controlled terms."""
        prompt = f"""
        You are an expert oncology data scientist and bioinformatics data engineer. 
        Review the following clinical trial brief title and its raw, unstructured biological target strings.
        
        Tasks:
        1. Clean and normalize the messy targets into a uniform, standardized target class nomenclature (e.g., convert 'Programmed cell death protein 1', 'PD1', or 'PD-1 receptor' to 'PD-1').
        2. Classify the primary technology modality into a strict controlled vocabulary choice (e.g., 'Monoclonal Antibody', 'Small Molecule', 'CAR-T Cell Therapy', 'Oncolytic Virus').

        Trial Brief Title: {brief_title}
        Messy Extracted Targets: {messy_targets}
        """
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=StandardizedBioEntities,
                    temperature=0.1,  # Low temperature forces deterministic database-style mapping
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            logging.warning(f"AI Extraction failed, falling back to safe default values: {e}")
            return {
                "standardized_target_classes": [],
                "primary_technology_modality": "UNKNOWN",
                "mechanism_of_action_summary": "API Connection / Extraction Failure"
            }