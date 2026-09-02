import requests
import json
import os
from dotenv import load_dotenv
load_dotenv("./.env")
api_key= os.getenv("youtube_api_key")
channel_handle= "CoComelon"

def get_playlistid():

    try:
        url= f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={api_key}"

        response= requests.get(url)
        response.raise_for_status()

        data= response.json()
        channel_items=data["items"][0]

        channel_playlistid=channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        return channel_playlistid
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the request: {e}")
        return None

if __name__ == "__main__":
    playlist_id= get_playlistid()
    if playlist_id:
        print(f"Playlist ID for channel '{channel_handle}': {playlist_id}")
    else:
        print("Failed to retrieve the playlist ID.")
else:
    print("This script is being imported as a module.")
