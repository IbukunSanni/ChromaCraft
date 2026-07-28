"""
Color processing constants.
Eliminates magic numbers in color operations.
"""

class ColorConstants:
    """Constants for color processing operations."""
    
    # Color format constants
    RGB_MAX_VALUE = 255
    RGB_MIN_VALUE = 0
    HEX_COMPONENT_LENGTH = 2
    HEX_COLOR_LENGTH = 6
    HEX_COLOR_LENGTH_WITH_HASH = 7
    
    # HSL constants
    HUE_MAX_VALUE = 360.0
    SATURATION_MAX_VALUE = 1.0
    LIGHTNESS_MAX_VALUE = 1.0
    
    # Default palette sizes
    DEFAULT_PALETTE_SIZE = 5
    MIN_PALETTE_SIZE = 1
    MAX_PALETTE_SIZE = 10
    
    # Image processing constants
    DEFAULT_IMAGE_RESIZE_WIDTH = 100
    DEFAULT_IMAGE_RESIZE_HEIGHT = 100
    MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
    
    # Color extraction constants
    MIN_COLOR_EXTRACTION_COUNT = 3
    MAX_COLOR_EXTRACTION_COUNT = 8
    KMEANS_MAX_ITERATIONS = 100
    KMEANS_RANDOM_STATE = 42
    
    # Color harmony constants
    COMPLEMENTARY_HUE_OFFSET = 0.5  # 180 degrees in 0-1 scale
    TRIADIC_HUE_OFFSET = 1/3        # 120 degrees in 0-1 scale
    TETRADIC_HUE_OFFSET = 0.25      # 90 degrees in 0-1 scale
    ANALOGOUS_HUE_RANGE = 0.08      # ~30 degrees in 0-1 scale
    SPLIT_COMPLEMENTARY_OFFSET = 0.08
    
    # Color adjustment constants
    BRIGHTNESS_ADJUSTMENT_FACTOR = 0.4
    HUE_SHIFT_WARM_FACTOR = 0.03
    HUE_SHIFT_COOL_FACTOR = -0.03
    SATURATION_ADJUSTMENT_FACTOR = 0.5
    
    # Color validation patterns
    HEX_COLOR_PATTERN = r'^#[0-9A-Fa-f]{6}$'
    HEX_COLOR_SHORT_PATTERN = r'^#[0-9A-Fa-f]{3}$'
    
    # Supported image formats
    SUPPORTED_IMAGE_FORMATS = ['PNG', 'JPEG', 'JPG', 'BMP', 'GIF', 'TIFF', 'WEBP']
    SUPPORTED_IMAGE_MODES = ['RGB', 'RGBA', 'P', 'L']
    
    # Color space conversion constants
    SRGB_GAMMA = 2.4
    LINEAR_RGB_THRESHOLD = 0.04045
    LINEAR_RGB_SCALE = 12.92
    LINEAR_RGB_OFFSET = 0.055
    LINEAR_RGB_POWER = 2.4
    
    # Color difference thresholds
    MIN_COLOR_DISTANCE = 10.0
    SIMILAR_COLOR_THRESHOLD = 30.0
    DIFFERENT_COLOR_THRESHOLD = 50.0


class ColorNames:
    """Constants for color naming operations."""
    
    # Default fallback names
    DEFAULT_COLOR_NAME = "Unknown Color"
    FALLBACK_COLOR_NAMES = [
        "Color 1", "Color 2", "Color 3", "Color 4", "Color 5",
        "Color 6", "Color 7", "Color 8", "Color 9", "Color 10"
    ]
    
    # Color naming confidence thresholds
    HIGH_CONFIDENCE_THRESHOLD = 0.9
    MEDIUM_CONFIDENCE_THRESHOLD = 0.7
    LOW_CONFIDENCE_THRESHOLD = 0.5


class HarmonyTypes:
    """Valid color harmony types."""
    
    COMPLEMENTARY = "complementary"
    TRIADIC = "triadic"
    ANALOGOUS = "analogous"
    TETRADIC = "tetradic"
    MONOCHROMATIC = "monochromatic"
    SPLIT_COMPLEMENTARY = "split_complementary"
    RANDOM = "random"
    
    # All valid harmony types
    ALL_TYPES = [
        COMPLEMENTARY,
        TRIADIC,
        ANALOGOUS,
        TETRADIC,
        MONOCHROMATIC,
        SPLIT_COMPLEMENTARY,
        RANDOM
    ]


class PaletteQuality:
    """Constants for palette quality assessment."""
    
    # Harmony confidence thresholds
    EXCELLENT_HARMONY = 0.9
    GOOD_HARMONY = 0.7
    FAIR_HARMONY = 0.5
    POOR_HARMONY = 0.3
    
    # Quality descriptors
    QUALITY_EXCELLENT = "excellent"
    QUALITY_GOOD = "good"
    QUALITY_FAIR = "fair"
    QUALITY_POOR = "poor"
    
    QUALITY_THRESHOLDS = {
        QUALITY_EXCELLENT: EXCELLENT_HARMONY,
        QUALITY_GOOD: GOOD_HARMONY,
        QUALITY_FAIR: FAIR_HARMONY,
        QUALITY_POOR: POOR_HARMONY
    }