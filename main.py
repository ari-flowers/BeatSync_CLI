from spotify_api.auth import get_spotify_client
from spotify_api.playlists import fetch_playlist_tracks, fetch_liked_songs, load_liked_songs
from local_library.file_scanner import scan_local_folder
from compare.compare_tracks import compare_tracks
from utils.helpers import export_to_csv

def display_tracks(tracks, title, total):
    print(f"\n🎵 {title} ({len(tracks)}/{total}):")
    for i, track in enumerate(tracks, 1):
        print(f"{i}. {track['name']} by {', '.join(track['artists'])}")

def fetch_tracks(sp, playlist_input):
    if playlist_input.startswith("liked"):
        if "--updatesaved" in playlist_input:
            print("\n🔄 Updating saved Liked Songs...")
            return fetch_liked_songs(sp, save=True)
        elif "--usesaved" in playlist_input:
            return load_liked_songs()
        else:
            return fetch_liked_songs(sp)
    else:
        print("\n🔎 Fetching Spotify playlist...")
        return fetch_playlist_tracks(sp, playlist_input)

def main():
    sp = get_spotify_client()
    playlist_input = input("Enter Spotify Playlist URL, ID, or 'liked' for Liked Songs: ").strip()
    folder_path = input("Enter path to your local music folder: ").strip()

    # Default threshold set to 85 (commented out user input)
    threshold = 85  
    # threshold = int(input("Enter match threshold (default 85): ") or 85)

    # Fetch Spotify tracks
    spotify_tracks = fetch_tracks(sp, playlist_input)
    total_tracks = len(spotify_tracks)
    print(f"✅ Found {total_tracks} tracks in Spotify collection.")

    # Scan local folder with progress bar
    local_tracks = scan_local_folder(folder_path)
    print(f"\n✅ Found {len(local_tracks)} tracks in local folder.")

    # Compare tracks with progress bar
    matched_tracks, missing_tracks = compare_tracks(spotify_tracks, local_tracks, threshold)

    # Display missing tracks
    display_tracks(missing_tracks, "Missing Tracks", total_tracks)

    # Optionally display matched tracks
    if matched_tracks and input("\nWould you like to see the matched tracks? (y/n): ").strip().lower() == 'y':
        display_tracks(matched_tracks, "Matched Tracks", total_tracks)

    # Optionally export to CSV
    if input("\nExport results to CSV? (y/n): ").strip().lower() == 'y':
        filename = input("Enter filename (default: track_report.csv): ").strip() or "track_report.csv"
        export_to_csv(matched_tracks, missing_tracks, total_tracks, filename)

    print("\n✅ Process complete!")

if __name__ == "__main__":
    main()