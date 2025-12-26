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

pi_camv2.capture_file("./test.jpg")