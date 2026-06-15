## 🔑 How to Create the Required API Keys

This script interacts with both the YouTube and Spotify platforms. To use it, you must generate credentials from their official developer portals. Follow the step-by-step instructions below.

---

### 1. Setting Up the YouTube Data API v3

To fetch titles from your YouTube playlists, you need an API key from the Google Cloud Console.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. **Create a New Project**: Click on the project dropdown menu at the top of the page, select **New Project**, give it a name, and click **Create**.
3. **Enable the API**:
* Open the left sidebar menu and navigate to **APIs & Services** > **Library**.
* Search for **"YouTube Data API v3"**.
* Click on it and hit the **Enable** button.


4. **Create Credentials**:
* Once enabled, go to the **APIs & Services** > **Credentials** tab on the left.
* Click **+ Create Credentials** at the top and select **API Key**.


5. **Copy Your Key**: Your new API key will appear on the screen. Copy it safely; this will be your `YOUTUBE_API_KEY`.

---

### 2. Setting Up the Spotify Web API

To search for tracks and automatically build playlists, you need to register an application on the Spotify Developer Portal.

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in with your regular Spotify account.
2. **Create an App**: Click the **Create app** button in the top right corner.
3. **Fill Out App Details**:
* **App name**: Choose any name (e.g., `YT Playlist Sync`).
* **App description**: Write a brief summary (e.g., `Python script to sync playlists`).
* **Redirect URI**: **This step is critical.** You must enter exactly: `[http://127.0.0.1:8888/callback](http://127.0.0.1:8888/callback)`


4. **Save the App**: Check the terms of service agreement box and click **Save**.
5. **Collect Your Credentials**:
* Open your newly created application dashboard.
* Click on **Settings** (usually a gear icon or tab at the top).
* Here you will find your **Client ID**. Click **Show client secret** to view your **Client Secret**.


6. **Copy Credentials**: Save both strings safely; these will be your `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`.

---

### 🛡️ Security Best Practice Reminder

> **Never hardcode these keys directly into your script!** If you push your keys to a public GitHub repository, automated bots will scrape them immediately. Always store them as environment variables in your terminal session before launching the program, as shown in the main installation setup.
