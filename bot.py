from dotenv import load_dotenv
from os import getenv
from telebot import types, async_telebot

from modules.DatabaseManager import DatabaseManager
from modules.models import Ad
from modules.processor import DataProcessor
import asyncio

load_dotenv()

TELEGRAM_BOT_TOKEN=getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_GROUP_LINK=getenv("TELEGRAM_GROUP_LINK", "")


def formatted_message(ad: Ad) -> str:
    max_length = 950
    message = f"""
{ad.subject}\n{ad.body}\n
"""
    if len(message) > max_length:
        message = message[:max_length-3] + "..."
    return message


async def main():
    db_manager = DatabaseManager()
    
    # Initialize data processor
    processor = DataProcessor(db_manager)
    ads = processor.get_recent_ads(5)
    print(f"Link: {TELEGRAM_GROUP_LINK}")
    bot = async_telebot.AsyncTeleBot(TELEGRAM_BOT_TOKEN)
    try:
        for i, ad in enumerate(ads):
            print(f"ad {ad.id}")
            media_group = [types.InputMediaPhoto(image.image_url) for image in ad.images[:7]]
            media_group[0].caption = f"#{i + 1} of Top 5 annonces of this week!\n\n"
            media_group[0].caption += formatted_message(ad)
            await bot.send_media_group(
                TELEGRAM_GROUP_LINK,
                media=media_group,
            )
            await asyncio.sleep(2)
    except Exception as e:
        print(f"Error! {e}")
    finally:
        # Properly close the bot session
        await bot.close_session()


if __name__=="__main__":
    asyncio.run(main())