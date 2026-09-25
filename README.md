#Zepto Data & AI Platform
This repository contains three independent modules covering data engineering, data analytics/modeling, and a Retrieval-Augmented Generation (RAG) based customer support assistant.

## Repository Structure

```text
project/
│
├── data_pipeline/
│   ├──queries
│   ├──books.db
│   ├── Datapipeline.ipynb
│   ├── requirements.txt
│   └── README.md
│
├── analytics/
│   ├── plots
│   ├──EDA
│   ├── modelling
│   ├── titanic.csv
│   ├── titanic_random_forest_pipeline.joblib
│   ├── requirements.txt
│   ├── README_TASK.md
│   └── README.md
│
├── support_assistant/
│   ├── docs/
│   ├── chroma_db/
│   ├── support_assistance.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
└── README.md
```

---

# 1. Data Pipeline

The `/data_pipeline` module contains the complete data processing workflow, including scraping, data cleaning, database loading, and SQL analysis.

### Contents

- Data scraping and collection code
- Data cleaning and preprocessing
- SQLite database
- Database loading scripts
- Executed SQL queries and outputs
- Module-level documentation

Detailed installation, execution steps, and design decisions are available in:

`/data_pipeline/README.md`

---

# 2. Analytics

The `/analytics` module contains exploratory data analysis and machine learning modeling using the Titanic dataset.

### Contents

- EDA notebook
- Modeling notebook
- `titanic.csv` offline fallback dataset
- Saved chart images
- Saved `joblib` pipeline
- Model comparison
- Required written interpretations
- Final model recommendation

### Main Workflow

```text
Titanic Dataset
      ↓
Data Cleaning
      ↓
Exploratory Data Analysis
      ↓
Feature Engineering
      ↓
Model Training
      ↓
Model Comparison
      ↓
Final Pipeline
```
Detailed installation, execution steps, and design decisions are available in:

`/analytics/README.md`

# 3. Support Assistant

The `/support_assistant` module contains a Zepto customer support assistant implemented using Retrieval-Augmented Generation (RAG), LangGraph, FastAPI, ChromaDB, and Sentence Transformers.

### Contents

- Zepto policy corpus files
- ChromaDB vector database
- LangGraph workflow
- FastAPI application
- Pydantic response validation
- Dockerfile
- Requirements file
- Example API call transcripts


### RAG Workflow

```text
Zepto Policy Documents
        ↓
     Ingestion
        ↓
Sentence Transformer
(all-MiniLM-L6-v2)
        ↓
     ChromaDB
  zepto_policies
        ↓
   User Question
        ↓
  classify_intent
      ↙      ↘
 Policy       General
 Question     Question
    ↓             ↓
retrieve_      direct_
and_answer     answer
    ↓             ↓
    └──────┬──────┘
           ↓
      FinalAnswer
           ↓
       FastAPI
       POST /ask
```

The application uses the default:

```text
MOCK_LLM=1
```

The mock configuration is used for the required graded baseline. Policy questions retrieve the top 3 relevant documents from ChromaDB, while general questions are handled by the direct-answer node.

The FastAPI endpoint is:

```text
POST /ask
```

The application can be run locally using Uvicorn, and the Dockerfile provides the required local containerization.

Detailed architecture, setup instructions, example API calls, and Docker instructions are available in:

`/support_assistant/README.md`

---

# Overall Project Structure

The repository demonstrates three related but independently organized workflows:

```text
                    PROJECT
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
 Web scraping    analytics    support_assistant
        │              │              │
   Data Pipeline      EDA & ML        RAG
        │              │              │
    SQLite DB      ML Pipeline     ChromaDB
                       │              │
                    Joblib         LangGraph
                                      │
                                    FastAPI
                                      │
                                    Docker
```

## Technologies Used

### Data Pipeline

- Python
- Pandas
- SQLite
- SQL

### Analytics

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Joblib

### Support Assistant

- Python
- Sentence Transformers
- ChromaDB
- LangGraph
- FastAPI
- Pydantic
- Uvicorn
- Docker
