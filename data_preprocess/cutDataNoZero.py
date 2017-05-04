#delete users who rating = 0 
import json
def cutDataNoZero(input_filename, output_filename,lines):
    '''
        to eliminate the rating with 0 from trainOut dataset
    '''
    with open(input_filename, 'r') as f:
        for i in range(lines):
            curlist = []
            curUserReview = json.loads(f.readline())
            for j in range (len(curUserReview['ratings'])):
                if int(curUserReview['ratings'][j]['rating']) != 0:
                    curlist.append(curUserReview['ratings'][j])
            if len(curlist)==0:
                continue
            curUserReview['ratings'] = curlist
            with open (output_filename,'a') as wf:
                json.dump(curUserReview,wf)
                wf.write('\n')
                
cutDataNoZero('trainOut1w.json', 'trainOutNoZero1w.json',10000)