"""
Core configuration management
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
    FAL_KEY = os.getenv("FAL_KEY")
    
    # Instagram
    INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID")
    
    # Database
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/database.db")
    
    # Image Generation
    IMAGE_GENERATOR = os.getenv("IMAGE_GENERATOR", "replicate")
    IMAGE_WIDTH = int(os.getenv("IMAGE_WIDTH", 1080))
    IMAGE_HEIGHT = int(os.getenv("IMAGE_HEIGHT", 1920))
    
    # Paths
    STORIES_DIR = "data/stories"
    IMAGES_DIR = "data/images"
    WEBTOONS_DIR = "data/webtoons"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = [
            "ANTHROPIC_API_KEY",
            "REPLICATE_API_TOKEN",
        ]
        
        missing = [key for key in required if not getattr(cls, key)]
        
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")
        
        return True
