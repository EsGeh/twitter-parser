#!/usr/bin/env python3


import psycopg2
import requests
from requests_oauthlib import OAuth1
from os import environ


#########################
# database abstraction:
#########################

def init_db():
    connection = psycopg2.connect(
        host = "twitter_parser_db",
        user = "postgres",
        database = "db",
    )
    connection.autocommit = True
    return connection

def db_get_keywords(connection):
    cursor = connection.cursor()
    cursor.execute(
        # sql stmt:
        """SELECT (keyword) FROM keywords"""
    )
    ret = cursor.fetchall()
    return list(map( lambda x: x[0], ret))

def db_write_tweet(
        keyword,
        tweet_json,
):
    pass

#########################
# twitter abstraction:
#########################

def init_twitter():
    twitter_app_token = environ.get("TWITTER_APP_TOKEN")
    twitter_app_secret = environ.get("TWITTER_APP_SECRET")

    auth = OAuth1(
            twitter_app_token,
            twitter_app_secret,
    )
    return auth

def twitter_fetch_tweets(
        auth,
        keywords,
        count = 15,
        max_id = None,
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


#########################
# actual program:
#########################

if __name__ == '__main__':
    print( "connecting to database..." )
    with init_db() as connection:
        keywords = db_get_keywords( connection )
        auth = init_twitter()
        print( f"fetching tweets containing {', '.join(keywords)}..." )

        # iterate through every keyword and aggregate "all" tweets that contain it:
        for keyword in keywords:
            print( f"tweets with keyword '{keyword}'" )
            lowest_id = None
            loaded_tweet_count = 0
            just_added_tweet_count = 0
            while( True ):
                (lowest_id, tweets) = twitter_fetch_tweets(
                        auth,
                        [keyword],
                        max_id=lowest_id,
                )
                just_added_tweet_count = len(tweets['statuses'])
                loaded_tweet_count += just_added_tweet_count
                print( f"received {just_added_tweet_count} tweets:" )
                for tweet in tweets['statuses']:
                    print( f"id: {tweet['id']}, date: {tweet['created_at']}" )
                if just_added_tweet_count == 0:
                    break
            print( f"for keyword '{keyword}' {loaded_tweet_count} tweets have been added." )

        # keys for some tweet:
        # ['created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'extended_entities', 'metadata', 'source', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user', 'geo', 'coordinates', 'place', 'contributors', 'retweeted_status', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'possibly_sensitive', 'lang'
        print( "closing connection to database..." )
