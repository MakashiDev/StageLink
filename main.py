from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import json
import base64
import cv2

from Agents.cameraAgent import CameraAgent
from Agents.cueAgent import CueAgent
from Agents.showAgent import ShowAgent


app = Flask(__name__)
socketio = SocketIO(app)

cameraAgent = CameraAgent(0)
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


def gen_frames():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FPS, 30)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame = cv2.resize(frame, (462, 220))
            ret, buffer = cv2.imencode(
                '.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/camera_feed')
def camera_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('connect')
def on_connect():
    print('Client connected')

# Camera feed


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=5000)
