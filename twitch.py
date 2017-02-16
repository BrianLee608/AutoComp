from config import *
import requests

class TwitchStream:
    def __init__(self, game='Counter-Strike: Global Offensive'):
        self._game = game

    @classmethod
    def _get(cls, game='', endpoint='', **kwargs):
        url = 'https://api.twitch.tv/kraken/' + endpoint
        headers = {'Client-ID': twitch_client_id}
        params = kwargs
        params['game'] = 'Counter-Strike: Global Offensive'
        return requests.get(url, headers=headers, params=kwargs)

    @classmethod
    def get_streams(cls, live='live', limit=10):
        res = cls._get(endpoint='streams', live=live, limit=limit).json()
        print(res['_total'])
        print(len(res))

# fix these classmethods

t = TwitchStream()
x = t.get_streams()
