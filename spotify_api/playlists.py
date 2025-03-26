import json
import os
from tqdm import tqdm

DATA_PATH = "data/liked_songs.json"

def save_liked_songs(tracks):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(tracks, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Saved Liked Songs to '{DATA_PATH}'.")

def load_liked_songs():
    if not os.path.exists(DATA_PATH):
        print("⚠️ No saved Liked Songs found. Please run with '--updatesaved' first.")
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        tracks = json.load(f)
    print(f"\n📂 Loaded {len(tracks)} Liked Songs from saved file.")
    return tracks

def fetch_liked_songs(sp, save=False):
    """
    Fetch Spotify Liked Songs with a progress bar.
    Each track will include a 'playlist' key set to "Liked Songs" for consistency.
    """
    limit = 50
    offset = 0

    print("\n🔎 Fetching Liked Songs... (in batches of 50)")
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)
    total = results['total'] or 0

    if total == 0:
        print("⚠️ No liked songs found.")
        return []

    tracks = []
    with tqdm(total=total, desc="Fetching Liked Songs", unit="track") as pbar:
        while results:
            for item in results['items']:
                track = item['track']
                artists = [artist['name'] for artist in track['artists']]
                # Attach playlist name for consistency
                tracks.append({'name': track['name'], 'artists': artists, 'playlist': "Liked Songs"})
                pbar.update(1)
            results = sp.next(results) if results['next'] else None

    print(f"\n🎉 Completed fetching Liked Songs: {len(tracks)}/{total}")

    if save:
        save_liked_songs(tracks)

    return tracks

def fetch_playlist_tracks(sp, playlist_id):
    """
    Fetch Spotify playlist tracks with a progress bar.
    Each track will include a 'playlist' key containing the playlist name.
    """
    limit = 100
    offset = 0
    tracks = []

    # Retrieve the playlist object to extract the playlist name
    playlist_obj = sp.playlist(playlist_id)
    playlist_name = playlist_obj.get('name', 'Unknown Playlist')

    print("\n🔎 Fetching Spotify playlist tracks...")
    results = sp.playlist_items(playlist_id, limit=limit, offset=offset)
    total = results['total'] or 0

    if total == 0:
        print("⚠️ No tracks found in playlist.")
        return []

    with tqdm(total=total, desc="Fetching Playlist", unit="track") as pbar:
        while results:
            for item in results['items']:
                track = item['track']
                artists = [artist['name'] for artist in track['artists']]
                # Attach playlist name to each track
                tracks.append({'name': track['name'], 'artists': artists, 'playlist': playlist_name})
                pbar.update(1)
            results = sp.next(results) if results['next'] else None

    print(f"\n🎉 Completed fetching playlist tracks: {len(tracks)}/{total}")
    return tracks