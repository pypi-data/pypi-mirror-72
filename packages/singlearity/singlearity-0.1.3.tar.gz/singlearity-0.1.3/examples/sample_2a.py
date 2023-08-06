from common import sing
from pprint import pprint
##########################################
# Some examples of simulating portions of games using Singlearity-PA.
# An Enterprise API key is required.
##########################################


from singlearity import State, Player, Team, Venue, Atmosphere, Matchup, Lineup, LineupPos, Game, ApiException, GameSimResults
from singlearity.rest import ApiException
import pdb
import pandas as pd
pd.options.display.max_rows = 999
import numpy as np

###############################################################
# First, validate that the API key is working
###############################################################
sing.hello_with_key()
print("YOOOO")

###############################################################
# Find the best closer against the Yankees from a list of candidates
###############################################################
def find_best_closer(pitchers, sims):
    print(f'\nFinding the best closer by simulating {sims} innings')
    yankees_lineup = Lineup(
        lineup = [
        LineupPos(player = sing.get_players(name = 'DJ LeMahieu')[0], position = '2B'),
        LineupPos(player = sing.get_players(name = 'Aaron Judge')[0], position = 'RF'),
        LineupPos(player = sing.get_players(name = 'Gleyber Torres')[0], position = 'SS'),
        LineupPos(player = sing.get_players(name = 'Giancarlo Stanton')[0], position = 'LF'),
        LineupPos(player = sing.get_players(name = 'Gary Sanchez')[0], position = 'C'),
        LineupPos(player = sing.get_players(name = 'Gio Urshela')[0], position = '3B'),
        LineupPos(player = sing.get_players(name = 'Luke Voit')[0], position = '1B'),
        LineupPos(player = sing.get_players(name = 'Miguel Andujar')[0], position = 'DH'),
        LineupPos(player = sing.get_players(name = 'Brett Gardner')[0], position = 'CF'),
        LineupPos(player = sing.get_players(name = 'Gerrit Cole')[0], position = 'P'),
        ]
    )


    rays_lineup_pos = [
        LineupPos(player = sing.get_players(name = 'DJ LeMahieu')[0], position = '2B'),
        LineupPos(player = sing.get_players(name = 'Aaron Judge')[0], position = 'RF'),
        LineupPos(player = sing.get_players(name = 'Gleyber Torres')[0], position = 'SS'),
        LineupPos(player = sing.get_players(name = 'Giancarlo Stanton')[0], position = 'LF'),
        LineupPos(player = sing.get_players(name = 'Gary Sanchez')[0], position = 'C'),
        LineupPos(player = sing.get_players(name = 'Gio Urshela')[0], position = '3B'),
        LineupPos(player = sing.get_players(name = 'Luke Voit')[0], position = '1B'),
        LineupPos(player = sing.get_players(name = 'Miguel Andujar')[0], position = 'DH'),
        LineupPos(player = sing.get_players(name = 'Brett Gardner')[0], position = 'CF'),
        LineupPos(player = sing.get_players(name = 'Gerrit Cole')[0], position = 'P'),
        ]

    location = sing.get_venues(stadium_name='Yankee')[0]
    home_team = sing.get_teams(name = "Yankees")[0]
    #one run lead facing top of Yankees lineup with no one on base
    bat_score_start = 2
    fld_score_start = 3 
    bat_lineup_start = 1  #start with #4 batter in the lineup 
    st = State(inning = 9, top = False, on_1b=True, on_2b=True, on_3b=True, outs = 0, bat_score = bat_score_start, fld_score = fld_score_start, bat_lineup_order = bat_lineup_start)
    for pitcher in pitchers:
        #for half inning simulation, only the pitcher is required
        rays_lineup_pos[9] = LineupPos(player = sing.get_players(name = pitcher)[0], position = 'P')
        rays_lineup = Lineup(lineup = rays_lineup_pos)
        game = Game(visit_lineup = rays_lineup, home_lineup = yankees_lineup, atmosphere = Atmosphere(venue = location, home_team = home_team))
        game_sim = sing.get_game_sim({'game' : game, 'start_state' :  st},  num_sims = sims)
        #pdb.set_trace()
        saves = len([1 for r in game_sim  if (r.away_score > r.home_score)])
        losses = len([1 for r in game_sim  if (r.away_score < r.home_score)]) 
        ties = len([1 for r in game_sim  if (r.away_score == r.home_score)]) 
        print('Pitcher: {:<20s}  Save Percentage: {:.1f}% Loss Percentage: {:.1f}%  Tie Percentage: {:.1f}%'.format(pitcher, 100*saves/sims
                ,100*losses/sims
                ,100*ties/sims))




if __name__ == '__main__':
    test_pitcher_list = ['Nick Anderson', 'Liam Hendriks', 'Brad Hand', 'Colin Poche', 'Scott Barlow', 'Oliver Drake', 'Ryan Pressly', 'Seth Lugo', 'Drew Pomeranz', 'Emilio Pagan', 'Diego Castillo', 'Ty Buttrey']
    #test_pitcher_list = ['Nick Anderson']
    for i in range(0, 20):
        find_best_closer(test_pitcher_list, sims = 5000)
    

