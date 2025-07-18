from dotenv import load_dotenv
from os import getenv
from telebot import types, async_telebot

from modules.DatabaseManager import DatabaseManager
from modules.processor import DataProcessor
import asyncio

load_dotenv()

TELEGRAM_BOT_TOKEN=getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_GROUP_LINK=getenv("TELEGRAM_GROUP_LINK", "")


def formatted_message(ads: list) -> str:
    return f"""
5 best ads in Thai:
{[ad.subject + '\n' + ad.body + '\n\n' for ad in ads]}
"""


async def main():
    db_manager = DatabaseManager()
    
    # Initialize data processor
    processor = DataProcessor(db_manager)
    ads = processor.get_recent_ads(5)
    print(f"Link: {TELEGRAM_GROUP_LINK}")
    if ads and len(ads):
        bot = async_telebot.AsyncTeleBot(TELEGRAM_BOT_TOKEN)
        await bot.send_media_group(
            TELEGRAM_GROUP_LINK,
            media=[types.InputMediaPhoto(ad.thumbnail_image) for ad in ads],
        )


if __name__=="__main__":
    asyncio.run(main())