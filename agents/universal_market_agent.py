from tools.real_cmc_tools import RealCoinMarketCapTools
from tools.universal_defillama import UniversalDefiLlamaTools
from tools.custom_tools import DataAnalysisTools

class UniversalMarketAgent:
    def __init__(self):
        self.cmc_tools = RealCoinMarketCapTools()
        self.defillama_tools = UniversalDefiLlamaTools()
        self.analysis_tools = DataAnalysisTools()
    
    def get_universal_market_data(self, coin_name):
        """Get comprehensive market data for any cryptocurrency"""
        print(f"🔍 Starting analysis for: {coin_name}")
        
        # Find coin in CoinMarketCap
        coin_info = self.cmc_tools.find_coin_info(coin_name)
        if not coin_info:
            return {"error": f"Cryptocurrency '{coin_name}' not found on CoinMarketCap"}
        
        coin_id = coin_info['id']
        actual_name = coin_info['name']
        symbol = coin_info['symbol']
        
        print(f"✅ Found: {actual_name} ({symbol})")
        
        # Get real-time data
        real_time_data = self.cmc_tools.get_real_time_data(coin_id)
        if not real_time_data:
            return {"error": f"Could not fetch data for {actual_name}"}
        
        print("📊 Successfully fetched market data")
        
        # Get TVL data
        tvl_data = self.defillama_tools.get_tvl_data(actual_name, symbol)
        
        # Process all data
        market_data = self._process_comprehensive_data(real_time_data, tvl_data)
        
        return market_data
    
    def _process_comprehensive_data(self, real_time_data, tvl_data):
        """Process and format all market data"""
        quote = real_time_data['quote']['USD']
        
        # Basic market data
        market_cap = quote.get('market_cap', 0)
        price = quote.get('price', 0)
        volume_24h = quote.get('volume_24h', 0)
        
        # Supply data
        circulating_supply = real_time_data.get('circulating_supply')
        total_supply = real_time_data.get('total_supply')
        max_supply = real_time_data.get('max_supply')
        
        # Advanced calculations
        fdv_analysis = self.analysis_tools.calculate_fully_diluted_valuation(price, total_supply)
        inflation_analysis = self.analysis_tools.analyze_inflation_rate(circulating_supply, total_supply, max_supply)
        
        # TVL/MC ratio calculation
        tvl_mcap_ratio = None
        tvl_analysis = {'ratio': 0, 'interpretation': 'No TVL data', 'risk_level': 'Unknown'}
        
        if market_cap and tvl_data['has_tvl'] and tvl_data['tvl'] > 0:
            tvl_mcap_ratio = (tvl_data['tvl'] / market_cap) * 100
            tvl_analysis = self.analysis_tools.calculate_tvl_mcap_ratio(tvl_data['tvl'], market_cap)
        
        return {
            # Basic Information
            'name': real_time_data['name'],
            'symbol': real_time_data['symbol'],
            'rank': real_time_data.get('cmc_rank', 0),
            
            # Price & Market Data
            'price': price,
            'price_formatted': f"${price:,.4f}",
            'market_cap': market_cap,
            'market_cap_formatted': f"${market_cap:,.0f}",
            'volume_24h': volume_24h,
            'volume_24h_formatted': f"${volume_24h:,.0f}",
            
            # Price Changes
            'percent_change_1h': quote.get('percent_change_1h', 0),
            'percent_change_24h': quote.get('percent_change_24h', 0),
            'percent_change_7d': quote.get('percent_change_7d', 0),
            
            # TVL Data
            'tvl': tvl_data['tvl'],
            'tvl_formatted': tvl_data['tvl_formatted'],
            'has_tvl': tvl_data['has_tvl'],
            'tvl_source': tvl_data['source'],
            'tvl_method': tvl_data['method'],
            'tvl_mcap_ratio': round(tvl_mcap_ratio, 2) if tvl_mcap_ratio else None,
            'tvl_analysis': tvl_analysis,
            
            # FDV Data
            'fdv': fdv_analysis['fdv'],
            'fdv_formatted': fdv_analysis['fdv_formatted'],
            'fdv_market_size': fdv_analysis['market_size'],
            'fdv_risk_level': fdv_analysis['risk_level'],
            
            # Inflation Data
            'inflation_rate': inflation_analysis['inflation_rate'],
            'inflation_severity': inflation_analysis['severity'],
            'inflation_description': inflation_analysis['description'],
            
            # Supply Data
            'circulating_supply': circulating_supply,
            'total_supply': total_supply,
            'max_supply': max_supply,
            'circulating_supply_formatted': f"{circulating_supply:,.0f}" if circulating_supply else "N/A",
            'total_supply_formatted': f"{total_supply:,.0f}" if total_supply else "N/A",
            'max_supply_formatted': f"{max_supply:,.0f}" if max_supply else "N/A",
            
            # Metadata
            'last_updated': quote.get('last_updated'),
            'data_status': 'Complete analysis with real data'
        }