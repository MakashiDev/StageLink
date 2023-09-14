from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import json
import cv2

from Agents.cameraAgent import CameraAgent
from Agents.showAgent import ShowAgent


app = Flask(__name__)
socketio = SocketIO(app)

cameraAgent = CameraAgent()
cameraAgent.app_context = app.app_context()
showAgent = ShowAgent()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.css')
def index_css():
    return Response(render_template('index.css'), mimetype='text/css')


@app.route("/show/<show_id>")
def show_page(show_id):
    return render_template('show.html', show_id=show_id)


@app.route('/api/shows/<show_id>')
def show(show_id):
    print(show_id)
    show = showAgent.select_show(show_id)
    showAgent.cues.set_show_id(show_id)
    print(show)
    # return json.dumps(show)
    return json.dumps(show)


@app.route('/api/shows')
def shows():
    shows = showAgent.shows
    return json.dumps({"shows": shows})


@app.route('/api/shows/<show_id>/cues')
def cues(show_id):
    cues = showAgent.cues.get_list()
    return json.dumps(cues)


@app.route('/api/shows/<show_id>/cues/<cue_id>')
def cue(show_id, cue_id):
    cue = showAgent.cues.get(cue_id)
    return json.dumps(cue)


@app.route('/api/shows/<show_id>/cues/next')
def next_cue(show_id, cue_id):
    showAgent.cues.next()
    return json.dumps(showAgent.cues.get_current())


@app.route('/api/shows/<show_id>/cues/previous')
def previous_cue(show_id, cue_id):
    showAgent.cues.previous()
    return json.dumps(showAgent.cues.get_current())


@app.route('/api/shows/<show_id>/start')
def start_show(show_id):
    return json.dumps(showAgent.start_show(show_id))


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
