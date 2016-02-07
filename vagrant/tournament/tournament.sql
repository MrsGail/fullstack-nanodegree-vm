-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- This is a .sql file to be run from the command line PostgreSQL environment
-- Log into a PostgreSQL psql and use the command \i tournament.sql to
-- import the whole file into psql at once.

-- Drop database to support re-running this script multiple times to
-- Start with a new, empty PostgreSQL database
\echo 'Dropping database tournament'
DROP DATABASE IF EXISTS tournament;

-- Create a new PostgreSQL database named tournament
\echo 'Creating database tournament'
CREATE DATABASE tournament;

-- Connect to database
\c tournament

-- Create tables and views
\echo 'Creating tables and views'

-- Create table player_names to track players in the tournament
CREATE TABLE player_names (
	player_id SERIAL CONSTRAINT playerkey PRIMARY KEY,
	name TEXT
);

-- Create table scorecards to track matches played and their results
-- Using the Swiss Scoring method, scorecards record matches
-- using the scoring method of tracking each player_id, opponent_id
-- and setting the player_id results for win = 3, ties = 1 and lost = 0
CREATE TABLE scorecards (
	player_id INTEGER,
	opponent_id INTEGER,
	result INTEGER
);

-- View player_standings provides the number of wins, matches and the 
-- player_standing based on the overall scorecard results for each player_id
CREATE VIEW player_standings 
	AS
	SELECT 
		player_names.player_id AS id,
		name AS name,
		COALESCE(SUM(win),0) AS wins,
		COUNT(match) AS matches,
		coalesce(SUM(stand),0) AS standing
	FROM
		player_names LEFT OUTER JOIN (
			SELECT scorecards.player_id, 
			win, 
			result AS match, 
			result AS stand
			FROM scorecards 
			LEFT OUTER JOIN (
				SELECT player_id, 
				1 AS win FROM scorecards 
		 		WHERE result = 3) AS won 
			ON scorecards.player_id = won.player_id) AS scores
	ON player_names.player_id = scores.player_id
	GROUP BY player_names.player_id;

\echo 'Tables and view created'
