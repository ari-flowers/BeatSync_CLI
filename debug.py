#!/usr/bin/env python

import os
from local_library.file_scanner import scan_local_folder

def main():
    folder_path = input("Enter the path to your local music folder: ").strip()
    
    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please try again.")
        return

    print("\nStarting scan...\n")
    local_tracks = scan_local_folder(folder_path)
    
    print("\nScan complete. Here are the results:\n")
    for track in local_tracks:
        title = track.get('title', 'Unknown')
        artists = ", ".join(track.get('artists', []))
        filename = track.get('filename', 'Unknown')
        audio = track.get('audio', {'format': 'Unknown', 'bitrate': None})
        
        # Build a quality string for MP3s if bitrate is available
        if audio.get('format') == 'MP3':
            if audio.get('bitrate') is not None:
                quality_str = f"{audio['bitrate']}kbps"
            else:
                quality_str = "MP3"
        else:
            quality_str = audio.get('format', 'Unknown')
        
        print(f"Track: {title} by {artists}")
        print(f"Filename: {filename}")
        print(f"Audio Quality: {quality_str}")
        print("-" * 40)

if __name__ == "__main__":
    main()