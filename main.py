"""
FastAPI Backend for Clinical Summary Generator

Provides REST API endpoints for patient data and summary generation.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data_layer import get_patient_ids, get_patient_data, format_for_llm
from src.llm_service import generate_summary


# FastAPI app initialization
app = FastAPI(
    title="Clinical Summary Generator API",
    description="Generate evidence-based clinical summaries for home health patients",
    version="1.0.0"
)

# CORS middleware to allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class SummaryRequest(BaseModel):
    """Request model for summary generation."""
    patient_id: int = Field(..., description="Patient ID to generate summary for")
    include_citations: bool = Field(True, description="Include citation tracking")


class SummaryResponse(BaseModel):
    """Response model for generated summary."""
    patient_id: int
    summary: Dict[str, Any]
    provider_used: str
    success: bool


class PatientListResponse(BaseModel):
    """Response model for patient list."""
    patient_ids: List[int]
    count: int


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    message: str


# API Endpoints

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check."""
    return {
        "status": "healthy",
        "message": "Clinical Summary Generator API is running"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "All systems operational"
    }


@app.get("/patients", response_model=PatientListResponse)
async def list_patients():
    """
    Get list of available patient IDs.
    
    Returns:
        PatientListResponse: List of patient IDs and count
    """
    try:
        patient_ids = get_patient_ids()
        
        if not patient_ids:
            raise HTTPException(
                status_code=404,
                detail="No patients found in database"
            )
        
        return {
            "patient_ids": patient_ids,
            "count": len(patient_ids)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching patient list: {str(e)}"
        )


@app.post("/generate_summary", response_model=SummaryResponse)
async def create_summary(request: SummaryRequest):
    """
    Generate clinical summary for a specific patient.
    
    Args:
        request: SummaryRequest with patient_id and options
        
    Returns:
        SummaryResponse: Generated summary with citations
        
    Raises:
        HTTPException: 404 if patient not found, 500 for other errors
    """
    try:
        # Validate patient exists
        available_patients = get_patient_ids()
        if request.patient_id not in available_patients:
            raise HTTPException(
                status_code=404,
                detail=f"Patient {request.patient_id} not found. Available patients: {available_patients}"
            )
        
        # Fetch patient data
        print(f"📋 Fetching data for patient {request.patient_id}...")
        patient_data = get_patient_data(request.patient_id)
        
        # Format for LLM
        print(f"✏️  Formatting data for LLM...")
        patient_context = format_for_llm(patient_data)
        
        # Generate summary
        print(f"🤖 Generating summary...")
        summary, provider = generate_summary(patient_context)
        
        return {
            "patient_id": request.patient_id,
            "summary": summary,
            "provider_used": provider,
            "success": True
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        # Internal server error
        error_detail = str(e)
        print(f"✗ Error generating summary: {error_detail}")
        
        # Provide helpful error messages
        if "API" in error_detail or "key" in error_detail.lower():
            error_detail += "\n\nMake sure you have configured API keys in .env file."
        
        raise HTTPException(
            status_code=500,
            detail=f"Error generating summary: {error_detail}"
        )


@app.get("/patient/{patient_id}/data")
async def get_raw_patient_data(patient_id: int):
    """
    Get raw patient data (for debugging/testing).
    
    Args:
        patient_id: Patient identifier
        
    Returns:
        Dict with all patient data
    """
    try:
        # Validate patient exists
        available_patients = get_patient_ids()
        if patient_id not in available_patients:
            raise HTTPException(
                status_code=404,
                detail=f"Patient {patient_id} not found. Available patients: {available_patients}"
            )
        
        patient_data = get_patient_data(patient_id)
        
        # Convert to counts for overview
        return {
            "patient_id": patient_id,
            "data_summary": {
                "diagnoses_count": len(patient_data.get('diagnoses', [])),
                "medications_count": len(patient_data.get('medications', [])),
                "vitals_count": len(patient_data.get('vitals', [])),
                "notes_count": len(patient_data.get('notes', [])),
                "wounds_count": len(patient_data.get('wounds', [])),
                "oasis_count": len(patient_data.get('oasis', []))
            },
            "full_data": patient_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching patient data: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Clinical Summary Generator API...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Interactive API: http://localhost:8000/redoc")
    print("\nPress Ctrl+C to stop\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
