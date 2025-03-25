from utils.helpers import normalize_string, join_and_normalize_artists

def preprocess_local_tracks(local_tracks):
    """Preprocess local tracks for fast comparison."""
    local_hash = {}
    local_strings = []

    for track in local_tracks:
        normalized_title = normalize_string(track.get('title', ''))
        normalized_artists = join_and_normalize_artists(track.get('artists', []))
        combined = f"{normalized_title} {normalized_artists}".strip()

        if combined:
            local_hash[combined] = track
            local_strings.append(combined)
        elif track.get('filename'):
            fallback = normalize_string(track['filename'])
            local_hash[fallback] = track
            local_strings.append(fallback)

    return local_hash, local_strings