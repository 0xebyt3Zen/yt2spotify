import os
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import MemoryCacheHandler
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs

# --- CONFIGURATIONS VIA ENVIRONMENT VARIABLES ---
# Credentials are now securely pulled from the operating system.
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', 'YOUR_YOUTUBE_API_KEY_HERE')
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', 'YOUR_SPOTIFY_CLIENT_ID_HERE')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', 'YOUR_SPOTIFY_CLIENT_SECRET_HERE')

# Standard loopback callback URL recommended by Spotify
SPOTIFY_REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SCOPE = 'playlist-modify-private playlist-modify-public'

# --- FUNCTIONS ---

def extract_playlist_id(url):
    """Extracts the playlist ID from a URL safely using urllib."""
    try:
        parsed_url = urlparse(url)
        url_values = parse_qs(parsed_url.query)
        if 'list' in url_values:
            return url_values['list'][0]
    except Exception:
        pass
    return None

def extract_youtube_titles_api(playlist_url):
    """Uses the official YouTube API to fetch video titles."""
    if YOUTUBE_API_KEY in ['YOUR_YOUTUBE_API_KEY_HERE', '']:
        print("❌ Error: Please set the YOUTUBE_API_KEY environment variable.")
        return []

    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print("❌ Could not find a valid playlist ID in the provided URL.")
        return []

    print(f"Playlist ID successfully identified: {playlist_id}")
    print("Fetching tracks via official YouTube API...")
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    titles = []
    next_page_token = None
    
    try:
        while True:
            res = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            
            for item in res.get('items', []):
                title = item['snippet']['title']
                if title not in ['Deleted video', 'Private video']:
                    titles.append(title)
            
            next_page_token = res.get('nextPageToken')
            if not next_page_token:
                break
                
        print(f"Success! {len(titles)} videos found via API.")
        return titles
    except Exception as e:
        print(f"Error accessing YouTube API: {e}")
        return []

def clean_youtube_title(title):
    """Removes classic YouTube title clutter to improve search accuracy."""
    # Removes anything inside parentheses or brackets (e.g., [Official Music Video])
    term = re.sub(r'[\(\[][^\]\)]*[\)\]]', '', title)
    # Removes common video marketing tags
    tags = ['official', 'officiel', 'clipe', 'video', 'vídeo', 'lyric', 'audio', 'áudio', 'prod.', 'remix']
    for tag in tags:
        term = re.sub(re.escape(tag), '', term, flags=re.IGNORECASE)
    return ' '.join(term.split()).strip()

def search_and_add_to_spotify(track_titles, spotify_playlist_name):
    """Authenticates with Spotify, creates the playlist, and adds the tracks accurately."""
    if SPOTIFY_CLIENT_ID in ['YOUR_SPOTIFY_CLIENT_ID_HERE', ''] or SPOTIFY_CLIENT_SECRET in ['YOUR_SPOTIFY_CLIENT_SECRET_HERE', '']:
        print("❌ Error: Please set your Spotify credentials (ID and SECRET).")
        return

    auth_manager = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE,
        open_browser=False,
        cache_handler=MemoryCacheHandler()
    )
    
    sp = spotipy.Spotify(auth_manager=auth_manager)
    user_id = sp.current_user()['id']
    
    print(f"Creating playlist '{spotify_playlist_name}' on Spotify...")
    new_playlist = sp.user_playlist_create(user=user_id, name=spotify_playlist_name, public=False)
    playlist_id = new_playlist['id']
    
    track_uris = []
    print("Searching tracks precisely on Spotify...")
    
    for original_title in track_titles:
        clean_title = clean_youtube_title(original_title)
        
        # 🛠️ SMART SEARCH STRATEGY:
        # If the title contains a hyphen "-", it usually means "Artist - Track"
        if " - " in clean_title:
            parts = clean_title.split(" - ", 1)
            artist = parts[0].strip()
            track = parts[1].strip()
            search_query = f'track:"{track}" artist:"{artist}"'
        else:
            # Fallback if no hyphen is present, prioritizing the main artist (e.g., LetoDie)
            search_query = f'track:"{clean_title}" artist:"LetoDie"'
            
        # First attempt: Strict field-restricted search
        result = sp.search(q=search_query, limit=1, type='track')
        tracks = result['tracks']['items']
        
        # Second attempt: If strict search fails, try broad intelligent search
        if not tracks:
            if " - " in clean_title:
                result = sp.search(q=clean_title, limit=1, type='track')
                tracks = result['tracks']['items']
            else:
                result = sp.search(q=f"{clean_title} LetoDie", limit=1, type='track')
                tracks = result['tracks']['items']

        # If track is found, append URI
        if tracks:
            track_uris.append(tracks[0]['uri'])
            print(f"✔ Found: {tracks[0]['name']} - {tracks[0]['artists'][0]['name']}")
        else:
            print(f"❌ Not found: {original_title}")
            
    if track_uris:
        print(f"\nAdding {len(track_uris)} tracks to the playlist...")
        for i in range(0, len(track_uris), 100):
            sp.playlist_add_items(playlist_id, track_uris[i:i+100])
        print("🎉 Playlist synced with maximum precision!")
    else:
        print("No matching tracks were found on Spotify.")

# --- EXECUTION ---
if __name__ == "__main__":
    youtube_url = input("Enter the YouTube playlist link: ").strip()
    playlist_name = input("Enter a name for your new Spotify playlist: ").strip()
    
    if youtube_url and playlist_name:
        songs = extract_youtube_titles_api(youtube_url)
        if songs:
            search_and_add_to_spotify(songs, playlist_name)
    else:
        print("Please fill out all fields.")
