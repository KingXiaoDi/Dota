from heroDict import heroes
import requests
import datetime
import getpass
import pandas
import json

def APIrequest(site):
	r = requests.get(site)
	if r.status_code == 200:
		print (r.status_code)
		return r.text
	else:
		print (r.status_code)

def getJSON(fileName):
	with open(fileName, 'r') as file:
		return json.load(file)

def getHeroList():
	"""Reads Steam's hero JSON, returns a sorted DataFrame of hero names and IDs used with the Steam API"""
	heroDF = pandas.DataFrame()
	heroJSON = getJSON('./heroes.json')['result']
	
	for each in heroJSON['heroes']:
		heroDF = heroDF.append(each, ignore_index=True)

	return heroDF.sort_values('id').reset_index(drop=True)

def cleanMatchDF(matchDF):
	"""Performs various adjustments to the match DataFrame created from Steam's API match list. Converts unix timestamp to readable date, converts match ID to a number, sorts the columns,
	and sorts the values by start time."""
	matchDF['start_time'] = pandas.to_datetime(matchDF['start_time'], unit='s')
#	matchDF['match_id'] = pandas.to_numeric(matchDF['match_id'])
	columns = ['match_id', 'series_id', 'match_seq_num', 'start_time', 'series_type', 'radiant_team_id', 'dire_team_id', 'lobby_type']
	return (matchDF.sort_values('start_time', ascending=False).reset_index(drop=True)[columns])	
	
def getTImatches():
	"""Reads a JSON from Steam's API and creates a DataFrame from the information therein."""
	matchDF = pandas.DataFrame()

	TImatchJSON = getJSON('./TImatches.json')['result']
	matches = TImatchJSON['matches']
	matchCount = TImatchJSON['total_results']
	TIstartDate = datetime.datetime.strptime('Aug 15 2018', '%b %d %Y')
	heroDF = getHeroList()

	for match in matches:
		matchDict = {}
		matchDate = (datetime.datetime.fromtimestamp(match['start_time']))
		if matchDate > TIstartDate:
			for key in match:
				if key == 'players':
					for player in match[key]:
						heroID = player['hero_id']
				else:
					matchDict[key] = match[key]
			matchDF = matchDF.append(matchDict, ignore_index=True)
	return cleanMatchDF(matchDF)

def getMatchIDs(matchDF):
	return matchDF['match_id'].values
	
def getMatchJSON(matchID):
	key = getpass.getpass()
	site = 'http://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1?match_id={}&key={}'.format(matchID, key)
	
	req = APIrequest(site)
	if req is not None:
		json.loads(req)
	
#matchDF = getTImatches()

getMatchJSON(1)	