

import sqlite3 # database module
import sys,os  # overwrite checking


"""
Build a database that stores game stats for a game of go fish. 

"""

# initialize build process
if __name__ == '__main__':
    
    # name the database
    db_wrapper = 'go_fish.db'
    
    # if the database file exists, exit so there's no overwrite.
    if os.path.exists(db_wrapper):
        sys.exit('Database already exists!')
        
    # otherwise create the file
    conn = sqlite3.connect(db_wrapper)
    curs = conn.cursor()
    
    # build a table inside database called game_stats
    # game_stats consists of
    #    - a time_stamp (time started game)
    #    - a boolean value indicating whether the user won the game
    #    - longest draw streak count (longest streak of turns where a player had to "go fish"
    #    - average card yield per request from either player
    #    - a string that denotes the difficulty of the computer
    
    curs.execute("CREATE TABLE game_stats (ts_begin text, ts_elapsed text, user_win int,"+
                                         "longest_draw int, avg_per_request real,"+
                                         "difficulty text,num_turns int,longest_empty int)")
    
    #commit to the changes
    conn.commit()
    
    #close the connection
    conn.close()