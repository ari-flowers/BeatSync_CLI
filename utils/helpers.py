import unicodedata
import re
import csv
import os

def export_to_csv(matched_tracks, missing_tracks, total_tracks, filename="track_report.csv"):
    """Export matched and missing tracks to a CSV file with section headers and spacing."""
    if not filename.endswith(".csv"):
        filename += ".csv"

    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", filename)

    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Missing Tracks Section
        writer.writerow([f"Missing Tracks ({len(missing_tracks)}/{total_tracks})"])
        writer.writerow(["Track Name", "Artist(s)"])
        for track in missing_tracks:
            writer.writerow([track['name'], ", ".join(track['artists'])])

        # Blank row between tables
        writer.writerow([])

        # Matched Tracks Section
        writer.writerow([f"Matched Tracks ({len(matched_tracks)}/{total_tracks})"])
        writer.writerow(["Track Name", "Artist(s)"])
        for track in matched_tracks:
            writer.writerow([track['name'], ", ".join(track['artists'])])

    print(f"\n✅ Exported to: {file_path}")
    
# def export_to_csv(matched_tracks, missing_tracks, total_tracks, filename="track_report.csv"):
#     # Ensure the filename ends with .csv
#     if not filename.endswith(".csv"):
#         filename += ".csv"

#     os.makedirs("data", exist_ok=True)
#     file_path = os.path.join("data", filename)

#     with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)

#         # Missing Tracks Section
#         writer.writerow([f"============ MISSING TRACKS ({len(missing_tracks)}/{total_tracks})============", "================"])
#         writer.writerow(["Track Name", "Artist"])
#         for track in missing_tracks:
#             writer.writerow([track['name'], ", ".join(track['artists'])])

#         # Clear separator between tables
#         writer.writerow(["."])
#         writer.writerow(["."])
#         writer.writerow(["."])
        

#         # Matched Tracks Section
#         writer.writerow([f"============ MATCHED TRACKS ({len(matched_tracks)}/{total_tracks})============", "================"])
#         writer.writerow(["Track Name", "Artist"])
#         for track in matched_tracks:
#             writer.writerow([track['name'], ", ".join(track['artists'])])

#     print(f"\n✅ Exported to: {file_path}")

def normalize_string(text):
    """Normalize text by lowering case, removing accents, and stripping special characters."""
    if not text:
        return ""

    # Lowercase the text
    text = text.lower()

    # Normalize unicode accents (e.g., é → e)
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')

    # Remove special characters and punctuation
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # Remove extra spaces
    return ' '.join(text.split())

def join_and_normalize_artists(artists):
    """Join artist names and normalize them for comparison."""
    return normalize_string(" ".join(artists)) if artists else ""