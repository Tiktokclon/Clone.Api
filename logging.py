import logging
from datetime import datetime
from fastapi import Request
from app.utils.database import db
from app.config import settings

class APILogger:
    def __init__(self):
        self.logger = logging.getLogger("api")
        self.logger.setLevel(logging.INFO)
        
        # Fichier de logs
        file_handler = logging.FileHandler('api.log')
        file_handler.setLevel(logging.INFO)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    async def log_request(self, request: Request, user_id: str, model: str, tokens: int):
        """Log une requête API dans la base de données"""
        log_data = {
            "timestamp": datetime.utcnow(),
            "user_id": user_id,
            "model": model,
            "tokens": tokens,
            "path": request.url.path,
            "method": request.method,
            "ip": request.client.host,
            "user_agent": request.headers.get("user-agent")
        }
        
        # Insert dans MongoDB
        await db.api_logs.insert_one(log_data)
        
        # Log local
        self.logger.info(
            f"Request from {user_id} - {model} - {tokens} tokens")

    async def log_error(self, error: Exception, context: str = None):
        """Log une erreur"""
        error_data = {
            "timestamp": datetime.utcnow(),
            "error": str(error),
            "context": context,
            "type": type(error).__name__
        }
        
        await db.error_logs.insert_one(error_data)
        self.logger.error(f"Error: {error} - Context: {context}")

logger = APILogger()
