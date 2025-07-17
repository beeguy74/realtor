# Data Processor Usage Example

## Overview
The `DataProcessor` class handles saving data from the Puller response to your database using SQLAlchemy models.

## Basic Usage

```python
from modules.DatabaseManager import DatabaseManager
from modules.processor import DataProcessor
from modules.puller import Puller

# Initialize components
db_manager = DatabaseManager()
db_manager.create_tables()  # Create tables if they don't exist

processor = DataProcessor(db_manager)
puller = Puller()

# Get data and process it
response = await puller.get_response()
if response:
    stats = processor.process_response(response)
    print(f"Processed: {stats}")
```

## Features

### Automatic Data Handling
- **Accounts**: Creates or updates account information from ads
- **Ads**: Saves all ad data with proper relationships
- **Images**: Handles multiple image types (regular, thumbnails, webp)
- **Parameters**: Saves ad-specific parameters and labels

### Error Handling
- Graceful handling of duplicate entries
- Transaction rollback on errors
- Detailed logging for debugging

### Statistics
The `process_response()` method returns statistics:
```python
{
    "accounts": 5,    # Number of accounts processed
    "ads": 20,        # Number of ads processed  
    "images": 60,     # Number of images processed
    "parameters": 40  # Number of parameters processed
}
```

### Database Models Used
- `Account`: Stores seller/account information
- `Ad`: Main ad data with all properties
- `AdImage`: Images associated with ads
- `AdParameter`: Ad-specific parameters and filters

## Configuration

### Database URL
Default: `sqlite:///reeltor.db`
Custom: Pass to `DatabaseManager("your_database_url")`

### Logging
The processor uses Python's logging module. Configure as needed:
```python
import logging
logging.basicConfig(level=logging.INFO)
```
