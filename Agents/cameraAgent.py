import cv2
import base64
from flask_socketio import SocketIO, emit


class CameraAgent:
    def __init__(self, cameraIndex):
        cameraIndex = cameraIndex

        self.cameraIndex = cameraIndex

    def get_live_camera_feed(self):
        camera = cv2.VideoCapture(self.cameraIndex)
        camera.set(cv2.CAP_PROP_FPS, 30)  # Set FPS value to 30
        while True:
            # Read a frame from the camera and resize it to 720p resolution
            ret, frame = camera.read()
            if frame is None:
                print("No frame")
                continue
            frame = cv2.resize(frame, (462, 220))

            # Convert the resized frame to a JPEG image with reduced quality
            ret, jpeg = cv2.imencode(
                '.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

            # Convert the JPEG image to a base64 encoded string
            base64_data = base64.b64encode(jpeg.tobytes())
            base64_string = base64_data.decode('utf-8')

            # Emit the base64 encoded string to the client
            print("Emitting camera feed")
            emit('camera_feed', base64_string, broadcast=True)
