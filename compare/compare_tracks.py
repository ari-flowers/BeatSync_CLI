from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from rapidfuzz import fuzz, process
from compare.preprocess import preprocess_local_tracks
from compare.match_helpers import get_normalized_spotify_string

def compare_single_track(spotify_track, local_hash, local_strings, threshold):
    """Compare a single Spotify track against local tracks using exact and fuzzy matching."""
    spotify_combined = get_normalized_spotify_string(spotify_track)

    # 1️⃣ Quick exact match using hash
    if spotify_combined in local_hash:
        return 'matched', spotify_track

    # 2️⃣ If no hash match, use fuzzy matching
    match, score, _ = process.extractOne(spotify_combined, local_strings, scorer=fuzz.ratio)
    return ('matched', spotify_track) if score >= threshold else ('missing', spotify_track)

def compare_tracks(spotify_tracks, local_tracks, threshold=85):
    """Optimized comparison with preprocessing, parallel execution, and fuzzy matching fallback."""
    print("\n⚡ Preprocessing local tracks...")
    local_hash, local_strings = preprocess_local_tracks(local_tracks)

    matched_tracks, missing_tracks = [], []

    print("\n🔍 Comparing tracks (parallel processing)...")
    with tqdm(total=len(spotify_tracks), desc="Comparing", unit="track") as pbar:
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(compare_single_track, track, local_hash, local_strings, threshold)
                for track in spotify_tracks
            ]

            for future in as_completed(futures):
                result, track = future.result()
                (matched_tracks if result == 'matched' else missing_tracks).append(track)
                pbar.update(1)

    return matched_tracks, missing_tracks