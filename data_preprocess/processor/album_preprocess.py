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
            # data.append(curAlbum.copy())
            with open(output_filename, 'a') as wf:
                json.dump(curAlbum, wf)
                wf.write('\n')

__album__preprocess__("albumData1.txt", "albumOut.json")