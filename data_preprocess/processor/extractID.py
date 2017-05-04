def extractID(input_filename, output_filename,itemID):
    '''
        extract ID of album and track
    '''
    itemList = []
    with open(input_filename, 'r') as f:
        for line in f:
            itemList.append(json.loads(line))
    
    file_object = open(output_filename, 'w')
    for i in range(len(itemList)):
        ID = itemList[i][itemID]
        file_object.write(ID)
        file_object.write('\n')
    file_object.close()

extractID('albumOut.json','album_out_idOnly.json','albumID') 
extractID('trackOut.json','track_out_idOnly.json','trackID')