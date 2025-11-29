import time
from datetime import datetime
from typing import Dict, Any

class InMemorySessionService:
    def __init__(self):
        self.sessions = {}
        self.session_timeout = 3600  # 1 hour
    
    def create_session(self, session_id: str, coin_name: str) -> Dict:
        """Create new session"""
        session_data = {
            'session_id': session_id,
            'coin_name': coin_name,
            'created_at': datetime.now(),
            'last_activity': time.time(),
            'data': {},
            'status': 'active'
        }
        self.sessions[session_id] = session_data
        return session_data
    
    def get_session(self, session_id: str) -> Dict:
        """Get session"""
        session = self.sessions.get(session_id)
        if session and time.time() - session['last_activity'] < self.session_timeout:
            session['last_activity'] = time.time()
            return session
        return None
    
    def update_session_data(self, session_id: str, key: str, value: Any):
        """Update session data"""
        if session_id in self.sessions:
            self.sessions[session_id]['data'][key] = value
            self.sessions[session_id]['last_activity'] = time.time()
    
    def compact_context(self, session_id: str, max_size: int = 1000) -> Dict:
        """Compact context for optimization"""
        session = self.get_session(session_id)
        if not session:
            return {}
        
        compact_data = {}
        for key, value in session['data'].items():
            if isinstance(value, dict) and len(str(value)) > 100:
                compact_data[key] = self._summarize_data(key, value)
            else:
                compact_data[key] = value
        
        return compact_data
    
    def _summarize_data(self, key: str, data: Dict) -> Dict:
        """Summarize large data"""
        if key == 'market_data':
            return {
                'summary': 'Compressed market data',
                'essential_keys': ['market_cap', 'price', 'volume_24h']
            }
        return {'summary': 'Compressed data'}