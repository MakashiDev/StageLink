from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import json

from Agents.cameraAgent import CameraAgent
from Agents.cueAgent import CueAgent
from Agents.showAgent import ShowAgent

sA = ShowAgent()

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show/<show_id>')
def show(show_id):
    print(show_id)
    show = sA.select_show(show_id)
    print(show)
    # return json.dumps(show)
    return json.dumps(show)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=5000)
