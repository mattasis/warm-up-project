
import sqlite3
import datetime
class DataBall :
    
    """
    An all encapsulating ball of data used to produce player statistics for games 
    of 'Go Fish'.The DataBall is instantiated at the beginning of the game and closed 
    at the end. During this time, DataBall is collecting specific measurements about
    the game.
    
    The class is divided into two parts, methods used in game and methods used 
    in order to query statistics. 
    
    Current list of statistics offered: 
        -Games played
        -games won by user (lost by user)
        -average number of cards dealt per request per game 
        -Longest/shortest game (time/turns)
        -Average number of turns
        -Average time played per game
        -Longest streak of guesses resulting in 'Go Fish' (empty guesses)
            - out of all games
            - for current game
            
        -Average value for longest streaks of empty guesses
       
"""

    def __init__(self,difficulty=0):
         
        """
        DataBall constructor, connect to the go_fish database, define a cursor,
        and get the start time of the game. Initialize several other fields used in the database.
        
        Parameters:         data type   purpose
        
            difficulty         int      assign integer value to difficulty field
        ------------------------------------------------------------------------
        
        Fields:             data type             purpose
        
        conn                sqlite3 connection    connect to database
        ------------------------------------------------------------------------
        curs                sqlite3 cursor        manipulate/query database
        ------------------------------------------------------------------------
        ts                  datetime              start time of game
        ------------------------------------------------------------------------
        won                 int                   boolean integer value 
                                                  (1 for win, 0 for loss)
        ------------------------------------------------------------------------
        cards_per_request   int                   running total for both players
                                                  of number of cards recieved upon
                                                  request     
        ------------------------------------------------------------------------
        turn_number         int                   incrementer on number of turns 
        ------------------------------------------------------------------------
        difficulty          int                   number indicating opponent difficulty
        ------------------------------------------------------------------------
        empty_guesses       int                   running streak of turns that recieved
                                                  no cards from the opponent
        ------------------------------------------------------------------------  
        top_empty_guess_ct  int                   highest streak of guesses that
                                                  recieve 0 cards
        ------------------------------------------------------------------------                             
                                        
        """
        self.conn = sqlite3.connect('go_fish.db') #Connect to database
        self.curs = self.conn.cursor()
        
        # start time of game
        self.ts  = datetime.datetime.now()
        
        # initialize other fields/qualifiers of the game
        self.won = None
        self.cards_per_request = 0
        self.turn_number = 1
        self.difficulty = difficulty
        
        # 'empty guess' tracking variable- an empty guess is a guess for which the 
        #  player had to 'go fish'
        self.empty_guesses = 0
        self.top_empty_guess_ct = 0
    
    
    ##############################################################################
    ############################ In Game Methods #################################
    ##############################################################################
    
    def close(self,win=0):
        
        """
        Close all counting processes, run final calculations, and write information
        to the database 
        
        Parameters:         data type   purpose
        
            win                int      act as boolean (1 for win, 0 for loss)
                                        used as integer for sqlite3 data type constraints
                                        and future computational ease.
        ------------------------------------------------------------------------                                
        
        """
        # get time past during game
        elapsed         = datetime.datetime.now() - self.ts
        # convert timestamps to strings (hour:minute:second - day/month/year)
        elapsed_str     = str(elapsed)
        ts_str          = self.ts.strftime("%H:%M:%S - %d/%m/%Y")
        
        # computer average number of cards per request
        avg_per_request = self.cards_per_request/self.turn_number    
        
        # check one last time for empty guess streak
        if (self.empty_guesses > self.top_empty_guess_ct):
                self.top_empty_guess_ct = self.empty_guesses
        
        # write game stats to database
        self.curs.execute("INSERT INTO game_stats (ts_begin,ts_elapsed, user_win,"+
                          "longest_draw, avg_per_request, difficulty)"+
                          " VALUES (?,?,?,?,?,?)",(ts_str,elapsed_str,win,
                                                   self.top_empty_guess_ct,
                                                   avg_per_request, self.difficulty))
                                                   
        # commit the changes
        self.conn.commit()
        
        # close connection to database
        self.conn.close()
        
    def hard_close(self):
        """
        Close the DataBall class without saving anything to the database.
        
        """
        
        self.conn.close()
        
        
    def update(self,cards_on_req=0):
        
        """
        Called at the end of each turn. Increments the turn count and adds to the
        sum of cards on request. Increments/resets empty guess streak.
        
        Parameters:         data type   purpose
        
          cards_on_req         int      add to the sum of cards recieved on request
          ------------------------------------------------------------------------
                          
        """
        
        # increment streak if guess is empty
        if (cards_on_req==0):
            self.empty_guesses += 1
        
        # otherwise check for a new max streak
        else:
    
            if (self.empty_guesses > self.top_empty_guess_ct):
                self.top_empty_guess_ct = self.empty_guesses
            
            self.empty_guesses = 0
        
        # increment number of cards per request and turn number
        self.cards_per_request += cards_on_req
        self.turn_number += 1
    
    ##############################################################################
    ######################## Statistics Functions ################################
    ##############################################################################
    
    def games_played(self,difficulties=[0,1,2]):
        """
        Get the total number of games for the specified difficulties.
        
        Parameters:         data type   purpose
        
            difficulties    list      specified difficulties to query
        ------------------------------------------------------------------------
        
        """
        
        total = 0
        for diff in difficulties:
            # query database for these difficulties
            self.curs.execute("SELECT * FROM game_stats WHERE difficulty = ?",(str(diff),))
            total += len(self.curs.fetchall())
        
        return total
    
    def games_won(self,difficulties=[0,1,2]):
        """
        Get the total number of games won by the user for the specified difficulties.
        
        Parameters:         data type   purpose
        
            difficulties    list      specified difficulties to query
        ------------------------------------------------------------------------
        """
        total = 0
        for diff in difficulties:
            # query database
            self.curs.execute("SELECT user_win FROM game_stats WHERE difficulty = ?",(str(diff),))
            
            # get sum of wins for that difficulty
            for row in self.curs.fetchall():
                total+=row [0]
        
        return total
    
    def win_loss_ratio(self,difficulties=[0,1,2],choice='win'):
        """
        Compute the win/overall or loss/overall ratios for game stored in the database
        for a given set of difficulties.
        
         Parameters:         data type   purpose
         
            difficulties     list      specified difficulties to query 
        ------------------------------------------------------------------------
        """
        if (choice == 'win'):
            return self.games_won(difficulties)/self.games_played(difficulties)
        
        return (self.games_played(difficulties) - self.games_won(difficulties)/self.games_played(difficulties))
    
    def average_per_request(self):
        """
        Compute and return the average number of cards per request for the current game.
        """
        
        return self.cards_per_request/self.turn_number
        
    def average_avg_per_req(self,difficulties=[0,1,2]):
        """
         Compute and return the average of the average number of cards per request per game
         for a given set of difficulties.
        
         Parameters:         data type   purpose
         
            difficulties     list      specified difficulties to query 
        ------------------------------------------------------------------------
    
        """
        avgs = []
        
        for diff in difficulties:
            # query database
            self.curs.execute("SELECT avg_per_request FROM game_stats WHERE difficulty = ?",(str(diff),))
            
            for avg in self.curs.fetchall():
                avgs.append(avg[0])
            
        return sum(avgs)/len(avgs)
        
    def superlative_game_len(self,time_metric,superl, difficulties=[0,1,2]):
        """
        
        Compute the max/min game length for some set of difficulties under one 
        of two time metrics (number of turns or traditional time) for a given
        superlative (aka max or min)
        
        Parameters:         data type   purpose
            
            time_metric      string     denote whether to measure in 'turns' or 'tradit'
                                        'num_turns'  --->  turn wise duration
                                        'ts_elapsed' --->  traditional time scale
        ------------------------------------------------------------------------
            superl           string     denote whether to take max or min of set
                                        'max'    --->  maximum
                                        'min'    --->  minimum
        ------------------------------------------------------------------------
            difficulties     list       specified difficulties to query 
        ------------------------------------------------------------------------
        Returns:
            superl_elt  <---- the longest/shortest game, temporally/turnwise and
                              its corresponding timestamp
            
        """
        
        # dictionary to map timestamps ---> game durations
        times = dict()
        
        # validate parameter input
        if (time_metric in ['num_turns','ts_elapsed'] and superl in ['max','min']):
            
            # iterate through difficulties and query database for desired values
            for diff in difficulties:
                self.curs.execute("SELECT {}, ts_begin FROM game_stats WHERE difficulty = ?".format(time_metric),(diff,))
                
                # map each timestamp to its game duration
                for time in self.curs.fetchall():
                    times[time[1]] = time[0]
            
            #isolate timestamps
            keys = [k for k in times.keys()]
            
            #define a superlative element to compare against
            superl_elt = [times[keys[0]],keys[0]]
            
            # iterate through timestamps, check if its corresponding duration
            # is greater or less than superl_elt
            for k in keys:
                if superl == 'max': # <--- max case
                    print(times[k])
                    if times[k] > superl_elt[0]:
                       superl_elt = [times[k],k]
                
                else: # <---- min case
                    if times[keys[k]] < superl_elt[0]:
                        superl_elt = [times[k],k]
            
            return superl_elt #return the superlative (min/max) element
            
        else: # <--- display error message
            print("Time metric or superlative incorrectly specified!\n"+
                  "Time metric:\n"+
                  "- 'ts_elapsed' ---> traditional temporal duration"+
                  "- 'num_turns'  ---> turn-wise duration")
    
    def avg_game_len(self,time_metric,difficulties=[0,1,2]):
        """
        Compute and return the average game length (in temporal time or turnwise)
        over a specific domain of difficulties.
        
         Parameters:         data type   purpose
            
            time_metric      string     denote whether to measure in 'turns' or 'tradit'
                                        'num_turns'  --->  turn wise duration
                                        'ts_elapsed' --->  traditional time scale
        ------------------------------------------------------------------------
            difficulties     list       specified difficulties to query 
        ------------------------------------------------------------------------
        
        """
        
        total       = 0 # running total of times
        total_games = 0 # number of games
        
        if (time_metric in ['num_turns','ts_elapsed']):
            # iterate through difficulties and query database for desired values
            for diff in difficulties:
                self.curs.execute("SELECT {} FROM game_stats WHERE difficulty = ?".format(time_metric),(diff,))
                games = [l[0] for l in self.curs.fetchall()]
                
                total         += sum(games)
                total_games   += len(games)
                
        return total/total_games
        
        
    def longest_streak(self,overall=False,difficulties=[0,1,2]):
        """
        
        Find the overall longest streak of empty guesses for a given domain of difficulties
        
        OR
        
        Find the longest streak of empty guesses for the current game.
        
        Parameters:         data type   purpose
            
            overall          boolean    denote whether to report the overall longest
                                        or longest in current game 
                                        (overall=True => report overall)
                                      
        ------------------------------------------------------------------------
            difficulties     list       specified difficulties to query 
        ------------------------------------------------------------------------
        
        Returns:
            the maximum length of a streak and the time stamp of the game.
        
        """
        if (overall): # if overall specified, query database and find max
            
            streaks = []  
            for diff in difficulties: # iterate through difficulties, query db and 
                                      # append fetched data to a list of streaks
                                      
                self.curs.execute("SELECT longest_draw,ts_begin FROM game_stats WHERE difficulty = ?",
                                      (diff,))
                                      
                streaks+=self.curs.fetchall() # append
            
            max_streak = max(streaks) # find overall max
            
            return max_streak
            
        return self.top_empty_guess_ct # eitherwise return the current max streak
        
        
    def avg_streak(self,difficulties=[0,1,2]):
        """
        
        Compute and return the average length of max empty guess streaks for 
        a given domain of difficulties.
        
        Parameters:         data type   purpose
            
            difficulties     list       specified difficulties to query 
        ------------------------------------------------------------------------
        
        """
        streaks = []
        for diff in difficulties:
            
            self.curs.execute("SELECT longest_draw FROM game_stats WHERE difficulty = ?",(diff,))
            streaks+=[l[0] for l in self.curs.fetchall()]
            
        return sum(streaks)/len(streaks)
            
        
                    
                    
            
            