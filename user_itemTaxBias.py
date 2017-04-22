import json
from math import sqrt

def readData(filename, list):
	with open(filename, 'r') as f:
		for line in f:
			list.append(json.loads(line))

#load the trainning data
trainDatas = []
# readData('data_preprocess/trainOut2w.json', trainDatas)
readData('data_preprocess/trainOut1w.json', trainDatas)
print("the number of users in trainning data is:" + str(len(trainDatas)) + "\n")
#print(trainDatas[0])

#construct the dict by itemID
trainReviews = {}#improve the speed of finding
for review in trainDatas:
    for rating in review["ratings"]:
        itemID = rating["itemID"]
        if itemID in trainReviews:
            trainReviews[itemID].append(rating)
        else:
            trainReviews[itemID] = [rating]
print('the number of distinct items is: ' + str(len(trainReviews)))

#load the test data
testDatas = []
# readData('data_preprocess/testOut2w.json', testDatas)
readData('data_preprocess/testOut1w.json', testDatas)
print("the number of users in test data is:" + str(len(testDatas)) + "\n")
#print(testDatas[0])

#the average of all rating
aveRate = 0
count = 0
for review in trainDatas:
    for rating in review["ratings"]:
        aveRate += int(rating["rating"])
        count += 1
aveRate /= float(count)
print('the overall average rating is: ' + str(aveRate))

def itemBias(itemID, aveRating):

    #    use the trainReviews(dict) which is sorted by itemId

    numRating = 0
    sumRating = 0
    if itemID in trainReviews:
        for rating in trainReviews[itemID]:
            numRating += 1
            sumRating += float(rating['rating'])
    else:#if there is no such itemID's rating the itemBias is zero
        return 0
    return sumRating / float(numRating) - aveRating

def userBias(userID, aveRating):

    #    use the trainOut format to find the userBias

    numRating = 0
    sumRating = 0
    for review in trainDatas:
        if review['userID'] == userID:
            for rating in review["ratings"]:
                numRating += 1
                sumRating += float(rating['rating'])
            break#if get the user info then stop the loop
    if numRating == 0:
        return 0
    return sumRating / float(numRating) - aveRating

#get the user bias matrix from train data
userBiases = {}
for review in trainDatas:
	userID = review['userID']
	userBiases[userID] = userBias(userID, aveRate)
print('the number of users is: ' + str(len(userBiases)))

#get the item bias matrix from train data
itemBiases = {}
for itemID in trainReviews:
    itemBiases[itemID] = itemBias(itemID, aveRate)
print('the number of items is: ' + str(len(itemBiases)))

#===============================================taxonomy method
#read the 4 type's all ID
def readIDData(filename):
	list = []
	with open(filename, 'r') as f:
		for line in f:
			list.append(line[:-1])#eliminate the newline character
	return list
#use add taxonomy bias
trackList = readIDData('data_preprocess/track_out_idOnly.txt')
artistList = readIDData('data_preprocess/artistData1.txt')
albumList = readIDData('data_preprocess/album_out_idOnly.txt')
genreList = readIDData('data_preprocess/genreData1.txt')

print('the length of track list is:' + str(len(trackList)))
print('the length of artistList is:' + str(len(artistList)))
print('the length of albumList is:' + str(len(albumList)))
print('the length of genreList is:' + str(len(genreList)))
#print(len(genreList[0]))

##
#  extract the items biases with different types from the partial trainData
##
#extract the track bias
trackBiases = {}
for itemID in trackList:
	if itemID in trainReviews:
		sumRating = 0
		numRating = 0
		for rating in trainReviews[itemID]:
			sumRating += float(rating['rating'])
			numRating += 1
		trackBiases[itemID] = float(sumRating) / float(numRating) - aveRate
	else:
		trackBiases[itemID] = 0
print('the size of trackBiases is: ' + str(len(trackBiases)))

#extract the album bias
albumBiases = {}
for itemID in albumList:
	if itemID in trainReviews:
		sumRating = 0
		numRating = 0
		for rating in trainReviews[itemID]:
			sumRating += float(rating['rating'])
			numRating += 1
		albumBiases[itemID] = float(sumRating) / float(numRating) - aveRate
	else:
		albumBiases[itemID] = 0
print('the size of albumBiases is: ' + str(len(albumBiases)))

#extract the artist bias
artistBiases = {}
for itemID in artistList:
	if itemID in trainReviews:
		sumRating = 0
		numRating = 0
		for rating in trainReviews[itemID]:
			sumRating += float(rating['rating'])
			numRating += 1
		artistBiases[itemID] = float(sumRating) / float(numRating) - aveRate
	else:
		artistBiases[itemID] = 0
print('the size of artistBiases is: ' + str(len(artistBiases)))

#extract the genre bias
genreBiases = {}
for itemID in genreList:
	if itemID in trainReviews:
		sumRating = 0
		numRating = 0
		for rating in trainReviews[itemID]:
			sumRating += float(rating['rating'])
			numRating += 1
		genreBiases[itemID] = float(sumRating) / float(numRating) - aveRate
	else:
		genreBiases[itemID] = 0
print('the size of genreBiases is: ' + str(len(genreBiases)))

#read the tracks
trackDatas = []
readData('data_preprocess/trackOut.json', trackDatas)
print('the size of track is: ' + str(len(trackDatas)))
# print(trackDatas[0])

#construct the dict by trackID
trackDict = {}
for track in trackDatas:
    trackDict[track['trackID']] = track
print('the number of tracks is: ' + str(len(trackDict)))
# print(trackDict['0'])

