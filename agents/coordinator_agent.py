# agents/coordinator_agent.py
import asyncio
from typing import Dict, List
from .market_agent import MarketAgent
from .token_agent import TokenAgent
from .research_agent import ResearchAgent

class CoordinatorAgent:
    def __init__(self):
        self.market_agent = MarketAgent()
        self.token_agent = TokenAgent() 
        self.research_agent = ResearchAgent()
        self.session_data = {}
    
    async def execute_sequential_workflow(self, coin_name: str):
        """اجرای ترتیبی عامل‌ها - Sequential Agents"""
        print("🚀 شروع فرآیند ترتیبی جمع‌آوری داده‌ها...")
        
        # مرحله 1: داده‌های بازار
        self.session_data['market'] = await self.market_agent.get_market_data(coin_name)
        
        # مرحله 2: داده‌های توکن
        self.session_data['token'] = await self.token_agent.get_token_data(coin_name)
        
        # مرحله 3: تحقیقات
        self.session_data['research'] = await self.research_agent.get_research_data(coin_name)
        
        return self.session_data
    
    async def execute_parallel_workflow(self, coin_name: str):
        """اجرای موازی عامل‌ها - Parallel Agents"""
        print("⚡ شروع فرآیند موازی جمع‌آوری داده‌ها...")
        
        # اجرای همزمان همه عامل‌ها
        tasks = [
            self.market_agent.get_market_data(coin_name),
            self.token_agent.get_token_data(coin_name),
            self.research_agent.get_research_data(coin_name)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        self.session_data.update({
            'market': results[0],
            'token': results[1], 
            'research': results[2]
        })
        
        return self.session_data