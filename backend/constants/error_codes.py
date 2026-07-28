"""
Error codes and messages for ChromaCraft backend.
Centralizes all error handling constants.
"""

from enum import Enum


class ErrorCodes:
    """Error codes for different types of failures."""
    
    # General errors
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    
    # Palette generation errors
    PALETTE_GENERATION_FAILED = "PALETTE_GENERATION_FAILED"
    RANDOM_PALETTE_FAILED = "RANDOM_PALETTE_FAILED"
    CONCEPT_PALETTE_FAILED = "CONCEPT_PALETTE_FAILED"
    HARMONY_VALIDATION_FAILED = "HARMONY_VALIDATION_FAILED"
    
    # Color processing errors
    IMAGE_PROCESSING_FAILED = "IMAGE_PROCESSING_FAILED"
    INVALID_IMAGE_FORMAT = "INVALID_IMAGE_FORMAT"
    CORRUPTED_IMAGE_FILE = "CORRUPTED_IMAGE_FILE"
    COLOR_EXTRACTION_FAILED = "COLOR_EXTRACTION_FAILED"
    CONCEPT_ADJUSTMENT_FAILED = "CONCEPT_ADJUSTMENT_FAILED"
    PNG_EXPORT_FAILED = "PNG_EXPORT_FAILED"
    EMPTY_COLOR_LIST = "EMPTY_COLOR_LIST"
    
    # AI/OpenAI errors
    OPENAI_API_ERROR = "OPENAI_API_ERROR"
    OPENAI_RATE_LIMIT = "OPENAI_RATE_LIMIT"
    OPENAI_TIMEOUT = "OPENAI_TIMEOUT"
    OPENAI_CONNECTION_ERROR = "OPENAI_CONNECTION_ERROR"
    OPENAI_INVALID_RESPONSE = "OPENAI_INVALID_RESPONSE"
    OPENAI_CONFIG_ERROR = "OPENAI_CONFIG_ERROR"
    
    # Concept processing errors
    CONCEPT_TOO_LONG = "CONCEPT_TOO_LONG"
    CONCEPT_EMPTY = "CONCEPT_EMPTY"
    CONCEPT_PROCESSING_FAILED = "CONCEPT_PROCESSING_FAILED"
    
    # Color validation errors
    INVALID_HEX_COLOR = "INVALID_HEX_COLOR"
    INVALID_COLOR_COUNT = "INVALID_COLOR_COUNT"
    UNSUPPORTED_HARMONY_TYPE = "UNSUPPORTED_HARMONY_TYPE"


class ErrorMessages:
    """Human-readable error messages corresponding to error codes."""
    
    # General errors
    INTERNAL_SERVER_ERROR = "An internal server error occurred"
    VALIDATION_ERROR = "Request validation failed"
    
    # Palette generation errors
    PALETTE_GENERATION_FAILED = "Failed to generate color palette"
    RANDOM_PALETTE_FAILED = "Random palette generation failed"
    CONCEPT_PALETTE_FAILED = "Concept-based palette generation failed"
    HARMONY_VALIDATION_FAILED = "Color harmony validation failed"
    
    # Color processing errors
    IMAGE_PROCESSING_FAILED = "Image processing failed"
    INVALID_IMAGE_FORMAT = "Invalid or unsupported image format"
    CORRUPTED_IMAGE_FILE = "Image file is corrupted or unreadable"
    COLOR_EXTRACTION_FAILED = "Failed to extract colors from image"
    CONCEPT_ADJUSTMENT_FAILED = "Failed to adjust palette based on concept"
    PNG_EXPORT_FAILED = "Failed to generate PNG image"
    EMPTY_COLOR_LIST = "Color list cannot be empty"
    
    # AI/OpenAI errors
    OPENAI_API_ERROR = "OpenAI API request failed"
    OPENAI_RATE_LIMIT = "OpenAI API rate limit exceeded"
    OPENAI_TIMEOUT = "OpenAI API request timed out"
    OPENAI_CONNECTION_ERROR = "Failed to connect to OpenAI API"
    OPENAI_INVALID_RESPONSE = "Received invalid response from OpenAI"
    OPENAI_CONFIG_ERROR = "OpenAI configuration error"
    
    # Concept processing errors
    CONCEPT_TOO_LONG = "Concept description is too long"
    CONCEPT_EMPTY = "Concept description cannot be empty"
    CONCEPT_PROCESSING_FAILED = "Failed to process concept description"
    
    # Color validation errors
    INVALID_HEX_COLOR = "Invalid HEX color format"
    INVALID_COLOR_COUNT = "Invalid color count specified"
    UNSUPPORTED_HARMONY_TYPE = "Unsupported color harmony type"


class ErrorSeverity(Enum):
    """Error severity levels for logging and monitoring."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# Error code to severity mapping
ERROR_SEVERITY_MAP = {
    # Critical errors
    ErrorCodes.INTERNAL_SERVER_ERROR: ErrorSeverity.CRITICAL,
    ErrorCodes.OPENAI_CONFIG_ERROR: ErrorSeverity.CRITICAL,
    
    # High severity
    ErrorCodes.OPENAI_API_ERROR: ErrorSeverity.HIGH,
    ErrorCodes.OPENAI_CONNECTION_ERROR: ErrorSeverity.HIGH,
    ErrorCodes.PALETTE_GENERATION_FAILED: ErrorSeverity.HIGH,
    
    # Medium severity
    ErrorCodes.IMAGE_PROCESSING_FAILED: ErrorSeverity.MEDIUM,
    ErrorCodes.CONCEPT_ADJUSTMENT_FAILED: ErrorSeverity.MEDIUM,
    ErrorCodes.OPENAI_TIMEOUT: ErrorSeverity.MEDIUM,
    ErrorCodes.OPENAI_RATE_LIMIT: ErrorSeverity.MEDIUM,
    
    # Low severity
    ErrorCodes.VALIDATION_ERROR: ErrorSeverity.LOW,
    ErrorCodes.INVALID_IMAGE_FORMAT: ErrorSeverity.LOW,
    ErrorCodes.CONCEPT_TOO_LONG: ErrorSeverity.LOW,
    ErrorCodes.EMPTY_COLOR_LIST: ErrorSeverity.LOW,
}