#!/usr/bin/env python

from __future__ import print_function, unicode_literals
try:
    # Try Python3
    from urllib.request import Request, urlopen
except ImportError:
    # Fall back to Python2
    from urllib2 import Request, urlopen
from json import loads
from os.path import isfile
from os import remove
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

# Keep track of how many iterations we must make
n = len(tracks)
# Number of digits to use, so the progress indication has the same length
number_width = str(int(log10(n)) + 1)

for i, track in enumerate(tracks):
    filename = track['track_file'].split('/')[-1]
    path = 'tracks/{file}'.format(file=filename)
    download_path = 'downloaded_tracks/{file}'.format(file=filename)

    # Print progress indication
    print(('{i:0' + number_width + '}/{n:0' + number_width + '} ').format(i=i+1, n=n), end="")

    if isfile(path) or isfile(download_path):
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
        print('Error while downloading, removed track')
    finally:
        s.close()
    f.close()
