import json
def cutData(input_filename, output_filename, lines):
    with open(input_filename, 'r') as f:
        for i in range(lines):
            curUserReview = json.loads(f.readline())
            with open(output_filename, 'a') as wf:
                json.dump(curUserReview, wf)
                wf.write('\n')

# cutData('trainOut.json', 'trainOut2w.json', 20000)
# cutData('testOut.json', 'testOut2w.json', 20000)

cutData('../trainOut.json', '../trainOut3w.json', 30000)
cutData('../testOut.json', '../testOut3w.json', 30000)

cutData('../trainOut.json', '../trainOut6w.json', 60000)
cutData('../testOut.json', '../testOut6w.json', 60000)
