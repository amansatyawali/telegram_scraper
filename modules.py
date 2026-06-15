from telethon_utils import get_entity_data, get_chats
import os
import time

def get_chat_entity(client, chat_name):
    entities = get_chats(client)
    chat_entity = ""

    for chat in entities:
        if chat.title == chat_name:
            chat_entity = chat
            break
    return chat_entity


# function to add logs to a file called logs.txt, with the format [timestamp] - message
def record_skipped_file(filename):
    with open("skipped.txt", "a") as f:
        f.write(f"{filename}\n")


def resumable_download(client, media, file_ext, output_path):
    """
    Resume Telegram media download if partial file exists.
    """
    CHUNK_SIZE = 1024 * 1024  # 1 MB
    
    directory_name, file_name = output_path.split('/', 1)
    output_path = directory_name + '/' + file_name.replace('/', '|')

    downloaded_bytes = 0

    if os.path.exists(output_path + file_ext):
        downloaded_bytes = os.path.getsize(output_path + file_ext)

    print(f"Resuming from {downloaded_bytes / (1024 * 1024):.2f} MB")

    with open(output_path + file_ext, "ab") as f:

        for chunk in client.iter_download(
            media,
            offset=downloaded_bytes,
            request_size=CHUNK_SIZE,
        ):
            f.write(chunk)


def download_media(client, message, media_dir, prev_media_ids, skipped_media_ids=None):
    message_id=str(message.id)
    media_id = None
    try :
        media_id = message.media.document.id
    except:
        media_id = message.media.photo.id

    group_id = ""
    if message.grouped_id is not None:
        group_id = f"gid-{message.grouped_id}"

    file_ext = message.file.ext

    title = message.text[:100].replace('/', '|').replace('\n', ' ').replace('.', '_')
    file_name = os.path.join(media_dir, "_-_".join([message_id, str(media_id), title, group_id]))

    if media_id in prev_media_ids:
        print(f"⚠️ Skipping {message.id} - already downloaded")
        record_skipped_file(f"{file_name}{file_ext}")
        return

    if skipped_media_ids and media_id in skipped_media_ids:
        print(f"⚠️ Skipping {message.id} - in skipped list")
        return

    max_retries = 2
    for attempt in range(max_retries + 1):

        try:
            print(media_id)
            # client.download_media(message.media, file=file_name)
            resumable_download(client, message.media, file_ext, file_name)
            
            # Add the media_id to the set of previously downloaded IDs to prevent future duplicates
            prev_media_ids.add(media_id)
        except Exception as e:

            print(f"❌ Download failed (attempt {attempt + 1}): {e}")

            if attempt < max_retries:
                print("🔄 Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("🚫 Max retries reached")
                exit(1)


async def get_chat_entity_async(client, chat_name):
    # iter_dialogs is the async equivalent of get_chats
    async for dialog in client.iter_dialogs():
        if dialog.title == chat_name:
            return dialog.entity
    return None

