from picamera2 import Picamera2
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
            }
        )

        picam2.configure(config)

        print("[Cam Setting] Pi camera V2 Setting Success..\n")
        picam2.start()
        time.sleep(2)
        return picam2
    
    except Exception as err:
        print("[Cam Setting] Pi camera V2 Setting Fail..\n")

def cam_streaming(picam2):
    while True:
        # 데이터는 ram
        data = io.BytesIO()
        
        # 데이터 압축은 cpu
        picam2.capture_file(data, format=img_format, quality=img_quality)

        


@app.route('/')
def home():
    return 'Raspberry Pi Zero2w'

@app.route('/stream')
def stream():
    return Response(cam_streaming(picam2), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    picam2 = cam_setting()

    # if 