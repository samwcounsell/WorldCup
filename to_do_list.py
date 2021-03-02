# for every function we want to be only have to pass through the following;
# (player_data, team_data, time_delay)

# team_data

# we need to put all the nations into one file and add a column called 'Confederation'
# then at the top of each confederation function add a line saying;

afc_team_data = team_data[(team_data["Confederation"] == AFC)]

# then at the end have the returned output be only a list, which the world cup file uses to select the teams for the world cup

# this allows us to collect data on teams as they go through the world cup such as, total games, total goals, goals per game, etc.

# in the actual world cup function we just need to pass through one extra variable "world_cup_teams" into the function to be used 
# to the play the mathces, but we keep recording the other data into team_data
