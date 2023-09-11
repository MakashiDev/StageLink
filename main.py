from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import json

from Agents.cameraAgent import CameraAgent
from Agents.cueAgent import CueAgent
from Agents.showAgent import ShowAgent


app = Flask(__name__)
socketio = SocketIO(app)

cameraAgent = CameraAgent(1)
cameraAgent.app_context = app.app_context()
showAgent = ShowAgent()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show/<show_id>')
def show(show_id):
    print(show_id)
    show = showAgent.select_show(show_id)
    print(show)
    # return json.dumps(show)
    return json.dumps(show)


# SocketIO events
@socketio.on('connect')
def on_connect():
    print('Client connected')

# Camera feed


@socketio.on('camera_feed_request')
def on_camera_feed_request():
    cameraAgent = CameraAgent(0)
    cameraAgent.app_context = app.app_context()
    cameraAgent.get_live_camera_feed()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=5000)
