import json


FLIGHTS_API_PATTERN = ('https://data-live.flightradar24.com/zones'
                       '/fcgi/feed.js?bounds={},{},{},{}'
                       '&faa=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1'
                       '&estimated=1&maxage=14400&gliders=1&stats=1')

HEADERS = {'Connection': 'keep-alive',
           'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; '
                          'x64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome')}

API_STRING = ("https://data-live.flightradar24.com/clickhandler/?flight={flight_id}")

