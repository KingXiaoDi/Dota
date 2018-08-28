from heroDict import heroes
import datetime
import pandas
import numpy
import json
import sys

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