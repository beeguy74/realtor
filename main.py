import json
from typing import Optional
from modules.puller import Puller, ResponseDict
from modules.processor import DataProcessor
from modules.DatabaseManager import DatabaseManager
import logging
import asyncio


# Configure logging to save to file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Application started")

async def main():
    # Initialize database manager
    db_manager = DatabaseManager()
    
    # Create tables if they don't exist
    db_manager.create_tables()
    
    # Initialize data processor
    processor = DataProcessor(db_manager)
    
    # Get data from puller
    puller = Puller()
    res_dict: Optional[ResponseDict] = await puller.get_response()
    
    if res_dict:
        logger.info("Response received, processing data...")
        # Process and save data to database
        stats = processor.process_response(res_dict)
        logger.info(f"Data processing completed: {stats}")
    else:
        logger.warning("No response received from puller")


if __name__ == "__main__":
    asyncio.run(main())
