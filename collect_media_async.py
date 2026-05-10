import asyncio
from modules import get_chat_entity_async, download_media_async, DownloadTracker
from telethon import TelegramClient
from config import app_config, paths

API_ID = app_config["app_api_id"]
API_HASH = app_config["app_api_hash"]

CHAT_NAME = ""
MEDIA_DIR = "data"
START_MESSAGE_ID = 42868
END_MESSAGE_ID = 0

MAX_CONCURRENT   = 5 
BATCH_SIZE = 50


client = TelegramClient('my_session', API_ID, API_HASH)


async def main():
    tracker = DownloadTracker("downloaded.txt")
    print(f"📋 Resuming with {len(tracker.downloaded_ids)} already-downloaded IDs")

    async with TelegramClient('my_session', API_ID, API_HASH) as client:
        chat_entity = await get_chat_entity_async(client, CHAT_NAME)
        sem = asyncio.Semaphore(MAX_CONCURRENT)

        async def bounded_download(message):
            async with sem:
                await download_media_async(client, message, MEDIA_DIR, tracker)

        tasks = []
        async for message in client.iter_messages(chat_entity):
            if message.media and message.id <= START_MESSAGE_ID:
                # Skip already-downloaded messages
                if tracker.is_downloaded(message.id):
                    print(f"⏭️  Skipping {message.id} (already downloaded)")
                    continue
                tasks.append(asyncio.create_task(bounded_download(message)))

            if message.id <= END_MESSAGE_ID:
                break

        await asyncio.gather(*tasks)

    # Save once at the very end, outside the client context
    tracker.save()
    print(f"🎉 Session complete — {len(tracker.downloaded_ids)} total downloads")


if __name__ == "__main__":
    asyncio.run(main())