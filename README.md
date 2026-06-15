# YouTube to Spotify Playlist Sync 🎵

An automated Python tool designed to seamlessly migrate playlists from YouTube directly into your Spotify account using official APIs. 

Unlike basic scripts that pull raw text and match incorrect tracks, this tool implements **intelligent title regex cleaning** and **strict field-restricted filtering** (`track:"..." artist:"..."`) to drastically minimize mismatches, covers, or unwanted remixes. It is also optimized to run **100% in-memory**, completely bypassing local cache file generation and sandbox permission errors (`EPERM`) often found in restricted Linux environments.

---

## ✨ Features

* 🚀 **Official API Integration**: Leverages Google API Client and Spotipy for stable, high-volume track extraction.
* 🧼 **Smart Title Purifier**: Uses regular expressions to strip out YouTube-specific clutter like `[Official Music Video]`, `(Lyric Video)`, `Prod. by`, and audio tags before hitting Spotify's search engine.
* 🎯 **Strict Dual-Layer Matching**: Dynamically parses titles looking for `"Artist - Track"` structures to isolate specific search boxes. If a video lacks an artist name but belongs to a dedicated playlist (e.g., LetoDie), it injects a fallback artist filter.
* 🧠 **Zero-Disk Footprint**: Utilizes a memory-only cache handler. It won't pollute your project directory with `.cache` files or fail due to write permissions.

---

## 🛠️ Prerequisites & Installation

Make sure you have Python 3 installed on your machine. Install the required official SDKs via `pip`:

```bash
pip install spotipy google-api-python-client
```

# 🔐 API Credentials Setup
This project uses Environment Variables to handle keys securely. This prevents you from accidentally pushing your private credentials to public GitHub repositories.

1. Get Your Keys
YouTube Key: Go to the Google Cloud Console, enable the YouTube Data API v3, and generate an API Key.

Spotify Credentials: Go to the Spotify Developer Dashboard, create an app, and copy your Client ID and Client Secret.

Crucial Step: Inside your Spotify App settings on the dashboard, add http://127.0.0.1:8888/callback into the Redirect URIs field and click Save.

2. Export Variables in your Terminal
Run these commands in your terminal before launching the script (replace with your actual keys):

``` bash
export YOUTUBE_API_KEY="AIzaSy..."
export SPOTIFY_CLIENT_ID="5b75c7..."
export SPOTIFY_CLIENT_SECRET="68a1e9..."
(Windows Users: use set instead of export in Command Prompt).
```

# 🚀 Step-by-Step Usage Guide
Once your environment variables are configured, follow these exact steps to run the script:

Step 1: Run the Script
Execute the script using Python:

``` bash
python3 yt_to_spotify.py
```

Step 2: Input Details
The script will prompt you for two inputs:

YouTube playlist link: Paste the full playlist URL (e.g., https://youtube.com/playlist?list=...).

Spotify playlist name: Type the name you want for your new Spotify playlist (e.g., LetoDie - MyPlay).

The tool will connect to YouTube and fetch all available videos (e.g., Success! 135 videos found via API).

Step 3: Authenticate with Spotify
Because open_browser is set to false to prevent Linux sandbox crashing, the script will generate a manual authorization link in the terminal looking like this:

Go to the following URL: [https://accounts.spotify.com/authorize?client_id=](https://accounts.spotify.com/authorize?client_id=)...
Enter the URL you were redirected to:
Copy that long https://accounts.spotify.com/authorize... link from your terminal.

Paste it into your web browser (e.g., Firefox/Chrome) and hit enter.

If prompted, log into your Spotify account and click Agree.

Step 4: Deal with the Redirect Link
After agreeing, your browser will attempt to load http://127.0.0.1:8888/callback?... and present a "Connection Error / Unable to Connect" page. This is normal and expected! Do not close it.

Go to your browser's address bar at the very top.

Select and copy the entire URL listed there. It must contain the validation code at the end (e.g., http://127.0.0.1:8888/callback?code=*****...).

Return to your active terminal, paste the full link into the prompt, and press Enter.

# 📊 Expected Output
The script will instantly read the token from memory, generate the private playlist on your account, and start parsing tracks with high precision:

```
Criando playlist 'YOURPLAYLIST' no Spotify...
Buscando as músicas de forma precisa no Spotify...
✔ Found: MUSIC - Artist
✔ Found: MUSIC - Artist
❌ Not found: Unreleased Session Video 2018
...
🎉 Playlist synced with maximum precision!
```
