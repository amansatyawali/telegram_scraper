import asyncio
from modules import get_chat_entity, download_media
from telethon import TelegramClient, sync
import os
import time
from config import app_config, paths

API_ID   = app_config["app_api_id"]
API_HASH = app_config["app_api_hash"]
OUTPUT_PATH = paths["raw_data"]
CHAT_NAME = "5. Jonney premium"
MEDIA_DIR = "data"
START_MESSAGE_ID = 41752
END_MESSAGE_ID = 0

client = TelegramClient('my_session', API_ID, API_HASH)
client.start()


chat_entity = get_chat_entity(client, CHAT_NAME)

def main():
    for message in client.iter_messages(chat_entity):
        print(message.text)
        if message.media:
            if message.id % 100 == 0:
                print(message.id, message.text)
            if message.id <= START_MESSAGE_ID:
                print(message.id, message.text)
                download_media(client, message, MEDIA_DIR)
            if message.id <= END_MESSAGE_ID:
                break


if __name__ == "__main__":
    main()