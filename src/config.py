"""Configuration settings for the TED Talk processing application."""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration class."""
    
    # API Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    TAVILY_API_KEY: str = os.getenv('TAVILY_API_KEY', '')
    
    # Model Configuration
    CHAT_MODEL: str = os.getenv('CHAT_MODEL', 'gpt-5')
    TTS_MODEL: str = os.getenv('TTS_MODEL', 'tts-1-hd')
    TTS_VOICE: str = os.getenv('TTS_VOICE', 'alloy')
    IMAGE_MODEL: str = os.getenv('IMAGE_MODEL', 'dall-e-3')
    IMAGE_SIZE: str = os.getenv('IMAGE_SIZE', '1792x1024')  # type: ignore
    
    # File Paths
    DATA_DIR: str = os.getenv('DATA_DIR', 'media')
    TRANSCRIPT_PATH: str = os.path.join(DATA_DIR, 'transcript')
    AUDIO_PATH: str = os.path.join(DATA_DIR, 'narrative.mp3')
    IMAGE_PATH: str = os.path.join(DATA_DIR, 'artwork.png')

    # Search Configuration
    MAX_SEARCH_RESULTS: int = int(os.getenv('MAX_SEARCH_RESULTS', '1'))
    SEARCH_QUERIES_COUNT: int = int(os.getenv('SEARCH_QUERIES_COUNT', '5'))
    
    # Display Configuration
    TEXT_WIDTH: int = int(os.getenv('TEXT_WIDTH', '80'))
    
    # Cache Configuration
    CACHE_SIZE: int = int(os.getenv('CACHE_SIZE', '10'))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        required_keys = ['OPENAI_API_KEY', 'TAVILY_API_KEY']
        missing_keys = [key for key in required_keys if not getattr(cls, key)]
        
        if missing_keys:
            raise ValueError(f"Missing required configuration: {', '.join(missing_keys)}")
        
        return True

config = Config()
