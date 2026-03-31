import logging
import sys

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # File handler
        fh = logging.FileHandler('app.log')
        fh.setLevel(logging.DEBUG)
        
        # Console handler (optional, but keep it for errors)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.ERROR)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
    return logger
