import sys
from agents.universal_market_agent import UniversalMarketAgent
from config import validate_config

class FundamentalAnalyzer:
    def __init__(self):
        self.agent = UniversalMarketAgent()
    
    def analyze_coin(self, coin_name: str):
        """Analyze a cryptocurrency and generate comprehensive report"""
        print(f"\n🎯 Analyzing: {coin_name}")
        print("=" * 60)
        
        try:
            data = self.agent.get_universal_market_data(coin_name)
            
            if 'error' in data:
                print(f"❌ Error: {data['error']}")
                return None
                
            self._display_comprehensive_report(data)
            return data
            
        except Exception as e:
            print(f"❌ Analysis Error: {e}")
            return None
    
    def _display_comprehensive_report(self, data):
        """Display comprehensive fundamental analysis report"""
        
        print(f"\n📊 COMPREHENSIVE FUNDAMENTAL ANALYSIS REPORT")
        print("=" * 50)
        
        # Basic Information
        print(f"🏷️  ASSET: {data['name']} ({data['symbol']})")
        print(f"🏆 RANK: #{data['rank']}")
        print(f"🕒 LAST UPDATED: {data.get('last_updated', 'N/A')}")
        print("")
        
        # Price and Market Data
        print("💰 PRICE & MARKET DATA")
        print("-" * 25)
        print(f"   💵 Price: {data['price_formatted']}")
        print(f"   📊 Market Cap: {data['market_cap_formatted']}")
        print(f"   💎 24h Volume: {data['volume_24h_formatted']}")
        print("")
        
        # Valuation Metrics
        print("🎯 VALUATION METRICS")
        print("-" * 20)
        print(f"   🏦 FDV: {data['fdv_formatted']}")
        print(f"   📈 FDV Market Size: {data['fdv_market_size']}")
        print(f"   ⚠️  FDV Risk: {data['fdv_risk_level']}")
        print("")
        
        # TVL Analysis
        print("🔗 TVL ANALYSIS")
        print("-" * 15)
        print(f"   💰 TVL: {data['tvl_formatted']}")
        print(f"   📍 Source: {data['tvl_source']}")
        print(f"   🔍 Method: {data['tvl_method']}")
        
        if data['has_tvl'] and data['tvl_mcap_ratio']:
            print(f"   📊 TVL/MC Ratio: {data['tvl_mcap_ratio']}%")
            print(f"   📝 Interpretation: {data['tvl_analysis']['interpretation']}")
            print(f"   🚨 Risk Level: {data['tvl_analysis']['risk_level']}")
        print("")
        
        # Supply and Inflation
        print("🔄 SUPPLY & INFLATION ANALYSIS")
        print("-" * 30)
        print(f"   🎯 Circulating Supply: {data['circulating_supply_formatted']}")
        print(f"   📦 Total Supply: {data['total_supply_formatted']}")
        if data['max_supply_formatted'] != "N/A":
            print(f"   🏁 Max Supply: {data['max_supply_formatted']}")
        print(f"   📈 Inflation Rate: {data['inflation_rate']}%")
        print(f"   ⚠️  Inflation Severity: {data['inflation_severity']}")
        print(f"   📝 {data['inflation_description']}")
        print("")
        
        # Data Quality
        print("✅ DATA QUALITY")
        print("-" * 15)
        print(f"   📋 Status: {data['data_status']}")
        print(f"   🔄 TVL Available: {data['has_tvl']}")
        print("")
        
        print("=" * 60)
        print("📈 REPORT COMPLETED - All fundamental parameters analyzed")
    
    def run_interactive_mode(self):
        """Run the analyzer in interactive mode"""
        print("🤖 AI Fundamental Analysis Agent")
        print("🔧 Supports All Major Cryptocurrencies")
        print("📊 Parameters: Price, Market Cap, Volume, FDV, TVL, Inflation, Supply")
        print("=" * 50)
        
        while True:
            print("\n" + "=" * 40)
            print("Options:")
            print("1. Analyze specific cryptocurrency")
            print("2. Exit")
            
            choice = input("\nPlease select option (1-2): ").strip()
            
            if choice == '1':
                coin_name = input("💰 Enter coin name or symbol: ").strip()
                if coin_name:
                    self.analyze_coin(coin_name)
                else:
                    print("❌ Please enter a coin name")
            
            elif choice == '2':
                print("👋 Thank you for using the Fundamental Analyzer!")
                break
            
            else:
                print("❌ Invalid option. Please enter 1 or 2.")

def main():
    """Main function"""
    # Validate configuration
    if not validate_config():
        print("❌ Please configure your API keys in .env file")
        print("💡 Create .env file with: COINMARKETCAP_API_KEY=your_api_key")
        return
    
    analyzer = FundamentalAnalyzer()
    
    # Command line support
    if len(sys.argv) > 1:
        coin_name = " ".join(sys.argv[1:])
        analyzer.analyze_coin(coin_name)
    else:
        analyzer.run_interactive_mode()

if __name__ == "__main__":
    print("🚀 AI Fundamental Analysis Agent v2.0")
    print("📊 Comprehensive Market Data Analysis")
    print("🔗 Real-time TVL & Valuation Metrics")
    print("💰 Price, Market Cap, FDV, Inflation, Supply Analysis")
    print("")
    
    main()