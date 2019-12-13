
import os
import googleapiclient.discovery

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyB7soJskc5W7mXFZCB_n3RqTmVvh31OnvY"

def search_serv(q, numResult, sortOrder):

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.search().list(
        type="video",
        order=sortOrder,
        part="snippet",
        maxResults=numResult,
        q=q
    )
    response = request.execute()

    return response

def vidcon_serv(id):

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=id
    )
    response = request.execute()

    return response

def playlist_serv(inputId, numResult):

    playId = '{}' .format(inputId.split('=')[2])

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=numResult,
        playlistId=playId
    )
    response = request.execute()

    return response