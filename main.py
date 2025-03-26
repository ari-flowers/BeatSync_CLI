import argparse
from spotify_api.auth import get_spotify_client
from spotify_api.playlists import fetch_playlist_tracks, fetch_liked_songs, load_liked_songs
from local_library.file_scanner import scan_local_folder
from compare.compare_tracks import compare_tracks
from utils.helpers import export_to_csv
from config import DEFAULT_MATCH_THRESHOLD

def display_tracks(tracks, title, total):
    print(f"\n🎵 {title} ({len(tracks)}/{total}):")
    for i, track in enumerate(tracks, 1):
        # For matched tracks, audio info may be merged, so try to show it if available
        audio = track.get('audio', {})
        if audio.get('format') == 'MP3' and audio.get('bitrate') is not None:
            quality_str = f"{audio['bitrate']}kbps"
        else:
            quality_str = audio.get('format', 'N/A')
        print(f"{i}. {track.get('name', 'Unknown')} by {', '.join(track.get('artists', []))} | Audio Quality: {quality_str}")

def fetch_tracks(sp, playlist_input):
    if playlist_input.lower().startswith("liked"):
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
    # Set up argument parsing for filtering
    parser = argparse.ArgumentParser(description="BeatSync CLI Tool")
    parser.add_argument("--lossless-only", action="store_true", help="Only include lossless local files")
    parser.add_argument("--mp3-only", action="store_true", help="Only include MP3 local files")
    parser.add_argument("--min-bitrate", type=int, default=0, help="Minimum bitrate (kbps) for MP3 files")
    args = parser.parse_args()

    sp = get_spotify_client()
    playlist_input = input("Enter Spotify Playlist URL, ID, or 'liked' for Liked Songs: ").strip()
    folder_path = input("Enter path to your local music folder: ").strip()

    threshold = DEFAULT_MATCH_THRESHOLD

    # Fetch Spotify tracks
    spotify_tracks = fetch_tracks(sp, playlist_input)
    total_tracks = len(spotify_tracks)
    print(f"✅ Found {total_tracks} tracks in Spotify collection.")

    # Scan local folder
    local_tracks = scan_local_folder(folder_path)
    print(f"\n✅ Found {len(local_tracks)} tracks in local folder.")

    # Apply filtering based on CLI flags
    filtered_local_tracks = local_tracks  # start with all local tracks

    if args.lossless_only:
        filtered_local_tracks = [track for track in filtered_local_tracks if track.get('audio', {}).get('lossless')]
    if args.mp3_only:
        filtered_local_tracks = [track for track in filtered_local_tracks if track.get('audio', {}).get('format') == 'MP3']
    if args.min_bitrate > 0:
        filtered_local_tracks = [
            track for track in filtered_local_tracks 
            if track.get('audio', {}).get('format') != 'MP3' or 
               (track.get('audio', {}).get('bitrate') is not None and track.get('audio', {}).get('bitrate') >= args.min_bitrate)
        ]

    print(f"\n✅ After filtering, {len(filtered_local_tracks)} local tracks remain.")

    # Compare tracks using the filtered local tracks
    matched_tracks, missing_tracks = compare_tracks(spotify_tracks, filtered_local_tracks, threshold)

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