import json
def cutData(input_filename, output_filename, lines):
	with open(input_filename, 'r') as f:
		for i in range(lines):
			curlist = []
			curUserReview = json.loads(f.readline())
			for j in len(curUserReview['ratings']):
				if int(curUserReview['ratings'][j]['rating']) != 0:
					curlist.append(curUserReview['ratings'][j])
			if len(curlist)==0:
				continue
			curUserReview['ratings'] = curlist

			with open(output_filename, 'a') as wf:
				json.dump(curUserReview, wf)
				wf.write('\n')

cutData('trainOut.json', 'trainOut1w.json', 10000)
cutData('testOut.json', 'testOut1w.json', 10000)
