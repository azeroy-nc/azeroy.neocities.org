# -*- coding: utf-8 -*-

# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import isodate
import datetime

#CHANNEL_ID = "UC5Inc-RJGL9LGDDD-0CCtmA"
#CHANNEL_REF = 'gyrotta'

CHANNEL_ID = "UCTa23iZGmKYdyQ_hijXl3bg"
CHANNEL_REF = 'yabujin'

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "YOUTUBE_SECRETS.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.search().list(
        part="snippet",
        channelId=CHANNEL_ID,
        type="video",
        maxResults=25
    )
    response = request.execute()

    ids = []
    for v in response['items']:
        ids.append(v['id']['videoId'])

    print(','.join(ids))

    vid_request = youtube.videos().list(
        part="snippet,status,contentDetails,statistics,id",
        id=','.join(ids)
    )
    vid_response = vid_request.execute()

    datestring = datetime.datetime.now().strftime("[%Y, %m, %d]")

    for video in vid_response['items']:
        #print(vid_response)

        print("id-fixme:")
        print(f"  title: {video['snippet']['title']}")
        print(f"  account: {CHANNEL_REF}")
        print(f"  length: {isodate.parse_duration(video['contentDetails']['duration']).total_seconds()}")
        print("  type: misc # check")
        print(f"  original_description: {video['snippet']['description'] or 'None'}")
        print("  status: up")
        print(f"  views: [{video['statistics']['viewCount']}, {datestring}]")
        print(f"  release_date: {datetime.datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('[%Y, %m, %d]')}")
        print("  links:")
        print(f'    "YouTube (official)": https://youtube.com/watch?v={video["id"]}')
        print("")

if __name__ == "__main__":
    main()