#expand the track bias
def getTaxTrackBias(itemID):
    if itemID in trackBiases:#should check this, since not all track in this partial train data
        bi = trackBiases[itemID]
    else:
        return 0

    genreRateSum = 0
    genreNum = 0
    biGenre = 0
    biAlbum = 0
    biArtist = 0

    track = trackDict[itemID]
    if track["albumID"] in albumBiases:
        #assume that the track only belong to exactly one album
        biAlbum = albumBiases[track["albumID"]]

    if track['artistID'] in artistBiases:
        #assume that the track only belong to exactly one artist
        biArtist = artistBiases[track["artistID"]]

    for genreID in track['genreList']:
        if genreID in genreBiases:
            genreRateSum += genreBiases[genreID]
            genreNum += 1
        if genreNum != 0:
            biGenre = float(genreRateSum) / float(genreNum)

    taxTrackBias = bi + biAlbum + biArtist + biGenre

    return taxTrackBias

#pre-build the trackTaxBiases
trackTaxBiases = {}
for itemID in trainReviews:
    if itemID in trackBiases:
        trackTaxBiases[itemID] = getTaxTrackBias(itemID)
print('the size of track tax biases is: ' + str(len(trackTaxBiases)))
# print(trackTaxBiases['0'])

#read the albums
albumDatas = []
readData('data_preprocess/albumOut.json', albumDatas)
print('the size of album is: ' + str(len(albumDatas)))
# print(albumDatas[0])

#construct the dict by albumID
albumDict = {}
for album in albumDatas:
    albumDict[album['albumID']] = album
print('the number of albums is: ' + str(len(albumDict)))
# print(albumDict['9'])

#expand the album bias
def getTaxAlbumBias(itemID):
    if itemID in albumBiases:#should check this, since not all album in this partial data
		bi = albumBiases[itemID]
    else:
		return 0

    genreRateSum = 0
    genreNum = 0
    biGenre = 0
    biArtist = 0

    album = albumDict[itemID]
    if album['artistID'] in artistBiases:
        #assume that the album only belong to exactly one artist
        biArtist = artistBiases[album["artistID"]]

    for genreID in album['genreList']:
        if genreID in genreBiases:
            genreRateSum += genreBiases[genreID]
            genreNum += 1
        if genreNum != 0:
            biGenre = float(genreRateSum) / float(genreNum)

    taxAlbumBias = bi + biArtist + biGenre
    return taxAlbumBias

#pre-build the albumTaxBiases
albumTaxBiases = {}
for itemID in trainReviews:
    if itemID in albumBiases:
        albumTaxBiases[itemID] = getTaxAlbumBias(itemID)
print('the size of album tax biases is: ' + str(len(albumTaxBiases)))
# print(albumTaxBiases['9'])

def userTaxBias(userID):
    bu = userBiases[userID]
    #initalized by basic user bias 
    userTaxBiases = {'track':bu,'album':bu,'artist':bu,'genre':bu}
    numTrackRate = 0
    numAlbumRate = 0
    numArtistRate = 0
    numGenreRate = 0

    sumTrackRate = 0
    sumAlbumRate = 0
    sumArtistRate = 0
    sumGenreRate = 0

    review = trainDatas[int(userID)]#since the ID of users is continuous
    for rating in review['ratings']:
        itemID = rating['itemID']
        score = float(rating['rating'])
        if itemID in trackBiases:
            sumTrackRate += score
            numTrackRate += 1
        elif itemID in albumBiases:
            sumAlbumRate += score
            numAlbumRate += 1
        elif itemID in artistBiases:
            sumArtistRate += score
            numArtistRate += 1
        elif itemID in genreBiases:
            sumGenreRate += score
            numGenreRate += 1
    if numTrackRate != 0:
        userTaxBiases['track'] = sumTrackRate / float(numTrackRate) - aveRate
    if numAlbumRate != 0:
        userTaxBiases['album'] = sumAlbumRate / float(numAlbumRate) - aveRate
    if numArtistRate != 0:
        userTaxBiases['artist'] = sumArtistRate / float(numArtistRate) - aveRate
    if numGenreRate != 0:
        userTaxBiases['genre'] = sumGenreRate / float(numGenreRate) - aveRate

    return userTaxBiases

#pre-build the tax user biases
userTaxBiases = {}
for review in trainDatas:
    userID = review['userID']
    userTaxBiases[userID] = userTaxBias(userID)
print('the number of users in train data is: ' + str(len(userTaxBiases)))
# print(userTaxBiases['0'])

#check the RMSE with full taxonomy bias model
count = 0
squareSum = 0
for review in testDatas:
    userID = review['userID']
    for rating in review['ratings']:
        itemID = rating['itemID']
        realRating = float(rating['rating'])
        count += 1
        if itemID in itemBiases:
            if itemID in trackBiases:
                curItemBias = trackTaxBiases[itemID]
                curUserBias = userTaxBiases[userID]['track']
            elif itemID in albumBiases:
                curItemBias = albumTaxBiases[itemID]
                curUserBias = userTaxBiases[userID]['album']
            else:
                if itemID in artistBiases:
                    curUserBias = userTaxBiases[userID]['artist']
                elif itemID in genreBiases:
                    curUserBias = userTaxBiases[userID]['genre']
                curItemBias = itemBiases[itemID]
        #if the current item does not exist in train data, the bias is zero
        else:
            curItemBias = 0
        squareSum += (aveRate + curItemBias + curUserBias - realRating) ** 2
#         squareSum += (aveRate + userBiases[userID] + curItemBias + curUserBias - realRating) ** 2


RMSE = sqrt(squareSum / float(count))
print('the full taxonomy model RMSE is: ' + str(RMSE))
print('the number of reviews in test data is: ' + str(count))
