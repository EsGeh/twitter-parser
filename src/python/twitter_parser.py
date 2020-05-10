#!/usr/bin/env python3

import db
import twitter


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
        (lowest_id, tweets) = twitter.fetch_tweets(
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
            db.write_tweet(
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
    with db.init() as db_connection:
        keywords = db.get_keywords( db_connection )
        auth = twitter.init()
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
