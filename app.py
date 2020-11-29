from flask import Flask, render_template
import subprocess

app = Flask(__name__)


def getSessions():
    files = subprocess.getoutput("ls /Users/armaankapoor/Public/MoteOutput").split()
    sessions = []
    for i in range(len(files)):
        #all sessions have at least one node
        if(files[i].split("_")[3][0] == "1"):
            sessions.append(int(files[i].split("_")[1]))
    return sessions

@app.route('/session/<num>')
def getSessionData(num=None):
    return render_template("session.html", sess=num)

@app.route('/', methods=['GET'])
def getIndex():
    return render_template("index.html", sessions=getSessions())


if __name__ == '__main__':
    app.run()
