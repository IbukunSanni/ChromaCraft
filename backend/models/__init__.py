"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel
from typing import List, Optional


class RandomPaletteRequest(BaseModel):
    """Request model for random palette generation."""
    locked_colors: Optional[List[str]] = None
    harmony_type: Optional[str] = None


class ConceptPaletteRequest(BaseModel):
    """Request model for concept-based palette generation."""
    concept: str
    color_count: Optional[int] = 5


class PaletteResponse(BaseModel):
    """Response model for palette generation endpoints."""
    colors: List[str]
    names: List[str]
    harmony_info: dict


class ColorExtractionResponse(BaseModel):
    """Response model for color extraction from images."""
    colors: List[str]
    names: List[str]


class ConceptAdjustmentResponse(BaseModel):
    """Response model for concept-based color adjustment."""
    adjusted_colors: List[str]
    names: List[str]