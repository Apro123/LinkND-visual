from flask import Flask, render_template, Response
import subprocess
import json
from datetime import datetime
from time import sleep
import os

app = Flask(__name__)

files = subprocess.getoutput("ls /Users/armaankapoor/Public/MoteOutput").split()

@app.route('/getInterval/<min>/<max>/', methods=['GET'])
def interval(min, max):
    min = int(min)
    max = int(max)
    # print(min)
    # print(max)
    tsdata = [] # { from:  to: node, data: [timestamp, link]
    for i in range(len(files)):
        # try:
            with open("/Users/armaankapoor/Public/MoteOutput/"+files[i], "r") as f:
                for line in f.readlines():
                    try:
                        date = int(float(line.split(" ")[0]) * 1000)
                    except:
                        date = 0

                    if(date != 0):
                        if(date >= min and date <= max):
                            restOfData = line.split(" ")[1].split(",")

                            found = False
                            for j in range(len(tsdata)):
                                if(int(tsdata[j]['from']) == int(restOfData[1]) and int(tsdata[j]['to']) == int(restOfData[2])):
                                    tsdata[j]['data'].append([date, int(restOfData[3].strip())])
                                    found = True
                            if(not found):
                                tsdata.append({"from": int(restOfData[1]), "to": int(restOfData[2]), "data": [[date, int(restOfData[3].strip())]]})
                            # tsdata.append([date, int(restOfData[1]), int(restOfData[2]), int(restOfData[3].strip())])
                        elif(date > max):
                            break
        # except:
        #     pass
    return Response(json.dumps(tsdata), content_type='application/json')

@app.route('/getMinDate', methods=['GET'])
def minDate():
    minDt = 9999999999999
    for i in range(len(files)):
        try:
            with open("/Users/armaankapoor/Public/MoteOutput/"+files[i], "r") as f:
                date = float(f.readline().split(" ")[0]) * 1000
                if(i == 0 or (date != 0 and minDt > date)):
                    minDt = date
        except:
            pass
    return Response(str(minDt), content_type='application/json')

@app.route('/stream', methods=['GET'])
def getDataStream():
    def stream():
        fileDes = []
        for i in range(len(files)):
            file = open("/Users/armaankapoor/Public/MoteOutput/"+files[i], "r")
            file.seek(0, 2)
            try:
                file.seek(file.tell() - 24 * 500, os.SEEK_SET)
            except:
                file.seek(0)
            fileDes.append(file)
        while True:
            dataToReturn = ""
            for f in fileDes:
                data = f.readline()
                if(data != ""):
                    dataToReturn += data
            yield dataToReturn
    return Response(stream(), content_type='application/json')

@app.route('/', methods=['GET'])
def getIndex():
    # file = open("/Users/armaankapoor/Public/MoteOutput/Node_4.txt", 'r')
    # print("-~-")
    # file.seek(0,2)
    # try:
    #     file.seek(file.tell() - 24*500, os.SEEK_SET)
    # except:
    #     file.seek(0)
    # print(file.readlines())
    # print("---")
    # return "4"
    return render_template("index.html")


#print(os.stat("/Users/armaankapoor/Public/MoteOutput/Node_4.txt").st_size/24); #number of lines

if __name__ == '__main__':
    app.run(debug=True)
