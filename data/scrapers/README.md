# Scrapers

These are quick and dirty utilities made to scrape data from specific channels.

## music-from-spotify.py

Usage:

```shell
# get these from https://developer.spotify.com/dashboard
export SPOTIPY_CLIENT_ID="clientid"
export SPOTIPY_CLIENT_SECRET="clientsecret"
python3 scrapers/music-from-spotify.py >> music-data.yml`
```

You will need to clean up the output afterwards.

## music-from-soundcloud.py

Usage:

```shell
python3 scrapers/music-from-soundcloud.py >> music-data.yml`
```

You will need to clean up the output afterwards.

## videos-from-youtube.py

See https://developers.google.com/youtube/v3/quickstart/python for a guide on how to ge the credentials JSON. Save as YOUTUBE_SECRETS.json.

Usage:

```shell
pip3 install isodate google-api-python-client google-auth-oauthlib google-auth-httplib2
cd scrapers
python3 scrapers/videos-from-youtube.py`
```

Manually copy the data that is output.

You will need to clean up the output afterwards.
