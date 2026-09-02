import requests
import json
import os
from dotenv import load_dotenv
from datetime import date
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

def extract_video_stats(video_ids):
    extracted_data=[]

    def batch_list(lst, batch_size):
        for i in range(0, len(lst), batch_size):
            yield lst[i:i + batch_size]
    video_stats= []
    for video_id in video_ids:
        url= f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_id}&key={api_key}"
        try:
            for batch in batch_list(video_ids, max_results):
                batch_ids= ",".join(batch)
                url= f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={batch_ids}&key={api_key}"
                response= requests.get(url)
                response.raise_for_status()
                data= response.json()
                #items= data.get("items", [])
                for item in data.get("items", []):
                    video_id= item["id"]
                    snippet= item["snippet"]
                    statistics= item["statistics"]
                    content_details= item["contentDetails"]


                    video_data={
                        "title": snippet["title"],
                        "description": snippet["description"],
                        "published_at": snippet["publishedAt"],
                        "view_count": statistics.get("viewCount", 0),
                        "like_count": statistics.get("likeCount", 0),
                        "comment_count": statistics.get("commentCount", 0)
                    }
                    video_stats.append(video_data)
            return video_stats

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while making the request for video ID {video_id}: {e}")

def save_video_stats_to_json(video_stats):
    filename=f"./data/video_stats_{date.today().strftime('%Y-%m-%d')}.json"
    try:
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(video_stats, json_file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error occurred while saving video stats to JSON file: {e}")

if __name__ == "__main__":
    playlist_id= get_playlistid()
    if playlist_id:
        print(f"Playlist ID for channel '{channel_handle}': {playlist_id}")
        video_ids= get_video_ids(playlist_id)
        if video_ids:
            print(f"Retrieved {len(video_ids)} video IDs.")
            video_stats= extract_video_stats(video_ids)
            if video_stats:
                print(f"Extracted stats for {len(video_stats)} videos.")
                save_video_stats_to_json(video_stats)
            else:
                print("Failed to extract video stats.")
        else:
            print("Failed to retrieve video IDs.")
    else:
        print("Failed to retrieve the playlist ID.")
else:
    print("This script is being imported as a module.")
