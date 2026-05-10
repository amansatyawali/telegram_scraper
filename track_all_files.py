import os
import pandas as pd

# Folder containing the files
media_dir = "./data"

rows = []

# Loop through all files in the folder
for filename in os.listdir(media_dir):

    full_path = os.path.join(media_dir, filename)

    # Skip directories
    if os.path.isfile(full_path):

        # Separate filename and extension
        name_without_ext, extension = os.path.splitext(filename)

        # Split using "_-_"
        parts = name_without_ext.split("_-_")

        # Ensure expected structure
        if len(parts) >= 4:
            message_id = parts[0]
            media_id = parts[1]
            title = parts[2]
            group_id = parts[3]

            rows.append({
                "filename": filename,
                "message_id": message_id,
                "media_id": media_id,
                "title": title,
                "group_id": group_id,
                "extension": extension
            })

# Create dataframe
df = pd.DataFrame(rows)
df.to_excel("records/all_files.xlsx", index=False)

print(df.head())