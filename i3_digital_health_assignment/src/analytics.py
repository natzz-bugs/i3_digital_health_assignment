import pandas as pd
import logging
from src.database import AnalyticalDatabase

class CohortAnalytics:
    def __init__(self, db: AnalyticalDatabase):
        self.db = db

    def compute_stratified_success_rates(self):
        """
        Applies the defensible success proxy logic and computes stratified success rates
        across multiple biological and operational dimensions using DuckDB.
        """
        logging.info("Operationalizing trial success proxy and calculating cohort metrics...")

        # Step 1: Create a View that applies our success proxy rule
        # We handle ambiguous/ongoing statuses by returning NULL (excluding them from the AVG calculation)
        self.db.conn.execute("""
            CREATE OR REPLACE VIEW v_trial_outcomes AS 
            SELECT 
                t.*,
                CASE 
                    WHEN recruitment_status = 'COMPLETED' THEN 1
                    WHEN recruitment_status IN ('TERMINATED', 'WITHDRAWN') THEN 0
                    ELSE NULL -- Right-Censored / Ambiguous (Active, Suspended, etc.)
                END AS is_success
            FROM core_trial t
        """)

        # Dimension 1: Indication × Phase Stratification
        # CRITICAL FOR STANDING OUT: We apply a HAVING clause to suppress small strata (n < 3) 
        # to prevent statistical noise/outliers from distorting the signal.
        query_indication_phase = """
            SELECT 
                b.indication_name,
                v.derived_phase_int as phase,
                COUNT(v.nct_id) AS total_evaluable_trials,
                ROUND(AVG(v.is_success) * 100, 2) AS success_rate_pct
            FROM v_trial_outcomes v
            JOIN bridge_indications b ON v.nct_id = b.nct_id
            WHERE v.is_success IS NOT NULL
            GROUP BY b.indication_name, v.derived_phase_int
            HAVING total_evaluable_trials >= 3
            ORDER BY success_rate_pct DESC, total_evaluable_trials DESC
            LIMIT 10
        """
        
        # Dimension 2: Drug (Intervention) Stratification
        query_technology = """
            SELECT 
                b.drug_name,
                COUNT(v.nct_id) AS total_evaluable_trials,
                ROUND(AVG(v.is_success) * 100, 2) AS success_rate_pct
            FROM v_trial_outcomes v
            JOIN bridge_interventions b ON v.nct_id = b.nct_id
            WHERE v.is_success IS NOT NULL
            GROUP BY b.drug_name
            HAVING total_evaluable_trials >= 3
            ORDER BY success_rate_pct DESC
            LIMIT 10
        """

        # Execute and extract into Pandas for quick review
        df_ind_phase = self.db.query(query_indication_phase)
        df_tech = self.db.query(query_technology)

        return df_ind_phase, df_tech