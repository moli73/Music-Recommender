import sys
def __track__preprocess__(input_filename, output_filename):
    '''
        This function is to split the track data into JSON file
        The inputfile should in same directory of the python script
        python items_preprocess.py input_filename output_filename
    '''
    import re
    import json
    with open(input_filename, 'r') as f:
        for line in f:
            curTrack = {}#the information of current track
            trackRecord = re.split('\||\n', line)
            if '' in trackRecord:
                trackRecord.remove('')
            curTrack['trackID'] = trackRecord[0]
            curTrack['albumID'] = trackRecord[1]
            curTrack['artistID'] = trackRecord[2]
            genreList = []
            for i in range(3, len(trackRecord)):
                genreList.append(trackRecord[i])
            curTrack['genreList'] = genreList
            with open(output_filename, 'a') as wf:
                json.dump(curTrack, wf)
                wf.write("\n")

#test trackData preprocess
__track__preprocess__("testTrackIn.txt", "testTrackOut.json")
# __track__preprocess__(sys.argv[1], sys.argv[2])
