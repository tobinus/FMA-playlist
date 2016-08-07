#FMA-playlist

Generate a playlist from the Free Music Archive API.

## Features

* Download mp3 files from the 
  [Free Music Archive](http://freemusicarchive.org/) and 
  place them in a dedicated folder.
* Strip silence from the start and end of the files.

## Setting up

The instructions assume you're using something similar to Ubuntu and are
somewhat familiar with Linux.

1.  Install dependencies.

    `sudo apt-get install sox libsox-fmt-mp3`

2.  Clone this repository and `cd` into it.

3.  Customize your criteria by editing `FMAdownloader.py`. By default, the top
    1000 tracks available for commercial use are chosen.

4.  Run the program for the first time.

    `make run`

    You will first be prompted for an API key, which you can obtain by
    reading and agreeing to [FMA API ToS](https://freemusicarchive.org/api/agreement).
    The key will be saved to `settings.py` and will be reused on further runs.
    Create `settings.py` with the appropriate content _before_ running the program
    if you cannot use the prompt (e.g. during automated installation).
    
    Next, all tracks will be downloaded to `downloaded_tracks/`, one at a time 
    (so we're not a burden for FMA). After that, they will have silence 
    removed from either end of them before they're moved to `tracks/`.

5.  Optional: to add new tracks as the search result changes over time, add
    `make run` to your crontab.

    `crontab -e`

    Add a line which runs `make run` once every month or so, like this:

    `0 10 1 * * make -C /path/to/FMA-playlist run > /path/to/FMA-playlist/runlog.log 2>&1`

    in which you replace `/path/to/FMA-playlist` with the actual path to this
    directory. (As a side note, you might want to remove the redirects if you want an
    email each time the job is run, and thus confirm that it works.)

Once you've done all this, the `tracks/` directory can be used as a playlist
of music from the Free Music Archive. Example of how to use it with [LiquidSoap][ls]:

```
fma = playlist("/path/to/FMA-playlist/tracks")
fma = normalize(fma, gain_max=1000.0, target=-1.0, window=2.0)
fma = nrj(fma)
fma = smart_crossfade(fma)
fma = strip_blank(max_blank=12., threshold=-80., track_sensitive=false, fma)
# Remember that fma is fallible; use mksafe if you want to output it directly
# Also use some mechanism to attribute the artist (you must follow the CC licenses!)
```

[ls]: http://savonet.sourceforge.net/index.html

