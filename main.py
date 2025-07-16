import json
from modules.puller import Puller
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
    puller = Puller()
    res_dict = json.loads(await puller.get_response())
    if res_dict:
        for key in res_dict.keys():
            print(res_dict[key])
            break


if __name__ == "__main__":
    asyncio.run(main())
