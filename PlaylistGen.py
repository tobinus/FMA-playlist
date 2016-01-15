#!/usr/bin/env python3

from urllib.request import urlopen
import json
import random

def convert_duration(duration):
    try:
        duration = [int(d) for d in duration.split(':')]
        ret = duration.pop() # seconds
        duration.reverse()
        m = 1
        for d in duration:
            ret += d*m*60
            m += 1
        return ret
    except:
        return 42

API_KEY = '3T5ZTK9OOH36XO4F'
SETTINGS = [
    'limit=1000',
    'sort_by=track_interest',
    'sort_dir=desc',
    'commercial=1',
    'min_duration=00:01:00',
    'max_duration=00:10:00'

]
BASE_URL = 'https://freemusicarchive.org/api/get/tracks.json'

URL = '{base}?{settings}&api_key={api_key}'.format(base=BASE_URL, settings='&'.join(SETTINGS), api_key=API_KEY)

file = urlopen(URL)
data = file.readall().decode('utf-8')
file.close()

data = json.loads(data)

tracks = data['dataset']

random.shuffle(tracks)

with open('playlist.m3u8', 'w') as f:
    f.write('#EXTM3U\n')
    for track in tracks:
        f.write('\n#EXTINF:{duration}, {artist} - {title}\n'.format(
            duration = convert_duration(track['track_duration']),
            artist = track['artist_name'],
            title = track['track_title']))
        f.write('{url}/download\n'.format(url=track['track_url']))
