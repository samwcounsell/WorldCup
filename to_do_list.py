# Idea 1: Datasets/Adding Players

# for every function we want to be only have to pass through the following;
# (player_data, team_data, time_delay)

# team_data

# we need to put all the nations into one file and add a column called 'Confederation'
# then at the top of each confederation function add a line saying;

afc_team_data = team_data[(team_data["Confederation"] == AFC)]

# this would mean what we pass into match_sim becomes (player_data, team_data, time_delay, acitve_team_data)

# then at the end have the returned output be only a list, which the world cup file uses to select the teams for the world cup

# this allows us to collect data on teams as they go through the world cup such as, total games, total goals, goals per game, etc.

# in the actual world cup function we just need to pass through one extra variable "world_cup_teams" into the function to be used 
# to the play the mathces, but we keep recording the other data into team_data



# Idea 2: Dash statistical analysis

# Use dash to present the results of our world cup simulation, in a similar style to gapminder example;

# Player categories to collect: total_goals, total_games, goals_per_game, goals_by_position
# Team categories to collect: total_goals_for, total_goals_against, total_games, formation (use code count("Position")),
# goals_for_per_game, goals_against_per_game, clean_sheets, place (where they finished)

# Graph ideas: (team) goals_for versus goals_against, (player) horizontal bar chart of top goals_scored, etc.
