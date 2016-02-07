#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    dbconn = connect()
    cur = dbconn.cursor()
    cur.execute("DELETE FROM scorecards;")
    cur.close()
    dbconn.commit()
    dbconn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    dbconn = connect()
    cur = dbconn.cursor()
    cur.execute("DELETE FROM player_names;")
    cur.close()
    dbconn.commit()
    dbconn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    dbconn = connect()
    cur = dbconn.cursor()
    cur.execute("SELECT count(*) FROM player_names;")
    row = cur.fetchone()
    cur.close()
    dbconn.close()
    return row[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    dbconn = connect()
    cur = dbconn.cursor()
    cur.execute("INSERT INTO player_names (name) VALUES (%s)", (name,))
    cur.close()
    dbconn.commit()
    dbconn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    dbconn = connect()
    cur = dbconn.cursor()
    cur.execute("SELECT id, name, wins, matches "
                "FROM player_standings "
                "ORDER BY wins DESC;")
    results = cur.fetchall()
    cur.close()
    dbconn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    dbconn = connect()
    cur = dbconn.cursor()
    cur.execute("INSERT INTO scorecards (player_id, opponent_id, result) "
                "VALUES (%s, %s, %s)", (winner, loser, 3))
    cur.execute("INSERT INTO scorecards (player_id, opponent_id, result) "
                "VALUES (%s, %s, %s)", (loser, winner, 0))
    cur.close()
    dbconn.commit()
    dbconn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player
    adjacent to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    dbconn = connect()
    cur = dbconn.cursor()
    cur.execute("SELECT id, name FROM player_standings "
                "ORDER BY standing DESC;")
    results = cur.fetchall()
    # Walk down list of results, pairing up players in order listed
    # pairing_half is used to indicate first or second half of the pair
    pairing_half = 1
    # pair is an empty list of pairings
    pair = []
    for row in results:
        # pair up partners one half at a time
        if pairing_half == 1:
            # record id1 and name1 of 1st half of pair in the pair list
            # set id2 and name2 to handle situation of odd number having a bye
            id1 = row[0]
            name1 = row[1]
            id2 = 0
            name2 = 'bye'
            # set pairing_half to second half
            pairing_half = 2
        else:
            # record id2 and name2 of 2nd half of pair in the pair list
            id2 = row[0]
            name2 = row[1]
            # set pairing_half back to 1st half for the next pairing
            pairing_half = 1
            # append pair to list
            pair.append((id1, name1, id2, name2))
    # completed for loop, append bye pair indicator to the list
    if pairing_half == 2:
        pair.append((id1, name1, id2, name2))
    cur.close()
    dbconn.close()
    return pair
