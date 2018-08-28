from heroDict import heroDict
import datetime
import pandas
import numpy

def makeHeroPicksList(picksColumn, heroDict):
	skip = ['Dark', 'Shadow', 'Phantom']
	newList = []
	for each in picksColumn:
		heroes = []
		for word in each.split(' '):
			if word not in skip:
				try:
					heroes.append(heroDict[word])
				except:
					pass
#					print ("{} not in dictionary!".format(word))
		if len(heroes) != 5:
			print (heroes)
			print ()
		newList.append(heroes)
	return newList
	
drafts = pandas.read_csv('gyro picks.csv')

#drafts['Gyro Won'] = numpy.where(drafts['Winner'] == 'Team A'), 1
drafts['Gyro Won'] = [1 if result == 'Team A' else 0 for result in drafts['Winner']]	

#drafts['Team A Heroes'] = makeHeroPicksList(drafts['Team A Heroes'], heroDict)
#drafts['Team B Heroes'] = makeHeroPicksList(drafts['Team B Heroes'], heroDict)

withIO = drafts.loc[drafts['Team A Heroes'].str.contains('Io')]
noIO = drafts.loc[~drafts['Team A Heroes'].str.contains('Io')]

gyroGames = drafts['Match ID'].count()
gyroWins = drafts['Gyro Won'].sum()

gamesWithIo = withIO['Match ID'].count()
winsWithIo = withIO['Gyro Won'].sum()

gamesWithoutIo = noIO['Match ID'].count()
winsWithoutIo = noIO['Gyro Won'].sum()


results = pandas.DataFrame({'Name': ['Gyro Games', 'With Io', 'Without Io'], 'Games': [gyroGames, gamesWithIo, gamesWithoutIo], 'Wins': [gyroWins, winsWithIo, winsWithoutIo]})

def getGyroDetailsByTeam(teamList, pickedBy=True):
	team = []
	picks = []
	picksWithIo = []
	picksWithoutIo = []
	wins = []
	winsWithIo = []
	winsWithoutIo = []
	
	column = 'Team A'
	name = 'Picked By'
	columns = ['Picked By', 'Picks', 'Wins', 'Picks w/ Io', 'Wins w/ Io', 'Picks w/out Io', 'Wins w/out Io']
	if not pickedBy:
		column = 'Team B' 
		name = 'Picked Against'
		columns = ['Picked Against', 'Picks', 'Wins', 'Picks w/ Io', 'Wins w/ Io', 'Picks w/out Io', 'Wins w/out Io']
	

	for each in teamList:
		team.append(each)
		picks.append(drafts.loc[drafts[column] == each]['Gyro Won'].count())
		wins.append(drafts.loc[drafts[column] == each]['Gyro Won'].sum())
		
		picksWithIo.append(withIO.loc[withIO[column] == each]['Gyro Won'].count())
		winsWithIo.append(withIO.loc[withIO[column] == each]['Gyro Won'].sum())
		
		picksWithoutIo.append(noIO.loc[noIO[column] == each]['Gyro Won'].count())
		winsWithoutIo.append(noIO.loc[noIO[column] == each]['Gyro Won'].sum())
	
	teamPicks = {name: teamList, 'Picks': picks, 'Wins': wins, 'Picks w/ Io': picksWithIo, 'Wins w/ Io': winsWithIo, 'Picks w/out Io': picksWithoutIo, 'Wins w/out Io': winsWithoutIo}
	df = (pandas.DataFrame(teamPicks).sort_values(by=['Picks', 'Wins'], ascending=[False, False])[columns])
	print (df)
	print (df['Picks'].sum())
	
getGyroDetailsByTeam(drafts['Team A'].unique())
print ()
getGyroDetailsByTeam(drafts['Team B'].unique(), pickedBy=False)
