from utils.helpers import normalize_string, join_and_normalize_artists

def get_normalized_spotify_string(track):
    """Return normalized string for a Spotify track."""
    return normalize_string(f"{track['name']} {join_and_normalize_artists(track['artists'])}")

def get_normalized_local_string(track):
    """Return normalized string for a local track (fallbacks to filename)."""
    if track.get("title") and track.get("artists"):
        return normalize_string(f"{track['title']} {join_and_normalize_artists(track['artists'])}")
    return normalize_string(track.get("filename", ""))