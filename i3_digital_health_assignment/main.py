from src.config import RAW_DATA_PATH
from src.ingestion import ExcelIngestor
from src.cleaner import DataCleaner, AIChatCleaner  # Added AIChatCleaner import
from src.database import AnalyticalDatabase
from src.analytics import CohortAnalytics
import logging

def main():
    logging.info("--- Starting I3 Health Pipeline ---")
    
    # 1. Ingest (Part 1A)
    ingestor = ExcelIngestor(filepath=RAW_DATA_PATH)
    raw_df = ingestor.load_data()
    
    # 2. Clean & Deserialize (Part 1B)
    cleaner = DataCleaner(raw_df)
    clean_df = cleaner.execute_cleaning()
    
    # 3. Build DuckDB Analytical Engine (Part 1B)
    db = AnalyticalDatabase()
    db.build_relational_schema(clean_df)
    
    # 4. Compute Success Metrics & Cohort Analysis (Part 2)
    analytics = CohortAnalytics(db)
    df_ind_phase, df_tech = analytics.compute_stratified_success_rates()
    
    print("\n --- STRATIFIED COHORT: INDICATION × PHASE ---")
    print(df_ind_phase.head(10))
    
    print("\n --- STRATIFIED COHORT: TOP DRUGS BY PROXY SUCCESS RATE ---")
    print(df_tech.head(10))

    # =========================================================================
    # NEW UPDATE: STEP 4 AI SEMANTIC PILOT SHOWCASE
    # =========================================================================
    print("\n --- GENERATING LIVE AI SEMANTIC HARMONIZATION SHOWCASE ---")
    ai_agent = AIChatCleaner()
    
    # Isolate a small 3-row subset to cleanly demonstrate the semantic cleanup
    showcase_batch = clean_df.head(3)
    
    for idx, row in showcase_batch.iterrows():
        print(f"\n[NCT ID]: {row['nct_id']}")
        print(f"[Raw Messy Targets Text]: {row['target_names']}")
        
        # Invoke the Live Gemini Model
        standardized_output = ai_agent.standardize_trial_entities(
            brief_title=row['brief_title'],
            messy_targets=str(row['target_names'])
        )
        
        print(f" [AI Normalized Targets]: {standardized_output['standardized_target_classes']}")
        print(f" [AI Controlled Modality]: {standardized_output['primary_technology_modality']}")
        print(f" [AI Brief Summary]: {standardized_output['mechanism_of_action_summary']}")
    
    print("\n --- END OF AI SHOWCASE PILOT ---")
    # =========================================================================

    logging.info("--- Pipeline Execution Complete ---")

if __name__ == "__main__":
    main()