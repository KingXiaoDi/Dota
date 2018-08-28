from heroDict import heroes
import datetime
import pandas
import numpy
import json
import sys


def getJSON(fileName):
	with open(fileName, 'r') as file:
		return json.load(file)
		
def getHeroList():
	heroDF = pandas.DataFrame()
	fileName = './heroes.json'

	heroJSON = getJSON(fileName)['result']
	for each in heroJSON['heroes']:
		heroDF = heroDF.append(each, ignore_index=True)

	return heroDF.sort_values('id').reset_index(drop=True)
	
def getMatches():
	matchDF = pandas.DataFrame()
	fileName = './TImatches.json'
	
	matchJSON = getJSON(fileName)['result']
	matchCount = matchJSON['total_results']
	matches = matchJSON['matches']
	
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
						print (heroes[heroDF.loc[heroDF['id']==heroID, 'name'].values[0]])
				else:
					matchDict[key] = match[key]
			matchDF = matchDF.append(matchDict, ignore_index=True)
		print ()
	matchDF['start_time'] = pandas.to_datetime(matchDF['start_time'], unit='s')
	matchDF['match_id'] = pandas.to_numeric(matchDF['match_id'])
	columns = ['match_id', 'series_id', 'match_seq_num', 'start_time', 'series_type', 'radiant_team_id', 'dire_team_id', 'lobby_type']
	return (matchDF.sort_values('start_time', ascending=False).reset_index(drop=True)[columns])	

def checkTowerStatus(towerBit, side):
	towerDict = {
			 0:  'Tier 1 Top',
			 1:  'Tier 2 Top',
			 2:  'Tier 3 Top',
			 3:  'Tier 1 Mid',
			 4:  'Tier 2 Mid',
			 5:  'Tier 3 Mid',
			 6:  'Tier 1 Bot',
			 7:  'Tier 2 Bot',
			 8:  'Tier 3 Bot',
			 9:  'Tier 4  A',
			 10: 'Tier 4  B'
	}
	for i in range(0,11):
		if (towerBit & 2**i):
			print ("{} {:10s} still standing.".format(side, towerDict[i]))
		else:
			print ("{} {:10s} has fallen.".format(side, towerDict[i]))
			
def checkRaxStatus(towerBit, side):
	raxDict = {
			 0:  'Bottom Ranged',
			 1:  'Bottom Melee',
			 2:  'Middle Ranged',
			 3:  'Middle Melee',
			 4:  'Top Ranged',
			 5:  'Top Melee',
	}
	for i in range(0,6):
		if (towerBit & 2**i):
			print ("{} {:12s} still standing.".format(side, raxDict[i]))
		else:
			print ("{} {:12s} has fallen.".format(side, raxDict[i]))
			
	
def getMatchJSON():
	fileName = './miracleGPM.json'
	
	matchJSON = getJSON(fileName)['result']
	for each in matchJSON:
		if each == 'players':
			for player in matchJSON[each]:
				for stat in player:
					print (stat)
					print (player[stat])
				print ()
		elif each == 'picks_bans':
			pass
		elif each == 'tower_status_radiant':
			radiantTower = matchJSON[each]
		elif each == 'tower_status_dire':
			direTower = matchJSON[each]
		elif each == 'barracks_status_radiant':
			radiantRax = matchJSON[each]
		elif each == 'barracks_status_dire':
			direRax = matchJSON[each]
			
def matchDataReader(matchJSON):
	pass

#getMatches().to_csv('./temp.csv', index=False)
#getMatches()

getMatchJSON()