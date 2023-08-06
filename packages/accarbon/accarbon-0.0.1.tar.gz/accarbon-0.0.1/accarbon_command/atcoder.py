import re


def url_validation(url):
    m = re.fullmatch(
        r'https://atcoder.jp/contests/\w+/submissions/\d+(\?lang=(ja|en))?', url)
    if m is None:
        return False
    else:
        return True


def get_submission_id(url):
    tmp = re.split('[/?]', url)
    if tmp[-1][0:4] == 'lang':
        return tmp[-2]
    else:
        return tmp[-1]


def get_submission_code(soup, submission_url):
    submission_code = soup.find(id='submission-code').get_text()
    return submission_code


def get_submission_info(soup, submission_url):
    tc = soup.find_all(class_='text-center')
    info = {
        'problem': tc[1].get_text(),
        'user': tc[2].get_text(),
        'lang': tc[3].get_text(),
        'length': tc[5].get_text(),
        'result': tc[6].get_text(),
        'time': tc[7].get_text(),
    }
    return info


def get_contest_title(soup, submission_url):
    title = soup.find(class_='contest-title').get_text()
    return title


def get_tweet_title(soup, submission_url):
    tweetinfo = soup.find(class_='a2a_kit')
    tweet_title = tweetinfo.get('data-a2a-title') + \
        ' ' + tweetinfo.get('data-a2a-url')
    return tweet_title
