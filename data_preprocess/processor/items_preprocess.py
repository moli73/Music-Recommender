import sys
def __items__preprocess__(input_filename, output_filename):
    '''
        This function is to split the raw trainning and test rating data JSON file
        The inputfile should in same directory of the python script
		python items_preprocess.py inputfilename outputfilename
    '''
    import re
    import json
    data = []
    userRecord = {}#each user's record of all rating
    with open(input_filename,'r') as f:
        #read the first line
        line = f.readline()
        userRecord["ratings"] = []
        line_split = re.split("\||\n", line)
        if '' in line_split:
            line_split.remove('')
        userRecord['userID'] = line_split[0]
        userRecord['numRating'] = line_split[1]
        for line in f:
            if '|' in line:
                #output the former record
                with open(output_filename, 'a') as wf:
                    json.dump(userRecord.copy(), wf)
                    wf.write("\n")
                userRecord.clear()#clear the former userRating record
                #construct the current record
                userRecord["ratings"] = []
                line_split = re.split("\||\n", line)
                if '' in line_split:
                    line_split.remove('')
                userRecord['userID'] = line_split[0]
                userRecord['numRating'] = line_split[1]
            else:
                line_split = re.split("\t|\n", line)
                if '' in line_split:
                    line_split.remove('')
                curRating = {}#current item rating of current user
                curRating['itemID'] = line_split[0]
                curRating['rating'] = line_split[1]
                curRating['number'] = line_split[2]
                curRating['time'] = line_split[3]
                userRecord["ratings"].append(curRating)
    #store the last user
    with open(output_filename, 'a') as wf:
        json.dump(userRecord.copy(), wf)

__items__preprocess__('trainIdx1.txt', 'trainOut.json')
__items__preprocess__('testIdx1.txt', 'testOut.json')
__items__preprocess__('validationIdx1.txt', 'validationOut.json')
