from mutagen import File
import os

def get_track_metadata(file_path):
    """
    Extract track title and multiple artists from file metadata.
    Fallback to filename if metadata is unavailable.
    """
    try:
        audio = File(file_path, easy=True)
        if audio:
            title = audio.get('title', [None])[0]
            artists = audio.get('artist', [])
            artists = [artist.strip() for artist in artists if artist] if artists else []
            if title and artists:
                return title, artists
    except Exception:
        pass

    # Fallback to filename if metadata is missing
    filename = os.path.basename(file_path)
    name = os.path.splitext(filename)[0]
    return name, []