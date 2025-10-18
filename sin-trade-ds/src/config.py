import os, pika, logging
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()


class DSConfig:
    PORT = os.environ.get("PORT", 5004)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL") or ""
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY") or ""
    CORS_ORIGINS = os.getenv("CORS_ORIGINS") or "http://localhost:5173"
    ENVIRONMENT = os.getenv("ENVIRONMENT") or "production"
    CLOUDAMQP_URL = os.getenv("CLOUDAMQP_URL") or ""
    POLYGON_KEY = os.getenv("POLYGON_KEY") or ""
    ALPHAVANTAGE_KEY = os.getenv("ALPHAVANTAGE_KEY") or ""

    supabase: Client
    params = pika.URLParameters(CLOUDAMQP_URL)

    if ENVIRONMENT == "development":
        logging.basicConfig(level=logging.INFO)

    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logging.info("set up supabase successfully")
    except Exception as e:
        logging.error(f"Failed to connect to database: {e}")
        supabase = None

    @staticmethod
    def get_connection():
        """Get a new AMQP connection"""
        try:
            return pika.BlockingConnection(DSConfig.params)
        except Exception as e:
            logging.error(f"Failed to create AMQP connection: {e}")
            return None
