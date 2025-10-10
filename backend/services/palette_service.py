"""
Palette generation business logic service.
Handles all palette generation operations and business rules.
"""

import time
from typing import List, Optional, Dict, Any

from utils.color_harmony import (
    generate_random_harmonious_palette,
    validate_color_harmony,
)
from utils.find_closest_color_name import find_closest_color_name
from utils.openai_palette_generator import openai_generator
from mycolors.xkcd_colors import xkcd_colors


class PaletteService:
    """Service class for palette generation operations."""
    
    def __init__(self):
        """Initialize the palette service."""
        pass
    
    def generate_random_palette(
        self, 
        harmony_type: Optional[str] = None, 
        locked_colors: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate a random harmonious color palette with support for locked colors.
        
        Args:
            harmony_type: Type of harmony ('complementary', 'triadic', etc.)
            locked_colors: List of HEX colors to keep unchanged
            
        Returns:
            Dictionary containing colors, names, and harmony info
        """
        print(f"🎨 Generating random palette with harmony: {harmony_type}")
        print(f"🔒 Locked colors: {locked_colors}")

        # Generate the palette
        colors = generate_random_harmonious_palette(
            harmony_type=harmony_type, 
            locked_colors=locked_colors or []
        )

        # Get color names
        names = [find_closest_color_name(color, xkcd_colors) for color in colors]

        # Validate harmony
        harmony_type_final = harmony_type or "random"
        harmony_info = validate_color_harmony(colors, harmony_type_final)

        # Add locked colors info to harmony_info
        if locked_colors:
            harmony_info["locked_colors_count"] = len(locked_colors)
            harmony_info["locked_colors"] = locked_colors

        print(f"✅ Generated palette: {colors}")
        print(f"📊 Harmony validation: {harmony_info}")

        return {
            "colors": colors,
            "names": names,
            "harmony_info": harmony_info
        }
    
    async def generate_concept_palette(
        self, 
        concept: str, 
        color_count: int = 5
    ) -> Dict[str, Any]:
        """
        Generate a color palette from a concept description using OpenAI.
        
        Args:
            concept: Text description of the desired palette
            color_count: Number of colors to generate
            
        Returns:
            Dictionary containing colors, names, and harmony info
        """
        start_time = time.time()
        
        print(f"🤖 Generating palette for concept: '{concept}'")
        print(f"📊 Color count: {color_count}")
        
        # Generate palette using OpenAI
        result = await openai_generator.generate_palette_from_concept(
            concept=concept,
            color_count=color_count
        )
        
        # Add timestamp to metadata
        result["metadata"]["timestamp"] = time.time()
        
        # Create response in the same format as other endpoints
        colors = result["colors"]
        names = result["names"]
        
        # Additional harmony info from OpenAI
        harmony_info = {
            "type": result.get("harmony_type", "ai_generated"),
            "mood": result.get("mood", "generated"),
            "description": result.get("description", ""),
            "source": "openai",
            "model": result["metadata"]["model"]
        }
        
        generation_time = time.time() - start_time
        print(f"✅ Generated {len(colors)} colors in {generation_time:.2f}s")
        print(f"🎨 Colors: {colors}")
        print(f"💭 Original concept: {result.get('concept', 'N/A')}")
        
        return {
            "colors": colors,
            "names": names,
            "harmony_info": harmony_info,
            "generation_time": generation_time
        }