package com.example.twitter_parser_java.types;

import com.example.twitter_parser_java.types.User;

import java.util.Date;

public class Tweet {
	public String id;
	public String text;
	public User user;
	public String keyword;
	public Date date;

	public Tweet(
			String id,
			String text,
			User user,
			String keyword,
			Date date
	) {
		this.id = id;
		this.text = text;
		this.user = user;
		this.keyword = keyword;
		this.date = date;
	}
}
