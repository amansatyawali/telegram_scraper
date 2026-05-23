import pandas
import os

# read the excel file present in data/
def read_excel_file(file_path):
    try:
        df = pandas.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None


def read_csv_file(file_path):
    try:
        df = pandas.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None


def create_row_from_filename(filename):
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

        return {
            "filename": filename,
            "message_id": message_id,
            "media_id": media_id,
            "title": title,
            "group_id": group_id,
            "extension": extension
        }
    return None


def get_previous_ids():
    df = read_csv_file("data/all_files.csv")
    
    all_media_ids = df['media_id'].tolist()
    print(f"Total media IDs: {len(all_media_ids)}")
    media_ids = set(all_media_ids)
    print(f"Unique media IDs: {len(media_ids)}")



    all_titles = df['title'].tolist()
    print(f"Total titles: {len(all_titles)}")
    titles = set(all_titles)
    print(f"Unique titles: {len(titles)}")
    return media_ids, titles


if __name__ == "__main__":
    get_previous_ids()

