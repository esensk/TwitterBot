import argparse
import oauth2 as oauth
import twython
import webbrowser as web

from conf import TOKENS

TWITTER_OAUTH_URL = 'https://twitter.com/oauth/'
REQUEST_TOKEN_URL = TWITTER_OAUTH_URL + 'request_token'
ACCESS_TOKEN_URL = TWITTER_OAUTH_URL + 'access_token'
AUTHENTICATE_URL = TWITTER_OAUTH_URL + 'authorize'

OAUTH_TOKEN = 'oauth_token'
OAUTH_TOKEN_SECRET = 'oauth_token_secret'


def parse_url(url):
    param = {}
    for i in url.split('&'):
        p = i.split('=')
        print(p)
        param.update({p[0]: p[1]})

    return param


def get_request_token_through_web():
    consumer = oauth.Consumer(key=TOKENS['consumer_key'], secret=TOKENS['consumer_secret'])
    client = oauth.Client(consumer)
    resp, content = client.request(REQUEST_TOKEN_URL, 'GET')
    print('取得したtoken')
    print(resp, content)
    print('----')

    request_token = dict(parse_url(content.decode('utf-8')))
    print('tokenを辞書化')
    print(request_token)
    print('----')

    url = AUTHENTICATE_URL + '?' + OAUTH_TOKEN + '=' + request_token[OAUTH_TOKEN]
    web.open(url)


def get_access_token(oauth_token, oauth_verifier):
    consumer = oauth.Consumer(key=TOKENS['consumer_key'], secret=TOKENS['consumer_secret'])
    token = oauth.Token(oauth_token, oauth_verifier)

    client = oauth.Client(consumer, token)
    resp, content = client.request(ACCESS_TOKEN_URL, 'POST', body='oauth_verifier={0}'.format(oauth_verifier))

    return content


def tweet(access_token_content):
    token = dict(parse_url(access_token_content.decode('utf-8')))
    twitter = twython.Twython(TOKENS['consumer_key'], TOKENS['consumer_secret'], token[OAUTH_TOKEN], token[OAUTH_TOKEN_SECRET])
    try:
        twitter.update_status(status='test')
    except twython.TwythonError as e:
        print(e)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--when_get_token', default='false')

    args = parser.parse_args()
    return args


def lambda_handler():
    tweet(get_access_token(TOKENS['oauth_token'], TOKENS['oauth_verifier']))


def main():
    args = get_args()

    when_get_token = args.when_get_token
    assert when_get_token == 'true' or when_get_token == 'false', '--when_get_token is in [true, false]'

    if args.when_get_token == 'true':
        get_request_token_through_web()

    else:
        c = get_access_token(TOKENS['oauth_token'], TOKENS['oauth_verifier'])
        tweet(c)


if __name__ == '__main__':
    main()
