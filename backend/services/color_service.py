"""
Color processing business logic service.
Handles image color extraction, concept adjustment, and export operations.
"""

import time
import io
from typing import List, Dict, Any
from io import BytesIO

from PIL import Image, UnidentifiedImageError
from utils.color_extractor import extract_colors
from utils.png_exporter import generate_png_swatch
from utils.find_closest_color_name import find_closest_color_name
from utils.concept_adjuster import get_adjustment_weights, adjust_palette_by_concept
from mycolors.xkcd_colors import xkcd_colors


class ColorService:
    """Service class for color processing operations."""
    
    def __init__(self):
        """Initialize the color service."""
        pass
    
    async def extract_colors_from_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        Extract dominant colors from an image.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Dictionary containing extracted colors and names
            
        Raises:
            ValueError: If image is invalid or corrupted
            RuntimeError: If image processing fails
        """
        try:
            # Load and process image
            image = Image.open(io.BytesIO(image_data))

            # Normalize mode to RGB if needed
            if image.mode in ("RGBA", "P", "L"):
                image = image.convert("RGB")
            image = image.resize((100, 100))  # Optimize for processing

            # Save resized image into memory buffer
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            # Extract colors
            colors = extract_colors(buffer)
            
            # Get color names
            names = [find_closest_color_name(color, xkcd_colors) for color in colors]
            
            print(f"✅ Extracted {len(colors)} colors from image")
            
            return {
                "colors": colors,
                "names": names
            }
            
        except UnidentifiedImageError as e:
            raise ValueError("Invalid or corrupted image file") from e
        except Exception as e:
            raise RuntimeError(f"Image processing failed: {str(e)}") from e
    
    async def adjust_palette_by_concept(
        self, 
        concept: str, 
        base_colors: List[str]
    ) -> Dict[str, Any]:
        """
        Adjust palette colors based on a concept description.
        
        Args:
            concept: Text description for adjustment direction
            base_colors: List of base HEX colors to adjust
            
        Returns:
            Dictionary containing adjusted colors and names
        """
        start_time = time.time()
        
        print(f"🎯 Adjusting concept: '{concept}' for {len(base_colors)} colors")

        # Get concept adjustment weights
        weights = await get_adjustment_weights(concept)
        
        # Apply concept-based adjustments
        adjusted_colors = adjust_palette_by_concept(base_colors, weights)
        
        # Get names for adjusted colors
        names = [find_closest_color_name(color, xkcd_colors) for color in adjusted_colors]

        processing_time = time.time() - start_time
        print(f"✅ Concept adjustment completed in {processing_time:.2f}s")

        return {
            "adjusted_colors": adjusted_colors,
            "names": names,
            "processing_time": processing_time,
            "concept": concept,
            "weights": weights
        }
    
    def generate_palette_image(self, colors: List[str]) -> Image.Image:
        """
        Generate a PNG image from a color palette.
        
        Args:
            colors: List of HEX color strings
            
        Returns:
            PIL Image object
            
        Raises:
            ValueError: If colors list is empty
            RuntimeError: If image generation fails
        """
        try:
            if not colors:
                raise ValueError("Colors list cannot be empty")
                
            image = generate_png_swatch(colors)
            
            print(f"✅ Generated palette image with {len(colors)} colors")
            
            return image
            
        except Exception as e:
            raise RuntimeError(f"Image generation failed: {str(e)}") from e