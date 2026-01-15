"""
Data Layer Module

Handles loading and querying patient data from CSV files.
Provides functions to fetch patient data and format it for LLM consumption.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
import os


# Get the project root directory (parent of src/)
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def load_all_data() -> Dict[str, pd.DataFrame]:
    """
    Load all CSV files into memory.
    
    Returns:
        Dictionary with DataFrame for each data type:
        {
            'diagnoses': DataFrame,
            'medications': DataFrame,
            'vitals': DataFrame,
            'notes': DataFrame,
            'wounds': DataFrame,
            'oasis': DataFrame
        }
    """
    data = {}
    
    csv_files = {
        'diagnoses': 'diagnoses.csv',
        'medications': 'medications.csv',
        'vitals': 'vitals.csv',
        'notes': 'notes.csv',
        'wounds': 'wounds.csv',
        'oasis': 'oasis.csv'
    }
    
    for key, filename in csv_files.items():
        filepath = DATA_DIR / filename
        try:
            data[key] = pd.read_csv(filepath)
            print(f"✓ Loaded {filename}: {len(data[key])} rows")
        except Exception as e:
            print(f"✗ Error loading {filename}: {e}")
            data[key] = pd.DataFrame()  # Empty DataFrame on error
    
    return data


def get_patient_ids() -> List[int]:
    """
    Get list of unique patient IDs from the diagnoses table.
    
    Returns:
        List of patient IDs (e.g., [1001, 1002])
    """
    data = load_all_data()
    if 'diagnoses' in data and not data['diagnoses'].empty:
        patient_ids = data['diagnoses']['patient_id'].unique().tolist()
        return sorted(patient_ids)
    return []


def get_patient_data(patient_id: int) -> Dict[str, Any]:
    """
    Fetch all clinical data for a specific patient.
    
    Args:
        patient_id: The patient identifier
        
    Returns:
        Dictionary containing all patient data:
        {
            'patient_id': int,
            'diagnoses': List[Dict],
            'medications': List[Dict],
            'vitals': List[Dict],
            'notes': List[Dict],
            'wounds': List[Dict],
            'oasis': List[Dict]
        }
    """
    data = load_all_data()
    patient_data = {'patient_id': patient_id}
    
    # Filter each dataset by patient_id
    for key in ['diagnoses', 'medications', 'vitals', 'notes', 'wounds', 'oasis']:
        if key in data and not data[key].empty:
            filtered = data[key][data[key]['patient_id'] == patient_id]
            # Convert to list of dictionaries for easier processing
            patient_data[key] = filtered.to_dict('records')
        else:
            patient_data[key] = []
    
    return patient_data


def format_for_llm(patient_data: Dict[str, Any]) -> str:
    """
    Format patient data into a clean, structured string for LLM consumption.
    
    Args:
        patient_data: Dictionary from get_patient_data()
        
    Returns:
        Formatted string with all patient information
    """
    patient_id = patient_data['patient_id']
    
    output = f"# Patient Clinical Data - ID: {patient_id}\n\n"
    
    # 1. DIAGNOSES
    output += "## PRIMARY DIAGNOSES\n"
    if patient_data['diagnoses']:
        # Get unique diagnoses
        unique_diagnoses = set()
        for diag in patient_data['diagnoses']:
            unique_diagnoses.add(diag.get('diagnosis_description', 'Unknown'))
        
        for idx, diag in enumerate(unique_diagnoses, 1):
            output += f"{idx}. {diag}\n"
    else:
        output += "No diagnosis data available.\n"
    output += "\n"
    
    # 2. MEDICATIONS
    output += "## ACTIVE MEDICATIONS\n"
    if patient_data['medications']:
        # Get unique medications
        seen_meds = set()
        for med in patient_data['medications']:
            med_name = med.get('medication_name', 'Unknown')
            if med_name not in seen_meds:
                seen_meds.add(med_name)
                freq = med.get('frequency', 'Unknown')
                classification = med.get('classification', 'Unknown')
                reason = med.get('reason', 'Unknown')
                output += f"- {med_name}\n"
                output += f"  Frequency: {freq} | Class: {classification} | Reason: {reason}\n"
    else:
        output += "No medication data available.\n"
    output += "\n"
    
    # 3. VITAL SIGNS
    output += "## VITAL SIGNS HISTORY\n"
    if patient_data['vitals']:
        # Sort by date
        vitals_df = pd.DataFrame(patient_data['vitals'])
        vitals_df['visit_date'] = pd.to_datetime(vitals_df['visit_date'])
        vitals_df = vitals_df.sort_values('visit_date', ascending=False)
        
        # Group by date
        for date, group in vitals_df.groupby('visit_date'):
            output += f"\n**{date.strftime('%Y-%m-%d')}:**\n"
            for _, row in group.iterrows():
                vital_type = row.get('vital_type', 'Unknown')
                reading = row.get('reading', 'N/A')
                output += f"  - {vital_type}: {reading}\n"
    else:
        output += "No vital signs data available.\n"
    output += "\n"
    
    # 4. WOUNDS
    output += "## ACTIVE WOUNDS\n"
    if patient_data['wounds']:
        wounds_df = pd.DataFrame(patient_data['wounds'])
        # Get most recent wound assessment per location
        wounds_df['visit_date'] = pd.to_datetime(wounds_df['visit_date'])
        latest_wounds = wounds_df.sort_values('visit_date', ascending=False).drop_duplicates(
            subset=['location', 'description'], keep='first'
        )
        
        for idx, wound in latest_wounds.iterrows():
            description = wound.get('description', 'Unknown')
            location = wound.get('location', 'Unknown')
            onset = wound.get('onset_date', 'Unknown')
            last_visit = wound.get('visit_date', 'Unknown')
            output += f"- {description} at {location}\n"
            output += f"  Onset: {onset} | Last Assessment: {last_visit}\n"
    else:
        output += "No wound data available.\n"
    output += "\n"
    
    # 5. FUNCTIONAL STATUS (OASIS)
    output += "## FUNCTIONAL STATUS (OASIS Assessment)\n"
    if patient_data['oasis']:
        # Get most recent assessment
        oasis_df = pd.DataFrame(patient_data['oasis'])
        oasis_df['assessment_date'] = pd.to_datetime(oasis_df['assessment_date'])
        latest_oasis = oasis_df.sort_values('assessment_date', ascending=False).iloc[0]
        
        output += f"**Assessment Date:** {latest_oasis.get('assessment_date', 'Unknown')}\n"
        output += f"**Type:** {latest_oasis.get('assessment_type', 'Unknown')}\n\n"
        output += f"- **Grooming:** {latest_oasis.get('grooming', 'Unknown')}\n"
        output += f"- **Bathing:** {latest_oasis.get('bathing', 'Unknown')}\n"
        output += f"- **Toilet Transfer:** {latest_oasis.get('toilet_transfer', 'Unknown')}\n"
        output += f"- **Transfer:** {latest_oasis.get('transfer', 'Unknown')}\n"
        output += f"- **Ambulation:** {latest_oasis.get('ambulation', 'Unknown')}\n"
    else:
        output += "No OASIS data available.\n"
    output += "\n"
    
    # 6. CLINICAL NOTES
    output += "## CLINICAL NOTES (Recent)\n"
    if patient_data['notes']:
        notes_df = pd.DataFrame(patient_data['notes'])
        notes_df['note_date'] = pd.to_datetime(notes_df['note_date'])
        recent_notes = notes_df.sort_values('note_date', ascending=False).head(3)
        
        for _, note in recent_notes.iterrows():
            note_date = note.get('note_date', 'Unknown')
            note_type = note.get('note_type', 'Unknown')
            note_text = note.get('note_text', 'No text')
            output += f"\n**{note_date} - {note_type}:**\n"
            output += f"{note_text[:500]}...\n"  # Truncate long notes
    else:
        output += "No clinical notes available.\n"
    
    return output


if __name__ == "__main__":
    # Test the data layer
    print("Testing Data Layer...\n")
    
    # Test 1: Load all data
    print("1. Loading all data files...")
    all_data = load_all_data()
    print()
    
    # Test 2: Get patient IDs
    print("2. Getting patient IDs...")
    patient_ids = get_patient_ids()
    print(f"   Found patients: {patient_ids}\n")
    
    # Test 3: Get data for first patient
    if patient_ids:
        patient_id = patient_ids[0]
        print(f"3. Getting data for patient {patient_id}...")
        patient_data = get_patient_data(patient_id)
        print(f"   Diagnoses: {len(patient_data['diagnoses'])} records")
        print(f"   Medications: {len(patient_data['medications'])} records")
        print(f"   Vitals: {len(patient_data['vitals'])} records")
        print(f"   Notes: {len(patient_data['notes'])} records")
        print(f"   Wounds: {len(patient_data['wounds'])} records")
        print(f"   OASIS: {len(patient_data['oasis'])} records\n")
        
        # Test 4: Format for LLM
        print("4. Formatting for LLM...")
        formatted = format_for_llm(patient_data)
        print(f"   Generated {len(formatted)} characters of formatted text")
        print("\n--- Preview ---")
        print(formatted[:500])
