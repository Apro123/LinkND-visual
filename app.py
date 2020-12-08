from flask import Flask, render_template
import subprocess
import json

app = Flask(__name__)

def getSessions():
    files = subprocess.getoutput("ls /Users/armaankapoor/Public/MoteOutput").split()
    sessions = {}
    for i in range(len(files)):
        #all sessions have at least one node
        if(files[i].split("_")[3][0] == "1"):
            sessions[(int(files[i].split("_")[1]))] = 1
        else:
            sessions[(int(files[i].split("_")[1]))] += 1
    return sessions

def getSessionData(sessNum):
    data = [
        # {nodeNumber: 3,
        # data: ["time 1,2,3,4", "time 1,2,3,4", etc...]}
    ]
    #
    for i in range(sessions[int(sessNum)]):
        with open("static/Session_" + sessNum + "_Node_" + str(i+1) + ".txt") as f:
            data.append({"node": i+1, "data": f.readlines()})
    return data

sessions = getSessions()

@app.route('/session/<sessNum>', methods=['GET'])
def getSession(sessNum=None):
    #serve static processed data files
    d = getSessionData(sessNum)
    return render_template("session.html", sess=sessNum, data=json.dumps(d))

@app.route('/', methods=['GET'])
def getIndex():
    return render_template("index.html", sessions=sessions)


if __name__ == '__main__':
    app.run(debug=True)
