# utils/logger.py
import logging
import sys

def setup_logger():
    """تنظیمات logging برای observability"""
    logger = logging.getLogger('crypto_agent')
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger