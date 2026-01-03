from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from flask import Flask, Response
import time, cv2, io

img_wdth = 1920
img_height = 1080
img_fps = 30.0
img_format = ['jpeg', 'png', 'bmp', 'gif']
img_format = img_format[0]
img_quality = 95

app = Flask(__name__)

def cam_setting():
    picam2 = Picamera2()

    try:
        config = picam2.create_video_configuration(
            main={
                "size" : (img_wdth, img_height)
            },
            controls={
                "FrameRate" : img_fps
            },
            encode="raw"
        )

        picam2.configure(config)

        print("[Cam Setting] Pi camera V2 Setting Success..\n")
        picam2.start()
        time.sleep(2)
        return picam2
    
    except Exception as err:
        print("[Cam Setting] Pi camera V2 Setting Fail..\n")

def cam_streaming(picam2):
    # 7.1.3. MJPEGEncoder 문서
    encoder = MJPEGEncoder()

    while True:
        picam2.start_recording(encoder)

        


@app.route('/')
def home():
    return 'Raspberry Pi Zero2w'

@app.route('/stream')
def stream():
    return Response(cam_streaming(picam2), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    picam2 = cam_setting()

    # if 