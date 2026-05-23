import os
import pandas as pd
from tracking_utils import get_previous_ids
from dotenv import load_dotenv

load_dotenv()

data_path = os.getenv("FILE_LIST_PATH")
media_dir = os.getenv("EXT_DATA_PATH")

all_files_df = pd.read_csv(data_path)
duplicate_filenames = all_files_df[all_files_df.duplicated(subset='media_id', keep='first')]['filename'].tolist()

print(f"Total duplicate filenames found: {len(duplicate_filenames)}")

duplicates_found_count = 0
for duplicate_file in duplicate_filenames:
    if os.path.exists(os.path.join(media_dir, duplicate_file)):
        duplicates_found_count += 1

        ################# Uncomment the below line to delete the duplicate files from the media directory #################
        # os.remove(os.path.join(media_dir, duplicate_file))
        ################# Be careful with the above line, it will permanently delete the files from your media directory #################


print(f"Duplicates files found: {duplicates_found_count}")
# write the duplicate filenames to a text file named duplicates.txt
with open("duplicates.txt", "w") as f:
    for filename in duplicate_filenames:
        f.write(filename + "\n")



