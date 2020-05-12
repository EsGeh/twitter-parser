package com.example.twitter_parser_java;

import com.example.twitter_parser_java.types.*;

import java.io.*;
import java.util.List;

public class TwitterParser {

	public static void main(String[] args) {
		System.out.println( "connecting to twitter..." );
		Twitter twitter = new Twitter();
		try {
			twitter.init();
			twitter.setKeyword( "adidas" );
			List<Tweet> tweets = null;
			do {
				tweets = twitter.getTweets();
				System.out.printf( "received %d tweets containing '%s'\n", tweets.size(), "adidas" );
				for( Tweet tweet : tweets ) {
					System.out.printf( "id: %s, date: %s\n", tweet.id, tweet.date.toString() );
				}
			}
			while( tweets != null );
		}
		catch(Exception e){
			System.out.println("error: " + e.toString());
			e.printStackTrace();
			System.exit(1);
		}
		System.out.println( "done." );
	}

}
