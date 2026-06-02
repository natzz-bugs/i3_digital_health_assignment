# I3 Digital Health Assignment

A comprehensive Python-based data pipeline for processing, analyzing, and harmonizing clinical trial health data using AI-powered semantic normalization.

## 📋 Overview

This project implements a complete data engineering and analytics solution for clinical trial information, including:

- **Data Ingestion**: Load and parse Excel-based clinical trial datasets
- **Data Cleaning**: Validate and standardize raw clinical trial information
- **Relational Database**: Build and query analytical schemas using DuckDB
- **Cohort Analytics**: Compute stratified success rates across trial indications and technologies
- **AI Semantic Harmonization**: Use Google Gemini API to intelligently standardize trial entities and clinical terminology

## 🏗️ Project Structure

```
i3_digital_health_assignment/
├── main.py                 # Main pipeline orchestration script
├── test_api.py             # Gemini API connection test utility
├── src/
│   ├── config.py           # Configuration and path definitions
│   ├── ingestion.py        # Excel data loading and ingestion
│   ├── cleaner.py          # Data validation and AI-powered cleaning
│   ├── database.py         # DuckDB analytical database schema
│   ├── analytics.py        # Cohort analysis and success metrics
│   └── __init__.py
├── data/                   # Raw and processed data directory
└── reports/                # Output reports and analytics results
```

## 🎯 Key Features

### 1. **Data Ingestion**
- Load Excel files containing clinical trial information
- Support for raw, unstructured data
- Configurable data paths via `src/config.py`

### 2. **Data Cleaning & Validation**
- Standardize clinical trial entities
- Deserialize and validate trial information
- Handle messy, unstructured text data

### 3. **Analytical Database**
- DuckDB-powered relational schema
- Optimized for cohort analysis queries
- Supports complex trial stratification

### 4. **Cohort Analytics**
Compute stratified success metrics including:
- **Indication × Phase Analysis**: Success rates across trial indications and clinical phases
- **Technology-Based Analysis**: Top drug/technology rankings by proxy success rates
- Custom cohort definitions and aggregations

### 5. **AI Semantic Harmonization** ✨
- Integration with Google Gemini 2.5 Flash API
- Intelligent standardization of trial entities (targets, modalities, mechanisms)
- Entity relationship extraction from clinical trial text
- Real-time semantic enhancement of clinical terminology

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API key (for AI features)
- Dependencies (see installation)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/natzz-bugs/i3_digital_health_assignment.git
   cd i3_digital_health_assignment
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   - Update `test_api.py` with your Google Gemini API key:
     ```python
     MY_KEY = "your_api_key_here"
     ```

### Usage

#### Run the Complete Pipeline
```bash
python main.py
```

This will:
1. Load clinical trial data from Excel
2. Clean and standardize the data
3. Build the DuckDB analytical schema
4. Compute cohort analysis metrics
5. Run AI semantic harmonization on sample trials
6. Output stratified success rates and insights

#### Test Gemini API Connection
```bash
python test_api.py
```

Verifies your Google Gemini API credentials are working properly.

## 📊 Output

The pipeline generates:

- **Stratified Cohort Analysis**: Success rates broken down by indication and clinical phase
- **Technology Rankings**: Top drugs/technologies ranked by success proxy metrics
- **AI-Normalized Entities**: Standardized target classes, modalities, and mechanisms of action
- **Logging**: Detailed pipeline execution logs

Example output structure:
```
--- STRATIFIED COHORT: INDICATION × PHASE ---
[DataFrame with indication, phase, success_count, success_rate]

--- STRATIFIED COHORT: TOP DRUGS BY PROXY SUCCESS RATE ---
[DataFrame with drug/technology, success_rate, trial_count]

--- AI SEMANTIC HARMONIZATION SHOWCASE ---
[NCT ID]: NCT03456789
[Raw Messy Targets Text]: "PI3K/mTOR pathway inhibitor, targeted therapy"
[AI Normalized Targets]: ["PI3K Inhibitor", "mTOR Inhibitor"]
[AI Controlled Modality]: ["Small Molecule", "Targeted Therapy"]
[AI Brief Summary]: "Dual pathway inhibition for oncology indication"
```

## 🤖 AI Features

### Google Gemini Integration

The `AIChatCleaner` class provides intelligent semantic harmonization:

```python
from src.cleaner import AIChatCleaner

ai_agent = AIChatCleaner()
result = ai_agent.standardize_trial_entities(
    brief_title="Phase II Trial of Novel mTOR Inhibitor",
    messy_targets="PI3K pathway blocker, mTOR inhibitor"
)

print(result['standardized_target_classes'])
print(result['primary_technology_modality'])
print(result['mechanism_of_action_summary'])
```

**Capabilities:**
- Normalize messy target descriptions to standardized classes
- Identify primary technology modalities
- Generate structured mechanism of action summaries
- Handle domain-specific clinical terminology

## 📝 Core Modules

### `src/config.py`
Configuration management including:
- Raw data path definitions
- API endpoints
- Database parameters

### `src/ingestion.py`
`ExcelIngestor` class for loading clinical trial data from Excel files.

### `src/cleaner.py`
- `DataCleaner`: Base data validation and standardization
- `AIChatCleaner`: AI-powered semantic harmonization using Gemini API

### `src/database.py`
`AnalyticalDatabase` class for DuckDB schema creation and relational data modeling.

### `src/analytics.py`
`CohortAnalytics` class for computing stratified success rates across multiple dimensions.

## 🔧 Configuration

Update `src/config.py` to customize:
- Data file paths
- DuckDB schema definitions
- Cohort analysis parameters
- AI model parameters

## 📚 Requirements

See `requirements.txt` for a complete dependency list. Key dependencies:
- `pandas`: Data manipulation and analysis
- `duckdb`: Analytical database engine
- `google-genai`: Gemini API client
- `openpyxl`: Excel file parsing

## 🧪 Testing

Run the API test to verify Gemini connectivity:
```bash
python test_api.py
```

Expected output:
```
📡 Attempting connection to Gemini...
🟢 SUCCESS! Your AI Studio Key is active.
🤖 Gemini Response: [Model response text]
```

## 📄 License

[Specify your license here]

## 👤 Author

**natzz-bugs**

## 📞 Support

For issues, questions, or contributions, please open a GitHub issue or submit a pull request.

---

**Last Updated**: June 2, 2026
