import duckdb
import pandas as pd
import logging

class AnalyticalDatabase:
    def __init__(self):
        # Initialize an in-memory analytical database
        self.conn = duckdb.connect(database=':memory:')

    def build_relational_schema(self, cleaned_df: pd.DataFrame):
        """Transforms the flat dataframe into a normalized relational model."""
        logging.info("Initializing DuckDB OLAP engine and building schema...")
        
        # Register the pandas dataframe as a virtual table in DuckDB
        self.conn.register('raw_trials', cleaned_df)

        # 1. Create Core Trial Table (Fact Table)
        # We exclude the nested lists here to keep the table strictly 1-to-1 with NCT_ID
        self.conn.execute("""
            CREATE TABLE core_trial AS 
            SELECT 
                nct_id,
                brief_title,
                recruitment_status,
                derived_phase_int,
                start_date,
                completion_date,
                date_diff('day', start_date, completion_date) AS derived_duration_days
            FROM raw_trials
        """)

        # 2. Create Indications Bridge Table (Many-to-Many)
        # UNNEST automatically explodes the python lists into separate rows!
        self.conn.execute("""
            CREATE TABLE bridge_indications AS 
            SELECT DISTINCT
                nct_id,
                UNNEST(indications) AS indication_name
            FROM raw_trials
            WHERE len(indications) > 0
        """)

        # 3. Create Interventions Bridge Table (Many-to-Many)
        self.conn.execute("""
            CREATE TABLE bridge_interventions AS 
            SELECT DISTINCT
                nct_id,
                UNNEST(interventions_drugs) AS drug_name
            FROM raw_trials
            WHERE len(interventions_drugs) > 0
        """)
        
        logging.info("Relational schema successfully constructed in DuckDB.")

    def query(self, sql_query: str) -> pd.DataFrame:
        """Executes a SQL query against the analytical schema and returns a DataFrame."""
        return self.conn.execute(sql_query).df()