import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60"))

    # CORS
    # Comma-separated list of exact origins allowed to call the API.
    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:3000,"
            "http://127.0.0.1:3000,"
            "https://color-palette-extractor.vercel.app",
        ).split(",")
        if origin.strip()
    ]
    # Regex for additional origins, e.g. Vercel preview deployments such as
    # https://color-palette-extractor-<hash>-<team>.vercel.app.
    # Wildcards inside ALLOWED_ORIGINS are not supported by CORSMiddleware.
    ALLOWED_ORIGIN_REGEX = os.getenv(
        "ALLOWED_ORIGIN_REGEX",
        r"https://color-palette-extractor(-[a-z0-9-]+)?\.vercel\.app",
    ) or None
    
    @classmethod
    def validate_openai_config(cls):
        """Validate that OpenAI is properly configured"""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please create a .env file based on .env.example"
            )
        return True