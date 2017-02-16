from config import *
import requests

# class TwitchStream:
#     def __init__(self, game='Counter-Strike: Global Offensive'):
#         self._game = game
#
#     @classmethod
#     def _get(cls, game='', endpoint='', **kwargs):
#         url = 'https://api.twitch.tv/kraken/' + endpoint
#         headers = {'Client-ID': twitch_client_id}
#         params = kwargs
#         params['game'] = 'Counter-Strike: Global Offensive'
#         return requests.get(url, headers=headers, params=kwargs)
#
#     @classmethod
#     def get_streams(cls, live='live', limit=10):
#         res = cls._get(endpoint='streams', live=live, limit=limit).json()
#         print(res['_total'])
#         print(len(res))


# t = TwitchStream()
# x = t.get_streams()

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

    def __init__(self, auth=None):
        '''
        Create API object.
        :param auth: An authorization token (optional)
        '''
        self.prefix = 'https://api.twitch.tv/kraken/'
        self._auth_headers = {'Client-ID': twitch_client_id}


    def _get(self, url, args=None, payload=None, **kwargs):
        if args:
            kwargs.update(args)
        kwargs['game'] = 'Counter-Strike: Global Offensive'
        retries = self.max_get_retries
        delay = 1
        url = self.prefix + 'streams'
        return requests.get(url, headers=self._auth_headers, params=kwargs)
        # while retries > 0:
        #     try:
        #         return requests.get(url=self.prefix, params=kwargs)
        #     except TwitchException as e:
        #         retries -= 1
        #         status = e.http_status
        #         # 429 is rate limit
        #         if status == 429 or (status >= 500 and status < 600):
        #             if retries < 0:
        #                 raise
        #             else:
        #                 sleep_seconds = int(e.headers.get('Retry-After', delay))
        #                 print ('retrying ...' + str(sleep_seconds) + 'secs')
        #                 time.sleep(sleep_seconds + 1)
        #                 delay += 1
        #         else:
        #             raise
        #     except Exception as e:
        #         raise
        #         print ('exception', str(e))
        #         # some other exception. Requests have
        #         # been know to throw a BadStatusLine exception
        #         retries -= 1
        #         if retries >= 0:
        #             sleep_seconds = int(e.headers.get('Retry-After', delay))
        #             print ('retrying ...' + str(delay) + 'secs')
        #             time.sleep(sleep_seconds + 1)
        #             delay += 1
        #         else:
        #             raise

t = Twitch()
r = t._get('')
print(r.json())
