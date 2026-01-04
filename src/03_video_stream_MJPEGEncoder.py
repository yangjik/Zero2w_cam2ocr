from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from flask import Flask, Response
import time, cv2, io

img_wdth = 1920
img_height = 1080
img_fps = 30.0
img_format = ['jpeg', 'png', 'bmp', 'gif']
img_format = img_format[0]
img_quality = 90
img_channel = ['XBGR8888',  # 32bit [R, G, B, 255]
               'XRGB8888',  # 32bit [B, G, R, 255]
               'RGB888',    # [B, G, R]
               'BGR888',    # [R, G, B]
               'YUV420'     # YUV420 
               ]
img_channel = img_channel[3]

app = Flask(__name__)

def cam_setting():
    picam2 = Picamera2()

    try:
        config = picam2.create_video_configuration(
            main={
                "size" : (img_wdth, img_height),
                "format" : img_channel
            },
            controls={
                "FrameRate" : img_fps
            },
            encode="main"
        )

        picam2.configure(config)

        print("[Cam Setting] Pi camera V2 Setting Success..\n")
        picam2.start()
        time.sleep(2)
        return picam2
    
    except Exception as err:
        print("[Cam Setting] Pi camera V2 Setting Fail..\n")
        return None
    
def cam_streaming(picam2):
    # 7.1.3. MJPEGEncoder 문서
    encoder = MJPEGEncoder()

    picam2.start_recording(encoder)
    
    try:
        while True:
            frame = encoder.wait_for_frame()
            
            if not frame:
                break

            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
    except Exception as err:
        print(f'[Cam Encoder] MJPEGEncoder fail\n')

    finally:
        picam2.stop_recording()
        print("[Cam Encoder] stop recording : [{err}]\n")

@app.route('/')
def home():
    return '<h1>Raspberry Pi Zero2w</h1>'

@app.route('/stream')
def stream():
    return Response(cam_streaming(picam2), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    picam2 = cam_setting()

    if picam2 != None:
        try:
            app.run(host='0.0.0.0', port=5000, threaded=True)
        finally:
            picam2.stop()
