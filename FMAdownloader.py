#!/usr/bin/env python

from __future__ import print_function, unicode_literals
try:
    # Try Python3
    from urllib.request import Request, urlopen
except ImportError:
    # Fall back to Python2
    from urllib2 import Request, urlopen
from json import loads
from os.path import isfile, basename
from os import remove, listdir
from math import log10

from settings import API_KEY

SETTINGS = [
    'limit=1000',
    'sort_by=track_interest',
    'sort_dir=desc',
    'commercial=1',
    'min_duration=00:01:30',
    'max_duration=00:10:00'
]

BASE_URL = 'https://freemusicarchive.org/api/get/tracks.json'

URL = '{base}?{settings}&api_key={api_key}'.format(base=BASE_URL, settings='&'.join(SETTINGS), api_key=API_KEY)

headers = {'User-Agent' : 'FMA-playlist 0.1'}
req = Request(URL, None, headers)
s = urlopen(req)
tracks = loads(s.read().decode('windows-1252'))['dataset']
s.close()

# What tracks must be downloaded?
top_track_filenames = set(
    [
    track['track_file'].split('/')[-1]
    for track in tracks
    ]
)
existing_tracks = set(
    [
    basename(filename)
    for filename in listdir('tracks')
    if isfile('tracks/' + filename) and not filename == '.dummy'
    ]
)
existing_downloaded_tracks = set(
    [
    basename(filename)
    for filename in listdir('downloaded_tracks')
    if isfile('downloaded_tracks/' + filename) and not filename == '.dummy'
    ]
)

already_downloaded = existing_tracks | existing_downloaded_tracks
to_be_downloaded = top_track_filenames - already_downloaded

tracks_to_be_removed = existing_tracks - top_track_filenames
downloaded_tracks_to_be_removed = existing_downloaded_tracks -\
    top_track_filenames

# Get list with all information about the tracks, not just their filenames
tracks_to_download = [
    track
    for track in tracks
    if track['track_file'].split('/')[-1] in to_be_downloaded
]

if tracks_to_download:
    # Keep track of how many iterations we must make
    n = len(tracks_to_download)
    # Number of digits to use, so the progress indication has the same length
    number_width = str(int(log10(n)) + 1)

    # Download the new tracks
    for i, track in enumerate(tracks_to_download):
        filename = track['track_file'].split('/')[-1]
        path = 'tracks/{file}'.format(file=filename)
        download_path = 'downloaded_tracks/{file}'.format(file=filename)

        # Print progress indication
        print(('{i:0' + number_width + '}/{n:0' + number_width + '} ').format(i=i+1, n=n), end="")

        if isfile(path) or isfile(download_path):
            # This should never be executed, but just in case we end up
            # running in parallel and someone else downloaded it before us,
            # it doesn't hurt to check
            print('Already got {title}'.format(title=track['track_title']))
            continue
        print('Downloading {title}'.format(title=track['track_title']))
        f = open(download_path, "wb")
        try:
            url = '{url}/download'.format(url=track['track_url'])
            s = urlopen(Request(url, None, headers))
            f.write(s.read())
        except:
            f.close()
            remove(download_path)
            print('Error while downloading {url}, removed track'
                .format(url=track['track_url']))
        finally:
            s.close()
        f.close()
else:
    print("No tracks to download.")

# Remove old tracks
paths_to_remove = [
    'tracks/{file}'.format(file=filename)
    for filename in tracks_to_be_removed
]
paths_to_remove.extend([
    'downloaded_tracks/{file}'.format(file=filename)
    for filename in downloaded_tracks_to_be_removed
])

if paths_to_remove:
    n = len(paths_to_remove)
    number_width = str(int(log10(n)) + 1)

    print("\nRemoving tracks that are no longer part of the search")

    for i, path in enumerate(paths_to_remove):
        print(('{i:0' + number_width + '}/{n:0' + number_width + '} ' +
            'Removing {path}').format(i=i+1, n=n, path=path))
        try:
            remove(path)
        except:
            print('Error while removing')
else:
    print("No tracks to remove.")

