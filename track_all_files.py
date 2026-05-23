import os
import pandas as pd
from tracking_utils import create_row_from_filename

# Folder containing the files
MEDIA_DIR = "data"
skipped_files_path = "skipped.txt"


def get_all_files_from_folder(folder_path):

    rows = []
    
    # Loop through all files in the folder
    for filename in os.listdir(MEDIA_DIR):

        full_path = os.path.join(MEDIA_DIR, filename)

        # Skip directories
        if os.path.isfile(full_path):

            row = create_row_from_filename(filename)
            if filename.endswith(('.xls', '.xlsx', '.csv')):
                continue
            #if any of the attributes of row is None, print it and skip it
            if row is None:    
                print(f"Skipping {filename} - missing attributes")
                continue
            rows.append(row)
    return rows


def get_all_skipped_files(skipped_files_path):
    
    rows = []
    
    #read all lines from skipped.txt and return a list of filenames
    with open(skipped_files_path, "r") as f:
        skipped_files = f.read().splitlines()
        
    for filename in skipped_files:
        row = create_row_from_filename(filename)
        if row is None:    
                print(f"Skipping {filename} - missing attributes")
                continue
        rows.append(row)
    return rows

def main():


    downloaded_files_rows = get_all_files_from_folder(MEDIA_DIR)
    print(f"Total downloaded files picked:{len(downloaded_files_rows)}")
    skipped_files_rows = get_all_skipped_files(skipped_files_path)
    print(f"Total skipped files picked:{len(skipped_files_rows)}")

    # Create dataframe
    downloaded_files_df = pd.DataFrame(downloaded_files_rows, columns=["filename", "message_id", "media_id", "title", "group_id"])
    skipped_files_df = pd.DataFrame(skipped_files_rows, columns=["filename", "message_id", "media_id", "title", "group_id"])
    #If there is a file in data/all_files.csv, then read it and append the dataframe to it, else create a new file
    output_file = "data/all_files.csv"
    existing_df = pd.read_csv(output_file)
    main_df = pd.concat([existing_df, downloaded_files_df], ignore_index=True) 
    main_df = pd.concat([main_df, skipped_files_df], ignore_index=True)
    #remove duplicates based on filename
    main_df = main_df.drop_duplicates(subset=["filename"], keep="first")
    main_df.to_csv('data/all_files.csv', index=False)

if __name__ == "__main__":
    main()