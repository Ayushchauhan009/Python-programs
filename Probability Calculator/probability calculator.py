import datetime
import time
import sys

# Base points is the picture of current points table. This will be used as starting point for each simulation
# Update this after completion each game
basePoints = { "mi":12, "dc":14, "kkr":8, "rcb":12, "srh":6, "rr":6, "csk":6, "kxip":4 }

# list of pending matches - manually edit this after each game
matches = [  
"srh:kkr",
"mi:kxip",
"csk:rr",
"kxip:dc",
"kkr:rcb",
"rr:srh",
"csk:mi",
"kkr:dc",
"kxip:srh",
"rcb:csk",
"rr:mi",
"kkr:kxip",
"srh:dc",
"mi:rcb",
"csk:kkr",
"kxip:rr",
"dc:mi",
"rcb:srh",
"csk:kxip",
"kkr:rr",
"dc:rcb",
"srh:mi"
]

#function to chop microseconds from timestamp - makes for better display
def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)

#if no argument is passed to the script it calculates probability based on current table
#you can pass one of the  team names of the next game and the script will calculate probabilities assuming that team wins

if len(sys.argv) > 1:
	winner = sys.argv[1]
	nextMatch=matches[0] 
	simulation_condition = winner + " is winner"
	print("running simulations assuming %s wins in %s" % (winner, nextMatch))
	
	#input team name passed should be playing the next game. Otherwise, throw an error and exit
	if not winner in nextMatch:
		print("%s is not a valid winner for the game %s\n" % (winner, nextMatch))
		exit(1)

	#increment points of the team passed as winner to the script and reduce number of games by 1
	print("incrementing base points of %s by 2 and reducing matches from %d to %d" % (winner, len(matches), len(matches)-1))
	basePoints[winner] += 2
	matches=matches[1:] #since we have assumed one team to be the winner of the next game, remove next game from the schedule
else:
	simulation_condition = "before game"
	print("running simulations before game %s" % matches[0])


# get list of teams in sorted order
teams = sorted( basePoints.keys() )

n=len(matches) # number of games left
combos = pow(2,n) # number of possible combinations left. Assumes each game has only 2 outcomes - no tie or washout
formatStr = "0{}b".format(n) #create a binary string n digits long - this will represent a sequence of events with each digit representing a game

print( "number of pending matches    = %d" % n )
print( "number of possible scenarios = %d" % combos )

top2Confirmed = {}
top2Possible  = {}
top4Confirmed = {}
top4Possible  = {}
binaryStr     = ""
print_every = 500000 #prints a log message for every n simulations
start_time = time.time()

# initialize probability to 0 for all teams
for team in teams:
	top2Confirmed[team] = 0
	top2Possible[team]  = 0
	top4Confirmed[team] = 0
	top4Possible[team]  = 0

# run simulations
for i in range(0,combos):

	#print progress of script for 'print_every' simulations
	if (i+1)%print_every == 0:
		elapsed_time = str(chop_microseconds(datetime.timedelta(seconds=time.time()-start_time)))
		eta = str(chop_microseconds(datetime.timedelta(seconds=(time.time()-start_time)* (combos-i+1)/(i+1))))
		#eta to complete script is calculated by estimating how long it took for the # of simulations calculated until now and extrapolate to remaining scenarios to compute
		print("Completed %s of %s sims (%10.10f percent ) elapsed %s should complete in %s" % ("{:,}".format(i+1), "{:,}".format(combos), (i+1)*100/combos, elapsed_time, eta) )

	binaryStr = format(i, formatStr)
	simPoints = basePoints.copy()
	matchCnt  = 0

	# iterate throught each digit of the binary string
	# each digit represents a match and the entire string represents a sequence of events
	# digit 0 means team1 wins and digit 1 means team2 wins
	# for example: for a game csk:rcb, a corresponding binary digit of 0 means csk wins and 1 means rcb wins
	for seq in binaryStr:
		team1, team2 = matches[matchCnt].split(":")
		if seq == "0":
			simPoints[ team1 ] = simPoints[ team1 ] + 2
		else:
			simPoints[ team2 ] = simPoints[ team2 ] + 2

		# increment points of winning team by 2
		matchCnt = matchCnt + 1

	# at the end of a sequence, determine positions for each team
	for team in teams:
		teamsAhead  = 0
		teamsBehind = 0

		# iterate through points of each team at the end of a sequence of events and determine how many teams and ahead/behind them
		for team1 in teams:
			if team1 == team:
				continue
			if simPoints[team1] > simPoints[team]:
				teamsAhead = teamsAhead + 1
			if simPoints[team1] < simPoints[team]:
				teamsBehind = teamsBehind + 1

		# we now have the net teams ahead/behind of each team. this will help determine the position of team in points table
		# if at max only 1 team is ahead of a team, the team is in consideration for top 2 finish, but might have to compete on NRR { indicated by T2P - Top 2 Possible }		
		# if at least 6 teams are below a team, the team is guaranteed a top 2 finish irrespective of NRR { indicated by T2C - Top 2 Confirmed }		
		# if at max only 3 teams are ahead of a team, the team is in consideration for top 4 finish, but might have to compete on NRR { indicated by T4P - Top 4 Possible }		
		# if at least 4 teams are below a team, the team is guaranteed a top 4 finish irrespective of NRR { indicated by T4C - Top 4 Confirmed }		
		if teamsAhead <= 1:
			top2Possible[team]=top2Possible[team]+1
		if teamsBehind >= 6:
			top2Confirmed[team]=top2Confirmed[team]+1	
		if teamsAhead <= 3:
			top4Possible[team]=top4Possible[team]+1
		if teamsBehind >= 4:
			top4Confirmed[team]=top4Confirmed[team]+1	

	# end of all simulations

#display final possibilities in terms of number of scenarios for each team
print
print( "Results:" )
print
print("==========" + simulation_condition + "==============")
print( "-------------------------------------- Possible Scenarios -------------------")
print( "%5s|%17s|%17s|%17s|%17s|" % ("Team", "Top 2 Confirmed", "Top 2 Possible", "Top 4 Confirmed", "Top 4 Possible") )
print( "-----------------------------------------------------------------------------")
for team in teams:
	print( "%5s|%17d|%17d|%17d|%17d|" % (team, top2Confirmed[team], top2Possible[team], top4Confirmed[team], top4Possible[team]) )

# display final possibilities in terms of % of number of scenarios to total possible scenarios
# a value of 0% means the team has absolutely no chance to come in that bucket and a value of 100% means its guaranteed that bucket

print
print( "-------------------------------------- Possible Scenarios % ------------------")
print( "%5s|%17s|%17s|%17s|%17s|" % ("Team", "Top 2 Confirmed", "Top 2 Possible", "Top 4 Confirmed", "Top 4 Possible") )
print( "------------------------------------------------------------------------------")
for team in teams:
	print( "%5s|%15.2f %%|%15.2f %%|%15.2f %%|%15.2f %%|" % (team, top2Confirmed[team] * 100.0/combos, top2Possible[team] * 100.0/combos, top4Confirmed[team] * 100.0/combos, top4Possible[team] * 100.0/combos) )