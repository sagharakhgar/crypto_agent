from typing import Dict

class DataAnalysisTools:
    """Custom data analysis tools for cryptocurrencies"""
    
    def calculate_tvl_mcap_ratio(self, tvl: float, market_cap: float) -> Dict:
        """Calculate TVL to Market Cap ratio"""
        if market_cap == 0 or tvl == 0:
            return {
                'ratio': 0,
                'interpretation': 'Insufficient data',
                'risk_level': 'Unknown'
            }
        
        ratio = (tvl / market_cap) * 100
        
        if ratio > 50:
            interpretation = "Very high TVL relative to market cap - indicates project health"
            risk_level = 'low'
        elif ratio > 20:
            interpretation = "Good TVL relative to market cap"
            risk_level = 'low'
        elif ratio > 10:
            interpretation = "Reasonable TVL"
            risk_level = 'medium'
        elif ratio > 5:
            interpretation = "Low TVL - needs more investigation"
            risk_level = 'high'
        else:
            interpretation = "Very low TVL - high risk"
            risk_level = 'very_high'
        
        return {
            'ratio': round(ratio, 2),
            'interpretation': interpretation,
            'risk_level': risk_level
        }
    
    def analyze_inflation_rate(self, circulating_supply: float, total_supply: float, max_supply: float = None) -> Dict:
        """Analyze token inflation rate"""
        if circulating_supply == 0:
            return {
                'inflation_rate': 0,
                'severity': 'Unknown',
                'description': 'Circulating supply is zero'
            }
        
        if total_supply and total_supply > circulating_supply:
            inflation_rate = ((total_supply - circulating_supply) / circulating_supply) * 100
        else:
            inflation_rate = 0
        
        if inflation_rate > 20:
            severity = 'Very High'
            description = 'Very high inflation - potential selling pressure'
        elif inflation_rate > 10:
            severity = 'High'
            description = 'High inflation - needs close monitoring'
        elif inflation_rate > 5:
            severity = 'Medium'
            description = 'Medium inflation - acceptable for most projects'
        elif inflation_rate > 1:
            severity = 'Low'
            description = 'Low inflation - ideal condition'
        else:
            severity = 'Very Low'
            description = 'Very low or zero inflation - optimal condition'
        
        return {
            'inflation_rate': round(inflation_rate, 2),
            'severity': severity,
            'description': description
        }
    
    def calculate_fully_diluted_valuation(self, current_price: float, total_supply: float) -> Dict:
        """Calculate Fully Diluted Valuation"""
        if not current_price or not total_supply:
            return {
                'fdv': 0,
                'fdv_formatted': '$0',
                'market_size': 'Unknown',
                'risk_level': 'Unknown'
            }
        
        fdv = current_price * total_supply
        
        if fdv > 10000000000:
            market_size = "Very Large"
            risk = "High (aggressive valuation)"
        elif fdv > 1000000000:
            market_size = "Large"
            risk = "Medium"
        elif fdv > 100000000:
            market_size = "Medium"
            risk = "Low"
        else:
            market_size = "Small"
            risk = "Very Low"
        
        return {
            'fdv': fdv,
            'fdv_formatted': f"${fdv:,.2f}",
            'market_size': market_size,
            'risk_level': risk
        }

class DataValidator:
    """Data validation tools"""
    
    def check_data_quality(self, data: Dict) -> Dict:
        """Check data quality"""
        required_fields = ['name', 'symbol', 'price', 'market_cap']
        filled_fields = sum(1 for field in required_fields if data.get(field))
        
        completeness_score = (filled_fields / len(required_fields)) * 100
        
        if completeness_score >= 80:
            quality = 'Excellent'
        elif completeness_score >= 60:
            quality = 'Good'
        elif completeness_score >= 40:
            quality = 'Medium'
        else:
            quality = 'Poor'
        
        return {
            'completeness_score': round(completeness_score, 2),
            'overall_quality': quality
        }