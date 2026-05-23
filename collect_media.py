import asyncio
from modules import get_chat_entity, download_media
from telethon import TelegramClient, sync
import os
import time
from config import app_config
from tracking_utils import get_previous_ids
from dotenv import load_dotenv

load_dotenv()

API_ID   = app_config["app_api_id"]
API_HASH = app_config["app_api_hash"]
CHAT_NAME = os.getenv("TG_CAHT_NAME")
MEDIA_DIR = "data"
START_MESSAGE_ID = int(os.getenv("START_MESSAGE_ID"))
END_MESSAGE_ID = int(os.getenv("END_MESSAGE_ID"))

skipped = []
skipped_media_ids = []

prev_media_ids, prev_titles = get_previous_ids()

client = TelegramClient('my_session', API_ID, API_HASH)
client.start()


chat_entity = get_chat_entity(client, CHAT_NAME)

def main():
    for message in client.iter_messages(chat_entity):
        print(message.text)
        if message.media:
            if message.id % 100 == 0:
                print(message.id, message.text)
                if message.id in skipped:
                    print(f"⚠️ Skipping {message.id} - in skipped list")
                    continue
            if message.id <= START_MESSAGE_ID:
                print(message.id, message.text)
                
                file_size = message.file.size if message.file else 0

                # Convert to MB for readability
                file_size_mb = round(file_size / (1024 * 1024), 2)
                print(f"File Size: {file_size_mb} MB")
                download_media(client, message, MEDIA_DIR, prev_media_ids, skipped_media_ids)
            if message.id <= END_MESSAGE_ID:
                break


if __name__ == "__main__":
    main()