from flask import Flask, render_template, Response
from flask import request, redirect, make_response, send_file
from flask_socketio import SocketIO, emit
import cv2
import random
import string
import base64

app = Flask(__name__)
socketio = SocketIO(app)

global pin
global currentUsers
global cameraindex
global reloadVideo

reloadVideo = False
pin=6969
cameraindex = 0 
currentUsers = {}


messages = []
            

# Define a function to generate a random session ID
def randomSessionId():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))

# Define the route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the user's email and password from the form
        user = request.form['email']
        pin = request.form['password']

        # Check if the password is correct
        if pin == pin:
            print("client is attempting to connect")
            # Create a response object and set the username and session ID cookies
            resp = make_response(redirect('/dashboard'))
            resp.set_cookie('username', user)
            sessionId = randomSessionId()
            resp.set_cookie("sessionID", sessionId)

           # Add the user to the currentUsers dictionary
            currentUsers[user] = sessionId
           

            # Return the response object to redirect to the dashboard
            return resp

        else:
            # If the password is incorrect, render the login page with an error message
            return render_template('login.html', error="unauthorized")
    else:
        # If the request method is GET, render the login page
        return render_template('login.html')
    
def video_stream():
    # Get the camera feed
    camera = cv2.VideoCapture(cameraindex)
    
    camera.set(cv2.CAP_PROP_FPS, 30) # Set FPS value to 30
    while True:
        # Read a frame from the camera and resize it to 720p resolution
        ret, frame = camera.read()
        frame = cv2.resize(frame, (462, 220))

        # Convert the resized frame to a JPEG image with reduced quality
        ret, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

        # Convert the JPEG image to a base64 encoded string
        base64_data = base64.b64encode(jpeg.tobytes())
        base64_string = base64_data.decode('utf-8')

        socketio.emit("video", {"image": base64_string})





# Define the route for the dashboard page
@app.route('/dashboard')
def dashboard():
    # Check if the user is authorized to access the dashboard
    if request.cookies.get('username') in currentUsers:
        user = request.cookies.get('username')
        print(f" giving {user} dashboard")
        

        # Render the dashboard template with the user's username
        return render_template('dashboard.html', username=user)
    else:
        # If the user is not authorized, redirect to the login page
        return redirect('/')
    

@app.route("/admin")
def admin():
    return render_template("admin.html", users=currentUsers, pin=pin, cameraindex=cameraindex)


# Define the socket event for standby mode
@socketio.on('standbye')
def go_mode():
    socketio.emit("standbye")
    print("standbye")
# Define the socket event for go mode
@socketio.on('go')
def go_mode():
    socketio.emit("go")
    print("go")
        
# Define the socket event for when user conncets to video stream
@socketio.on('connect')
def connect():
    print("user conneted")
    socketio.emit("newUser", {"users": currentUsers})
# Listen for client to reqesut video stream

@socketio.on("disconnect")
def disconnect():
    print("user disconnected")
    currentUsers.pop(request.cookies.get('username'))
    socketio.emit("newUser", {"users": currentUsers})

videoStarted = False
reloadVideo = False
@socketio.on("reuqestVideo")
def requestVideo(data):
    global videoStarted
    global reloadVideo
    if reloadVideo == True:
        reloadVideo = False
        videoStarted = False
    if videoStarted == False:
        videoStarted = True
        print(data)
        print("video requested")
        socketio.start_background_task(video_stream)
    else:
        print("video already started")

socketio.on("reload")
def reload():
    global reloadVideo
    reloadVideo = True


@socketio.on("changePin")
def changePin(data):
    print(data)
    pin = data["pin"]
    print(pin)


# when /socket.io.min.js is requested return the file soccket.io.min,js
@app.route('/socketJS')
def send_socketio():
    return send_file('socket.io.min.js', mimetype='text/javascript')


        
     





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
