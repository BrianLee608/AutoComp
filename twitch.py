from config import *
import requests


class TwitchException(Exception):
    def __init__(self, http_status, code, msg):
        self.http_status = http_status
        self.code = code
        self.msg = msg

    def __str__(self):
        return 'http status: {0}, code:{1} - {2}'.format(
            self.http_status, self.code, self.msg)

class Twitch:
    max_get_retries = 10

    def __init__(self):
        ''' Create a Twitch API Object '''

        self.prefix = 'https://api.twitch.tv/kraken/'
        self._auth_headers = {'Client-ID': twitch_client_id}

    def _get(self, endpoint, **kwargs):
        url = self.prefix + endpoint
        return requests.get(url, headers=self._auth_headers, params=kwargs)

    def get_channel(self, channel):
        # for now, i can't get channel by _id.. so just use channel name
        r = self._get('channels/' + str(channel))
        return r.json()

    def get_stream(self, channel):
        r = self._get('streams/' + str(channel))
        return r.json()

    def get_live_streams(self, game=None, **kwargs):
        r = self._get('streams/', **kwargs).json()
        streams = r['streams']
        return [s for s in streams if self._valid_stream(s)]

    def _valid_stream(self, stream):
        # channel must be live and at least 300 viewers
        return stream['channel']['status'] and stream['viewers'] >= 300
        return True

    def get_viewers(self, channel):
        return self.get_stream(channel)['stream']['viewers']

# t = Twitch()
# # r = t.get_live_streams(game='Counter-Strike: Global Offensive', limit=2)
# r = t.get_channel('dreamhackcs')
#
# print(r)
