import requests
from config import COINMARKETCAP_API_KEY

class RealCoinMarketCapTools:
    def __init__(self):
        self.base_url = "https://pro-api.coinmarketcap.com/v1/"
        self.headers = {'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY}
        self.coins_cache = None
    
    def get_all_coins(self):
        """Get all coins from CoinMarketCap"""
        if self.coins_cache is None:
            try:
                url = f"{self.base_url}cryptocurrency/map"
                params = {'limit': 5000}
                response = requests.get(url, headers=self.headers, params=params, timeout=20)
                if response.status_code == 200:
                    self.coins_cache = response.json()['data']
                else:
                    print(f"API Error: {response.status_code}")
                    self.coins_cache = []
            except Exception as e:
                print(f"Error fetching coins: {e}")
                self.coins_cache = []
        return self.coins_cache
    
    def find_coin_info(self, coin_name):
        """Find coin information by name or symbol"""
        coins = self.get_all_coins()
        if not coins:
            return None
            
        coin_lower = coin_name.lower()
        
        # Exact matches
        for coin in coins:
            if (coin['name'].lower() == coin_lower or 
                coin['symbol'].lower() == coin_lower or
                coin['slug'].lower() == coin_lower):
                return coin
        
        # Partial matches
        for coin in coins:
            if (coin_lower in coin['name'].lower() or 
                coin_lower in coin['symbol'].lower()):
                return coin
        
        return None
    
    def get_real_time_data(self, coin_id):
        """Get real-time data for coin"""
        try:
            url = f"{self.base_url}cryptocurrency/quotes/latest"
            params = {'id': coin_id, 'convert': 'USD'}
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return data['data'][str(coin_id)]
            else:
                print(f"API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching real-time data: {e}")
            return None