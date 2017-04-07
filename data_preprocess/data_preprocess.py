def __rating__preprocess__(input_filename, output_filename):
    '''
        This function is to split the raw trainning and test rating data JSON file
        The filename should include the full directory.
    '''    
    import re
    import json
    data = []
    userRecord = {}#each user's record of all rating
    with open(input_filename,'r') as f:
        for line in f:
            if '|' in line:
                data.append(userRecord.copy())#append former user record to data collection, use the value passing
                userRecord.clear()#clear the former userRating record
            
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
    data.append(userRecord.copy())
    #remove the first null dict
    data = data[1:]
        
    # for rating  in data:
    #     print(rating)
    
    with open(output_filename, 'w') as wf:
        json.dump(data, wf)
#def test
__rating__preprocess__('raw_data.txt', 'preprocessed_data.txt')
