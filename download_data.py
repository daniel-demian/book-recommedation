import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

DATA_DIR = "data"
DATASET = "arashnic/book-recommendation-dataset"
FILES = ["Ratings.csv", "Books.csv"]

def get_missing_csvs():
    """Return list of CSV files that are missing"""
    return [
        f for f in FILES
        if not os.path.exists(os.path.join(DATA_DIR, f))
    ]

def download_and_extract():
    missing_files = get_missing_csvs()

    if not missing_files:
        print("✅ All CSV files already exist, nothing to do.")
        return

    print(f"Missing files detected: {missing_files}")
    os.makedirs(DATA_DIR, exist_ok=True)

    api = KaggleApi()
    api.authenticate()

    for file_name in missing_files:
        print(f"Downloading {file_name}...")

        # Kaggle saves ZIP as file_name (e.g. Ratings.csv)
        zip_path = os.path.join(DATA_DIR, file_name)
        safe_zip_path = zip_path + ".zip"

        api.dataset_download_file(
            dataset=DATASET,
            file_name=file_name,
            path=DATA_DIR,
            force=False,
            quiet=False
        )

        # Rename ZIP to avoid name collision
        os.rename(zip_path, safe_zip_path)

        # Extract real CSV
        with zipfile.ZipFile(safe_zip_path, "r") as zip_ref:
            zip_ref.extractall(DATA_DIR)

        # Remove ZIP
        os.remove(safe_zip_path)

        print(f"✅ {file_name} ready")

    print("All required CSV files are now available.")

if __name__ == "__main__":
    download_and_extract()
