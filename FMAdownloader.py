#!/usr/bin/env python

from urllib2 import Request, urlopen
import urllib2
from json import loads
from os.path import isfile
from os import remove
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
tracks = loads(s.read())['dataset']
s.close()

for track in tracks:
    path = 'tracks/{file}'.format(file=track['track_file'].split('/')[-1])
    if isfile(path):
        print 'Already got {title}'.format(title=track['track_title'].encode('utf-8', errors='replace'))
        continue
    print 'Downloading {title}'.format(title=track['track_title'].encode('utf-8', errors='replace'))
    f = open(path, "wb")
    try:
        url = '{url}/download'.format(url=track['track_url'])
        s = urlopen(Request(url, None, headers))
        f.write(s.read())
    except:
        f.close()
        remove(path)
        print 'Error while downloading, removed track'
    finally:
        s.close()
    f.close()
