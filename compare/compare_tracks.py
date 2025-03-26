from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from rapidfuzz import fuzz, process
from compare.preprocess import preprocess_local_tracks
from compare.match_helpers import get_normalized_spotify_string

def compare_single_track(spotify_track, local_hash, local_strings, threshold):
    """
    Compare a single Spotify track against local tracks using exact and fuzzy matching.
    If a match is found, merge the local track's audio data into the Spotify track.
    """
    spotify_combined = get_normalized_spotify_string(spotify_track)
    
    # Quick exact match using hash
    if spotify_combined in local_hash:
        local_track = local_hash[spotify_combined]
        spotify_track['audio'] = local_track.get('audio')
        return ('matched', spotify_track)
    
    # Fuzzy match fallback using rapidfuzz
    match, score, _ = process.extractOne(spotify_combined, local_strings, scorer=fuzz.ratio)
    if score >= threshold:
        local_track = local_hash[match]
        spotify_track['audio'] = local_track.get('audio')
        return ('matched', spotify_track)
    else:
        return ('missing', spotify_track)

def compare_tracks(spotify_tracks, local_tracks, threshold=85):
    """
    Compares Spotify tracks to local tracks using parallel processing.
    Preprocesses the local tracks for fast lookups.
    Returns two lists: matched_tracks and missing_tracks.
    """
    local_hash, local_strings = preprocess_local_tracks(local_tracks)
    
    matched_tracks = []
    missing_tracks = []

    with tqdm(total=len(spotify_tracks), desc="Comparing", unit="track") as pbar:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(compare_single_track, track, local_hash, local_strings, threshold)
                       for track in spotify_tracks]
            for future in as_completed(futures):
                result, track = future.result()
                if result == 'matched':
                    matched_tracks.append(track)
                else:
                    missing_tracks.append(track)
                pbar.update(1)
                
    return matched_tracks, missing_tracks