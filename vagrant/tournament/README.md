## Synopsis

A Swiss tournament application consisting of a PostgreSQL database, named tournament, used to keep track of players and matches in a Swiss Tournament style game.  The data manipulation functions are coded in python and located in tournament.py.  These functions are used to track the Swiss tournament players, match results, current standings and generate Swiss pairing for tournament rounds.  

## Code Examples

Return a connection to the tournament database:
 
    connect()

Delete all match records from the database:
 
    deleteMatches()

Delete all player records from the database:

    deletePlayers()

Register a player for a tournament:

    registerPlayer("Player Name")

Return a count of all players registered in a tournament:

    countPlayers()

Return the current player standings as a list of tuples (id, name, wins, matches) ordered from most wins to least:

    standings = playerStandings()

Return the Swiss pairing of players for the next round as a list of tuples (id1, name1, id2, name2):

    pairings = swissPairings()

Record a match completed with id1 as the winner, and id2 as the loser:

    reportMatch(id1, id2)

## Motivation

The database tournament is composed of two tables, player_names and scorecards.  Player_names tracks the players registered for the tournament.  Each player will have a scorecard record of the opponent played.  Using the Swiss Scoring method, scorecards record matches between player and opponent, setting the match results for the player to the value: win = 3, ties = 1 and lost = 0.  The view player_standings provides the number of wins, matches and the player_standing based on the overall scorecard results for each player.

## Installation

### Understand the purpose of each file
tournament.sql  - this file is used create and set up the tournament database schema
tournament.py - this file is used to provide access to the database via a library of functions which can add, delete or query data in the tournament database to another python program (a client program). 
tournament_test.py - this is a client program to test the database installation and implementation of functions in tournament.py

### How to get the project files
Files are located in GitHub repository https://github.com/MrsGail/fullstack-nanodegree-vm.git
Fork the MrsGail/fullstack-nanodegree-vm repository so that you have a version of your own within your Github account.

### Install Vagrant VM and PostgreSQL per Udacity instruction guide
Follow instructions https://docs.google.com/a/knowlabs.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true

### Install database
To use the Vagrant virtual machine, navigate to the full-stack-nanodegree-vm/tournament directory in the terminal, then use the command vagrant up (powers on the virtual machine) followed by vagrant ssh (logs into the virtual machine).  
Remember, once you have executed the vagrant ssh command, you will want to cd /vagrant to change directory to the synced folders in order to work on your project, once your cd /vagrant, if you type ls on the command line, you'll see your tournament folder.

The Vagrant VM provided in the fullstack repo already has PostgreSQL server installed, as well as the psql command line interface (CLI), so you'll need to have your VM on and be logged into it to run the database configuration file (tournament.sql).
To build and access the database:
cd /tournament
psql 
\i tournament.sql
\q

## Tests

Describe and show how to run the tests with code examples.

Once you have the .sql and .py files installed, test them out against the testing file provided to you (tournament_test.py). To run the series of tests defined in this test suite, run the program from the command line >> python tournament_test.

Output should show 10 numbered test lines as follows, followed by sample output of the 8 player test.  The sample output of the 8 player test may not exactly match the below, but will reflect players with wins being paired with players with wins, followed by Success message as last line.

    1. Old matches can be deleted.
    2. Player records can be deleted.
    3. After deleting, countPlayers() returns zero.
    4. After registering a player, countPlayers() returns 1.
    5. Players can be registered and deleted.
    6. Newly registered players appear in the standings with no matches.
    7. After a match, players have updated standings.
    8. After one match, players with one win are paired.
    Success!  All tests pass!
    Success test
    9. After a match, players have updated standings.
    10. After one match, players with one win are paired.
    [(41, 'player3', 1L, 1L), (43, 'player5', 1L, 1L), (46, 'player8', 1L, 1L), (42, 'player4', 1L, 1L), (45, 'player7', 0L, 1L), (44,     'player6', 0L, 1L), (40, 'player2', 0L, 1L), (39, 'player1', 0L, 1L)]
    [(41, 'player3', 43, 'player5'), (46, 'player8', 42, 'player4'), (45, 'player7', 44, 'player6'), (40, 'player2', 39, 'player1')]
    Success! Using 8 players, tests pass
