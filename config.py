import logging
import os

# Database configuration
DATABASE_URL = "sqlite:///./items.db"

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# API configuration
API_TITLE = "Items API"
API_DESCRIPTION = "A simple REST API for managing items"
API_VERSION = "1.0.0"