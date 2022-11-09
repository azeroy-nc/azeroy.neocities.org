# coding: utf-8
"""
Utility to generate .yml file contents from Spotify data
"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

ARTIST_URL = 'https://open.spotify.com/artist/3xMSStWH6Wz2KAJqkZwXLu'
ACCOUNT = 'yabujin'

albums = sp.artist_albums(ARTIST_URL, album_type='album,single,compilation')

for album in albums['items']:
    if album["album_type"] == 'appears_on':
        continue
    print(f"{album['name'].lower().replace(' ', '-').replace('(', '').replace(')', '')}:")
    print(f'  title: {album["name"]}')
    print(f"     account: {ACCOUNT}")
    if album["total_tracks"] == 1:
        _type = 'single'
        print('  type: single')
    else:
        _type = 'album'
        print('  type: album # check')
    release_split = album["release_date"].split("-")
    release_date = f'[{release_split[0]}, {release_split[1].rjust(2, "0")}, {release_split[2].rjust(2, "0")}]'
    print(f'  release_date: {release_date}')
    print("  status: up")
    print("  links:")
    print(f'    "Spotify (official)": {album["external_urls"]["spotify"]}')
    if _type == 'album':
        print("  tracks:")
        tracks = sp.album_tracks(album["id"])
        for track in tracks['items']:
            print(f"    {track['name'].lower().replace(' ', '-')}:")
            print(f"      title: {track['name']}")
            print(f"      length: {int(track['duration_ms'] / 1000)}")
            print("      links:")
            print(f'        "Spotify (official)": {track["external_urls"]["spotify"]}')
    print("")
