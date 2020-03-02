
import os
import googleapiclient.discovery
from yt_play import vidcon_serv

def playlist_serv(inputId, numResult):
    
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ.get('YT_KEY')

    if len(inputId.split('=')) == 3:
        playId = '{}' .format(inputId.split('=')[2])

    elif len(inputId.split('=')) == 2:
        playId = '{}' .format(inputId.split('=')[1])

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=numResult,
        playlistId=playId
    )
    response = request.execute()
    list_str = response

    results_list = []

    for result in list_str['items']:
        vid_raw = vidcon_serv(result['snippet']['resourceId']['videoId'])
        vid_title = vid_raw['items'][0]['snippet']['title']
        vid_view = vid_raw['items'][0]['statistics']['viewCount']
        vid_like = vid_raw['items'][0]['statistics']['likeCount']
        vid_dislike = vid_raw['items'][0]['statistics']['dislikeCount']

        vid_data = {
            'title': vid_title,
            'views': vid_view,
            'likes': vid_like,
            'dislikes': vid_dislike
            }

        results_list.append(vid_data)

    return results_list
    
