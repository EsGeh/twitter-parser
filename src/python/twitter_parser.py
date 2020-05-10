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
        """SELECT (keyword) FROM keywords;"""
    )
    ret = cursor.fetchall()
    return list(map( lambda x: x[0], ret))

def db_write_tweet(
        db_connection,
        keyword,
        tweet_json,
):
    cursor = db_connection.cursor()
    # test if tweet already in db:
    cursor.execute(
        """
        SELECT (id)
        FROM tweets
        WHERE id=%(id)s;
        """,
        {
            "id": tweet_json['id_str'],
        }
    )
    ret = cursor.fetchall()
    # if already in database, do nothing:
    if( len(ret) > 0 ):
        print( f"already in db: '{tweet_json['id']}'" )
        return
    else:
        # add user:
        cursor.execute(
            """
            SELECT (id)
            FROM users
            WHERE id=%(user_id)s;
            """,
            {
                "user_id": tweet_json['user']['id_str'],
            }
        )
        ret = cursor.fetchall()
        if len(ret) == 0:
            cursor.execute(
                """
                INSERT INTO users (id,name)
                VALUES (%(user_id)s, %(user_name)s);
                """,
                {
                    "user_id": tweet_json['user']['id_str'],
                    "user_name": tweet_json['user']['name'],
                }
            )
        cursor.execute(
            """
            INSERT INTO tweets (id,text,user_id)
            VALUES (%(id)s, %(text)s, %(user_id)s);
            """,
            {
                "id": tweet_json['id_str'],
                "text": tweet_json['text'],
                "user_id": tweet_json['user']['id_str'],
            }
        )
        db_connection.commit()
    # remember (keyword, tweet):
    cursor.execute(
        """
        SELECT (keyword)
        FROM keywords_tweets_rel
        WHERE keyword=%(keyword)s AND tweet_id=%(tweet_id)s;
        """,
        {
            "keyword": keyword,
            "tweet_id": tweet_json['id_str'],
        }
    )
    ret = cursor.fetchall()
    # if already in database, do nothing:
    if( len(ret) > 0 ):
        print( f"already in db: '{tweet_json['id']}'" )
        return
    else:
        cursor.execute(
            """
            INSERT INTO keywords_tweets_rel
            VALUES (%(keyword)s, %(tweet_id)s);
            """,
            {
                "keyword": keyword,
                "tweet_id": tweet_json['id_str'],
            }
        )
        db_connection.commit()

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

def fetch_and_write_tweets(
        keyword,
        db_connection,
        twitter_connection
):
    latest_tweet_id = None
    lowest_id = None
    loaded_tweet_count = 0
    just_added_tweet_count = 0
    first_pass = True
    while( True ):
        (lowest_id, tweets) = twitter_fetch_tweets(
                auth,
                [keyword],
                max_id=lowest_id,
        )
        just_added_tweet_count = len(tweets['statuses'])
        loaded_tweet_count += just_added_tweet_count
        if first_pass and just_added_tweet_count > 0:
            latest_tweet_id = tweets['statuses'][-1]['id']
        # debug print:
        print( f"received {just_added_tweet_count} tweets containing '{keyword}':" )
        for tweet in tweets['statuses']:
            print( f"id: {tweet['id']}, date: {tweet['created_at']}" )
        # write to database:
        for tweet in tweets['statuses']:
            db_write_tweet(
                    db_connection,
                    keyword,
                    tweet
            )
        # break loop, if no more tweets:
        if just_added_tweet_count == 0:
            break
        else:
            first_pass = False
    return {
            "latest_tweet_id" : latest_tweet_id,
            "added_tweet_count" : loaded_tweet_count,
    }

    # keys for some tweet:
    # ['created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'extended_entities', 'metadata', 'source', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user', 'geo', 'coordinates', 'place', 'contributors', 'retweeted_status', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'possibly_sensitive', 'lang'


#########################
# actual program:
#########################

if __name__ == '__main__':
    print( "connecting to database..." )
    with init_db() as db_connection:
        keywords = db_get_keywords( db_connection )
        auth = init_twitter()
        print( f"fetching tweets containing {', '.join(keywords)}..." )

        keyword_to_latest_tweet_id = {}
        for keyword in keywords:
            keyword_to_latest_tweet_id[keyword] = None
        # iterate through every keyword and aggregate "all" tweets that contain it:
        for keyword in keywords:
            print( f"tweets with keyword '{keyword}'" )
            tweets_info = fetch_and_write_tweets(
                    keyword,
                    db_connection=db_connection,
                    twitter_connection=auth
            )
            keyword_to_latest_tweet_id = tweets_info['latest_tweet_id']
            print( f"for keyword '{keyword}' {tweets_info['added_tweet_count']} tweets have been added." )
        print( "closing connection to database..." )
