import requests
import json
import os
from dotenv import load_dotenv
load_dotenv("./.env")
api_key= os.getenv("youtube_api_key")
channel_handle= "CoComelon"
max_results= 50

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


def get_video_ids(playlistid):
    base_url= f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlistid}&key={api_key}"
    pageToken= None
    video_ids= []
    try:
        while True:
            url= base_url
            if pageToken:
                url += f"&pageToken={pageToken}"

            response= requests.get(url)
            response.raise_for_status()

            data= response.json()
            items= data.get("items", [])
            for item in items:
                video_id= item["contentDetails"]["videoId"]
                video_ids.append(video_id)

            pageToken= data.get("nextPageToken")
            if not pageToken:
                break
        return video_ids

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the request: {e}")
        return None


if __name__ == "__main__":
    playlist_id= get_playlistid()
    if playlist_id:
        print(f"Playlist ID for channel '{channel_handle}': {playlist_id}")
        video_ids= get_video_ids(playlist_id)
        if video_ids:
            print(f"Video IDs for channel '{channel_handle}': {video_ids}")
        else:
            print("Failed to retrieve video IDs.")
    else:
        print("Failed to retrieve the playlist ID.")
else:
    print("This script is being imported as a module.")
