# BeatSync CLI Tool

BeatSync is a command-line tool designed to help DJs and music curators compare their Spotify playlists (or liked songs) with their local music libraries. The tool identifies missing tracks, matches available ones, and exports detailed reports—including audio quality and playlist source information—to CSV.

---

## Features

- **Multiple Playlist Support:**  
  Accepts multiple Spotify playlist URLs/IDs (comma-separated) and combines their tracks. Also supports Spotify Liked Songs (with options to update or use cached results).

- **Audio Quality Detection:**  
  Uses Mutagen to detect the audio format (e.g., MP3, FLAC, WAV) and, for MP3 files, retrieves the bitrate (e.g., "320kbps").

- **Filtering:**  
  Supports filtering of local tracks based on:
  - `--lossless-only`: Only include lossless local files.
  - `--mp3-only`: Only include MP3 files.
  - `--min-bitrate`: Only include MP3 files with a bitrate at or above the specified value.

- **CSV Export:**  
  Exports results to a CSV file with two sections:
  - **Missing Tracks:** Columns: *Track Name, Artist, Source, Playlist*. Missing tracks will show "Spotify" as the source.
  - **Matched Tracks:** Columns: *Track Name, Artist, Audio Quality, Playlist*. For MP3s, the audio quality column shows the bitrate (e.g., "320kbps"); otherwise, it shows the format.

- **Modular Architecture:**  
  The codebase is organized into modules for Spotify API interactions, local library scanning (with audio quality detection), track comparison (with fuzzy matching and merging of audio data), and various helper functions.

- **CLI Start Script:**  
  A `start.sh` script is provided for convenience. It activates the virtual environment and forwards any command-line arguments to the tool.

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ari-flowers/BeatSync_CLI.git
   cd BeatSync_CLI
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running the Tool

You can run the tool directly via Python or use the provided start script.

- **Using the start script (recommended):**
  ```bash
  ./start.sh [options]
  ```
  *Example:*
  ```bash
  ./start.sh --lossless-only --min-bitrate 320
  ```

- **Directly via Python:**
  ```bash
  python main.py [options]
  ```

### Interactive Prompts

- **Spotify Input:**  
  Enter a Spotify Playlist URL, Playlist ID, or `"liked"` for your Liked Songs.  
  For multiple playlists, separate entries with commas (e.g., `playlistID1, playlistID2`).

- **Local Music Folder:**  
  Enter the full path to your local music folder.

### Filtering Options

- `--lossless-only`  
  Filters local tracks so that only lossless files are considered.

- `--mp3-only`  
  Filters local tracks so that only MP3 files are considered.

- `--min-bitrate <kbps>`  
  Filters out MP3 tracks with a bitrate lower than the specified value.

### CSV Export

After comparison, you’ll be prompted to export results to CSV. The export includes:

- **Missing Tracks Section:**  
  Columns: *Track Name, Artist, Source, Playlist*. The "Source" is fixed as "Spotify".

- **Matched Tracks Section:**  
  Columns: *Track Name, Artist, Audio Quality, Playlist*. For MP3s, audio quality displays the bitrate (e.g., "320kbps"); otherwise, it displays the format.

---

## Project Structure

```
BeatSync_CLI/
├── main.py                   # Entry point for the CLI tool
├── config.py                 # Centralized configuration (default threshold, paths, etc.)
├── spotify_api/              # Spotify API interaction module
│   ├── __init__.py
│   ├── auth.py               # Handles Spotify OAuth and client setup
│   ├── playlists.py          # Fetches playlist and liked songs, attaches playlist name
├── local_library/            # Local music file handling
│   ├── __init__.py
│   ├── file_scanner.py       # Scans local folders, extracts metadata, calls audio quality
│   ├── audio_quality.py      # Detects audio format, bitrate, and lossless status using Mutagen
│   └── metadata_reader.py    # Reads basic track metadata from files
├── compare/                  # Track comparison logic
│   ├── __init__.py
│   ├── compare_tracks.py     # Orchestrates the comparison, merging local audio data into Spotify tracks
│   ├── match_helpers.py      # Normalizes and prepares track data for comparison
│   └── preprocess.py         # Preprocesses local tracks for fast lookup during comparison
├── utils/                    # Helper functions
│   ├── __init__.py
│   ├── helpers.py            # Contains utility functions (normalize strings, CSV export, etc.)
├── data/                     # Directory for cached files (e.g., liked_songs.json) and CSV exports
├── start.sh                  # Start script to activate the venv and run the tool with arguments
└── requirements.txt          # Project dependencies
```

---

## Next Steps

Future enhancements include:
- Refining the audio quality module (e.g., more detailed bitrate info, additional codecs).
- Adding support for other streaming services.
- Implementing data caching to reduce API calls.
- Transitioning the tool to a scalable Laravel web app.
- Dockerizing the application for consistent deployment across environments.

---

## Troubleshooting

- **Dependencies:**  
  If you encounter module errors, ensure your virtual environment is active and all packages are installed via `pip install -r requirements.txt`.

- **Filtering:**  
  Ensure you’re passing filtering flags correctly. The start script forwards all flags to `main.py`.

- **CSV Export:**  
  Verify the exported CSV file in the `data/` folder for proper formatting.

---

Happy mixing, and enjoy curating your sets with BeatSync CLI!