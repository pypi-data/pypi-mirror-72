import json
import random
import webbrowser
from urllib import parse
from requests_oauthlib import OAuth1Session

from .env import API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def get_twitter():
    twitter = OAuth1Session(API_KEY, API_KEY_SECRET,
                            ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return twitter


def get_media_id(twitter, image):
    media_upload_url = 'https://upload.twitter.com/1.1/media/upload.json'
    files = {'media': image}
    res = twitter.post(media_upload_url, files=files)
    if res.status_code != 200:
        print('Can\'t upload media')
        exit()
    media_id = json.loads(res.text)['media_id_string']
    return media_id


def get_tweet_status(submission_id):
    return 'submission: ' + submission_id + '\n' + str(random.randrange(1000000000)) + '(rand)'


def get_display_url(twitter, media_id, submission_id):
    post_tweet_text = 'https://api.twitter.com/1.1/statuses/update.json'
    status = get_tweet_status(submission_id)
    params = {'status': status, 'media_ids': media_id}
    res = twitter.post(post_tweet_text, params=params)
    if res.status_code != 200:
        print('Can\'t post tweet')
        exit()
    display_url = json.loads(res.text)['entities']['media'][0]['display_url']
    return display_url


def tweet(tweet_title, display_url):
    open_twitter_url = 'https://www.addtoany.com/add_to/twitter?linkurl=' + \
        parse.quote(display_url) + '&linkname=' + \
        parse.quote(tweet_title) + '&linknote='
    webbrowser.open(open_twitter_url)
