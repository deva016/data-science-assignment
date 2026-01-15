"""
LLM Service Module

Handles LLM interactions with dual-provider fallback strategy:
- Primary: Google Gemini 1.5 Flash (FREE)
- Backup: OpenAI GPT-4o / Anthropic Claude

Generates clinical summaries with citation tracking.
"""

import os
import json
from typing import Dict, Any, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import LLM clients
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠ Google Generative AI library not installed. Gemini will not be available.")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠ OpenAI library not installed. GPT-4o will not be available.")


# Configuration
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
USE_FALLBACK = os.getenv("USE_FALLBACK", "true").lower() == "true"
FORCE_PROVIDER = os.getenv("FORCE_PROVIDER", "").lower()


def _build_system_prompt() -> str:
    """Build the system prompt for the clinical summary generation."""
    return """You are an expert home health clinician with decades of experience in patient care documentation. Your role is to create concise, evidence-based clinical summaries that tell the story of a patient's current condition.

CRITICAL REQUIREMENTS:
1. Every claim must be backed by specific data from the patient record
2. Include citations in the format: [Source: <file>csv, Date: YYYY-MM-DD] or [Source: <file>.csv]
3. Focus on clinically relevant information
4. Highlight trends (improving, stable, declining)
5. Note any concerning findings

OUTPUT FORMAT:
Return a JSON object with this structure:
{
  "summary": "Overall narrative summary (2-3 paragraphs)",
  "sections": {
    "diagnoses": {
      "content": "Primary diagnoses and comorbidities",
      "citations": ["Source: diagnoses.csv"]
    },
    "vitals": {
      "content": "Recent vital sign trends with specific values",
      "citations": ["Source: vitals.csv, Date: 2026-01-08"]
    },
    "wounds": {
      "content": "Active wounds, location, stage, and healing status",
      "citations": ["Source: wounds.csv, Date: 2026-01-08"]
    },
    "medications": {
      "content": "Active medication regimen with classifications",
      "citations": ["Source: medications.csv"]
    },
    "functional_status": {
      "content": "OASIS assessment interpretation - ability to perform ADLs",
      "citations": ["Source: oasis.csv, Date: YYYY-MM-DD"]
    },
    "clinical_notes": {
      "content": "Key observations from nursing notes",
      "citations": ["Source: notes.csv, Date: YYYY-MM-DD"]
    }
  },
  "provider_used": "gemini" or "openai"
}

CRITICAL: You MUST use actual dates from the data, not placeholder dates. Return ONLY valid JSON."""


def _build_user_prompt(patient_context: str) -> str:
    """Build the user prompt with patient data."""
    return f"""Please generate a comprehensive clinical summary for this home health patient.

{patient_context}

Generate the summary following the JSON structure specified above. Ensure every clinical claim has a citation. Return ONLY the JSON object, no additional text."""


def _call_gemini(patient_context: str) -> Dict[str, Any]:
    """
    Call Google Gemini API to generate summary.
    
    Args:
        patient_context: Formatted patient data string
        
    Returns:
        Parsed JSON response from Gemini
        
    Raises:
        Exception: If Gemini API call fails
    """
    if not GEMINI_AVAILABLE:
        raise Exception("Google Generative AI library not installed")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.startswith("your-"):
        raise Exception("GEMINI_API_KEY not configured in .env file")
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    try:
        # Initialize model (don't add models/ prefix, API handles it)
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config={
                "temperature": TEMPERATURE,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )
        
        # Build full prompt
        full_prompt = f"""{_build_system_prompt()}

{_build_user_prompt(patient_context)}"""
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        # Extract text
        response_text = response.text
        
        # Clean up response (remove markdown code blocks if present)
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()
        
        # Parse JSON
        summary_data = json.loads(response_text)
        summary_data['provider_used'] = 'gemini'
        
        print("✓ Gemini API call successful")
        return summary_data
        
    except json.JSONDecodeError as e:
        raise Exception(f"Gemini returned invalid JSON: {e}\nResponse: {response_text[:200]}")
    except Exception as e:
        raise Exception(f"Gemini API error: {str(e)}")


