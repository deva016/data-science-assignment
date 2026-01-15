"""
Streamlit Frontend for Clinical Summary Generator

User-friendly interface for generating and viewing clinical summaries.
"""

import streamlit as st
import requests
import json
from typing import Dict, Any


# Page configuration
st.set_page_config(
    page_title="Clinical Summary Generator",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Configuration
API_BASE_URL = st.sidebar.text_input(
    "API Base URL",
    value="http://localhost:8000",
    help="URL of the FastAPI backend"
)


def fetch_patients() -> list:
    """Fetch available patient IDs from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/patients", timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("patient_ids", [])
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to API. Make sure the backend is running.")
        st.info("Start the backend with: `uvicorn main:app --reload`")
        return []
    except Exception as e:
        st.error(f"Error fetching patients: {e}")
        return []


def generate_summary(patient_id: int, include_citations: bool = True) -> Dict[str, Any]:
    """Call API to generate summary."""
    try:
        payload = {
            "patient_id": patient_id,
            "include_citations": include_citations
        }
        
        response = requests.post(
            f"{API_BASE_URL}/generate_summary",
            json=payload,
            timeout=60  # LLM calls can take time
        )
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The LLM might be taking longer than expected.")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error: {e}")
        st.error(f"Response: {e.response.text}")
        return None
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None


def display_section(section_name: str, section_data: Dict[str, Any]):
    """Display a summary section with citations."""
    content = section_data.get("content", "No data available")
    citations = section_data.get("citations", [])
    
    st.markdown(f"**{content}**")
    
    if citations:
        citation_text = " | ".join([f"`{cite}`" for cite in citations])
        st.caption(f"📚 Sources: {citation_text}")


def display_summary(summary_data: Dict[str, Any]):
    """Display the complete clinical summary."""
    
    # Overall Summary
    st.markdown("### 📋 Clinical Summary")
    overall_summary = summary_data.get("summary", "No summary available")
    st.markdown(overall_summary)
    
    st.divider()
    
    # Detailed Sections
    sections = summary_data.get("sections", {})
    
    if sections:
        st.markdown("### 📊 Detailed Clinical Findings")
        
        # Create tabs for each section
        section_names = list(sections.keys())
        section_labels = [name.replace("_", " ").title() for name in section_names]
        tabs = st.tabs(section_labels)
        
        for tab, section_name in zip(tabs, section_names):
            with tab:
                section_data = sections[section_name]
                display_section(section_name, section_data)
    
    # Provider info
    provider = summary_data.get("provider_used", "unknown")
    st.divider()
    
    provider_emoji = "🟣" if provider == "claude" else "🟢"
    st.caption(f"{provider_emoji} Generated using: **{provider.upper()}**")


def main():
    """Main application."""
    
    # Header
    st.title("🏥 Clinical Summary Generator")
    st.markdown("""
    Generate comprehensive, evidence-based clinical summaries for home health patients 
    using advanced AI with citation tracking.
    """)
    
    # Check API health
    try:
        health_response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            st.sidebar.success("✅ API Connected")
        else:
            st.sidebar.error("❌ API Error")
    except:
        st.sidebar.error("❌ API Offline")
        st.sidebar.info("Start backend: `uvicorn main:app --reload`")
    
    # Sidebar controls
    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ Configuration")
    
    # Fetch available patients
    patients = fetch_patients()
    
    if not patients:
        st.warning("⚠️ No patients available. Please check the backend connection.")
        st.stop()
    
    # Patient selection
    selected_patient = st.sidebar.selectbox(
        "Select Patient ID",
        options=patients,
        format_func=lambda x: f"Patient {x}"
    )
    
    # Include citations toggle
    include_citations = st.sidebar.checkbox(
        "Include Citations",
        value=True,
        help="Track source data for every clinical claim"
    )
    
    # Provider info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 AI Providers")
    st.sidebar.info("""
    **Primary:** Claude 3.5 Sonnet (Anthropic)  
    **Backup:** GPT-4o (OpenAI)
    
    The system automatically falls back to OpenAI if Claude is unavailable.
    """)
    
    # Generate button
    st.sidebar.markdown("---")
    generate_button = st.sidebar.button(
        "🚀 Generate Summary",
        type="primary",
        use_container_width=True
    )
    
    # Main content area
    if generate_button:
        with st.spinner(f"🔄 Generating clinical summary for Patient {selected_patient}..."):
            result = generate_summary(selected_patient, include_citations)
            
            if result and result.get("success"):
                st.success(f"✅ Summary generated successfully for Patient {selected_patient}")
                
                # Store in session state
                st.session_state['last_summary'] = result
                st.session_state['last_patient_id'] = selected_patient
            else:
                st.error("❌ Failed to generate summary. Check the errors above.")
    
    # Display cached summary if available
    if 'last_summary' in st.session_state:
        st.markdown("---")
        
        # Download button
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            summary_json = json.dumps(
                st.session_state['last_summary']['summary'],
                indent=2
            )
            st.download_button(
                label="📥 Download JSON",
                data=summary_json,
                file_name=f"patient_{st.session_state['last_patient_id']}_summary.json",
                mime="application/json"
            )
        
        with col2:
            # Create text version
            summary_obj = st.session_state['last_summary']['summary']
            text_summary = f"CLINICAL SUMMARY - Patient {st.session_state['last_patient_id']}\n\n"
            text_summary += summary_obj.get('summary', '') + "\n\n"
            
            st.download_button(
                label="📄 Download Text",
                data=text_summary,
                file_name=f"patient_{st.session_state['last_patient_id']}_summary.txt",
                mime="text/plain"
            )
        
        # Display summary
        display_summary(st.session_state['last_summary']['summary'])
    
    else:
        # Welcome message
        st.info("👈 Select a patient and click **Generate Summary** to begin")
        
        # Show example
        with st.expander("ℹ️ About this Application"):
            st.markdown("""
            ### Features
            - **Dual-LLM Architecture**: Uses Claude 3.5 Sonnet with OpenAI fallback
            - **Citation Tracking**: Every claim is backed by source data
            - **Comprehensive Analysis**: Covers diagnoses, vitals, wounds, medications, and functional status
            - **Evidence-Based**: All summaries are grounded in actual patient data
            
            ### How It Works
            1. Select a patient from the dropdown
            2. Click "Generate Summary"
            3. The system fetches patient data from CSV files
            4. AI generates a clinical summary with citations
            5. View, download, or share the summary
            
            ### Data Sources
            - `diagnoses.csv` - Medical conditions
            - `medications.csv` - Active prescriptions
            - `vitals.csv` - Vital sign history
            - `notes.csv` - Clinical notes
            - `wounds.csv` - Wound assessments
            - `oasis.csv` - Functional status
            """)


if __name__ == "__main__":
    main()
