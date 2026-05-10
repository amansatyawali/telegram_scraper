from telethon_utils import get_entity_data, get_chats
import os

def get_chat_entity(client, chat_name):
    entities = get_chats(client)
    chat_entity = ""

    for chat in entities:
        if chat.title == chat_name:
            chat_entity = chat
            break
    return chat_entity


def download_media(client, message, media_dir):
    message_id=str(message.id)
    media_id = ""
    try :
        media_id = str(message.media.document.id)
    except:
        media_id = str(message.media.photo.id)

    title = message.text[:100]
    group_id = ""
    if message.grouped_id is not None:
        group_id = f"gid-{message.grouped_id}"

    print(media_id)
    file_name = os.path.join(media_dir, "_-_".join([message_id, media_id, title, group_id]))
    client.download_media(message.media, file=file_name)


async def get_chat_entity_async(client, chat_name):
    # iter_dialogs is the async equivalent of get_chats
    async for dialog in client.iter_dialogs():
        if dialog.title == chat_name:
            return dialog.entity
    return None


class DownloadTracker:
    def __init__(self, tracker_file: str = "downloaded.txt"):
        self.tracker_file = tracker_file
        self.downloaded_ids: set[int] = self._load()

    def _load(self) -> set[int]:
        """Load existing IDs from file on startup."""
        if not os.path.exists(self.tracker_file):
            return set()
        with open(self.tracker_file, "r") as f:
            return {int(line.strip()) for line in f if line.strip().isdigit()}

    def mark_done(self, message_id: int):
        """Add a completed ID to the in-memory set."""
        self.downloaded_ids.add(message_id)

    def is_downloaded(self, message_id: int) -> bool:
        """Check if a message was already downloaded (useful for resuming)."""
        return message_id in self.downloaded_ids

    def save(self):
        """Flush the full set to disk, sorted for readability."""
        with open(self.tracker_file, "w") as f:
            f.writelines(f"{mid}\n" for mid in sorted(self.downloaded_ids))
        print(f"💾 Saved {len(self.downloaded_ids)} IDs to {self.tracker_file}")

async def download_media_async(client, message, media_dir, tracker: DownloadTracker = None):
    try:
        print(f"📥 Preparing download for message {message.id}")

        message_id = str(message.id)

        try:
            media_id = str(message.media.document.id)
        except AttributeError:
            media_id = str(message.media.photo.id)

        title = (message.text or "")[:50].replace("/", "_")
        group_id = f"gid-{message.grouped_id}" if message.grouped_id else ""

        file_name = os.path.join(
            media_dir,
            "_-_".join(filter(None, [message_id, media_id, title, group_id]))
        )

        print(f"💾 Saving to: {file_name}")
        await client.download_media(message.media, file=file_name)
        print(f"✅ Done: {message.id}")

        # Mark as done only after successful download
        if tracker:
            tracker.mark_done(message.id)

    except Exception as e:
        print(f"❌ Error downloading {message.id}: {e}")
