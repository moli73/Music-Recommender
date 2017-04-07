import sys
def __album__preprocess__(input_filename, output_filename):
    '''
        This function is to split the album data into JSON file
        The inputfile should in same directory of the python script    
        python items_preprocess.py input_filename output_filename
    '''
    import re
    import json
    data = []
    with open(input_filename, 'r') as f:
        for line in f:
            curAlbum = {}#the information of current album
            albumRecord = re.split('\||\n', line)
            if '' in albumRecord:
                albumRecord.remove('')
            curAlbum['albumID'] = albumRecord[0]
            curAlbum['artistID'] = albumRecord[1]
            genreList = []
            for i in range(2, len(albumRecord)):
                genreList.append(albumRecord[i])
            curAlbum['genreList'] = genreList
            data.append(curAlbum.copy())
    with open(output_filename, 'w') as wf:
        json.dump(data, wf)
#test albumData preprocess
#__album__preprocess__("testAlbumIn.txt", "testAlbumOut.txt")
__album__preprocess__(sys.argv[1], sys.argv[2])
