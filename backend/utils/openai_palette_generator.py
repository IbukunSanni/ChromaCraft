import openai
import json
import re
import asyncio
import random
from typing import List, Dict, Any
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MAX_CONCEPT_LENGTH = 200
RETRY_DELAYS = [1, 2, 4, 8]  # Exponential backoff delays in seconds
MAX_RETRIES = len(RETRY_DELAYS)

class OpenAIPaletteGenerator:
    def __init__(self):
        # Validate configuration on initialization
        Config.validate_openai_config()
        
        # Initialize OpenAI client
        self.client = openai.AsyncOpenAI(
            api_key=Config.OPENAI_API_KEY
        )
        self.model = Config.OPENAI_MODEL
    
    def validate_concept(self, concept: str) -> str:
        """Validate and clean the concept input"""
        if not concept or not concept.strip():
            raise ValueError("Concept cannot be empty")
        
        concept = concept.strip()
        
        if len(concept) > MAX_CONCEPT_LENGTH:
            raise ValueError(f"Concept must be {MAX_CONCEPT_LENGTH} characters or less. Current length: {len(concept)}")
        
        return concept
    
    async def generate_palette_from_concept(
        self, 
        concept: str, 
        color_count: int = 5
    ) -> Dict[str, Any]:
        """
        Generate a color palette from a concept description using OpenAI.
        
        Args:
            concept: Text description (e.g., "sunset over the ocean", max 200 chars)
            color_count: Number of colors to generate (default: 5)
            
        Returns:
            Dict containing colors, names, metadata, and original concept
        """
        try:
            # Validate concept input
            concept = self.validate_concept(concept)
            logger.info(f"🎨 Generating palette for concept: '{concept}'")
            
            # Build the system message for color generation
            system_message = self._build_system_message(color_count)
            
            # Build the user message
            user_message = self._build_user_message(concept, color_count)
            
            # Call OpenAI API with retry logic
            response = await self._call_openai_with_retry(
                system_message, user_message
            )
            
            # Parse the response
            result = self._parse_openai_response(response, concept)
            
            logger.info(f"✅ Generated {len(result['colors'])} colors for concept: '{concept}'")
            return result
            
        except ValueError as e:
            logger.error(f"❌ Validation error: {e}")
            raise Exception(str(e))
        except openai.APIError as e:
            logger.error(f"❌ OpenAI API error: {e}")
            raise Exception(f"OpenAI API error: {str(e)}")
        except Exception as e:
            logger.error(f"❌ Error generating palette: {e}")
            raise Exception(f"Palette generation failed: {str(e)}")
    
    async def _call_openai_with_retry(self, system_message: str, user_message: str):
        """Call OpenAI API with exponential backoff retry logic"""
        last_exception = None
        
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"🔄 OpenAI API call attempt {attempt + 1}/{MAX_RETRIES}")
                
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.7,  # Some creativity, but not too random
                    max_tokens=500,
                    response_format={"type": "json_object"}
                )
                
                logger.info(f"✅ OpenAI API call successful on attempt {attempt + 1}")
                return response
                
            except openai.RateLimitError as e:
                logger.warning(f"⏳ Rate limit hit on attempt {attempt + 1}: {e}")
                last_exception = e
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAYS[attempt] + random.uniform(0, 1)  # Add jitter
                    logger.info(f"🔄 Retrying in {delay:.1f} seconds...")
                    await asyncio.sleep(delay)
                
            except openai.APITimeoutError as e:
                logger.warning(f"⏰ Timeout on attempt {attempt + 1}: {e}")
                last_exception = e
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAYS[attempt]
                    logger.info(f"🔄 Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                    
            except openai.APIConnectionError as e:
                logger.warning(f"🔌 Connection error on attempt {attempt + 1}: {e}")
                last_exception = e
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAYS[attempt]
                    logger.info(f"🔄 Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                    
            except openai.InternalServerError as e:
                logger.warning(f"🔧 Server error on attempt {attempt + 1}: {e}")
                last_exception = e
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAYS[attempt]
                    logger.info(f"🔄 Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                # For unexpected errors, don't retry
                logger.error(f"❌ Unexpected error on attempt {attempt + 1}: {e}")
                raise e
        
        # If all retries failed, raise the last exception
        logger.error(f"❌ All {MAX_RETRIES} retry attempts failed")
        raise last_exception or Exception("OpenAI API call failed after all retries")
    
    def _build_system_message(self, color_count: int) -> str:
        """Build the system message for GPT"""
        return f"""You are a professional color palette designer and artist. Your job is to create beautiful, harmonious color palettes based on concept descriptions.

RULES:
1. Generate exactly {color_count} colors in hex format (#RRGGBB)
2. Colors should be harmonious and work well together
3. Consider color theory (complementary, analogous, triadic, etc.)
4. Provide meaningful, descriptive names for each color
5. Ensure colors are accessible and visually appealing

OUTPUT FORMAT (JSON):
{{
    "colors": ["#FF5733", "#33FF57", "#3357FF"],
    "names": ["Sunset Orange", "Ocean Green", "Sky Blue"],
    "harmony_type": "triadic",
    "mood": "vibrant and energetic",
    "description": "Brief description of the palette inspiration"
}}

IMPORTANT: Always return valid JSON. Hex colors must be uppercase and exactly 7 characters (#RRGGBB)."""
    
    def _build_user_message(self, concept: str, color_count: int) -> str:
        """Build the user message with the specific concept"""
        return f"""Create a {color_count}-color palette inspired by: '{concept}'

Consider the emotions, objects, lighting, and atmosphere this concept evokes. Return your response as JSON."""
    
    def _parse_openai_response(self, response, original_concept: str) -> Dict[str, Any]:
        """Parse and validate the OpenAI response"""
        try:
            # Extract the JSON content
            content = response.choices[0].message.content
            result = json.loads(content)
            
            # Validate required fields
            if not all(key in result for key in ["colors", "names"]):
                raise ValueError("Missing required fields in OpenAI response")
            
            colors = result["colors"]
            names = result["names"]
            
            # Validate colors format
            validated_colors = self._validate_and_fix_colors(colors)
            
            # Ensure we have matching lengths
            if len(validated_colors) != len(names):
                # Pad names if necessary
                while len(names) < len(validated_colors):
                    names.append(f"Color {len(names) + 1}")
                names = names[:len(validated_colors)]
            
            return {
                "colors": validated_colors,
                "names": names,
                "harmony_type": result.get("harmony_type", "custom"),
                "mood": result.get("mood", "generated"),
                "description": result.get("description", "AI-generated palette"),
                "concept": original_concept,  # Return the original concept
                "metadata": {
                    "source": "openai",
                    "model": self.model,
                    "original_concept": original_concept,
                    "timestamp": None  # Will be added by the API endpoint
                }
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse JSON from OpenAI: {e}")
            # Fallback: try to extract hex colors from text
            return self._fallback_color_extraction(response.choices[0].message.content, original_concept)
        except Exception as e:
            logger.error(f"❌ Error parsing OpenAI response: {e}")
            raise Exception(f"Failed to parse OpenAI response: {str(e)}")
    
    def _validate_and_fix_colors(self, colors: List[str]) -> List[str]:
        """Validate and fix hex color format"""
        validated_colors = []
        
        for color in colors:
            # Remove whitespace and ensure # prefix
            color = color.strip()
            if not color.startswith('#'):
                color = '#' + color
            
            # Validate hex format
            if re.match(r'^#[0-9A-Fa-f]{6}$', color):
                validated_colors.append(color.upper())
            else:
                logger.warning(f"⚠️  Invalid color format: {color}, skipping")
        
        if len(validated_colors) == 0:
            raise ValueError("No valid colors found in OpenAI response")
            
        return validated_colors
    
    def _fallback_color_extraction(self, content: str, original_concept: str) -> Dict[str, Any]:
        """Fallback method to extract colors from text if JSON parsing fails"""
        logger.info("🔄 Attempting fallback color extraction")
        
        # Look for hex colors in the text
        hex_pattern = r'#[0-9A-Fa-f]{6}'
        colors = re.findall(hex_pattern, content)
        
        if not colors:
            # Generate some default colors if nothing found
            logger.warning("⚠️  No colors found in OpenAI response, using defaults")
            colors = ["#FF5733", "#33FF57", "#3357FF", "#FF33F5", "#33F5FF"]
        
        colors = [color.upper() for color in colors[:5]]  # Limit to 5 colors
        names = [f"Color {i+1}" for i in range(len(colors))]
        
        return {
            "colors": colors,
            "names": names,
            "harmony_type": "unknown",
            "mood": "fallback",
            "description": f"Fallback palette for: {original_concept}",
            "concept": original_concept,
            "metadata": {
                "source": "openai_fallback",
                "model": self.model,
                "original_concept": original_concept,
                "timestamp": None
            }
        }

# Global instance
openai_generator = OpenAIPaletteGenerator()