import subprocess
import os
import sys
import re

#get the sessions and files
files = subprocess.getoutput("ls /Users/armaankapoor/Public/MoteOutput/Session_*").split()

sessions = []
# {
#     "session":,
#     "nodes": [],
#     "data": []
# }
for i in range(len(files)):
    #all sessions have at least one node
    nodeID = files[i].split("_")[3][0]
    if(nodeID == "1"):
        sessionNum = int(files[i].split("_")[1])
        sessions.append({
            "session": sessionNum,
            "nodes": []
        })
    sessions[-1]['nodes'].append(nodeID)

for i in range(len(files)):
    outputFile = os.path.join(sys.path[0], "static/" + "Session_" + "_".join(files[i].split("_")[1:]))
    # print(outputFile)
    #
    with open(outputFile, 'w') as outF, open(files[i], 'r') as inF:
        for line in inF:
            if(len(line.split(",")) == 4 and line[0].isdigit()):
                timeAndData = line.split("--")
                valid = True
                lineToWrite = ""
                # add the time
                lineToWrite += timeAndData[0] + " "

                # testing
                # if("1606604959.37" == timeAndData[0]):
                #     print("Before: " + line)

                #extract all numbers from data
                data = timeAndData[1].split(",")
                for i in range(len(data)):
                    #data[i] = each data point
                    for num in data[i]:
                        try:
                            lineToWrite += str(int(num))
                        except:
                            pass
                    lineToWrite += ","
                lineToWrite = lineToWrite[:-1]
                # testing
                # if ("1606604959.37" == timeAndData[0]):
                #     print("After: " + lineToWrite)
                tempStr = lineToWrite.split(',')
                if('' not in tempStr and not re.match("^[0-9 ]+$", lineToWrite) and tempStr[1] != tempStr[2] and len(lineToWrite.split(' ')) == 2):
                    outF.write(lineToWrite + "\n")

# print(sessions)
