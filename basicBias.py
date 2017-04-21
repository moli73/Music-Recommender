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

#check basic model RMSE
count = 0
squareSum = 0
for review in testDatas:
    userID = review['userID']
    for rating in review['ratings']:
        itemID = rating['itemID']
        realRating = float(rating['rating'])
        count += 1
        if itemID in itemBiases:
            squareSum += (aveRate + userBiases[userID] + itemBiases[itemID] - realRating) ** 2
        #if the current item does not exist in train data, the bias is zero
        else:
            squareSum += (aveRate + userBiases[userID] + 0 - realRating) ** 2

RMSE = sqrt(squareSum / float(count))
print('the basic model RMSE is: ' + str(RMSE))
print('the number of test reviews in test data is: ' + str(count))
