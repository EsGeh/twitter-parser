#!/usr/bin/env python3

import db
import twitter

from time import sleep


def fetch_and_write_tweets(
        keyword,
        db_connection,
        twitter_connection,
        limit = None,
        since_id = None,
):
    latest_tweet_id = None
    lowest_id = None
    tweet_count_akk = 0
    first_pass = True
    while( True ):
        (lowest_id, tweets) = twitter.fetch_tweets(
                auth,
                [keyword],
                max_id=lowest_id,
                since_id=since_id,
        )
        # debug print:
        print( f"received {len(tweets['statuses'])} tweets containing '{keyword}':" )
        for tweet in tweets['statuses']:
            print( f"id: {tweet['id']}, date: {tweet['created_at']}" )

        # just_added_tweet_count = len(tweets['statuses'])
        if first_pass and len(tweets['statuses']) > 0:
            latest_tweet_id = tweets['statuses'][0]['id']
        # write to database:
        just_added_tweet_count = 0
        for tweet in tweets['statuses']:
            just_added_tweet_count += db.write_tweet(
                    db_connection,
                    keyword,
                    tweet
            )
        # debug print:
        print( f"wrote {just_added_tweet_count} tweets to database:" )

        tweet_count_akk += just_added_tweet_count
        # break loop, if no more tweets:
        if just_added_tweet_count == 0 \
                or (limit is not None and tweet_count_akk >= limit):
            break
        else:
            first_pass = False
    return {
            "latest_tweet_id" : latest_tweet_id,
            "added_tweet_count" : tweet_count_akk,
    }

    # keys for some tweet:
    # ['created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'extended_entities', 'metadata', 'source', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user', 'geo', 'coordinates', 'place', 'contributors', 'retweeted_status', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'possibly_sensitive', 'lang'


#########################
# actual program:
#########################

if __name__ == '__main__':
    print( "connecting to database..." )
    with db.init() as db_connection:
        keywords = db.get_keywords( db_connection )
        auth = twitter.init()

        print( "-----------------------------------" )
        print( f"fetching old tweets containing {', '.join(keywords)}..." )
        keyword_to_latest_tweet_id = {}
        for keyword in keywords:
            keyword_to_latest_tweet_id[keyword] = None
        # iterate through every keyword and aggregate "all" tweets that contain it:
        for keyword in keywords:
            print( f"tweets with keyword '{keyword}'" )
            tweets_info = fetch_and_write_tweets(
                    keyword,
                    db_connection=db_connection,
                    twitter_connection=auth,
                    limit = 100
            )
            keyword_to_latest_tweet_id[keyword] = tweets_info['latest_tweet_id']
            print( f"for keyword '{keyword}' {tweets_info['added_tweet_count']} tweets have been added." )

        print( "-----------------------------------" )
        print( "listen for new tweets:" )
        while True:
            # iterate through every keyword and aggregate "all" tweets that contain it:
            for keyword, latest_tweet in keyword_to_latest_tweet_id.items():
                print( f"tweets with keyword '{keyword}'" )
                tweets_info = fetch_and_write_tweets(
                        keyword,
                        db_connection=db_connection,
                        twitter_connection=auth,
                        since_id=latest_tweet,
                )
                keyword_to_latest_tweet_id[keyword] = tweets_info['latest_tweet_id']
                print( f"for keyword '{keyword}' {tweets_info['added_tweet_count']} tweets have been added." )
            sleep( 10 )

        print( "closing connection to database..." )
