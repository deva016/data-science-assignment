"""
Clinical Summary Generator - Core Package

This package provides data layer and LLM services for generating
evidence-based clinical summaries for home health patients.
"""

from .data_layer import (
    load_all_data,
    get_patient_ids,
    get_patient_data,
    format_for_llm
)

from .llm_service import generate_summary

__version__ = "1.0.0"
__all__ = [
    "load_all_data",
    "get_patient_ids", 
    "get_patient_data",
    "format_for_llm",
    "generate_summary"
]
