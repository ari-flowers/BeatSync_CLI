import os
from tqdm import tqdm
from .metadata_reader import get_track_metadata

def scan_local_folder(folder_path):
    """Scans the local music folder with a progress bar and extracts track metadata."""
    supported_extensions = ('.mp3', '.wav', '.flac', '.m4a')
    local_tracks = []

    # Count total files for the progress bar
    total_files = sum(len(files) for _, _, files in os.walk(folder_path))

    print("\n🔍 Scanning local folder...")

    with tqdm(total=total_files, desc="Scanning Files", unit="file") as pbar:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(supported_extensions):
                    file_path = os.path.join(root, file)
                    title, artists = get_track_metadata(file_path)
                    local_tracks.append({'title': title, 'artists': artists, 'filename': file})
                pbar.update(1)  # Update progress for every scanned file

    return local_tracks