from flask import Flask, render_template, Response
import subprocess
import json
from datetime import datetime
from time import sleep
import os

app = Flask(__name__)

numFiles = len(subprocess.getoutput("ls /Users/armaankapoor/Public/MoteOutput").split())

@app.route('/stream', methods=['GET'])
def getDataStream():
    def stream():
        fileDes = []
        for i in range(numFiles):
            file = open("/Users/armaankapoor/Public/MoteOutput/Node_" + str(i+1) + ".txt", "r")
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
