import json

readFileDict = {}
with open('./cryptos.json','r', encoding="utf-8") as json_File :
    readFileDict=json.load(json_File)

readFileList = readFileDict["values"]
fillDict = {}
for line in readFileList:
    fillDict[line[2]] = int(line[0])
      

with open('./codeToID.json', 'w') as f:
        json.dump(fillDict, f)

