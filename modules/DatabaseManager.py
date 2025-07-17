from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.models import Base
from dotenv import load_dotenv
import logging
import os

load_dotenv()
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, database_url: str = None):
        if database_url is None:
            database_url = self._get_database_url()
        
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def _get_database_url(self) -> str:
        """Get database URL from environment variables, fallback to SQLite"""
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        db_host = os.getenv("DB_HOST", 'localhost')
        
        if all([db_user, db_password, db_name, db_host]):
            url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"
            logger.info(f"Using PostgreSQL database: {db_host}/{db_name}")
            return url
        else:
            logger.warning("PostgreSQL environment variables not found, falling back to SQLite")
            return "sqlite:///reeltor.db"
        
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise