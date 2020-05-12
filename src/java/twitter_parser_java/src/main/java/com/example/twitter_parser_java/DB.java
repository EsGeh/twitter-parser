package com.example.twitter_parser_java;

import com.example.twitter_parser_java.types.*;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.io.IOException;

import java.util.List;
import java.util.ArrayList;


public class DB {
	private Connection connection;

	public void init() throws SQLException {
		this.connection =
			DriverManager.getConnection(
				"jdbc:postgresql://twitter_parser_db/db",
				"postgres", ""
			);
	}

	public void close() throws SQLException {
		this.connection.close();
	}

	public List<String> getKeywords() throws SQLException {
		List<String> ret = new ArrayList<String>();
		Statement stmt = connection.createStatement();
		ResultSet rs = stmt.executeQuery(
				"SELECT (keyword) FROM keywords;"
		);
		while( rs.next() ) {
			ret.add( rs.getString("keyword") );
		}
		rs.close();
		stmt.close();
		return ret;
	}
}
