package com.example.twitter_parser_java;

import com.example.twitter_parser_java.types.*;
import com.example.twitter_parser_java.DB;

import java.io.*;
import java.util.List;

public class TwitterParser {

	public static void main(String[] args) {
		try {
			System.out.println( "connecting to database..." );
			DB db = new DB();
			db.init();
			System.out.println( "connecting to twitter..." );
			Twitter twitter = new Twitter();
			twitter.init();
			List<String> keywords = db.getKeywords();
			for( String keyword : keywords ) {
				twitter.setKeyword( keyword );
				List<Tweet> tweets = null;
				do {
					tweets = twitter.getTweets();
					System.out.printf( "received %d tweets containing '%s'\n", tweets.size(), keyword );
					for( Tweet tweet : tweets ) {
						System.out.printf( "id: %s, date: %s\n", tweet.id, tweet.date.toString() );
					}
				}
				while( tweets != null );
			}
			db.close();
		}
		catch(Exception e){
			System.out.println("error: " + e.toString());
			e.printStackTrace();
			System.exit(1);
		}
		System.out.println( "done." );
	}

}
