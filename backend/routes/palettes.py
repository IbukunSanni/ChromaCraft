"""
Palette generation routes for random and AI-powered palette creation.
Thin routes that delegate business logic to service layer.
"""

from fastapi import APIRouter, HTTPException

from services.palette_service import PaletteService
from routes.health import print_mem
from models import RandomPaletteRequest, ConceptPaletteRequest, PaletteResponse
from constants import ErrorCodes, ErrorMessages, HTTPStatusCodes

router = APIRouter(prefix="/generate", tags=["palette-generation"])
palette_service = PaletteService()


@router.post("/random", response_model=PaletteResponse)
async def generate_random_palette(request: RandomPaletteRequest):
    """Generate a random harmonious color palette with support for locked colors."""
    try:
        result = palette_service.generate_random_palette(
            harmony_type=request.harmony_type,
            locked_colors=request.locked_colors
        )
        
        return PaletteResponse(**result)
        
    except Exception as e:
        print(f"❌ Error generating random palette: {e}")
        raise HTTPException(
            status_code=HTTPStatusCodes.INTERNAL_SERVER_ERROR,
            detail=f"{ErrorMessages.RANDOM_PALETTE_FAILED}: {str(e)}"
        )


@router.post("/concept", response_model=PaletteResponse)
async def generate_palette_from_concept(request: ConceptPaletteRequest):
    """Generate a color palette from a concept description using OpenAI."""
    try:
        result = await palette_service.generate_concept_palette(
            concept=request.concept,
            color_count=request.color_count
        )
        
        print_mem("after /generate/concept")
        
        return PaletteResponse(**result)
        
    except Exception as e:
        print(f"❌ Error in /generate/concept: {e}")
        raise HTTPException(
            status_code=HTTPStatusCodes.INTERNAL_SERVER_ERROR,
            detail=f"{ErrorMessages.CONCEPT_PALETTE_FAILED}: {str(e)}"
        )
