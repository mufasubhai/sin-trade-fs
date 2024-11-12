import os
from dotenv import load_dotenv


class DataServiceConfig:
    load_dotenv()
    PORT = os.environ.get("PORT", 5004)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL") 
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY") 
    CORS_ORIGINS = os.getenv("CORS_ORIGINS")
    ENVIRONMENT = os.getenv("ENVIRONMENT") or "production"