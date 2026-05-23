import os
from dotenv import load_dotenv

load_dotenv()

app_config = {
    "app_api_id" : int(os.getenv("app_api_id")),
    "app_api_hash" : os.getenv("app_api_hash"),
    "app_title" : os.getenv("app_title"),
    "app_short_name" : os.getenv("app_short_name"),
    "test_url" : os.getenv("test_url"),
    "test_public_key" : os.getenv("test_public_key")
}