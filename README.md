# Clinical Summary Generator Project

## Objective
Build a "Clinical Summary Generator" application that ingests patient data from CSV files and uses an LLM to generate a structured clinical summary.

## Overview
You are provided with a set of CSV files in the `data/` directory representing a simplified Electronic Health Record (EHR) database. Your task is to build a system that allows a user to select a patient and generate a concise, evidence-based clinical summary.

## Requirements

### 1. Data Layer
- Ingest data from the provided CSV files (`diagnoses.csv`, `medications.csv`, `vitals.csv`, `notes.csv`, `wounds.csv`, `oasis.csv`).
- Implement a way to filter/query this data by `patient_id`.
- Imagine these CSVs represent tables in a relational database.

### 2. Core Functionality
- **Objective**: Generate a clinical summary for a specific patient.
- **Process**: 
    1. Accept a `patient_id` as input.
    2. Fetch all relevant clinical data (meds, vitals, notes, etc.) for that patient from the Data Layer.
    3. Format this data into a context string.
    4. Send the context to an LLM to generate the summary.

### 3. Access Points
The core functionality must be accessible via two interfaces:

#### A. Backend API
- Create a Python API (e.g., FastAPI, Flask) with at least one endpoint:
    - `POST /generate_summary`: Accepts `patient_id` -> Returns the generated summary.

#### B. Frontend UI
- Build a simple **Streamlit** app.
- Input field for `patient_id`.
- A "Generate Summary" button that calls your API.
- Display the generated summary in a clear, readable format.

### 4. LLM Integration
- Construct a prompt that instructs the LLM to act as a home health clinician.
- **Goal**: The summary should tell the story of the patient's current condition, focusing on:
    - Primary diagnoses
    - Recent vital sign trends
    - Active wounds (if any)
    - Medication adherence or changes
    - Recent functional status (OASIS)
### 5. Bonus: Citations & Evidence
Clinical summaries must be verifiable.
- **Requirement**: The LLM should not just generate text; it should cite *where* the information came from.
- **Implementation**:
    - Instruct the LLM to include the source file or date for every claim. 
    - Example: "Patient's blood pressure has been elevated (145/88 on 2023-10-01) [Source: Vitals Log]."
    - **Advanced**: Return the response in a structured format (JSON) that links each sentence to a specific data point from the CSVs.
    - **UI**: Display these citations so the user can trust the summary.

## Deliverables
- A GitHub repository (or zip file) containing:
    - `app.py` (Streamlit frontend)
    - `main.py` (API backend) or a unified app structure.
    - `requirements.txt`
    - A brief `README.md` explaining how to run your code.

## Evaluation Criteria
- **Code Quality**: Clean, readable, and structured code.
- **System Design**: Separation of concerns (Data vs. Logic vs. UI).
- **Prompt Engineering**: How well does the prompt handle the raw data?
- **User Experience**: Is the application intuitive?

## Getting Started
1.  Explore the `data/` directory to understand the schema.
2.  Set up your virtual environment.
3.  Start building!
