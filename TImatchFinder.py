from heroDict import heroes
import requests
import datetime
import pandas
import json

def getJSON(fileName):
	with open(fileName, 'r') as file:
		return json.load(file)

def getHeroList():
	heroDF = pandas.DataFrame()
	heroJSON = getJSON('./heroes.json')['result']
	
	for each in heroJSON['heroes']:
		heroDF = heroDF.append(each, ignore_index=True)

	return heroDF.sort_values('id').reset_index(drop=True)

def cleanMatchDF(matchDF):
	matchDF['start_time'] = pandas.to_datetime(matchDF['start_time'], unit='s')
	matchDF['match_id'] = pandas.to_numeric(matchDF['match_id'])
	columns = ['match_id', 'series_id', 'match_seq_num', 'start_time', 'series_type', 'radiant_team_id', 'dire_team_id', 'lobby_type']
	return (matchDF.sort_values('start_time', ascending=False).reset_index(drop=True)[columns])	
	
def getTImatches():
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
	
print (getTImatches())