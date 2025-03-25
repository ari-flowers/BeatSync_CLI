# 🎵 **BeatSync - DJ Setlist Curation Tool (Quick Start Guide)**

A simple tool to compare your Spotify playlists or Liked Songs with your local music library to identify missing tracks.

---

## 🚀 **Setup**

1. **Clone the repo:**

```bash
git clone <your-repo-url>
cd BeatSync
```

2. **Create and activate the virtual environment:**

```bash
# Create venv (if not already created)
python -m venv venv

# Activate venv (Mac/Linux)
source venv/bin/activate

# Activate venv (Windows)
venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## 🎧 **Usage**

Run the tool:

```bash
python main.py
```

### **Inputs during runtime:**

- **Spotify input:**  
  Enter one of the following:
  - Spotify Playlist URL or ID (e.g., `https://open.spotify.com/playlist/...` or `37i9dQZF1DXcBWIGoYBM5M`)
  - `"liked"` → Fetch Liked Songs from Spotify.  
  - `"liked --updatesaved"` → Fetch and **save Liked Songs** to a local JSON file.  
  - `"liked --usesaved"` → **Load Liked Songs from the saved file** (faster, no API call).  

- **Local music folder path:**  
  Enter the path to your local music directory.

---

## ⚙️ **Spotify Liked Songs Flags**

| **Flag**              | **Description**                                            |
|-----------------------|------------------------------------------------------------|
| `liked`               | Fetch Liked Songs from Spotify API (may take longer).      |
| `liked --updatesaved` | Fetch from Spotify and save to `data/liked_songs.json`.    |
| `liked --usesaved`    | Load Liked Songs from `data/liked_songs.json` (faster).    |

> ✅ Use `liked --usesaved` for quicker tests after saving your Liked Songs.

---

## 📂 **File Structure Overview**

```
BeatSync/
├─ main.py
├─ spotify_api/
│  ├─ playlists.py     # Handles Spotify API interactions and local saving
│  ├─ auth.py          # Spotify authentication
├─ local_library/      # Scans and processes local music files
├─ compare/            # Track comparison logic
├─ data/
│  ├─ liked_songs.json # Saved Liked Songs (if using --updatesaved flag)
├─ requirements.txt
```

---

## ✅ **Example Workflow**

1. **First-time use (save Liked Songs):**

```bash
python main.py
Enter Spotify Playlist URL, ID, or 'liked' for Liked Songs: liked --updatesaved
```

2. **Subsequent runs (use saved Liked Songs):**

```bash
python main.py
Enter Spotify Playlist URL, ID, or 'liked' for Liked Songs: liked --usesaved
```

3. **Compare with a playlist directly:**

```bash
python main.py
Enter Spotify Playlist URL, ID, or 'liked' for Liked Songs: https://open.spotify.com/playlist/...
```

---

## 📝 **Notes**

- Default **fuzzy match threshold** is set to **85** (user input is disabled for now).  
- Liked Songs are saved in `data/liked_songs.json`.  
- Use **progress bars** to track fetching, scanning, and comparison steps.

---

🔄 **This README is temporary** and will be rewritten later with more details.