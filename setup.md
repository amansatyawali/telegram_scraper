## Create the .env file with these variables and set their values
app_api_id =
app_api_hash =
app_title =
app_short_name =
test_url =
test_public_key =
TG_CAHT_NAME=
EXT_DATA_PATH=
FILE_LIST_PATH=
START_MESSAGE_ID=
END_MESSAGE_ID=

# Mount drive to WSL
sudo mkdir -p /mnt/e
sudo mount -t drvfs I: /mnt/e

# Start downloading media
python collect_media.py 

# Track all files after download is done
python track_all_files.py