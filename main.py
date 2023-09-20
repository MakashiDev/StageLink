from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import json
import cv2

from Agents.cameraAgent import CameraAgent
from Agents.showAgent import ShowAgent


app = Flask(__name__,
            static_folder='public',
            template_folder='templates'
            )
socketio = SocketIO(app)

cameraAgent = CameraAgent()
cameraAgent.app_context = app.app_context()
show = ShowAgent()

currentShow = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.css')
def index_css():
    return Response(render_template('index.css'), mimetype='text/css')


@app.route("/validate")
def validate():
    return render_template('validate.html')


@app.route("/show/<show_slug>")
def show_page(show_slug):
    return render_template('show.html', show_slug=show_slug)


@app.route("/showold/<show_slug>")
def show_old_page(show_slug):
    return render_template('show_old.html', show_slug=show_slug)


@app.route('/api/show/<show_slug>')
def showHTML(show_slug):
    print(show_slug)
    show.select(show_slug)

    # return json.dumps(show)
    return show.show


@app.route('/api/show/<show_slug>/start')
def startShow(show_slug):
    print(show_slug)
    show.select(show_slug)

    # return json.dumps(show)
    return show.show


@app.route('/api/shows')
def showList():
    print("Getting shows")
    shows = show.load()
    return json.dumps(shows)


@socketio.on('get/shows')
def get_shows():
    list = showList()
    emit('return/shows', list)


# ? Show stuff

@socketio.on('select/show')
def select_show(show_slug):
    print("Selecting show: " + show_slug)
    show.select(show_slug)
    emit('return/show', show.show)


@app.route('/select/show/<show_slug>')
def select_show_page(show_slug):
    print("Selecting show: " + show_slug)
    try:
        show.select(show_slug)
        return json.dumps(show.show)
    except show.ShowNotFound as e:
        print(e)
        return e.message, 404


# ? Camera stuff

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=5000)
