import requests
import json

import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
maxResults = 50

def get_playlistID():
    
    try:
    
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url)
    
        response.raise_for_status()
        
        data = response.json()
        #print(json.dumps(data,indent=4))

        channel_items = data["items"][0]
        
        channel_playlistID = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlistID)

        return channel_playlistID
    
    except requests.exceptions.RequestException as e:
        raise e
   


def get_video_ids(playlistID):
    
    #initialise container for all videos id as an emtpty list
    video_ids = []
    
    #create page token variable and initialise to None 
    pagetoken = None
    
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistID}&key={API_KEY}"  
    
    try:
        #start a loop that will break when there are no more page token to go through(the first iteration will be false)
        while True:
            
            url = base_url
            
            if pagetoken:
                #if a pagetoken is returned the url will append the page token part to the main url
                url += f"&pageToken={pagetoken}"
                
            response = requests.get(url)
    
            response.raise_for_status()
                
            data = response.json()
                
                #get the value from the item scheme, use for loop to loop through the item scheme
            for item in data.get("items", []):
                video_id = item["contentDetails"]['videoId']
                video_ids.append(video_id)
                    
            pagetoken = data.get('nextPageToken')
                
            if not pagetoken:
                break
            
        return video_ids
        
    except requests.exceptions.RequestException as e:
        raise e
    
if __name__=="__main__":
    playlistID = get_playlistID()
    get_video_ids(playlistID)