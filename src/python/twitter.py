#!/usr/bin/env python3

import requests
from requests_oauthlib import OAuth1
from os import environ


#########################
# twitter abstraction:
#########################

def init():
    twitter_app_token = environ.get("TWITTER_APP_TOKEN")
    twitter_app_secret = environ.get("TWITTER_APP_SECRET")
    auth = OAuth1(
            twitter_app_token,
            twitter_app_secret,
    )
    return auth

def fetch_tweets(
        auth,
        keywords,
        count = 15,
        max_id = None,
        since_id = None,
):
    """fetch up to 'count' tweets containing all 'keywords'
    if 'max_id' given, get only tweets with ids lower or eq
    """
    params = {
        "q": ' '.join(keywords),
        "count": count,

        # "until": "2020-05-09",
    }
    if max_id is not None:
        params["max_id"] = max_id
    if since_id is not None:
        params["since_id"] = since_id
    resp = requests.get(
            "https://api.twitter.com/1.1/search/tweets.json",
            params=params,
            auth=auth
    )
    resp.raise_for_status()
    json = resp.json()
    if len(json['statuses']) > 0:
        lowest_id = json['statuses'][-1]['id']
    else:
        lowest_id = None
    return (lowest_id, json)
