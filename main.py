from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import json
import cv2

from Agents.cameraAgent import CameraAgent
from Agents.cueAgent import CueAgent
from Agents.showAgent import ShowAgent


app = Flask(__name__)
socketio = SocketIO(app)

cameraAgent = CameraAgent()
cameraAgent.app_context = app.app_context()
showAgent = ShowAgent()


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/test")
def test():
    return render_template('testing.html')


@app.route('/show/<show_id>')
def show(show_id):
    print(show_id)
    show = showAgent.select_show(show_id)
    print(show)
    # return json.dumps(show)
    return json.dumps(show)


@app.route('/camera_feed/<int:index>')
def camera_feed(index=0):
    return Response(cameraAgent.gen_frames(index), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/default_camera_feed')
def default_camera_feed():
    return Response(cameraAgent.gen_frames(0), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera_feeds')
def camera_feeds():
    cameras = cameraAgent.get_cameras()
    return json.dumps(cameras)


@socketio.on('connect')
def on_connect():
    print('Client connected')

# Camera feed


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=5000)
