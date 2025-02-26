import cv2
import base64
from flask_socketio import SocketIO, emit
import os


class CameraAgent:
    """
    This class is responsible for handling the camera feed.

 """

    def gen_frames(self, index=0):
        import psutil
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

        camera.set(cv2.CAP_PROP_FPS, 30)
        while True:
            success, frame = camera.read()  # read the camera frame
            if not success:
                print("Failed to access camera feed!")
                break
            else:
                battery = psutil.sensors_battery()
                # Optimize frame size for better performance while maintaining quality
                frame = cv2.resize(frame, (854, 480))
                from PIL import ImageFont, ImageDraw, Image
                import numpy as np

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_im = Image.fromarray(frame)
                draw = ImageDraw.Draw(pil_im)
                font = ImageFont.truetype("../Arial.ttf", 18)

                # Battery status with optimized text rendering
                battery_text = f"{battery.percent}% Charging" if battery.power_plugged else f"{battery.percent}%"
                battery_color = (0, 255, 0) if battery.power_plugged else (255, 0, 0) if battery.percent < 20 else (255, 255, 255)
                draw.text((10, 10), battery_text, battery_color, font=font, stroke_width=1, stroke_fill=(0, 0, 0))

                # Time display
                import datetime
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                draw.text((10, 30), time, (255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))

                # Add show name and creator credit
                draw.text((10, 50), "Matilda", (255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
                draw.text((frame.shape[1] - 200, frame.shape[0] - 30), "Made by Christian Furr", (255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
                frame = np.array(pil_im)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
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
