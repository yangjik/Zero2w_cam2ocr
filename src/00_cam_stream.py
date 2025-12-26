from picamera2 import Picamera2, Preview
from flask import Flask, Response
import cv2, time

img_w = 1920
img_h = 1080

app = Flask(__name__)

# 카메라 초기화
# 해상도랑, 포멧만 가능
pi_camv2 = Picamera2()
cam_config= pi_camv2.create_preview_configuration(
    main={"size" : (img_w, img_h),
          "format" : "YUV420"
    }
)

pi_camv2.configure(cam_config)
pi_camv2.start()

# 공식문서에서 start 하고 2초 기다림
time.sleep(2)

# 카메라 동작 하고 1프레임만 저장
try:
    pi_camv2.capture_file("./test.jpg")
    print("capture success!!!\n")
except Exception as e:
    print("capture fail!!!!!\n", e)

pi_camv2.stop_preview()
pi_camv2.stop()