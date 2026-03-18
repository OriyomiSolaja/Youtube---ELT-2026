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
        #print(channel_playlistID)

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
    


#define main function for extracting data

def extract_video_data(video_ids):
    
    extracted_data = []
    
    #create a helper function to split the video id list into batches(the paramenter for video ids can only take up tp 50 video id)
    def batch_list(video_id_lst, batch_size):
        #define a for loop that will loop through the list and batches of size batch size
        for video_id in range(0,len(video_id_lst), batch_size):
            yield video_id_lst[video_id : video_id + batch_size]
    
    try:
     #loop through the whole list in batches, at each batch defining the concatenated video ID string using the Python Join method, which we will then use to build the url
        for batch in batch_list(video_ids, maxResults):
            #join video ids into a comma seperated string as per the docs
            video_ids_str = ",".join(batch)
            
            url = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}'
            
            response = requests.get(url)
    
            response.raise_for_status()
                
            data = response.json()
            
            for item in data.get('items', []):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails =item['contentDetails']
                statistics = item['statistics']
             
                #define dictionary that will take the variables from the loop above   
                video_data = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt": snippet['publishedAt'],
                    "duration": contentDetails['duration'],
                    "viewCount": statistics.get('viewCount', None),
                    "likeCount": statistics.get('likeCount', None),
                    "commentCount": statistics.get('commentCount', None)     
                }
                
                extracted_data.append(video_data)
        return extracted_data   
    except requests.exceptions.RequestException as e:
        raise e
if __name__=="__main__":
    playlistID = get_playlistID()
    video_ids = get_video_ids(playlistID)
    extract_video_data(video_ids)