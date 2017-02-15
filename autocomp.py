from config import *
from datetime import datetime, timedelta
import glob
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os.path
import praw
import re
import youtube_dl

# register with Reddit as script app
reddit = praw.Reddit(client_id = client_id,
                     client_secret = client_secret,
                     password = password,
                     user_agent = user_agent,
                     username = username)

yt_re = re.compile('^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$')
twitch_re = re.compile('^(https?\:\/\/)?(clips.twitch.tv)\/\w+\/.+')
# alternatively we can check domains instead of doing regex but
# I did not verify that reddit's submission object will always return
# a non-None domain attribute
# domains = {'youtube.com', 'youtu.be', 'clips.twitch.tv'}

n_days_ago = datetime.now() - timedelta(days=7)

def get_threads(subreddit, max_dls=10, limit=25):
    """ Get a list of threads whose contents are twitch or YT clips """

    sub = reddit.subreddit(subreddit)
    vod_urls = set()

    for th in sub.new(limit=limit):
        if len(vod_urls) > max_dls:
            break
        if (yt_re.match(th.url) or twitch_re.match(th.url)) and \
                datetime.fromtimestamp(th.created) >= n_days_ago:
            vod_urls.add(th.url)
            max_dls += 1

    return vod_urls

def _get_dt(date):
    """ YYYYMMDD => datetime object """

    year, month, day = int(date[:4]), int(date[4:6]), int(date[6:])
    return datetime(year, month, day)

def _video_meets_criteria(info):
    """ Ensure that video meets criteria """

    # extractor_key gives domain of url.
    # yt-dl does not support upload_date and duration for twitch domains
    # so for now, let all twitch clips through. They're usually short anyways
    if info.get('extractor_key', None) == 'Youtube':
        dt = _get_dt(info.get('upload_date', None))
        # vid must be less than 7 days ago and less than 120 sec
        if dt > n_days_ago or info.get('duration', 0) > 120:
            return False

    return True

# Youtube object keys
# dict_keys(['uploader_url', 'dislike_count', 'playlist', 'duration', 'format',
 # 'view_count', 'series', 'extractor_key', 'description', 'filesize', 'title',
 #  'episode_number', 'formats', 'like_count', 'ext', 'tbr', 'playlist_index', 'url',
 #   'season_number', 'tags', 'display_id', 'id', 'average_rating', 'automatic_captions', 'webpage_url_basename', 'start_time', 'extractor',
 #    'preference', 'age_limit', 'protocol', 'end_time', 'abr', 'thumbnail',
 #     'annotations', 'uploader', 'requested_subtitles', 'http_headers', 'license',
 #      'acodec', 'creator', 'uploader_id', 'vcodec', 'categories', 'thumbnails',
 #       'subtitles', 'format_id', 'alt_title', 'webpage_url', 'format_note', 'is_live',
 #        'player_url', 'upload_date'])
#
# Twitch object keys
# dict_keys(['webpage_url_basename', 'playlist', 'extractor', 'id', 'extractor_key',
 # 'uploader', 'http_headers', 'title', 'thumbnail', 'height', 'thumbnails', 'requested_subtitles', 'protocol', 'formats', 'ext', 'uploader_id', 'format',
 #  'creator', 'playlist_index', 'format_id', 'display_id', 'url', 'webpage_url'])

def download(vod_urls, savedir='./'):
    """ Download the vids in the iterable, vod_urls, to the filesystem """

    opts = {
        'format': 'bestaudio/best', # best quality
        'outtmpl': savedir + '%(title)s.%(ext)s', # output
        'noplaylist' : True, # skip playlist dls jsut in case
        'ignoreerrors': True, # ignore errors like private,age restr, etc..
        'nooverwrites': True, # don't overwrite pre-existing files
        'quiet': True, # no printing to std out
    }

    with youtube_dl.YoutubeDL(opts) as ydl:
        for v in vod_urls:
            try:
                info = ydl.extract_info(v, download=False)
                # sometimes videos are blocked/private so ignore them
                if info is None:
                    continue
                if _video_meets_criteria(info):
                    ydl.download([v])
            except Error as e:
                pass

# files = glob.glob(os.path.join(dir, '*.mp4'))

# clips = [VideoFileClip(f) for f in files]
# final_clip = concatenate_videoclips(clips)
# final_clip.fps = 30
# final_clip.write_videofile("my_concatenation.mp4")

if __name__ == '__main__':
    vod_urls = get_threads('GlobalOffensive', max_dls=2, limit=25)
    savedir = './media/'
    download(vod_urls, savedir)