def _call_openai(patient_context: str) -> Dict[str, Any]:
    """
    Call OpenAI GPT-4o API to generate summary.
    
    Args:
        patient_context: Formatted patient data string
        
    Returns:
        Parsed JSON response from OpenAI
        
    Raises:
        Exception: If OpenAI API call fails
    """
    if not OPENAI_AVAILABLE:
        raise Exception("OpenAI library not installed")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-your"):
        raise Exception("OPENAI_API_KEY not configured in .env file")
    
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            temperature=TEMPERATURE,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": _build_system_prompt()
                },
                {
                    "role": "user",
                    "content": _build_user_prompt(patient_context)
                }
            ]
        )
        
        # Extract and parse JSON
        response_text = response.choices[0].message.content
        summary_data = json.loads(response_text)
        summary_data['provider_used'] = 'openai'
        
        print("✓ OpenAI API call successful")
        return summary_data
        
    except json.JSONDecodeError as e:
        raise Exception(f"OpenAI returned invalid JSON: {e}")
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")


def generate_summary(patient_context: str) -> Tuple[Dict[str, Any], str]:
    """
    Generate clinical summary using dual-provider fallback strategy.
    
    Primary: Google Gemini 1.5 Flash (FREE)
    Backup: OpenAI GPT-4o
    
    Args:
        patient_context: Formatted patient data string from data_layer
        
    Returns:
        Tuple of (summary_dict, provider_name)
        
    Raises:
        Exception: If both providers fail
    """
    
    # Check if forced to use specific provider
    if FORCE_PROVIDER == "openai":
        print("🔧 Forced to use OpenAI")
        summary = _call_openai(patient_context)
        return summary, "openai"
    
    if FORCE_PROVIDER == "gemini":
        print("🔧 Forced to use Gemini")
        summary = _call_gemini(patient_context)
        return summary, "gemini"
    
    # Default: Try Gemini first, fallback to OpenAI
    gemini_error = None
    openai_error = None
    
    # PRIMARY: Try Gemini
    try:
        print("🎯 Attempting Gemini (Primary - FREE)...")
        summary = _call_gemini(patient_context)
        return summary, "gemini"
        
    except Exception as e:
        gemini_error = str(e)
        print(f"✗ Gemini failed: {gemini_error}")
    
    # BACKUP: Try OpenAI if fallback enabled
    if USE_FALLBACK:
        try:
            print("🔄 Falling back to OpenAI (Backup)...")
            summary = _call_openai(patient_context)
            return summary, "openai"
            
        except Exception as e:
            openai_error = str(e)
            print(f"✗ OpenAI failed: {openai_error}")
    
    # Both failed - raise comprehensive error
    error_msg = "Both LLM providers failed:\n"
    error_msg += f"  Gemini: {gemini_error}\n"
    if USE_FALLBACK:
        error_msg += f"  OpenAI: {openai_error}\n"
    else:
        error_msg += "  OpenAI: Fallback disabled\n"
    
    raise Exception(error_msg)


if __name__ == "__main__":
    # Test the LLM service
    print("Testing LLM Service...\n")
    
    # Simple test context
    test_context = """# Patient Clinical Data - ID: 9999

## PRIMARY DIAGNOSES
1. Test Diagnosis - Hypertension

## ACTIVE MEDICATIONS
- Test Medication 10mg
  Frequency: DAILY | Class: Cardiovascular | Reason: Blood Pressure

## VITAL SIGNS HISTORY
**2026-01-15:**
  - Blood Pressure: 140/90
  - Heart Rate: 75

## ACTIVE WOUNDS
No wounds

## FUNCTIONAL STATUS (OASIS Assessment)
**Assessment Date:** 2026-01-01
- Grooming: Independent
- Bathing: Independent

## CLINICAL NOTES
**2026-01-15 - NARRATIVE:**
Patient stable, vitals within normal limits.
"""
    
    try:
        summary, provider = generate_summary(test_context)
        print(f"\n✓ Summary generated successfully using: {provider}")
        print(f"\nSummary preview:")
        print(json.dumps(summary, indent=2)[:500])
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure you have:")
        print("1. Created .env file (copy from .env.example)")
        print("2. Added your GEMINI_API_KEY")
        print("3. Installed dependencies: pip install -r requirements.txt")
        print("\nGet FREE Gemini API key at: https://aistudio.google.com/apikey")
