import requests
from typing import Optional, List, Dict
import time

class UniversalDefiLlamaTools:
    def __init__(self):
        self.base_url = "https://api.llama.fi/"
        self.protocols_cache = None
        self.last_fetch_time = 0
        self.cache_duration = 3600
    
    def _get_protocols_with_cache(self):
        """Get protocols with caching"""
        current_time = time.time()
        
        if (self.protocols_cache is None or 
            current_time - self.last_fetch_time > self.cache_duration):
            try:
                print("🔄 Fetching protocols from DefiLlama...")
                response = requests.get(f"{self.base_url}protocols", timeout=25)
                if response.status_code == 200:
                    self.protocols_cache = response.json()
                    self.last_fetch_time = current_time
                    print(f"✅ Loaded {len(self.protocols_cache)} protocols")
                else:
                    print(f"❌ Failed to fetch protocols: {response.status_code}")
                    self.protocols_cache = []
            except Exception as e:
                print(f"❌ Error fetching protocols: {e}")
                self.protocols_cache = []
        
        return self.protocols_cache or []
    
    def get_tvl_data(self, coin_name: str, symbol: str = "") -> Dict:
        """Get TVL data with multiple strategies"""
        print(f"🔍 Searching TVL for: {coin_name} ({symbol})")
        
        tvl_result = {
            'tvl': 0,
            'tvl_formatted': 'Not available',
            'has_tvl': False,
            'source': 'DefiLlama',
            'method': 'Not found'
        }
        
        try:
            protocols = self._get_protocols_with_cache()
            if not protocols:
                return tvl_result
            
            coin_lower = coin_name.lower().strip()
            symbol_lower = symbol.lower().strip() if symbol else ""
            
            # Strategy 1: Direct match from common mappings
            common_mappings = {
                'bitcoin': 'bitcoin', 'btc': 'bitcoin',
                'ethereum': 'ethereum', 'eth': 'ethereum',
                'binance coin': 'binancecoin', 'bnb': 'binancecoin',
                'ripple': 'ripple', 'xrp': 'ripple',
                'cardano': 'cardano', 'ada': 'cardano',
                'solana': 'solana', 'sol': 'solana',
                'polkadot': 'polkadot', 'dot': 'polkadot',
                'dogecoin': 'dogecoin', 'doge': 'dogecoin',
                'avalanche': 'avalanche', 'avax': 'avalanche',
                'chainlink': 'chainlink', 'link': 'chainlink',
                'uniswap': 'uniswap', 'uni': 'uniswap',
                'aave': 'aave', 'compound': 'compound', 'comp': 'compound',
                'polygon': 'matic-network', 'matic': 'matic-network',
                'litecoin': 'litecoin', 'ltc': 'litecoin',
                'cosmos': 'cosmos', 'atom': 'cosmos',
            }
            
            # Check common mappings first
            if coin_lower in common_mappings:
                protocol_slug = common_mappings[coin_lower]
                tvl = self._get_tvl_by_slug(protocol_slug)
                if tvl > 0:
                    tvl_result.update({
                        'tvl': tvl,
                        'tvl_formatted': f"${tvl:,.0f}",
                        'has_tvl': True,
                        'method': 'Common mapping'
                    })
                    return tvl_result
            
            if symbol_lower in common_mappings:
                protocol_slug = common_mappings[symbol_lower]
                tvl = self._get_tvl_by_slug(protocol_slug)
                if tvl > 0:
                    tvl_result.update({
                        'tvl': tvl,
                        'tvl_formatted': f"${tvl:,.0f}",
                        'has_tvl': True,
                        'method': 'Symbol mapping'
                    })
                    return tvl_result
            
            # Strategy 2: Search in protocols list
            for protocol in protocols:
                protocol_name = protocol.get('name', '').lower()
                protocol_symbol = protocol.get('symbol', '').lower()
                protocol_slug = protocol.get('slug', '').lower()
                
                if (protocol_name == coin_lower or 
                    protocol_symbol == coin_lower or 
                    protocol_slug == coin_lower or
                    (symbol_lower and protocol_symbol == symbol_lower)):
                    
                    tvl = protocol.get('tvl', 0)
                    if tvl > 0:
                        print(f"✅ TVL found in protocols list: ${tvl:,.0f}")
                        tvl_result.update({
                            'tvl': tvl,
                            'tvl_formatted': f"${tvl:,.0f}",
                            'has_tvl': True,
                            'method': 'Protocols list match'
                        })
                        return tvl_result
            
            # Strategy 3: Partial matching
            for protocol in protocols:
                protocol_name = protocol.get('name', '').lower()
                if coin_lower in protocol_name:
                    tvl = protocol.get('tvl', 0)
                    if tvl > 0:
                        print(f"✅ TVL found with partial match: ${tvl:,.0f}")
                        tvl_result.update({
                            'tvl': tvl,
                            'tvl_formatted': f"${tvl:,.0f}",
                            'has_tvl': True,
                            'method': 'Partial match'
                        })
                        return tvl_result
            
            print("ℹ️ No TVL data found")
            return tvl_result
            
        except Exception as e:
            print(f"❌ TVL search error: {e}")
            return tvl_result
    
    def _get_tvl_by_slug(self, protocol_slug: str) -> float:
        """Get TVL by protocol slug"""
        try:
            # First try to get from protocols list
            protocols = self._get_protocols_with_cache()
            for protocol in protocols:
                if protocol.get('slug') == protocol_slug:
                    tvl = protocol.get('tvl', 0)
                    if tvl > 0:
                        return tvl
            
            # Fallback: try detailed protocol endpoint
            response = requests.get(f"{self.base_url}protocol/{protocol_slug}", timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                # Try different TVL data structures
                if 'currentChainTvls' in data and data['currentChainTvls']:
                    return sum(data['currentChainTvls'].values())
                
                if 'tvl' in data and isinstance(data['tvl'], list) and data['tvl']:
                    latest = data['tvl'][-1]
                    return latest.get('totalLiquidityUSD', latest.get('tvl', 0))
                
                if 'tvl' in data and isinstance(data['tvl'], (int, float)):
                    return data['tvl']
            
            return 0
            
        except Exception as e:
            print(f"Error getting TVL for {protocol_slug}: {e}")
            return 0