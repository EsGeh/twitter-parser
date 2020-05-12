package com.example.twitter_parser_java;

import com.example.twitter_parser_java.types.*;

//import twitter4j.Twitter;
import twitter4j.TwitterFactory;
import twitter4j.Query;
import twitter4j.QueryResult;
import twitter4j.auth.RequestToken;
import twitter4j.auth.AccessToken;
import twitter4j.conf.ConfigurationBuilder;
import twitter4j.Status;
import twitter4j.TwitterException;

/*
import kong.unirest.Unirest;
import kong.unirest.HttpResponse;
import kong.unirest.JsonNode;
*/
import java.io.IOException;
import static org.junit.Assert.*;

import java.util.List;
import java.util.ArrayList;


public class Twitter {
	private twitter4j.Twitter twitter;
	private String keyword;
	private Query query;

	public void init() {
		String twitter_app_token = System.getenv( "TWITTER_APP_TOKEN" );
		String twitter_app_secret = System.getenv( "TWITTER_APP_SECRET" );
		String twitter_access_token = System.getenv( "TWITTER_ACCESS_TOKEN" );
		String twitter_access_secret = System.getenv( "TWITTER_ACCESS_SECRET" );
		if(twitter_app_token == null)
			throw new RuntimeException("environment variable 'TWITTER_APP_TOKEN' not found!");
		if(twitter_app_secret == null)
			throw new RuntimeException("environment variable 'TWITTER_APP_SECRET' not found!");
		if(twitter_access_token == null)
			throw new RuntimeException("environment variable 'TWITTER_ACCESS_TOKEN' not found!");
		if(twitter_access_secret == null)
			throw new RuntimeException("environment variable 'TWITTER_ACCESS_SECRET' not found!");

		ConfigurationBuilder cb = new ConfigurationBuilder();
		cb.setDebugEnabled(true)
			.setOAuthConsumerKey(twitter_app_token)
			.setOAuthConsumerSecret(twitter_app_secret)
			.setOAuthAccessToken(twitter_access_token)
			.setOAuthAccessTokenSecret(twitter_access_secret);
		TwitterFactory tf = new TwitterFactory(cb.build());
		twitter = tf.getInstance();
	}

	public void setKeyword( String keyword ) {
		this.keyword = keyword;
		this.query = new Query(keyword);
	}

	public List<Tweet> getTweets() throws TwitterException {
		if( query == null ) {
			return new ArrayList<Tweet>();
		}
    QueryResult result = twitter.search(query);
		query = result.nextQuery();
		List<Tweet> ret = new ArrayList<Tweet>();
		for(Status tweet : result.getTweets()) {
			ret.add(
				new Tweet(
					Long.toString(tweet.getId()),
					tweet.getText(),
					new User(
						Long.toString(tweet.getUser().getId()),
						tweet.getUser().getName().toString()
					),
					this.keyword,
					tweet.getCreatedAt()
				)
			);
		}
		return ret;
		/*
		List<Status> tweets = result.getTweets();
		
    for (Status status : ) {
      System.out.println("@" + status.getUser().getScreenName() + ":" + status.getText());
    }
		*/
		//return new Tweet();
	}
}
