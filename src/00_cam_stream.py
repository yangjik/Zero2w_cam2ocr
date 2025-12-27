from picamera2 import Picamera2, Preview
from flask import Flask, Response
import cv2, time

img_w = 1920
img_h = 1080
img_format = ['YUV420',     #  YUV images with a plane of Y values followed by a quarter plane of U values and then a quarter plane of V values.
              'XBGR8888',   # every pixel is packed into 32-bits, with a dummy 255 value at the end, so a pixel would look like [R, G, B, 255] when captured in Python.
              'XRGB8888',   # as above, with a pixel looking like [B, G, R, 255]
              'RGB888',     # 24 bits per pixel, ordered [B, G, R].
              'BGR888'      # as above, but ordered [R, G, B].
              ]

img_format = img_format[3]

current_stream = False

app = Flask(__name__)

# 카메라 초기화
# 해상도랑, 포멧만 가능
def cam_setting():
    pi_camv2 = Picamera2()
    cam_config= pi_camv2.create_preview_configuration(
        main={"size" : (img_w, img_h),
            "format" : img_format
        }
    )
    try:
        pi_camv2.configure(cam_config)
        print(f"[cam setting] current image width, height : [{img_w}, {img_h}] / image format : [{img_format}]\n")
    except Exception as e:
        print('[cam setting] camera setting error : [{e}]\n')
    pi_camv2.start()
    # 공식문서에서 start 하고 2초 기다림
    time.sleep(2)

    return pi_camv2

def cam_setting_after(pi_camv2):
    # 카메라 동작 하고 1프레임만 저장
    try:
        pi_camv2.capture_file("./test.jpg")
        print("capture success!!!\n")
    except Exception as e:
        print("capture fail!!!!!\n", e)

    pi_camv2.stop_preview()
    pi_camv2.stop()

def cam_streamming(pi_camv2):
    while True:
        frame = pi_camv2.capture_array()

        retval, jpg_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

        frame_byte = jpg_frame.tobytes()

        if not retval:
            print("[Encoding] img encoding fail\n")
        else:
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + 
                frame_byte + b'\r\n')
            
            time.sleep(0.05)


@app.route('/stream')
def stream():
    return Response(cam_streamming(pi_camv2), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    pi_camv2 = cam_setting()

    app.run(host='0.0.0.0', port='8000')

    # 카메라 동작 후 원샷
    # cam_setting_after(pi_camv2)

    # 스트리밍