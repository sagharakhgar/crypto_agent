import requests
from typing import Dict
from config import COINMARKETCAP_API_KEY

class APITools:
    def __init__(self):
        pass
    
    def coinmarketcap_request(self, endpoint: str, params: Dict) -> Dict:
        """Make request to CoinMarketCap API"""
        url = f"https://pro-api.coinmarketcap.com/v1/{endpoint}"
        headers = {
            'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
            'Accept': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=20)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"CoinMarketCap API error: {e}")