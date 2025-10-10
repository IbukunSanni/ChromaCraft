"""
Color processing routes for extraction, adjustment, and export.
Thin routes that delegate business logic to service layer.
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from typing import List

from services.color_service import ColorService
from routes.health import print_mem
from models import ColorExtractionResponse, ConceptAdjustmentResponse
from constants import ErrorCodes, ErrorMessages, HTTPStatusCodes

router = APIRouter(tags=["color-processing"])
color_service = ColorService()


@router.post("/extract-colors", response_model=ColorExtractionResponse)
async def extract_colors_endpoint(file: UploadFile = File(...)):
    """Extract dominant colors from an uploaded image."""
    try:
        image_data = await file.read()
        result = await color_service.extract_colors_from_image(image_data)
        
        return ColorExtractionResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatusCodes.BAD_REQUEST, 
            detail=f"{ErrorMessages.INVALID_IMAGE_FORMAT}: {str(e)}"
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=HTTPStatusCodes.INTERNAL_SERVER_ERROR, 
            detail=f"{ErrorMessages.IMAGE_PROCESSING_FAILED}: {str(e)}"
        )


@router.post("/adjust-concept", response_model=ConceptAdjustmentResponse)
async def adjust_concept_endpoint(
    concept: str = Form(...), base_colors: List[str] = Form(...)
):
    """Adjust palette colors based on a concept description."""
    try:
        result = await color_service.adjust_palette_by_concept(
            concept=concept,
            base_colors=base_colors
        )
        
        print_mem("after /adjust-concept")
        
        return ConceptAdjustmentResponse(**result)
        
    except Exception as e:
        print(f"❌ Error in /adjust-concept: {e}")
        raise HTTPException(
            status_code=HTTPStatusCodes.INTERNAL_SERVER_ERROR,
            detail=ErrorMessages.CONCEPT_ADJUSTMENT_FAILED
        )


@router.post("/export-png")
async def export_png(colors: List[str] = Form(...)):
    """Export a color palette as a PNG image."""
    try:
        image = color_service.generate_palette_image(colors)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="image/png")
        
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatusCodes.BAD_REQUEST, 
            detail=f"{ErrorMessages.EMPTY_COLOR_LIST}: {str(e)}"
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=HTTPStatusCodes.INTERNAL_SERVER_ERROR, 
            detail=f"{ErrorMessages.PNG_EXPORT_FAILED}: {str(e)}"
        )
