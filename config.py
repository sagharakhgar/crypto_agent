import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
COINMARKETCAP_API_KEY = os.getenv('COINMARKETCAP_API_KEY')

# API URLs
COINMARKETCAP_BASE_URL = "https://pro-api.coinmarketcap.com/v1/"
DEFILLAMA_BASE_URL = "https://api.llama.fi/"

# Settings
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3

def validate_config():
    """Validate API configuration"""
    if not COINMARKETCAP_API_KEY:
        print("❌ COINMARKETCAP_API_KEY not found in .env file")
        return False
    
    print("✅ Configuration loaded successfully")
    return True