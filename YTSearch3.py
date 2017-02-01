# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 15:24:11 2016

@author: ebiw
"""
#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import sys
import pandas as pd #pip install pandas
import matplotlib as plt
import json
import csv
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyAPY7J0-a8ci4LF8S7ssIkMP5cjRfFCu3k"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)
def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    #part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []
  res = []
  k = []
  v = []
  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#channel":
        #videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]
#==============================================================================
        videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
        k.append("%s " % (search_result["id"]["channelId"]))
        v.append("%s " % (search_result["snippet"]["title"]))
#==============================================================================
#==============================================================================
#     elif search_result["id"]["kind"] == "youtube#channel":
#       channels.append("%s (%s)" % (search_result["snippet"]["title"],
#                                    search_result["id"]["channelId"]))
#     elif search_result["id"]["kind"] == "youtube#playlist":
#       playlists.append("%s (%s)" % (search_result["snippet"]["title"],
#                                     search_result["id"]["playlistId"]))
#==============================================================================
  uprint("Videos:\n", "\n".join(videos), "\n")
  uprint("Ks:\n", "\n".join(k), "\n")
  uprint("Vs:\n", "\n".join(v), "\n")
#==============================================================================
#   uprint("Videos:\n", "\n".join(videos), "\n")
#   uprint("Channels:\n", "\n".join(channels), "\n")
#   uprint("Playlists:\n", "\n".join(playlists), "\n")
#==============================================================================
  #s = ','.join(videos.keys())
  s = ','.join(k)
  print("Printing s val", s)
  videos_list_response = youtube.channels().list(
     id=s,
     part='id,statistics'
  ).execute()
  #videos_list_response['items'].sort(key=lambda x: int(x['statistics']['likeCount']), reverse=True)
  res = pd.read_json(json.dumps(videos_list_response['items']))
  uprint(res)
#==============================================================================
#   with open("chdump", "w", encoding="utf8") as output_file:
#         print("Start of dumps")
#         json.dump(videos_list_response['items'], output_file)
#         print("End of dumps")
#==============================================================================
  jsonobj = json.dumps(videos_list_response['items'])
 
  x = json.loads(jsonobj)
  f = csv.writer(open("channels_.csv", "w",newline=''))
# Write CSV Header, If you dont need that, remove this line
  f.writerow(["kind", "id", "viewCount", "hiddenSubscriberCount", "commentCount","videoCount","subscriberCount"])
  for x in x:
    f.writerow([x["kind"],
                x["id"],
                x["statistics"]["viewCount"],
                x["statistics"]["hiddenSubscriberCount"],
                x["statistics"]["commentCount"],
                x["statistics"]["videoCount"],
                x["statistics"]["subscriberCount"]])

if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="Krittibas Bhattacharya")
  argparser.add_argument("--max-results", help="Max results", default=50)
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError as e:
    print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
