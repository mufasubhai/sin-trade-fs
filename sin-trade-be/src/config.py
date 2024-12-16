import os
from dotenv import load_dotenv
from supabase import create_client, Client
import logging


load_dotenv()


class BackendConfig:
    PORT = os.environ.get("PORT", 5002)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL") 
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY") 
    CORS_ORIGINS = os.getenv("CORS_ORIGINS")
    ENVIRONMENT = os.getenv("ENVIRONMENT") or "production"


    supabase: Client 
    
    if ENVIRONMENT == "development": 
        logging.basicConfig(level=logging.INFO)
        
    
    try: 
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        breakpoint()
        logging.info("set up supabase successfully")
    except Exception as e:
        logging.error(f"Failed to connect to database: {e}")
        supabase = None


