import datetime
import pandas
import json

def getJSON(fileName):
	with open(fileName, 'r') as file:
		return json.load(file)
		
def getTImatches():
	TImatchJSON = getJSON('./TImatches.json')['result']
	matchDF = pandas.DataFrame()
	
	matchCount = TImatchJSON['total_results']
	
	matches = TImatchJSON['matches']
	for match in matches:
		matchDict = {}
		for each in match:
			if each == 'players':
				pass
			else:
				matchDict[each] = match[each]
		print (matchDict)
	
getTImatches()