import cv2
import base64
from flask_socketio import SocketIO, emit
import os


class CameraAgent:
    """ 
    This class is responsible for handling the camera feed.

 """

    def gen_frames(self, index=0):
        """
        This function is responsible for capturing the camera feed and converting it to a base64 encoded string.
        """

        operation_system = os.name
        print(operation_system)  # nt = windows, posix = linux or mac
        if operation_system == "nt":
            print("Windows")
            camera = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        else:
            print("Linux or Mac")
            camera = cv2.VideoCapture(index)

        camera.set(cv2.CAP_PROP_FPS, 60)
        while True:
            success, frame = camera.read()  # read the camera frame
            if not success:
                print("Failed to access camera feed!")
                break
            else:
                frame = cv2.resize(frame, (462, 220))
                ret, buffer = cv2.imencode(
                    '.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

    def get_cameras(self):
        """
        This function is responsible for getting all the available cameras.
        """
        cameras = {}
        for i in range(0, 10):
            operation_system = os.name
            if operation_system == "nt":
                print("Windows")
                camera = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            else:
                print("Linux or Mac")
                camera = cv2.VideoCapture(i)
            if camera.isOpened():
                # get name of camera
                ret, frame = camera.read()
                if ret:
                    cameras[i] = {
                        "name": camera.getBackendName(),
                        "index": i
                    }
                camera.release()

        return cameras
