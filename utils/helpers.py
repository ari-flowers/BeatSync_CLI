import unicodedata
import re
import csv
import os

def export_to_csv(matched_tracks, missing_tracks, total_tracks, filename="track_report.csv"):
    # Ensure the filename ends with .csv
    if not filename.endswith(".csv"):
        filename += ".csv"

    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", filename)

    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Missing Tracks Section with "Source" column
        writer.writerow([f"============ MISSING TRACKS ({len(missing_tracks)}/{total_tracks})============", "================"])
        writer.writerow(["Track Name", "Artist", "Source"])
        if missing_tracks:
            for track in missing_tracks:
                writer.writerow([track.get('name', 'Unknown'),
                                 ", ".join(track.get('artists', [])),
                                 "Spotify"])
        else:
            writer.writerow(["No missing tracks found", "", ""])
            
        # Blank rows as separator
        writer.writerow([""])
        writer.writerow([""])
        
        # Matched Tracks Section with "Audio Quality" column
        writer.writerow([f"============ MATCHED TRACKS ({len(matched_tracks)}/{total_tracks})============", "================"])
        writer.writerow(["Track Name", "Artist", "Audio Quality"])
        if matched_tracks:
            for track in matched_tracks:
                if 'audio' in track:
                    audio = track.get('audio', {'format': 'Unknown', 'bitrate': None})
                    if audio.get('format') == 'MP3' and audio.get('bitrate') is not None:
                        quality_str = f"{audio['bitrate']}kbps"
                    else:
                        quality_str = audio.get('format', 'Unknown')
                else:
                    quality_str = "N/A"
                writer.writerow([track.get('name', 'Unknown'),
                                 ", ".join(track.get('artists', [])),
                                 quality_str])
        else:
            writer.writerow(["No matched tracks found", "", ""])

    print(f"\n✅ Exported to: {file_path}")
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