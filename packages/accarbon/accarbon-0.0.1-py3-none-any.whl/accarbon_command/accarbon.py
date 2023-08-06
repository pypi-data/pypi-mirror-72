import sys
from urllib import request
from bs4 import BeautifulSoup

from .atcoder import url_validation, get_submission_id, get_submission_code, get_submission_info, get_tweet_title
from .carbon import get_lang_para, get_carbon_image
from .twitter import get_twitter, get_media_id, get_display_url, tweet


def get_soup(submission_url):
    html = request.urlopen(submission_url)
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def accarbon():
    # urlを入力として受け取る
    args = sys.argv
    if len(args) < 2:
        print('URL is needed')
        exit()
    submission_url = args[1]
    if url_validation(submission_url) is False:
        print('Invalid URL')
        exit()

    # AtCoderから必要な情報を取り出す
    soup = get_soup(submission_url)
    submission_code = get_submission_code(soup, submission_url)
    info = get_submission_info(soup, submission_url)
    lang_para = get_lang_para(info['lang'])

    # carbonの画像を取得
    image = get_carbon_image(submission_code, lang_para)

    # 画像をbotでアップロード
    twitter = get_twitter()
    media_id = get_media_id(twitter, image)
    display_url = get_display_url(
        twitter, media_id, get_submission_id(submission_url))

    # ツイート
    tweet_title = get_tweet_title(soup, submission_url)
    tweet(tweet_title, display_url)
