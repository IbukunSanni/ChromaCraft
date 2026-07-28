"""
AI and machine learning constants.
Eliminates magic numbers in AI/ML operations.
"""

class AIConstants:
    """Constants for AI processing operations."""
    
    # OpenAI API constants
    DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
    FALLBACK_OPENAI_MODEL = "gpt-3.5-turbo"
    MAX_OPENAI_TOKENS = 500
    DEFAULT_TEMPERATURE = 0.7
    MAX_CONCEPT_LENGTH = 200
    MIN_CONCEPT_LENGTH = 1
    
    # Retry configuration
    MAX_RETRIES = 4
    RETRY_DELAYS = [1, 2, 4, 8]  # Exponential backoff in seconds
    JITTER_MAX = 1.0  # Maximum jitter to add to delays
    
    # Rate limiting
    DEFAULT_MAX_REQUESTS_PER_MINUTE = 60
    OPENAI_RATE_LIMIT_BUFFER = 0.1  # 10% buffer for rate limiting
    
    # Response validation
    MIN_COLORS_IN_RESPONSE = 1
    MAX_COLORS_IN_RESPONSE = 10
    REQUIRED_RESPONSE_FIELDS = ["colors", "names"]
    
    # Concept processing
    CONCEPT_ENCODING_MODEL = "paraphrase-albert-small-v2"
    CONCEPT_SIMILARITY_THRESHOLD = 0.5
    
    # Reference concept encodings for mood adjustment
    REFERENCE_CONCEPTS = [
        "bright", "dark", "warm", "cool", 
        "saturated", "desaturated", "vibrant", "muted"
    ]
    
    # Mood adjustment weights
    MOOD_WEIGHT_THRESHOLD = 0.5
    BRIGHTNESS_FACTOR = 0.4
    HUE_SHIFT_FACTOR = 0.03
    SATURATION_FACTOR_RANGE = 0.5
    
    # Memory management
    ENABLE_MEMORY_TRACKING = True
    MEMORY_WARNING_THRESHOLD_MB = 1000  # 1GB
    MEMORY_CRITICAL_THRESHOLD_MB = 2000  # 2GB


class ModelConstants:
    """Constants for machine learning models."""
    
    # Sentence transformer model
    SENTENCE_TRANSFORMER_MODEL = "paraphrase-albert-small-v2"
    SENTENCE_TRANSFORMER_DEVICE = "cpu"  # Use CPU for consistency
    
    # Embedding dimensions
    CONCEPT_EMBEDDING_DIM = 768  # ALBERT small embedding size
    
    # Similarity computation
    COSINE_SIMILARITY_THRESHOLD = 0.7
    EUCLIDEAN_DISTANCE_THRESHOLD = 0.5
    
    # Batch processing
    MAX_BATCH_SIZE = 32
    DEFAULT_BATCH_SIZE = 8


class OpenAIConstants:
    """OpenAI-specific constants."""
    
    # Model configurations
    MODELS = {
        "gpt-4o-mini": {
            "max_tokens": 4096,
            "cost_per_1k_tokens": 0.0015,
            "supports_json_mode": True
        },
        "gpt-4o": {
            "max_tokens": 8192,
            "cost_per_1k_tokens": 0.03,
            "supports_json_mode": True
        },
        "gpt-3.5-turbo": {
            "max_tokens": 4096,
            "cost_per_1k_tokens": 0.002,
            "supports_json_mode": True
        }
    }
    
    # API timeouts (in seconds)
    DEFAULT_TIMEOUT = 30
    LONG_REQUEST_TIMEOUT = 60
    CONNECTION_TIMEOUT = 10
    
    # Response format
    JSON_RESPONSE_FORMAT = {"type": "json_object"}
    
    # Error handling
    RETRYABLE_ERRORS = [
        "rate_limit_exceeded",
        "timeout",
        "connection_error",
        "server_error"
    ]
    
    # Prompt engineering constants
    SYSTEM_MESSAGE_MAX_LENGTH = 2000
    USER_MESSAGE_MAX_LENGTH = 1000
    PALETTE_DESCRIPTION_MAX_LENGTH = 500


class ConceptConstants:
    """Constants for concept processing."""
    
    # Concept categories
    MOOD_CONCEPTS = [
        "happy", "sad", "energetic", "calm", "peaceful", "intense",
        "mysterious", "bright", "dark", "warm", "cool", "playful"
    ]
    
    NATURE_CONCEPTS = [
        "ocean", "forest", "desert", "mountain", "sky", "sunset",
        "sunrise", "autumn", "spring", "winter", "summer"
    ]
    
    EMOTION_CONCEPTS = [
        "love", "anger", "joy", "fear", "surprise", "disgust",
        "trust", "anticipation", "excitement", "serenity"
    ]
    
    # Concept validation
    MIN_CONCEPT_WORDS = 1
    MAX_CONCEPT_WORDS = 20
    BLOCKED_CONCEPTS = []  # Add inappropriate concepts here
    
    # Concept processing weights
    CONCEPT_WEIGHT_MULTIPLIER = 1.0
    CONCEPT_BOOST_FACTOR = 1.2
    CONCEPT_PENALTY_FACTOR = 0.8